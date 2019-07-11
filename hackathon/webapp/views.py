# from google.cloud import firestore
import os
import pickle

import firebase_admin
from django.http import HttpResponse
from django.shortcuts import render
from firebase_admin import credentials, firestore, storage
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

cred = credentials.Certificate( os.path.join(os.path.dirname(os.path.abspath(__file__)), 'key.json')  )
firebase_admin.initialize_app(cred)

spreadsheet_id = "1Moej841MoASt-hqLi_CkumLj2-eQ6x0xrMm19tc9g2k"

spread_cred = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')

# Landing Page
def index(request):
#     firebase_upload()
    write_spreadsheet()
    return render(request, 'webapp/landing.html')

def write_spreadsheet():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                spread_cred, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()


    values = [
    [
        "Part2", "Part2", "Part2", "Part1", "Part1", "Part1", 
    ],
    # Additional rows ...
    ]
    body = {
        'values': values
    }
    result = sheet.values().append(
        spreadsheetId=spreadsheet_id, range="Sheet1", body=body, valueInputOption="RAW").execute()
    print('{0} cells appended.'.format(result \
                                        .get('updates') \
                                        .get('updatedCells')))

def firebase_upload():
    bucket = storage.bucket("tata-hackathon.appspot.com")

    destination_blob_name = "ke.yjkon"
    source_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'key.json') 
    
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))
