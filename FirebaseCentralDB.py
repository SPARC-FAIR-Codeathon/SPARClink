#--------------------------------------------------------------
# FirebaseCentralDB.py
# This script uses the external APIs to query all the datasets and papers associated with them,
# insert add them to a firebase central database.
#
# Author: Sachira Kuruppu
# Date  : 20/07/2021
#--------------------------------------------------------------

import time
import pyrebase

from ExternalAPIs.NIH_NCBI import NIH_NCBI
from backend.metadata_extraction import get_list_of_datasets_with_metadata
#from metadata_extraction import get_list_of_datasets_with_metadata

firebaseConfig = {
    'apiKey': "AIzaSyBZGI1EbzcsoPnplzgBGWYZBF0CHwR4BnY",
    'authDomain': "sparclink-f151d.firebaseapp.com",
    'databaseURL': "https://sparclink-f151d-default-rtdb.firebaseio.com",
    'projectId': "sparclink-f151d",
    'storageBucket': "sparclink-f151d.appspot.com",
    'messagingSenderId': "168500342210",
    'appId': "1:168500342210:web:8675fcd3db2f527916ba5b",
    'measurementId': "G-N1K2EXBDZG"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth     = firebase.auth()

email    = 'aa@aa.com'#input('Enter email: ')
passw    = '123456'#input('Enter password: ')
user     = auth.sign_in_with_email_and_password(email, passw)

db = firebase.database()
NN = NIH_NCBI()

disallowed_chars = {ord(c):None for c in "$#[]/. "}

def main():
    global user

    # Get all the datasets from Sparc Portal
    sparc_dataset_list = []
    sparc_dataset_list = get_list_of_datasets_with_metadata(sparc_dataset_list)

    Timestamp = time.time()

    i = 0
    for dataset in sparc_dataset_list:
        print('Processing dataset: ' + str(i) + ' : ' + dataset['datasetDOI'])
        i += 1

        # update the user token if its been more than 30 min
        dt = time.time() - Timestamp
        if (dt > 1800):
            refreshed_user       = auth.refresh(user['refreshToken'])
            user['idToken']      = refreshed_user['idToken']
            user['refreshToken'] = refreshed_user['refreshToken']
            Timestamp = time.time()

        # Insert the dataset to the database
        dataset_key = dataset['datasetDOI'].translate(disallowed_chars)

        dataset_record                  = {}
        dataset_record['doi']           = dataset['datasetDOI']
        dataset_record['name']          = dataset['name']
        dataset_record['description']   = dataset['description']
        dataset_record['award']         = dataset['properties']['award_id']
        dataset_record['protocols']     = [ p.translate(disallowed_chars) for p in dataset['protocolsDOI'] ]
        dataset_record['tags']          = dataset['tags']

        db.child(user['localId']).child('Datasets').update({dataset_key: dataset_record}, user['idToken'])

        # Find papers associated with the dataset. Upload.
        j = 0
        dataset_pub_records = NN.getPublicationWithSearchTerm('"{0}"'.format(dataset_record['doi'].split('.org/')[1]))
        for k in dataset_pub_records:
            print('--- Processing paper: ' + str(j))
            j += 1

            paper_key = k.translate(disallowed_chars)
            dataset_pub_records[k]['datasets'] = [dataset_key]
            dataset_pub_records[k]['awards']   = []
            dataset_pub_records[k]['papers']   = []
            dataset_pub_records[k]['citations']= 0

            uploadPaperOrUpdate(paper_key, 'datasets', dataset_pub_records[k])

        # Find the funding awards (NIH) associated with the datasets. Add to award db
        print('- Processing awards: ' + str(dataset_record['award']))
        award_record = NN.generateRecord(NN.getProjectFundingDetails([ dataset_record['award'] ]))
        db.child(user['localId']).child('Awards').update({dataset_record['award']: award_record}, user['idToken'])

        # Find the papers associated with the award.
        j = 0
        award_pub = {}
        for k in award_record:
            print('- Processing award: ' + str(j))
            j += 1

            sub_award = award_record[k]
            pubs = NN.getPublications(sub_award['appl_id'])
            award_pub.update(pubs)

        # Upload the award papers
        j = 0
        for k in award_pub:
            print('--- Processing award paper: ' + str(j))
            j += 1

            paper_key = k.translate(disallowed_chars)
            award_pub[k]['datasets'] = []
            award_pub[k]['awards']   = [dataset_record['award']]
            award_pub[k]['papers']   = []
            award_pub[k]['citations']= 0

            uploadPaperOrUpdate(paper_key, 'awards', award_pub[k])

        # Find citations of the papers found above
        uploadCitations(award_pub.update(dataset_pub_records))

    return

#-----------------------------------------------------------------------------------
# uploadCitations:
# Given a set of papers, upload the citations to firebase
#-----------------------------------------------------------------------------------
def uploadCitations (records):
    if records is None:
        print('Error!! records empty.')
        return
    
    for k in records:
        print('---- Looking for citations of: ' + str(k))

        citedby = {}
        if ('pm_id' in records[k]):
            citedby = NN.getCitedBy('pm_id', records[k]['pm_id'])
        elif ('pmc_id' in records[k]):
            citedby = NN.getCitedBy('pm_id', records[k]['pmc_id'])
        
        db.child(user['localId']).child('Papers').child(k.translate(disallowed_chars)).update({'citations': len(citedby)})

        i = 0
        for kk in citedby:
            i += 1
            print('---- Uploading citation ' + str(i) + ' / ' + str(len(citedby)))

            citedby[kk]['datasets'] = []
            citedby[kk]['awards']   = []
            citedby[kk]['papers']   = [k.translate(disallowed_chars)]

            uploadPaperOrUpdate(kk.translate(disallowed_chars), 'papers', citedby[kk])

    return


#-----------------------------------------------------------------------------------
# uploadPaperOrUpdate:
# Upload the given paper record 'newPaper' to the database if does not exist. If it
# exists, update the field (list) stipulated by 'update_key' (which can be datasets,
# awards, or papers) by appending the values in 'newPaper'.
#-----------------------------------------------------------------------------------
def uploadPaperOrUpdate (paper_key, update_key, newPaper):
    # See if the db already has this paper
    pub_data = db.child(user['localId']).child('Papers').child(paper_key).get(user['idToken']).val()
    if pub_data is None:
        # The db does not have this paper
        db.child(user['localId']).child('Papers').update({paper_key: newPaper}, user['idToken'])
    else:
        # The db has this paper. Only update the datasets field
        update_field = pub_data[update_key]
        update_field += newPaper[update_key]
        update_field = set(update_field) # remove duplicates
        db.child(user['localId']).child('Papers').child(paper_key).update({update_key: list(update_field)}, user['idToken'])
    return

if __name__ == '__main__':
    main()


