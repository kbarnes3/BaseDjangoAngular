from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, given_name, surname, password=None):
        user = self.model(username=username, given_name=given_name, surname=surname)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, given_name, surname, password):
        user = self.create_user(username, given_name, surname, password)
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.EmailField('email address', max_length=255, unique=True)
    given_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    is_active = models.BooleanField(
        default=True,
        help_text=
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ,
    )
    is_admin = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    registration_completed = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'username'
    REQUIRED_FIELDS = ['given_name', 'surname']

    def get_full_name(self):
        full_name = f'{self.given_name} {self.surname}'
        return full_name.strip()

    def get_short_name(self):
        return self.given_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.username], **kwargs)

    def has_perm(self, perm, obj=None):  # pylint: disable=unused-argument
        if obj:
            return obj.is_admin

        return self.is_admin

    def has_module_perms(self, app_label):  # pylint: disable=unused-argument
        return self.is_admin

    def __str__(self):
        return self.primary_email

    @property
    def is_staff(self):
        return self.is_admin
