import json
from rest_framework.views import status

from tests.base import BaseTestClass

class FinanceViewsTestCase(BaseTestClass):

    def test_create_transactions(self):
        token = self.authenticate()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(
            self.transactions_url,
            data=json.dumps(self.transaction_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 

    def test_get_transactions(self):
        token = self.authenticate()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(
            self.transactions_url,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_limits(self):
        token = self.authenticate()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(
            self.limits_url,
            data=json.dumps(self.limit_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_limits(self):
        token = self.authenticate()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(
            self.limits_url,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)