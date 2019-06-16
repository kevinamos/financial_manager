from django.core.exceptions import ValidationError
from django.test import TestCase
from app.accounts.models import User


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(first_name='James', last_name='Njenga',
                            password='this!@#', email='jamesnjenga@gmail.com')
        User.objects.create(first_name='Agnes', last_name='Nzani',
                            password='this!@#', email='agnesnzani@gmail.com')
        User.objects.create_superuser(
            password='this!@#tet', email='agnesddddnzani@gmail.com')

    def test_user_string_formating(self):
        james = User.objects.get(email='jamesnjenga@gmail.com')

        self.assertEqual(james.__str__(), '%s %s - %s' %
                         (james.first_name, james.last_name, james.email))

    def test_users_have_full_names(self):
        """
        Users have full_names

        """
        james = User.objects.get(email='jamesnjenga@gmail.com')
        agnes = User.objects.get(email='agnesnzani@gmail.com')
        self.assertEqual(james.full_name, 'James Njenga')
        self.assertEqual(agnes.full_name, 'Agnes Nzani')

    def test_user_valid_phone_number(self):
        james = User.objects.get(email='jamesnjenga@gmail.com')
        james.phone_number = '+254717611434'
        james.save()

        self.assertEqual(james.phone_number, '+254717611434')

    def test_user_invalid_phone_number(self):
        james = User.objects.get(email='jamesnjenga@gmail.com')

        with(self.assertRaises(ValidationError)):
            james.phone_number = '+2547176114342342'
            james.save()

    def test_user_valid_mail(self):
        james = User.objects.get(email='jamesnjenga@gmail.com')
        james.email = 'jamesnjenga1@gmail.com'
        james.save()
        self.assertEqual(james.email, 'jamesnjenga1@gmail.com')

    def test_user_invalid_mail(self):
        james = User.objects.get(email='jamesnjenga@gmail.com')

        with(self.assertRaises(ValidationError)):
            james.email = 'email'
            james.save()
