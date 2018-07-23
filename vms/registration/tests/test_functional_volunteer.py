# standard party
import re

# third party
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Django
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core import mail

# local Django
from pom.pageUrls import PageUrls
from pom.pages.volunteerRegistrationPage import VolunteerRegistrationPage
from registration.tokens import account_activation_token
from shift.utils import create_organization, create_country


class SignUpVolunteer(LiveServerTestCase):
    """
    SignUpVolunteer Class contains tests to register volunteer User
    Tests included.

    Name Fields:
        - Test Null values
        - Test legit characters in first_name, last_name fields
        - Register volunteer with already registered username
        - Test length of name fields ( 30 char, limit)

    Password Field:
        - Check if password and confirm password are same

    Location Field (Address, City, State, Country):
        - Test Null Values
        - Test legit characters as per Models defined

    Email Field:
        - Test Null Values
        - Test uniqueness of field

    Phone Number Field:
        - Test Null Values
        - Test validity of number against country entered
        - Test legit characters as per Models defined

    Organization Field:
        - Test Null Values
        - Test legit characters as per Models defined

    Retention of fields:
        - Field values are checked to see that they are not lost when the page gets reloaded
    """

    @classmethod
    def setUpClass(cls):
        """Method to initiate class level objects.

        This method initiates Firefox WebDriver, WebDriverWait and
        the corresponding POM objects for this Test Class
        """
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.page = VolunteerRegistrationPage(cls.driver)
        cls.wait = WebDriverWait(cls.driver, 10)
        super(SignUpVolunteer, cls).setUpClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        create_organization()
        # country created so that phone number can be checked
        create_country()

    def tearDown(self):
        """
        Method consists of statements to be executed at
        end of each test.
        """
        pass

    @classmethod
    def tearDownClass(cls):
        """
        Class method to quit the Firefox WebDriver session after
        execution of all tests in class.
        """
        cls.driver.quit()
        super(SignUpVolunteer, cls).tearDownClass()

    def verify_field_values(self, info):
        """
        Utility function to perform assertions on user information.
        :param info:  Iterable containing information of user.
        """
        page = self.page
        values = page.get_field_values()
        self.assertEqual(values['username'], info[0])
        self.assertEqual(values['first_name'], info[1])
        self.assertEqual(values['last_name'], info[2])
        self.assertEqual(values['email'], info[3])
        self.assertEqual(values['address'], info[4])
        self.assertEqual(values['city'], info[5])
        self.assertEqual(values['state'], info[6])
        self.assertEqual(values['country'], info[7])
        self.assertEqual(values['phone'], info[8])
        self.assertEqual(values['organization'], info[9])

    def test_null_values(self):
        """
        Test errors raised when creating user with null values.
        """
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_volunteer_registration_page()

        entry = ['', '', '', '', '', '', '', '', '', '', '', '']
        page.fill_registration_form(entry)

        blocks = page.get_help_blocks()
        self.assertNotEqual(blocks, None)
        # Verify that all of the fields are compulsory
        self.assertEqual(len(blocks), 11)

    def test_activation_email(self):
        u1 = User.objects.create_user(username='volunteer',password='volunteer')
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_message_box_text(), page.confirm_email_message)
        uid = urlsafe_base64_encode(force_bytes(u1.pk))
        token = account_activation_token.make_token(u1)
        response = self.client.get(reverse('registration:activate', args=[uid,token]))
        self.assertEqual(response.status_code, 200)

    def test_successful_registration(self):
        """
        Test registration of user with valid details.
        """
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_message_box_text(), page.confirm_email_message)

    def test_user_registration_with_same_username(self):
        """
        Test error raised when user registers with username which already exists.
        """
        # Register valid volunteer user
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.confirm_email_message)

        # Register a user again with username same as already registered user
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.volunteer_registration_page)
        page.get_volunteer_registration_page()

        entry = [
            'volunteer-username', 'volunteer-password!@#$%^&*()_',
            'volunteer-password!@#$%^&*()_', 'volunteer-first-name',
            'volunteer-last-name',
            'volunteer-email1@systers.org', 'volunteer-address',
            'volunteer-city', 'volunteer-state', 'volunteer-country',
            '9999999999', 'volunteer-org'
        ]
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_username_error_text(),
                         page.USER_EXISTS)

    def test_user_fills_different_passwords(self):
        """
        Test error raised when user inputs different passwords while
        registering.
        """
        # register valid volunteer user
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.confirm_email_message)

        page.get_volunteer_registration_page()

        entry = [
            'volunteer-username-1', 'volunteer-password!@#$%^&*()_',
            'jddvolunteer-password!@#$%^&*()_',
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-email1@systers.org', 'volunteer-address',
            'volunteer-city', 'volunteer-state', 'volunteer-country',
            '9999999999', 'volunteer-org'
        ]
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_password_error_text(),
                         page.NO_MATCH)


    def test_numeric_characters_in_first_and_last_name(self):
        """
        Test error raised when using numeric characters in
        first and last name while registering.
        """
        # register valid volunteer user
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.confirm_email_message)

        page.get_volunteer_registration_page()

        entry = [
            'volunteer-username-1', 'volunteer-password!@#$%^&*()_',
            'volunteer-password!@#$%^&*()_',
            'volunteer-first-name-1', 'volunteer-last-name-1',
            'volunteer-email1@systers.org', 'volunteer-address',
            'volunteer-city', 'volunteer-state', 'volunteer-country',
            '9999999999', 'volunteer-org'
        ]
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_first_name_error_text(),
                         page.ENTER_VALID_VALUE)
        self.assertEqual(page.get_last_name_error_text(),
                         page.ENTER_VALID_VALUE)

    def test_special_characters_in_first_and_last_name(self):
        """
        Test error raised when using special characters in
        first and last name while registering.
        """
        # register valid volunteer user
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.confirm_email_message)

        page.get_volunteer_registration_page()

        entry = [
            'volunteer-username-1', 'volunteer-password!@#$%^&*()_',
            'volunteer-password!@#$%^&*()_',
            'first-name-!@#$%^&*()_', 'last-name!@#$%^&*()_',
            'volunteer-email3@systers.org', 'volunteer-address',
            'volunteer-city', 'volunteer-state', 'volunteer-country',
            '9999999999', 'volunteer-org'
        ]
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_first_name_error_text(),
                         page.ENTER_VALID_VALUE)
        self.assertEqual(page.get_last_name_error_text(),
                         page.ENTER_VALID_VALUE)

    def test_length_of_first_and_last_name(self):
        """
        Test error raised when registering with length of
        first and last name greater than thirty.
        """
        # register valid volunteer user
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.confirm_email_message)

        page.get_volunteer_registration_page()

        entry = [
            'volunteer-username-1', 'volunteer-password!@#$%^&*()_',
            'volunteer-password!@#$%^&*()_',
            'volunteer-first-name-long-asdfghjkl',
            'volunteer-last-name-long-asdfghjkl',
            'volunteer-email4@systers.org', 'volunteer-address',
            'volunteer-city', 'volunteer-state', 'volunteer-country',
            '9999999999', 'volunteer-org'
        ]
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(), None)
        error_message = page.get_first_name_error_text()
        self.assertTrue(
            bool(
                re.search(r'Ensure this value has at most 30 characters',
                          str(error_message))))

        error_message = page.get_last_name_error_text()
        self.assertTrue(
            bool(
                re.search(r'Ensure this value has at most 30 characters',
                          str(error_message))))

    def test_special_characters_in_location(self):
        """
        Test error raised when using special characters in location
        while registering.
        """
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_volunteer_registration_page()

        entry = [
            'volunteer-username-1', 'volunteer-password!@#$%^&*()_',
            'volunteer-password!@#$%^&*()_',
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-email1@systers.org', '123 New-City address',
            '1 volunteer-city', '007 volunteer-state', '54 volunteer-country',
            '9999999999', 'volunteer-org'
        ]
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.volunteer_registration_page)

        self.assertEqual(page.get_city_error_text(), page.ENTER_VALID_VALUE)
        self.assertEqual(page.get_state_error_text(), page.ENTER_VALID_VALUE)
        self.assertEqual(page.get_country_error_text(), page.ENTER_VALID_VALUE)

        page.get_volunteer_registration_page()

        entry = [
            'volunteer-username-2', 'volunteer-password!@#$%^&*()_',
            'volunteer-password!@#$%^&*()_',
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-email2@systers.org', 'volunteer-address!@#$()',
            '!$@%^#&volunteer-city', '!$@%^#&volunteer-state',
            '&%^*volunteer-country!@$#', '9999999999', 'volunteer-org'
        ]
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.volunteer_registration_page)

        # verify that messages are displayed for all fields
        self.assertEqual(page.get_address_error_text(), page.ENTER_VALID_VALUE)
        self.assertEqual(page.get_city_error_text(), page.ENTER_VALID_VALUE)
        self.assertEqual(page.get_state_error_text(), page.ENTER_VALID_VALUE)
        self.assertEqual(page.get_country_error_text(), page.ENTER_VALID_VALUE)

    def test_email_field(self):
        """
        Test error raised when user tries to register with an email
        address which is already in use.
        """
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()

        # verify successful registration
        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.confirm_email_message)
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.volunteer_registration_page)

        # Try to register volunteer again with same email address
        page.get_volunteer_registration_page()

        entry = [
            'volunteer-username-1', 'volunteer-password!@#$%^&*()_',
            'volunteer-password!@#$%^&*()_',
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-email@systers.org', 'volunteer-address',
            'volunteer-city', 'volunteer-state', 'volunteer-country',
            '9999999999', 'volunteer-org'
        ]
        page.fill_registration_form(entry)

        # Verify that volunteer wasn't registered
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.volunteer_registration_page)
        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_email_error_text(),
                         'Volunteer with this Email already exists.')

    def test_phone_in_different_country(self):
        """
        Test validation of phone number in a country.
        """
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_volunteer_registration_page()

        entry = [
            'volunteer-username', 'volunteer-password!@#$%^&*()_',
            'volunteer-password!@#$%^&*()_',
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-email@systers.org', 'volunteer-address',
            'volunteer-city', 'volunteer-state', 'volunteer-country',
            '9999999999', 'volunteer-org'
        ]
        page.fill_registration_form(entry)

        # verify successful registration
        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.confirm_email_message)
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.volunteer_registration_page)

        # Try to register volunteer with incorrect phone number for country
        page.get_volunteer_registration_page()

        entry = [
            'volunteer-username-1', 'volunteer-password!@#$%^&*()_',
            'volunteer-password!@#$%^&*()_',
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-email1@systers.org', 'volunteer-address',
            'volunteer-city', 'volunteer-state', 'India', '237937913',
            'volunteer-org'
        ]
        page.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.volunteer_registration_page)
        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_phone_error_text(),
                         page.INVALID_PHONE_FOR_COUNTRY)

    def test_phone_with_invalid_characters(self):
        """
        Test error raised while using invalid characters in phone number.
        """
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_volunteer_registration_page()

        entry = [
            'volunteer-username-1', 'volunteer-password!@#$%^&*()_',
            'volunteer-password!@#$%^&*()_',
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-email1@systers.org', 'volunteer-address',
            'volunteer-city', 'volunteer-state', 'India', '23&79^37913',
            'volunteer-org'
        ]
        page.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.volunteer_registration_page)
        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_phone_error_text(),
                         page.INVALID_PHONE)

    def test_organization_with_numeric_characters(self):
        """
        Test error raised while using numeric characters in organization name.
        """
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_volunteer_registration_page()

        entry = [
            'volunteer-username-1', 'volunteer-password!@#$%^&*()_',
            'volunteer-password!@#$%^&*()_',
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-email1@systers.org', 'volunteer-address',
            'volunteer-city', 'volunteer-state', 'volunteer-country',
            '9999999999', 'volunteer-org 13'
        ]
        page.fill_registration_form(entry)

        # Verify successful registration
        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.confirm_email_message)
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.volunteer_registration_page)

    def test_organization_with_invalid_characters(self):
        """
        Test error raised while using invalid characters in organization name.
        """
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_volunteer_registration_page()

        entry = [
            'volunteer-username-2', 'volunteer-password!@#$%^&*()_',
            'volunteer-password!@#$%^&*()_',
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-email2@systers.org', 'volunteer-address',
            'volunteer-city', 'volunteer-state', 'volunteer-country',
            '9999999999', '!*^$volunteer-org'
        ]
        page.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.volunteer_registration_page)
        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_organization_error_text(),
                         page.ENTER_VALID_VALUE)


# Retention test are buggy and unstable, issue is open to fix them
# https://github.com/systers/vms/pull/794
'''
    def test_field_value_retention_in_first_name_state_phone_organization(self):
        """
        Test field values are retained in first name, state and phone when entered
        invalid information in form.
        """
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_volunteer_registration_page()

        entry = [
            'volunteer-username', 'volunteer-password!@#$%^&*()_',
            'volunteer-password!@#$%^&*()_',
            'volunteer-first-name-3', 'volunteer-last-name',
            'volunteer-email@systers.org', 'volunteer-address',
            'volunteer-city', 'volunteer-state!', 'volunteer-country',
            '99999.!9999', '@#volunteer-org'
        ]
        page.fill_registration_form(entry)

        # verify that user wasn't registered and that field values are not erased
        self.assertEqual(
            page.remove_i18n(self.driver.current_url),
            self.live_server_url + page.volunteer_registration_page)
        details = [
            'volunteer-username', 'volunteer-first-name-3',
            'volunteer-last-name', 'volunteer-email@systers.org',
            'volunteer-address', 'volunteer-city', 'volunteer-state!',
            'volunteer-country', '99999.!9999', '@#volunteer-org'
        ]
        self.wait.until(EC.presence_of_element_located((By.ID, "id_username")))
        self.verify_field_values(details)

    def test_field_value_retention_in_last_name_address_city_country(self):
        """
        Test field values are retained in last name, address, city and country when entered
        invalid information in form.
        """
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_volunteer_registration_page()

        entry = [
            'volunteer-username', 'volunteer-password!@#$%^&*()_',
            'volunteer-password!@#$%^&*()_',
            'volunteer-first-name', 'volunteer-last-name-3',
            'volunteer-email@systers.org', 'volunteer-address$@!',
            'volunteer-city#$', 'volunteer-state', 'volunteer-country 15',
            '9999999999', 'volunteer-org'
        ]
        page.fill_registration_form(entry)

        # verify that user wasn't registered and that field values are not erased
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.volunteer_registration_page)
        details = [
            'volunteer-username', 'volunteer-first-name',
            'volunteer-last-name-3', 'volunteer-email@systers.org',
            'volunteer-address$@!', 'volunteer-city#$', 'volunteer-state',
            'volunteer-country 15', '9999999999', 'volunteer-org'
        ]
        self.wait.until(EC.presence_of_element_located((By.ID, "id_username")))
        self.wait.until(EC.presence_of_element_located((By.ID, "id_first_name")))
        self.verify_field_values(details)
'''
