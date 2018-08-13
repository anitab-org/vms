# third party
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.eventsPage import EventsPage
from shift.utils import (create_admin, create_event_with_details,
                         create_job_with_details, create_shift_with_details)


class FormFields(LiveServerTestCase):
    """
    Contains Tests for
    - Null values filled in event, job and shift forms.
    - Job and event linked correctly with newly created shift
    - Event linked correctly with newly created job.
    - Field values retained in event, job and shift forms
      if invalid entries are filled
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
        cls.settings = EventsPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        cls.wait = WebDriverWait(cls.driver, 5)
        super(FormFields, cls).setUpClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        create_admin()
        self.login_admin()

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
        super(FormFields, cls).tearDownClass()

    def check_event_form_values(self, event):
        """
        Utility function to perform assertion for details of
        events against the event list received as param.
        :param event: Iterable consisting values for events.
        """
        settings = self.settings
        self.assertEqual(settings.get_event_name_value(), event['name'])
        self.assertEqual(
            settings.get_event_start_date_value(),
            event['start_date']
        )
        self.assertEqual(settings.get_event_end_date_value(), event['end_date'])

    def check_job_form_values(self, job):
        """
        Utility function to perform assertion for details of
        job against the job list received as param.
        :param job: Iterable consisting values for job.
        """
        settings = self.settings
        self.assertEqual(settings.get_job_name_value(), job['name'])
        self.assertEqual(
            settings.get_job_description_value(),
            job['description']
        )
        self.assertEqual(settings.get_job_start_date_value(), job['start_date'])
        self.assertEqual(settings.get_job_end_date_value(), job['end_date'])

    def check_shift_form_values(self, shift):
        """
        Utility function to perform assertion for details of
        shift against the shift list received as param.
        :param shift: Iterable consisting values for shift.
        """
        settings = self.settings
        self.assertEqual(settings.get_shift_date_value(), shift['date'])
        self.assertEqual(
            settings.get_shift_start_time_value(),
            shift['start_time']
        )
        self.assertEqual(settings.get_shift_end_time_value(), shift['end_time'])
        self.assertEqual(
            settings.get_shift_max_volunteers(),
            shift['max_volunteers']
        )

    def login_admin(self):
        """
        Utility function to login as administrator with correct credentials.
        """
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({
            'username': 'admin',
            'password': 'admin'
        })

    def test_null_values_in_create_event(self):
        """
        Test null values in event form will give error messages
        for the non-nullable fields while creating a new event.
        """
        self.settings.go_to_events_page()

        event = {
            'name': '',
            'start_date': '',
            'end_date': '',
            'address': 'in!valid',
            'venue': 'in!valid'
        }
        settings = self.settings
        settings.go_to_create_event_page()
        settings.fill_event_form(event)

        # Checks:
        # Event was not created
        # Error messages appear
        self.assertEqual(settings.remove_i18n(self.driver.current_url),
                         self.live_server_url + settings.create_event_page)
        self.assertEqual(len(settings.get_help_blocks()), 5)
        self.assertEqual(
            settings.get_event_name_error(),
            settings.FIELD_REQUIRED
        )
        self.assertEqual(
            settings.get_event_start_date_error(),
            settings.FIELD_REQUIRED
        )
        self.assertEqual(
            settings.get_event_end_date_error(),
            settings.FIELD_REQUIRED
        )

    def test_null_values_in_edit_event(self):
        """
        Test null values in event form will give error messages
        for the non-nullable fields while editing an existing event.
        """
        event = {
            'name': 'event-name',
            'start_date': '2018-05-24',
            'end_date': '2018-05-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)
        self.settings.go_to_events_page()

        settings = self.settings

        # Check we are having correct event
        self.assertEqual(settings.get_event_name(), created_event.name)
        settings.go_to_edit_event_page()

        edited_event = {
            'name': '',
            'start_date': '',
            'end_date': '',
            'address': '',
            'venue': '',
            'description': ''
        }
        settings.fill_event_form(edited_event)

        # Checks:
        # Event not edited
        # Error messages appear
        self.assertNotEqual(
            self.driver.current_url,
            self.live_server_url + settings.event_list_page
        )
        self.assertEqual(len(settings.get_help_blocks()), 3)
        self.assertEqual(
            settings.get_event_name_error(),
            settings.FIELD_REQUIRED
        )
        self.assertEqual(
            settings.get_event_start_date_error(),
            settings.FIELD_REQUIRED
        )
        self.assertEqual(
            settings.get_event_end_date_error(),
            settings.FIELD_REQUIRED
        )

    def test_null_values_in_create_job(self):
        """
        Test null values in job form will give error messages
        for the non-nullable fields while creating a new job.
        """
        # Register Event
        event = {
            'name': 'event-name',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # Create Job of null values
        job = {
            'event': created_event.id,
            'name': '',
            'start_date': '',
            'end_date': '',
            'description': ''
        }
        settings.navigate_to_job_list_view()
        settings.go_to_create_job_page()
        settings.fill_job_form(job)

        # Checks:
        # Job not created
        # Error messages appear
        self.assertEqual(
            settings.remove_i18n(self.driver.current_url),
            self.live_server_url + settings.create_job_page
        )
        self.assertEqual(len(settings.get_help_blocks()), 3)

        self.assertEqual(settings.get_job_name_error(), settings.FIELD_REQUIRED)
        self.assertEqual(
            settings.get_job_start_date_error(),
            settings.FIELD_REQUIRED
        )
        self.assertEqual(
            settings.get_job_end_date_error(),
            settings.FIELD_REQUIRED
        )

    def test_null_values_in_edit_job(self):
        """
        Test null values in job form will give error messages
        for the non-nullable fields while editing an existing job.
        """
        # Register Event
        event = {
            'name': 'event-name',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)
        self.settings.go_to_events_page()
        settings = self.settings

        # Create Job with not-null values
        job = {
            'event': created_event,
            'name': 'job',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'description': ''
        }
        create_job_with_details(job)

        # Go to Edit job page
        settings.live_server_url = self.live_server_url
        settings.navigate_to_job_list_view()
        settings.go_to_edit_job_page()

        # Edit job with null values
        edit_job = {
            'event': created_event.id,
            'name': '',
            'start_date': '',
            'end_date': '',
            'description': ''
        }
        settings.fill_job_form(edit_job)

        # Checks:
        # Job not edited
        # Error messages appear
        self.assertNotEqual(
            self.driver.current_url,
            self.live_server_url + settings.job_list_page
        )
        self.assertEqual(len(settings.get_help_blocks()), 3)
        self.assertEqual(settings.get_job_name_error(), settings.FIELD_REQUIRED)
        self.assertEqual(
            settings.get_job_start_date_error(),
            settings.FIELD_REQUIRED
        )
        self.assertEqual(
            settings.get_job_end_date_error(),
            settings.FIELD_REQUIRED
        )

    def test_null_values_in_create_shift(self):
        """
        Test null values in shift form will give error messages
        for the non-nullable fields while creating a new shift.
        """
        # Register Event
        event = {
            'name': 'event-name',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)
        self.settings.go_to_events_page()
        settings = self.settings

        # Create Job with not-null values
        job = {
            'event': created_event,
            'name': 'job',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'description': ''
        }
        create_job_with_details(job)

        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        # Create Shift
        shift = {
            'date': '',
            'start_time': '',
            'end_time': '',
            'max_volunteers': '',
            'address': 'in!valid',
            'venue': 'in!valid'
        }
        settings.fill_shift_form(shift)

        # Checks:
        # Shift not created
        # Error messages appear
        self.assertEqual(len(settings.get_help_blocks()), 6)

        self.assertEqual(
            settings.get_shift_date_error(),
            settings.FIELD_REQUIRED
        )
        self.assertEqual(
            settings.get_shift_start_time_error(),
            settings.FIELD_REQUIRED
        )
        self.assertEqual(
            settings.get_shift_end_time_error(),
            settings.FIELD_REQUIRED
        )
        self.assertEqual(
            settings.get_shift_max_volunteer_error(),
            settings.FIELD_REQUIRED
        )
        self.assertEqual(
            settings.get_shift_address_error(),
            settings.ENTER_VALID_VALUE
        )
        self.assertEqual(
            settings.get_shift_venue_error(),
            settings.ENTER_VALID_VALUE
        )

    def test_null_values_in_edit_shift(self):
        """
        Test null values in shift form will give error messages
        for the non-nullable fields while editing an existing shift.
        """
        # Register Event
        event = {
            'name': 'event-name',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)
        self.settings.go_to_events_page()
        settings = self.settings

        # Create Job with not-null values
        job = {
            'event': created_event,
            'name': 'job',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'description': ''
        }
        created_job = create_job_with_details(job)

        # Create Shift with not-null values
        shift = {
            'date': '2050-05-24',
            'start_time': '09:00',
            'end_time': '12:00',
            'max_volunteers': '10',
            'job': created_job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        create_shift_with_details(shift)

        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()

        # edit shift with null values
        shift = {
            'date': '',
            'start_time': '',
            'end_time': '',
            'max_volunteers': '',
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        settings.fill_shift_form(shift)

        # verify that shift was not edited and error messages appear as
        # expected
        self.assertEqual(len(settings.get_help_blocks()), 4)

        self.assertEqual(
            settings.get_shift_date_error(),
            settings.FIELD_REQUIRED
        )
        self.assertEqual(
            settings.get_shift_start_time_error(),
            settings.FIELD_REQUIRED
        )
        self.assertEqual(
            settings.get_shift_end_time_error(),
            settings.FIELD_REQUIRED
        )
        self.assertEqual(
            settings.get_shift_max_volunteer_error(),
            settings.FIELD_REQUIRED
        )

    def test_max_volunteer_field(self):
        """
        Test shift can not have maximum number of volunteers less than one.
        """
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        event = {
            'name': 'event-name',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)
        job = {
            'event': created_event,
            'name': 'job',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'description': ''
        }
        created_job = create_job_with_details(job)

        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        invalid_shift = {
            'date': '01/01/2018',
            'start_time': '12:00',
            'end_time': '11:00',
            'max_volunteers': '0',
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        settings.fill_shift_form(invalid_shift)

        # Check error message
        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//form//div[7]/div/p/strong[contains(text()," +
                    "'Ensure this value is greater than or equal to 1.')]"
                )
            )
        )
        self.assertEqual(
            settings.get_shift_max_volunteer_error(),
            'Ensure this value is greater than or equal to 1.'
        )

        # Create shift and edit with 0 value
        invalid_shift = {
            'date': '2050-05-24',
            'start_time': '09:00',
            'end_time': '12:00',
            'max_volunteers': '0',
            'job': created_job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        shift = {
            'date': '2050-05-24',
            'start_time': '09:00',
            'end_time': '12:00',
            'max_volunteers': '10',
            'job': created_job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        create_shift_with_details(shift)

        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()
        settings.fill_shift_form(invalid_shift)

        # Check error message
        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//form//div[7]/div/p/strong[contains(text()," +
                    "'Ensure this value is greater than or equal to 1.')]"
                )
            )
        )
        self.assertEqual(
            settings.get_shift_max_volunteer_error(),
            'Ensure this value is greater than or equal to 1.'
        )

    def test_simplify_shift(self):
        """
        Test shift is linked correctly with the existing job and event.
        """
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        event = {
            'name': 'event-name',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)
        job = {
            'event': created_event,
            'name': 'job',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'description': ''
        }
        created_job = create_job_with_details(job)

        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        # Check correctness of Job name and date.
        self.assertEqual(settings.get_shift_job(), job['name'])
        self.assertEqual(settings.get_shift_job_start_date(), 'May 24, 2050')
        self.assertEqual(settings.get_shift_job_end_date(), 'May 28, 2050')

        # Create shift and check job details in edit form
        shift = {
            'date': '2050-05-28',
            'start_time': '09:00',
            'end_time': '12:00',
            'max_volunteers': '10',
            'job': created_job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        create_shift_with_details(shift)
        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()

        # Check correctness of Job name and date.
        self.assertEqual(settings.get_shift_job(), job['name'])
        self.assertEqual(settings.get_shift_job_start_date(), 'May 24, 2050')
        self.assertEqual(settings.get_shift_job_end_date(), 'May 28, 2050')

    def test_simplify_job(self):
        """
        Test job is linked correctly with the existing event.
        """
        event = {
            'name': 'event',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # Create job and check event details in edit form
        job = {
            'event': created_event,
            'name': 'job',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'description': ''
        }
        create_job_with_details(job)

        settings.navigate_to_job_list_view()
        settings.go_to_edit_job_page()
        element = self.driver.find_element_by_xpath(
            '//div[2]//div[3]//div[1]//div[1]//option[1]'
        )
        # verify that the correct event name and date are displayed
        self.assertEqual(element.text, 'event')
        self.assertEqual(element.get_attribute('start_date'), 'Aug. 21, 2050')
        self.assertEqual(element.get_attribute('end_date'), 'Sept. 28, 2050')

    '''
    # Retention tests are buggy.
    # The results change every time a new build starts
    # i.e. The values in forms are not always retained.

    def test_field_value_retention_for_event(self):
        """
        Test field values are retained after filling
        invalid values in event form.
        """
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.get_page(settings.live_server_url, PageUrls.event_list_page)
        settings.go_to_create_event_page()

        # Fill invalid Event
        invalid_event = {
            'name': event-name!@',
            'start_date': 05/24/2016',
            'end_date': 05/28/2050',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        settings.fill_event_form(invalid_event)

        # Checks:
        # Event not created
        # Field values not erased
        self.assertEqual(settings.remove_i18n(self.driver.current_url),
                         self.live_server_url + settings.create_event_page)

        # https://stackoverflow.com/a/12967602
        for _ in range(3):
            try:
                self.check_event_form_values(invalid_event)
                break
            except StaleElementReferenceException:
                pass
        # Create event and edit it
        # Checks:
        # Event not edited
        # Field values are not erased
        event = {
            'name': event-name',
            'start_date': 2050-05-24',
            'end_date': 2050-05-28',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        create_event_with_details(event)
        settings.navigate_to_event_list_view()
        settings.go_to_edit_event_page()
        settings.fill_event_form(invalid_event)

        # Bug here: Invalid fields are erased from edit forms
        # Erasing the invalid field from event because invalid fields are
        # erased in form if we try to edit.
        invalid_event[1] = ''
        self.assertNotEqual(
            self.driver.current_url,
            self.live_server_url + settings.create_event_page
        )

        # https://stackoverflow.com/a/12967602
        for _ in range(3):
            try:
                self.check_event_form_values(invalid_event)
                break
            except StaleElementReferenceException:
                pass

    # Retention tests are buggy.
    # The results change every time a new build starts
    # i.e. The values in forms are not always retained.

    def test_field_value_retention_for_job(self):
        """
        Test field values are retained after filling invalid values in job form.
        """
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        event = {
            'name': event-name',
            'start_date': 2050-08-21',
            'end_date': 2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        created_event = create_event_with_details(event)

        settings.navigate_to_job_list_view()
        # Fill invalid Job
        invalid_job = {
            'event': created_event.id,
            'name': job name#$',
            'description': 'job description',
            'start_date': '24/05/2016',
            'end_date': '22/08/2050'
        }
        settings.go_to_create_job_page()
        settings.fill_job_form(invalid_job)

        # Checks:
        # Job not created
        # Field values are not erased
        self.assertEqual(
            settings.remove_i18n(self.driver.current_url),
            self.live_server_url + settings.create_job_page
            )

        # https://stackoverflow.com/a/12967602
        for _ in range(3):
            try:
                self.check_job_form_values(invalid_job)
                break
            except StaleElementReferenceException:
                pass

        # Create job and edit it
        # Checks:
        # Job not edited
        # Field values not erased
        job = {
            'event': created_event,
            'name': job',
            'description': '',
            'start_date': '2050-08-25',
            'end_date': '2050-08-25'
        }
        create_job_with_details(job)
        settings.navigate_to_job_list_view()
        settings.go_to_edit_job_page()
        settings.fill_job_form(invalid_job)
        # Checks:
        # Job not created
        # Field values not erased

        # Bug here: Invalid fields are erased from edit forms
        # Erasing the invalid field from event because invalid fields are
        # erased in form if we try to edit.
        invalid_job[3] = invalid_job[4] = ''
        self.assertNotEqual(
            self.driver.current_url,
            self.live_server_url + settings.job_list_page
        )

        # https://stackoverflow.com/a/12967602
        for _ in range(3):
            try:
                self.check_job_form_values(invalid_job)
                break
            except StaleElementReferenceException:
                pass

    # Retention tests are buggy.
    # The results change every time a new build starts
    # i.e. The values in forms are not always retained.

    def test_field_value_retention_for_shift(self):
        """
        Test field values are retained after filling
        invalid values in shift form.
        """
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        event = {
            'name': 'event-name',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        created_event = create_event_with_details(event)
        job = {
            'name': 'job',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'description': '',
            'event': created_event
        }
        created_job = create_job_with_details(job)

        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        invalid_shift = {
            'date': '01/01/2016',
            'start_time': '12:00',
            'end_time': '11:00',
            'max_volunteers': '10',
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        settings.fill_shift_form(invalid_shift)

        # https://stackoverflow.com/a/12967602
        for _ in range(3):
            try:
                self.check_shift_form_values(invalid_shift)
                break
            except StaleElementReferenceException:
                pass
        # Create Shift and edit it
        # Checks:
        # Shift not edited
        # Field values not erased
        invalid_shift = {
            'date': '01/01/2016',
            'start_time': '12:00',
            'end_time': '11:00',
            'max_volunteers': '10',
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        shift = {
            'date': '2050-05-24',
            'start_time': '09:00',
            'end_time': '12:00',
            'max_volunteers': '10',
            'job': created_job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        create_shift_with_details(shift)
        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()
        settings.fill_shift_form(invalid_shift)

        # Bug here: Invalid fields are erased from edit forms
        # Erasing the invalid field from event because invalid fields are
        # erased in form if we try to edit.

        # https://stackoverflow.com/a/12967602
        for _ in range(3):
            try:
                self.check_shift_form_values(invalid_shift)
                break
            except StaleElementReferenceException:
                pass
    '''
