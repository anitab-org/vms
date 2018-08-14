# third party
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.volunteerSearchPage import VolunteerSearchPage
from pom.pages.volunteerReportPage import VolunteerReportPage
from pom.locators.volunteerSearchPageLocators import VolunteerSearchPageLocators
from pom.pageUrls import PageUrls
from shift.utils import (create_admin, create_country, create_state,
                         create_city, create_volunteer_with_details,
                         create_organization_with_details,
                         register_past_event_utility,
                         register_past_shift_utility,
                         register_past_job_utility,
                         create_report_with_details, log_hours_with_details,
                         register_volunteer_for_shift_utility,
                         get_country_by_name, get_state_by_name,
                         get_city_by_name, register_event_utility,
                         register_job_utility, register_shift_utility)


class SearchVolunteer(LiveServerTestCase):
    """
    SearchVolunteer class contains tests to check '/voluneer/search/' view.
    Choices of parameters contains
    - First Name
    - Last Name
    - City
    - State
    - Country
    - Organization
    - Event
    - Job
    Class contains 9 tests to check each parameter separately and also to check
    if a combination of parameters entered, then intersection of all results is
    obtained.
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
        cls.search_page = VolunteerSearchPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        cls.report_page = VolunteerReportPage(cls.driver)
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.elements = VolunteerSearchPageLocators()
        super(SearchVolunteer, cls).setUpClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        create_admin()
        self.login_admin()
        self.wait_for_home_page()

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
        super(SearchVolunteer, cls).tearDownClass()

    def login_admin(self):
        """
        Utility function to login an admin user to perform all tests.
        """
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({
            'username': 'admin',
            'password': 'admin'
        })

    def verify_report_details(self, reports):
        """
        Utility function to verify the shift details.
        :param reports: Total number of reports as filled in form.
        """
        total_no_of_reports = self.report_page.get_report_hours()
        self.assertEqual(total_no_of_reports, reports)

    def wait_for_home_page(self):
        """
        Utility function to perform explicit wait for home page.
        """
        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//h1[contains(text(),"
                    " 'Volunteer Management System')]"
                )
            )
        )

    def test_volunteer_first_name_field(self):
        """
        Test volunteer search form using the first name of the volunteers.
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url
        search_page.navigate_to_volunteer_search_page()

        country = create_country()
        state = create_state()
        city = create_city()
        credentials_1 = {
            'username': 'volunteer-username',
            'first_name': 'VOLUNTEER-FIRST-NAME',
            'last_name': 'volunteer-last-name',
            'address': 'volunteer-address',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email@systers.org'
        }

        org_name = 'volunteer-organization'
        org_obj = create_organization_with_details(org_name)
        volunteer_1 = create_volunteer_with_details(credentials_1, org_obj)

        credentials_2 = {
            'username': 'volunteer-usernameq',
            'first_name': 'volunteer-first-name',
            'last_name': 'volunteer-last-nameq',
            'address': 'volunteer-addressq',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email2@systers.orgq'
        }

        org_name = 'volunteer-organizationq'
        org_obj = create_organization_with_details(org_name)
        volunteer_2 = create_volunteer_with_details(credentials_2, org_obj)

        expected_result_one = [
            'VOLUNTEER-FIRST-NAME', 'volunteer-last-name',
            'volunteer-address', 'Roorkee,', 'Uttarakhand,',
            'India', 'Uttarakhand,', 'India', 'India',
            'volunteer-organization', '9999999999',
            'volunteer-email@systers.org', 'View'
        ]

        expected_result_two = [
            'volunteer-first-name', 'volunteer-last-nameq',
            'volunteer-addressq', 'Roorkee,', 'Uttarakhand,',
            'India', 'Uttarakhand,', 'India', 'India',
            'volunteer-organizationq', '9999999999',
            'volunteer-email2@systers.orgq', 'View'
        ]

        search_page.search_first_name_field('volunteer')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_two in result)
        self.assertTrue(expected_result_one in result)

        search_page.search_first_name_field('e')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 2)

        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        search_page.search_first_name_field('vol-')
        search_page.submit_form()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_first_name_field('volunteer-fail-test')
        search_page.submit_form()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_first_name_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(), None)

    def test_volunteer_last_name_field(self):
        """
        Test volunteer search form using the last name of the volunteers.
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url
        search_page.navigate_to_volunteer_search_page()

        country = create_country()
        state = create_state()
        city = create_city()
        credentials_1 = {
            'username': 'volunteer-username',
            'first_name': 'volunteer-first-name',
            'last_name': 'VOLUNTEER-LAST-NAME',
            'address': 'volunteer-address',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email@systers.org'
        }

        org_name = 'volunteer-organization'
        org_obj = create_organization_with_details(org_name)
        volunteer_1 = create_volunteer_with_details(credentials_1, org_obj)

        credentials_2 = {
            'username': 'volunteer-usernameq',
            'first_name': 'volunteer-first-nameq',
            'last_name': 'volunteer-last-name',
            'address': 'volunteer-addressq',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email2@systers.orgq'
        }
        org_name = 'volunteer-organizationq'
        org_obj = create_organization_with_details(org_name)
        volunteer_2 = create_volunteer_with_details(credentials_2, org_obj)

        expected_result_one = [
            'volunteer-first-name', 'VOLUNTEER-LAST-NAME',
            'volunteer-address', 'Roorkee,', 'Uttarakhand,',
            'India', 'Uttarakhand,', 'India', 'India',
            'volunteer-organization', '9999999999',
            'volunteer-email@systers.org', 'View'
        ]

        expected_result_two = [
            'volunteer-first-nameq', 'volunteer-last-name',
            'volunteer-addressq', 'Roorkee,', 'Uttarakhand,',
            'India', 'Uttarakhand,', 'India', 'India',
            'volunteer-organizationq', '9999999999',
            'volunteer-email2@systers.orgq', 'View'
        ]

        search_page.search_last_name_field('volunteer')
        search_page.submit_form()

        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)

        self.assertTrue(expected_result_two in result)
        self.assertTrue(expected_result_one in result)

        search_page.search_last_name_field('v')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 2)

        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        search_page.search_last_name_field('vol-')
        search_page.submit_form()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_last_name_field('volunteer-fail-test')
        search_page.submit_form()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_last_name_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(), None)

    def test_volunteer_city_field(self):
        """
        Test volunteer search form using the city field of the volunteers.
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url
        search_page.navigate_to_volunteer_search_page()

        country = create_country()
        state = create_state()
        city = create_city()
        credentials_1 = {
            'username': 'volunteer-username',
            'first_name': 'volunteer-first-name',
            'last_name': 'volunteer-last-name',
            'address': 'volunteer-address',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email@systers.org'
        }

        org_name = 'volunteer-organization'
        org_obj = create_organization_with_details(org_name)
        volunteer_1 = create_volunteer_with_details(credentials_1, org_obj)

        country_name = 'United States'
        state_name = 'Washington'
        city_name = 'Bothell'
        second_country = get_country_by_name(country_name)
        second_state = get_state_by_name(state_name)
        second_city = get_city_by_name(city_name)
        credentials_2 = {
            'username': 'volunteer-usernameq',
            'first_name': 'volunteer-first-nameq',
            'last_name': 'volunteer-last-nameq',
            'address': 'volunteer-addressq',
            'city': second_city,
            'state': second_state,
            'country': second_country,
            'phone_number': '9999999999',
            'email': 'volunteer-email2@systers.orgq'
        }

        org_name = 'volunteer-organizationq'
        org_obj = create_organization_with_details(org_name)
        volunteer_2 = create_volunteer_with_details(credentials_2, org_obj)

        expected_result_one = [
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-address', 'Roorkee,', 'Uttarakhand,',
            'India', 'Uttarakhand,', 'India', 'India',
            'volunteer-organization', '9999999999',
            'volunteer-email@systers.org', 'View'
        ]

        expected_result_two = [
            'volunteer-first-nameq', 'volunteer-last-nameq',
            'volunteer-addressq', 'Bothell,', 'Washington,',
            'United', 'States', 'Washington,', 'United',
            'States', 'United', 'States', 'volunteer-organizationq',
            '9999999999', 'volunteer-email2@systers.orgq', 'View'
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

        search_page.search_city_field('vol-')
        search_page.submit_form()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_city_field('volunteer-fail-test')
        search_page.submit_form()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_city_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(), None)

    def test_volunteer_state_field(self):
        """
        Test volunteer search form using the state field of the volunteers.
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url
        search_page.navigate_to_volunteer_search_page()

        country = create_country()
        state = create_state()
        city = create_city()
        credentials_1 = {
            'username': 'volunteer-username',
            'first_name': 'volunteer-first-name',
            'last_name': 'volunteer-last-name',
            'address': 'volunteer-address',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email@systers.org'
        }

        org_name = 'volunteer-organization'
        org_obj = create_organization_with_details(org_name)
        volunteer_1 = create_volunteer_with_details(credentials_1, org_obj)

        country_name = 'United States'
        state_name = 'Washington'
        city_name = 'Bothell'
        second_country = get_country_by_name(country_name)
        second_state = get_state_by_name(state_name)
        second_city = get_city_by_name(city_name)
        credentials_2 = {
            'username': 'volunteer-usernameq',
            'first_name': 'volunteer-first-nameq',
            'last_name': 'volunteer-last-nameq',
            'address': 'volunteer-addressq',
            'city': second_city,
            'state': second_state,
            'country': second_country,
            'phone_number': '9999999999',
            'email': 'volunteer-email2@systers.orgq'
        }

        org_name = 'volunteer-organizationq'
        org_obj = create_organization_with_details(org_name)
        volunteer_2 = create_volunteer_with_details(credentials_2, org_obj)

        expected_result_one = [
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-address', 'Roorkee,', 'Uttarakhand,',
            'India', 'Uttarakhand,', 'India', 'India',
            'volunteer-organization', '9999999999',
            'volunteer-email@systers.org', 'View'
        ]

        expected_result_two = [
            'volunteer-first-nameq', 'volunteer-last-nameq',
            'volunteer-addressq', 'Bothell,', 'Washington,',
            'United', 'States', 'Washington,', 'United',
            'States', 'United', 'States', 'volunteer-organizationq',
            '9999999999', 'volunteer-email2@systers.orgq', 'View'
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

        search_page.search_state_field('vol-')
        search_page.submit_form()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_state_field('volunteer-fail-test')
        search_page.submit_form()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_state_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(), None)

    def test_volunteer_country_field(self):
        """
        Test volunteer search form using the country field of the volunteers.
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url
        search_page.navigate_to_volunteer_search_page()

        country = create_country()
        state = create_state()
        city = create_city()
        credentials_1 = {
            'username': 'volunteer-username',
            'first_name': 'volunteer-first-name',
            'last_name': 'volunteer-last-name',
            'address': 'volunteer-address',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email@systers.org'
        }

        org_name = 'volunteer-organization'
        org_obj = create_organization_with_details(org_name)
        volunteer_1 = create_volunteer_with_details(credentials_1, org_obj)

        country_name = 'United States'
        state_name = 'Washington'
        city_name = 'Bothell'
        second_country = get_country_by_name(country_name)
        second_state = get_state_by_name(state_name)
        second_city = get_city_by_name(city_name)
        credentials_2 = {
            'username': 'volunteer-usernameq',
            'first_name': 'volunteer-first-nameq',
            'last_name': 'volunteer-last-nameq',
            'address': 'volunteer-addressq',
            'city': second_city,
            'state': second_state,
            'country': second_country,
            'phone_number': '9999999999',
            'email': 'volunteer-email2@systers.orgq'
        }

        org_name = 'volunteer-organizationq'
        org_obj = create_organization_with_details(org_name)
        volunteer_2 = create_volunteer_with_details(credentials_2, org_obj)

        expected_result_one = [
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-address', 'Roorkee,', 'Uttarakhand,',
            'India', 'Uttarakhand,', 'India', 'India',
            'volunteer-organization', '9999999999',
            'volunteer-email@systers.org', 'View'
        ]

        expected_result_two = [
            'volunteer-first-nameq', 'volunteer-last-nameq',
            'volunteer-addressq', 'Bothell,', 'Washington,',
            'United', 'States', 'Washington,', 'United',
            'States', 'United', 'States', 'volunteer-organizationq',
            '9999999999', 'volunteer-email2@systers.orgq', 'View'
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

        search_page.search_country_field('vol-')
        search_page.submit_form()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_country_field('volunteer-fail-test')
        search_page.submit_form()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_country_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(), None)

    def test_volunteer_valid_organization_field(self):
        """
        Test volunteer search form using the
        organization field of the volunteers.
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url

        country = create_country()
        state = create_state()
        city = create_city()
        credentials_1 = {
            'username': 'volunteer-username',
            'first_name': 'volunteer-first-name',
            'last_name': 'volunteer-last-name',
            'address': 'volunteer-address',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email@systers.org'
        }
        org_name = 'volunteer-organization'
        org_obj = create_organization_with_details(org_name)
        volunteer_1 = create_volunteer_with_details(credentials_1, org_obj)

        credentials_2 = {
            'username': 'volunteer-usernameq',
            'first_name': 'volunteer-first-nameq',
            'last_name': 'volunteer-last-nameq',
            'address': 'volunteer-addressq',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email2@systers.orgq'
        }

        org_name = 'volunteer-organizationq'
        org_obj = create_organization_with_details(org_name)
        volunteer_2 = create_volunteer_with_details(credentials_2, org_obj)

        expected_result_one = [
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-address', 'Roorkee,', 'Uttarakhand,', 'India',
            'Uttarakhand,', 'India', 'India', 'volunteer-organization',
            '9999999999', 'volunteer-email@systers.org', 'View'
        ]

        expected_result_two = [
            'volunteer-first-nameq', 'volunteer-last-nameq',
            'volunteer-addressq', 'Roorkee,', 'Uttarakhand,',
            'India', 'Uttarakhand,', 'India', 'India',
            'volunteer-organizationq', '9999999999',
            'volunteer-email2@systers.orgq', 'View'
        ]

        search_page.navigate_to_volunteer_search_page()
        search_page.search_organization_field('volunteer')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)

        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        search_page.navigate_to_volunteer_search_page()
        search_page.search_organization_field('v')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)

        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

    def test_volunteer_event_field(self):
        """
        Test volunteer search form using the event field of the volunteers.
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url
        search_page.navigate_to_volunteer_search_page()

        country = create_country()
        state = create_state()
        city = create_city()
        credentials_1 = {
            'username': 'volunteer-username',
            'first_name': 'volunteer-first-name',
            'last_name': 'volunteer-last-name',
            'address': 'volunteer-address',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email@systers.org'
        }

        org_name = 'volunteer-organization'
        org_obj = create_organization_with_details(org_name)
        volunteer_1 = create_volunteer_with_details(credentials_1, org_obj)

        credentials_2 = {
            'username': 'volunteer-usernameq',
            'first_name': 'volunteer-first-nameq',
            'last_name': 'volunteer-last-nameq',
            'address': 'volunteer-addressq',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email2@systers.orgq'
        }

        org_name = 'volunteer-organizationq'
        org_obj = create_organization_with_details(org_name)
        volunteer_2 = create_volunteer_with_details(credentials_2, org_obj)

        register_event_utility()
        register_job_utility()
        shift = register_shift_utility()

        expected_result_one = [
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-address', 'Roorkee,', 'Uttarakhand,',
            'India', 'Uttarakhand,', 'India', 'India',
            'volunteer-organization', '9999999999',
            'volunteer-email@systers.org', 'View'
        ]

        expected_result_two = [
            'volunteer-first-nameq', 'volunteer-last-nameq',
            'volunteer-addressq', 'Roorkee,', 'Uttarakhand,',
            'India', 'Uttarakhand,', 'India', 'India',
            'volunteer-organizationq', '9999999999',
            'volunteer-email2@systers.orgq', 'View'
        ]

        # search events with no volunteers
        search_page.search_event_field("event")
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        # volunteer_1 and volunteer_2 both registered for event
        register_volunteer_for_shift_utility(shift, volunteer_1)
        register_volunteer_for_shift_utility(shift, volunteer_2)

        # search event
        search_page.navigate_to_volunteer_search_page()
        search_page.search_event_field("event")
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

    def test_volunteer_job_field(self):
        """
        Test volunteer search form using the job field of the volunteers.
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url

        country = create_country()
        state = create_state()
        city = create_city()
        credentials_1 = {
            'username': 'volunteer-username',
            'first_name': 'volunteer-first-name',
            'last_name': 'volunteer-last-name',
            'address': 'volunteer-address',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email@systers.org'
        }

        org_name = 'volunteer-organization'
        org_obj = create_organization_with_details(org_name)
        volunteer_1 = create_volunteer_with_details(credentials_1, org_obj)

        credentials_2 = {
            'username': 'volunteer-usernameq',
            'first_name': 'volunteer-first-nameq',
            'last_name': 'volunteer-last-nameq',
            'address': 'volunteer-addressq',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email2@systers.orgq'
        }

        org_name = 'volunteer-organizationq'
        org_obj = create_organization_with_details(org_name)
        volunteer_2 = create_volunteer_with_details(credentials_2, org_obj)

        register_event_utility()
        register_job_utility()
        shift = register_shift_utility()

        expected_result_one = [
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-address', 'Roorkee,', 'Uttarakhand,',
            'India', 'Uttarakhand,', 'India', 'India',
            'volunteer-organization', '9999999999',
            'volunteer-email@systers.org', 'View'
        ]

        expected_result_two = [
            'volunteer-first-nameq', 'volunteer-last-nameq',
            'volunteer-addressq', 'Roorkee,', 'Uttarakhand,',
            'India', 'Uttarakhand,', 'India', 'India',
            'volunteer-organizationq', '9999999999',
            'volunteer-email2@systers.orgq', 'View'
        ]

        # volunteer_1 and volunteer_2 registered for job
        register_volunteer_for_shift_utility(shift, volunteer_1)
        register_volunteer_for_shift_utility(shift, volunteer_2)

        # search job
        search_page.navigate_to_volunteer_search_page()
        search_page.search_job_field("job")
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        # search incorrect job
        search_page.navigate_to_volunteer_search_page()
        search_page.search_job_field("wrong-job")
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

    def test_intersection_of_all_fields(self):
        """
        Test volunteer search form using multiple fields of the volunteers.
        """
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url

        country = create_country()
        state = create_state()
        city = create_city()
        credentials_1 = {
            'username': 'volunteer-username',
            'first_name': 'volunteer-first-name',
            'last_name': 'volunteer-last-name',
            'address': 'volunteer-address',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email@systers.org'
        }

        org_name = 'volunteer-organization'
        org_obj = create_organization_with_details(org_name)
        volunteer_1 = create_volunteer_with_details(credentials_1, org_obj)

        credentials_2 = {
            'username': 'volunteer-usernameq',
            'first_name': 'volunteer-first-nameq',
            'last_name': 'volunteer-last-nameq',
            'address': 'volunteer-addressq',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email2@systers.orgq'
        }

        org_name = 'volunteer-organizationq'
        org_obj = create_organization_with_details(org_name)
        volunteer_2 = create_volunteer_with_details(credentials_2, org_obj)

        search_page.navigate_to_volunteer_search_page()

        search_page.search_first_name_field('volunteer')
        search_page.search_last_name_field('volunteer')
        search_page.search_city_field('Roorkee')
        search_page.search_state_field('Uttarakhand')
        search_page.search_country_field('India')
        search_page.search_organization_field('volunteer')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)

        register_event_utility()
        register_job_utility()
        shift = register_shift_utility()
        register_volunteer_for_shift_utility(shift, volunteer_1)
        register_volunteer_for_shift_utility(shift, volunteer_2)

        expected_result_one = [
            'volunteer-first-name', 'volunteer-last-name',
            'volunteer-address', 'Roorkee,', 'Uttarakhand,',
            'India', 'Uttarakhand,', 'India', 'India',
            'volunteer-organization', '9999999999',
            'volunteer-email@systers.org', 'View'
        ]

        expected_result_two = [
            'volunteer-first-nameq', 'volunteer-last-nameq',
            'volunteer-addressq', 'Roorkee,', 'Uttarakhand,',
            'India', 'Uttarakhand,', 'India', 'India',
            'volunteer-organizationq', '9999999999',
            'volunteer-email2@systers.orgq', 'View'
        ]

        search_page.navigate_to_volunteer_search_page()
        search_page.search_first_name_field('volunteer')
        search_page.search_last_name_field('volunteer')
        search_page.search_city_field('Roorkee')
        search_page.search_state_field('Uttarakhand')
        search_page.search_country_field('India')
        search_page.search_organization_field('volunteer')
        search_page.search_event_field('event')
        search_page.search_job_field('job')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        search_page.search_first_name_field('volunteer')
        search_page.search_country_field('wrong-country')
        search_page.search_organization_field('org')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

        search_page.search_last_name_field('volunteer')
        search_page.search_city_field('wrong-city')
        search_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: //table//tbody',
                                search_page.get_search_results)

    def test_check_volunteer_reports(self):
        search_page = self.search_page
        search_page.live_server_url = self.live_server_url

        country = create_country()
        state = create_state()
        city = create_city()
        credentials_1 = {
            'username': 'volunteer-username',
            'first_name': 'volunteer-first-name',
            'last_name': 'VOLUNTEER-LAST-NAME',
            'address': 'volunteer-address',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email@systers.org'
        }
        org_name = 'volunteer-organization'
        org_obj = create_organization_with_details(org_name)
        vol = create_volunteer_with_details(credentials_1, org_obj)

        register_past_event_utility()
        register_past_job_utility()
        shift = register_past_shift_utility()
        start = datetime.time(hour=10, minute=0)
        end = datetime.time(hour=11, minute=0)
        logged_shift = log_hours_with_details(vol, shift, start, end)
        report = create_report_with_details(vol, logged_shift)
        report.confirm_status = 1
        report.save()

        search_page.navigate_to_volunteer_search_page()
        search_page.submit_form()

        self.assertEqual(
            search_page.element_by_xpath(self.elements.VIEW_REPORTS).text,
            'View'
        )
        search_page.element_by_xpath(self.elements.VIEW_REPORTS + '//a').click()
        self.assertEqual(
            search_page.remove_i18n(self.driver.current_url),
            self.live_server_url + PageUrls.volunteer_history_page + str(vol.id)
        )
        self.verify_report_details('1')

