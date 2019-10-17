"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
from django.test import TestCase
from django.urls import reverse

from users.models import User


class LoggedInApi(TestCase):
    LOGGED_IN_KEY = 'loggedIn'
    GIVEN_NAME_KEY = 'givenName'
    SURNAME_KEY = 'surname'
    EXAMPLE_EMAIL = 'foo@example.com'
    EXAMPLE_PASSWORD = 'Complex1234'
    EXAMPLE_GIVEN_NAME = 'John'
    EXAMPLE_SURNAME = 'Doe'

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(LoggedInApi.EXAMPLE_EMAIL,
                                 LoggedInApi.EXAMPLE_GIVEN_NAME,
                                 LoggedInApi.EXAMPLE_SURNAME,
                                 LoggedInApi.EXAMPLE_PASSWORD)

    def test_logged_out(self):
        response = self.client.get(reverse('logged_in_api'))
        json_response = json.loads(response.content)
        self.assertFalse(json_response[LoggedInApi.LOGGED_IN_KEY])
        self.assertFalse(LoggedInApi.GIVEN_NAME_KEY in json_response)
        self.assertFalse(LoggedInApi.SURNAME_KEY in json_response)

    def test_logged_in(self):
        self.client.login(username=LoggedInApi.EXAMPLE_EMAIL, password=LoggedInApi.EXAMPLE_PASSWORD)
        response = self.client.get(reverse('logged_in_api'))
        json_response = json.loads(response.content)
        self.assertTrue(json_response[LoggedInApi.LOGGED_IN_KEY])
        self.assertEqual(LoggedInApi.EXAMPLE_GIVEN_NAME, json_response[LoggedInApi.GIVEN_NAME_KEY])
        self.assertEqual(LoggedInApi.EXAMPLE_SURNAME, json_response[LoggedInApi.SURNAME_KEY])
