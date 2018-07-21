# standard library
import re

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
from pom.pages.manageShiftPage import ManageShiftPage
from pom.pages.upcomingShiftsPage import UpcomingShiftsPage
from shift.utils import (create_volunteer, create_event_with_details,
                         create_job_with_details, create_shift_with_details,
                         register_volunteer_for_shift_utility, create_volunteer_with_details)


class ViewVolunteerShift(LiveServerTestCase):
    """
    Contains Tests for View Volunteer Shift Details Page

    Status of shift page is checked for following cases -
    - Access another registered volunteer
    - Access another unregistered volunteer
    - Access no assigned shifts view
    - Log hours and Shift not displayed in Upcoming Shifts
    - View Assigned and Unlogged shifts
    - Cancel shift registration
    """

    @classmethod
    def setUpClass(cls):
        """Method to initiate class level objects.

        This method initiates Firefox WebDriver, WebDriverWait and
        the corresponding POM objects for this Test Class
        """
        cls.driver = webdriver.Firefox()
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
        created_event = create_event_with_details(
            ['event-four', '2050-06-01', '2050-06-10'])
        created_job = create_job_with_details([
            'jobOneInEventFour', '2050-06-01', '2050-06-10', 'job description',
            created_event
        ])
        created_shift = create_shift_with_details(
            ['2050-06-01', '09:00', '15:00', '10', created_job])
        registered_shift = register_volunteer_for_shift_utility(created_shift, self.v1)

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
        details = ['test_volunteer', 'volunteer-first-name', 'volunteer-last-name',
                   'volunteer-address', 'volunteer-city', 'volunteer-state', 'volunteer-country',
                   '9999999999', 'volunteer-email2@systers.org', 'volunteer-organization']
        test_volunteer = create_volunteer_with_details(details)
        upcoming_shift_page.get_page(upcoming_shift_page.live_server_url,
                                     upcoming_shift_page.view_shift_page + str(test_volunteer.id))
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

        self.assertEqual(upcoming_shift_page.get_shift_job(), 'jobOneInEventFour')
        self.assertEqual(upcoming_shift_page.get_shift_date(), 'June 1, 2050')
        self.assertEqual(upcoming_shift_page.get_shift_start_time(), '9 a.m.')
        self.assertEqual(upcoming_shift_page.get_shift_end_time(), '3 p.m.')

    def test_log_hours_and_logged_shift_does_not_appear_in_upcoming_shifts(self):
        """
        Test that already logged shift and hours do not appear in upcoming shifts.
        """
        self.register_dataset()
        upcoming_shift_page = self.upcoming_shift_page
        upcoming_shift_page.live_server_url = self.live_server_url
        upcoming_shift_page.view_upcoming_shifts()

        self.assertEqual(upcoming_shift_page.get_log_hours(), 'Log Hours')

        upcoming_shift_page.click_to_log_hours()
        upcoming_shift_page.log_shift_timings('09:00', '12:00')

        # Check logged shift does not appear in Upcoming Shifts
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
