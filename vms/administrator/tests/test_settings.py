# third party
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from pom.pages.eventsPage import EventsPage
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.jobDetailsPage import JobDetailsPage
from pom.locators.eventsPageLocators import EventsPageLocators
from shift.utils import (create_admin_with_unlisted_org,
                         create_event_with_details,
                         create_job_with_details, create_organization,
                         create_shift_with_details, create_volunteer,
                         register_volunteer_for_shift_utility)


class Settings(LiveServerTestCase):
    """
    Settings Class contains UI testcases for `Events` tab in
    Administrator profile. This view consists of Events, Jobs, Shifts,
    Organization tabs.

    Event:
        - Null values in Create and edit event form
        - Create Event
        - Edit Event
        - Delete Event with No Associated Job
        - Delete event with Associated Job

    Job:
        - Null values in Create and edit job form
        - Create Job without any event
        - Edit Job
        - Create/Edit Job with invalid dates
        - Delete Job without Associated Shift
        - Delete Job with Shifts

    Shift:
        - Null values in Create and edit shift form
        - Create Shift without any Job
        - Edit Shift
        - Delete shift
        - Delete shift with volunteer
        - Create/Edit Shift with invalid timing
        - Create/Edit Shift with invalid date

    Organization:
        - Create Organization
        - Edit Organization
        - Replication of Organization
        - Delete Org's with registered volunteers
        - Delete Org without registered volunteers

    Additional Note:
    It needs to be ensured that the dates in the test functions
    given below are later than the current date so that there are no
    failures while creating an event. Due to this reason, the date
    at several places has been updated to 2050
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
        cls.job_details_page = JobDetailsPage(cls.driver)
        cls.elements = EventsPageLocators()
        super(Settings, cls).setUpClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        create_admin_with_unlisted_org()
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
        super(Settings, cls).tearDownClass()

    def login_admin(self):
        """
        Utility function to login as administrator with correct credentials.
        """
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({
            'username': 'admin',
            'password': 'admin'
        })

    def delete_event_from_list(self):
        """
        Utility function to delete a particular event.
        """
        settings = self.settings
        self.assertEqual(
            settings.element_by_xpath(self.elements.DELETE_EVENT).text,
            'Delete'
        )
        settings.element_by_xpath(self.elements.DELETE_EVENT + '//a').click()
        self.assertNotEqual(settings.get_deletion_box(), None)
        self.assertEqual(settings.get_deletion_context(), 'Delete Event')
        settings.submit_form()

    def delete_job_from_list(self):
        """
        Utility function to delete a particular job.
        """
        settings = self.settings
        self.assertEqual(
            settings.element_by_xpath(self.elements.DELETE_JOB).text,
            'Delete'
        )
        settings.element_by_xpath(self.elements.DELETE_JOB + '//a').click()

        self.assertNotEqual(settings.get_deletion_box(), None)
        self.assertEqual(settings.get_deletion_context(), 'Delete Job')
        settings.submit_form()

    def delete_shift_from_list(self):
        """
        Utility function to delete a particular shift.
        """
        settings = self.settings
        self.assertEqual(
            settings.element_by_xpath(self.elements.DELETE_SHIFT).text,
            'Delete'
        )
        settings.element_by_xpath(self.elements.DELETE_SHIFT + '//a').click()

        # confirm on delete
        self.assertNotEqual(settings.get_deletion_box(), None)
        self.assertEqual(settings.get_deletion_context(), 'Delete Shift')
        settings.submit_form()

    def delete_organization_from_list(self):
        """
        Utility function to delete a particular organization.
        """
        settings = self.settings
        self.assertEqual(
            settings.element_by_xpath(self.elements.DELETE_ORG).text,
            'Delete'
        )
        settings.element_by_xpath(self.elements.DELETE_ORG + '//a').click()

        # confirm on delete
        self.assertNotEqual(settings.get_deletion_box(), None)
        self.assertEqual(settings.get_deletion_context(), 'Delete Organization')
        settings.submit_form()

    def test_event_tab(self):
        """
        Test event details view with no events registered.
        """
        self.settings.go_to_events_page()
        settings = self.settings

        self.assertEqual(settings.get_message_context(), 'No event found.')

    def test_job_tab_and_create_job_without_event(self):
        """
        Test job details view with no events registered.
        """
        self.settings.go_to_events_page()
        settings = self.settings
        settings.click_link(settings.jobs_tab)
        self.assertEqual(
            settings.remove_i18n(self.driver.current_url),
            self.live_server_url + settings.job_list_page
        )
        self.assertEqual(
            settings.get_message_context(),
            self.job_details_page.NO_JOBS_PRESENT
        )
        settings.click_link('Create Job')
        self.assertEqual(
            settings.remove_i18n(self.driver.current_url),
            self.live_server_url + settings.create_job_page
        )
        self.assertEqual(
            settings.get_message_context(),
            'Please add events to associate with jobs first.'
        )

    def test_shift_tab_and_create_shift_without_job(self):
        """
        Test shift details view with no jobs registered.
        """
        self.settings.go_to_events_page()
        settings = self.settings
        settings.click_link(settings.shift_tab)
        self.assertEqual(
            settings.remove_i18n(self.driver.current_url),
            self.live_server_url + settings.shift_list_page
        )
        self.assertEqual(
            settings.get_message_context(),
            self.job_details_page.NO_JOBS_PRESENT
        )

    def test_create_event(self):
        """
        Test event creation with valid values.
        """
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        settings.go_to_create_event_page()
        settings.fill_event_form(event)
        settings.navigate_to_event_list_view()

        # Check event created
        self.assertEqual(
            settings.remove_i18n(self.driver.current_url),
            self.live_server_url + settings.event_list_page
        )
        self.assertEqual(settings.get_event_name(), event['name'])

    ''' commented till the portal gets live with its api
    def test_create_event_from_meetup(self):
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.go_to_create_event_page()
        settings.create_meetup()
        self.assertEqual(
            settings.remove_i18n(self.driver.current_url),
            self.live_server_url + settings.event_list_page
        )
    '''

    def test_edit_event(self):
        """
        Test event edit with valid values.
        """
        event = {
            'name': 'event-name',
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

        # Create event
        settings.navigate_to_event_list_view()
        self.assertEqual(settings.get_event_name(), created_event.name)

        settings.go_to_edit_event_page()
        edited_event = {
            'name': 'new-event-name',
            'start_date': '2050-09-21',
            'end_date': '2050-09-28',
            'address': 'new-event-address',
            'venue': 'new-event-venue',
            'description': 'event-description'
        }
        settings.fill_event_form(edited_event)
        settings.navigate_to_event_list_view()

        # Check event edit
        self.assertEqual(
            settings.remove_i18n(self.driver.current_url),
            self.live_server_url + settings.event_list_page
        )
        self.assertEqual(
            settings.get_event_name(),
            edited_event['name']
        )

    def test_create_and_edit_event_with_invalid_start_date(self):
        """
        Test event creation and edit with invalid start date.
        """
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.go_to_create_event_page()
        invalid_event = {
            'name': 'event-name-invalid',
            'start_date': '05/17/2016',
            'end_date': '09/28/2016',
            'address': 'event-address-invalid',
            'venue': 'event-venue-invalid',
            'description': 'event-description'
        }
        settings.fill_event_form(invalid_event)

        # Check event not created and error message displayed
        self.assertNotEqual(
            self.driver.current_url,
            self.live_server_url + settings.event_list_page
        )
        self.assertEqual(
            settings.get_warning_context(),
            "Start date should be today's date or later."
        )

        settings.navigate_to_event_list_view()
        settings.go_to_create_event_page()
        valid_event = {
            'name': 'event-name',
            'start_date': '2050-05-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        valid_event_created = create_event_with_details(valid_event)

        settings.navigate_to_event_list_view()
        self.assertEqual(settings.get_event_name(), valid_event_created.name)

        settings.go_to_edit_event_page()
        settings.fill_event_form(invalid_event)

        # check event not edited and error message displayed
        self.assertNotEqual(
            self.driver.current_url,
            self.live_server_url + settings.event_list_page
        )
        self.assertEqual(
            settings.get_warning_context(),
            "Start date should be today's date or later."
        )

    def test_edit_event_with_elapsed_start_date(self):
        """
        Test edit of an event which is currently going on.
        """
        elapsed_event = {
            'name': 'event-name',
            'start_date': '2016-05-21',
            'end_date': '2050-08-09',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }

        # Create an event with elapsed start date
        created_event = create_event_with_details(elapsed_event)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_event_list_view()
        self.assertEqual(settings.get_event_name(), created_event.name)

        settings.go_to_edit_event_page()

        # Try editing any one field - (event name in this case)
        settings.element_by_xpath(self.elements.CREATE_EVENT_NAME).clear()
        settings.send_value_to_xpath(
            self.elements.CREATE_EVENT_NAME,
            'changed-event-name'
        )
        settings.submit_form()

        # check event not edited
        self.assertNotEqual(
            self.driver.current_url,
            self.live_server_url + settings.event_list_page
        )

    def test_edit_event_with_invalid_job_date(self):
        """
        Test edit of event with invalid date such that
        the job dates do not lie in it.
        """
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # Create Job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-21',
            'description': '',
            'event': created_event
        }
        create_job_with_details(job)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_event_list_view()

        self.assertEqual(settings.get_event_name(), created_event.name)
        settings.go_to_edit_event_page()

        # Edit event such that job is no longer in the new date range
        new_event = {
            'name': 'new-event-name',
            'start_date': '2017-08-30',
            'end_date': '2017-09-21',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        settings.fill_event_form(new_event)

        # check event not edited and error message displayed
        self.assertNotEqual(
            self.driver.current_url,
            self.live_server_url + settings.event_list_page
        )
        self.assertEqual(
            settings.element_by_xpath(
                self.elements.TEMPLATE_ERROR_MESSAGE
            ).text,
            'You cannot edit this event as the following associated '
            'job no longer lies within the new date range :'
        )

    def test_delete_event_with_no_associated_job(self):
        """
        Test deletion of events with no jobs linked.
        """
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # create event
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_event_list_view()
        self.assertEqual(settings.get_event_name(), created_event.name)

        self.delete_event_from_list()
        settings.navigate_to_event_list_view()

        # check event deleted
        self.assertEqual(
            settings.remove_i18n(self.driver.current_url),
            self.live_server_url + settings.event_list_page
        )
        with self.assertRaises(NoSuchElementException):
            settings.get_results()

    def test_delete_event_with_associated_job(self):
        """
        Test deletion of events with linked jobs.
        """
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # create job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-21',
            'description': '',
            'event': created_event
        }
        create_job_with_details(job)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # check event created
        settings.navigate_to_event_list_view()
        self.assertEqual(settings.get_event_name(), created_event.name)

        # delete event
        self.delete_event_from_list()

        self.assertNotEqual(settings.get_danger_message(), None)
        self.assertEqual(
            settings.get_template_error_message(),
            'You cannot delete an event that a job '
            'is currently associated with.'
        )

        # check event NOT deleted
        settings.navigate_to_event_list_view()
        self.assertEqual(settings.get_event_name(), event['name'])

    def test_create_job(self):
        """
        Test creation of job with valid values.
        """
        # register event first to create job
        event = {
            'name': 'event-name',
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

        # create job
        job = {
            'event': 'event-name',
            'name': 'job name',
            'description': 'job description',
            'start_date': '2050-08-21',
            'end_date': '2050-08-28'
        }
        settings.navigate_to_job_list_view()
        settings.go_to_create_job_page()
        settings.fill_job_form(job)

        # check job created
        settings.navigate_to_job_list_view()
        self.assertEqual(settings.get_job_name(), job['name'])
        self.assertEqual(settings.get_job_event(), created_event.name)

    def test_edit_job(self):
        """
        Test edit of job with valid values.
        """
        # register event first to create job
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # create job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-21',
            'description': '',
            'event': created_event
        }
        create_job_with_details(job)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        edit_job = {
            'event': 'event-name',
            'name': 'changed job name',
            'description': 'job description',
            'start_date': '2050-08-25',
            'end_date': '2050-08-25'
        }
        settings.navigate_to_job_list_view()
        settings.go_to_edit_job_page()
        settings.fill_job_form(edit_job)

        settings.navigate_to_job_list_view()
        # check job edited
        self.assertEqual(
            settings.remove_i18n(self.driver.current_url),
            self.live_server_url + settings.job_list_page
        )
        self.assertEqual(settings.get_job_name(), edit_job['name'])

    def test_create_job_with_invalid_event_date(self):
        """
        Test creation of job with date not lying in event's date.
        """
        # register event first to create job
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        create_event_with_details(event)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # create job with start date outside range
        job = {
            'event': 'event-name',
            'name': 'job name',
            'description': 'job description',
            'start_date': '08/10/2050',
            'end_date': '09/11/2050'
        }
        settings.navigate_to_job_list_view()
        settings.go_to_create_job_page()
        settings.fill_job_form(job)

        # check job not created and proper error message displayed
        self.assertNotEqual(
            self.driver.current_url,
            self.live_server_url + settings.job_list_page
        )
        self.assertEqual(
            settings.get_warning_context(),
            'Job dates should lie within Event dates'
        )

        # create job with end date outside range
        job = {
            'event': 'event-name',
            'name': 'job name',
            'description': 'job description',
            'start_date': '08/30/2050',
            'end_date': '09/29/2050'
        }
        settings.navigate_to_job_list_view()
        settings.go_to_create_job_page()
        settings.fill_job_form(job)

        # check job not created and proper error message displayed
        self.assertNotEqual(
            self.driver.current_url,
            self.live_server_url + settings.job_list_page
        )
        self.assertEqual(
            settings.get_warning_context(),
            'Job dates should lie within Event dates'
        )

    def test_edit_job_with_invalid_event_date(self):
        """
        Test edit of job with date not lying in event's date.
        """
        # register event first to create job
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # create job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-21',
            'description': '',
            'event': created_event
        }
        create_job_with_details(job)

        invalid_job_one = {
            'event': 'event-name',
            'name': 'changed job name',
            'description': 'job description',
            'start_date': '2050-05-03',
            'end_date': '2050-11-09'
        }

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # edit job with start date outside event start date
        settings.navigate_to_job_list_view()
        settings.go_to_edit_job_page()
        settings.fill_job_form(invalid_job_one)

        # check job not edited and proper error message displayed
        self.assertNotEqual(
            self.driver.current_url,
            self.live_server_url + settings.job_list_page
        )
        self.assertEqual(
            settings.get_warning_context(),
            'Job dates should lie within Event dates'
        )

        invalid_job_two = {
            'event': 'event-name',
            'name': 'changed job name',
            'description': 'job description',
            'start_date': '2050-09-14',
            'end_date': '2050-12-31'
        }
        settings.navigate_to_job_list_view()
        settings.go_to_edit_job_page()
        settings.fill_job_form(invalid_job_two)

        # check job not edited and proper error message displayed
        self.assertNotEqual(
            self.driver.current_url,
            self.live_server_url + settings.job_list_page
        )
        self.assertEqual(
            settings.get_warning_context(),
            'Job dates should lie within Event dates'
        )

    def test_edit_job_with_invalid_shift_date(self):
        """
        Test edit of job with date not lying in shift's date.
        """

        # register event first to create job
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # create job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-21',
            'description': '',
            'event': created_event
        }
        created_job = create_job_with_details(job)

        # create shift
        shift = {
            'date': '2050-08-21',
            'start_time': '09:00',
            'end_time': '12:00',
            'max_volunteers': '10',
            'job': created_job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        create_shift_with_details(shift)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_job_list_view()

        invalid_job_one = {
            'event': 'event-name',
            'name': 'changed job name',
            'description': 'job description',
            'start_date': '2050-09-01',
            'end_date': '2050-09-11'
        }

        # edit job with date range such that the shift start date no longer
        # falls in the range
        settings.go_to_edit_job_page()
        settings.fill_job_form(invalid_job_one)

        # check job not edited and proper error message displayed
        self.assertNotEqual(
            self.driver.current_url,
            self.live_server_url + settings.job_list_page
        )
        self.assertEqual(
            settings.get_template_error_message(),
            'You cannot edit this job as 1 associated shift '
            'no longer lies within the new date range'
        )

    def test_delete_job_without_associated_shift(self):
        """
        Test deletion of job with shifts not linked.
        """
        # register event first to create job
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # create job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-21',
            'description': '',
            'event': created_event
        }
        create_job_with_details(job)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_job_list_view()
        self.assertEqual(settings.get_job_name(), 'job')
        self.assertEqual(settings.get_job_event(), 'event-name')

        # delete job
        self.delete_job_from_list()
        settings.navigate_to_job_list_view()

        # check event deleted
        self.assertEqual(
            settings.remove_i18n(self.driver.current_url),
            self.live_server_url + settings.job_list_page
        )
        with self.assertRaises(NoSuchElementException):
            settings.get_results()

    def test_delete_job_with_associated_shifts(self):
        """
        Test deletion of job with shifts linked.
        """
        # register event first to create job
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # create job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-21',
            'description': '',
            'event': created_event
        }
        created_job = create_job_with_details(job)

        # create shift
        shift = {
            'date': '2050-08-21',
            'start_time': '09:00',
            'end_time': '12:00',
            'max_volunteers': '10',
            'job': created_job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        create_shift_with_details(shift)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # delete job
        settings.navigate_to_job_list_view()
        self.delete_job_from_list()

        self.assertNotEqual(settings.get_danger_message(), None)
        self.assertEqual(
            settings.get_template_error_message(),
            'You cannot delete a job that a shift is '
            'currently associated with.'
        )

        # check job NOT deleted
        settings.navigate_to_job_list_view()
        self.assertEqual(settings.get_job_name(), job['name'])

    def test_create_shift(self):
        """
        Test creation of shift with valid values.
        """
        # register event first to create job
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # create job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-30',
            'description': '',
            'event': created_event
        }
        create_job_with_details(job)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # create shift
        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        shift = {
            'date': '08/30/2050',
            'start_time': '09:00',
            'end_time': '12:00',
            'max_volunteers': '10',
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        settings.fill_shift_form(shift)

        # verify that shift was created
        self.assertNotEqual(settings.get_results(), None)
        with self.assertRaises(NoSuchElementException):
            settings.get_help_block()

    def test_create_shift_with_invalid_timings(self):
        """
        Test creation of shift with invalid time.
        """
        # register event first to create job
        event = {
            'name': 'event-name',
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

        # create job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-30',
            'description': '',
            'event': created_event
        }
        create_job_with_details(job)

        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        # create shift where end hours is less than start hours
        shift = {
            'date': '08/30/2050',
            'start_time': '14:00',
            'end_time': '12:00',
            'max_volunteers': '5',
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        settings.fill_shift_form(shift)

        # verify that shift was not created and error message displayed
        self.assertEqual(
            settings.get_help_block().text,
            'Start time must be before the end time'
        )

    def test_edit_shift_with_invalid_timings(self):
        """
        Test edit of shift with invalid time.
        """
        # register event first to create job
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # create job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-30',
            'description': '',
            'event': created_event
        }
        created_job = create_job_with_details(job)

        # create shift
        shift = {
            'date': '2050-08-21',
            'start_time': '09:00',
            'end_time': '12:00',
            'max_volunteers': '10',
            'job': created_job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        create_shift_with_details(shift)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()

        # edit shift with end hours less than start hours
        invalid_shift = {
            'date': '08/30/2050',
            'start_time': '18:00',
            'end_time': '13:00',
            'max_volunteers': '5',
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        settings.fill_shift_form(invalid_shift)

        # verify that shift was not edited and error message displayed
        self.assertEqual(
            settings.get_help_block().text,
            'Start time must be before the end time'
        )

    def test_create_shift_with_invalid_date(self):
        """
        Test creation of shift with date not lying in job's date.
        """
        # register event first to create job
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # create job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-30',
            'description': '',
            'event': created_event
        }
        create_job_with_details(job)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # create shift
        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        shift = {
            'date': '06/30/2050',
            'start_time': '14:00',
            'end_time': '18:00',
            'max_volunteers': '5',
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        settings.fill_shift_form(shift)

        # verify that shift was not created and error message displayed
        self.assertEqual(
            settings.get_warning_context(),
            'Shift date should lie within Job dates'
        )

    def test_edit_shift_with_invalid_date(self):
        """
        Test edit of shift with date not lying in job's date.
        """
        # register event first to create job
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # create job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-30',
            'description': '',
            'event': created_event
        }
        created_job = create_job_with_details(job)

        # create shift
        shift = {
            'date': '2050-08-21',
            'start_time': '09:00',
            'end_time': '12:00',
            'max_volunteers': '10',
            'job': created_job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        create_shift_with_details(shift)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()

        # edit shift with date not between job dates
        invalid_shift = {
            'date': '02/05/2050',
            'start_time': '04:00',
            'end_time': '13:00',
            'max_volunteers': '2',
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        settings.fill_shift_form(invalid_shift)

        # verify that shift was not edited and error message displayed
        self.assertEqual(
            settings.get_warning_context(),
            'Shift date should lie within Job dates'
        )

    def test_edit_shift(self):
        """
        Test edit of shift with valid values.
        """
        # register event first to create job
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # create job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-30',
            'description': '',
            'event': created_event
        }
        created_job = create_job_with_details(job)

        # create shift
        shift = {
            'date': '2050-08-21',
            'start_time': '09:00',
            'end_time': '12:00',
            'max_volunteers': '10',
            'job': created_job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        create_shift_with_details(shift)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()

        # edit shift with date between job dates
        shift = {
            'date': '08/25/2050',
            'start_time': '10:00',
            'end_time': '13:00',
            'max_volunteers': '2',
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        settings.fill_shift_form(shift)

        with self.assertRaises(NoSuchElementException):
            settings.get_help_block()

        self.assertEqual(settings.get_shift_date(), 'Aug. 25, 2050')

    def test_delete_shift(self):
        """
        Test deletion of shift.
        """
        # register event first to create job
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # create job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-30',
            'description': '',
            'event': created_event
        }
        created_job = create_job_with_details(job)

        # create shift
        shift = {
            'date': '2050-08-21',
            'start_time': '09:00',
            'end_time': '12:00',
            'max_volunteers': '10',
            'job': created_job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        create_shift_with_details(shift)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()
        self.assertNotEqual(settings.get_results(), None)

        # delete shift
        self.delete_shift_from_list()

        # check deletion of shift
        settings.navigate_to_shift_list_view()
        self.assertEqual(
            settings.get_message_context(),
            'There are currently no shifts. Please create shifts first.'
        )

    def test_delete_shift_with_volunteer(self):
        """
        Test deletion of shift with volunteer linked with it.
        """
        # register event first to create job
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # create job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-30',
            'description': '',
            'event': created_event
        }
        created_job = create_job_with_details(job)

        # create shift
        shift = {
            'date': '2050-08-21',
            'start_time': '09:00',
            'end_time': '12:00',
            'max_volunteers': '10',
            'job': created_job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        created_shift = create_shift_with_details(shift)

        # create volunteer for shift
        volunteer = create_volunteer()
        register_volunteer_for_shift_utility(created_shift, volunteer)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()

        # delete shift
        self.delete_shift_from_list()

        # check error message displayed and shift not deleted
        self.assertEqual(
            settings.get_template_error_message(),
            'You cannot delete a shift that a volunteer has signed up for.'
        )

    def test_organization(self):
        """
        Test creation of organization with valid values.
        """
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.click_link(settings.organization_tab)
        self.assertEqual(settings.remove_i18n(self.driver.current_url),
                         self.live_server_url + settings.organization_list_page)

        settings.click_link('Create Organization')
        self.assertEqual(
            settings.remove_i18n(self.driver.current_url),
            self.live_server_url + settings.create_organization_page
        )

        # Test all valid characters for organization
        # [(A-Z)|(a-z)|(0-9)|(\s)|(\-)|(:)]
        settings.fill_organization_form('Org-name 92:4 CA')
        self.assertEqual(settings.get_org_name(), 'Org-name 92:4 CA')

    def test_replication_of_organization(self):
        """
        Test creation of organization with name same as that of existing one.
        """
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_organization_view()
        settings.go_to_create_organization_page()

        settings.fill_organization_form('Organization')
        self.assertEqual(settings.get_org_name(), 'Organization')

        # Create same organization again
        settings.go_to_create_organization_page()
        settings.fill_organization_form('Organization')

        self.assertEqual(
            settings.get_help_block().text,
            'Organization with this Name already exists.'
        )

    def test_edit_org(self):
        """
        Test edit of organization with valid values.
        """
        # create org
        create_organization()
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_organization_view()

        # edit org
        self.assertEqual(
            settings.element_by_xpath(self.elements.EDIT_ORG).text,
            'Edit'
        )
        settings.element_by_xpath(self.elements.EDIT_ORG + '//a').click()

        settings.fill_organization_form('changed-organization')

        # check edited org
        org_list = list()
        org_list.append(settings.get_org_name())

        self.assertTrue('changed-organization' in org_list)

    def test_delete_org_without_associated_users(self):
        """
        Test deletion of organization with no users linked with it.
        """
        # create org
        create_organization()
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_organization_view()

        # delete org
        self.delete_organization_from_list()

        # check org deleted
        with self.assertRaises(NoSuchElementException):
            settings.element_by_xpath('//*[@id="confirmed"]//tbody//tr[1]')

    def test_delete_org_with_associated_users(self):
        """
        Test deletion of organization with users linked with it.
        """
        # create org
        org = create_organization()
        volunteer = create_volunteer()

        volunteer.organization = org
        volunteer.save()

        # delete org
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_organization_view()
        self.delete_organization_from_list()

        # check org not deleted message received
        self.assertNotEqual(settings.get_danger_message(), None)
        self.assertEqual(
            settings.get_template_error_message(),
            'You cannot delete an organization that '
            'users are currently associated with.'
        )

    # Feature not yet added.
    '''
    def test_duplicate_event(self):
        """
        Test creation of duplicate event with same details.
        """
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        self.settings.go_to_events_page()
        settings = self.settings
        # Check event created
        self.assertEqual(
            self.driver.current_url,
            self.live_server_url + settings.event_list_page
            )
        self.assertEqual(settings.get_event_name(), 'event-name')

        settings.go_to_create_event_page()
        settings.fill_event_form(event)

        # TBA here - more checks depending on behaviour that should be reflected
        self.assertNotEqual(
            self.driver.current_url,
            self.live_server_url + settings.event_list_page
        )

    # Feature not yet implemented
    def test_duplicate_job(self):
        """
        Test creation of duplicate job with same details.
        """
        # register event first to create job
        event = {
            'name': 'event-name',
            'start_date': '2050-08-21',
            'end_date': '2050-09-28',
            'address': 'event-address',
            'venue': 'event-venue',
            'description': 'event-description'
        }
        created_event = create_event_with_details(event)

        # create job
        job = {
            'name': 'job',
            'start_date': '2050-08-21',
            'end_date': '2050-08-30',
            'description': 'job-description',
            'event': created_event
        }
        create_job_with_details(job)

        settings = self.settings

        # check job created
        settings.navigate_to_job_list_view(self.live_server_url)
        self.assertEqual(settings.get_job_name(), 'job name')
        self.assertEqual(settings.get_job_event(), 'event-name')

        # Create another job with same details within the same event
        settings.go_to_create_job_page()
        settings.fill_job_form(job)

        # TBA here - more checks depending on logic that should be reflected
        # check job not created - commented out due to bug
        self.assertNotEqual(
            self.driver.current_url,
            self.live_server_url + settings.job_list_page
        )
    '''
