from django.contrib.staticfiles.testing import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.volunteerSearchPage import VolunteerSearchPage

from shift.utils import (
    create_admin,
    create_volunteer_with_details
    )


class SearchVolunteer(LiveServerTestCase):
    '''
    SearchVolunteer class contains tests to check '/voluneer/search/' view.
    Choices of parameters contains
    - First Name
    - Last Name
    - City
    - State
    - Country
    - Organization
    Class contains 7 tests to check each parameter separately and also to check
    if a combination of parameters entered, then intersection of all results is
    obtained.
    '''

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.search_page = VolunteerSearchPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(SearchVolunteer, cls).setUpClass()

    def setUp(self):
        create_admin()
        self.login_admin()
        self.search_page.get_page(self.live_server_url, self.search_page.volunteer_search_page)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(SearchVolunteer, cls).tearDownClass()

    def login_admin(self):
        '''
        Utility function to login an admin user to perform all tests.
        '''
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({ 'username' : 'admin', 'password' : 'admin'})

    def test_volunteer_first_name_field(self):         
        credentials_1 = ['volunteer-username', 'VOLUNTEER-FIRST-NAME', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'volunteer-state',
                'volunteer-country', '9999999999', 'volunteer-email@systers.org',
                'volunteer-organization']

        v1 = create_volunteer_with_details(credentials_1)

        credentials_2 = ['volunteer-usernameq', 'volunteer-first-name', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq', 'volunteer-countryq',
                '9999999999', 'volunteer-email2@systers.orgq', 'volunteer-organizationq']

        v2 = create_volunteer_with_details(credentials_2)

        expected_result_one = credentials_1[1:-1]
        expected_result_two = credentials_2[1:-1]
        
        search_page = self.search_page
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

        with self.assertRaises(NoSuchElementException):
            search_results = search_page.get_search_results()

        search_page.search_first_name_field('volunteer-fail-test')
        search_page.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = search_page.get_search_results()

        search_page.search_first_name_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(),None)

    def test_volunteer_last_name_field(self):            
        credentials_1 = ['volunteer-username', 'volunteer-first-name', 'VOLUNTEER-LAST-NAME',
                'volunteer-address', 'volunteer-city', 'volunteer-state', 'volunteer-country',
                '9999999999', 'volunteer-email@systers.org','volunteer-organization']
        v1 = create_volunteer_with_details(credentials_1)

        credentials_2 = ['volunteer-usernameq', 'volunteer-first-nameq', 'volunteer-last-name',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq', 'volunteer-countryq',
                '9999999999', 'volunteer-email2@systers.orgq', 'volunteer-organizationq']
        v2 = create_volunteer_with_details(credentials_2)

        expected_result_one = credentials_1[1:-1]
        expected_result_two = credentials_2[1:-1]

        search_page = self.search_page
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

        with self.assertRaises(NoSuchElementException):
            search_results = search_page.get_search_results()

        search_page.search_last_name_field('volunteer-fail-test')
        search_page.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = search_page.get_search_results()

        search_page.search_last_name_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(),None)

    def test_volunteer_city_field(self):            
        credentials_1 = ['volunteer-username', 'volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'VOLUNTEER-CITY', 'volunteer-state', 'volunteer-country',
                '9999999999', 'volunteer-email@systers.org', 'volunteer-organization']

        v1 = create_volunteer_with_details(credentials_1)

        credentials_2 = ['volunteer-usernameq', 'volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-city', 'volunteer-stateq', 'volunteer-countryq',
                '9999999999', 'volunteer-email2@systers.orgq','volunteer-organizationq']

        v2 = create_volunteer_with_details(credentials_2)

        search_page = self.search_page

        expected_result_one = credentials_1[1:-1]
        expected_result_two = credentials_2[1:-1]

        search_page.search_city_field('volunteer')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 2)
        
        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        search_page.search_city_field('v')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        self.assertEqual(len(result), 2)

        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        search_page.search_city_field('vol-')
        search_page.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = search_page.get_search_results()

        search_page.search_city_field('volunteer-fail-test')
        search_page.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = search_page.get_search_results()

        search_page.search_city_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(),None)

    def test_volunteer_state_field(self):            
        credentials_1 = ['volunteer-username', 'volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'VOLUNTEER-STATE', 'volunteer-country',
                '9999999999', 'volunteer-email@systers.org', 'volunteer-organization']

        v1 = create_volunteer_with_details(credentials_1)

        credentials_2 = ['volunteer-usernameq', 'volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-state', 'volunteer-countryq',
                '9999999999', 'volunteer-email2@systers.orgq', 'volunteer-organizationq']

        v2 = create_volunteer_with_details(credentials_2)

        search_page = self.search_page

        expected_result_one = credentials_1[1:-1]
        expected_result_two = credentials_2[1:-1]

        search_page.search_state_field('volunteer')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)

        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_two in result)
        self.assertTrue(expected_result_one in result)

        search_page.search_state_field('v')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        
        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_two in result)
        self.assertTrue(expected_result_one in result)

        search_page.search_state_field('vol-')
        search_page.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = search_page.get_search_results()

        search_page.search_state_field('volunteer-fail-test')
        search_page.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = search_page.get_search_results()

        search_page.search_state_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(), None)

    def test_volunteer_country_field(self):            
        credentials_1 = ['volunteer-username', 'volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'volunteer-state', 'VOLUNTEER-COUNTRY',
                '9999999999', 'volunteer-email@systers.org', 'volunteer-organization']

        v1 = create_volunteer_with_details(credentials_1)

        credentials_2 = ['volunteer-usernameq', 'volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq', 'volunteer-country',
                '9999999999', 'volunteer-email2@systers.orgq', 'volunteer-organizationq']

        v2 = create_volunteer_with_details(credentials_2)

        search_page = self.search_page

        expected_result_one = credentials_1[1:-1]
        expected_result_two = credentials_2[1:-1]

        search_page.search_country_field('volunteer')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)
        
        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_two in result)
        self.assertTrue(expected_result_one in result)

        search_page.search_country_field('v')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)

        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_two in result)
        self.assertTrue(expected_result_one in result)

        search_page.search_country_field('vol-')
        search_page.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = search_page.get_search_results()

        search_page.search_country_field('volunteer-fail-test')
        search_page.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = search_page.get_search_results()

        search_page.search_country_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(), None)

    def test_volunteer_organization_field(self):            
        credentials_1 = ['volunteer-username', 'volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'volunteer-state', 'volunteer-country',
                '9999999999', 'volunteer-email@systers.org']

        v1 = create_volunteer_with_details(credentials_1)

        credentials_2 = ['volunteer-usernameq', 'volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq', 'volunteer-countryq',
                '9999999999', 'volunteer-email2@systers.orgq']

        v2 = create_volunteer_with_details(credentials_2)

        v2.unlisted_organization="volunteer-organization"
        v1.unlisted_organization="VOLUNTEER-ORGANIZATION"
        v1.save()
        v2.save()

        search_page = self.search_page

        expected_result_one = ['volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq',
                'volunteer-countryq', 'volunteer-organization', '9999999999',
                'volunteer-email2@systers.orgq']

        expected_result_two = ['volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'volunteer-state',
                'volunteer-country', 'VOLUNTEER-ORGANIZATION', '9999999999',
                'volunteer-email@systers.org']

        search_page.search_organization_field('volunteer')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)

        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        search_page.search_organization_field('v')
        search_page.submit_form()
        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)

        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        search_page.search_organization_field('vol-')
        search_page.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = search_page.get_search_results()

        search_page.search_organization_field('volunteer-fail-test')
        search_page.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = search_page.get_search_results()

        search_page.search_organization_field('!@#$%^&*()_')
        search_page.submit_form()
        self.assertNotEqual(search_page.get_help_block(),None)

    def test_intersection_of_all_fields(self):            
        credentials_1 = ['volunteer-username', 'volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'volunteer-state', 'volunteer-country',
                '9999999999', 'volunteer-email@systers.org']

        v1 = create_volunteer_with_details(credentials_1)

        credentials_2 = ['volunteer-usernameq', 'volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq', 'volunteer-countryq',
                '9999999999', 'volunteer-email2@systers.orgq']

        v2 = create_volunteer_with_details(credentials_2)

        v2.unlisted_organization="volunteer-organization"
        v1.unlisted_organization="VOLUNTEER-ORGANIZATION"
        v1.save()
        v2.save()

        search_page = self.search_page

        search_page.search_first_name_field('volunteer')
        search_page.search_last_name_field('volunteer')
        search_page.search_city_field('volunteer')
        search_page.search_state_field('volunteer')
        search_page.search_country_field('volunteer')
        search_page.search_organization_field('volunteer')
        search_page.submit_form()

        search_results = search_page.get_search_results()
        result = search_page.get_results_list(search_results)

        expected_result_one = ['volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq',
                'volunteer-countryq', 'volunteer-organization', '9999999999',
                'volunteer-email2@systers.orgq']

        expected_result_two = ['volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'volunteer-state',
                'volunteer-country', 'VOLUNTEER-ORGANIZATION', '9999999999',
                'volunteer-email@systers.org']

        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        search_page.search_first_name_field('volunteer')
        search_page.search_country_field('wrong-country')
        search_page.search_organization_field('org')
        search_page.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = search_page.get_search_results()
        
        search_page.search_last_name_field('volunteer')
        search_page.search_city_field('wrong-city')
        search_page.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = search_page.get_search_results()
