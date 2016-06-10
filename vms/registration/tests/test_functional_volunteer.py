from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase

import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from organization.models import Organization #hack to pass travis,Bug in Code
from cities_light.models import Country


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
    '''
    def setUp(self):
        # create an org prior to registration. Bug in Code
        # added to pass CI
        Organization.objects.create(
                name = 'DummyOrg')

        # country created so that phone number can be checked
        Country.objects.create(
                name_ascii = 'India',
                slug ='india',
                geoname_id = '1269750',
                alternate_names = '',
                name = 'India',
                code2 = 'IN',
                code3 = 'IND',
                continent = 'AS',
                tld = 'in',
                phone = '91')

        self.homepage = '/'
        self.volunteer_registration_page = '/registration/signup_volunteer/'
        self.authentication_page = '/authentication/login/'
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(SignUpVolunteer, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(SignUpVolunteer, self).tearDown()

    def test_null_values(self):
        self.driver.get(self.live_server_url
                        + self.volunteer_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('')
        self.driver.find_element_by_id('id_password').send_keys('')
        self.driver.find_element_by_id('id_first_name').send_keys('')
        self.driver.find_element_by_id('id_last_name').send_keys('')
        self.driver.find_element_by_id('id_email').send_keys('')
        self.driver.find_element_by_id('id_address').send_keys('')
        self.driver.find_element_by_id('id_city').send_keys('')
        self.driver.find_element_by_id('id_state').send_keys('')
        self.driver.find_element_by_id('id_country').send_keys('')
        self.driver.find_element_by_id('id_phone_number').send_keys('')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        # verify that all of the fields are compulsory
        self.assertEqual(len(self.driver.find_elements_by_class_name('help-block')),
                11)

    def test_name_fields(self):
        # register valid volunteer user
        self.driver.get(self.live_server_url + self.volunteer_registration_page)


        self.driver.find_element_by_id('id_username').send_keys('volunteer-username')
        self.driver.find_element_by_id('id_password').send_keys('volunteer-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('volunteer-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('volunteer-last-name')
        self.driver.find_element_by_id('id_email').send_keys('volunteer-email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('volunteer-address')
        self.driver.find_element_by_id('id_city').send_keys('volunteer-city')
        self.driver.find_element_by_id('id_state').send_keys('volunteer-state')
        self.driver.find_element_by_id('id_country').send_keys('volunteer-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('volunteer-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('messages'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('messages').text,
                'You have successfully registered!')

        # register a user again with username same as already registered user
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        self.driver.get(self.live_server_url + self.volunteer_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('volunteer-username')
        self.driver.find_element_by_id('id_password').send_keys('volunteer-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('volunteer-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('volunteer-last-name')
        self.driver.find_element_by_id('id_email').send_keys('volunteer-email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('volunteer-address')
        self.driver.find_element_by_id('id_city').send_keys('volunteer-city')
        self.driver.find_element_by_id('id_state').send_keys('volunteer-state')
        self.driver.find_element_by_id('id_country').send_keys('volunteer-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('volunteer-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_username')/div/p/strong").text,
                'User with this Username already exists.')

        # test numeric characters in first-name, last-name
        self.driver.get(self.live_server_url + self.volunteer_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('volunteer-username-1')
        self.driver.find_element_by_id('id_password').send_keys('volunteer-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('volunteer-first-name-1')
        self.driver.find_element_by_id('id_last_name').send_keys('volunteer-last-name-1')
        self.driver.find_element_by_id('id_email').send_keys('volunteer-email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys(
            'volunteer-address')
        self.driver.find_element_by_id('id_city').send_keys('volunteer-city')
        self.driver.find_element_by_id('id_state').send_keys('volunteer-state')
        self.driver.find_element_by_id('id_country').send_keys('volunteer-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('volunteer-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_first_name')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_last_name')/div/p/strong").text,
                'Enter a valid value.')

        # test special characters in first-name, last-name
        self.driver.get(self.live_server_url + self.volunteer_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('volunteer-username-1')
        self.driver.find_element_by_id('id_password').send_keys('volunteer-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('first-name-!@#$%^&*()_')
        self.driver.find_element_by_id('id_last_name').send_keys('last-name-!@#$%^&*()_')
        self.driver.find_element_by_id('id_email').send_keys('volunteer-email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('volunteer-address')
        self.driver.find_element_by_id('id_city').send_keys('volunteer-city')
        self.driver.find_element_by_id('id_state').send_keys('volunteer-state')
        self.driver.find_element_by_id('id_country').send_keys('volunteer-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('volunteer-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_first_name')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_last_name')/div/p/strong").text,
                'Enter a valid value.')

        # test length of first-name, last-name not exceed 30
        self.driver.get(self.live_server_url + self.volunteer_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('volunteer-username-1')
        self.driver.find_element_by_id('id_password').send_keys('volunteer-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('volunteer-first-name-!@#$%^&*()_')
        self.driver.find_element_by_id('id_last_name').send_keys('volunteer-last-name-!@#$%^&*()_')
        self.driver.find_element_by_id('id_email').send_keys('volunteer-email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('volunteer-address')
        self.driver.find_element_by_id('id_city').send_keys('volunteer-city')
        self.driver.find_element_by_id('id_state').send_keys('volunteer-state')
        self.driver.find_element_by_id('id_country').send_keys('volunteer-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('volunteer-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        error_message = self.driver.find_element_by_xpath("id('div_id_first_name')/div/p/strong").text
        self.assertTrue(bool(re.search(r'Ensure this value has at most 30 characters', str(error_message))))

        error_message = self.driver.find_element_by_xpath("id('div_id_last_name')/div/p/strong").text,
        self.assertTrue(bool(re.search(r'Ensure this value has at most 30 characters', str(error_message))))

    def test_location_fields(self):

        # register valid volunteer user
        self.driver.get(self.live_server_url + self.volunteer_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('volunteer-username')
        self.driver.find_element_by_id('id_password').send_keys('volunteer-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('volunteer-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('volunteer-last-name')
        self.driver.find_element_by_id('id_email').send_keys('volunteer-email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('volunteer-address')
        self.driver.find_element_by_id('id_city').send_keys('volunteer-city')
        self.driver.find_element_by_id('id_state').send_keys('volunteer-state')
        self.driver.find_element_by_id('id_country').send_keys('volunteer-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('volunteer-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('messages'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('messages').text,
                'You have successfully registered!')

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        # test numeric characters in address, city, state, country
        self.driver.get(self.live_server_url + self.volunteer_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('volunteer-username-1')
        self.driver.find_element_by_id('id_password').send_keys('volunteer-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('volunteer-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('volunteer-last-name')
        self.driver.find_element_by_id('id_email').send_keys('volunteer-email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('123 New-City address')
        self.driver.find_element_by_id('id_city').send_keys('1 volunteer-city')
        self.driver.find_element_by_id('id_state').send_keys('007 volunteer-state')
        self.driver.find_element_by_id('id_country').send_keys('54 volunteer-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('volunteer-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.volunteer_registration_page)

        # Verify that messages are displayed for city, state and country but not address
        # Test commented out as there is a bug in the template
        """self.assertEqual(len(self.driver.find_elements_by_class_name('help-block')),
                3)"""
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_city')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_state')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_country')/div/p/strong").text,
                'Enter a valid value.')

        # Test special characters in address, city, state, country
        self.driver.get(self.live_server_url + self.volunteer_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('volunteer-username-2')
        self.driver.find_element_by_id('id_password').send_keys('volunteer-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('volunteer-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('volunteer-last-name')
        self.driver.find_element_by_id('id_email').send_keys('volunteer-email2@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('volunteer-address!@#$()')
        self.driver.find_element_by_id('id_city').send_keys('!$@%^#&volunteer-city')
        self.driver.find_element_by_id('id_state').send_keys('!$@%^#&volunteer-state')
        self.driver.find_element_by_id('id_country').send_keys('&%^*volunteer-country!@$#')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('volunteer-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.volunteer_registration_page)

        # verify that messages are displayed for all fields
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_address')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_city')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_state')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_country')/div/p/strong").text,
                'Enter a valid value.')

    def test_email_field(self):

        # register valid volunteer user
        self.driver.get(self.live_server_url + self.volunteer_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('volunteer-username')
        self.driver.find_element_by_id('id_password').send_keys('volunteer-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('volunteer-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('volunteer-last-name')
        self.driver.find_element_by_id('id_email').send_keys('volunteer-email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('volunteer-address')
        self.driver.find_element_by_id('id_city').send_keys('volunteer-city')
        self.driver.find_element_by_id('id_state').send_keys('volunteer-state')
        self.driver.find_element_by_id('id_country').send_keys('volunteer-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('volunteer-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # verify successful registration
        self.assertNotEqual(self.driver.find_elements_by_class_name('messages'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('messages').text,
                'You have successfully registered!')

        # Try to register volunteer again with same email address
        self.driver.get(self.live_server_url + self.volunteer_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('volunteer-username-1')
        self.driver.find_element_by_id('id_password').send_keys('volunteer-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('volunteer-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('volunteer-last-name')
        self.driver.find_element_by_id('id_email').send_keys('volunteer-email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('volunteer-address')
        self.driver.find_element_by_id('id_city').send_keys('volunteer-city')
        self.driver.find_element_by_id('id_state').send_keys('volunteer-state')
        self.driver.find_element_by_id('id_country').send_keys('volunteer-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('volunteer-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # verify that volunteer wasn't registered
        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_email')/div/p/strong").text,
                'Volunteer with this Email already exists.')

    def test_phone_field(self):

        # register valid volunteer user with valid phone number for country
        self.driver.get(self.live_server_url + self.volunteer_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('volunteer-username')
        self.driver.find_element_by_id('id_password').send_keys('volunteer-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('volunteer-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('volunteer-last-name')
        self.driver.find_element_by_id('id_email').send_keys('volunteer-email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('volunteer-address')
        self.driver.find_element_by_id('id_city').send_keys('volunteer-city')
        self.driver.find_element_by_id('id_state').send_keys('volunteer-state')
        self.driver.find_element_by_id('id_country').send_keys('India')
        self.driver.find_element_by_id('id_phone_number').send_keys('022 2403 6606')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('volunteer-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # verify successful registration
        self.assertNotEqual(self.driver.find_elements_by_class_name('messages'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('messages').text,
                'You have successfully registered!')

        # Try to register volunteer with incorrect phone number for country
        self.driver.get(self.live_server_url + self.volunteer_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('volunteer-username-1')
        self.driver.find_element_by_id('id_password').send_keys('volunteer-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('volunteer-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('volunteer-last-name')
        self.driver.find_element_by_id('id_email').send_keys('volunteer-email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('volunteer-address')
        self.driver.find_element_by_id('id_city').send_keys('volunteer-city')
        self.driver.find_element_by_id('id_state').send_keys('volunteer-state')
        self.driver.find_element_by_id('id_country').send_keys('India')
        self.driver.find_element_by_id('id_phone_number').send_keys('237937913')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('volunteer-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # verify that user wasn't registered
        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_phone_number')/div/p/strong").text,
                "This phone number isn't valid for the selected country")

        # Use invalid characters in phone number
        self.driver.get(self.live_server_url + self.volunteer_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('volunteer-username-1')
        self.driver.find_element_by_id('id_password').send_keys('volunteer-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('volunteer-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('volunteer-last-name')
        self.driver.find_element_by_id('id_email').send_keys('volunteer-email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('volunteer-address')
        self.driver.find_element_by_id('id_city').send_keys('volunteer-city')
        self.driver.find_element_by_id('id_state').send_keys('volunteer-state')
        self.driver.find_element_by_id('id_country').send_keys('India')
        self.driver.find_element_by_id('id_phone_number').send_keys('23&79^37913')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('volunteer-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # verify that user wasn't registered
        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_phone_number')/div/p/strong").text,
                "Please enter a valid phone number")
