import datetime

from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase, APIClient

from app.accounts.models import User
from app.finance.models import Tag


class BaseTestClass(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/v1/rest-auth/login/'
        self.transactions_url = '/api/v1/account/transactions/'
        self.limits_url = '/api/v1/account/limits/'
        self.custom_login_url = '/api/v1/users/login/'
        self.custom_register_url = '/api/v1/users/register/'
        self.transaction_data = {
            'amount': 100,
            "description": "string",
            "tag": "tag"
        }
        self.limit_data = {
            "tag": str(self.get_mock_tag().id),
            "amount": 100,
            "start_date": datetime.datetime.now().isoformat(),
            "enddate": datetime.datetime.now().isoformat(),

        }
        self.valid_registration__email_data = {
            "email": "kwanj@gmail.com",
            "password": "kwanjkay"
        }
        self.valid_registration__phone_data = {
            "phone_number": "+254703852334",
            "password": "kwanjkay"
        }
        self.valid_registration__email_data = {
            "email": "kwanj@gmail.com",
            "password": "kwanjkay"
        }
        self.invalid_registration__email_data = {
            "email": "kwanjmail.com",
            "password": "kwanjkay"
        }
        self.invalid_registration__phone_data = {
            "phone_number": "+2547038525334",
            "password": "kwanjkay"
        }
        self.no_data = {
            "password": "kwanjkay"
        }
        self.no_password = {
            "phone_number": "+2547038525334"
        }

        self.user = None

    def authenticate(self):
        user =self.get_mock_user()

        response = self.client.post(self.login_url, {
            'email': user.email,
            'password': 'this!@#'
        })
        return response.data['key']

    def get_mock_tag(self):
        return Tag.objects.create(
            created_by=self.get_mock_user(),
            name='salary'
        )

    def get_mock_user(self):
        user = User.objects.filter(email='agnesnzani@gmail.com').first()
        if user is None:
            user = User.objects.create(
                first_name='Agnes',
                last_name='Nzani',
                password=make_password('this!@#'),
                email='agnesnzani@gmail.com')

        return user