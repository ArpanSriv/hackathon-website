import os
import pickle
import re

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

spreadsheet_id = "1Moej841MoASt-hqLi_CkumLj2-eQ6x0xrMm19tc9g2k"

credentials = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')


def update_google_sheets(team_name, persons):
    service = get_spreadsheet_service()

    # Call the Sheets API
    sheet = service.spreadsheets()

    values = [
        [
            { 'values': persons[0] }
        ]
    ]

    body = {
        'values': [persons[0], persons[1], persons[2], persons[3]]
    }
    result = sheet.values().append(
        spreadsheetId=spreadsheet_id, range="Individuals", body=body, valueInputOption="RAW").execute()
    print('{0} cells appended.'.format(result \
                                        .get('updates').get('updatedRange')))

    team_name_range = result.get('updates').get('updatedRange')

    # Replace with team name column name
    team_name_range = re.sub(r'([A-Z])(\d)', repl='K\\2', string=team_name_range)

    print("Range to put team in : {0}".format(team_name_range))

    team_name_body = {
        'values': [[team_name], [team_name], [team_name], [team_name]]
    }

    team_name_update_result = sheet.values().append(spreadsheetId=spreadsheet_id, range=team_name_range, body=team_name_body, valueInputOption="RAW").execute()
    # merge_columns(team_name_update_result.get('updates').get('updatedRange')) # TODO


def get_spreadsheet_service():
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
                credentials, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service


def merge_columns(range): # TODO
    service = get_spreadsheet_service()

    results = service.spreadsheets().batchUpdate(
        spreadsheetId = spreadsheet_id,
        body = {
            "requests": [
                {
                    "mergeCells": {
                        "mergeType": "MERGE_ROWS",
                        "range": {
                            "sheetId": 0,
                            "startRowIndex": 0,
                            "endRowIndex": 2,
                            "startColumnIndex": 0,
                            "endColumnIndex": 1
                        }
                    }
                },
            ]
    }).execute() 