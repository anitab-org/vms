# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# third party
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# local Django
from job.models import Job
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.eventSignUpPage import EventSignUpPage
from shift.utils import (
    create_volunteer, register_event_utility, register_job_utility,
    register_shift_utility, create_shift_with_details, create_volunteer_with_details,
    register_volunteer_for_shift_utility)


class ShiftSignUp(LiveServerTestCase):
    """
    Tests dealing with Event app in aspect
    of Volunteer's view of website.
    """

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.sign_up_page = EventSignUpPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(ShiftSignUp, cls).setUpClass()

    def setUp(self):
        create_volunteer()
        self.login_volunteer()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.authentication_page.logout()
        cls.driver.quit()
        super(ShiftSignUp, cls).tearDownClass()

    def login_volunteer(self):
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({
            'username': 'volunteer',
            'password': 'volunteer'
        })

    def test_events_page_with_no_events(self):
        sign_up_page = self.sign_up_page
        sign_up_page.navigate_to_sign_up()
        self.assertEqual(sign_up_page.get_info_box().text, sign_up_page.no_event_message)

    def test_signup_shifts_with_registered_shifts(self):
        registered_event = register_event_utility()
        registered_job = register_job_utility()
        registered_shift = register_shift_utility()

        sign_up_page = self.sign_up_page

        # Open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # On event page
        sign_up_page.click_to_view_jobs()

        # On jobs page
        sign_up_page.click_to_view_shifts()

        # On shifts page
        sign_up_page.click_to_sign_up()

        # Confirm shift assignment
        sign_up_page.submit_form()
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_danger_box()

        # check shift signed up
        self.assertEqual(sign_up_page.get_signed_up_shift_text(), 'Upcoming Shifts')
        self.assertEqual(sign_up_page.get_shift_job(), 'job')
        self.assertEqual(sign_up_page.get_shift_date(), 'June 15, 2050')
        self.assertEqual(sign_up_page.get_shift_start_time(), '9 a.m.')
        self.assertEqual(sign_up_page.get_shift_end_time(), '3 p.m.')

    def test_signup_for_same_shift_again(self):
        registered_event = register_event_utility()
        registered_job = register_job_utility()
        registered_shift = register_shift_utility()

        sign_up_page = self.sign_up_page
        # Open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # Events shown in table
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_info_box()
        sign_up_page.click_to_view_jobs()

        # On jobs page
        sign_up_page.click_to_view_shifts()

        # On shifts page, Sign up this shift !
        sign_up_page.click_to_sign_up()

        # Confirm on shift sign up
        sign_up_page.submit_form()
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_danger_box()

        # Sign up same shift again
        # Open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # Events page
        self.assertEqual(sign_up_page.get_info_box().text, sign_up_page.no_event_message)

        with self.assertRaises(NoSuchElementException):
            sign_up_page.find_table_tag()

    def test_empty_events(self):
        registered_event = register_event_utility()
        sign_up_page = self.sign_up_page
        # Open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # On event page
        self.assertEqual(sign_up_page.get_info_box().text, sign_up_page.no_event_message)

        with self.assertRaises(NoSuchElementException):
            sign_up_page.find_table_tag()
            sign_up_page.click_to_view_jobs()

        registered_job = register_job_utility()

        self.assertEqual(sign_up_page.get_info_box().text, sign_up_page.no_event_message)

        with self.assertRaises(NoSuchElementException):
            sign_up_page.find_table_tag()

    def test_shift_sign_up_with_outdated_shifts(self):
        registered_event = register_event_utility()
        registered_job = register_job_utility()
        sign_up_page = self.sign_up_page

        # create outdated shift
        shift_1 = ["2016-05-11", "9:00", "15:00", 6, Job.objects.get(name='job')]
        created_shift = create_shift_with_details(shift_1)

        # open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # on event page
        sign_up_page.click_to_view_jobs()

        # on jobs page
        sign_up_page.click_to_view_shifts()
        self.assertEqual(sign_up_page.get_info_box().text,
                         sign_up_page.get_message_shift_not_available_for_job('job'))

    def test_shift_sign_up_with_no_slots(self):
        registered_event = register_event_utility()
        registered_job = register_job_utility()

        sign_up_page = self.sign_up_page

        # create shift with no slot
        shift_2 = ["2050-05-11", "9:00", "15:00", 1, Job.objects.get(name='job')]
        s2 = create_shift_with_details(shift_2)

        # Create another volunteer
        volunteer_2 = ['volunteer-2', "Sam", "Turtle", "Mario Land", "Nintendo Land", "Nintendo State",
                       "Nintendo Nation", "2374983247", "volunteer2@volunteer.com"]
        v2 = create_volunteer_with_details(volunteer_2)

        # Assign shift to the volunteer
        registered_vol_shift = register_volunteer_for_shift_utility(s2, v2)

        # open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # on event page
        self.assertEqual(sign_up_page.get_info_box().text, sign_up_page.no_event_message)

    def test_search_event(self):
        register_event_utility()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page

        # Enter date range in which an event starts
        sign_up_page.navigate_to_sign_up()
        date = ['05/08/2050', '05/31/2050']
        sign_up_page.fill_search_form(date)
        # Verify that the event shows up
        self.assertEqual(sign_up_page.get_event_name(), 'event')

        # Enter only correct starting date
        sign_up_page.navigate_to_sign_up()
        date = ['05/10/2050', '']
        sign_up_page.fill_search_form(date)
        # Verify that the event shows up
        self.assertEqual(sign_up_page.get_event_name(), 'event')

        # Enter correct ending date
        sign_up_page.navigate_to_sign_up()
        date = ['', '06/15/2050']
        sign_up_page.fill_search_form(date)
        # Verify that the event shows up
        self.assertEqual(sign_up_page.get_event_name(), 'event')
