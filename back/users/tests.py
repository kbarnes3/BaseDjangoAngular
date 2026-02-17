"""Tests for users app and allauth headless API."""
from django.test import TestCase

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
