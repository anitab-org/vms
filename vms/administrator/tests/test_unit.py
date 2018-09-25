# third party

# Django
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.test.testcases import TestCase

# local Django
from administrator.models import Administrator
from pom.pages.basePage import BasePage
from shift.utils import (create_admin_with_details, create_country,
                         create_state, create_city)


class AdministratorModelTests(TestCase):
    """
    Contains database tests for
    - administrator create with valid and invalid values.
    - administrator edit with valid and invalid values.
    - administrator delete.
    - administrator model representation.
    """

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        self.country = create_country()
        self.state = create_state()
        self.city = create_city()

    def tearDown(self):
        """
        Method consists of statements to be executed at
        end of each test.
        """
        pass

    def create_valid_administrator(self):
        """
        Utility function to create a valid administrator.
        :return: Event type object
        """
        admin = {
            'username': 'admin-username',
            'password': 'admin-password!@#$%^&*()_',
            'first_name': 'admin-first-name',
            'last_name': 'admin-last-name',
            'email': 'admin-email1@systers.org',
            'address': 'admin-address',
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone_number': '9999999999',
            'organization': 'admin-org'
        }
        return create_admin_with_details(admin)

    def test_valid_model_create(self):
        """
        Database test for model creation with valid values.
        """
        admin = {
            'username': 'admin-username',
            'password': 'admin-password!@#$%^&*()_',
            'first_name': 'admin-first-name',
            'last_name': 'admin-last-name',
            'email': 'admin-email1@systers.org',
            'address': 'admin-address',
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone_number': '9999999999',
            'organization': 'admin-org'
        }
        created_admin = create_admin_with_details(admin)

        # Database check for admin creation
        self.assertEqual(len(Administrator.objects.all()), 1)

        admin_in_db = Administrator.objects.get(
            Q(first_name='admin-first-name')
        )
        # Verify correctness
        self.assertEqual(admin_in_db.first_name, admin['first_name'])
        self.assertEqual(admin_in_db.last_name, admin['last_name'])
        self.assertEqual(admin_in_db.email, admin['email'])
        self.assertEqual(admin_in_db.address, admin['address'])
        self.assertEqual(admin_in_db.city, admin['city'])
        self.assertEqual(admin_in_db.state, admin['state'])
        self.assertEqual(admin_in_db.country, admin['country'])
        self.assertEqual(admin_in_db.phone_number, admin['phone_number'])
        self.assertEqual(str(admin_in_db.organization), admin['organization'])

    def test_invalid_first_name_in_model_create(self):
        """
        Database test for model creation with invalid first name.
        """
        admin = {
            'username': 'adminusername1',
            'password': 'admin-password!@#$%^&*()_',
            'first_name': 'admin~first~name',
            'last_name': 'admin last name',
            'email': 'adminemail2@systers.org',
            'address': 'admin address',
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone_number': '9999999999',
            'organization': 'admin org2'
        }
        created_admin = create_admin_with_details(admin)
        self.assertRaisesRegexp(
            ValidationError,
            BasePage.ENTER_VALID_VALUE,
            created_admin.full_clean
        )

    def test_invalid_last_name_in_model_create(self):
        """
        Database test for model creation with invalid last name.
        """
        admin = {
            'username': 'adminusername2',
            'password': 'admin-password!@#$%^&*()_',
            'first_name': 'admin first name',
            'last_name': 'admin~last~name',
            'email': 'adminemail3@systers.org',
            'address': 'admin address',
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone_number': '9999999999',
            'organization': 'admin org3'
        }
        created_admin = create_admin_with_details(admin)
        self.assertRaisesRegexp(
            ValidationError,
            BasePage.ENTER_VALID_VALUE,
            created_admin.full_clean
        )

    def test_invalid_city_in_model_create(self):
        """
        Database test for model creation with invalid city.
        """
        admin = {
            'username': 'adminusername5',
            'password': 'admin-password!@#$%^&*()_',
            'first_name': 'admin first name',
            'last_name': 'admin last name',
            'email': 'adminemail6@systers.org',
            'address': 'admin address',
            'city': 'admin~city',
            'state': self.state,
            'country': self.country,
            'phone_number': '9999999999',
            'organization': 'admin org6'
        }

        self.assertRaisesRegexp(ValueError,
                                'Cannot assign "\'admin~city\'": '
                                '"Administrator.city" must be '
                                'a "City" instance.',
                                create_admin_with_details, admin)

    def test_invalid_state_in_model_create(self):
        """
        Database test for model creation with invalid state.
        """
        admin = {
            'username': 'adminusername6',
            'password': 'admin-password!@#$%^&*()_',
            'first_name': 'admin first name',
            'last_name': 'admin last name',
            'email': 'adminemail7@systers.org',
            'address': 'admin address',
            'city': self.city,
            'state': 'admin~state',
            'country': self.country,
            'phone_number': '9999999999',
            'organization': 'admin org7'
        }

        self.assertRaisesRegexp(ValueError,
                                'Cannot assign "\'admin~state\'": '
                                '"Administrator.state" must be '
                                'a "Region" instance.',
                                create_admin_with_details, admin)

    def test_invalid_country_in_model_create(self):
        """
        Database test for model creation with invalid country.
        """
        admin = {
            'username': 'adminusername7',
            'password': 'admin-password!@#$%^&*()_',
            'first_name': 'admin first name',
            'last_name': 'admin last name',
            'email': 'adminemail7@systers.org',
            'address': 'admin address',
            'city': self.city,
            'state': self.state,
            'country': 'admin~country',
            'phone_number': '9999999999',
            'organization': 'admin org7'
        }

        self.assertRaisesRegexp(ValueError,
                                'Cannot assign "\'admin~country\'": '
                                '"Administrator.country" must be '
                                'a "Country" instance.',
                                create_admin_with_details, admin)

    def test_invalid_email_in_model_create(self):
        """
        Database test for model creation with invalid email.
        """
        admin = {
            'username': 'adminusername3',
            'password': 'admin-password!@#$%^&*()_',
            'first_name': 'admin first name',
            'last_name': 'admin last name',
            'email': 'adminemail4~systers.org',
            'address': 'admin address',
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone_number': '9999999999',
            'organization': 'admin org4'
        }
        created_admin = create_admin_with_details(admin)
        self.assertRaisesRegexp(
            ValidationError,
            'Enter a valid email address.',
            created_admin.full_clean)

    def test_invalid_address_in_model_create(self):
        """
        Database test for model creation with invalid address.
        """
        admin = {
            'username': 'adminusername4',
            'password': 'admin-password!@#$%^&*()_',
            'first_name': 'admin first name',
            'last_name': 'admin last name',
            'email': 'adminemail5@systers.org',
            'address': 'admin!address!',
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone_number': '9999999999',
            'organization': 'admin org5'
        }
        created_admin = create_admin_with_details(admin)
        self.assertRaisesRegexp(
            ValidationError,
            BasePage.ENTER_VALID_VALUE,
            created_admin.full_clean
        )

    def test_invalid_phone_number_in_model_create(self):
        """
        Database test for model creation with invalid phone number.
        """
        admin = {
            'username': 'adminusername8',
            'password': 'admin-password!@#$%^&*()_',
            'first_name': 'admin first name',
            'last_name': 'admin last name',
            'email': 'adminemail9@systers.org',
            'address': 'admin address',
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone_number': '99999999~99',
            'organization': 'admin org9'
        }
        created_admin = create_admin_with_details(admin)
        self.assertRaisesRegexp(
            ValidationError,
            'Please enter a valid phone number',
            created_admin.full_clean
        )

    def test_model_edit_with_valid_values(self):
        """
        Database test for model edit with valid values.
        """
        created_admin = self.create_valid_administrator()

        # Verify creation
        self.assertEqual(len(Administrator.objects.all()), 1)

        # Edit values
        admin_in_db = Administrator.objects.get(Q(last_name='admin-last-name'))
        admin_in_db.first_name = 'new-first-name'
        admin_in_db.email = 'newemail@systers.org'
        admin_in_db.save()

        admin_in_db = Administrator.objects.get(Q(last_name='admin-last-name'))
        # Check values
        self.assertEqual(admin_in_db.first_name, 'new-first-name')
        self.assertEqual(admin_in_db.last_name, created_admin.last_name)
        self.assertEqual(admin_in_db.email, 'newemail@systers.org')
        self.assertEqual(admin_in_db.address, created_admin.address)
        self.assertEqual(admin_in_db.city, created_admin.city)
        self.assertEqual(admin_in_db.state, created_admin.state)
        self.assertEqual(admin_in_db.country, created_admin.country)
        self.assertEqual(admin_in_db.phone_number, created_admin.phone_number)

    def test_model_edit_with_invalid_values(self):
        """
        Database test for model edit with invalid values.
        """
        created_admin = self.create_valid_administrator()

        # Verify creation
        self.assertEqual(len(Administrator.objects.all()), 1)

        # Edit values
        admin_in_db = Administrator.objects.get(Q(last_name='admin-last-name'))
        admin_in_db.first_name = 'new!first!name'
        admin_in_db.save()

        self.assertRaisesRegexp(
            ValidationError,
            BasePage.ENTER_VALID_VALUE,
            admin_in_db.full_clean
        )

    def test_model_delete(self):
        """
        Database test for model deletion.
        """
        created_admin = self.create_valid_administrator()

        # Verify creation.
        self.assertEqual(len(Administrator.objects.all()), 1)

        admin_in_db = Administrator.objects.get(Q(last_name='admin-last-name'))
        # Basic checks to verify correct object.
        self.assertEqual(admin_in_db.first_name, created_admin.first_name)
        self.assertEqual(admin_in_db.last_name, created_admin.last_name)
        self.assertEqual(admin_in_db.email, created_admin.email)

        admin_in_db.delete()
        # Check if delete is successful.
        self.assertEqual(len(Administrator.objects.all()), 0)

    def test_model_representation(self):
        """
        Database test for model representation.
        """
        created_admin = self.create_valid_administrator()

        # Verify creation.
        self.assertEqual(len(Administrator.objects.all()), 1)

        admin_in_db = Administrator.objects.get(Q(last_name='admin-last-name'))
        # Basic checks to verify correct object.
        self.assertEqual(admin_in_db.first_name, created_admin.first_name)
        self.assertEqual(admin_in_db.last_name, created_admin.last_name)
        self.assertEqual(admin_in_db.email, created_admin.email)

        # Check representation
        self.assertEqual(str(admin_in_db), created_admin.user.username)
