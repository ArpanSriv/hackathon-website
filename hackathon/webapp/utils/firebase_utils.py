import os

import firebase_admin
from firebase_admin import credentials, firestore

from .constants import INDIVIDUAL, STARTUP

cred = credentials.Certificate(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'firebase_key.json'))
firebase_admin.initialize_app(cred)
db = firestore.client()


def upload_on_firebase(team_type, json_data):
    if team_type == INDIVIDUAL:
        team_ref = db.collection('individuals').document(json_data['teamName'])
        team_ref.set(json_data)

    elif team_type == STARTUP:
        team_ref = db.collection('startups').document(json_data['startupName'])
        team_ref.set(json_data)
