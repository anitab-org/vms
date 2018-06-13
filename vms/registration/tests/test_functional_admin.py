# standard library
import re

# third party
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from pom.pages.adminRegistrationPage import AdminRegistrationPage
from pom.pageUrls import PageUrls
from shift.utils import create_organization, create_country


class SignUpAdmin(LiveServerTestCase):
    """
    SignUpAdmin Class contains tests to register a admin User
    Tests included.

    Name Fields:
        - Test Null values
        - Test legit characters in first_name, last_name fields
        - Register admin with already registered username
        - Test length of name fields ( 30 char, limit)

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
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.page = AdminRegistrationPage(cls.driver)
        cls.wait = WebDriverWait(cls.driver, 10)
        super(SignUpAdmin, cls).setUpClass()

    def setUp(self):
        create_organization()
        # country created so that phone number can be checked
        create_country()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(SignUpAdmin, cls).tearDownClass()

    def verify_field_values(self, info):
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
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_admin_registration_page()

        entry = ['', '', '', '', '', '', '', '', '', '', '']
        page.fill_registration_form(entry)
        self.assertNotEqual(page.get_help_blocks(), None)
        # Verify that 10 of the fields are compulsory
        self.assertEqual(len(page.get_help_blocks()), 10)

    def test_successful_registration(self):
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_message_box_text(), page.success_message)

    def test_user_registration_with_same_username(self):
        # Register valid admin user
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.success_message)
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + PageUrls.homepage)

        page.get_admin_registration_page()

        entry = [
            'admin-username', 'admin-password!@#$%^&*()_', 'admin-first-name',
            'admin-last-name', 'admin-email1@systers.org', 'admin-address',
            'admin-city', 'admin-state', 'admin-country', '9999999999',
            'admin-org'
        ]
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_username_error_text(),
                         page.USER_EXISTS)

    def test_numeric_characters_in_first_and_last_name(self):
        # Register valid admin user
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.success_message)
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + PageUrls.homepage)

        page.get_admin_registration_page()

        entry = [
            'admin-username-1', 'admin-password!@#$%^&*()_',
            'admin-first-name-1', 'admin-last-name-1',
            'admin-email1@systers.org', 'admin-address', 'admin-city',
            'admin-state', 'admin-country', '9999999999', 'admin-org'
        ]
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_first_name_error_text(),
                         page.ENTER_VALID_VALUE)
        self.assertEqual(page.get_last_name_error_text(),
                         page.ENTER_VALID_VALUE)

    def test_special_characters_in_first_and_last_name(self):
        # Register valid admin user
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.success_message)
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + PageUrls.homepage)

        page.get_admin_registration_page()

        entry = [
            'admin-username', 'admin-password!@#$%^&*()_', 'name-!@#$%^&*()_',
            'name-!@#$%^&*()_', 'admin-email1@systers.org', 'admin-address',
            'admin-city', 'admin-state', 'admin-country', '9999999999',
            'admin-org'
        ]
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_first_name_error_text(),
                         page.ENTER_VALID_VALUE)
        self.assertEqual(page.get_last_name_error_text(),
                         page.ENTER_VALID_VALUE)

    def test_length_of_first_and_last_name(self):
        # Register valid admin user
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.success_message)
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + PageUrls.homepage)

        page.get_admin_registration_page()

        entry = [
            'admin-username', 'admin-password!@#$%^&*()_',
            'admin-first-name-!@#$%^&*()_lolwatneedlength',
            'admin-last-name-!@#$%^&*()_lolwatneedlength',
            'admin-email1@systers.org', 'admin-address', 'admin-city',
            'admin-state', 'admin-country', '9999999999', 'admin-org'
        ]
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(), None)
        error_message = page.get_first_name_error_text()
        print(str(error_message))
        self.assertTrue(
            bool(
                re.search(r'Ensure this value has at most 30 characters',
                          str(error_message))))

        error_message = page.get_last_name_error_text()
        self.assertTrue(
            bool(
                re.search(r'Ensure this value has at most 30 characters',
                          str(error_message))))

    def test_numeric_characters_in_location(self):
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_admin_registration_page()
        entry = [
            'admin-username-1', 'admin-password!@#$%^&*()_',
            'admin-first-name', 'admin-last-name', 'email1@systers.org',
            '123 New-City address', '1 admin-city', '007 admin-state',
            '54 admin-country', '9999999999', 'admin-org'
        ]
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.admin_registration_page)

        # Verify that messages are displayed for city, state and country but not address
        self.assertEqual(len(page.get_help_blocks()), 3)
        self.assertEqual(page.get_city_error_text(), page.ENTER_VALID_VALUE)
        self.assertEqual(page.get_state_error_text(), page.ENTER_VALID_VALUE)
        self.assertEqual(page.get_country_error_text(), page.ENTER_VALID_VALUE)

    def test_special_characters_in_location(self):
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_admin_registration_page()

        entry = [
            'admin-username-2', 'admin-password!@#$%^&*()_',
            'admin-first-name', 'admin-last-name', 'email2@systers.org',
            'admin-address!@#$()', '!$@%^#&admin-city', '!$@%^#&admin-state',
            '&%^*admin-country!@$#', '9999999999', 'admin-org'
        ]
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.admin_registration_page)

        # Verify that messages are displayed for all fields
        self.assertEqual(page.get_address_error_text(), page.ENTER_VALID_VALUE)
        self.assertEqual(page.get_city_error_text(), page.ENTER_VALID_VALUE)
        self.assertEqual(page.get_state_error_text(), page.ENTER_VALID_VALUE)
        self.assertEqual(page.get_country_error_text(), page.ENTER_VALID_VALUE)

    def test_email_field(self):
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()

        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.success_message)
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + PageUrls.homepage)

        # Try to register admin again with same email address
        page.get_admin_registration_page()

        entry = [
            'admin-username-1', 'admin-password!@#$%^&*()_',
            'admin-first-name', 'admin-last-name', 'admin-email@systers.org',
            'admin-address', 'admin-city', 'admin-state', 'admin-country',
            '9999999999', 'admin-org'
        ]
        page.fill_registration_form(entry)

        # Verify that user wasn't registered
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.admin_registration_page)
        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_email_error_text(),
                         'Administrator with this Email already exists.')

    def test_phone_in_different_country(self):
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_admin_registration_page()

        entry = [
            'admin-username', 'admin-password!@#$%^&*()_', 'admin-first-name',
            'admin-last-name', 'admin-email@systers.org', 'admin-address',
            'admin-city', 'admin-state', 'India', '022 2403 6606', 'admin-org'
        ]
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.success_message)
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + PageUrls.homepage)

        # Try to register admin with incorrect phone number for country
        page.get_admin_registration_page()

        entry = [
            'admin-username-1', 'admin-password!@#$%^&*()_',
            'admin-first-name', 'admin-last-name', 'admin-email1@systers.org',
            'admin-address', 'admin-city', 'admin-state', 'India', '237937913',
            'admin-org'
        ]
        page.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.admin_registration_page)
        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_phone_error_text(),
                         page.INVALID_PHONE_FOR_COUNTRY)

    def test_phone_with_invalid_characters(self):
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_admin_registration_page()

        entry = [
            'admin-username', 'admin-password!@#$%^&*()_', 'admin-first-name',
            'admin-last-name', 'admin-email@systers.org', 'admin-address',
            'admin-city', 'admin-state', 'India', '022 2403 6606', 'admin-org'
        ]
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.success_message)
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + PageUrls.homepage)

        page.get_admin_registration_page()

        entry = [
            'admin-username-1', 'admin-password!@#$%^&*()_',
            'admin-first-name', 'admin-last-name', 'admin-email1@systers.org',
            'admin-address', 'admin-city', 'admin-state', 'India',
            '23&79^37913', 'admin-org'
        ]
        page.fill_registration_form(entry)

        # Verify that user wasn't registered
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.admin_registration_page)
        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_phone_error_text(),
                         page.INVALID_PHONE)

    def test_organization_with_numeric_characters(self):
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_admin_registration_page()

        entry = [
            'admin-username-1', 'admin-password!@#$%^&*()_',
            'admin-first-name', 'admin-last-name', 'email1@systers.org',
            'admin-address', 'admin-city', 'admin-state', 'admin-country',
            '9999999999', '13 admin-org'
        ]
        page.fill_registration_form(entry)

        # verify successful registration
        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(), page.success_message)
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + PageUrls.homepage)

    def test_organization_with_invalid_characters(self):
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_admin_registration_page()

        entry = [
            'admin-username-2', 'admin-password!@#$%^&*()_',
            'admin-first-name', 'admin-last-name', 'email2@systers.org',
            'admin-address', 'admin-city', 'admin-state', 'admin-country',
            '9999999999', '!$&admin-org'
        ]
        page.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.admin_registration_page)
        self.assertNotEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_organization_error_text(),
                         page.ENTER_VALID_VALUE)

    def test_field_value_retention_in_first_name_state_phone_organization(self):
        page = self.page
        page.live_server_url = self.live_server_url

        page.get_admin_registration_page()

        entry = [
            'admin-username', 'admin-password!@#$%^&*()_',
            'admin-first-name-3', 'admin-last-name', 'email1@systers.org',
            'admin-address', 'admin-city', 'admin-state', 'admin-country',
            '99999.!9999', '@#admin-org'
        ]
        page.fill_registration_form(entry)

        # Verify that user wasn't registered and that field values are not erased
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.admin_registration_page)
        details = [
            'admin-username', 'admin-first-name-3', 'admin-last-name',
            'email1@systers.org', 'admin-address', 'admin-city', 'admin-state',
            'admin-country', '99999.!9999', '@#admin-org'
        ]
        self.wait.until(EC.presence_of_element_located((By.ID, "id_username")))
        self.verify_field_values(details)

    def test_field_value_retention_in_last_name_address_city_country(self):
        page = self.page
        page.live_server_url = self.live_server_url

        page.get_admin_registration_page()

        entry = [
            'admin-username', 'admin-password!@#$%^&*()_', 'admin-first-name',
            'admin-last-name-3', 'email1@systers.org', 'admin-address$@!',
            'admin-city#$', 'admin-state', 'admin-country 15', '99999.!9999',
            '@#admin-org'
        ]
        page.fill_registration_form(entry)

        # verify that user wasn't registered and that field values are not erased
        self.assertEqual(page.remove_i18n(self.driver.current_url),
                         self.live_server_url + page.admin_registration_page)
        details = [
            'admin-username', 'admin-first-name', 'admin-last-name-3',
            'email1@systers.org', 'admin-address$@!', 'admin-city#$',
            'admin-state', 'admin-country 15', '99999.!9999', '@#admin-org'
        ]
        self.wait.until(EC.presence_of_element_located((By.ID, "id_username")))
        self.verify_field_values(details)

