# standard library
import re

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
from pom.pages.manageShiftPage import ManageShiftPage
from pom.pages.upcomingShiftsPage import UpcomingShiftsPage
from shift.utils import (create_second_city, register_past_job_utility,
                         create_second_country, create_volunteer,
                         create_event_with_details, create_job_with_details,
                         create_shift_with_details, register_past_shift_utility,
                         create_organization_with_details,
                         register_volunteer_for_shift_utility,
                         create_volunteer_with_details,
                         register_past_event_utility, create_second_state)


class ViewVolunteerShift(LiveServerTestCase):
    """
    Contains Tests for View Volunteer Shift Details Page

    Status of shift page is checked for following cases -
    - Access another registered volunteer
    - Access another unregistered volunteer
    - Access no assigned shifts view
    - Only future shifts displayed in Upcoming Shifts
    - View Assigned and Unlogged shifts
    - Cancel shift registration
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
        cls.manage_shift_page = ManageShiftPage(cls.driver)
        cls.upcoming_shift_page = UpcomingShiftsPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        cls.wait = WebDriverWait(cls.driver, 10)
        super(ViewVolunteerShift, cls).setUpClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        self.v1 = create_volunteer()
        self.login_volunteer()

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
        super(ViewVolunteerShift, cls).tearDownClass()

    def login_volunteer(self):
        """
        Utility function to login as volunteer.
        """
        credentials = {
            'username': 'volunteer',
            'password': 'volunteer'
        }
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login(credentials)

    def register_dataset(self):
        """
        Utility function to register data for testing.
        """
        created_event = create_event_with_details({
            'name': 'event-four',
            'start_date': '2050-06-01',
            'end_date': '2050-06-10',
            'address': 'event-address',
            'description': 'event-description',
            'venue': 'event-venue'
        })
        created_job = create_job_with_details({
            'name': 'jobOneInEventFour',
            'start_date': '2050-06-01',
            'end_date': '2050-06-10',
            'description': 'job description',
            'event': created_event
        })
        created_shift = create_shift_with_details({
            'date': '2050-06-01',
            'start_time': '09:00',
            'end_time': '15:00',
            'max_volunteers': '10',
            'job': created_job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        })
        registered_shift =\
            register_volunteer_for_shift_utility(created_shift, self.v1)

    def test_access_another_existing_volunteer_view(self):
        """
        Test error raised while volunteer is trying to access profile page of
        another existing volunteer.
        """
        upcoming_shift_page = self.upcoming_shift_page
        upcoming_shift_page.live_server_url = self.live_server_url
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//h1[contains(text(), 'Volunteer Management System')]"
                 )
            )
        )
        upcoming_shift_page.view_upcoming_shifts()
        self.assertEqual(upcoming_shift_page.get_info_box(),
                         upcoming_shift_page.no_shift_message)
        second_country = create_second_country()
        second_state = create_second_state()
        second_city = create_second_city()
        details = {
            'username': 'test_volunteer',
            'first_name': 'volunteer-first-name',
            'last_name': 'volunteer-last-name',
            'address': 'volunteer-address',
            'city': second_city,
            'state': second_state,
            'country': second_country,
            'phone_number': '9999999999',
            'email': 'volunteer-email2@systers.org'
        }

        org_name = 'volunteer-organization'
        org_obj = create_organization_with_details(org_name)
        test_volunteer = create_volunteer_with_details(details, org_obj)

        upcoming_shift_page.get_page(
            upcoming_shift_page.live_server_url,
            upcoming_shift_page.view_shift_page + str(test_volunteer.id)
        )
        found = re.search('You don\'t have the required rights',
                          self.driver.page_source)
        self.assertNotEqual(found, None)

    def test_access_another_nonexisting_volunteer_view(self):
        """
        Test error raised while volunteer is trying to access profile page of
        another non-existing volunteer.
        """
        upcoming_shift_page = self.upcoming_shift_page
        upcoming_shift_page.live_server_url = self.live_server_url
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//h1[contains(text(), 'Volunteer Management System')]"
                 )
            )
        )
        upcoming_shift_page.get_page(
            upcoming_shift_page.live_server_url,
            upcoming_shift_page.view_shift_page + '65459'
        )
        found = re.search('You don\'t have the required rights',
                          self.driver.page_source)
        self.assertNotEqual(found, None)

    def test_view_without_any_assigned_shift(self):
        """
        Test display of shifts with no assigned shifts.
        """
        upcoming_shift_page = self.upcoming_shift_page
        upcoming_shift_page.view_upcoming_shifts()
        self.assertEqual(upcoming_shift_page.get_info_box(),
                         upcoming_shift_page.no_shift_message)

    def test_view_with_assigned_and_unlogged_shift(self):
        """
        Test display of assigned but unlogged shift.
        """
        self.register_dataset()
        upcoming_shift_page = self.upcoming_shift_page
        upcoming_shift_page.live_server_url = self.live_server_url
        upcoming_shift_page.view_upcoming_shifts()

        self.assertEqual(
            upcoming_shift_page.get_shift_job(),
            'jobOneInEventFour'
        )
        self.assertEqual(upcoming_shift_page.get_shift_date(), 'June 1, 2050')
        self.assertEqual(upcoming_shift_page.get_shift_start_time(), '9 a.m.')
        self.assertEqual(upcoming_shift_page.get_shift_end_time(), '3 p.m.')

    def test_future_shifts_appear_in_upcoming_shifts(self):
        """
        Test display of only future shifts.
        """
        self.register_dataset()
        upcoming_shift_page = self.upcoming_shift_page
        upcoming_shift_page.live_server_url = self.live_server_url
        upcoming_shift_page.view_upcoming_shifts()

        self.assertEqual(
            upcoming_shift_page.get_shift_job(),
            'jobOneInEventFour'
        )
        self.assertEqual(upcoming_shift_page.get_shift_date(), 'June 1, 2050')
        self.assertEqual(upcoming_shift_page.get_shift_start_time(), '9 a.m.')
        self.assertEqual(upcoming_shift_page.get_shift_end_time(), '3 p.m.')

    def test_past_shifts_donot_appear_in_upcoming_shifts(self):
        register_past_event_utility()
        register_past_job_utility()
        shift = register_past_shift_utility()
        register_volunteer_for_shift_utility(shift, self.v1)

        upcoming_shift_page = self.upcoming_shift_page
        upcoming_shift_page.live_server_url = self.live_server_url
        upcoming_shift_page.view_upcoming_shifts()
        self.assertEqual(upcoming_shift_page.get_info_box(),
                         upcoming_shift_page.no_shift_message)
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table',
                                upcoming_shift_page.get_result_container)

    def test_cancel_shift_registration(self):
        """
        Test cancellation of registered shift.
        """
        self.register_dataset()
        upcoming_shift_page = self.upcoming_shift_page
        upcoming_shift_page.live_server_url = self.live_server_url
        manage_shift_page = self.manage_shift_page
        upcoming_shift_page.view_upcoming_shifts()

        self.assertEqual(upcoming_shift_page.get_cancel_shift().text,
                         'Cancel Shift Registration')
        upcoming_shift_page.cancel_shift()

        self.assertNotEqual(manage_shift_page.get_cancellation_box(), None)
        self.assertEqual(manage_shift_page.get_cancellation_header(),
                         'Cancel Shift Confirmation')
        self.assertEqual(manage_shift_page.get_cancellation_message(),
                         'Yes, Cancel this Shift')
        manage_shift_page.submit_form()

        # check shift removed from upcoming shifts
        upcoming_shift_page.view_upcoming_shifts()
        self.assertEqual(upcoming_shift_page.get_info_box(),
                         upcoming_shift_page.no_shift_message)
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table',
                                upcoming_shift_page.get_result_container)
