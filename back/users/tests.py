"""
Tests for users app and allauth headless API.
"""
import json
from django.test import TestCase
from django.urls import reverse

from users.models import User


class LoggedInApi(TestCase):
    LOGGED_IN_KEY = 'loggedIn'
    FIRST_NAME_KEY = 'firstName'
    LAST_NAME_KEY = 'lastName'
    EXAMPLE_EMAIL = 'foo@example.com'
    EXAMPLE_PASSWORD = 'Complex1234'
    EXAMPLE_FIRST_NAME = 'John'
    EXAMPLE_LAST_NAME = 'Doe'

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(LoggedInApi.EXAMPLE_EMAIL,
                                 LoggedInApi.EXAMPLE_FIRST_NAME,
                                 LoggedInApi.EXAMPLE_LAST_NAME,
                                 LoggedInApi.EXAMPLE_PASSWORD)

    def test_logged_out(self):
        response = self.client.get(reverse('logged_in_api'))
        json_response = json.loads(response.content)
        self.assertFalse(json_response[LoggedInApi.LOGGED_IN_KEY])
        self.assertFalse(LoggedInApi.FIRST_NAME_KEY in json_response)
        self.assertFalse(LoggedInApi.LAST_NAME_KEY in json_response)

    def test_logged_in(self):
        self.client.login(username=LoggedInApi.EXAMPLE_EMAIL, password=LoggedInApi.EXAMPLE_PASSWORD)
        response = self.client.get(reverse('logged_in_api'))
        json_response = json.loads(response.content)
        self.assertTrue(json_response[LoggedInApi.LOGGED_IN_KEY])
        self.assertEqual(LoggedInApi.EXAMPLE_FIRST_NAME, json_response[LoggedInApi.FIRST_NAME_KEY])
        self.assertEqual(LoggedInApi.EXAMPLE_LAST_NAME, json_response[LoggedInApi.LAST_NAME_KEY])


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
