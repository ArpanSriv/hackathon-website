import csv
import datetime
import logging
import os
import secrets
import string
import time

import boto3
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from rest_framework import permissions, status, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

# # Solution Upload
from webapp import views as webapp_views
from .config_aws import (
    AWS_UPLOAD_BUCKET,
    AWS_UPLOAD_REGION,
    AWS_UPLOAD_ACCESS_KEY_ID,
    AWS_UPLOAD_SECRET_KEY
)
from .models import *


@login_required()
def logout_hackathon(request):
    logout(request)
    return redirect('/')


def login_solution(request):
    logging.info("Method for login: {}".format(request.method))
    if request.method == 'POST':
        # Authenticate user
        username = request.POST.get('teamEmail')
        password = request.POST.get('password')

        if username is not None and password is not None:
            user = authenticate(username=username, password=password)

            if user is not None:

                login(request, user)
                return redirect('/upload_solution')

            else:
                # FIXME
                return render(request, 'solutions/upload_login.html', context={
                    'message': 'The username and password do not match! Please try again'
                })

        return redirect("Facebook.com")
    elif request.method == 'GET':
        return render(request, 'solutions/upload_login.html')


def redirect_with_error(message, url=None):
    # TODO Push messages in the message framework
    if url is None:
        return redirect(webapp_views.index)
    else:
        return redirect(url)
    pass


def get_file_uploaded_statues(team_id):
    team = Team.objects.get(id=team_id)

    files = FileItem.objects.filter(user=team)

    files_status = {
        '1': {
            'docker': 'Not Uploaded',
            'program': 'Not Uploaded',
            'ppt': 'Not Uploaded',
        },
        '2': {
            'docker': 'Not Uploaded',
            'program': 'Not Uploaded',
            'ppt': 'Not Uploaded',
        }
    }

    if files.exists():
        for problem_no in files_status:
            for file_type in files_status[problem_no]:
                if FileItem.objects.filter(user=team, file_type=file_type, problem=problem_no).first():
                    files_status[problem_no][file_type] = 'Uploaded'

    print(files_status)
    # if files.exists():
    #     if FileItem.objects.filter(user=team, file_type='docker').first():
    #         files_status['docker'] = 'Uploaded'
    #
    #     if FileItem.objects.filter(user=team, file_type='program').first():
    #         files_status['program'] = 'Uploaded'
    #
    #     # if FileItem.objects.filter(user=team, file_type='information').first():
    #     #     files_status['information'] = 'Uploaded'
    #
    #     if FileItem.objects.filter(user=team, file_type='ppt').first():
    #         files_status['ppt'] = 'Uploaded'

    return files_status


@login_required(login_url='/login')
def upload_solution(request):
    # if request.user is not Team:
    #     raise Exception("Team should be the auth type.")
    team_id = request.user.id  # Team id
    print("Team id mila re baba: {}".format(team_id))

    if team_id is not None:
        team = Team.objects.get(id=team_id)
        members = Member.objects.filter(team=team)

        team_name = getattr(team, 'team_name')
        reg_no = getattr(team, 'reg_no')

        files_uploaded = get_file_uploaded_statues(team_id)

        survey_status = False

        survey = SurveyResponses.objects.filter(user=team)

        if survey.exists():
            survey_status = True

        return render(request, 'solutions/upload_solution.html', context={
            'members': members,
            'file_status': files_uploaded,
            'survey_status': survey_status,
            'team_name': team_name,
            'reg_no': reg_no,
        })

    else:
        return redirect_with_error('Team id is none')  # TODO


class FilePolicyAPI(APIView):
    """
    This view is to get the AWS Upload Policy for our s3 bucket.
    What we do here is first create a FileItem object instance in our
    Django backend. This is to include the FileItem instance in the path
    we will use within our bucket as you'll see below.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        """
        The initial post request includes the filename
        and auth credientails. In our case, we'll use
        Session Authentication but any auth should work.
        """
        filename_req = request.data.get('filename')
        if not filename_req:
            return Response({"message": "A filename is required"}, status=status.HTTP_400_BAD_REQUEST)
        policy_expires = int(time.time() + 5000)
        user = request.user
        username_str = str(request.user.username)
        """
        Below we create the Django object. We'll use this
        in our upload path to AWS.

        Example:
        To-be-uploaded file's name: Some Random File.mp4
        Eventual Path on S3: <bucket>/username/2312/2312.mp4
        """
        file_obj = FileItem(user=user, name=filename_req)
        file_obj_id = file_obj.id

        reg_no = request.user.reg_no
        team_name = request.user.team_name
        filetype = request.POST.get('filetype')
        problem_no = request.POST.get('problem')

        problem = "problem_{}".format(problem_no)
        # upload_start_path = "/upload_solutions/{username}/{file_obj_id}/".format(
        #     username=username_str,
        # )
        _, file_extension = os.path.splitext(filename_req)
        filename_final = "{file_obj_id}{file_extension}".format(
            file_obj_id=file_obj_id,
            file_extension=file_extension

        )

        key = "hackathon_solutions/{}_{}/{}/".format(
            team_name, reg_no, problem)

        s3_upload_path = key + \
            "{}_{}{}".format(reg_no, filetype, file_extension)

        # if filetype == 'docker':
        #     s3_upload_path = key + "{}_{}".format(reg_no, filetype)

        """
        Eventual file_upload_path includes the renamed file to the
        Django-stored FileItem instance ID. Renaming the file is
        done to prevent issues with user generated formatted names.
        """
        # final_upload_path = "{upload_start_path}{filename_final}".format(
        #     upload_start_path=upload_start_path,
        #     filename_final=filename_final,
        # )
        if filename_req:
            """
            Save the eventual path to the Django-stored FileItem instance
            """
            file_obj.path = s3_upload_path

            file_obj.file_type = filetype
            file_obj.problem = problem_no
            file_obj.save()

        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_UPLOAD_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_UPLOAD_SECRET_KEY,
            region_name=AWS_UPLOAD_REGION,
            config=boto3.session.Config(signature_version='s3v4')
        )

        data = s3.generate_presigned_post(
            Bucket=AWS_UPLOAD_BUCKET,
            Key=s3_upload_path,
            ExpiresIn=5000
        )

        data['file_bucket_path'] = s3_upload_path
        data['filename'] = filename_final
        data['file_id'] = file_obj_id
        data['awsAccessKeyId'] = AWS_UPLOAD_ACCESS_KEY_ID

        return Response(data, status=status.HTTP_200_OK)


class FileUploadCompleteHandler(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        file_id = request.POST.get('file')
        size = request.POST.get('fileSize')
        data = {}
        type_ = request.POST.get('fileType')
        if file_id:
            obj = FileItem.objects.get(id=int(file_id))
            obj.size = int(size)
            obj.uploaded = True
            obj.type = type_
            obj.save()
            data['id'] = obj.id
            data['saved'] = True
        return Response(data, status=status.HTTP_200_OK)


@login_required(login_url='/login')
def process_survey(request):
    if request.method == 'POST':
        response_1 = request.POST.get('response_1')
        response_2 = request.POST.get('response_2')
        response_3 = request.POST.get('response_3')
        response_4 = request.POST.get('response_4')

        answer_1 = False
        answer_2 = False
        answer_3 = False
        answer_4 = False

        if response_1 == 'on':
            answer_1 = True
        if response_2 == 'on':
            answer_2 = True
        if response_3 == 'on':
            answer_3 = True
        if response_4 == 'on':
            answer_4 = True

        survey_response = SurveyResponses(user=request.user, answer_1=answer_1, answer_2=answer_2, answer_3=answer_3,
                                          answer_4=answer_4)

        try:
            survey_response.save()
        except IntegrityError:
            return redirect_with_error("You have already filled the form.", upload_solution)

        return redirect(upload_solution)
    else:
        return HttpResponse(status=403)


def generate_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))

    return password


def find_password_for_user(email):
    with open('/home/ubuntu/hackathon-website/hackathon/solutions/team_data.csv', 'r') as csv_file:
        password_csv = csv.reader(csv_file)
        for row in password_csv:
            if email == row[0]:
                return row[1]

    return -1


def insert_users(request):

    print("Inside insert users.", flush=True)
    print("Haha yoyu.", flush=True)

    with open('/home/ubuntu/hackathon-website/hackathon/solutions/hackathon.csv', 'r') as f:
        print("Opened first.", flush=True)

        with open('/home/ubuntu/hackathon-website/hackathon/solutions/csv/mysql_team_out.csv', mode='a') as output_csv_file:
            data = csv.DictReader(f)
            print("Opened second:", flush=True)
            writer = csv.writer(output_csv_file, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)

            row_count = 0
            teams_created = 0
            duplicate_teams_inserted = 0

            for raw in data:

                team_email = raw.get('team_email')

                team = Team.objects.filter(email__contains=team_email)

                if not team.exists():
                    password = find_password_for_user(team_email)

                    if password != -1:

                        team_name = raw.get('team_name')
                        reg_no = raw.get('reg_no')

                        duplicate_team_present = False
                        team_name_change_allowed = False

                        duplicate_team = Team.objects.filter(team_name=team_name)

                        if duplicate_team.exists():
                            duplicate_team_present = True
                            team_name_change_allowed = True

                        try:
                            print("Create user: {} with password: {}".format(team_email, password))
                            Team.objects.create_user(email=team_email,
                                                    password=password,
                                                    team_name=team_name,
                                                    reg_no=reg_no,
                                                    duplicate_team=duplicate_team_present,
                                                    team_name_change_allowed=team_name_change_allowed)
                        except IntegrityError as e:
                            print("Integrity Error: {}".format(e))
                            print("Team Details: team_name={}, team_email={}, reg_no={}".format(team_name, team_email,
                                                                                                reg_no))
                            break

                        writer.writerow([team_email, password])

                        print("User created: " + team_email + " " + password)

                        teams_created += 1

                        if duplicate_team_present:
                            duplicate_teams_inserted += 1

                    else:
                        raise Exception("Couldn't find password for email: {}".format(team_email))

                row_count += 1

                print("Total Rows: {}, Inserted: {}, Duplicates: {}".format(row_count, teams_created,
                                                                            duplicate_teams_inserted))

    with open('/home/ubuntu/hackathon-website/hackathon/solutions/hackathon.csv', 'r') as f:
        data = csv.DictReader(f)

        row_count = 0
        users_created = 0
        duplicate_users_present = 0

        for raw in data:
            member_email = raw.get('email')

            if Member.objects.filter(email=member_email).exists():
                duplicate_users_present += 1

            else:
                team_email = raw.get('team_email')

                team = Team.objects.filter(email__contains=team_email)

                if team.exists():
                    # dob_proper = datetime.datetime.strptime(raw.get('dob'), '%d/%m/%Y').strftime('%Y-%m-%d')

                    user = Member(
                        email=raw.get('email'),
                        first_name=raw.get('first_name'),
                        last_name=raw.get('last_name'),
                        dob='1998-01-01',  # Oops! :
                        phone=raw.get('phone'),
                        university=raw.get('university'),
                        specialization=raw.get('specialization'),
                        address_line_1=raw.get('address_line_1'),
                        address_line_2=raw.get('address_line_2'),
                        pincode=raw.get('pincode'),
                        city=raw.get('city'),
                        state=raw.get('state'),
                        projects='',
                        team=team.first(),
                    )

                    user.save()

                    # writer.writerow([team_email, password])

                    print("User created: {}, {}".format(member_email, team))

                    users_created += 1

            row_count += 1

            print("User: Total Rows: {}, Inserted: {}, Duplicates: {}".format(row_count, users_created,
                                                                        duplicate_users_present))

    return HttpResponse(status=200)


def check_entries(request):
    with open('solutions/emails.tsv') as file:
        email_count = 0
        teams_found = 0

        for email in file:

            try:
                Team.objects.get(email=email.rstrip())
                teams_found += 1
            except:
                print("Team Not Found: {}".format(email))

            email_count += 1

        print("Teams_found: {}, email_count: {}".format(teams_found, email_count))

    return HttpResponse("Teams_found: {}, email_count: {}".format(teams_found, email_count), status=200)


def sendmails(request):
    from_email = 'aihackathon@sitpune.edu.in'

    with open('solutions/team_data_new.csv', 'r') as f:
        data = csv.reader(f)
        mail_sent_count = 0

        with open('solutions/csv/test_email_log_actual.csv', 'a') as o:
            writer = csv.writer(o, delimiter=',')

            for raw in data:
                email_to_send = raw[0]
                password = raw[1]

                html_message = loader.render_to_string(
                    'webapp/mail/mail.html',
                    {
                        'email': email_to_send,
                        'password': password,
                    }
                )

                send_mail(subject="AI Hackathon 2019 (Login Credentials)",
                          from_email=from_email,
                          recipient_list=[email_to_send],
                          fail_silently=False,
                          html_message=html_message,
                          message="Login Credentials")

                writer.writerow(
                    [email_to_send, password, 1, datetime.datetime.now()])

                mail_sent_count += 1
                print("------------", flush=True)
                print("Mail sent to: {}, count: {}".format(
                    email_to_send, mail_sent_count), flush=True)

    return HttpResponse('mail sent, count: {}'.format(mail_sent_count), 200)

def send_credential_mail(team_email, password):
    html_message = loader.render_to_string(
        'webapp/mail/mail.html',
        {
            'email': team_email,
            'password': password,
        }
    )

    send_mail(subject="AI Hackathon 2019 (Login Credentials)",
              from_email='aihackathon@sitpune.edu.in',
              recipient_list=[team_email],
              fail_silently=False,
              html_message=html_message,
              message="Login Credentials")

    print("Mail sent to {}".format(team_email))



@login_required
def register_new(request):
    if request.method == 'POST':
        data = request.POST.get('registerData')
        send_mail = request.POST.get('sendMail')

        print("Sendmail: {}".format(send_mail))
        members = {
            'member1': {},
            'member2': {},
        }

        # Parse data
        lines = data.splitlines()

        mentor_details = lines[0]
        member1_line = lines[1]

        mentor_details_split = mentor_details.split('\t')
        member1_details = member1_line.strip().split('\t')

        reg_no = mentor_details_split[0]
        team_name = mentor_details_split[1]
        team_email = mentor_details_split[2]

        members['member1']['first_name'] = mentor_details_split[3]
        members['member1']['last_name'] = mentor_details_split[4]
        # members['member1']['dob'] = mentor_details_split[5]

        members['member1']['email'] = mentor_details_split[6]
        members['member1']['phone'] = mentor_details_split[7]
        members['member1']['university'] = mentor_details_split[8]
        members['member1']['specialization'] = mentor_details_split[9]
        members['member1']['address_line_1'] = mentor_details_split[10]
        members['member1']['address_line_2'] = mentor_details_split[11]
        members['member1']['pincode'] = mentor_details_split[12]
        members['member1']['city'] = mentor_details_split[13]
        members['member1']['state'] = mentor_details_split[14]

        members['member2']['first_name'] = member1_details[0]
        members['member2']['last_name'] = member1_details[1]
        # members['member2']['dob'] = mentor_details_split[2]

        members['member2']['email'] = member1_details[3]
        members['member2']['phone'] = member1_details[4]
        members['member2']['university'] = member1_details[5]
        members['member2']['specialization'] = member1_details[6]
        members['member2']['address_line_1'] = member1_details[7]
        members['member2']['address_line_2'] = member1_details[8]
        members['member2']['pincode'] = member1_details[9]
        members['member2']['city'] = member1_details[10]
        members['member2']['state'] = member1_details[11]

        print("{}".format(members))

        password = generate_password()

        team = Team.objects.filter(email=team_email)

        if team.exists():
            return HttpResponse("Team already exists.", status=502)
        else:
            Team.objects.create_user(email=team_email, password=password, reg_no=reg_no, team_name=team_name)
            print("{},{}".format(team_email, password))

        team = Team.objects.filter(email=team_email)

        if team.exists():
            m1 = Member(
                email=members['member1'].get('email'),
                first_name=members['member1'].get('first_name'),
                last_name=members['member1'].get('last_name'),
                dob='1998-01-01',  # Oops! :
                phone=members['member1'].get('phone'),
                university=members['member1'].get('university'),
                specialization=members['member1'].get('specialization'),
                address_line_1=members['member1'].get('address_line_1'),
                address_line_2=members['member1'].get('address_line_2'),
                pincode=members['member1'].get('pincode'),
                city=members['member1'].get('city'),
                state=members['member1'].get('state'),
                projects='',
                team=team.first(),
            )

            m1.save()

            m2 = Member(
                email=members['member2'].get('email'),
                first_name=members['member2'].get('first_name'),
                last_name=members['member2'].get('last_name'),
                dob='1998-01-01',  # Oops! :
                phone=members['member2'].get('phone'),
                university=members['member2'].get('university'),
                specialization=members['member2'].get('specialization'),
                address_line_1=members['member2'].get('address_line_1'),
                address_line_2=members['member2'].get('address_line_2'),
                pincode=members['member2'].get('pincode'),
                city=members['member2'].get('city'),
                state=members['member2'].get('state'),
                projects='',
                team=team.first(),
            )

            m2.save()

            if send_mail == 'on':
                send_credential_mail(team_email, password)
                print("Email Sent.")

            return HttpResponse('All ok.', status=200)

        return HttpResponse("Team created but still couldn't find", 500)

    else:
        return render(request, 'solutions/register_new.html')
