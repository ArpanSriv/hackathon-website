from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=200)
    # TODO: ADD Model

# class StartupPerson(models.Model):
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     dob = models.DateField()
#     email = models.CharField()
#     phone = models.CharField(10)
#     address_1 = models.CharField()
#     address_2 = models.CharField()
#     pincode = models.CharField()
#     city = models.CharField()
#     state = models.CharField()
#     experience = models.CharField()
#
#
# class StartupForm(forms.ModelForm):
#     team_name = models.CharField(max_length=50)
#     startup_name = models.CharField(max_length=100)
#     email_for_contact = models.CharField()
#     date_of_registration = models.DateField()
#     technology_domain = models.CharField()
#     startup_desc = models.CharField()
#
#     registration_cert = forms.FileField()
#
#     member_1 = StartupPerson()
#     member_2 = StartupPerson()
#     member_3 = StartupPerson(blank=True)
#     member_4 = StartupPerson(blank=True)
#

# 'firstName': 'First Name',
#     'lastName': 'Last Name',
#     'dob': 'Date of Birth',
#     'personalEmail': 'Personal Email',
#     'mobileNo': 'Phone No.',
#     'university': 'University',
#     'specialization': 'Specialization',
#     'addressLine1': 'Address Line 1',
#     'addressLine2': 'Address Line 2',
#     'pincode': 'Pincode',
#     'city': 'City',
#     'state': 'State',
#     'projects': 'Projects',
