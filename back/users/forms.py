from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django_registration import validators
from users.models import User


class EmailPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.

        """
        active_users = User.objects.filter(
            primary_email__iexact=email)
        return (u for u in active_users if u.has_usable_password())


class RegistrationForm(UserCreationForm):
    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.

    Subclasses should feel free to add any additional validation they
    need, but should take care when overriding ``save()`` to respect
    the ``commit=False`` argument, as several registration workflows
    will make use of it to create inactive user accounts.

    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'primary_email',
            'given_name',
            'surname',
            'password1',
            'password2',
        ]
        labels = {
            'primary_email': 'Email'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['primary_email'].validators.extend(
            (validators.HTML5EmailValidator(), validators.validate_confusables_email)
        )
