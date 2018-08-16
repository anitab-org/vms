# third party
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.jobDetailsPage import JobDetailsPage
from shift.utils import (create_admin, create_event_with_details,
                         create_job_with_details)


class JobDetails(LiveServerTestCase):
    """
    Contains Tests for Job app.
    - Creation with valid and invalid values.
    - Edit with valid and invalid values.
    - Deletion of registered job.
    - Registering job with no event registered
    - Registering with start date after end date.
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
        cls.job_details_page = JobDetailsPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(JobDetails, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """
        Class method to quit the Firefox WebDriver session after
        execution of all tests in class.
        """
        cls.driver.quit()
        super(JobDetails, cls).tearDownClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        self.admin = create_admin()
        self.login_admin()

    def tearDown(self):
        """
        Method consists of statements to be executed at
        end of each test.
        """
        self.authentication_page.logout()

    @staticmethod
    def register_valid_event():
        """
        Utility function to register event with valid details.
        :return: Event type object.
        """
        created_event = create_event_with_details({
            'name': 'event',
            'start_date': '2050-06-11',
            'end_date': '2050-06-19',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        })
        return created_event

    @staticmethod
    def register_valid_job(created_event):
        """
        Utility function to register job with valid details.
        :param created_event: Event type object.
        :return: Job type object.
        """
        created_job = create_job_with_details({
            'name': 'job',
            'start_date': '2050-06-15',
            'end_date': '2050-06-18',
            'description': '',
            'event': created_event
        })
        return created_job

    def check_error_messages(self):
        """
        Utility function to check error messages which appear in job form.
        """
        job_details_page = self.job_details_page
        error_message = job_details_page.FIELD_REQUIRED
        self.assertEqual(len(job_details_page.get_help_blocks()), 3)
        self.assertEqual(job_details_page.get_job_name_error(), error_message)
        self.assertEqual(
            job_details_page.get_job_start_date_error(),
            error_message
        )
        self.assertEqual(
            job_details_page.get_job_end_date_error(),
            error_message
        )

    def login_admin(self):
        """
        Utility function to login as administrator.
        """
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.login(
            {
                'username': 'admin',
                'password': 'admin'
            }
        )

    def test_job_details_view(self):
        """
        Test job details view table with registered job.
        """
        created_event = JobDetails.register_valid_event()

        self.job_details_page.navigate_to_event_list_view()

        created_job = JobDetails.register_valid_job(created_event)

        job_details_page = self.job_details_page
        job_details_page.live_server_url = self.live_server_url
        job_details_page.navigate_to_job_details_view()

        # Verify details
        self.assertEqual(job_details_page.get_name(), created_job.name)
        self.assertEqual(job_details_page.get_start_date(), 'June 15, 2050')
        self.assertEqual(job_details_page.get_end_date(), 'June 18, 2050')
        self.assertEqual(job_details_page.get_event_name(), created_event.name)

    def test_valid_job_create(self):
        """
        Test job creation with valid values.
        """
        created_event = JobDetails.register_valid_event()
        self.job_details_page.navigate_to_event_list_view()
        created_job = JobDetails.register_valid_job(created_event)

        job_details_page = self.job_details_page
        job_details_page.live_server_url = self.live_server_url
        job_details_page.navigate_to_job_details_view()

        # Check job creation
        self.assertEqual(job_details_page.get_name(), created_job.name)
        self.assertEqual(job_details_page.get_event_name(), created_event.name)

    def test_invalid_job_create(self):
        """
        Test job creation with invalid values.
        """
        created_event = JobDetails.register_valid_event()
        self.job_details_page.navigate_to_event_list_view()

        job_details_page = self.job_details_page
        job_details_page.live_server_url = self.live_server_url

        # Create empty job
        job = {
            'event': created_event.id,
            'name': '',
            'description': '',
            'start_date': '',
            'end_date': ''
        }
        job_details_page.navigate_to_job_list_view()
        job_details_page.go_to_create_job_page()
        job_details_page.fill_job_form(job)

        # Check error messages
        self.check_error_messages()

    def test_invalid_job_edit(self):
        """
        Test job edit with invalid values.
        """
        created_event = JobDetails.register_valid_event()
        self.job_details_page.navigate_to_event_list_view()
        JobDetails.register_valid_job(created_event)

        job_details_page = self.job_details_page
        job_details_page.live_server_url = self.live_server_url
        job_details_page.navigate_to_job_list_view()
        job_details_page.go_to_edit_job_page()

        null_valued_job = {
            'event': created_event.id,
            'name': '',
            'description': '',
            'start_date': '',
            'end_date': ''
        }
        job_details_page.fill_job_form(null_valued_job)
        self.check_error_messages()

    def test_valid_job_edit(self):
        """
        Test job edit with valid values.
        """
        created_event = JobDetails.register_valid_event()
        self.job_details_page.navigate_to_event_list_view()
        JobDetails.register_valid_job(created_event)

        job_details_page = self.job_details_page
        job_details_page.live_server_url = self.live_server_url
        job_details_page.navigate_to_job_list_view()

        edit_job = {
            'event': 'event',
            'name': 'new job name',
            'description': 'new-job-description',
            'start_date': '2050-06-16',
            'end_date': '2050-06-16'
        }
        job_details_page.go_to_edit_job_page()
        job_details_page.fill_job_form(edit_job)
        job_details_page.navigate_to_job_list_view()

        self.assertEqual(job_details_page.get_name(), edit_job['name'])
        self.assertEqual(
            job_details_page.get_description(),
            edit_job['description']
        )

    def test_job_delete(self):
        """
        Test job deletion.
        """
        job_details_page = self.job_details_page
        job_details_page.live_server_url = self.live_server_url

        created_event = JobDetails.register_valid_event()
        job_details_page.navigate_to_event_list_view()
        JobDetails.register_valid_job(created_event)

        job_details_page.navigate_to_job_list_view()
        self.assertEqual(job_details_page.get_delete_element('').text, 'Delete')
        job_details_page.get_delete_element('//a').click()
        self.assertEqual(job_details_page.get_deletion_context(), 'Delete Job')
        job_details_page.submit_form()

    def test_create_job_with_no_event_present(self):
        """
        Test job creation with no registered events present.
        """
        job_details_page = self.job_details_page
        job_details_page.navigate_to_event_list_view()
        job_details_page.click_link(job_details_page.jobs_tab)
        self.assertEqual(job_details_page.remove_i18n(self.driver.current_url),
                         self.live_server_url + job_details_page.job_list_page)
        self.assertEqual(job_details_page.get_message_context(),
                         job_details_page.NO_JOBS_PRESENT)

        job_details_page.click_link(job_details_page.create_job_tab)
        self.assertEqual(
            job_details_page.remove_i18n(self.driver.current_url),
            self.live_server_url + job_details_page.create_job_page
        )
        self.assertEqual(job_details_page.get_message_context(),
                         job_details_page.ADD_EVENTS_TO_JOB)

    def test_start_date_after_end_date(self):
        """
        Test start date of job after end date.
        """
        created_event = JobDetails.register_valid_event()
        self.job_details_page.navigate_to_event_list_view()

        job_details_page = self.job_details_page
        job_details_page.live_server_url = self.live_server_url
        job_details_page.navigate_to_job_list_view()
        job_details_page.go_to_create_job_page()

        job_start_after_end = {
            'event': created_event.id,
            'name': 'job name',
            'description': 'job-description',
            'start_date': '2050-06-17',
            'end_date': '2050-06-16'
        }
        job_details_page.fill_job_form(job_start_after_end)

        # Check error.
        self.assertEqual(job_details_page.get_job_start_date_error(),
                         job_details_page.START_BEFORE_END)


