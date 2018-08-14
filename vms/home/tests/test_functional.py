# third party
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.homePage import HomePage
from pom.pageUrls import PageUrls

from shift.utils import (create_admin, create_volunteer)


class CheckURLAccess(LiveServerTestCase):
    """
    CheckURLAccess contains methods to browse(via URL) a volunteer page view
    after logging in from an admin account and vice-versa. Tests included:
    - Admin cannot access volunteer URL's
    - Volunteer cannot access admin URL's
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
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.home_page = HomePage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        cls.wait = WebDriverWait(cls.driver, 10)
        super(CheckURLAccess, cls).setUpClass()

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
        super(CheckURLAccess, cls).tearDownClass()

    def verify_admin_page_error(self, admin_url):
        """
        Utility function to verify errors raised on the
        pages when user tries to admin pages provided as
        admin_url in param.
        :param admin_url: URL of admin page to check errors on.
        """
        home_page = self.home_page
        home_page.get_page(self.live_server_url, admin_url)
        heading = home_page.get_no_admin_right()
        body = home_page.get_no_admin_right_content()
        self.assertNotEqual(heading, None)
        self.assertNotEqual(body, None)
        self.assertEqual(heading.text, 'No Access')
        self.assertEqual(body.text, 'You don\'t have administrator rights')

    def verify_volunteer_page_error(self, volunteer_url):
        """
        Utility function to verify errors raised on the
        pages when user tries to volunteer pages provided as
        volunteer_url in param.
        :param volunteer_url: URL of volunteer page to check errors on.
        """
        home_page = self.home_page
        home_page.get_page(self.live_server_url, volunteer_url)
        head = home_page.get_no_volunteer_right()
        body = home_page.get_no_volunteer_right_content()
        self.assertNotEqual(head, None)
        self.assertNotEqual(body, None)
        self.assertEqual(head.text, 'No Access')
        self.assertEqual(body.text, 'You don\'t have the required rights')

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

    def test_admin_cannot_access_volunteer_urls(self):
        """
        Test admin will be shown errors when they try to access
        volunteers URLs.
        """

        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        self.login(username='admin', password='admin')
        self.wait_for_home_page()

        self.verify_volunteer_page_error(PageUrls.upcoming_shifts_page + '1000')
        self.verify_volunteer_page_error(
            PageUrls.completed_shifts_page + '1000'
        )
        self.verify_volunteer_page_error(
            PageUrls.volunteer_report_page + '1000'
        )
        self.verify_volunteer_page_error(
            PageUrls.volunteer_profile_page + '1000'
        )

    def test_volunteer_cannot_access_admin_urls(self):
        """
        Test volunteer will be shown errors when they try to access
        admin URLs.
        """
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        self.login(username='volunteer', password='volunteer')
        self.wait_for_home_page()

        self.verify_admin_page_error(PageUrls.manage_volunteer_shift_page)
        self.verify_admin_page_error(PageUrls.admin_settings_page)
        self.verify_admin_page_error(PageUrls.volunteer_search_page)


class CheckContentAndRedirection(LiveServerTestCase):
    """
    This Class contains methods to check if

    - an administrator or a volunteer are provided their respective views
    links on their dashboard.
    - all links in the nav-bar for admin and volunteer page redirect to desired
    views.

    For content, following checks are implemented:
    - Check admin page content
    - check volunteer page content

    Admin views nav-bar consists of:
    - Volunteer Search
    - Manage Volunteer Shifts
    - Report
    - Settings
    - Create Admin Account
    - Change Password
    - Logout

    Volunteer views nav-bar consists of:
    - Upcoming Shifts
    - Shift Hours
    - Shift SignUp
    - Report
    - Profile
    - Change Password
    - Logout
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
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.home_page = HomePage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        cls.wait = WebDriverWait(cls.driver, 10)
        super(CheckContentAndRedirection, cls).setUpClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        self.admin = create_admin()
        self.volunteer = create_volunteer()
        self.volunteer_id = str(self.volunteer.id)

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
        super(CheckContentAndRedirection, cls).tearDownClass()

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

    def test_check_admin_page_content(self):
        """
        Check if an admin user has following functionalities on its home page.
        - Volunteer Search
        - Manage Volunteer Shift
        - Report
        - Settings
        - Create Admin Account
        """
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        home_page = self.home_page

        self.login(username='admin', password='admin')
        self.wait_for_home_page()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: Log In',
                                home_page.get_login_link)
        self.assertNotEqual(home_page.get_volunteer_search_link(), None)
        self.assertNotEqual(home_page.get_manage_shifts_link(), None)
        self.assertNotEqual(home_page.get_admin_report_link(), None)
        self.assertNotEqual(home_page.get_events_link(), None)
        self.assertNotEqual(home_page.get_create_admin_link(), None)
        self.assertNotEqual(home_page.get_change_password_link(), None)
        self.assertNotEqual(home_page.get_logout_link(), None)

    def test_check_volunteer_page_content(self):
        """
        Check if a volunteer user has following functionalities on its home
        page.
        - UpComing Shift
        - Shift Hours
        - Shift Sign Up
        - Report
        - Profile
        """
        home_page = self.home_page
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        self.login(username='volunteer', password='volunteer')
        self.wait_for_home_page()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: Log In',
                                home_page.get_login_link)
        self.assertNotEqual(home_page.get_upcoming_shifts_link(), None)
        self.assertNotEqual(home_page.get_completed_shifts_link(), None)
        self.assertNotEqual(home_page.get_shift_signup_link(), None)
        self.assertNotEqual(home_page.get_volunteer_report_link(), None)
        self.assertNotEqual(home_page.get_volunteer_profile_link(), None)
        self.assertNotEqual(home_page.get_change_password_link(), None)
        self.assertNotEqual(home_page.get_logout_link(), None)

    def test_admin_page_redirection(self):
        """
        Test admin is redirected corrected to home page after
        successful authorization by checking different elements
        on home page.
        """
        home_page = self.home_page
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        self.login(username='admin', password='admin')
        self.wait_for_home_page()

        self.assertEqual(
            authentication_page.remove_i18n(self.driver.current_url),
            self.live_server_url + PageUrls.homepage
        )
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: Log In',
                                home_page.get_login_link)

        volunteer_search_link = \
            home_page.get_volunteer_search_link().get_attribute('href')
        self.assertEqual(
            home_page.remove_i18n(volunteer_search_link),
            self.live_server_url + PageUrls.volunteer_search_page
        )

        manage_volunteer_shift_link = \
            home_page.get_manage_shifts_link().get_attribute('href')
        self.assertEqual(
            home_page.remove_i18n(manage_volunteer_shift_link),
            self.live_server_url + PageUrls.manage_volunteer_shift_page
        )

        report_link = \
            home_page.get_admin_report_link().get_attribute('href')
        self.assertEqual(
            home_page.remove_i18n(report_link),
            self.live_server_url + PageUrls.administrator_report_page
        )

        settings_link = \
            home_page.get_events_link().get_attribute('href')
        self.assertEqual(
            home_page.remove_i18n(settings_link),
            self.live_server_url + PageUrls.admin_settings_page
        )

        create_account_link = \
            home_page.get_create_admin_link().get_attribute('href')
        self.assertEqual(
            home_page.remove_i18n(create_account_link),
            self.live_server_url + PageUrls.admin_registration_page
        )

        change_password_link = \
            home_page.get_change_password_link().get_attribute('href')
        self.assertEqual(
            home_page.remove_i18n(change_password_link),
            self.live_server_url + PageUrls.password_change_page
        )

        logout_link = \
            home_page.get_logout_link().get_attribute('href')
        self.assertEqual(
            home_page.remove_i18n(logout_link),
            self.live_server_url + PageUrls.logout_page
        )

    def test_volunteer_page_redirection(self):
        """
        Test volunteer is redirected corrected to home page after
        successful authorization by checking different elements
        on home page.
        """
        home_page = self.home_page
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        self.login(username='volunteer', password='volunteer')
        self.wait_for_home_page()

        self.assertEqual(
            home_page.remove_i18n(self.driver.current_url),
            self.live_server_url + PageUrls.homepage
        )
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: Log In',
                                home_page.get_login_link)

        upcoming_shift_link = \
            home_page.get_upcoming_shifts_link().get_attribute('href')
        self.assertEqual(
            home_page.remove_i18n(upcoming_shift_link),
            self.live_server_url +
            PageUrls.upcoming_shifts_page +
            self.volunteer_id
        )

        shift_hours_link = \
            home_page.get_completed_shifts_link().get_attribute('href')
        self.assertEqual(
            home_page.remove_i18n(shift_hours_link),
            self.live_server_url +
            PageUrls.completed_shifts_page +
            self.volunteer_id
        )

        shift_signup_link = \
            home_page.get_shift_signup_link().get_attribute('href')
        self.assertEqual(
            home_page.remove_i18n(shift_signup_link),
            self.live_server_url +
            PageUrls.shift_sign_up_page +
            self.volunteer_id
        )

        report_link = \
            home_page.get_volunteer_report_link().get_attribute('href')
        self.assertEqual(
            home_page.remove_i18n(report_link),
            self.live_server_url +
            PageUrls.volunteer_report_page +
            self.volunteer_id
        )

        profile_link = \
            home_page.get_volunteer_profile_link().get_attribute('href')
        self.assertEqual(
            home_page.remove_i18n(profile_link),
            self.live_server_url +
            PageUrls.volunteer_profile_page +
            self.volunteer_id
        )

        change_password_link = \
            home_page.get_change_password_link().get_attribute('href')
        self.assertEqual(home_page.remove_i18n(change_password_link),
                         self.live_server_url + PageUrls.password_change_page)

        logout_link = home_page.get_logout_link().get_attribute('href')
        self.assertEqual(home_page.remove_i18n(logout_link),
                         self.live_server_url + PageUrls.logout_page)

