from django.contrib.staticfiles.testing import LiveServerTestCase

from job.models import Job
from shift.models import VolunteerShift

from pom.pages.eventSignUpPage import EventSignUpPage
from pom.pages.authenticationPage import AuthenticationPage

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from shift.utils import (
    create_volunteer,
    register_event_utility,
    register_job_utility,
    register_shift_utility,
    create_volunteer_with_details,
    create_shift_with_details,
    register_volunteer_for_shift_utility
    )

class ShiftSignUp(LiveServerTestCase):
    '''
    '''
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.sign_up_page = EventSignUpPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(ShiftSignUp, cls).setUpClass()

    def setUp(self):
        self.volunteer = create_volunteer()
        self.login_volunteer()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(ShiftSignUp, cls).tearDownClass()

    def login_volunteer(self):
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({ 'username' : 'volunteer', 'password' : 'volunteer'})

    def test_events_page_with_no_events(self):
        sign_up_page = self.sign_up_page
        sign_up_page.navigate_to_sign_up()
        self.assertEqual(sign_up_page.get_info_box().text,sign_up_page.no_event_message)

    def test_signup_shifts_with_registered_shifts(self):

        created_event = register_event_utility()
        created_job = register_job_utility()
        created_shift = register_shift_utility()

        sign_up_page = self.sign_up_page

        # open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # on event page
        sign_up_page.click_to_view_jobs()

        # on jobs page
        sign_up_page.click_to_view_shifts()

        # on shifts page
        sign_up_page.click_to_sign_up()

        # confirm shift assignment
        sign_up_page.submit_form()
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_danger_box()

        # check shift signed up
        self.assertEqual(sign_up_page.get_signed_up_shift_text(),'Upcoming Shifts')
        self.assertEqual(sign_up_page.get_shift_job(),'job')
        self.assertEqual(sign_up_page.get_shift_date(),'June 15, 2017')
        self.assertEqual(sign_up_page.get_shift_start_time(),'9 a.m.')
        self.assertEqual(sign_up_page.get_shift_end_time(),'3 p.m.')

        # database check to ensure volunteer has signed up for the shift
        self.assertEqual(len(VolunteerShift.objects.all()), 1)
        self.assertNotEqual(len(VolunteerShift.objects.filter(
            volunteer_id=self.volunteer.id, shift_id = created_shift.id)), 0)

    """def test_signup_for_same_shift_again(self):

        register_event_utility()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page
        # open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # events shown in table
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_info_box()
        sign_up_page.click_to_view_jobs()

        # on jobs page
        sign_up_page.click_to_view_shifts()

        # on shifts page, Sign up this shift !
        sign_up_page.click_to_sign_up()

        # confirm on shift sign up
        sign_up_page.submit_form()
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_danger_box()

        # sign up same shift again
        # open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # events page
        self.assertEqual(sign_up_page.get_info_box().text,sign_up_page.no_event_message)

        with self.assertRaises(NoSuchElementException):
            sign_up_page.find_table_tag()

    def test_empty_events(self):
        
        register_event_utility()
        sign_up_page = self.sign_up_page
        # open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # on event page
        self.assertEqual(sign_up_page.get_info_box().text,sign_up_page.no_event_message)

        with self.assertRaises(NoSuchElementException):
            sign_up_page.find_table_tag()
            sign_up_page.click_to_view_jobs()

        register_job_utility()

        self.assertEqual(sign_up_page.get_info_box().text,sign_up_page.no_event_message)

        with self.assertRaises(NoSuchElementException):
            sign_up_page.find_table_tag()

    def test_shift_sign_up_with_outdated_shifts(self):

        register_event_utility()
        register_job_utility()
        sign_up_page = self.sign_up_page

        # create outdated shift
        shift_1 = ["2016-05-11","9:00","15:00",6,Job.objects.get(name = 'job')]
        s1 = create_shift_with_details(shift_1)

        # open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # on event page
        sign_up_page.click_to_view_jobs()

        # on jobs page
        sign_up_page.click_to_view_shifts()
        self.assertEqual(sign_up_page.get_info_box().text,'There are currently no shifts for the job job.')

    def test_shift_sign_up_with_no_slots(self):

        register_event_utility()
        register_job_utility()

        sign_up_page = self.sign_up_page

        # create shift with no slot
        shift_2 = ["2016-05-11","9:00","15:00",1,Job.objects.get(name = 'job')]
        s2 = create_shift_with_details(shift_2)

        # Create another volunteer
        volunteer_2 = ['volunteer-2',"Sam","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","volunteer2@volunteer.com"]
        v2 = create_volunteer_with_details(volunteer_2)

        # Assign shift to the volunteer
        vol_shift = register_volunteer_for_shift_utility(s2, v2)

        # open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # on event page
        self.assertEqual(sign_up_page.get_info_box().text,sign_up_page.no_event_message)

    def test_search_event(self):

        register_event_utility()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page

        # open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # enter date range in which an event starts
        date = ['05/08/2016', '08/31/2017']
        sign_up_page.fill_search_form(date)
        # verify that the event shows up
        self.assertEqual(sign_up_page.get_event_name(), 'event')

        # enter date range in which no event starts
        date = ['10/08/2016', '08/31/2017']
        sign_up_page.fill_search_form(date)
        # verify that no event shows up on event page
        self.assertEqual(sign_up_page.get_info_box().text,sign_up_page.no_event_message)

        # comm
        # enter only incorrect starting date
        date = ['10/08/2016', '']
        sign_up_page.fill_search_form(date)
        # verify that no event shows up on event page
        self.assertEqual(sign_up_page.get_info_box().text,sign_up_page.no_event_message)

        # enter only correct starting date
        date = ['05/10/2016', '']
        sign_up_page.fill_search_form(date)
        # verify that the event shows up
        self.assertEqual(sign_up_page.get_event_name() 'event')

        # enter only incorrect ending date
        date = ['', '10/08/2015']
        sign_up_page.fill_search_form(date)
        # verify that no event shows up on event page
        self.assertEqual(sign_up_page.get_info_box().text,sign_up_page.no_event_message)

        # enter correct ending date
        date = ['', '06/15/2017']
        sign_up_page.fill_search_form(date)
        # verify that the event shows up
        self.assertEqual(sign_up_page.get_event_name(), 'event')"""
