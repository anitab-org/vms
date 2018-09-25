# third party
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.shiftDetailsPage import ShiftDetailsPage
from shift.utils import (create_volunteer, create_admin,
                         create_event_with_details, create_job_with_details,
                         create_shift_with_details, log_hours_with_details,
                         register_volunteer_for_shift_utility)


class ShiftDetails(LiveServerTestCase):
    """
    Contains Tests for View Shift Details Page

    Status of shift page is checked for following cases -
    - No Volunteer is registered
    - Volunteer registered but no hours logged
    - Volunteer with logged shift hours
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
        cls.shift_details_page = ShiftDetailsPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        cls.wait = WebDriverWait(cls.driver, 10)
        super(ShiftDetails, cls).setUpClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        self.admin = create_admin()
        self.login_admin()
        self.shift = ShiftDetails.register_dataset()

    def tearDown(self):
        """
        Method consists of statements to be executed at
        end of each test.
        """
        self.authentication_page.logout()

    @classmethod
    def tearDownClass(cls):
        """
        Class method to quit the Firefox WebDriver session after
        execution of all tests in class.
        """
        cls.driver.quit()
        super(ShiftDetails, cls).tearDownClass()

    def login_admin(self):
        """
        Utility function to login as administrator.
        """
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.login({
            'username': 'admin',
            'password': 'admin'
        })

    @staticmethod
    def register_dataset():
        """
        Utility function to create data for testing
        :return: Shift type of object.
        """
        e1 = create_event_with_details({
            'name': 'event',
            'start_date': '2050-06-15',
            'end_date': '2050-06-17',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        })
        j1 = create_job_with_details({
            'name': 'job',
            'start_date': '2050-06-15',
            'end_date': '2050-06-15',
            'description': 'job description',
            'event': e1
        })
        s1 = create_shift_with_details({
            'date': '2050-06-15',
            'start_time': '09:00',
            'end_time': '15:00',
            'max_volunteers': '6',
            'job': j1,
            'address': 'shift-address',
            'venue': 'shift-venue'
        })
        return s1

    def wait_for_home_page(self):
        """
        Utility function to perform explicit wait for home page.
        """
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//h1[contains(text(), 'Volunteer Management System')]"
                 )
            )
        )

    def test_view_with_unregistered_volunteers(self):
        """
        Test display of shift details with no registered volunteer.
        """
        shift_details_page = self.shift_details_page
        shift_details_page.live_server_url = self.live_server_url

        self.wait_for_home_page()

        shift_details_page.navigate_to_shift_details_view()

        # Verify details and slots remaining
        self.assertEqual(shift_details_page.get_shift_job(), 'job')
        self.assertEqual(shift_details_page.get_shift_date(), 'June 15, 2050')
        self.assertEqual(shift_details_page.get_max_shift_volunteer(), '6')
        self.assertEqual(shift_details_page.get_shift_start_time(), '9 a.m.')
        self.assertEqual(shift_details_page.get_shift_end_time(), '3 p.m.')

        # Verify that there are no registered shifts or logged hours
        self.assertEqual(shift_details_page.get_message_box(),
                         'There are currently no volunteers assigned '
                         'to this shift. Please assign volunteers to '
                         'view more details'
                         )

    def test_view_with_only_registered_volunteers(self):
        """
        Test display of shift details with registered volunteer.
        """
        shift_details_page = self.shift_details_page
        shift_details_page.live_server_url = self.live_server_url
        volunteer = create_volunteer()
        volunteer_shift = register_volunteer_for_shift_utility(
            self.shift, volunteer)

        self.wait_for_home_page()

        shift_details_page.navigate_to_shift_details_view()

        # verify that the shift slot is decreased by 1
        self.assertEqual(shift_details_page.get_shift_job(), 'job')
        self.assertEqual(shift_details_page.get_max_shift_volunteer(), '5')

        # verify that assigned volunteers shows up but no logged hours yet
        self.assertEqual(len(shift_details_page.get_registered_volunteers()), 1)
        self.assertEqual(
            shift_details_page.get_registered_volunteer_name(),
            'Prince'
        )
        self.assertEqual(
            shift_details_page.get_registered_volunteer_email(),
            'volunteer@volunteer.com'
        )
        self.assertEqual(
            shift_details_page.get_message_box(),
            'There are no logged hours at the moment'
        )

    def test_view_with_logged_hours(self):
        """
        Test display of shift details with hours logged in the shift.
        """
        shift_details_page = self.shift_details_page
        shift_details_page.live_server_url = self.live_server_url
        volunteer = create_volunteer()

        log_hours_with_details(volunteer, self.shift, '13:00', '14:00')

        self.wait_for_home_page()

        shift_details_page.navigate_to_shift_details_view()

        # verify that the shift slot is decreased by 1
        self.assertEqual(shift_details_page.get_shift_job(), 'job')
        self.assertEqual(shift_details_page.get_max_shift_volunteer(), '5')

        # verify that assigned volunteers shows up
        self.assertEqual(len(shift_details_page.get_registered_volunteers()), 1)
        self.assertEqual(
            shift_details_page.get_registered_volunteer_email(),
            'volunteer@volunteer.com'
        )

        # verify that hours are logged by volunteer
        self.assertEqual(len(shift_details_page.get_logged_volunteers()), 1)
        self.assertEqual(
            shift_details_page.get_logged_volunteer_name(),
            'Prince'
        )
        self.assertEqual(shift_details_page.get_logged_start_time(), '1 p.m.')
        self.assertEqual(shift_details_page.get_logged_end_time(), '2 p.m.')

