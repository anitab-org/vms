# third party

# Django
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.test.testcases import TestCase

# local Django
from pom.pages.basePage import BasePage
from shift.utils import (create_organization_with_details,
                         create_country, create_state,
                         create_city, create_volunteer_with_details)
from volunteer.models import Volunteer


class VolunteerModelTests(TestCase):
    """
    Contains database tests for
    - volunteer create with valid and invalid values.
    - volunteer edit with valid and invalid values.
    - volunteer delete.
    - volunteer model representation.
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

    def create_valid_vol(self):
        """
        Utility function to create a valid volunteer.
        :return: Volunteer type object
        """
        vol = {
            'username': 'Goku',
            'first_name': "Son",
            'last_name': "Goku",
            'address': "Kame House",
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone_number': "9999999999",
            'email': "idonthave@gmail.com"
        }
        org_name = 'organization'
        org_obj = create_organization_with_details(org_name)
        return create_volunteer_with_details(vol, org_obj)

    def create_invalid_vol(self):
        """
        Utility function to create an invalid volunteer.
        :return: Volunteer type object
        """
        vol = {
            'username': 'Goku~',
            'first_name': "Son",
            'last_name': "Goku",
            'address': "Kame House",
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone_number': "9999999999",
            'email': "idonthave1@gmail.com"
        }
        org_name = 'org'
        org_obj = create_organization_with_details(org_name)
        return create_volunteer_with_details(vol, org_obj)

    def test_valid_model_create(self):
        """
        Database test for model creation with valid values.
        """
        valid_volunteer = self.create_valid_vol()

        # Check DB for volunteer create.
        self.assertEqual(len(Volunteer.objects.all()), 1)

        volunteer_in_db = Volunteer.objects.get(Q(first_name='Son'))
        # Verify correctness.
        self.assertEqual(valid_volunteer.first_name, volunteer_in_db.first_name)
        self.assertEqual(valid_volunteer.last_name, volunteer_in_db.last_name)
        self.assertEqual(valid_volunteer.email, volunteer_in_db.email)
        self.assertEqual(
            valid_volunteer.phone_number,
            volunteer_in_db.phone_number
        )

    def test_invalid_username_in_model_create(self):
        """
        Database test for model creation with invalid username.
        """
        volunteer = {
            'username': '',
            'first_name': "Son",
            'last_name': "Goku",
            'address': "Kame House",
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone_number': "9999999999",
            'email': "idonthave@gmail.com"
        }
        org_name = 'org'
        org_obj = create_organization_with_details(org_name)
        self.assertRaisesRegexp(ValueError,
                                'The given username must be set',
                                create_volunteer_with_details,
                                volunteer, org_obj)

    def test_invalid_first_name_in_model_create(self):
        """
        Database test for model creation with invalid first name.
        """
        volunteer = {
            'username': 'Goku2',
            'first_name': "Son~",
            'last_name': "Goku",
            'address': "Kame House",
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone_number': "9999999999",
            'email': "idonthave2@gmail.com"
        }
        org_name = 'org'
        org_obj = create_organization_with_details(org_name)
        created_volunteer = create_volunteer_with_details(volunteer, org_obj)
        self.assertRaisesRegexp(
            ValidationError,
            BasePage.ENTER_VALID_VALUE,
            created_volunteer.full_clean
        )

    def test_invalid_last_name_in_model_create(self):
        """
        Database test for model creation with invalid last name.
        """
        volunteer = {
            'username': 'Goku3',
            'first_name': "Son",
            'last_name': "Goku!",
            'address': "Kame House",
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone_number': "9999999999",
            'email': "idonthave3@gmail.com"
        }
        org_name = 'org'
        org_obj = create_organization_with_details(org_name)
        created_volunteer = create_volunteer_with_details(volunteer, org_obj)
        self.assertRaisesRegexp(
            ValidationError,
            BasePage.ENTER_VALID_VALUE,
            created_volunteer.full_clean
        )

    def test_invalid_city_in_model_create(self):
        """
        Database test for model creation with invalid city.
        """
        volunteer = {
            'username': 'Goku5',
            'first_name': "Son",
            'last_name': "Goku",
            'address': "Kame House",
            'city': "East!District!",
            'state': self.state,
            'country': self.country,
            'phone_number': "9999999999",
            'email': "idonthave@gmail.com"
        }
        org_name = 'org'
        org_obj = create_organization_with_details(org_name)
        self.assertRaisesRegexp(ValueError,
                                'Cannot assign "\'East!District!\'": '
                                '"Volunteer.city" must be '
                                'a "City" instance.',
                                create_volunteer_with_details,
                                volunteer, org_obj)

    def test_invalid_state_in_model_create(self):
        """
        Database test for model creation with invalid state.
        """
        volunteer = {
            'username': 'Goku6',
            'first_name': "Son",
            'last_name': "Goku",
            'address': "Kame House",
            'city': self.city,
            'state': "East!District!",
            'country': self.country,
            'phone_number': "9999999999",
            'email': "idonthave6@gmail.com"
        }
        org_name = 'org'
        org_obj = create_organization_with_details(org_name)
        self.assertRaisesRegexp(ValueError,
                                'Cannot assign "\'East!District!\'": '
                                '"Volunteer.state" must be '
                                'a "Region" instance.',
                                create_volunteer_with_details,
                                volunteer, org_obj)

    def test_invalid_country_in_model_create(self):
        """
        Database test for model creation with invalid country.
        """
        volunteer = {
            'username': 'Goku7',
            'first_name': "Son",
            'last_name': "Goku",
            'address': "Kame House",
            'city': self.city,
            'state': self.state,
            'country': "East!District!",
            'phone_number': "9999999999",
            'email': "idonthave7@gmail.com"
        }
        org_name = 'org'
        org_obj = create_organization_with_details(org_name)
        self.assertRaisesRegexp(ValueError,
                                'Cannot assign "\'East!District!\'": '
                                '"Volunteer.country" must be '
                                'a "Country" instance.',
                                create_volunteer_with_details,
                                volunteer, org_obj)

    def test_invalid_address_in_model_create(self):
        """
        Database test for model creation with invalid address.
        """
        volunteer = {
            'username': 'Goku4',
            'first_name': "Son",
            'last_name': "Goku",
            'address': "Kame!House!",
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone_number': "9999999999",
            'email': "idonthave4@gmail.com"
        }
        org_name = 'org'
        org_obj = create_organization_with_details(org_name)
        created_volunteer = create_volunteer_with_details(volunteer, org_obj)
        self.assertRaisesRegexp(
            ValidationError,
            BasePage.ENTER_VALID_VALUE,
            created_volunteer.full_clean
        )

    def test_invalid_phone_number_in_model_create(self):
        """
        Database test for model creation with invalid phone number.
        """
        volunteer = {
            'username': 'Goku8',
            'first_name': "Son",
            'last_name': "Goku",
            'address': "Kame House",
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone_number': "99999999!9",
            'email': "idonthave8@gmail.com"
        }
        org_name = 'org'
        org_obj = create_organization_with_details(org_name)
        created_volunteer = create_volunteer_with_details(volunteer, org_obj)
        self.assertRaisesRegexp(
            ValidationError,
            'Please enter a valid phone number',
            created_volunteer.full_clean
        )

    def test_invalid_email_in_model_create(self):
        """
        Database test for model creation with invalid email.
        """
        volunteer = {
            'username': 'Goku9',
            'first_name': "Son",
            'last_name': "Goku",
            'address': "Kame House",
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'phone_number': "9999999999",
            'email': "idonthave9~gmail.com"
        }
        org_name = 'org'
        org_obj = create_organization_with_details(org_name)
        created_volunteer = create_volunteer_with_details(volunteer, org_obj)
        self.assertRaisesRegexp(
            ValidationError,
            'Enter a valid email address.',
            created_volunteer.full_clean
        )

    def test_model_edit_with_valid_values(self):
        """
        Database test for model edit with valid values.
        """
        valid_volunteer = self.create_valid_vol()

        # Check DB for volunteer create.
        self.assertEqual(len(Volunteer.objects.all()), 1)

        volunteer_in_db = Volunteer.objects.get(Q(first_name='Son'))
        # Verify correctness.
        self.assertEqual(valid_volunteer.first_name, volunteer_in_db.first_name)
        self.assertEqual(valid_volunteer.last_name, volunteer_in_db.last_name)
        self.assertEqual(valid_volunteer.email, volunteer_in_db.email)
        self.assertEqual(
            valid_volunteer.phone_number,
            volunteer_in_db.phone_number
        )

        valid_volunteer.first_name = 'Prince'
        valid_volunteer.last_name = 'Vegeta'
        valid_volunteer.email = 'iwishihadone@gmail.com'
        valid_volunteer.phone_number = '1234567890'
        valid_volunteer.save()

        # Check single instance
        self.assertEqual(len(Volunteer.objects.all()), 1)

        volunteer_in_db = Volunteer.objects.get(Q(first_name='Prince'))
        # Verify correctness.
        self.assertEqual(valid_volunteer.first_name, volunteer_in_db.first_name)
        self.assertEqual(valid_volunteer.last_name, volunteer_in_db.last_name)
        self.assertEqual(valid_volunteer.email, volunteer_in_db.email)
        self.assertEqual(
            valid_volunteer.phone_number,
            volunteer_in_db.phone_number
        )

    def test_model_edit_with_invalid_values(self):
        """
        Database test for model edit with invalid values.
        """
        valid_volunteer = self.create_valid_vol()

        # Check DB for volunteer create.
        self.assertEqual(len(Volunteer.objects.all()), 1)

        volunteer_in_db = Volunteer.objects.get(Q(first_name='Son'))
        # Verify correctness.
        self.assertEqual(valid_volunteer.first_name, volunteer_in_db.first_name)
        self.assertEqual(valid_volunteer.last_name, volunteer_in_db.last_name)
        self.assertEqual(valid_volunteer.email, volunteer_in_db.email)
        self.assertEqual(
            valid_volunteer.phone_number,
            volunteer_in_db.phone_number
        )

        valid_volunteer.first_name = ''
        valid_volunteer.last_name = 'Vegeta'
        valid_volunteer.email = 'iwishihadone@gmail.com'
        valid_volunteer.phone_number = '1234567890'

        # Check save isn't working.
        self.assertRaisesRegexp(
            ValidationError,
            BasePage.FIELD_CANNOT_LEFT_BLANK,
            valid_volunteer.full_clean
        )
        # Check single instance
        self.assertEqual(len(Volunteer.objects.all()), 1)

    def test_model_delete(self):
        """
        Database test for model deletion.
        """
        valid_volunteer = self.create_valid_vol()

        # Check DB for volunteer create.
        self.assertEqual(len(Volunteer.objects.all()), 1)

        volunteer_in_db = Volunteer.objects.get(Q(first_name='Son'))
        # Verify correctness.
        self.assertEqual(valid_volunteer.first_name, volunteer_in_db.first_name)
        self.assertEqual(valid_volunteer.last_name, volunteer_in_db.last_name)
        self.assertEqual(valid_volunteer.email, volunteer_in_db.email)
        self.assertEqual(
            valid_volunteer.phone_number,
            volunteer_in_db.phone_number
        )

        volunteer_in_db.delete()

        # Check 0 instance
        self.assertEqual(len(Volunteer.objects.all()), 0)

    def test_model_representation(self):
        """
        Database test for model representation.
        """
        valid_volunteer = self.create_valid_vol()

        # Check DB for volunteer create.
        self.assertEqual(len(Volunteer.objects.all()), 1)

        volunteer_in_db = Volunteer.objects.get(Q(first_name='Son'))
        # Verify correctness.
        self.assertEqual(valid_volunteer.first_name, volunteer_in_db.first_name)
        self.assertEqual(valid_volunteer.last_name, volunteer_in_db.last_name)
        self.assertEqual(valid_volunteer.email, volunteer_in_db.email)
        self.assertEqual(
            valid_volunteer.phone_number,
            volunteer_in_db.phone_number
        )

        # Check representation
        self.assertEqual(str(volunteer_in_db), 'Son Goku')

