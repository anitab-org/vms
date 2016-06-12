from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User

import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from organization.models import Organization #hack to pass travis,Bug in Code
from cities_light.models import Country

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
        self.admin_registration_page = '/registration/signup_administrator/'
        self.authentication_page = '/authentication/login/'
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(SignUpAdmin, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(SignUpAdmin, self).tearDown()

    def test_null_values(self):
        self.driver.get(self.live_server_url + self.admin_registration_page)

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
        # verify that 10 of the fields are compulsory
        self.assertEqual(len(self.driver.find_elements_by_class_name('help-block')),
                10)

    def test_name_fields(self):
        # register valid admin user
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('messages'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('messages').text,
                'You have successfully registered!')

        # register a user again with username same as already registered user
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_username')/div/p/strong").text,
                'User with this Username already exists.')

        # test numeric characters in first-name, last-name
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-1')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name-1')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name-1')
        self.driver.find_element_by_id('id_email').send_keys('email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_first_name')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_last_name')/div/p/strong").text,
                'Enter a valid value.')

        # test special characters in first-name, last-name
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-1')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('name-!@#$%^&*()_')
        self.driver.find_element_by_id('id_last_name').send_keys('name-!@#$%^&*()_')
        self.driver.find_element_by_id('id_email').send_keys('email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_first_name')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_last_name')/div/p/strong").text,
                'Enter a valid value.')

        # test length of first-name, last-name not exceed 30
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-1')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name-!@#$%^&*()_')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name-!@#$%^&*()_')
        self.driver.find_element_by_id('id_email').send_keys('email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        error_message = self.driver.find_element_by_xpath("id('div_id_first_name')/div/p/strong").text
        self.assertTrue(bool(re.search(r'Ensure this value has at most 20 characters', str(error_message))))

        error_message = self.driver.find_element_by_xpath("id('div_id_last_name')/div/p/strong").text,
        self.assertTrue(bool(re.search(r'Ensure this value has at most 20 characters', str(error_message))))

    def test_location_fields(self):
        # register valid admin user
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('messages'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('messages').text,
                'You have successfully registered!')

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        # test numeric characters in address, city, state, country
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-1')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('123 New-City address')
        self.driver.find_element_by_id('id_city').send_keys('1 admin-city')
        self.driver.find_element_by_id('id_state').send_keys('007 admin-state')
        self.driver.find_element_by_id('id_country').send_keys('54 admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.admin_registration_page)

        #verify that messages are displayed for city, state and country but not address
        self.assertEqual(len(self.driver.find_elements_by_class_name('help-block')),
                3)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_city')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_state')/div/p/strong").text,
                'Enter a valid value.')
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_country')/div/p/strong").text,
                'Enter a valid value.')

        # test special characters in address, city, state, country
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-2')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('last-name')
        self.driver.find_element_by_id('id_email').send_keys('email2@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address!@#$()')
        self.driver.find_element_by_id('id_city').send_keys('!$@%^#&admin-city')
        self.driver.find_element_by_id('id_state').send_keys('!$@%^#&admin-state')
        self.driver.find_element_by_id('id_country').send_keys('&%^*admin-country!@$#')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.admin_registration_page)

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

        # register valid admin user
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # verify successful registration
        self.assertNotEqual(self.driver.find_elements_by_class_name('messages'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('messages').text,
                'You have successfully registered!')
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        # Try to register admin again with same email address
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-1')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('9999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # verify that user wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.admin_registration_page)
        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_email')/div/p/strong").text,
                'Administrator with this Email already exists.')

    def test_phone_field(self):

        # register valid admin user with valid phone number for country
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('India')
        self.driver.find_element_by_id('id_phone_number').send_keys('022 2403 6606')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # verify successful registration
        self.assertNotEqual(self.driver.find_elements_by_class_name('messages'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('messages').text,
                'You have successfully registered!')
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        # Try to register admin with incorrect phone number for country
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-1')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('India')
        self.driver.find_element_by_id('id_phone_number').send_keys('237937913')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # verify that user wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.admin_registration_page)
        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_phone_number')/div/p/strong").text,
                "This phone number isn't valid for the selected country")

        # Use invalid characters in phone number
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-1')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('India')
        self.driver.find_element_by_id('id_phone_number').send_keys('23&79^37913')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # verify that user wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.admin_registration_page)
        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_phone_number')/div/p/strong").text,
                "Please enter a valid phone number")

    def test_organization_field(self):

        # register valid admin user
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # verify successful registration
        self.assertNotEqual(self.driver.find_elements_by_class_name('messages'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('messages').text,
                'You have successfully registered!')
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        # test numeric characters in organization
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-1')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('13 admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # verify successful registration
        self.assertNotEqual(self.driver.find_elements_by_class_name('messages'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('messages').text,
                'You have successfully registered!')
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        # Use invalid characters in organization
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username-2')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email2@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('!$&admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # verify that user wasn't registered
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.admin_registration_page)
        self.assertNotEqual(self.driver.find_elements_by_class_name('help-block'),
                None)
        self.assertEqual(self.driver.find_element_by_xpath("id('div_id_unlisted_organization')/div/p/strong").text,
                "Enter a valid value.")

    def test_field_value_retention(self):

        # send invalid value in fields - first name, state, phone, organization
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name-3')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name')
        self.driver.find_element_by_id('id_email').send_keys('email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address')
        self.driver.find_element_by_id('id_city').send_keys('admin-city')
        self.driver.find_element_by_id('id_state').send_keys('admin-state!')
        self.driver.find_element_by_id('id_country').send_keys('admin-country')
        self.driver.find_element_by_id('id_phone_number').send_keys('99999.!9999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('@#admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # verify that user wasn't registered and that field values are not erased
        self.assertEqual(self.driver.current_url, self.live_server_url + self.admin_registration_page)
        self.assertEqual(self.driver.find_element_by_id('id_username').get_attribute('value'),'admin-username')
        self.assertEqual(self.driver.find_element_by_id('id_first_name').get_attribute('value'),'admin-first-name-3')
        self.assertEqual(self.driver.find_element_by_id('id_last_name').get_attribute('value'),'admin-last-name')
        self.assertEqual(self.driver.find_element_by_id('id_email').get_attribute('value'),'email1@systers.org')
        self.assertEqual(self.driver.find_element_by_id('id_address').get_attribute('value'),'admin-address')
        self.assertEqual(self.driver.find_element_by_id('id_city').get_attribute('value'),'admin-city')
        self.assertEqual(self.driver.find_element_by_id('id_state').get_attribute('value'),'admin-state!')
        self.assertEqual(self.driver.find_element_by_id('id_country').get_attribute('value'),'admin-country')
        self.assertEqual(self.driver.find_element_by_id('id_phone_number').get_attribute('value'),'99999.!9999')
        self.assertEqual(self.driver.find_element_by_id('id_unlisted_organization').get_attribute('value'),'@#admin-org')

        # send invalid value in fields - last name, address, city, country
        self.driver.get(self.live_server_url + self.admin_registration_page)

        self.driver.find_element_by_id('id_username').send_keys('admin-username')
        self.driver.find_element_by_id('id_password').send_keys('admin-password!@#$%^&*()_')
        self.driver.find_element_by_id('id_first_name').send_keys('admin-first-name')
        self.driver.find_element_by_id('id_last_name').send_keys('admin-last-name-3')
        self.driver.find_element_by_id('id_email').send_keys('email1@systers.org')
        self.driver.find_element_by_id('id_address').send_keys('admin-address$@!')
        self.driver.find_element_by_id('id_city').send_keys('admin-city#$')
        self.driver.find_element_by_id('id_state').send_keys('admin-state')
        self.driver.find_element_by_id('id_country').send_keys('admin-country 15')
        self.driver.find_element_by_id('id_phone_number').send_keys('999999999')
        self.driver.find_element_by_id('id_unlisted_organization').send_keys('admin-org')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # verify that user wasn't registered and that field values are not erased
        self.assertEqual(self.driver.current_url, self.live_server_url + self.admin_registration_page)
        self.assertEqual(self.driver.find_element_by_id('id_username').get_attribute('value'),'admin-username')
        self.assertEqual(self.driver.find_element_by_id('id_first_name').get_attribute('value'),'admin-first-name')
        self.assertEqual(self.driver.find_element_by_id('id_last_name').get_attribute('value'),'admin-last-name-3')
        self.assertEqual(self.driver.find_element_by_id('id_email').get_attribute('value'),'email1@systers.org')
        self.assertEqual(self.driver.find_element_by_id('id_address').get_attribute('value'),'admin-address$@!')
        self.assertEqual(self.driver.find_element_by_id('id_city').get_attribute('value'),'admin-city#$')
        self.assertEqual(self.driver.find_element_by_id('id_state').get_attribute('value'),'admin-state')
        self.assertEqual(self.driver.find_element_by_id('id_country').get_attribute('value'),'admin-country 15')
        self.assertEqual(self.driver.find_element_by_id('id_phone_number').get_attribute('value'),'999999999')
        self.assertEqual(self.driver.find_element_by_id('id_unlisted_organization').get_attribute('value'),'admin-org')