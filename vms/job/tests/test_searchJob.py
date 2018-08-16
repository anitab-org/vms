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
from pom.pages.jobSearchPage import JobSearchPage
from shift.utils import (get_country_by_name, get_state_by_name,
                         get_city_by_name, create_admin,
                         create_event_with_details, create_job_with_details,
                         create_country, create_state, create_city)


class SearchJob(LiveServerTestCase):
    """
    SearchJob class contains tests to check '/job/list/' view.
    Choices of parameters contains
    - Name
    - Start Date
    - End Date
    - City
    - State
    - Country
    - Event
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

        cls.event_1 = {
            'name': 'event',
            'start_date': '2050-05-10',
            'end_date': '2050-06-16',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }

        cls.event_2 = {
            'name': 'eventq',
            'start_date': '2050-05-10',
            'end_date': '2050-06-16',
            'description': 'event-descriptionq',
            'address': 'event-addressq',
            'venue': 'event-venueq'
        }

        cls.expected_result_one = [
            'job-name', 'event', 'June', '10,', '2050',
            'June', '11,', '2050', 'Details', 'Edit', 'Delete'
        ]
        cls.expected_result_two = [
            'job-nameq', 'eventq', 'May', '15,', '2050',
            'May', '20,', '2050', 'Details', 'Edit', 'Delete'
        ]

        firefox_options = Options()
        firefox_options.add_argument('-headless')
        cls.driver = webdriver.Firefox(firefox_options=firefox_options)
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.search_page = JobSearchPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        cls.wait = WebDriverWait(cls.driver, 10)
        super(SearchJob, cls).setUpClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test
        """
        e1 = create_event_with_details(self.event_1)
        e2 = create_event_with_details(self.event_2)
        country = create_country()
        state = create_state()
        city = create_city()
        e1.city = city
        e1.state = state
        e1.country = country
        e1.save()

        create_admin()
        city_name = 'Bothell'
        second_city = get_city_by_name(city_name)
        state_name = 'Washington'
        second_state = get_state_by_name(state_name)
        country_name = 'United States'
        second_country = get_country_by_name(country_name)
        e2.city = second_city
        e2.state = second_state
        e2.country = second_country
        e2.save()
        job_1 = {
            'name': 'job-name',
            'start_date': '2050-06-10',
            'end_date': '2050-06-11',
            'description': 'job-description',
            'event': e1
        }
        job_2 = {
            'name': 'job-nameq',
            'start_date': '2050-05-15',
            'end_date': '2050-05-20',
            'description': 'job-description',
            'event': e2
        }
        j1 = create_job_with_details(job_1)
        j2 = create_job_with_details(job_2)
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
        super(SearchJob, cls).tearDownClass()

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
        Utility function to perform explicit wait for home page.
        """
        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//h1[contains(text(), 'Volunteer Management System')]"
                )
            )
        )

    def test_job_name_field(self):
        """
        Test search results for job name
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url

        search_page.navigate_to_job_search_page()

        search_page.search_name_field('job')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 2)
        self.assertTrue(self.expected_result_one in result)
        self.assertTrue(self.expected_result_two in result)

        search_page.search_name_field('j')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 2)
        self.assertTrue(self.expected_result_one in result)
        self.assertTrue(self.expected_result_two in result)

        search_page.search_name_field('jobq-')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_name_field('job-fail-test')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_name_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(), None)

    def test_job_start_and_end_date_field(self):
        """
        Test search results for job start date and end date
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url

        search_page.navigate_to_job_search_page()

        # search for jobs filling only start date
        search_page.search_start_date_field('06/11/2050')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        # search filling end date only
        search_page.navigate_to_job_search_page()
        search_page.search_end_date_field('06/10/2050')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 2)
        self.assertTrue(self.expected_result_one in result)
        self.assertTrue(self.expected_result_two in result)

        # search filling both start and end date
        search_page.navigate_to_job_search_page()
        search_page.search_start_date_field('05/15/2050')
        search_page.search_end_date_field('06/09/2050')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 1)
        self.assertTrue(self.expected_result_two in result)

    def test_job_city_field(self):
        """
        Test search results for job city
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url

        search_page.navigate_to_job_search_page()
        search_page.search_city_field('Roorkee')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 1)
        self.assertTrue(self.expected_result_one in result)

        search_page.search_city_field('Bothell')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 1)
        self.assertTrue(self.expected_result_two in result)

        search_page.search_city_field('job-fail-test')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_city_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(), None)

    def test_job_state_field(self):
        """
        Test search results for job state
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url

        search_page.navigate_to_job_search_page()
        search_page.search_state_field('Uttarakhand')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 1)
        self.assertTrue(self.expected_result_one in result)

        search_page.search_state_field('Washington')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 1)
        self.assertTrue(self.expected_result_two in result)

        search_page.search_state_field('job-fail-test')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_state_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(), None)

    def test_job_country_field(self):
        """
        Test search results for job country
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url

        search_page.navigate_to_job_search_page()
        search_page.search_country_field('India')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 1)
        self.assertTrue(self.expected_result_one in result)

        search_page.search_country_field('United States')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 1)
        self.assertTrue(self.expected_result_two in result)

        search_page.search_country_field('job-fail-test')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_country_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(), None)

    def test_job_event_field(self):
        """
        Test search results for job event
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url

        search_page.navigate_to_job_search_page()
        search_page.search_event_field('event')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 2)
        self.assertTrue(self.expected_result_one in result)
        self.assertTrue(self.expected_result_two in result)

        search_page.search_event_field('wrong-event')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

    def test_intersection_of_all_fields(self):
        """
        Test search results for different combinations of job name,
        start date, end date, city, state, country and event
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url

        search_page.navigate_to_job_search_page()
        search_page.search_name_field('job')
        search_page.search_start_date_field('01/01/2017')
        search_page.search_end_date_field('10/06/2050')
        search_page.search_city_field('Roorkee')
        search_page.search_state_field('Uttarakhand')
        search_page.search_country_field('India')
        search_page.search_event_field('event')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 1)
        self.assertTrue(self.expected_result_one in result)

        search_page.search_name_field('job')
        search_page.search_country_field('wrong-country')
        search_page.search_event_field('event')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_state_field('job')
        search_page.search_city_field('wrong-city')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

