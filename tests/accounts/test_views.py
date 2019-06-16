from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client

from app.accounts.models import User
from tests.base import BaseTestClass


class AccountViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_proper_creation(self):
        response = self.client.post('/api/v1/rest-auth/registration/', {
            'first_name': 'John',
            'last_name': 'Otieno',
            'password1': 'acpas!@#',
            'password2': 'acpas!@#',
            'username': 'johnee@gmail.com',
            'email': 'john@gmail.com'
        })

        self.assertEqual(response.status_code, 201)

    def test_not_matching_passwords(self):
        response = self.client.post('/api/v1/rest-auth/registration/', {
            'first_name': 'John',
            'last_name': 'Otieno',
            'password1': 'acpas!@#',
            'password2': 'acpas!@',
            'username': 'johnee@gmail.com',
            'email': 'john@gmail.com'
        })

        self.assertEqual(response.status_code, 400)

    def test_short_passwords(self):
        response = self.client.post('/api/v1/rest-auth/registration/', {
            'first_name': 'John',
            'last_name': 'Otieno',
            'password1': 'acpas',
            'password2': 'acpas',
            'username': 'johnee@gmail.com',
            'email': 'john@gmail.com'
        })

        self.assertEqual(response.status_code, 400)

    def test_login(self):
        User.objects.create(
            first_name='Agnes',
            last_name='Nzani',
            password=make_password('this!@#'),
            email='agnesnzani@gmail.com'
        )

        response = self.client.post('/api/v1/rest-auth/login/', {
            'email': 'agnesnzani@gmail.com',
            'password': 'this!@#'
        })

        self.assertEqual(response.status_code, 200)


class AccountCustomAuthTests(BaseTestClass):
    def test_registration_with_email(self):
        response = self.client.post(
            self.custom_register_url,
            self.valid_registration__email_data
        )
        self.assertEqual(response.status_code, 201)

    def test_registration_with_phone(self):
        response = self.client.post(
            self.custom_register_url,
            self.valid_registration__phone_data
        )
        self.assertEqual(response.status_code, 201)

    def test_login_with_email(self):
        self.client.post(
            self.custom_register_url,
            self.valid_registration__email_data
        )
        response = self.client.post(
            self.custom_login_url,
            self.valid_registration__email_data
        )
        self.assertEqual(response.status_code, 200)

    def test_login_with_phone(self):
        self.client.post(
            self.custom_register_url,
            self.valid_registration__phone_data
        )
        response = self.client.post(
            self.custom_login_url,
            self.valid_registration__phone_data
        )
        self.assertEqual(response.status_code, 200)

    def test_registration_with_invalid_email(self):
        response = self.client.post(
            self.custom_register_url,
            self.invalid_registration__email_data
        )
        self.assertEqual(response.status_code, 400)

    def test_registration_with_invalid_phone(self):
        response = self.client.post(
            self.custom_register_url,
            self.invalid_registration__phone_data
        )
        self.assertEqual(response.status_code, 400)

    def test_registration_with_no_data(self):
        response = self.client.post(
            self.custom_register_url,
            self.no_data
        )
        self.assertEqual(response.status_code, 400)

    def test_registration_with_existing_email(self):
        self.client.post(
            self.custom_register_url,
            self.valid_registration__email_data
        )
        response = self.client.post(
            self.custom_register_url,
            self.valid_registration__email_data
        )
        self.assertEqual(response.status_code, 400)

    def test_registration_with_existing_phone(self):
        self.client.post(
            self.custom_register_url,
            self.valid_registration__phone_data
        )
        response = self.client.post(
            self.custom_register_url,
            self.valid_registration__phone_data
        )
        self.assertEqual(response.status_code, 400)

    def test_login_with_no_data(self):
        response = self.client.post(
            self.custom_login_url,
            self.no_data
        )
        self.assertEqual(response.status_code, 400)

    def test_login_with_no_password(self):
        response = self.client.post(
            self.custom_login_url,
            self.no_password
        )
        self.assertEqual(response.status_code, 400)

    def test_login_with_non_existing(self):
        response = self.client.post(
            self.custom_login_url,
            self.valid_registration__email_data
        )
        self.assertEqual(response.status_code, 400)
