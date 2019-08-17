import logging
import os
import time

import boto3
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
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

        files_uploaded = get_file_uploaded_statues(team_id)

        survey_status = False

        survey = SurveyResponses.objects.filter(user=team)

        if survey.exists():
            survey_status = True

        return render(request, 'solutions/upload_solution.html', context={
            'members': members,
            'file_status': files_uploaded,
            'survey_status': survey_status
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

        key = "solutions_test/{}_{}/{}/".format(team_name, reg_no, problem)

        s3_upload_path = key + "{}_{}{}".format(reg_no, filetype, file_extension)

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

        survey_response.save()

        return redirect(upload_solution)
    else:
        return HttpResponse(status=403)
