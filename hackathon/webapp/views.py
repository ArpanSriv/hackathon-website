# from google.cloud import firestore
import json

from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader

from .utils.constants import *
from .utils.firebase_utils import upload_on_firebase
from .utils.sheet_utils import update_google_sheets
from .utils.progress_util import ProgressUtils

progress_utils = ProgressUtils.get_instance()


# Landing Page
def index(request):
    return render(request, 'webapp/landing.html')


def registration(request):
    return render(request, 'webapp/registration.html')


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
            if json_data['memberDetails']['member1']['firstName'] == '' or json_data['memberDetails']['member2'][
                'firstName'] == '':
                print('member 1 and member 2 found empty')

                resp['message'] = 'Members found but empty. Are you sure you entered all details correctly?'

                return HttpResponseBadRequest(json.dumps(resp), content_type='application/json')

            progress_id = json_data['progressID']

            # Found members 1 and 2 and also found some data there.
            resp = {
                'correct': '1',
                'message': 'Data found sufficient.'
            }

            reg_no = generate_reg_no(INDIVIDUAL)

            progress_utils.update_progress(progress_id, 20)

            print("Uploading to sheets...")

            # Upload the Data on Spreadsheet and Firebase :p
            update_google_sheets(INDIVIDUAL, reg_no, json_data, progress_id)

            progress_utils.update_progress(progress_id, 50)

            upload_on_firebase(INDIVIDUAL, json_data)

            progress_utils.update_progress(progress_id, 70)

            sendmail(json_data['teamName'], reg_no, json_data['teamEmail'])

            progress_utils.update_progress(progress_id, 100)

            progress_utils.remove_progress(progress_id)

            return HttpResponse(json.dumps(resp), content_type='application/json')

    # Normal GET Request.
    elif request.method == 'GET':
        progress_id = generate_progress_id()

        progress_utils.init_progress(progress_id)

        return render(request, 'webapp/individualregistration.html', {
            'progress_id': progress_id
        })


def poll_state(request):
    """ A view to report the progress to the user """
    data = 'Fail'
    if request.is_ajax():
        progress_id = request.GET.get('Progress-ID')
        data = {
            'progress': progress_utils.get_progress(progress_id)
        }

        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')


def registration_startup(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode("utf-8"))

        resp = {
            'correct': '1',
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
            if json_data['memberDetails']['member1']['firstName'] == '' or json_data['memberDetails']['member2'][
                'firstName'] == '':
                print('member 1 and member 2 found empty -> Startup')

                resp['message'] = 'Members found but empty. Are you sure you entered all details correctly?'

                return HttpResponseBadRequest(json.dumps(resp), content_type='application/json')

            # Found members 1 and 2 and also found some data there.
            resp = {
                'correct': '1',
                'message': 'Data found sufficient.'
            }

            progress_id = json_data['progressID']
            print("Progress ID = " + progress_id)

            progress_utils.update_progress(progress_id, 10)
            # # Upload to ftp
            # FTP_USERNAME = "django_auto@aihackathon.in"

            reg_no = generate_reg_no(STARTUP)

            print("Uploading to sheets...")

            progress_utils.update_progress(progress_id, 30)
            # Upload the Data on Spreadsheet and Firebase :p
            update_google_sheets(STARTUP, reg_no, json_data, progress_id)

            progress_utils.update_progress(progress_id, 70)

            upload_on_firebase(STARTUP, json_data)

            progress_utils.update_progress(progress_id, 75)

            sendmail(json_data['startupName'], reg_no, json_data['startupEmail'])

            progress_utils.update_progress(progress_id, 80)

            resp['teamName'] = json_data['teamName']
            resp['teamRegNo'] = reg_no

        return HttpResponse(json.dumps(resp), content_type='application/json')

    elif request.method == 'GET':
        progress_id = generate_progress_id()

        progress_utils.init_progress(progress_id)

        return render(request, 'webapp/startupregistration.html', {
            'progress_id': progress_id
        })


def privacy_policy(request):
    return render(request, 'webapp/privacy.html')


def about_us(request):
    return render(request, 'webapp/aboutus.html')


def contact_us(request):
    return render(request, 'webapp/contactus.html')


def thank_you(request):
    return render(request, 'webapp/thankyou.html')


def sendmail(team_name, reg_no, email_to_send):
    from_email = 'aihackathon@sitpune.edu.in'

    html_message = loader.render_to_string(
        'webapp/mail/mail.html',
        {
            'team_name': team_name,
            'reg_no': reg_no,
        }
    )

    send_mail(subject="AI Hackathon 2019",
              from_email=from_email,
              recipient_list=[email_to_send],
              fail_silently=False,
              html_message=html_message,
              message="You have been registered successfully.")


def generate_reg_no(type):
    import string
    import random
    min_char = 5
    max_char = 5

    allchar = string.ascii_uppercase + string.digits
    reg = "".join(random.choice(allchar) for x in range(random.randint(min_char, max_char)))

    if type == INDIVIDUAL:
        return "I-" + reg

    elif type == STARTUP:
        return "S-" + reg


def generate_progress_id():
    import string
    import random
    min_char = 3
    max_char = 3

    allchar = string.ascii_uppercase + string.digits
    reg = "".join(random.choice(allchar) for x in range(random.randint(min_char, max_char)))

    return reg
