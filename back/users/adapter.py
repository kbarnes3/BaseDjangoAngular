from django.conf import settings
from django.core.mail import mail_admins

from allauth.account.adapter import DefaultAccountAdapter


class UserAdapter(DefaultAccountAdapter):  # pylint: disable=abstract-method

    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_CREATION_MODE', 'default') != 'disabled'

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=commit)
        if getattr(settings, 'ACCOUNT_CREATION_MODE', 'default') == 'notify':
            mail_admins(
                subject='New account created',
                message=f'A new account has been created:\n\n'
                        f'Email: {user.email}\n'
                        f'Name: {user.get_full_name()}\n',
            )
        return user
