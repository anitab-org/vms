# third party

# Django
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.test.testcases import TestCase

# local Django
from administrator.models import Administrator
from pom.pages.basePage import BasePage
from shift.utils import create_admin_with_details


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
        pass

    def tearDown(self):
        """
        Method consists of statements to be executed at
        end of each test.
        """
        pass

    @staticmethod
    def create_valid_administrator():
        """
        Utility function to create a valid administrator.
        :return: Event type object
        """
        admin = [
            'admin-username', 'admin-password!@#$%^&*()_', 'admin-first-name',
            'admin-last-name', 'admin-email1@systers.org', 'admin-address',
            'admin-city', 'admin-state', 'admin-country', '9999999999',
            'admin-org'
        ]
        return create_admin_with_details(admin)

    def test_valid_model_create(self):
        """
        Database test for model creation with valid values.
        """
        admin = [
            'admin-username', 'admin-password!@#$%^&*()_', 'admin-first-name',
            'admin-last-name', 'admin-email1@systers.org', 'admin-address',
            'admin-city', 'admin-state', 'admin-country', '9999999999',
            'admin-org'
        ]
        created_admin = create_admin_with_details(admin)

        # Database check for admin creation
        self.assertEqual(len(Administrator.objects.all()), 1)

        admin_in_db = Administrator.objects.get(Q(first_name='admin-first-name'))
        # Verify correctness
        self.assertEqual(admin_in_db.first_name, admin[2])
        self.assertEqual(admin_in_db.last_name, admin[3])
        self.assertEqual(admin_in_db.email, admin[4])
        self.assertEqual(admin_in_db.address, admin[5])
        self.assertEqual(admin_in_db.city, admin[6])
        self.assertEqual(admin_in_db.state, admin[7])
        self.assertEqual(admin_in_db.country, admin[8])
        self.assertEqual(admin_in_db.phone_number, admin[9])
        self.assertEqual(admin_in_db.unlisted_organization, admin[10])

    def test_invalid_model_create(self):
        """
        Database test for model creation with invalid values.
        """
        admin = [
            'admin-username', 'admin-password!@#$%^&*()_', 'admin!first!name',
            'admin-last-name', 'admin-email1@systers.org', 'admin-address',
            'admin-city', 'admin-state', 'admin-country', '9999999999',
            'admin-org'
        ]
        created_admin = create_admin_with_details(admin)
        self.assertRaisesRegexp(ValidationError, BasePage.ENTER_VALID_VALUE, created_admin.full_clean)

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
        self.assertEqual(admin_in_db.unlisted_organization, created_admin.unlisted_organization)

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

        self.assertRaisesRegexp(ValidationError, BasePage.ENTER_VALID_VALUE, admin_in_db.full_clean)

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
        self.assertEqual(admin_in_db.user.username, created_admin.user.username)
