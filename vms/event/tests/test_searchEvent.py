# third party
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.eventSearchPage import EventSearchPage
from shift.utils import (create_country, create_city,
                         create_state, create_admin,
                         create_event_with_details,
                         create_job_with_details, get_city_by_name,
                         get_state_by_name, get_country_by_name)


class SearchEvent(LiveServerTestCase):
    """
    SearchEvent class contains tests to check '/event/search/' view.
    Choices of parameters contains
    - Name
    - Start Date
    - End Date
    - City
    - State
    - Country
    - Job
    Class contains 7 tests to check each parameter separately and also to check
    if a combination of parameters entered, then intersection of all results is
    obtained.
    """

    @classmethod
    def setUpClass(cls):
        """
        Method to initiate class level objects.

        This method initiates Firefox WebDriver, WebDriverWait and
        the corresponding POM objects for this Test Class
        """
        firefox_options = Options()
        firefox_options.add_argument('-headless')
        cls.driver = webdriver.Firefox(firefox_options=firefox_options)
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.search_page = EventSearchPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        cls.wait = WebDriverWait(cls.driver, 10)
        super(SearchEvent, cls).setUpClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test
        """
        create_admin()
        self.login_admin()
        self.wait_for_home_page()

    def tearDown(self):
        """
        Method contains statements to be executed at the end of
        each test.
        """
        self.authentication_page.logout()

    @classmethod
    def tearDownClass(cls):
        """
        Class method to quit the Firefox WebDriver session after
        execution of all tests in class.
        """
        cls.driver.quit()
        super(SearchEvent, cls).tearDownClass()

    def login_admin(self):
        """
        Utility function to login an admin user to perform all tests.
        """
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({
            'username': 'admin',
            'password': 'admin'
        })

    def wait_for_home_page(self):
        """

        """
        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//h1[contains(text(), 'Volunteer Management System')]"
                )
            )
        )

    def test_event_name_field(self):
        """
        Test search results for event name
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url
        search_page.navigate_to_event_search_page()

        credentials_1 = {
            'name': 'event-name',
            'start_date': '2015-01-01',
            'end_date': '2015-03-01',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }

        event_1 = create_event_with_details(credentials_1)

        credentials_2 = {
            'name': 'event-nameq',
            'start_date': '2015-02-01',
            'end_date': '2015-04-01',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }

        event_2 = create_event_with_details(credentials_2)

        expected_result_one = [
            'event-name', 'Jan.', '1,', '2015', 'March',
            '1,', '2015', 'Details', 'Edit', 'Delete'
        ]
        expected_result_two = [
            'event-nameq', 'Feb.', '1,', '2015', 'April',
            '1,', '2015', 'Details', 'Edit', 'Delete'
        ]

        search_page.search_name_field('event')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 2)

        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        search_page.search_name_field('n')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 2)

        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        search_page.search_name_field('eve-')
        search_page.submit_form()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_name_field('event-fail-test')
        search_page.submit_form()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_name_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(), None)

    def test_event_start_and_end_date_field(self):
        """
        Test search results for event start date and end date
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url
        search_page.navigate_to_event_search_page()

        credentials_1 = {
            'name': 'event-name',
            'start_date': '2015-01-01',
            'end_date': '2015-03-01',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }

        event_1 = create_event_with_details(credentials_1)

        credentials_2 = {
            'name': 'event-nameq',
            'start_date': '2015-02-01',
            'end_date': '2015-04-01',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }

        event_2 = create_event_with_details(credentials_2)

        expected_result_one = [
            'event-name', 'Jan.', '1,', '2015', 'March',
            '1,', '2015', 'Details', 'Edit', 'Delete'
        ]
        expected_result_two = [
            'event-nameq', 'Feb.', '1,', '2015', 'April',
            '1,', '2015', 'Details', 'Edit', 'Delete'
        ]

        # search for events filling only start date
        search_page.search_start_date_field('12/01/2015')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        # search filling end date only
        search_page.navigate_to_event_search_page()
        search_page.search_end_date_field('02/15/2015')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)

        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_two in result)
        self.assertTrue(expected_result_one in result)

        # search filling both start and end date
        search_page.navigate_to_event_search_page()
        search_page.search_start_date_field('01/01/2015')
        search_page.search_end_date_field('01/15/2015')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 1)
        self.assertTrue(expected_result_one in result)

    def test_event_city_field(self):
        """
        Test search results for event city
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url
        search_page.navigate_to_event_search_page()

        create_country()
        create_state()
        city = create_city()
        credentials_1 = {
            'name': 'event-name',
            'start_date': '2015-01-01',
            'end_date': '2015-03-01',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }

        event_1 = create_event_with_details(credentials_1)
        event_1.city = city
        event_1.save()

        credentials_2 = {
            'name': 'event-nameq',
            'start_date': '2015-02-01',
            'end_date': '2015-04-01',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }

        city_name = 'Bothell'
        second_city = get_city_by_name(city_name)
        event_2 = create_event_with_details(credentials_2)
        event_2.city = second_city
        event_2.save()

        expected_result_one = [
            'event-name', 'Jan.', '1,', '2015', 'March',
            '1,', '2015', 'Details', 'Edit', 'Delete'
        ]
        expected_result_two = [
            'event-nameq', 'Feb.', '1,', '2015', 'April',
            '1,', '2015', 'Details', 'Edit', 'Delete'
        ]

        search_page.search_city_field('Roorkee')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 1)
        self.assertTrue(expected_result_one in result)

        search_page.search_city_field('Bothell')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 1)
        self.assertTrue(expected_result_two in result)

        search_page.search_city_field('eve-')
        search_page.submit_form()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_city_field('event-fail-test')
        search_page.submit_form()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_city_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(), None)

    def test_event_state_field(self):
        """
        Test search results for event state field
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url
        search_page.navigate_to_event_search_page()

        credentials_1 = {
            'name': 'event-name',
            'start_date': '2015-01-01',
            'end_date': '2015-03-01',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        event_1 = create_event_with_details(credentials_1)
        create_country()
        state = create_state()
        event_1.state = state
        event_1.save()

        credentials_2 = {
            'name': 'event-nameq',
            'start_date': '2015-02-01',
            'end_date': '2015-04-01',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        event_2 = create_event_with_details(credentials_2)

        state_name = 'Washington'
        second_state = get_state_by_name(state_name)
        event_2.state = second_state
        event_2.save()

        expected_result_one = [
            'event-name', 'Jan.', '1,', '2015', 'March',
            '1,', '2015', 'Details', 'Edit', 'Delete'
        ]
        expected_result_two = [
            'event-nameq', 'Feb.', '1,', '2015', 'April',
            '1,', '2015', 'Details', 'Edit', 'Delete'
        ]

        search_page.search_state_field('Uttarakhand')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 1)
        self.assertTrue(expected_result_one in result)

        search_page.search_state_field('Washington')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 1)
        self.assertTrue(expected_result_two in result)

        search_page.search_state_field('eve-')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_state_field('event-fail-test')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_state_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(), None)

    def test_event_country_field(self):
        """
        Test search results for event country field
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url
        search_page.navigate_to_event_search_page()

        credentials_1 = {
            'name': 'event-name',
            'start_date': '2015-01-01',
            'end_date': '2015-03-01',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }

        country = create_country()
        event_1 = create_event_with_details(credentials_1)
        event_1.country = country
        event_1.save()

        credentials_2 = {
            'name': 'event-nameq',
            'start_date': '2015-02-01',
            'end_date': '2015-04-01',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }

        country_name = 'United States'
        second_country = get_country_by_name(country_name)
        event_2 = create_event_with_details(credentials_2)
        event_2.country = second_country
        event_2.save()

        expected_result_one = [
            'event-name', 'Jan.', '1,', '2015', 'March',
            '1,', '2015', 'Details', 'Edit', 'Delete'
        ]
        expected_result_two = [
            'event-nameq', 'Feb.', '1,', '2015', 'April',
            '1,', '2015', 'Details', 'Edit', 'Delete'
        ]

        search_page.search_country_field('India')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 1)
        self.assertTrue(expected_result_one in result)

        search_page.search_country_field('United States')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 1)
        self.assertTrue(expected_result_two in result)

        search_page.search_country_field('eve-')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_country_field('event-fail-test')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_country_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(), None)

    def test_event_job_field(self):
        """
        Test search results for event job field
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url

        credentials_1 = {
            'name': 'event-name',
            'start_date': '2015-01-01',
            'end_date': '2015-03-01',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }

        event_1 = create_event_with_details(credentials_1)

        credentials_2 = {
            'name': 'event-nameq',
            'start_date': '2015-02-01',
            'end_date': '2015-04-01',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        event_2 = create_event_with_details(credentials_2)

        expected_result_one = [
            'event-name', 'Jan.', '1,', '2015', 'March',
            '1,', '2015', 'Details', 'Edit', 'Delete'
        ]
        expected_result_two = [
            'event-nameq', 'Feb.', '1,', '2015', 'April',
            '1,', '2015', 'Details', 'Edit', 'Delete'
        ]

        # job_1 for event_1, job_2 for event_2
        job = {
            'name': 'job-name',
            'start_date': '2015-02-01',
            'end_date': '2015-02-15',
            'description': 'job-description',
            'event': event_1
        }
        job_1 = create_job_with_details(job)

        job = {
            'name': 'job-nameq',
            'start_date': '2015-02-02',
            'end_date': '2015-02-15',
            'description': 'job-description',
            'event': event_2
        }
        job_2 = create_job_with_details(job)

        # search job_1 and job_2
        search_page.navigate_to_event_search_page()
        search_page.search_job_field("job-name")
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

    def test_intersection_of_all_fields(self):
        """
        Test search results for different combinations of
        event name, start date, end date, city, state, country and job
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url

        credentials_1 = {
            'name': 'event-name',
            'start_date': '2015-01-01',
            'end_date': '2015-03-01',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }

        country = create_country()
        state = create_state()
        city = create_city()
        event_1 = create_event_with_details(credentials_1)
        event_1.country = country
        event_1.state = state
        event_1.city = city
        event_1.save()
        job = {
            'name': 'job',
            'start_date': '2015-02-01',
            'end_date': '2015-02-15',
            'description': 'descriptionq',
            'event': event_1
        }
        job_1 = create_job_with_details(job)

        credentials_2 = {
            'name': 'event-nameq',
            'start_date': '2015-02-01',
            'end_date': '2015-04-01',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        event_2 = create_event_with_details(credentials_2)
        country_name = 'United States'
        state_name = 'Washington'
        city_name = 'Bothell'
        second_country = get_country_by_name(country_name)
        second_state = get_state_by_name(state_name)
        second_city = get_city_by_name(city_name)
        event_2.country = second_country
        event_2.state = second_state
        event_2.city = second_city
        event_2.save()
        job = {
            'name': 'jobq',
            'start_date': '2015-02-02',
            'end_date': '2015-02-15',
            'description': 'job-description',
            'event': event_2
        }
        job_2 = create_job_with_details(job)

        expected_result_one = [
            'event-name', 'Jan.', '1,', '2015', 'March',
            '1,', '2015', 'Details', 'Edit', 'Delete'
        ]
        expected_result_two = [
            'event-nameq', 'Feb.', '1,', '2015', 'April',
            '1,', '2015', 'Details', 'Edit', 'Delete'
        ]
        search_page.navigate_to_event_search_page()

        search_page.search_name_field('event')
        search_page.search_start_date_field('2015-01-01')
        search_page.search_end_date_field('2015-04-01')
        search_page.search_state_field('Uttarakhand')
        search_page.search_country_field('India')
        search_page.search_job_field('job')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertTrue(expected_result_one in result)

        search_page.search_name_field('event')
        search_page.search_country_field('wrong-country')
        search_page.search_job_field(job_1.id)
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_state_field('event')
        search_page.search_city_field('wrong-city')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

