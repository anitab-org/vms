# third party
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pageUrls import PageUrls
from pom.locators.authenticationPageLocators import AuthenticationPageLocators
from shift.utils import (create_admin, create_volunteer)
import ipdb

class TestAccessControl(LiveServerTestCase):
    """
    TestAccessControl class contains the functional tests to check Admin and
    Volunteer can access '/home' view of VMS. Following tests are included:
    Administrator:
        - Login admin with correct credentials
        - Login admin with incorrect credentials
    Volunteer:
        - Login volunteer with correct credentials
        - Login volunteer with incorrect credentials
    """

    @classmethod
    def setUpClass(cls):
        """Method to initiate class level objects.

        This method initiates Firefox WebDriver, WebDriverWait and
        the corresponding POM objects for this Test Class
        """
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        cls.authentication_page = AuthenticationPage(cls.driver)
        cls.wait = WebDriverWait(cls.driver, 5)
        super(TestAccessControl, cls).setUpClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        create_admin()
        create_volunteer()

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
        super(TestAccessControl, cls).tearDownClass()

    def login(self, username, password):
        """
        Utility function to login with credentials received as parameters.
        :param username: Username of the user
        :param password: Password of the user
        """
        self.authentication_page.login({
            'username': username,
            'password': password
        })

    def test_correct_admin_credentials(self):
        """
        Test user redirected to home page after logging in as
        admin with correct credentials.
        """
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.go_to_authentication_page()
        username = password = 'admin'
        self.login(username, password)

        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//h1[contains(text(), 'Volunteer Management System')]"))
        )

        self.assertEqual(authentication_page.remove_i18n(self.driver.current_url),
                         self.live_server_url + authentication_page.homepage)

        self.assertRaisesRegexp(NoSuchElementException,
                                'Message: Unable to locate element: .alert-danger',
                                authentication_page.get_incorrect_login_message)
        authentication_page.logout()

    def test_incorrect_admin_credentials(self):
        """
        Test correct error message displayed while logging as
        admin with incorrect credentials.
        """
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.go_to_authentication_page()
        username = 'admin'
        password = 'wrong_password'
        self.login(username, password)

        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.' + AuthenticationPageLocators.INCORRECT_LOGIN_ERROR))
        )

        self.assertNotEqual(authentication_page.remove_i18n(self.driver.current_url),
                            self.live_server_url + authentication_page.homepage)

        self.assertEqual(authentication_page.remove_i18n(self.driver.current_url),
                         self.live_server_url + authentication_page.url)

        self.assertNotEqual(authentication_page.get_incorrect_login_message(),
                            None)

    def test_correct_volunteer_credentials(self):
        """
        Test user redirected to home page after logging in as
        volunteer with correct credentials.
        """
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.go_to_authentication_page()
        username = password = 'volunteer'
        self.login(username, password)

        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//h1[contains(text(), 'Volunteer Management System')]"))
        )

        self.assertEqual(authentication_page.remove_i18n(self.driver.current_url),
                         self.live_server_url + authentication_page.homepage)

        self.assertRaisesRegexp(NoSuchElementException,
                                'Message: Unable to locate element: .alert-danger',
                                authentication_page.get_incorrect_login_message)
        authentication_page.logout()

    def test_incorrect_volunteer_credentials(self):
        """
        Test correct error message displayed while logging as
        volunteer with incorrect credentials.
        """
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.go_to_authentication_page()
        username = 'volunteer'
        password = 'wrong_password'
        self.login(username, password)

        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.' + AuthenticationPageLocators.INCORRECT_LOGIN_ERROR))
        )

        self.assertNotEqual(authentication_page.remove_i18n(self.driver.current_url),
                            self.live_server_url + authentication_page.homepage)

        self.assertEqual(authentication_page.remove_i18n(self.driver.current_url),
                         self.live_server_url + authentication_page.url)
        self.assertNotEqual(authentication_page.get_incorrect_login_message(), None)

    def test_login_page_after_authentication(self):
        """
        Test user redirected to home page if they try to access login page
        after logging in.
        """
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        username = password = 'admin'
        self.login(username, password)

        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//h1[contains(text(), 'Volunteer Management System')]"))
        )

        self.assertEqual(authentication_page.remove_i18n(self.driver.current_url),
                         self.live_server_url + authentication_page.homepage)

        self.assertRaisesRegexp(NoSuchElementException,
                                'Message: Unable to locate element: .alert-danger',
                                authentication_page.get_incorrect_login_message)

        authentication_page.get_page(authentication_page.server_url, '/authentication/')

        self.assertEqual(authentication_page.remove_i18n(self.driver.current_url),
                         self.live_server_url + authentication_page.homepage)

        authentication_page.logout()

    def test_forgot_password(self):
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.go_to_authentication_page()
        authentication_page.go_to_forgot_password_page()
        self.assertEqual(authentication_page.remove_i18n(self.driver.current_url), self.live_server_url + PageUrls.password_reset_page)
        authentication_page.fill_password_reset_form('volunteer@volunteer.com') 
        self.assertEqual(authentication_page.remove_i18n(self.driver.current_url), self.live_server_url + PageUrls.password_reset_done_page)

