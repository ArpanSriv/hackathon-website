import os
import pickle
import re

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .constants import INDIVIDUAL, STARTUP

spreadsheet_id = "1Moej841MoASt-hqLi_CkumLj2-eQ6x0xrMm19tc9g2k"

credentials = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')


def convert_member_json_to_array_individual(reg_no, team_name, team_email, member):
    member_array = [reg_no, team_name, team_email]

    for member_field in member:
        member_array.append(member[member_field])

    return member_array


def convert_member_json_to_array_startup(reg_no, startup_name, startup_email, startup_dor, startup_domain, startup_desc, member):
    member_array = [reg_no, startup_name, startup_email, startup_dor, startup_domain, startup_desc]

    for member_field in member:
        member_array.append(member[member_field])

    return member_array


def update_google_sheets(type, reg_no, team_data):
    service = get_spreadsheet_service()

    # Call the Sheets API
    sheet = service.spreadsheets()

    if type == INDIVIDUAL:

        team_name = team_data['teamName']
        team_email = team_data['teamEmail']
        members = team_data['memberDetails']

        body = {
            'values': []
        }

        for member_no in members:
            member_converted = convert_member_json_to_array_individual(reg_no, team_name, team_email, members[member_no])
            print(member_converted)
            body['values'].append(member_converted)

        result = sheet.values().append(
            spreadsheetId=spreadsheet_id, range="Individuals", body=body, valueInputOption="RAW").execute()

        # Merge the cells v1
        updated_range = result.get('updates').get('updatedRange')

        # Replace with team name column name (A -> reg_no)
        reg_no_range = re.sub(r'([A-Z])(\d)', repl='A\\2', string=updated_range)
        team_name_no_range = re.sub(r'([A-Z])(\d)', repl='B\\2', string=updated_range)
        team_email_range = re.sub(r'([A-Z])(\d)', repl='C\\2', string=updated_range)

        merge_columns(reg_no_range)
        merge_columns(team_name_no_range)
        merge_columns(team_email_range)

    elif type == STARTUP:

        startup_name = team_data['startupName']
        startup_email = team_data['startupEmail']
        startup_dor = team_data['startupDOR']
        startup_domain = team_data['startupDomain']
        startup_desc = team_data['startupDesc']

        members = team_data['memberDetails']

        body = {
            'values': []
        }

        for member_no in members:
            member_converted = convert_member_json_to_array_startup(reg_no, startup_name, startup_email, startup_dor, startup_domain, startup_desc, members[member_no])
            print(member_converted)
            body['values'].append(member_converted)

        result = sheet.values().append(
            spreadsheetId=spreadsheet_id, range="Startups", body=body, valueInputOption="RAW").execute()

        # Merge the cells v1
        updated_range = result.get('updates').get('updatedRange')

        for char in 'ABCDEF':
            range_to_merge = re.sub(r'([A-Z])(\d)', repl=f'{char}\\2', string=updated_range)
            merge_columns(range_to_merge)


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


def get_sheet_index_from_name(sheet_name) -> int:
    ids = {
        "Individuals": 0,
        "Startups": 911829110
    }
    return ids[sheet_name]


def merge_columns(range_to_merge):
    service = get_spreadsheet_service()

    # Range Example: Individuals!A4:A5
    print("Range got: " + range_to_merge)

    range_data = re.match(u'(^.+)!(.+):(.+$)', range_to_merge)

    co1 = re.match(r"(\D+)(\d+)", range_data[2])
    co2 = re.match(r"(\D+)(\d+)", range_data[3])

    grid_range = {
        'sheetId': get_sheet_index_from_name(range_data[1]),
        'startRowIndex': int(co1[2]) - 1,
        'endRowIndex': str(co2[2]),
        'startColumnIndex': alpha2num(co1[1]),
        'endColumnIndex': str(int(alpha2num((co2[1])) + 1))
    }

    print(grid_range)

    results = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "requests": [
                {
                    "mergeCells": {
                        "mergeType": "MERGE_COLUMNS",
                        "range": grid_range
                    }
                },
            ]
        }).execute()


def alpha2num(alpha):
    print("Alpha got: " + alpha)
    return ord(alpha) - ord('A')
