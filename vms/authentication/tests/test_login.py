from django.contrib.staticfiles.testing import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from shift.utils import (
    create_admin,
    create_volunteer
    )

import re

class TestAccessControl(LiveServerTestCase):
    '''
    TestAccessControl class contains the functional tests to check Admin and
    Volunteer can access '/home' view of VMS. Following tests are included:
    Administrator:
        - Login admin with correct credentials
        - Login admin with incorrect credentials 
    Volunteer:
        - Login volunteer with correct credentials
        - Login volunteer with incorrect credentials 
    '''
    @classmethod
    def setUpClass(cls):
        cls.homepage = '/'
        cls.authentication_page = '/authentication/login/'
        cls.login_id = 'id_login'
        cls.login_password = 'id_password'
        cls.incorrect_login_error = 'alert-danger'

        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        super(TestAccessControl, cls).setUpClass()

    def setUp(self):
        admin = create_admin()
        volunteer = create_volunteer()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(TestAccessControl, cls).tearDownClass()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id(self.login_id).send_keys(credentials['username'])
        self.driver.find_element_by_id(self.login_password).send_keys(credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def logout(self):
        self.driver.find_element_by_link_text('Log Out').click()

    def test_authentication_page(self):
        self.driver.get(self.live_server_url + self.homepage)
        self.driver.find_element_by_link_text('Log In').click()
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.authentication_page)

    def test_correct_admin_credentials(self):
        '''
        Method to simulate logging in of a valid admin user and check if they
        redirected to '/home' and no errors are generated.
        '''
        self.login({ 'username' : 'admin', 'password' : 'admin'})
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name(self.incorrect_login_error)
        self.logout()

    def test_incorrect_admin_credentials(self):
        '''
        Method to simulate logging in of an Invalid admin user and check if
        they are displayed an error and redirected to login page again.
        '''
        self.login({ 'username' : 'admin', 'password' : 'wrong_password'})
        self.assertNotEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.authentication_page)

        self.assertNotEqual(self.driver.find_element_by_class_name(
            self.incorrect_login_error), None)

    def test_correct_volunteer_credentials(self):
        '''
        Method to simulate logging in of a valid volunteer user and check if
        they are redirected to '/home'
        '''
        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name(self.incorrect_login_error)
        self.logout()

    def test_incorrect_volunteer_credentials(self):
        '''
        Method to simulate logging in of a Invalid volunteer user and check if
        they are displayed an error and redirected to login page again.
        '''
        self.login({ 'username' : 'volunteer', 'password' : 'wrong_password'})
        
        self.assertNotEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.authentication_page)

        self.assertNotEqual(self.driver.find_element_by_class_name(
            self.incorrect_login_error), None)
