# third party
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.core import mail

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.completedShiftsPage import CompletedShiftsPage
from shift.utils import (create_volunteer, create_event_with_details,
                         create_job_with_details, create_shift_with_details,
                         log_hours_with_details,
                         register_volunteer_for_shift_utility)


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
        firefox_options = Options()
        firefox_options.add_argument('-headless')
        cls.driver = webdriver.Firefox(firefox_options=firefox_options)
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

    def register_unlogged_dataset(self):
        """
        Utility function to register data for testing.
        """
        created_event = create_event_with_details({
            'name': 'event-unlogged',
            'start_date': '2015-06-01',
            'end_date': '2015-06-10',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        })
        created_job = create_job_with_details({
            'name': 'jobUnlogged',
            'start_date': '2015-06-01',
            'end_date': '2015-06-10',
            'description': 'job description',
            'event': created_event
        })
        created_shift = create_shift_with_details({
            'date': '2015-06-01',
            'start_time': '09:00',
            'end_time': '15:00',
            'max_volunteers': '10',
            'job': created_job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        })
        registered_shift =\
            register_volunteer_for_shift_utility(created_shift, self.v1)

    def register_logged_dataset(self):
        """
        Utility function to create valid data for test.
        """
        # Create shift and log hours
        e1 = create_event_with_details({
            'name': 'event',
            'start_date': '2015-06-15',
            'end_date': '2015-06-17',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        })
        j1 = create_job_with_details({
            'name': 'job',
            'start_date': '2015-06-15',
            'end_date': '2015-06-15',
            'description': 'job description',
            'event': e1
        })
        s1 = create_shift_with_details({
            'date': '2015-06-15',
            'start_time': '09:00',
            'end_time': '15:00',
            'max_volunteers': '6',
            'job': j1,
            'address': 'shift-address',
            'venue': 'shift-venue'
        })
        log_hours_with_details(self.v1, s1, '12:00', '13:00')

    def test_view_without_unlogged_shift(self):
        """
        Test display of shift hours without unlogged shifts.
        """
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.live_server_url = self.live_server_url
        completed_shifts_page.go_to_completed_shifts()
        self.assertEqual(
            completed_shifts_page.remove_i18n(self.driver.current_url),
            self.live_server_url +
            completed_shifts_page.view_hours_page +
            str(self.v1.id)
        )

        self.assertEqual(completed_shifts_page.get_unlogged_info_box(),
                         'You have no unlogged shifts.')

    def test_view_without_logged_shift(self):
        """
        Test display of shift hours without logged shifts.
        """
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.live_server_url = self.live_server_url
        completed_shifts_page.go_to_completed_shifts()
        self.assertEqual(
            completed_shifts_page.remove_i18n(self.driver.current_url),
            self.live_server_url +
            completed_shifts_page.view_hours_page +
            str(self.v1.id)
        )

        self.assertEqual(completed_shifts_page.get_logged_info_box(),
                         'You have not logged any hours.')

    def test_view_with_unlogged_shift(self):
        """
        Test display of shift hours with logged shifts.
        """
        self.register_unlogged_dataset()
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.go_to_completed_shifts()

        self.assertEqual(
            completed_shifts_page.get_unlogged_shift_job(),
            'jobUnlogged'
        )
        self.assertEqual(
            completed_shifts_page.get_unlogged_shift_date(),
            'June 1, 2015'
        )
        self.assertEqual(
            completed_shifts_page.get_unlogged_shift_start_time(),
            '9 a.m.'
        )
        self.assertEqual(
            completed_shifts_page.get_unlogged_shift_end_time(),
            '3 p.m.'
        )
        self.assertEqual(
            completed_shifts_page.get_log_hours(),
            'Log Hours'
        )

    def test_log_hours(self):
        self.register_unlogged_dataset()
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.live_server_url = self.live_server_url
        completed_shifts_page.go_to_completed_shifts()

        self.assertEqual(completed_shifts_page.get_log_hours(), 'Log Hours')

        completed_shifts_page.click_to_log_hours()
        completed_shifts_page.log_shift_timings('09:00', '12:00')

        # Check logged shift does not appear in unlogged Shifts
        completed_shifts_page.go_to_completed_shifts()
        self.assertEqual(completed_shifts_page.get_unlogged_info_box(),
                         "You have no unlogged shifts.")
        with self.assertRaises(NoSuchElementException):
            completed_shifts_page.get_result_container()

    def test_view_with_logged_shift(self):
        """
        Test display of shift hours with logged shifts.
        """
        self.register_logged_dataset()
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.go_to_completed_shifts()

        self.assertEqual(completed_shifts_page.get_logged_shift_job(), 'job')
        self.assertEqual(
            completed_shifts_page.get_logged_shift_date(),
            'June 15, 2015'
        )
        self.assertEqual(
            completed_shifts_page.get_logged_shift_start_time(),
            'noon'
        )
        self.assertEqual(
            completed_shifts_page.get_logged_shift_end_time(),
            '1 p.m.'
        )
        self.assertEqual(completed_shifts_page.get_edit_hours(), 'Edit Hours')

    def test_edit_hours(self):
        """
        Test edit of the logged hours.
        """
        self.register_logged_dataset()
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.go_to_completed_shifts()

        completed_shifts_page.edit_hours('10:00', '13:00')
        mail.outbox = []
        mail.send_mail(
            "Edit Request", "message",
            "messanger@locahost.com", ["admin@admin.com"]
        )
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.subject, "Edit Request")
        self.assertEqual(msg.to, ['admin@admin.com'])

    def test_end_hours_less_than_start_hours(self):
        """
        Test in edit that end time is after start time.
        """
        self.register_logged_dataset()
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
        self.register_logged_dataset()
        completed_shifts_page = self.completed_shifts_page
        completed_shifts_page.go_to_completed_shifts()

        completed_shifts_page.edit_hours('10:00', '16:00')
        self.assertEqual(completed_shifts_page.get_danger_box().text,
                         'Logged hours should be between shift hours')

