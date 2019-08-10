from django.shortcuts import render


# # Solution Upload
def login_solution(request):
    return render(request, 'solutions/upload_login.html')


def upload_solution(request):
    return render(request, 'solutions/upload_solution.html')


import os
import time
from rest_framework import permissions, status, authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from .config_aws import (
    AWS_UPLOAD_BUCKET,
    AWS_UPLOAD_REGION,
    AWS_UPLOAD_ACCESS_KEY_ID,
    AWS_UPLOAD_SECRET_KEY
)
from .models import FileItem
import boto3


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
        file_obj = FileItem.objects.create(user=user, name=filename_req)
        file_obj_id = file_obj.id
        upload_start_path = "{username}/{file_obj_id}/".format(
            username=username_str,
            file_obj_id=file_obj_id
        )
        _, file_extension = os.path.splitext(filename_req)
        filename_final = "{file_obj_id}{file_extension}".format(
            file_obj_id=file_obj_id,
            file_extension=file_extension

        )
        """
        Eventual file_upload_path includes the renamed file to the
        Django-stored FileItem instance ID. Renaming the file is
        done to prevent issues with user generated formatted names.
        """
        final_upload_path = "{upload_start_path}{filename_final}".format(
            upload_start_path=upload_start_path,
            filename_final=filename_final,
        )
        if filename_req and file_extension:
            """
            Save the eventual path to the Django-stored FileItem instance
            """
            file_obj.path = final_upload_path
            file_obj.save()

        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_UPLOAD_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_UPLOAD_SECRET_KEY,
            region_name=AWS_UPLOAD_REGION,
            config=boto3.session.Config(signature_version='s3v4')
        )

        reg_no = request.data.get('reg_no')
        team_name = request.data.get('team')

        key = "solutions_test/{}_{}/".format(team_name, "I-4AB5S")

        data = s3.generate_presigned_post(
            Bucket=AWS_UPLOAD_BUCKET,
            Key=key + "${filename}",
            ExpiresIn=5000
        )

        data['file_bucket_path'] = upload_start_path
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
