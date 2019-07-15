# from google.cloud import firestore
import json
import os
import re

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .utils.firebase_utils import upload_on_firebase
from .utils.sheet_utils import update_google_sheets

from .utils.constants import *

# Landing Page
def index(request):
#     firebase_upload()
    # write_spreadsheet()
    return render(request, 'webapp/landing.html')


def registration(request):
    # if not request.is_ajax(): #TODO: Change it later
    if request.method == 'GET': # TODO: Change Later...
        # TODO: Get all the real info from the request.
        #raw_json = request.body

        team_name = "YOLO MAN"

        # Array of persons
        persons = []

        # Person 1
        person = {
            "first_name": "Andy",
            "last_name": "Mason",
            "dob": "26/09/1998",
            "email": "sample@abc.com",
            "phone": "+91123456700",
            "university": "SIU, Pune",
            "specialization": "CS",
            "city": "Mumbai",
            "state": "Maharashtra",
            "projects": "Some thing in NLP/CV"
        }

        person = [
            "Andy",
            "Mason",
            "26/09/1998",
            "sample@abc.com",
            "+91123456700",
            "SIU, Pune",
            "CS",
            "Mumbai",
            "Maharashtra",
            "Some thing in NLP/CV"
        ]

        persons.append(person)
        persons.append(person)
        persons.append(person)
        persons.append(person)

        # update_google_sheets(team_name, persons)
        #
        # upload_on_firebase('individuals', team_name, persons)

        return render(request, 'webapp/registration.html')
    # return render(request, 'webapp/registration.html')


def registration_individual(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode("utf-8"))

        print(json_data)

        resp = {
            'correct': '0',
            'message': 'Internal Server Error.'
        }

        # Team Name Empty
        if json_data['teamName'] == '':
            resp['message'] = 'A valid team name is required.'
            return HttpResponseBadRequest(json.dumps(resp), content_type='application/json')

        # Team Email Empty
        if json_data['teamEmail'] == '':
            resp['message'] = 'A valid team email is required.'
            return HttpResponseBadRequest(json.dumps(resp), content_type='application/json')

        # Team Members Validation
        if 'member1' not in json_data['memberDetails'] and 'member2' not in json_data['memberDetails']:
            print('member 1 and member 2 not found.')

            resp = {
                'correct': '0',
                'message': 'Member 1 and Member 2 are required.'
            }

            return HttpResponseBadRequest(json.dumps(resp), content_type='application/json')

        elif 'member1' in json_data['memberDetails'] and 'member2' in json_data['memberDetails']:
            if json_data['memberDetails']['member1']['firstName'] == '' or json_data['memberDetails']['member2']['firstName'] == '':
                print('member 1 and member 2 found empty')

                resp['message'] = 'Members found but empty. Are you sure you entered all details correctly?'

                return HttpResponseBadRequest(json.dumps(resp), content_type='application/json')

            # Found members 1 and 2 and also found some data there.
            resp = {
                'correct': '1',
                'message': 'Data found sufficient.'
            }

            reg_no = ''  # TODO

            print("Uploading to sheets...")

            # Upload the Data on Spreadsheet and Firebase :p
            update_google_sheets(INDIVIDUAL, reg_no, json_data)
            upload_on_firebase(INDIVIDUAL, json_data)

            return HttpResponse(json.dumps(resp), content_type='application/json')

    # Normal GET Request.
    return render(request, 'webapp/individualregistration.html')


def registration_startup(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode("utf-8"))

        resp = {
            'correct': '0',
            'message': 'Internal Server Error.'
        }

        # Startup Name Empty
        if 'startupName' in json_data:
            if json_data['startupName'] == '':
                resp['message'] = 'A valid Startup Name is required.'
                return HttpResponseBadRequest(json.dumps(resp), content_type='application/json')

        # Team Email Empty
        if 'startupEmail' in json_data:
            if json_data['startupEmail'] == '':
                resp['message'] = 'A valid Startup Email is required.'
                return HttpResponseBadRequest(json.dumps(resp), content_type='application/json')

        # Team DOR Empty
        if 'startupDOR' in json_data:
            if json_data['startupDOR'] == '':
                resp['message'] = 'A valid Startup Email is required.'
                return HttpResponseBadRequest(json.dumps(resp), content_type='application/json')

        # Team Domain Empty
        if 'startupDomain' in json_data:
            if json_data['startupDomain'] == '':
                resp['message'] = 'A valid Startup Technology Domain is required.'
                return HttpResponseBadRequest(json.dumps(resp), content_type='application/json')

        # Team Domain Empty
        if json_data['startupDesc'] == '':
            resp['message'] = 'A valid Startup Description is required.'
            return HttpResponseBadRequest(json.dumps(resp), content_type='application/json')

        # Team Members Validation
        if 'member1' not in json_data['memberDetails'] and 'member2' not in json_data['memberDetails']:
            print('member 1 and member 2 not found. -> Startup')

            resp = {
                'correct': '0',
                'message': 'Member 1 and Member 2 are required.'
            }

            return HttpResponseBadRequest(json.dumps(resp), content_type='application/json')

        elif 'member1' in json_data['memberDetails'] and 'member2' in json_data['memberDetails']:
            if json_data['memberDetails']['member1']['firstName'] == '' or json_data['memberDetails']['member2']['firstName'] == '':
                print('member 1 and member 2 found empty -> Startup')

                resp['message'] = 'Members found but empty. Are you sure you entered all details correctly?'

                return HttpResponseBadRequest(json.dumps(resp), content_type='application/json')

            # Found members 1 and 2 and also found some data there.
            resp = {
                'correct': '1',
                'message': 'Data found sufficient.'
            }

            reg_no = ''  # TODO

            print("Uploading to sheets...")

            # Upload the Data on Spreadsheet and Firebase :p
            update_google_sheets(STARTUP, reg_no, json_data)
            upload_on_firebase(STARTUP, json_data)

            return HttpResponse(json.dumps(resp), content_type='application/json')

    return render(request, 'webapp/startupregistration.html')


def privacy_policy(request):
    return render(request, 'webapp/privacy.html')


def about_us(request):
    return render(request, 'webapp/aboutus.html')


def contact_us(request):
    return render(request, 'webapp/contactus.html')




