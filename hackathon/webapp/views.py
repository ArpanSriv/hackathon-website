# from google.cloud import firestore
import json
import os

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .utils.firebase_utils import upload_on_firebase
from .utils.sheet_utils import update_google_sheets


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

        update_google_sheets(team_name, persons)

        upload_on_firebase('individuals', team_name, persons)

        return render(request, 'webapp/registration.html')
    # return render(request, 'webapp/registration.html')

@csrf_exempt
def registration_individual(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body.decode("utf-8"))

        print("Recieved::: " + received_json_data)

    return render(request, 'webapp/individualregistration.html')


def registration_startup(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body.decode("utf-8"))

        print("Recieved::: " + received_json_data)

    return render(request, 'webapp/startupregistration.html')












