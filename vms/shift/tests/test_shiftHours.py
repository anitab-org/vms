# third party
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.core import mail

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.completedShiftsPage import CompletedShiftsPage
from shift.utils import (create_volunteer, create_event_with_details,
                         create_job_with_details, create_shift_with_details,
                         log_hours_with_details)


class ShiftHours(LiveServerTestCase):
    """
    Contains tests for
    - Display hours with logged and unlogged shifts.
    - Edit hours with valid values.
    - Edit hours with end time after start time.
    - Edit hours with time outside shift time.
    - Cancellation of hours.
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
        cls.completed_shifts_page = CompletedShiftsPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(ShiftHours, cls).setUpClass()

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
        super(ShiftHours, cls).tearDownClass()

    def login_volunteer(self):
        """
        Utility function to login as volunteer.
        """
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({
            'username': 'volunteer',
            'password': 'volunteer'
        })

    def register_dataset(self):
        """
        Utility function to create valid data for test.
        """
        # Create shift and log hours
        e1 = create_event_with_details(
            ['event', '2050-06-15', '2050-06-17']
        )
        j1 = create_job_with_details(
            ['job', '2050-06-15', '2050-06-15', 'job description', e1]
        )
        s1 = create_shift_with_details(
            ['2050-06-15', '09:00', '15:00', '6', j1]
        )
        log_hours_with_details(self.v1, s1, '12:00', '13:00')

    def test_view_with_unlogged_shift(self):
        """
        Test display of shift hours with unlogged shifts.
        """
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.live_server_url = self.live_server_url
        completed_shifts_page.go_to_completed_shifts()
        self.assertEqual(completed_shifts_page.remove_i18n(self.driver.current_url),
                         self.live_server_url + completed_shifts_page.view_hours_page
                         + str(self.v1.id)
        )

        self.assertEqual(completed_shifts_page.get_info_box(),
                         'You have not logged any hours.')

    def test_view_with_logged_shift(self):
        """
        Test display of shift hours with logged shifts.
        """
        self.register_dataset()
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.go_to_completed_shifts()

        self.assertEqual(completed_shifts_page.get_shift_job(), 'job')
        self.assertEqual(completed_shifts_page.get_shift_date(), 'June 15, 2050')
        self.assertEqual(completed_shifts_page.get_shift_start_time(), 'noon')
        self.assertEqual(completed_shifts_page.get_shift_end_time(), '1 p.m.')
        self.assertEqual(completed_shifts_page.get_edit_shift_hours(), 'Edit Hours')
        self.assertEqual(completed_shifts_page.get_clear_shift_hours(), 'Clear Hours')

    def test_edit_hours(self):
        """
        Test edit of the logged hours.
        """
        self.register_dataset()
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.go_to_completed_shifts()

        completed_shifts_page.edit_hours('10:00', '13:00')
        mail.outbox = []
        mail.send_mail("Edit Request", "message", "messanger@locahost.com", ["admin@admin.com"] )
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.subject, "Edit Request")
        self.assertEqual(msg.to, ['admin@admin.com'])

    def test_end_hours_less_than_start_hours(self):
        """
        Test in edit that end time is after start time.
        """
        self.register_dataset()
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.go_to_completed_shifts()

        completed_shifts_page.edit_hours('14:00', '12:00')
        completed_shifts_page.get_danger_box()
        try:
            completed_shifts_page.get_danger_box()
        except NoSuchElementException:
            raise Exception("End hours should be greater than start hours")

    def test_logged_hours_between_shift_hours(self):
        """
        Test edit of logged hours to time outside the shift.
        """
        self.register_dataset()
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.go_to_completed_shifts()

        completed_shifts_page.edit_hours('10:00', '16:00')
        self.assertEqual(completed_shifts_page.get_danger_box().text,
                         'Logged hours should be between shift hours')

    def test_cancel_hours(self):
        """
        Test clearing of shift hours.
        """
        self.register_dataset()
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.go_to_completed_shifts()

        self.assertEqual(completed_shifts_page.get_shift_job(), 'job')
        self.assertEqual(completed_shifts_page.get_clear_shift_hours(), 'Clear Hours')
        completed_shifts_page.click_to_clear_hours()

        self.assertEqual(completed_shifts_page.get_clear_shift_hours_text(), 'Clear Shift Hours')
        completed_shifts_page.submit_form()

        with self.assertRaises(NoSuchElementException):
            self.assertEqual(completed_shifts_page.get_shift_job(), 'job')

