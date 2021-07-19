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

email    = input('Enter email: ')
passw    = input('Enter password: ')
user     = auth.sign_in_with_email_and_password(email, passw)

award_db   = firebase.database().child(user['localId']).child('Awards')
dataset_db = firebase.database().child(user['localId']).child('Datasets')
paper_db   = firebase.database().child(user['localId']).child('Papers')

# Get all the datasets from Sparc Portal
sparc_dataset_list = []
sparc_dataset_list = get_list_of_datasets_with_metadata(sparc_dataset_list)

for dataset in sparc_dataset_list:
    # Find the awards associated with the datasets
    



#db.child(user['localId']).push('james', user['idToken'])

# NIH = NIH_NCBI()
# project_num = 'OT3OD025349'
# funding_details = NIH.getProjectFundingDetails([project_num])
# funding_report = NIH.generateRecord(funding_details)
# db.set({project_num: funding_report}, user['idToken'])