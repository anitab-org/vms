# third party
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.eventsPage import EventsPage
from shift.utils import (create_admin, create_event_with_details)


class EventDetails(LiveServerTestCase):
    """
    Contains tests for event app from administrator view:
    - Event details view
    - Event creation with valid and invalid values
    - Event deletion
    - Start date of event after end date
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
        cls.event_details_page = EventsPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(EventDetails, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """
        Class method to quit the Firefox WebDriver session after
        execution of all tests in class.
        """
        cls.driver.quit()
        super(EventDetails, cls).tearDownClass()

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

    @staticmethod
    def register_valid_event():
        """
        Utility function to create a valid event.
        :return: Event type object
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

    def check_error_messages(self):
        """
        Utility function to check event errors raised after form filling
        """
        event_details_page = self.event_details_page
        self.assertEqual(len(event_details_page.get_help_blocks()), 3)
        self.assertEqual(
            event_details_page.get_event_name_error(),
            event_details_page.FIELD_REQUIRED
        )
        self.assertEqual(
            event_details_page.get_event_start_date_error(),
            event_details_page.FIELD_REQUIRED
        )
        self.assertEqual(
            event_details_page.get_event_end_date_error(),
            event_details_page.FIELD_REQUIRED
        )

    def login_admin(self):
        """
        Utility function to login as administrator with correct credentials.
        """
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.login(
            {
                'username': 'admin',
                'password': 'admin'
            }
        )

    def test_event_details_view(self):
        """
         Test event details view for existing events.
        """
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
        self.assertEqual(
            event_details_page.get_event_name(),
            created_event.name
        )
        self.assertEqual(
            event_details_page.get_event_start_date(),
            'June 11, 2050'
        )
        self.assertEqual(
            event_details_page.get_event_end_date(),
            'June 19, 2050'
        )

    def test_event_detail_page(self):
        # Navigate to event view
        created_event = create_event_with_details({
            'name': 'event',
            'start_date': '2050-06-11',
            'end_date': '2050-06-19',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        })
        event_details_page = self.event_details_page
        event_details_page.live_server_url = self.live_server_url
        event_details_page.go_to_events_page()

        event_details_page.go_to_details_event_page()
        self.assertEqual(
            event_details_page.get_event_name(),
            created_event.name
        )
        self.assertEqual(
            event_details_page.get_event_start_date(),
            'June 11, 2050'
        )
        self.assertEqual(
            event_details_page.get_event_end_date(),
            'June 19, 2050'
        )
        self.assertEqual(
            event_details_page.get_event_description(),
            'event-description'
        )

    def test_valid_event_create(self):
        """
        Test event create with valid details.
        """
        created_event = EventDetails.register_valid_event()

        event_details_page = self.event_details_page
        event_details_page.live_server_url = self.live_server_url
        event_details_page.go_to_events_page()

        # Check event creation
        self.assertEqual(
            event_details_page.get_event_name(),
            created_event.name
        )
        self.assertEqual(
            event_details_page.get_event_start_date(),
            'June 11, 2050'
        )
        self.assertEqual(
            event_details_page.get_event_end_date(),
            'June 19, 2050'
        )

    def test_invalid_event_create(self):
        """
        Test event create with invalid values.
        """
        event_details_page = self.event_details_page
        event_details_page.live_server_url = self.live_server_url
        event_details_page.go_to_events_page()

        # Create empty job
        event = {
            'name': '',
            'start_date': '',
            'end_date': '',
            'description': '',
            'address': '',
            'venue': ''
        }
        event_details_page.go_to_create_event_page()
        event_details_page.fill_event_form(event)

        # Check error messages
        self.check_error_messages()

    def test_invalid_event_edit(self):
        """
        Test event edit with invalid values.
        """
        registered_event = EventDetails.register_valid_event()
        event_details_page = self.event_details_page
        event_details_page.live_server_url = self.live_server_url
        event_details_page.go_to_events_page()

        event_details_page.go_to_edit_event_page()

        null_valued_event = {
            'name': '',
            'start_date': '',
            'end_date': '',
            'description': '',
            'address': '',
            'venue': ''
        }
        event_details_page.fill_event_form(null_valued_event)
        self.check_error_messages()

    def test_valid_event_edit(self):
        """
        Test event edit with valid values.
        """
        registered_event = EventDetails.register_valid_event()
        event_details_page = self.event_details_page
        event_details_page.live_server_url = self.live_server_url
        event_details_page.go_to_events_page()

        edit_event = {
            'name': 'newevent',
            'start_date': '2050-06-12',
            'end_date': '2050-06-20',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        event_details_page.go_to_edit_event_page()
        event_details_page.fill_event_form(edit_event)
        event_details_page.navigate_to_event_list_view()

        self.assertEqual(
            event_details_page.get_event_name(),
            edit_event['name']
        )
        self.assertEqual(
            event_details_page.get_event_start_date(),
            'June 12, 2050'
        )
        self.assertEqual(
            event_details_page.get_event_end_date(),
            'June 20, 2050'
        )

    def test_event_delete(self):
        """
        Test event delete.
        """
        registered_event = EventDetails.register_valid_event()
        event_details_page = self.event_details_page
        event_details_page.live_server_url = self.live_server_url
        event_details_page.go_to_events_page()

        self.assertEqual(
            event_details_page.get_delete_event_element('').text,
            'Delete'
        )
        event_details_page.get_delete_event_element('//a').click()
        self.assertEqual(
            event_details_page.get_deletion_context(),
            'Delete Event'
        )
        event_details_page.submit_form()

    def test_start_date_after_end_date(self):
        """
        Test event start date after its end date.
        """
        event_details_page = self.event_details_page
        event_details_page.live_server_url = self.live_server_url
        event_details_page.go_to_events_page()
        event_details_page.go_to_create_event_page()

        event_start_after_end = {
            'name': 'event name',
            'start_date': '2050-06-17',
            'end_date': '2050-06-16',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        event_details_page.fill_event_form(event_start_after_end)

        # Check error.
        self.assertEqual(event_details_page.get_event_start_date_error(),
                         event_details_page.START_BEFORE_END)
