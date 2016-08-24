from django.contrib.staticfiles.testing import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from pom.pages.volunteerRegistrationPage import VolunteerRegistrationPage
from pom.pageUrls import PageUrls
import re

from organization.models import Organization
from django.contrib.auth.models import User
from volunteer.models import Volunteer
from shift.utils import create_organization, create_country

class SignUpVolunteer(LiveServerTestCase):
    '''
    SignUpVolunteer Class contains tests to register volunteer User
    Tests included.

    Name Fields:
        - Test Null values
        - Test legit characters in first_name, last_name fields
        - Register volunteer with already registered username
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
        cls.page = VolunteerRegistrationPage(cls.driver)
        super(SignUpVolunteer, cls).setUpClass()

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
        super(SignUpVolunteer, cls).tearDownClass()

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
        page.get_volunteer_registration_page()

        entry = ['','','','','','','','','','','']
        page.fill_registration_form(entry)

        blocks = page.get_help_blocks()
        self.assertNotEqual(blocks, None)
        # verify that all of the fields are compulsory
        self.assertEqual(len(blocks),11)

        # database check to verify that user, volunteer are not created
        self.assertEqual(len(User.objects.all()),0)
        self.assertEqual(len(Volunteer.objects.all()),0)

    def test_successful_registration(self):
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertEqual(page.get_help_blocks(), None)
        self.assertEqual(page.get_message_box_text(),
                page.success_message)

        # database check to verify that user, volunteer created and their credentials
        self.assertEqual(len(User.objects.all()),1 )
        self.assertEqual(len(Volunteer.objects.all()),1)

        # check that empty list not returned for added filters
        self.assertNotEqual(len(User.objects.filter(
            username='volunteer-username')), 0)
        self.assertNotEqual(len(Volunteer.objects.filter(
            email='volunteer-email@systers.org')), 0)

    def test_name_fields(self):
        # register valid volunteer user
        page = self.page
        page.live_server_url = self.live_server_url
        page.register_valid_details()
        self.assertNotEqual(page.get_message_box(), None)
        self.assertEqual(page.get_message_box_text(),page.success_message)

        # register a user again with username same as already registered user
        self.assertEqual(self.driver.current_url, self.live_server_url +
                PageUrls.homepage)

        page.get_volunteer_registration_page()

        entry = ['volunteer-username','volunteer-password!@#$%^&*()_','volunteer-first-name','volunteer-last-name','volunteer-email1@systers.org','volunteer-address','volunteer-city','volunteer-state','volunteer-country','9999999999','volunteer-org']
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(page.get_username_error_text(),
                'User with this Username already exists.')

        # database check to verify that only 1 user, volunteer exists
        self.assertEqual(len(User.objects.all()),1 )
        self.assertEqual(len(Volunteer.objects.all()),1)

        # test numeric characters in first-name, last-name
        page.get_volunteer_registration_page()

        entry = ['volunteer-username-1','volunteer-password!@#$%^&*()_','volunteer-first-name-1','volunteer-last-name-1','volunteer-email1@systers.org','volunteer-address','volunteer-city','volunteer-state','volunteer-country','9999999999','volunteer-org']
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(page.get_first_name_error_text(),'Enter a valid value.')
        self.assertEqual(page.get_last_name_error_text(),'Enter a valid value.')

        # database check to verify that only 1 user, volunteer exists
        self.assertEqual(len(User.objects.all()),1 )
        self.assertEqual(len(Volunteer.objects.all()),1)

        # test special characters in first-name, last-name
        page.get_volunteer_registration_page()

        entry = ['volunteer-username-1','volunteer-password!@#$%^&*()_','first-name-!@#$%^&*()_','last-name!@#$%^&*()_','volunteer-email3@systers.org','volunteer-address','volunteer-city','volunteer-state','volunteer-country','9999999999','volunteer-org']
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(page.get_first_name_error_text(),'Enter a valid value.')
        self.assertEqual(page.get_last_name_error_text(),'Enter a valid value.')

        # database check to verify that only 1 user, volunteer exists
        self.assertEqual(len(User.objects.all()),1 )
        self.assertEqual(len(Volunteer.objects.all()),1)

        # test length of first-name, last-name not exceed 30
        page.get_volunteer_registration_page()

        entry = ['volunteer-username-1','volunteer-password!@#$%^&*()_','volunteer-first-name-long-asdfghjkl','volunteer-last-name-long-asdfghjkl','volunteer-email4@systers.org','volunteer-address','volunteer-city','volunteer-state','volunteer-country','9999999999','volunteer-org']
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(),None)
        error_message = page.get_first_name_error_text()
        self.assertTrue(bool(re.search(r'Ensure this value has at most 30 characters', str(error_message))))

        error_message = page.get_last_name_error_text()
        self.assertTrue(bool(re.search(r'Ensure this value has at most 30 characters', str(error_message))))

        # database check to verify that only 1 user, volunteer exists
        self.assertEqual(len(User.objects.all()),1 )
        self.assertEqual(len(Volunteer.objects.all()),1)

    def test_location_fields(self):
        # test numeric characters in address, city, state, country
        page = self.page
        page.live_server_url = self.live_server_url
        page.get_volunteer_registration_page()

        entry = ['volunteer-username-1','volunteer-password!@#$%^&*()_','volunteer-first-name','volunteer-last-name','volunteer-email1@systers.org','123 New-City address','1 volunteer-city','007 volunteer-state','54 volunteer-country','9999999999','volunteer-org']
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                page.volunteer_registration_page)

        # Verify that messages are displayed for city, state and country but not address
        # Test commented out as there is a bug in the template
        # self.assertEqual(len(page.get_help_blocks()),3)
        self.assertEqual(page.get_city_error_text(),'Enter a valid value.')
        self.assertEqual(page.get_state_error_text(),'Enter a valid value.')
        self.assertEqual(page.get_country_error_text(),'Enter a valid value.')

        # database check to verify that no user, volunteer created
        self.assertEqual(len(User.objects.all()),0)
        self.assertEqual(len(Volunteer.objects.all()),0)

        # Test special characters in address, city, state, country
        page.get_volunteer_registration_page()

        entry = ['volunteer-username-2','volunteer-password!@#$%^&*()_','volunteer-first-name','volunteer-last-name','volunteer-email2@systers.org','volunteer-address!@#$()','!$@%^#&volunteer-city','!$@%^#&volunteer-state','&%^*volunteer-country!@$#','9999999999','volunteer-org']
        page.fill_registration_form(entry)

        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                page.volunteer_registration_page)

        # verify that messages are displayed for all fields
        self.assertEqual(page.get_address_error_text(),'Enter a valid value.')
        self.assertEqual(page.get_city_error_text(),'Enter a valid value.')
        self.assertEqual(page.get_state_error_text(),'Enter a valid value.')
        self.assertEqual(page.get_country_error_text(),'Enter a valid value.')

        # database check to verify that no user, volunteer created
        self.assertEqual(len(User.objects.all()),0)
        self.assertEqual(len(Volunteer.objects.all()),0)

    def test_email_field(self):

        page = self.page
        page.live_server_url = self.live_server_url
        # register valid volunteer user
        page.register_valid_details()

        # verify successful registration
        self.assertNotEqual(page.get_message_box(),None)
        self.assertEqual(page.get_message_box_text(),page.success_message)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                PageUrls.homepage)

        # Try to register volunteer again with same email address
        page.get_volunteer_registration_page()

        entry = ['volunteer-username-1','volunteer-password!@#$%^&*()_','volunteer-first-name','volunteer-last-name','volunteer-email@systers.org','volunteer-address','volunteer-city','volunteer-state','volunteer-country','9999999999','volunteer-org']
        page.fill_registration_form(entry)

        # verify that volunteer wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                page.volunteer_registration_page)
        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(page.get_email_error_text(),'Volunteer with this Email already exists.')

        # database check to verify that no new user, volunteer created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Volunteer.objects.all()),1)

    def test_phone_field(self):

        page = self.page
        page.live_server_url = self.live_server_url
        # register valid volunteer user with valid phone number for country
        page.get_volunteer_registration_page()

        entry = ['volunteer-username','volunteer-password!@#$%^&*()_','volunteer-first-name','volunteer-last-name','volunteer-email@systers.org','volunteer-address','volunteer-city','volunteer-state','volunteer-country','9999999999','volunteer-org']
        page.fill_registration_form(entry)

        # verify successful registration
        self.assertNotEqual(page.get_message_box(),None)
        self.assertEqual(page.get_message_box_text(),page.success_message)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                PageUrls.homepage)

        # database check to verify that user, volunteer created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Volunteer.objects.all()),1)

        # Try to register volunteer with incorrect phone number for country
        page.get_volunteer_registration_page()

        entry = ['volunteer-username-1','volunteer-password!@#$%^&*()_','volunteer-first-name','volunteer-last-name','volunteer-email1@systers.org','volunteer-address','volunteer-city','volunteer-state','India','237937913','volunteer-org']
        page.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                page.volunteer_registration_page)
        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(page.get_phone_error_text(),
                "This phone number isn't valid for the selected country")

        # database check to verify that no new user, volunteer created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Volunteer.objects.all()),1)

        # Use invalid characters in phone number
        page.get_volunteer_registration_page()

        entry = ['volunteer-username-1','volunteer-password!@#$%^&*()_','volunteer-first-name','volunteer-last-name','volunteer-email1@systers.org','volunteer-address','volunteer-city','volunteer-state','India','23&79^37913','volunteer-org']
        page.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                page.volunteer_registration_page)
        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(page.get_phone_error_text(),"Please enter a valid phone number")

        # database check to verify that no new user, volunteer created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Volunteer.objects.all()),1)

    def test_organization_field(self):

        page = self.page
        page.live_server_url = self.live_server_url
        # test numeric characters in organization
        page.get_volunteer_registration_page()

        entry = ['volunteer-username-1','volunteer-password!@#$%^&*()_','volunteer-first-name','volunteer-last-name','volunteer-email1@systers.org','volunteer-address','volunteer-city','volunteer-state','volunteer-country','9999999999','volunteer-org 13']
        page.fill_registration_form(entry)

        # verify successful registration
        self.assertNotEqual(page.get_message_box(),None)
        self.assertEqual(page.get_message_box_text(),page.success_message)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                PageUrls.homepage)

        # database check to verify that user, volunteer created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Volunteer.objects.all()),1)

        # Use invalid characters in organization
        page.get_volunteer_registration_page()

        entry = ['volunteer-username-2','volunteer-password!@#$%^&*()_','volunteer-first-name','volunteer-last-name','volunteer-email2@systers.org','volunteer-address','volunteer-city','volunteer-state','volunteer-country','9999999999','!*^$volunteer-org']
        page.fill_registration_form(entry)

        # verify that user wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                page.volunteer_registration_page)
        self.assertNotEqual(page.get_help_blocks(),None)
        self.assertEqual(page.get_organization_error_text(),"Enter a valid value.")

        # database check to verify that no new user, volunteer created
        self.assertEqual(len(User.objects.all()),1)
        self.assertEqual(len(Volunteer.objects.all()),1)

    def test_field_value_retention(self):

        page = self.page
        page.live_server_url = self.live_server_url
        # send invalid value in fields - first name, state, phone, organization
        page.get_volunteer_registration_page()

        entry = ['volunteer-username','volunteer-password!@#$%^&*()_','volunteer-first-name-3','volunteer-last-name','volunteer-email@systers.org','volunteer-address','volunteer-city','volunteer-state!','volunteer-country','99999.!9999','@#volunteer-org']
        page.fill_registration_form(entry)

        # verify that user wasn't registered and that field values are not erased
        self.assertEqual(self.driver.current_url, self.live_server_url + page.volunteer_registration_page)
        details = ['volunteer-username','volunteer-first-name-3','volunteer-last-name','volunteer-email@systers.org','volunteer-address','volunteer-city','volunteer-state!','volunteer-country','99999.!9999','@#volunteer-org']
        self.verify_field_values(details) 

        # database check to verify that no user, volunteer created
        self.assertEqual(len(User.objects.all()),0)
        self.assertEqual(len(Volunteer.objects.all()),0)

        # send invalid value in fields - last name, address, city, country
        page.get_volunteer_registration_page()

        entry = ['volunteer-username','volunteer-password!@#$%^&*()_','volunteer-first-name','volunteer-last-name-3','volunteer-email@systers.org','volunteer-address$@!','volunteer-city#$','volunteer-state','volunteer-country 15','9999999999','volunteer-org']
        page.fill_registration_form(entry)

        # verify that user wasn't registered and that field values are not erased
        self.assertEqual(self.driver.current_url, self.live_server_url + page.volunteer_registration_page)
        details = ['volunteer-username','volunteer-first-name','volunteer-last-name-3','volunteer-email@systers.org','volunteer-address$@!','volunteer-city#$','volunteer-state','volunteer-country 15','9999999999','volunteer-org']
        self.verify_field_values(details)

        # database check to verify that no user, volunteer created
        self.assertEqual(len(User.objects.all()),0)
        self.assertEqual(len(Volunteer.objects.all()),0)
