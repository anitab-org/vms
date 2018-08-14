# third party
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.volunteerReportPage import VolunteerReportPage
from shift.utils import (create_volunteer, register_past_event_utility,
                         register_past_job_utility, register_past_shift_utility,
                         log_hours_utility)


class VolunteerReport(LiveServerTestCase):
    """
    Contains Tests for
    - Report generation with no shifts.
    - Report generation with data filled
    - Report generation with data empty
    - Only shift with logged hours are shown
    - Report details verified against the filled details.
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
        cls.report_page = VolunteerReportPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(VolunteerReport, cls).setUpClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        create_volunteer()
        self.login()

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
        super(VolunteerReport, cls).tearDownClass()

    def verify_shift_details(self, hours):
        """
        Utility function to verify the shift details.
        :param total_shifts: Total number of shifts as filled in form.
        :param hours: Total number of hours as filled in form.
        """
        total_no_of_hours = self.report_page.get_report_hours()
        self.assertEqual(total_no_of_hours, hours)

    def login(self):
        """
        Utility function to login as volunteer with correct credentials.
        """
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({
            'username': 'volunteer',
            'password': 'volunteer'
        })

    def test_report_without_any_created_shifts(self):
        """
        Test report generation with no shifts performed by volunteer.
        """
        report_page = self.report_page
        report_page.live_server_url = self.live_server_url
        report_page.navigate_to_report_page()
        report_page.submit_form()
        self.assertEqual(
            report_page.get_alert_box_text(),
            report_page.no_results_message
        )

    def test_report_with_empty_fields(self):
        """
        Test report generation with no fields filled in form.
        """
        report_page = self.report_page
        report_page.live_server_url = self.live_server_url
        register_past_event_utility()
        register_past_job_utility()
        register_past_shift_utility()
        log_hours_utility()

        report_page.navigate_to_report_page()
        report_page.submit_form()
        self.verify_shift_details('3.0')

    def test_only_logged_shifts_appear_in_report(self):
        """
        Test only shifts with logged hours is shown in report.
        """
        report_page = self.report_page
        report_page.live_server_url = self.live_server_url

        register_past_event_utility()
        register_past_job_utility()
        register_past_shift_utility()

        report_page.navigate_to_report_page()
        report_page.submit_form()
        self.assertEqual(report_page.get_alert_box_text(),
                         report_page.no_results_message)

    def test_shifts_appear_in_one_report(self):
        """
        Test only shifts with logged hours is shown in report.
        """

        report_page = self.report_page
        report_page.live_server_url = self.live_server_url
        register_past_event_utility()
        register_past_job_utility()
        register_past_shift_utility()
        log_hours_utility()

        report_page.navigate_to_report_page()
        report_page.submit_form()
        self.verify_shift_details('3.0')

        # try to create report again
        report_page.submit_form()
        self.assertEqual(report_page.get_alert_box_text(),
                         report_page.no_results_message)

    def test_date_field(self):
        """
        Test report generation using date field.
        """
        report_page = self.report_page
        report_page.live_server_url = self.live_server_url

        register_past_event_utility()
        register_past_job_utility()
        register_past_shift_utility()
        log_hours_utility()

        report_page.navigate_to_report_page()
        report_page.fill_report_form({
            'start': '2012-06-11',
            'end': '2012-06-16'
        })
        self.verify_shift_details('3.0')

        # Incorrect date
        report_page.fill_report_form({
            'start': '2015-05-10',
            'end': '2015-06-01'
        })
        self.assertEqual(
            report_page.get_alert_box_text(),
            report_page.no_results_message
        )

    def test_event_field(self):
        """
        Test event generation using event field.
        """
        report_page = self.report_page
        report_page.live_server_url = self.live_server_url

        register_past_event_utility()
        register_past_job_utility()
        register_past_shift_utility()
        log_hours_utility()

        report_page.navigate_to_report_page()
        [select1, select2] = report_page.get_event_job_selectors()
        select1.select_by_visible_text('event')

        report_page.submit_form()
        self.verify_shift_details('3.0')

    def test_job_field(self):
        """
        Test event generation using job field.
        """
        report_page = self.report_page
        report_page.live_server_url = self.live_server_url

        register_past_event_utility()
        register_past_job_utility()
        register_past_shift_utility()
        log_hours_utility()

        report_page.navigate_to_report_page()
        [select1, select2] = report_page.get_event_job_selectors()
        select2.select_by_visible_text('job')
        report_page.submit_form()
        self.verify_shift_details('3.0')

    def test_intersection_of_fields(self):
        """
        Test event generation using multiple fields at a time.
        """
        report_page = self.report_page
        report_page.live_server_url = self.live_server_url

        register_past_event_utility()
        register_past_job_utility()
        register_past_shift_utility()
        log_hours_utility()

        report_page.navigate_to_report_page()
        [select1, select2] = report_page.get_event_job_selectors()
        select1.select_by_visible_text('event')
        select2.select_by_visible_text('job')
        report_page.fill_report_form({
            'start': '2012-06-11',
            'end': '2012-06-16'})
        self.verify_shift_details('3.0')

        # Event, Job correct and date incorrect
        [select1, select2] = report_page.get_event_job_selectors()
        select1.select_by_visible_text('event')
        select2.select_by_visible_text('job')
        report_page.fill_report_form({
            'start': '2015-05-10',
            'end': '2015-06-01'
        })
        self.assertEqual(
            report_page.get_alert_box_text(),
            report_page.no_results_message
        )

