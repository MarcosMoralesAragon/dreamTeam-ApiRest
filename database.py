import this

import pyrebase
import string

firebaseConfig = {
    'apiKey': "AIzaSyAf9T-kFsZYaPUb6-fqENFwafW5FDAPZE0",
    'authDomain': "dream-team-c9ca7.firebaseapp.com",
    'databaseURL': "https://dream-team-c9ca7-default-rtdb.europe-west1.firebasedatabase.app",
    'projectId': "dream-team-c9ca7",
    'storageBucket': "dream-team-c9ca7.appspot.com",
    'messagingSenderId': "505880151049",
    'appId': "1:505880151049:web:a7b0af22c78910084924d8"
}
firebase = pyrebase.initialize_app(firebaseConfig)


def create_data(where: string, data_id, data):
    db = firebase.database()
    return db.child(where).child(data_id).set(data)


def update_data(where: string, data_id, data):
    db = firebase.database()
    return db.child(where).child(data_id).update(data)


def get_database(where: string):
    db = firebase.database()
    return db.child(where).get()


def get_db_instance():
    db = firebase.database()
    return db