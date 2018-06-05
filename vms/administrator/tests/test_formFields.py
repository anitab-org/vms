# third party
from selenium import webdriver

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.eventsPage import EventsPage
from shift.utils import (create_admin, create_event_with_details,
                         create_job_with_details, create_shift_with_details,
                         register_job_utility)


class FormFields(LiveServerTestCase):
    """
    Contains Tests for
    - checking if value in forms are saved for event, shift
    and job forms
    - validation of number of volunteers field
    """

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.settings = EventsPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(FormFields, cls).setUpClass()

    def setUp(self):
        create_admin()
        self.login_admin()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(FormFields, cls).tearDownClass()

    def check_event_form_values(self, event):
        settings = self.settings
        self.assertEqual(settings.get_event_name_value(), event[0])
        self.assertEqual(settings.get_event_start_date_value(), event[1])
        self.assertEqual(settings.get_event_end_date_value(), event[2])

    def check_job_form_values(self, job):
        settings = self.settings
        self.assertEqual(settings.get_job_name_value(), job[1])
        self.assertEqual(settings.get_job_description_value(), job[2])
        self.assertEqual(settings.get_job_start_date_value(), job[3])
        self.assertEqual(settings.get_job_end_date_value(), job[4])

    def check_shift_form_values(self, shift):
        settings = self.settings
        self.assertEqual(settings.get_shift_date_value(), shift[0])
        self.assertEqual(settings.get_shift_start_time_value(), shift[1])
        self.assertEqual(settings.get_shift_end_time_value(), shift[2])
        self.assertEqual(settings.get_shift_max_volunteers(), shift[3])

    def login_admin(self):
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({
            'username': 'admin',
            'password': 'admin'
        })

    def test_null_values_in_create_event(self):
        self.settings.go_to_events_page()
        event = ['', '', '']
        settings = self.settings
        settings.go_to_create_event_page()
        settings.fill_event_form(event)

        # Checks:
        # Event was not created
        # Error messages appear
        self.assertEqual(settings.remove_i18n(self.driver.current_url),
                         self.live_server_url + settings.create_event_page)
        self.assertEqual(len(settings.get_help_blocks()), 3)
        self.assertEqual(settings.get_event_name_error(), 'This field is required.')
        self.assertEqual(settings.get_event_start_date_error(), 'This field is required.')
        self.assertEqual(settings.get_event_end_date_error(), 'This field is required.')

    def test_null_values_in_edit_event(self):
        event = ['event-name', '2018-05-24', '2018-05-28']
        created_event = create_event_with_details(event)
        self.settings.go_to_events_page()

        settings = self.settings

        # Check we are having correct event
        self.assertEqual(settings.get_event_name(), created_event.name)
        settings.go_to_edit_event_page()

        edited_event = ['', '', '']
        settings.fill_event_form(edited_event)

        # Checks:
        # Event not edited
        # Error messages appear
        self.assertNotEqual(self.driver.current_url, self.live_server_url + settings.event_list_page)
        self.assertEqual(len(settings.get_help_blocks()), 3)
        self.assertEqual(settings.get_event_name_error(), 'This field is required.')
        self.assertEqual(settings.get_event_start_date_error(), 'This field is required.')
        self.assertEqual(settings.get_event_end_date_error(), 'This field is required.')

    def test_null_values_in_create_job(self):
        # Register Event
        event = ['event-name', '2050-05-24', '2050-05-28']
        created_event = create_event_with_details(event)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # Create Job of null values
        job = [created_event.id, '', '', '', '']
        settings.navigate_to_job_list_view()
        settings.go_to_create_job_page()
        settings.fill_job_form(job)

        # Checks:
        # Job not created
        # Error messages appear
        self.assertEqual(settings.remove_i18n(self.driver.current_url), self.live_server_url + settings.create_job_page)
        self.assertEqual(len(settings.get_help_blocks()), 3)

        self.assertEqual(settings.get_job_name_error(), 'This field is required.')
        self.assertEqual(settings.get_job_start_date_error(), 'This field is required.')
        self.assertEqual(settings.get_job_end_date_error(), 'This field is required.')

    def test_null_values_in_edit_job(self):
        # Register Event
        event = ['event-name', '2050-05-24', '2050-05-28']
        created_event = create_event_with_details(event)
        self.settings.go_to_events_page()
        settings = self.settings

        # Create Job with not-null values
        job = ['job', '2050-05-24', '2050-05-28', '', created_event]
        create_job_with_details(job)

        # Go to Edit job page
        settings.live_server_url = self.live_server_url
        settings.navigate_to_job_list_view()
        settings.go_to_edit_job_page()

        # Edit job with null values
        settings.fill_job_form([created_event.id, '', '', '', ''])

        # Checks:
        # Job not edited
        # Error messages appear
        self.assertNotEqual(self.driver.current_url, self.live_server_url + settings.job_list_page)
        self.assertEqual(len(settings.get_help_blocks()), 3)
        self.assertEqual(settings.get_job_name_error(), 'This field is required.')
        self.assertEqual(settings.get_job_start_date_error(), 'This field is required.')
        self.assertEqual(settings.get_job_end_date_error(), 'This field is required.')

    def test_null_values_in_create_shift(self):
        # Register Event
        event = ['event-name', '2050-05-24', '2050-05-28']
        created_event = create_event_with_details(event)
        self.settings.go_to_events_page()
        settings = self.settings

        # Create Job with not-null values
        job = ['job', '2050-05-24', '2050-05-28', '', created_event]
        create_job_with_details(job)

        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        # Create Shift
        shift = ['', '', '', '']
        settings.fill_shift_form(shift)

        # Checks:
        # Shift not created
        # Error messages appear
        self.assertEqual(len(settings.get_help_blocks()), 4)

        self.assertEqual(settings.get_shift_date_error(), 'This field is required.')
        self.assertEqual(settings.get_shift_start_time_error(), 'This field is required.')
        self.assertEqual(settings.get_shift_end_time_error(), 'This field is required.')
        self.assertEqual(settings.get_shift_max_volunteer_error(), 'This field is required.')

    def test_null_values_in_edit_shift(self):
        # Register Event
        event = ['event-name', '2050-05-24', '2050-05-28']
        created_event = create_event_with_details(event)
        self.settings.go_to_events_page()
        settings = self.settings

        # Create Job with not-null values
        job = ['job', '2050-05-24', '2050-05-28', '', created_event]
        created_job = create_job_with_details(job)

        # Create Shift with not-null values
        shift = ['2050-05-24', '09:00', '12:00', '10', created_job]
        create_shift_with_details(shift)

        settings.live_server_url = self.live_server_url
        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()

        # edit shift with null values
        shift = ['', '', '', '']
        settings.fill_shift_form(shift)

        # verify that shift was not edited and error messages appear as
        # expected
        self.assertEqual(len(settings.get_help_blocks()), 4)

        self.assertEqual(settings.get_shift_date_error(), 'This field is required.')
        self.assertEqual(settings.get_shift_start_time_error(), 'This field is required.')
        self.assertEqual(settings.get_shift_end_time_error(), 'This field is required.')
        self.assertEqual(settings.get_shift_max_volunteer_error(), 'This field is required.')

    def test_max_volunteer_field(self):
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        event = ['event-name', '2050-05-24', '2050-05-28']
        created_event = create_event_with_details(event)
        job = ['job', '2050-05-24', '2050-05-28', '', created_event]
        created_job = create_job_with_details(job)

        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        invalid_shift = ['01/01/2018', '12:00', '11:00', '0']
        settings.fill_shift_form(invalid_shift)

        # Check error message
        self.assertEqual(settings.get_shift_max_volunteer_error(), 'Ensure this value is greater than or equal to 1.')

        # Create shift and edit with 0 value
        shift = ['2050-05-24', '09:00', '12:00', '10', created_job]
        create_shift_with_details(shift)

        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()
        settings.fill_shift_form(invalid_shift)

        # Check error message
        self.assertEqual(settings.get_shift_max_volunteer_error(), 'Ensure this value is greater than or equal to 1.')

    def test_simplify_shift(self):
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        event = ['event-name', '2050-05-24', '2050-05-28']
        created_event = create_event_with_details(event)
        job = ['job', '2050-05-24', '2050-05-28', '', created_event]
        created_job = create_job_with_details(job)

        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        # Check correctness of Job name and date.
        self.assertEqual(settings.get_shift_job(), 'job')
        self.assertEqual(settings.get_shift_job_start_date(), 'May 24, 2050')
        self.assertEqual(settings.get_shift_job_end_date(), 'May 28, 2050')

        # Create shift and check job details in edit form
        shift = ['2050-05-28', '09:00', '12:00', '10', created_job]
        create_shift_with_details(shift)
        settings.navigate_to_shift_list_view()
        settings.go_to_edit_shift_page()

        # Check correctness of Job name and date.
        self.assertEqual(settings.get_shift_job(), 'job')
        self.assertEqual(settings.get_shift_job_start_date(), 'May 24, 2050')
        self.assertEqual(settings.get_shift_job_end_date(), 'May 28, 2050')

    def test_simplify_job(self):
        event = ['event', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        # Create job and check event details in edit form
        job = ['job', '2050-08-24', '2050-08-28', '', created_event]
        create_job_with_details(job)

        settings.navigate_to_job_list_view()
        settings.go_to_edit_job_page()
        element = self.driver.find_element_by_xpath('//div[2]//div[3]//div[1]//div[1]//option[1]')
        # verify that the correct event name and date are displayed
        self.assertEqual(element.text, 'event')
        self.assertEqual(element.get_attribute('start_date'), 'Aug. 21, 2050')
        self.assertEqual(element.get_attribute('end_date'), 'Sept. 28, 2050')

    """
    # Retention tests are buggy.
    # The results change every time a new build starts
    # i.e. The values in forms are not always retained.

    def test_field_value_retention_for_event(self):
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url
        settings.get_page(settings.live_server_url, PageUrls.event_list_page)
        settings.go_to_create_event_page()

        # Fill invalid Event
        invalid_event = ['event-name!@', '05/24/2016', '05/28/2050']
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
        event = ['event-name', '2050-05-24', '2050-05-28']
        create_event_with_details(event)
        settings.navigate_to_event_list_view()
        settings.go_to_edit_event_page()
        settings.fill_event_form(invalid_event)

        # Bug here: Invalid fields are erased from edit forms
        # Erasing the invalid field from event because invalid fields are
        # erased in form if we try to edit.
        invalid_event[1] = ''
        self.assertNotEqual(self.driver.current_url, self.live_server_url + settings.create_event_page)

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
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        event = ['event-name', '2050-08-21', '2050-09-28']
        created_event = create_event_with_details(event)

        settings.navigate_to_job_list_view()
        # Fill invalid Job
        invalid_job = [created_event.id, 'job name#$', 'job description', '24/05/2016', '22/08/2050']
        settings.go_to_create_job_page()
        settings.fill_job_form(invalid_job)

        # Checks:
        # Job not created
        # Field values are not erased
        self.assertEqual(settings.remove_i18n(self.driver.current_url), self.live_server_url + settings.create_job_page)

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
        job = ['job', '2050-08-25', '2050-08-25', '', created_event]
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
        self.assertNotEqual(self.driver.current_url, self.live_server_url + settings.job_list_page)

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
        self.settings.go_to_events_page()
        settings = self.settings
        settings.live_server_url = self.live_server_url

        event = ['event-name', '2050-05-24', '2050-05-28']
        created_event = create_event_with_details(event)
        job = ['job', '2050-05-24', '2050-05-28', '', created_event]
        created_job = create_job_with_details(job)

        settings.navigate_to_shift_list_view()
        settings.go_to_create_shift_page()

        invalid_shift = ['01/01/2016', '12:00', '11:00', '10']
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
        invalid_shift = ['01/01/2016', '12:00', '11:00', '10']
        shift = ['2050-05-24', '09:00', '12:00', '10', created_job]
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
    """
