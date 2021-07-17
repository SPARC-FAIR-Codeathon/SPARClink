
import pyrebase
import NIHScraper

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

db = firebase.database().child(user['localId']).child('NIH')
#db.child(user['localId']).push('james', user['idToken'])

NIH = NIHScraper.NIHScraper()
project_num = 'OT3OD025349'
funding_details = NIH.getProjectFundingDetails([project_num])
funding_report = NIH.generateRecord(funding_details)
db.set({project_num: funding_report}, user['idToken'])