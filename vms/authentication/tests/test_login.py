# third party
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.utils.http import urlsafe_base64_encode
from django.core import mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.homePage import HomePage
from pom.pageUrls import PageUrls
from pom.locators.authenticationPageLocators import AuthenticationPageLocators
from shift.utils import (create_admin, create_volunteer)
from volunteer.models import Volunteer


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
        firefox_options = Options()
        firefox_options.add_argument('-headless')
        cls.driver = webdriver.Firefox(firefox_options=firefox_options)
        cls.driver.maximize_window()
        cls.home_page = HomePage(cls.driver)
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

    def wait_for_home_page(self):
        """
        Utility function to perform a explicit wait for home page.
        """
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//h1[contains(text(), 'Volunteer Management System')]")
            )
        )

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

        self.assertEqual(
            authentication_page.remove_i18n(self.driver.current_url),
            self.live_server_url + authentication_page.homepage
        )

        self.assertRaisesRegexp(
            NoSuchElementException,
            'Message: Unable to locate element: .alert-danger',
            authentication_page.get_incorrect_login_message
        )
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
                (
                    By.CSS_SELECTOR,
                    '.' + AuthenticationPageLocators.INCORRECT_LOGIN_ERROR
                )
            )
        )

        self.assertNotEqual(
            authentication_page.remove_i18n(self.driver.current_url),
            self.live_server_url + authentication_page.homepage
        )

        self.assertEqual(
            authentication_page.remove_i18n(self.driver.current_url),
            self.live_server_url + authentication_page.url
        )

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

        self.assertEqual(
            authentication_page.remove_i18n(self.driver.current_url),
            self.live_server_url + authentication_page.homepage
        )

        self.assertRaisesRegexp(
            NoSuchElementException,
            'Message: Unable to locate element: .alert-danger',
            authentication_page.get_incorrect_login_message
        )
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
                (
                    By.CSS_SELECTOR,
                    '.' + AuthenticationPageLocators.INCORRECT_LOGIN_ERROR
                )
            )
        )

        self.assertNotEqual(
            authentication_page.remove_i18n(self.driver.current_url),
            self.live_server_url + authentication_page.homepage
        )

        self.assertEqual(
            authentication_page.remove_i18n(self.driver.current_url),
            self.live_server_url + authentication_page.url
        )
        self.assertNotEqual(
            authentication_page.get_incorrect_login_message(),
            None
        )

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

        self.assertEqual(
            authentication_page.remove_i18n(self.driver.current_url),
            self.live_server_url + authentication_page.homepage
        )

        self.assertRaisesRegexp(
            NoSuchElementException,
            'Message: Unable to locate element: .alert-danger',
            authentication_page.get_incorrect_login_message
        )

        authentication_page.get_page(
            authentication_page.server_url,
            '/authentication/'
        )

        self.assertEqual(
            authentication_page.remove_i18n(self.driver.current_url),
            self.live_server_url + authentication_page.homepage
        )

        authentication_page.logout()

    def test_forgot_password(self):
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.go_to_authentication_page()
        authentication_page.go_to_forgot_password_page()
        self.assertEqual(
            authentication_page.remove_i18n(self.driver.current_url),
            self.live_server_url + PageUrls.password_reset_page
        )
        authentication_page.fill_email_form('volunteer@volunteer.com')
        self.assertEqual(
            authentication_page.remove_i18n(self.driver.current_url),
            self.live_server_url + PageUrls.password_reset_done_page
        )
        v1 = Volunteer.objects.get(first_name='Prince')
        vol_email = v1.email
        mail.outbox = []
        mail.send_mail(
            'VMS Password Reset', "message",
            'messanger@localhost.com', [vol_email]
        )
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.subject, 'VMS Password Reset')
        self.assertEqual(msg.to, ['volunteer@volunteer.com'])
        u1 = v1.user
        uid = urlsafe_base64_encode(force_bytes(u1.pk)).decode()
        token = default_token_generator.make_token(u1)
        response = self.client.get(
            reverse(
                'authentication:password_reset_confirm',
                args=[uid, token]
            )
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(
            reverse('authentication:password_reset_complete')
        )
        self.assertEqual(response.status_code, 200)

    def test_change_password(self):
        home_page = self.home_page
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        self.login(username='volunteer', password='volunteer')
        self.wait_for_home_page()
        home_page.go_to_change_password_page()
        self.assertEqual(
            home_page.remove_i18n(self.driver.current_url),
            self.live_server_url + PageUrls.password_change_page
        )
        password = {
            'old_password': 'volunteer',
            'new_password': 'new-password',
            'confirm_new_password': 'new-password'
        }
        home_page.fill_password_change_form(password)
        self.assertEqual(
            home_page.remove_i18n(self.driver.current_url),
            self.live_server_url + PageUrls.password_change_done_page
        )
        usr = User.objects.get(username='volunteer')
        self.assertEqual(usr.check_password('new-password'), True)

