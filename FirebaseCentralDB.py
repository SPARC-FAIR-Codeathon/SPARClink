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
from backend.pennsieve_metadata import get_list_of_datasets_with_metadata

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

email    = input('Enter email: ')
passw    = input('Enter password: ')
user     = auth.sign_in_with_email_and_password(email, passw)

db = firebase.database()
NN = NIH_NCBI()

def main():
    global user

    # Get all the datasets from Sparc Portal
    sparc_dataset_list = []
    sparc_dataset_list = get_list_of_datasets_with_metadata(sparc_dataset_list)

    disallowed_chars = {ord(c):None for c in "$#[]/. "}

    Timestamp = time.time()

    i = 0
    for dataset in sparc_dataset_list:
        print('Processing dataset: ' + str(i))
        i += 1

        # update the user token if its been more than 30 min
        dt = time.time() - Timestamp
        if (dt > 1800):
            user = auth.refresh(user['refreshToken'])
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
        dataset_pub_records = NN.getPublicationsOfDataset(dataset_record['doi'].split('.org/')[1])
        for k in dataset_pub_records:
            print('--- Processing paper: ' + str(j))
            j += 1

            paper_key = k.translate(disallowed_chars)
            dataset_pub_records[k]['datasets'] = [dataset_key]
            dataset_pub_records[k]['awards']   = []
            dataset_pub_records[k]['papers']   = []

            uploadPaperOrUpdate(paper_key, 'datasets', dataset_pub_records[k])

        # Find the funding awards (NIH) associated with the datasets. Add to award db
        print('- Processing awards')
        award_record = NN.generateRecord(NN.getProjectFundingDetails([ dataset_record['award'] ]))
        db.child(user['localId']).child('Awards').update({dataset_record['award']: award_record}, user['idToken'])

        # Find the papers associated with the award. Upload.
        j = 0
        award_pub = {}
        for k in award_record:
            print('--- Processing paper: ' + str(j))
            j += 1

            sub_award = award_record[k]
            pubs = NN.getPublications(sub_award['appl_id'])
            award_pub.update(pubs)

        j = 0
        for k in award_pub:
            print('--- Processing paper: ' + str(j))
            j += 1

            paper_key = k.translate(disallowed_chars)
            award_pub[k]['datasets'] = []
            award_pub[k]['awards']   = [dataset_record['award']]
            award_pub[k]['papers']   = []

            uploadPaperOrUpdate(paper_key, 'awards', award_pub[k])


    return

#-----------------------------------------------------------------------------------
# uploadPaperOrUpdate:
# Upload the given paper record 'newPaper' to the database if does not exist. If it
# exists, update the field (list) stipulated by 'update_key' (which can be datasets,
# awards, or papers) by appending the values in 'newPaper'.
#-----------------------------------------------------------------------------------
def uploadPaperOrUpdate(paper_key, update_key, newPaper):
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


