from django.db.utils import IntegrityError
from django.test import TestCase

from app.accounts.models import User
from app.finance.models import Tag, Transaction


class BaseFinanceModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(first_name='James', last_name='Njenga',
                                        password='this!@#', email='jamesnjenga@gmail.com')


class TagModelTestCase(BaseFinanceModelsTestCase):
    def test_successful_tag_creation(self):
        tag = Tag.objects.create(
            created_by=self.user,
            name='salary'
        )

        self.assertEqual(tag.name, 'salary')

    def test_successful_tag_description(self):
        tag = Tag.objects.create(
            created_by=self.user,
            name='salary',
            description='The description of this tag'
        )

        self.assertEqual(tag.description, 'The description of this tag')

    def test_no_tag_creator_fails(self):
        with self.assertRaises(IntegrityError):
            Tag.objects.create(
                name='salary'
            )

    def test_tag_color_not_empty(self):
        tag = Tag.objects.create(
            created_by=self.user,
            name='salary'
        )

        self.assertTrue(tag.color)


class TransactionModelTestCase(BaseFinanceModelsTestCase):
    def setUp(self):
        super(TransactionModelTestCase, self).setUp()
        self.tag = Tag.objects.create(
            created_by=self.user,
            name='salary'
        )

    def test_successful_transaction_creation(self):
        transaction = Transaction.objects.create(
            created_by=self.user,
            tag=self.tag,
            amount=100
        )

        self.assertEqual(transaction.amount, 100)
