# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# third party
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

# local Django
from job.models import Job
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.eventSignUpPage import EventSignUpPage
from shift.utils import (create_volunteer, create_organization_with_details,
                         create_second_country, create_second_state,
                         create_second_city, get_country_by_name,
                         get_state_by_name, get_city_by_name,
                         register_event_utility, register_job_utility,
                         register_shift_utility, create_shift_with_details,
                         create_volunteer_with_details,
                         register_volunteer_for_shift_utility)


class ShiftSignUp(LiveServerTestCase):
    """
    Contains tests for for event app from volunteer view:
    -
    -
    -
    -
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
        cls.sign_up_page = EventSignUpPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(ShiftSignUp, cls).setUpClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        create_volunteer()
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
        super(ShiftSignUp, cls).tearDownClass()

    def login_volunteer(self):
        """
        Utility function to login as volunteer with correct credentials.
        """
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({
            'username': 'volunteer',
            'password': 'volunteer'
        })

    def test_events_page_with_no_events(self):
        """
        Test event view with no registered events.
        """
        sign_up_page = self.sign_up_page
        sign_up_page.navigate_to_sign_up()
        self.assertEqual(
            sign_up_page.get_info_box().text,
            sign_up_page.no_event_message
        )

    def test_signup_shifts_with_registered_shifts(self):
        """
        Test volunteer signing for a shift which is registered.
        """
        registered_event = register_event_utility()
        registered_job = register_job_utility()
        registered_shift = register_shift_utility()

        sign_up_page = self.sign_up_page

        # Open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # On event page
        sign_up_page.click_to_view_jobs()

        # On jobs page
        sign_up_page.click_to_view_shifts()

        # On shifts page
        sign_up_page.click_to_sign_up()

        # Confirm shift assignment
        sign_up_page.submit_form()
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_danger_box()

        # check shift signed up
        self.assertEqual(
            sign_up_page.get_signed_up_shift_text(),
            'Upcoming Shifts'
        )
        self.assertEqual(sign_up_page.get_shift_job(), 'job')
        self.assertEqual(sign_up_page.get_shift_date(), 'June 15, 2050')
        self.assertEqual(sign_up_page.get_shift_start_time(), '9 a.m.')
        self.assertEqual(sign_up_page.get_shift_end_time(), '3 p.m.')

    def test_signup_for_same_shift_again(self):
        """
        Test volunteer signing up for the same shift again.
        """
        registered_event = register_event_utility()
        registered_job = register_job_utility()
        registered_shift = register_shift_utility()

        sign_up_page = self.sign_up_page
        # Open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # Events shown in table
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_info_box()
        sign_up_page.click_to_view_jobs()

        # On jobs page
        sign_up_page.click_to_view_shifts()

        # On shifts page, Sign up this shift !
        sign_up_page.click_to_sign_up()

        # Confirm on shift sign up
        sign_up_page.submit_form()
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_danger_box()

        # Sign up same shift again
        # Open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # Events page
        self.assertEqual(
            sign_up_page.get_info_box().text,
            sign_up_page.no_event_message
        )

        with self.assertRaises(NoSuchElementException):
            sign_up_page.find_table_tag()

    def test_empty_events(self):
        """
        Test no events present in the event view.
        """
        registered_event = register_event_utility()
        sign_up_page = self.sign_up_page
        # Open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # On event page
        self.assertEqual(
            sign_up_page.get_info_box().text,
            sign_up_page.no_event_message
        )

        with self.assertRaises(NoSuchElementException):
            sign_up_page.find_table_tag()
            sign_up_page.click_to_view_jobs()

        registered_job = register_job_utility()

        self.assertEqual(
            sign_up_page.get_info_box().text,
            sign_up_page.no_event_message
        )

        with self.assertRaises(NoSuchElementException):
            sign_up_page.find_table_tag()

    def test_shift_sign_up_with_outdated_shifts(self):
        """
        Test signing up for the shifts whose date have passed.
        """
        registered_event = register_event_utility()
        registered_job = register_job_utility()
        sign_up_page = self.sign_up_page

        # create outdated shift
        shift_1 = {
            'date': "2016-05-11",
            'start_time': "9:00",
            'end_time': "15:00",
            'max_volunteers': 6,
            'job': Job.objects.get(name='job'),
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        created_shift = create_shift_with_details(shift_1)

        # open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # on event page
        sign_up_page.click_to_view_jobs()

        # on jobs page
        sign_up_page.click_to_view_shifts()
        self.assertEqual(
            sign_up_page.get_info_box().text,
            sign_up_page.get_message_shift_not_available_for_job('job')
        )

    def test_shift_sign_up_with_no_slots(self):
        """
        Test signing up for a shift for which volunteer needed is zero.
        """
        registered_event = register_event_utility()
        registered_job = register_job_utility()

        sign_up_page = self.sign_up_page

        # create shift with no slot
        shift_2 = {
            'date': "2016-05-11",
            'start_time': "9:00",
            'end_time': "15:00",
            'max_volunteers': 1,
            'job': Job.objects.get(name='job'),
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        s2 = create_shift_with_details(shift_2)

        # Create another volunteer
        org_name = 'volunteer-organization'
        org_obj = create_organization_with_details(org_name)

        second_country = create_second_country()
        second_state = create_second_state()
        second_city = create_second_city()
        volunteer_2 = {
            'username': 'volunteer-2',
            'first_name': "Sam",
            'last_name': "Turtle",
            'address': "Mario Land",
            'city': second_city,
            'state': second_state,
            'country': second_country,
            'phone_number': "2374983247",
            'email': "volunteer2@volunteer.com"
        }
        v2 = create_volunteer_with_details(volunteer_2, org_obj)

        # Assign shift to the volunteer
        registered_vol_shift = register_volunteer_for_shift_utility(s2, v2)

        # open Shift Sign Up
        sign_up_page.navigate_to_sign_up()

        # on event page
        self.assertEqual(
            sign_up_page.get_info_box().text,
            sign_up_page.no_event_message
        )

    def test_search_event_name_present(self):
        """
        tests for search results on the basis of event name
        """
        register_event_utility()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page
        sign_up_page.live_server_url = self.live_server_url

        # Enter name of the event
        sign_up_page.go_to_sign_up_page()
        parameters = {
            'name': 'event',
            'date_from': '',
            'date_to': '',
            'city': '',
            'state': '',
            'country': ''
        }
        sign_up_page.fill_search_form(parameters)
        # Verify that the event shows up
        self.assertEqual(sign_up_page.get_event_name(), 'event')

    def test_search_event_both_date_present(self):
        """
        tests for search results on the basis of event start date and end date
        """
        register_event_utility()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page
        sign_up_page.live_server_url = self.live_server_url

        # Enter date range in which an event starts
        sign_up_page.go_to_sign_up_page()
        parameters = {
            'name': '',
            'date_from': '05/08/2050',
            'date_to': '05/31/2050',
            'city': '',
            'state': '',
            'country': ''
        }
        sign_up_page.fill_search_form(parameters)
        # Verify that the event shows up
        self.assertEqual(sign_up_page.get_event_name(), 'event')

    def test_search_event_start_date_present(self):
        """
        tests for search results on the basis of event start date
        """
        register_event_utility()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page
        sign_up_page.live_server_url = self.live_server_url
        # Enter only correct starting date
        sign_up_page.go_to_sign_up_page()
        parameters = {
            'name': '',
            'date_from': '05/08/2050',
            'date_to': '',
            'city': '',
            'state': '',
            'country': ''
        }
        sign_up_page.fill_search_form(parameters)
        # Verify that the event shows up
        self.assertEqual(sign_up_page.get_event_name(), 'event')

    def test_search_event_end_date_present(self):
        """
        tests for search results on the basis of event end date
        """
        register_event_utility()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page
        sign_up_page.live_server_url = self.live_server_url

        # Enter correct ending date
        sign_up_page.go_to_sign_up_page()
        parameters = {
            'name': '',
            'date_from': '',
            'date_to': '06/15/2050',
            'city': '',
            'state': '',
            'country': ''
        }
        sign_up_page.fill_search_form(parameters)
        # Verify that the event shows up
        self.assertEqual(sign_up_page.get_event_name(), 'event')

    def test_search_event_city_present(self):
        """
        tests for search results on the basis of event city
        """
        event = register_event_utility()
        city_name = 'Roorkee'
        city = get_city_by_name(city_name)
        event.city = city
        event.save()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page
        sign_up_page.live_server_url = self.live_server_url

        # Enter correct city
        sign_up_page.go_to_sign_up_page()
        parameters = parameters = {
            'name': '',
            'date_from': '',
            'date_to': '',
            'city': 'Roorkee',
            'state': '',
            'country': ''
        }
        sign_up_page.fill_search_form(parameters)
        # Verify that the event shows up
        self.assertEqual(sign_up_page.get_event_name(), 'event')

    def test_search_event_state_present(self):
        """
        tests for search results on the basis of event state
        """
        event = register_event_utility()
        state_name = 'Uttarakhand'
        state = get_state_by_name(state_name)
        event.state = state
        event.save()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page
        sign_up_page.live_server_url = self.live_server_url

        # Enter correct state
        sign_up_page.go_to_sign_up_page()
        parameters = parameters = {
            'name': '',
            'date_from': '',
            'date_to': '',
            'city': '',
            'state': 'Uttarakhand',
            'country': ''
        }
        sign_up_page.fill_search_form(parameters)
        # Verify that the event shows up
        self.assertEqual(sign_up_page.get_event_name(), 'event')

    def test_search_event_country_present(self):
        """
        tests for search results on the basis of event country
        """
        event = register_event_utility()
        country_name = 'India'
        country = get_country_by_name(country_name)
        event.country = country
        event.save()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page
        sign_up_page.live_server_url = self.live_server_url

        # Enter correct country
        sign_up_page.go_to_sign_up_page()
        parameters = {
            'name': '',
            'date_from': '',
            'date_to': '',
            'city': '',
            'state': '',
            'country': 'India'
        }
        sign_up_page.fill_search_form(parameters)
        # Verify that the event shows up
        self.assertEqual(sign_up_page.get_event_name(), 'event')

    def test_search_job_name_present(self):
        """
        tests for search results on the basis of job name
        """
        register_event_utility()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page
        sign_up_page.live_server_url = self.live_server_url
        sign_up_page.navigate_to_sign_up()
        sign_up_page.click_to_view_jobs()

        # Enter name of the job
        parameters = {
            'name': 'job',
            'date_from': '',
            'date_to': '',
            'city': '',
            'state': '',
            'country': ''
        }
        sign_up_page.fill_job_search_form(parameters)
        # Verify that the job shows up
        self.assertEqual(sign_up_page.get_job_name(), 'job')

    def test_search_job_both_date_present(self):
        """
        tests for search results on the basis of start and end date
        """
        register_event_utility()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page
        sign_up_page.live_server_url = self.live_server_url
        sign_up_page.navigate_to_sign_up()
        sign_up_page.click_to_view_jobs()

        # Enter date range in which a job starts
        parameters = {
            'name': '',
            'date_from': '05/10/2050',
            'date_to': '06/15/2050',
            'city': '',
            'state': '',
            'country': ''
        }
        sign_up_page.fill_job_search_form(parameters)
        # Verify that the job shows up
        self.assertEqual(sign_up_page.get_job_name(), 'job')

    def test_search_job_start_date_present(self):
        """
        tests for search results on the basis of start date
        """
        register_event_utility()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page
        sign_up_page.live_server_url = self.live_server_url
        # Enter only correct starting date
        sign_up_page.navigate_to_sign_up()
        sign_up_page.click_to_view_jobs()

        parameters = {
            'name': '',
            'date_from': '05/10/2050',
            'date_to': '',
            'city': '',
            'state': '',
            'country': ''
        }
        sign_up_page.fill_job_search_form(parameters)
        # Verify that the job shows up
        self.assertEqual(sign_up_page.get_job_name(), 'job')

    def test_search_job_end_date_present(self):
        """
        tests for search results on the basis of end date
        """
        register_event_utility()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page
        sign_up_page.live_server_url = self.live_server_url
        sign_up_page.navigate_to_sign_up()
        sign_up_page.click_to_view_jobs()

        # Enter correct ending date
        parameters = {
            'name': '',
            'date_from': '',
            'date_to': '06/15/2050',
            'city': '',
            'state': '',
            'country': ''
        }
        sign_up_page.fill_job_search_form(parameters)
        # Verify that the job shows up
        self.assertEqual(sign_up_page.get_job_name(), 'job')

    def test_search_job_city_present(self):
        """
        tests for search results on the basis of city
        """
        event_obj = register_event_utility()
        city_name = 'Roorkee'
        city = get_city_by_name(city_name)
        event_obj.city = city
        event_obj.save()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page
        sign_up_page.live_server_url = self.live_server_url
        sign_up_page.navigate_to_sign_up()
        sign_up_page.click_to_view_jobs()

        # Enter correct city
        parameters = {
            'name': '',
            'date_from': '',
            'date_to': '',
            'city': 'Roorkee',
            'state': '',
            'country': ''
        }
        sign_up_page.fill_job_search_form(parameters)
        # Verify that the job shows up
        self.assertEqual(sign_up_page.get_job_name(), 'job')

    def test_search_job_state_present(self):
        """
        tests for search results on the basis of state
        """
        event_obj = register_event_utility()
        state_name = 'Uttarakhand'
        state = get_state_by_name(state_name)
        event_obj.state = state
        event_obj.save()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page
        sign_up_page.live_server_url = self.live_server_url
        sign_up_page.navigate_to_sign_up()
        sign_up_page.click_to_view_jobs()

        # Enter correct state
        parameters = {
            'name': '',
            'date_from': '',
            'date_to': '',
            'city': '',
            'state': 'Uttarakhand',
            'country': ''
        }
        sign_up_page.fill_job_search_form(parameters)
        # Verify that the job shows up
        self.assertEqual(sign_up_page.get_job_name(), 'job')

    def test_search_job_country_present(self):
        """
        tests for search results on the basis of country
        """
        event_obj = register_event_utility()
        country_name = 'India'
        country = get_country_by_name(country_name)
        event_obj.country = country
        event_obj.save()
        register_job_utility()
        register_shift_utility()

        sign_up_page = self.sign_up_page
        sign_up_page.live_server_url = self.live_server_url
        sign_up_page.navigate_to_sign_up()
        sign_up_page.click_to_view_jobs()

        # Enter correct country
        parameters = {
            'name': '',
            'date_from': '',
            'date_to': '',
            'city': '',
            'state': '',
            'country': 'India'
        }
        sign_up_page.fill_job_search_form(parameters)
        # Verify that the job shows up
        self.assertEqual(sign_up_page.get_job_name(), 'job')

