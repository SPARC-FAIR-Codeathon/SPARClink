#--------------------------------------------------------------
# FirebaseCentralDB.py
# This script uses the external APIs to query all the datasets and papers associated with them,
# insert add them to a firebase central database.
#--------------------------------------------------------------

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

email    = 'nah_ncbi@sparclink.com'#input('Enter email: ')
passw    = '123456'#input('Enter password: ')
user     = auth.sign_in_with_email_and_password(email, passw)

db = firebase.database()
award_db   = firebase.database().child(user['localId']).child('Awards')
dataset_db = firebase.database().child(user['localId']).child('Datasets')
paper_db   = firebase.database().child(user['localId']).child('Papers')

NN = NIH_NCBI()

# Get all the datasets from Sparc Portal
sparc_dataset_list = []
sparc_dataset_list = get_list_of_datasets_with_metadata(sparc_dataset_list)

disallowed_chars = {ord(c):None for c in "$#[]/. "}

for dataset in sparc_dataset_list:
    # Insert the dataset to the database
    dataset_key = dataset['datasetDOI'].translate(disallowed_chars)
    
    dataset_record                  = {}
    dataset_record['doi']           = dataset['datasetDOI']
    dataset_record['name']          = dataset['name']
    dataset_record['description']   = dataset['description']
    dataset_record['project_num']   = dataset['properties']['award_id']
    dataset_record['protocol_dois'] = dataset['protocolsDOI']
    dataset_record['tags']          = dataset['tags']

    db.child(user['localId']).child('Datasets').update({dataset_key: dataset_record}, user['idToken'])

    # Find the funding awards (NIH) associated with the datasets. Add to award db
    award_record              = NN.generateRecord(NN.getProjectFundingDetails([ dataset_record['project_num'] ]))
    db.child(user['localId']).child('Awards').update({dataset_record['project_num']: award_record}, user['idToken'])
    
#    # Find papers associated with the dataset
#    dataset_pub_records = NN.getPublicationsOfDataset(dataset_doi.split('./org')[1])
#    for k in dataset_pub_records:
#        dataset_pub_records[k]['dataset'] = dataset_doi
#    
#    # Find papers associated with the award
#    funding_publications = {}
#    for k in award_record:
#        item = award_record[k]
#        pub_record = NN.getPublications(item['appl_id'])
#        funding_publications.update(pub_record)
#    
#    # Add the papers to the award db record
#    award_record['papers']    = []
#    for paper_doi in funding_publications:
#        award_record.append(paper_doi)
    


#db.child(user['localId']).push('james', user['idToken'])

# NIH = NIH_NCBI()
# project_num = 'OT3OD025349'
# funding_details = NIH.getProjectFundingDetails([project_num])
# funding_report = NIH.generateRecord(funding_details)
# db.set({project_num: funding_report}, user['idToken'])