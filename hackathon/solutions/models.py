from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TeamManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a Team with the given email and password, and members.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self._create_user(email, password, **extra_fields)


class Team(AbstractUser):
    reg_no = models.CharField(_('registration number'), unique=True, max_length=7)
    email = models.CharField(_('email'), max_length=50, unique=True)
    username = models.CharField(blank=True, null=True, max_length=10)
    team_name = models.CharField(_('team name'), max_length=30)
    duplicate_team = models.BooleanField(_('duplicate team name'), default=False)
    team_name_change_allowed = models.BooleanField(_('team name change allowed'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['team_name', 'reg_no']

    objects = TeamManager()

    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')

    def get_full_name(self):
        return "{}: {}: {}".format(self.reg_no, self.team_name, self.email)

    def get_short_name(self):
        return self.team_name


class Member(models.Model):
    email = models.EmailField(_('email address'), unique=False)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    dob = models.DateField(_('date of birth'))
    phone = models.CharField(_('phone number'), max_length=10)
    university = models.CharField(_('university'), max_length=100)
    specialization = models.CharField(_('specialization'), max_length=50)
    address_line_1 = models.CharField(_('address line 1'), max_length=50)
    address_line_2 = models.CharField(_('address line 2'), max_length=50)
    pincode = models.CharField(_('pincode'), max_length=7)
    city = models.CharField(_('city'), max_length=30)
    state = models.CharField(_('state'), max_length=30)
    projects = models.CharField(_('projects'), max_length=50)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {} <{}>".format(self.first_name, self.last_name, self.email)


class FileItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=True, blank=True)
    path = models.TextField(blank=True, null=True)
    size = models.BigIntegerField(default=0)
    file_type = models.CharField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uploaded = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    problem = models.CharField(max_length=1, default='1')

    @property
    def title(self):
        return str(self.name)

    def __str__(self):
        return "{}, {}, {}".format(self.name, self.path, self.user)


class SurveyResponses(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    answer_1 = models.BooleanField(default=False)
    answer_2 = models.BooleanField(default=False)
    answer_3 = models.BooleanField(default=False)
    answer_4 = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
