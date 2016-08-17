from django.contrib.staticfiles.testing import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from pom.pages.adminRegistrationPage import AdminRegistrationPage
from pom.pageUrls import PageUrls
import re

from organization.models import Organization
from django.contrib.auth.models import User
from administrator.models import Administrator

from shift.utils import create_organization, create_country

class SignUpAdmin(LiveServerTestCase):
    '''
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
    '''

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        super(SignUpAdmin, cls).setUpClass()
        cls.page = AdminRegistrationPage(cls.driver)

    def setUp(self):
        # create an org prior to registration. Bug in Code
        # added to pass CI
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
        self.assertEqual(values['username'],info[0])
        self.assertEqual(values['first_name'],info[1])
        self.assertEqual(values['last_name'],info[2])
        self.assertEqual(values['email'],info[3])
        self.assertEqual(values['address'],info[4])
        self.assertEqual(values['city'],info[5])
        self.assertEqual(values['state'],info[6])
        self.assertEqual(values['country'],info[7])
        self.assertEqual(values['phone'],info[8])
        self.assertEqual(values['organization'],info[9])

    def test_null_values(self):
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_admin_registration_page()

        entry = ['','','','','','','','','','','']
        page.fill_registration_form(entry)

        blocks = page.get_help_blocks()
        self.assertNotEqual(blocks, None)
        # verify that 10 of the fields are compulsory
        self.assertEqual(len(blocks),10)

        # database check to verify that user, administrator are not created
        self.assertEqual(len(User.objects.all()),0)
        self.assertEqual(len(Administrator.objects.all()),0)

    def test_successful_registration(self):
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_message_box_text(),
                page.success_message)

        # database check to verify that user, administrator are created with correct credentials
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Administrator.objects.all()),1)

        # check that empty list not returned for added filters
        self.assertNotEqual(len(User.objects.filter(
            username='admin-username')), 0)
        self.assertNotEqual(len(Administrator.objects.filter(
            email='admin-email@systers.org')), 0)

    def test_name_fields(self):
        # register valid admin user
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(),page.success_message)

        # register a user again with username same as already registered user
        self.assertEqual(self.driver.current_url, self.live_server_url +
                PageUrls.homepage)

        page.get_admin_registration_page()

        entry = ['admin-username','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','admin-email1@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','admin-org']
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(page.get_username_error_text(),
                'User with this Username already exists.')

        # database check to verify that new user, administrator are not created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Administrator.objects.all()),1)

        # test numeric characters in first-name, last-name
        page.get_admin_registration_page()

        entry = ['admin-username-1','admin-password!@#$%^&*()_','admin-first-name-1','admin-last-name-1','admin-email1@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','admin-org']
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(page.get_first_name_error_text(),'Enter a valid value.')
        self.assertEqual(page.get_last_name_error_text(),'Enter a valid value.')

        # database check to verify that new user, administrator are not created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Administrator.objects.all()),1)

        # test special characters in first-name, last-name
        page.get_admin_registration_page()

        entry = ['admin-username','admin-password!@#$%^&*()_','name-!@#$%^&*()_','name-!@#$%^&*()_','admin-email1@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','admin-org']
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(page.get_first_name_error_text(),'Enter a valid value.')
        self.assertEqual(page.get_last_name_error_text(),'Enter a valid value.')

        # database check to verify that new user, administrator are not created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Administrator.objects.all()),1)

        # test length of first-name, last-name not exceed 30
        page.get_admin_registration_page()

        entry = ['admin-username','admin-password!@#$%^&*()_','admin-first-name-!@#$%^&*()_','admin-last-name-!@#$%^&*()_','admin-email1@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','admin-org']
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(),None)
        error_message = page.get_first_name_error_text()
        self.assertTrue(bool(re.search(r'Ensure this value has at most 20 characters', str(error_message))))

        error_message = page.get_last_name_error_text()
        self.assertTrue(bool(re.search(r'Ensure this value has at most 20 characters', str(error_message))))

        # database check to verify that new user, administrator are not created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Administrator.objects.all()),1)

    def test_location_fields(self):
        # test numeric characters in address, city, state, country
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_admin_registration_page()

        entry = ['admin-username-1','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','email1@systers.org','123 New-City address','1 admin-city','007 admin-state','54 admin-country','9999999999','admin-org']
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                page.admin_registration_page)

        #verify that messages are displayed for city, state and country but not address
        self.assertEqual(len(page.get_help_blocks()),3)
        self.assertEqual(page.get_city_error_text(),'Enter a valid value.')
        self.assertEqual(page.get_state_error_text(),'Enter a valid value.')
        self.assertEqual(page.get_country_error_text(),'Enter a valid value.')

        # database check to verify that user, administrator is not created
        self.assertEqual(len(User.objects.all()),0)
        self.assertEqual(len(Administrator.objects.all()),0)

        # test special characters in address, city, state, country
        page.get_admin_registration_page()

        entry = ['admin-username-2','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','email2@systers.org','admin-address!@#$()','!$@%^#&admin-city','!$@%^#&admin-state','&%^*admin-country!@$#','9999999999','admin-org']
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                page.admin_registration_page)

        # verify that messages are displayed for all fields
        self.assertEqual(page.get_address_error_text(),'Enter a valid value.')
        self.assertEqual(page.get_city_error_text(),'Enter a valid value.')
        self.assertEqual(page.get_state_error_text(),'Enter a valid value.')
        self.assertEqual(page.get_country_error_text(),'Enter a valid value.')

        # database check to verify that user, administrator is not created
        self.assertEqual(len(User.objects.all()),0)
        self.assertEqual(len(Administrator.objects.all()),0)

    def test_email_field(self):

        page = self.page
        page.live_server_url = self.live_server_url
        # register valid admin user
        page.register_valid_details()

        # verify successful registration
        self.assertNotEqual(page.get_message_box(),None)
        self.assertEqual(page.get_message_box_text(),page.success_message)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                PageUrls.homepage)

        # Try to register admin again with same email address
        page.get_admin_registration_page()

        entry = ['admin-username-1','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','admin-email@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','admin-org']
        page.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                page.admin_registration_page)
        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(page.get_email_error_text(),
                'Administrator with this Email already exists.')

        # database check to verify that no user, administrator is created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Administrator.objects.all()),1)

    def test_phone_field(self):

        page = self.page
        page.live_server_url = self.live_server_url
        # register valid admin user with valid phone number for country
        page.get_admin_registration_page()

        entry = ['admin-username','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','admin-email@systers.org','admin-address','admin-city','admin-state','India','022 2403 6606','admin-org']
        page.fill_registration_form(entry)

        # verify successful registration
        self.assertNotEqual(page.get_message_box(),None)
        self.assertEqual(page.get_message_box_text(),page.success_message)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                PageUrls.homepage)

        # database check to verify that user, administrator is created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Administrator.objects.all()),1)

        # Try to register admin with incorrect phone number for country
        page.get_admin_registration_page()

        entry = ['admin-username-1','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','admin-email1@systers.org','admin-address','admin-city','admin-state','India','237937913','admin-org']
        page.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                page.admin_registration_page)
        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(page.get_phone_error_text(),
                "This phone number isn't valid for the selected country")

        # database check to verify that no new user, administrator is created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Administrator.objects.all()),1)

        # Use invalid characters in phone number
        page.get_admin_registration_page()

        entry = ['admin-username-1','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','admin-email1@systers.org','admin-address','admin-city','admin-state','India','23&79^37913','admin-org']
        page.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                page.admin_registration_page)
        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(page.get_phone_error_text(),"Please enter a valid phone number")

        # database check to verify that no new user, administrator is created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Administrator.objects.all()),1)

    def test_organization_field(self):

        page = self.page
        page.live_server_url = self.live_server_url
        # test numeric characters in organization
        page.get_admin_registration_page()

        entry = ['admin-username-1','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','email1@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','13 admin-org']
        page.fill_registration_form(entry)

        # verify successful registration
        self.assertNotEqual(page.get_message_box(),None)
        self.assertEqual(page.get_message_box_text(),page.success_message)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                PageUrls.homepage)

        # database check to verify that user, administrator is created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Administrator.objects.all()),1)

        # Use invalid characters in organization
        page.get_admin_registration_page()

        entry = ['admin-username-2','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','email2@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','!$&admin-org']
        page.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                page.admin_registration_page)
        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(page.get_organization_error_text(),"Enter a valid value.")

        # database check to verify that no new user, administrator is created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Administrator.objects.all()),1)

    def test_field_value_retention(self):

        page = self.page
        page.live_server_url = self.live_server_url
        # send invalid value in fields - first name, state, phone, organization
        page.get_admin_registration_page()

        entry = ['admin-username','admin-password!@#$%^&*()_','admin-first-name-3','admin-last-name','email1@systers.org','admin-address','admin-city','admin-state','admin-country','99999.!9999','@#admin-org']
        page.fill_registration_form(entry)

        # verify that user wasn't registered and that field values are not erased
        self.assertEqual(self.driver.current_url, self.live_server_url + page.admin_registration_page)
        details = ['admin-username','admin-first-name-3','admin-last-name','email1@systers.org','admin-address','admin-city','admin-state','admin-country','99999.!9999','@#admin-org']
        self.verify_field_values(details)

        # database check to verify that no user, administrator is created
        self.assertEqual(len(User.objects.all()),0)
        self.assertEqual(len(Administrator.objects.all()),0)

        # send invalid value in fields - last name, address, city, country
        page.get_admin_registration_page()

        entry = ['admin-username','admin-password!@#$%^&*()_','admin-first-name','admin-last-name-3','email1@systers.org','admin-address$@!','admin-city#$','admin-state','admin-country 15','99999.!9999','@#admin-org']
        page.fill_registration_form(entry)

        # verify that user wasn't registered and that field values are not erased
        self.assertEqual(self.driver.current_url, self.live_server_url + page.admin_registration_page)
        details = ['admin-username','admin-first-name','admin-last-name-3','email1@systers.org','admin-address$@!','admin-city#$','admin-state','admin-country 15','99999.!9999','@#admin-org']
        self.verify_field_values(details)

        # database check to verify that no user, administrator is created
        self.assertEqual(len(User.objects.all()),0)
        self.assertEqual(len(Administrator.objects.all()),0)
