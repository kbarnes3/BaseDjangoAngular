"""Tests for users app and allauth headless API."""
from allauth.account.models import EmailAddress
from django.core import mail
from django.test import TestCase, override_settings

from users.models import User


class AllAuthHeadlessApi(TestCase):
    BASE_URL = '/_allauth/browser/v1'

    def test_config_endpoint(self):
        response = self.client.get(f'{self.BASE_URL}/config')
        self.assertEqual(response.status_code, 200)

    def test_session_unauthenticated(self):
        response = self.client.get(f'{self.BASE_URL}/auth/session')
        self.assertEqual(response.status_code, 401)

    def test_signup_requires_email_verification(self):
        response = self.client.post(
            f'{self.BASE_URL}/auth/signup',
            data={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User',
                'password': 'ComplexPass123!',
            },
            content_type='application/json',
        )
        # 401 because email verification is mandatory
        self.assertEqual(response.status_code, 401)

        user = User.objects.get(email='test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')


class SiteConfigEndpoint(TestCase):
    """Tests for the /api/config/ endpoint."""

    def test_returns_default_mode(self):
        response = self.client.get('/api/config/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['account_creation_mode'], 'default')

    @override_settings(ACCOUNT_CREATION_MODE='notify')
    def test_returns_notify_mode(self):
        response = self.client.get('/api/config/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['account_creation_mode'], 'notify')

    @override_settings(ACCOUNT_CREATION_MODE='disabled')
    def test_returns_disabled_mode(self):
        response = self.client.get('/api/config/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['account_creation_mode'], 'disabled')


class AccountCreationModeDefault(TestCase):
    """Tests for ACCOUNT_CREATION_MODE = 'default'."""
    SIGNUP_URL = '/_allauth/browser/v1/auth/signup'

    def test_signup_works(self):
        response = self.client.post(
            self.SIGNUP_URL,
            data={
                'email': 'default@example.com',
                'first_name': 'Default',
                'last_name': 'User',
                'password': 'ComplexPass123!',
            },
            content_type='application/json',
        )
        self.assertIn(response.status_code, [200, 401])  # 401 = email verification pending
        self.assertTrue(User.objects.filter(email='default@example.com').exists())

    def test_no_admin_email_sent(self):
        mail.outbox.clear()
        self.client.post(
            self.SIGNUP_URL,
            data={
                'email': 'default2@example.com',
                'first_name': 'Default',
                'last_name': 'User',
                'password': 'ComplexPass123!',
            },
            content_type='application/json',
        )
        # Only the email verification email should be sent, not an admin notification
        admin_emails = [m for m in mail.outbox if 'New account created' in m.subject]
        self.assertEqual(len(admin_emails), 0)


@override_settings(ACCOUNT_CREATION_MODE='notify')
class AccountCreationModeNotify(TestCase):
    """Tests for ACCOUNT_CREATION_MODE = 'notify'."""
    SIGNUP_URL = '/_allauth/browser/v1/auth/signup'

    def test_signup_works(self):
        response = self.client.post(
            self.SIGNUP_URL,
            data={
                'email': 'notify@example.com',
                'first_name': 'Notify',
                'last_name': 'User',
                'password': 'ComplexPass123!',
            },
            content_type='application/json',
        )
        self.assertIn(response.status_code, [200, 401])
        self.assertTrue(User.objects.filter(email='notify@example.com').exists())

    def test_admin_email_sent(self):
        mail.outbox.clear()
        self.client.post(
            self.SIGNUP_URL,
            data={
                'email': 'notify2@example.com',
                'first_name': 'Notify',
                'last_name': 'User',
                'password': 'ComplexPass123!',
            },
            content_type='application/json',
        )
        admin_emails = [m for m in mail.outbox if 'New account created' in m.subject]
        self.assertEqual(len(admin_emails), 1)
        self.assertIn('notify2@example.com', admin_emails[0].body)


@override_settings(ACCOUNT_CREATION_MODE='disabled')
class AccountCreationModeDisabled(TestCase):
    """Tests for ACCOUNT_CREATION_MODE = 'disabled'."""
    SIGNUP_URL = '/_allauth/browser/v1/auth/signup'

    def test_signup_blocked(self):
        response = self.client.post(
            self.SIGNUP_URL,
            data={
                'email': 'disabled@example.com',
                'first_name': 'Disabled',
                'last_name': 'User',
                'password': 'ComplexPass123!',
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(User.objects.filter(email='disabled@example.com').exists())


class ManagementCommandUserCreation(TestCase):
    """Tests that users created via management commands have verified emails."""

    def test_create_superuser_has_verified_email(self):
        user = User.objects.create_superuser(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='ComplexPass123!',
        )
        email_address = EmailAddress.objects.get(user=user)
        self.assertTrue(email_address.verified)
        self.assertTrue(email_address.primary)
        self.assertEqual(email_address.email, 'admin@example.com')

    def test_create_user_has_verified_email(self):
        user = User.objects.create_user(
            email='regular@example.com',
            first_name='Regular',
            last_name='User',
            password='ComplexPass123!',
        )
        email_address = EmailAddress.objects.get(user=user)
        self.assertTrue(email_address.verified)
        self.assertTrue(email_address.primary)
        self.assertEqual(email_address.email, 'regular@example.com')
