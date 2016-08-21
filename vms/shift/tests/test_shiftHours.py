from django.contrib.staticfiles.testing import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from pom.pages.completedShiftsPage import CompletedShiftsPage
from pom.pages.authenticationPage import AuthenticationPage

from shift.models import VolunteerShift

from shift.utils import (
    create_volunteer,
    create_event_with_details,
    create_job_with_details,
    create_shift_with_details,
    log_hours_with_details
    )

class ShiftHours(LiveServerTestCase):
    '''
    '''

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.completed_shifts_page = CompletedShiftsPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(ShiftHours, cls).setUpClass()

    def setUp(self):
        self.v1 = create_volunteer()
        self.login_volunteer()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(ShiftHours, cls).tearDownClass()

    def login_volunteer(self):
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({'username' : 'volunteer', 'password' : 'volunteer'})

    def register_dataset(self):
        
        # create shift and log hours
        e1 = create_event_with_details(['event', '2017-06-15', '2017-06-17'])
        j1 = create_job_with_details(['job', '2017-06-15', '2017-06-15', 'job description', e1])
        s1 = create_shift_with_details(['2017-06-15', '09:00', '15:00', '6', j1])
        log_hours_with_details(self.v1, s1, '12:00', '13:00')

    def test_view_with_unlogged_shift(self):
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.go_to_completed_shifts()
        self.assertEqual(self.driver.current_url, self.live_server_url + 
            completed_shifts_page.view_hours_page + str(self.v1.id))

        self.assertEqual(completed_shifts_page.get_info_box(),
            'You have not logged any hours.')

    def test_view_with_logged_shift(self):
        self.register_dataset()
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.go_to_completed_shifts()

        self.assertEqual(completed_shifts_page.get_shift_job(), 'job')
        self.assertEqual(completed_shifts_page.get_shift_date(), 'June 15, 2017')
        self.assertEqual(completed_shifts_page.get_shift_start_time(), 'noon')
        self.assertEqual(completed_shifts_page.get_shift_end_time(), '1 p.m.')
        self.assertEqual(completed_shifts_page.get_edit_shift_hours(), 'Edit Hours')
        self.assertEqual(completed_shifts_page.get_clear_shift_hours(), 'Clear Hours')

    def test_edit_hours(self):
        self.register_dataset()
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.go_to_completed_shifts()

        completed_shifts_page.edit_hours('10:00','13:00')
        self.assertEqual(completed_shifts_page.get_shift_start_time(), '10 a.m.')
        self.assertEqual(completed_shifts_page.get_shift_end_time(), '1 p.m.')

        # database check to ensure logged hours are edited
        self.assertEqual(len(VolunteerShift.objects.all()), 1)
        self.assertNotEqual(len(VolunteerShift.objects.filter(
            start_time='10:00', end_time='13:00')), 0)

    def test_end_hours_less_than_start_hours(self):
        self.register_dataset()
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.go_to_completed_shifts()

        completed_shifts_page.edit_hours('14:00', '12:00')

        try:
            completed_shifts_page.get_danger_box()
        except NoSuchElementException:
            raise Exception("End hours greater than start hours")

        # database check to ensure logged hours are not edited
        self.assertEqual(len(VolunteerShift.objects.all()), 1)
        self.assertNotEqual(len(VolunteerShift.objects.filter(
            start_time='12:00', end_time='13:00')), 0)

    def test_logged_hours_between_shift_hours(self):
        self.register_dataset()
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.go_to_completed_shifts()

        completed_shifts_page.edit_hours('10:00','16:00')
        self.assertEqual(completed_shifts_page.get_danger_box().text,
            'Logged hours should be between shift hours')

        # database check to ensure logged hours are not edited
        self.assertEqual(len(VolunteerShift.objects.all()), 1)
        self.assertNotEqual(len(VolunteerShift.objects.filter(
            start_time='12:00', end_time='13:00')), 0)

    def test_cancel_hours(self):
        self.register_dataset()
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.go_to_completed_shifts()

        self.assertEqual(completed_shifts_page.get_shift_job(), 'job')
        self.assertEqual(completed_shifts_page.get_clear_shift_hours(), 'Clear Hours')
        completed_shifts_page.click_to_clear_hours()

        self.assertEqual(completed_shifts_page.get_clear_shift_hours_text(),
            'Clear Shift Hours')
        completed_shifts_page.submit_form()

        with self.assertRaises(NoSuchElementException):
            self.assertEqual(completed_shifts_page.get_shift_job(), 'job')

        # database check to ensure logged hours are cleared
        self.assertEqual(len(VolunteerShift.objects.all()), 1)
        self.assertEqual(len(VolunteerShift.objects.filter(
            start_time__isnull=False, end_time__isnull=False)), 0)
