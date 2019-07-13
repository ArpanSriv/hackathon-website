import firebase_admin
from firebase_admin import credentials, firestore
import os
from .person_converter import get_team_json_from_array

cred = credentials.Certificate(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'firebase_key.json'))

firebase_admin.initialize_app(cred)

db = firestore.client()


def upload_on_firebase(team_type, team_name, persons):
    
    team_json = {}

    team_json[team_name] = []

    for person in persons:
        person_json = get_team_json_from_array(person)
        team_json[team_name].append(person_json)

    team_ref = db.collection(u'users').document(team_name)
    team_ref.set(team_json)

