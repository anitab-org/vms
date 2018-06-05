# third party
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from pom.pages.eventsPage import EventsPage
from pom.pages.authenticationPage import AuthenticationPage
from pom.locators.eventsPageLocators import EventsPageLocators
from shift.utils import (
    create_admin, create_event_with_details, create_job_with_details,
    create_shift_with_details, create_volunteer,
    register_volunteer_for_shift_utility, create_organization)


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
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.settings = EventsPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        cls.elements = EventsPageLocators()
        super(Settings, cls).setUpClass()

    def setUp(self):
        create_admin()
        self.login_admin()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(Settings, cls).tearDownClass()

    def login_admin(self):
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({
            'username': 'admin',
            'password': 'admin'
        })

    def delete_event_from_list(self):
        settings = self.settings
        self.assertEqual(settings.element_by_xpath(self.elements.DELETE_EVENT).text, 'Delete')
        settings.element_by_xpath(self.elements.DELETE_EVENT + '//a').click()
        self.assertNotEqual(settings.get_deletion_box(), None)
        self.assertEqual(settings.get_deletion_context(), 'Delete Event')
        settings.submit_form()

    def delete_job_from_list(self):
        settings = self.settings
        self.assertEqual(settings.element_by_xpath(self.elements.DELETE_JOB).text, 'Delete')
        settings.element_by_xpath(self.elements.DELETE_JOB + '//a').click()

        self.assertNotEqual(settings.get_deletion_box(), None)
        self.assertEqual(settings.get_deletion_context(), 'Delete Job')
        settings.submit_form()

    def delete_shift_from_list(self):
        settings = self.settings
        self.assertEqual(settings.element_by_xpath(self.elements.DELETE_SHIFT).text, 'Delete')
        settings.element_by_xpath(self.elements.DELETE_SHIFT + '//a').click()

        # confirm on delete
        self.assertNotEqual(settings.get_deletion_box(), None)
        self.assertEqual(settings.get_deletion_context(), 'Delete Shift')
        settings.submit_form()

    def delete_organization_from_list(self):
        settings = self.settings
        self.assertEqual(settings.element_by_xpath(self.elements.DELETE_ORG).text, 'Delete')
        settings.element_by_xpath(self.elements.DELETE_ORG + '//a').click()

        # confirm on delete
        self.assertNotEqual(settings.get_deletion_box(), None)
        self.assertEqual(settings.get_deletion_context(), 'Delete Organization')
        settings.submit_form()

    def test_event_tab(self):
        self.settings.go_to_events_page()
        settings = self.settings

        self.assertEqual(settings.get_message_context(), 'There are currently no events. Please create events first.')

    def test_job_tab_and_create_job_without_event(self):
        self.settings.go_to_events_page()
        settings = self.settings
        settings.click_link(settings.jobs_tab)
        self.assertEqual(settings.remove_i18n(self.driver.current_url), self.live_server_url + settings.job_list_page)
        self.assertEqual(settings.get_message_context(), 'There are currently no jobs. Please create jobs first.')

        settings.click_link('Create Job')
        self.assertEqual(settings.remove_i18n(self.driver.current_url), self.live_server_url + settings.create_job_page)
        self.assertEqual(settings.get_message_context(), 'Please add events to associate with jobs first.')

    def test_shift_tab_and_create_shift_without_job(self):
        self.settings.go_to_events_page()
        settings = self.settings
        settings.click_link(settings.shift_tab)
        self.assertEqual(settings.remove_i18n(self.driver.current_url), self.live_server_url + settings.shift_list_page)
        self.assertEqual(settings.get_message_context(), 'There are currently no jobs. Please create jobs first.')

    def test_create_event(self):
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        event = ['event-name', '2050-08-21', '2050-09-28']
        settings.go_to_create_event_page()
        settings.fill_event_form(event)
        settings.navigate_to_event_list_view()

        # Check event created
        self.assertEqual(settings.remove_i18n(self.driver.current_url), self.live_server_url + settings.event_list_page)
        self.assertEqual(settings.get_event_name(), 'event-name')

    def test_edit_event(self):
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # Create event
        settings.navigate_to_event_list_view()
        self.assertEqual(settings.get_event_name(), created_event.name)

        settings.go_to_edit_event_page()
        edited_event = ['new-event-name', '2050-09-21', '2050-09-28']
        settings.fill_event_form(edited_event)
        settings.navigate_to_event_list_view()

        # Check event edit
        self.assertEqual(settings.remove_i18n(self.driver.current_url), self.live_server_url + settings.event_list_page)
        self.assertEqual(settings.get_event_name(), 'new-event-name')

    def test_create_and_edit_event_with_invalid_start_date(self):
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.go_to_create_event_page()
        invalid_event = ['event-name-invalid', '05/17/2016', '09/28/2016']
        settings.fill_event_form(invalid_event)

        # Check event not created and error message displayed
        self.assertNotEqual(self.driver.current_url, self.live_server_url + settings.event_list_page)
        self.assertEqual(settings.get_warning_context(), "Start date should be today's date or later.")

        settings.navigate_to_event_list_view()
        settings.go_to_create_event_page()
        valid_event = ['event-name', '2050-05-21', '2050-09-28']
        valid_event_created = create_event_with_details(valid_event)

        settings.navigate_to_event_list_view()
        self.assertEqual(settings.get_event_name(), valid_event_created.name)

        settings.go_to_edit_event_page()
        settings.fill_event_form(invalid_event)

        # check event not edited and error message displayed
        self.assertNotEqual(self.driver.current_url, self.live_server_url + settings.event_list_page)
        self.assertEqual(settings.get_warning_context(), "Start date should be today's date or later.")

    def test_edit_event_with_elapsed_start_date(self):
        elapsed_event = ['event-name', '2016-05-21', '2050-08-09']

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
        settings.send_value_to_xpath(self.elements.CREATE_EVENT_NAME, 'changed-event-name')
        settings.submit_form()

        # check event not edited
        self.assertNotEqual(self.driver.current_url, self.live_server_url + settings.event_list_page)

    def test_edit_event_with_invalid_job_date(self):
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        # Create Job
        job = ['job', '2050-08-21', '2050-08-21', '', created_event]
        create_job_with_details(job)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_event_list_view()

        self.assertEqual(settings.get_event_name(), created_event.name)
        settings.go_to_edit_event_page()

        # Edit event such that job is no longer in the new date range
        new_event = ['new-event-name', '2017-08-30', '2017-09-21']
        settings.fill_event_form(new_event)

        # check event not edited and error message displayed
        self.assertNotEqual(self.driver.current_url, self.live_server_url + settings.event_list_page)
        self.assertEqual(settings.element_by_xpath(self.elements.TEMPLATE_ERROR_MESSAGE).text,
                         'You cannot edit this event as the following associated job no longer '
                         'lies within the new date range :')

    def test_delete_event_with_no_associated_job(self):
        event = ['event-name', '2050-08-21', '2050-09-28']
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
        self.assertEqual(settings.remove_i18n(self.driver.current_url), self.live_server_url + settings.event_list_page)
        with self.assertRaises(NoSuchElementException):
            settings.get_results()

    def test_delete_event_with_associated_job(self):
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2050-08-21', '2050-08-21', '', created_event]
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
        self.assertEqual(settings.get_template_error_message(),
                         'You cannot delete an event that a job is currently associated with.')

        # check event NOT deleted
        settings.navigate_to_event_list_view()
        self.assertEqual(settings.get_event_name(), 'event-name')

    def test_create_job(self):
        # register event first to create job
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # create job
        job = ['event-name', 'job name', 'job description', '2050-08-21', '2050-08-28']
        settings.navigate_to_job_list_view()
        settings.go_to_create_job_page()
        settings.fill_job_form(job)

        # check job created
        settings.navigate_to_job_list_view()
        self.assertEqual(settings.get_job_name(), 'job name')
        self.assertEqual(settings.get_job_event(), created_event.name)

    def test_edit_job(self):
        # register event first to create job
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2050-08-21', '2050-08-21', '', created_event]
        create_job_with_details(job)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        edit_job = ['event-name', 'changed job name', 'job description', '2050-08-25', '2050-08-25']
        settings.navigate_to_job_list_view()
        settings.go_to_edit_job_page()
        settings.fill_job_form(edit_job)

        settings.navigate_to_job_list_view()
        # check job edited
        self.assertEqual(settings.remove_i18n(self.driver.current_url), self.live_server_url + settings.job_list_page)
        self.assertEqual(settings.get_job_name(), 'changed job name')

    def test_create_job_with_invalid_event_date(self):
        # register event first to create job
        event = ['event-name', '2050-08-21', '2050-09-28']
        create_event_with_details(event)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # create job with start date outside range
        job = ['event-name', 'job name', 'job description', '08/10/2050', '09/11/2050']
        settings.navigate_to_job_list_view()
        settings.go_to_create_job_page()
        settings.fill_job_form(job)

        # check job not created and proper error message displayed
        self.assertNotEqual(self.driver.current_url, self.live_server_url + settings.job_list_page)
        self.assertEqual(settings.get_warning_context(), 'Job dates should lie within Event dates')

        # create job with end date outside range
        job = ['event-name', 'job name', 'job description', '08/30/2050', '09/29/2050']
        settings.navigate_to_job_list_view()
        settings.go_to_create_job_page()
        settings.fill_job_form(job)

        # check job not created and proper error message displayed
        self.assertNotEqual(self.driver.current_url, self.live_server_url + settings.job_list_page)
        self.assertEqual(settings.get_warning_context(), 'Job dates should lie within Event dates')

    def test_edit_job_with_invalid_event_date(self):
        # register event first to create job
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2050-08-21', '2050-08-21', '', created_event]
        create_job_with_details(job)

        invalid_job_one = ['event-name', 'changed job name', 'job description', '2050-05-03', '2050-11-09']

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # edit job with start date outside event start date
        settings.navigate_to_job_list_view()
        settings.go_to_edit_job_page()
        settings.fill_job_form(invalid_job_one)

        # check job not edited and proper error message displayed
        self.assertNotEqual(self.driver.current_url, self.live_server_url + settings.job_list_page)
        self.assertEqual(settings.get_warning_context(), 'Job dates should lie within Event dates')

        invalid_job_two = ['event-name', 'changed job name', 'job description', '2050-09-14', '2050-12-31']
        settings.navigate_to_job_list_view()
        settings.go_to_edit_job_page()
        settings.fill_job_form(invalid_job_two)

        # check job not edited and proper error message displayed
        self.assertNotEqual(self.driver.current_url, self.live_server_url + settings.job_list_page)
        self.assertEqual(settings.get_warning_context(), 'Job dates should lie within Event dates')

    def test_edit_job_with_invalid_shift_date(self):
        # register event first to create job
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2050-08-21', '2050-08-21', '', created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2050-08-21', '09:00', '12:00', '10', created_job]
        create_shift_with_details(shift)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_job_list_view()

        invalid_job_one = ['event-name', 'changed job name', 'job description', '2050-09-01', '2050-09-11']

        # edit job with date range such that the shift start date no longer
        # falls in the range
        settings.go_to_edit_job_page()
        settings.fill_job_form(invalid_job_one)

        # check job not edited and proper error message displayed
        self.assertNotEqual(self.driver.current_url, self.live_server_url + settings.job_list_page)
        self.assertEqual(settings.get_template_error_message(),
                         'You cannot edit this job as 1 associated shift no longer lies within the new date range')

    def test_delete_job_without_associated_shift(self):
        # register event first to create job
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2050-08-21', '2050-08-21', '', created_event]
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
        self.assertEqual(settings.remove_i18n(self.driver.current_url), self.live_server_url + settings.job_list_page)
        with self.assertRaises(NoSuchElementException):
            settings.get_results()

    def test_delete_job_with_associated_shifts(self):
        # register event first to create job
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2050-08-21', '2050-08-21', '', created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2050-08-21', '09:00', '12:00', '10', created_job]
        create_shift_with_details(shift)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # delete job
        settings.navigate_to_job_list_view()
        self.delete_job_from_list()

        self.assertNotEqual(settings.get_danger_message(), None)
        self.assertEqual(settings.get_template_error_message(),
                         'You cannot delete a job that a shift is currently associated with.')

        # check job NOT deleted
        settings.navigate_to_job_list_view()
        self.assertEqual(settings.get_job_name(), 'job')

    def test_create_shift(self):
        # register event first to create job
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2050-08-21', '2050-08-30', '', created_event]
        create_job_with_details(job)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # create shift
        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        shift = ['08/30/2050', '09:00', '12:00', '10']
        settings.fill_shift_form(shift)

        # verify that shift was created
        self.assertNotEqual(settings.get_results(), None)
        with self.assertRaises(NoSuchElementException):
            settings.get_help_block()

    def test_create_shift_with_invalid_timings(self):
        # register event first to create job
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # create job
        job = ['job', '2050-08-21', '2050-08-30', '', created_event]
        create_job_with_details(job)

        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        # create shift where end hours is less than start hours
        shift = ['08/30/2050', '14:00', '12:00', '5']
        settings.fill_shift_form(shift)

        # verify that shift was not created and error message displayed
        self.assertEqual(settings.get_warning_context(), 'Shift end time should be greater than start time')

    def test_edit_shift_with_invalid_timings(self):
        # register event first to create job
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2050-08-21', '2050-08-30', '', created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2050-08-21', '09:00', '12:00', '10', created_job]
        create_shift_with_details(shift)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()

        # edit shift with end hours less than start hours
        invalid_shift = ['08/30/2050', '18:00', '13:00', '5']
        settings.fill_shift_form(invalid_shift)

        # verify that shift was not edited and error message displayed
        self.assertEqual(settings.get_warning_context(), 'Shift end time should be greater than start time')

    def test_create_shift_with_invalid_date(self):
        # register event first to create job
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2050-08-21', '2017-08-30', '', created_event]
        create_job_with_details(job)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # create shift
        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        shift = ['06/30/2050', '14:00', '18:00', '5']
        settings.fill_shift_form(shift)

        # verify that shift was not created and error message displayed
        self.assertEqual(settings.get_warning_context(), 'Shift date should lie within Job dates')

    def test_edit_shift_with_invalid_date(self):
        # register event first to create job
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2050-08-21', '2050-08-30', '', created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2050-08-21', '09:00', '12:00', '10', created_job]
        create_shift_with_details(shift)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()

        # edit shift with date not between job dates
        invalid_shift = ['02/05/2050', '04:00', '13:00', '2']
        settings.fill_shift_form(invalid_shift)

        # verify that shift was not edited and error message displayed
        self.assertEqual(settings.get_warning_context(), 'Shift date should lie within Job dates')

    def test_edit_shift(self):
        # register event first to create job
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2050-08-21', '2050-08-30', '', created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2050-08-21', '09:00', '12:00', '10', created_job]
        create_shift_with_details(shift)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()

        # edit shift with date between job dates
        shift = ['08/25/2050', '10:00', '13:00', '2']
        settings.fill_shift_form(shift)

        with self.assertRaises(NoSuchElementException):
            settings.get_help_block()

        self.assertEqual(settings.get_shift_date(), 'Aug. 25, 2050')

    def test_delete_shift(self):
        # register event first to create job
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2050-08-21', '2050-08-30', '', created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2050-08-21', '09:00', '12:00', '10', created_job]
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
        self.assertEqual(settings.get_message_context(), 'There are currently no shifts. Please create shifts first.')

    def test_delete_shift_with_volunteer(self):
        # register event first to create job
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2050-08-21', '2050-08-30', '', created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2050-08-21', '09:00', '12:00', '10', created_job]
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
        self.assertEqual(settings.get_template_error_message(),
                         'You cannot delete a shift that a volunteer has signed up for.')

    def test_organization(self):
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.click_link(settings.organization_tab)
        self.assertEqual(settings.remove_i18n(self.driver.current_url),
                         self.live_server_url + settings.organization_list_page)

        settings.click_link('Create Organization')
        self.assertEqual(settings.remove_i18n(self.driver.current_url),
                         self.live_server_url + settings.create_organization_page)

        # Test all valid characters for organization
        # [(A-Z)|(a-z)|(0-9)|(\s)|(\-)|(:)]
        settings.fill_organization_form('Org-name 92:4 CA')
        self.assertEqual(settings.get_org_name(), 'Org-name 92:4 CA')

    def test_replication_of_organization(self):
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

        self.assertEqual(settings.get_help_block().text, 'Organization with this Name already exists.')

    def test_edit_org(self):
        # create org
        create_organization()
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.navigate_to_organization_view()

        # edit org
        self.assertEqual(settings.element_by_xpath(self.elements.EDIT_ORG).text, 'Edit')
        settings.element_by_xpath(self.elements.EDIT_ORG + '//a').click()

        settings.fill_organization_form('changed-organization')

        # check edited org
        org_list = list()
        org_list.append(settings.get_org_name())

        self.assertTrue('changed-organization' in org_list)

    def test_delete_org_without_associated_users(self):
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
            settings.element_by_xpath('//table//tbody//tr[1]')

    def test_delete_org_with_associated_users(self):
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
        self.assertEqual(settings.get_template_error_message(),
                         'You cannot delete an organization that users are currently associated with.')

    # Feature not yet added.
    """
    def test_duplicate_event(self):
        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        self.settings.go_to_events_page()
        settings = self.settings
        # Check event created
        self.assertEqual(self.driver.current_url, self.live_server_url + settings.event_list_page)
        self.assertEqual(settings.get_event_name(), 'event-name')

        settings.go_to_create_event_page()
        settings.fill_event_form(event)

        # TBA here - more checks depending on behaviour that should be reflected
        self.assertNotEqual(self.driver.current_url, self.live_server_url + settings.event_list_page)

    # Feature not yet implemented
    def test_duplicate_job(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['event-name', 'job name', 'job description', '2017-08-21', '2017-08-28']
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
        self.assertNotEqual(self.driver.current_url, self.live_server_url + settings.job_list_page)
    """
