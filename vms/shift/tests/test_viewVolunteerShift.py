from django.contrib.staticfiles.testing import LiveServerTestCase

from pom.pages.upcomingShiftsPage import UpcomingShiftsPage
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.manageShiftPage import ManageShiftPage

from shift.models import VolunteerShift

from shift.utils import (
    create_volunteer,
    create_event_with_details,
    create_job_with_details,
    create_shift_with_details,
    create_volunteer_with_details,
    register_volunteer_for_shift_utility
    )

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import re

class ViewVolunteerShift(LiveServerTestCase):
    '''
    '''
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.manage_shift_page = ManageShiftPage(cls.driver)
        cls.upcoming_shift_page = UpcomingShiftsPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(ViewVolunteerShift, cls).setUpClass()

    def setUp(self):
        self.v1 = create_volunteer()
        self.login_volunteer()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(ViewVolunteerShift, cls).tearDownClass()

    def login_volunteer(self):
        credentials = {'username' : 'volunteer', 'password' : 'volunteer'}
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login(credentials)

    def test_access_another_existing_volunteer_view(self):
        '''
        details = ['test_volunteer', 'volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-city', 'volunteer-stateq', 'volunteer-countryq',
                '9999999999', 'volunteer-email2@systers.orgq','volunteer-organizationq']

        test_volunteer = create_volunteer_with_details(details)

        self.login_volunteer()
        upcoming_shift_page = self.upcoming_shift_page
        upcoming_shift_page.get_page(self.live_server_url, upcoming_shift_page.view_shift_page + str(test_volunteer_id))
        '''
        pass

    def test_access_another_nonexisting_volunteer_view(self):
        upcoming_shift_page = self.upcoming_shift_page
        upcoming_shift_page.get_page(self.live_server_url, upcoming_shift_page.view_shift_page + '65459')
        found = re.search('Not Found', self.driver.page_source)
        self.assertNotEqual(found, None)

    def test_view_without_any_assigned_shift(self):
        upcoming_shift_page = self.upcoming_shift_page
        upcoming_shift_page.view_upcoming_shifts()
        self.assertEqual(upcoming_shift_page.get_info_box(), upcoming_shift_page.no_shift_message)

    def register_dataset(self):

        created_event = create_event_with_details(['event-four', '2017-06-01', '2017-06-10'])
        created_job = create_job_with_details(
            ['jobOneInEventFour', '2017-06-01', '2017-06-10', 'job description', created_event]
            )
        created_shift = create_shift_with_details(['2017-06-01', '09:00', '15:00', '10', created_job])
        registered_shift = register_volunteer_for_shift_utility(created_shift, self.v1)

    def test_view_with_assigned_and_unlogged_shift(self):

        self.register_dataset()
        upcoming_shift_page = self.upcoming_shift_page
        upcoming_shift_page.view_upcoming_shifts()

        self.assertEqual(upcoming_shift_page.get_shift_job(), 'jobOneInEventFour')
        self.assertEqual(upcoming_shift_page.get_shift_date(), 'June 1, 2017')
        self.assertEqual(upcoming_shift_page.get_shift_start_time(), '9 a.m.')
        self.assertEqual(upcoming_shift_page.get_shift_end_time(), '3 p.m.')

    def test_log_hours_and_logged_shift_does_not_appear_in_upcoming_shifts(self):

        self.register_dataset()
        upcoming_shift_page = self.upcoming_shift_page
        upcoming_shift_page.view_upcoming_shifts()

        self.assertEqual(upcoming_shift_page.get_log_hours(), 'Log Hours')

        upcoming_shift_page.click_to_log_hours()
        upcoming_shift_page.log_shift_timings('09:00', '12:00')

        # check logged shift does not appear in Upcoming Shifts
        upcoming_shift_page.view_upcoming_shifts()
        self.assertEqual(upcoming_shift_page.get_info_box(), upcoming_shift_page.no_shift_message)
        with self.assertRaises(NoSuchElementException):
            upcoming_shift_page.get_result_container()

        # database check to ensure volunteer has logged the hours
        self.assertEqual(len(VolunteerShift.objects.all()), 1)
        self.assertNotEqual(len(VolunteerShift.objects.filter(
            start_time__isnull=False, end_time__isnull=False)), 0)
        self.assertNotEqual(len(VolunteerShift.objects.filter(
            start_time='09:00', end_time='12:00')), 0)

    def test_cancel_shift_registration(self):

        self.register_dataset()
        upcoming_shift_page = self.upcoming_shift_page
        manage_shift_page = self.manage_shift_page
        upcoming_shift_page.view_upcoming_shifts()

        self.assertEqual(upcoming_shift_page.get_cancel_shift().text, 'Cancel Shift Registration')
        upcoming_shift_page.cancel_shift()

        self.assertNotEqual(manage_shift_page.get_cancellation_box(),None)
        self.assertEqual(manage_shift_page.get_cancellation_header(),
            'Cancel Shift Confirmation')
        self.assertEqual(manage_shift_page.get_cancellation_message(),
                'Yes, Cancel this Shift')
        manage_shift_page.submit_form()

        # check shift removed from upcoming shifts
        upcoming_shift_page.view_upcoming_shifts()
        self.assertEqual(upcoming_shift_page.get_info_box(),
            upcoming_shift_page.no_shift_message)
        with self.assertRaises(NoSuchElementException):
            upcoming_shift_page.get_result_container()

        # database check to ensure shift registration is cancelled
        self.assertEqual(len(VolunteerShift.objects.all()), 0)
