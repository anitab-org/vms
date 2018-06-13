# third party
from selenium import webdriver

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.eventsPage import EventsPage
from shift.utils import (create_admin, create_event_with_details)


class EventDetails(LiveServerTestCase):
    """
    Contains Tests for Job app in aspect of
    an admin's view of website.
    """

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.event_details_page = EventsPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(EventDetails, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(EventDetails, cls).tearDownClass()

    def setUp(self):
        create_admin()
        self.login_admin()

    def tearDown(self):
        self.authentication_page.logout()

    @staticmethod
    def register_valid_event():
        created_event = create_event_with_details(['event', '2050-06-11', '2050-06-19'])
        return created_event

    def check_error_messages(self):
        event_details_page = self.event_details_page
        self.assertEqual(len(event_details_page.get_help_blocks()), 3)
        self.assertEqual(event_details_page.get_event_name_error(), event_details_page.FIELD_REQUIRED)
        self.assertEqual(event_details_page.get_event_start_date_error(), event_details_page.FIELD_REQUIRED)
        self.assertEqual(event_details_page.get_event_end_date_error(), event_details_page.FIELD_REQUIRED)

    def login_admin(self):
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.login(
            {
                'username': 'admin',
                'password': 'admin'
            }
        )

    def test_event_details_view(self):
        # Navgate to event view
        event_details_page = self.event_details_page
        event_details_page.live_server_url = self.live_server_url
        event_details_page.go_to_events_page()

        self.assertEqual(event_details_page.get_message_context(),
                         event_details_page.NO_EVENT_PRESENT)

        # Create a valid event
        created_event = EventDetails.register_valid_event()

        # Verify Details
        event_details_page.navigate_to_event_list_view()
        self.assertEqual(event_details_page.get_event_name(), created_event.name)
        self.assertEqual(event_details_page.get_event_start_date(), 'June 11, 2050')
        self.assertEqual(event_details_page.get_event_end_date(), 'June 19, 2050')

    def test_valid_event_create(self):
        created_event = EventDetails.register_valid_event()

        event_details_page = self.event_details_page
        event_details_page.live_server_url = self.live_server_url
        event_details_page.go_to_events_page()

        # Check event creation
        self.assertEqual(event_details_page.get_event_name(), created_event.name)
        self.assertEqual(event_details_page.get_event_start_date(), 'June 11, 2050')
        self.assertEqual(event_details_page.get_event_end_date(), 'June 19, 2050')

    def test_invalid_event_create(self):
        event_details_page = self.event_details_page
        event_details_page.live_server_url = self.live_server_url
        event_details_page.go_to_events_page()

        # Create empty job
        event = ['', '', '']
        event_details_page.go_to_create_event_page()
        event_details_page.fill_event_form(event)

        # Check error messages
        self.check_error_messages()

    def test_invalid_event_edit(self):
        registered_event = EventDetails.register_valid_event()
        event_details_page = self.event_details_page
        event_details_page.live_server_url = self.live_server_url
        event_details_page.go_to_events_page()

        event_details_page.go_to_edit_event_page()

        null_valued_event = ['', '', '']
        event_details_page.fill_event_form(null_valued_event)
        self.check_error_messages()

    def test_valid_event_edit(self):
        registered_event = EventDetails.register_valid_event()
        event_details_page = self.event_details_page
        event_details_page.live_server_url = self.live_server_url
        event_details_page.go_to_events_page()

        edit_job = ['newevent', '2050-06-12', '2050-06-20']
        event_details_page.go_to_edit_event_page()
        event_details_page.fill_event_form(edit_job)
        event_details_page.navigate_to_event_list_view()

        self.assertEqual(event_details_page.get_event_name(), edit_job[0])
        self.assertEqual(event_details_page.get_event_start_date(), 'June 12, 2050')
        self.assertEqual(event_details_page.get_event_end_date(), 'June 20, 2050')

    def test_event_delete(self):
        registered_event = EventDetails.register_valid_event()
        event_details_page = self.event_details_page
        event_details_page.live_server_url = self.live_server_url
        event_details_page.go_to_events_page()

        self.assertEqual(event_details_page.get_delete_event_element('').text, 'Delete')
        event_details_page.get_delete_event_element('//a').click()
        self.assertEqual(event_details_page.get_deletion_context(), 'Delete Event')
        event_details_page.submit_form()

    def test_start_date_after_end_date(self):
        event_details_page = self.event_details_page
        event_details_page.live_server_url = self.live_server_url
        event_details_page.go_to_events_page()
        event_details_page.go_to_create_event_page()

        event_start_after_end = ['event name', '2050-06-17', '2050-06-16']
        event_details_page.fill_event_form(event_start_after_end)

        # Check error.
        self.assertEqual(event_details_page.get_event_start_date_error(),
                         event_details_page.START_BEFORE_END)
