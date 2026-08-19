import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Load Firebase Service Account Key
cred = credentials.Certificate("firebase_key.json")

# Initialize Firebase
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://interactive-mat-b38b8-default-rtdb.firebaseio.com/"
})

# Create database reference
database = db.reference("/")