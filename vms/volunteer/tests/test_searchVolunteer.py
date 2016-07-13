from django.contrib.staticfiles.testing import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

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
        cls.homepage = '/'
        cls.authentication_page = '/authentication/login/'
        cls.volunteer_search = '/volunteer/search/'
        cls.first_name_field = ".form-control[name='first_name']"
        cls.last_name_field = ".form-control[name='last_name']"
        cls.city_field = ".form-control[name='city']"
        cls.state_field = ".form-control[name='state']"
        cls.country_field = ".form-control[name='country']"
        cls.org_field = ".form-control[name='organization']"

        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        super(SearchVolunteer, cls).setUpClass()

    def setUp(self):
        create_admin()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(SearchVolunteer, cls).tearDownClass()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys(credentials['username'])
        self.driver.find_element_by_id('id_password').send_keys(credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def login_admin(self):
        '''
        Utility function to login an admin user to perform all tests.
        '''
        self.login({ 'username' : 'admin', 'password' : 'admin'})
        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

    def submit_form(self):
        self.driver.find_element_by_class_name('btn').click()

    def search_first_name_field(self, search_text):
        self.driver.find_element_by_css_selector(self.first_name_field).clear()
        self.driver.find_element_by_css_selector(self.first_name_field).send_keys(search_text)

    def search_last_name_field(self, search_text):
        self.driver.find_element_by_css_selector(self.last_name_field).clear()
        self.driver.find_element_by_css_selector(self.last_name_field).send_keys(search_text)

    def search_city_field(self, search_text):
        self.driver.find_element_by_css_selector(self.city_field).clear()
        self.driver.find_element_by_css_selector(self.city_field).send_keys(search_text)

    def search_state_field(self, search_text):
        self.driver.find_element_by_css_selector(self.state_field).clear()
        self.driver.find_element_by_css_selector(self.state_field).send_keys(search_text)

    def search_country_field(self, search_text):
        self.driver.find_element_by_css_selector(self.country_field).clear()
        self.driver.find_element_by_css_selector(self.country_field).send_keys(search_text)

    def search_organization_field(self, search_text):
        self.driver.find_element_by_css_selector(self.org_field).clear()
        self.driver.find_element_by_css_selector(self.org_field).send_keys(search_text)

    def get_search_results(self):
        search_results = self.driver.find_element_by_xpath('//table//tbody')
        return search_results

    def get_results_list(self, search_results):

        result = []
        for tr in search_results.find_elements_by_tag_name('tr'):
            row = tr.text.split()
            result.append(row)

        return result

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

        self.login_admin()
        self.driver.get(self.live_server_url + self.volunteer_search)

        expected_result_one = credentials_1[1:-1]
        expected_result_two = credentials_2[1:-1]
        
        self.search_first_name_field('volunteer')
        self.submit_form()
        search_results = self.get_search_results()
        result = self.get_results_list(search_results)
        self.assertEqual(len(result), 2)

        self.assertTrue(expected_result_two in result)
        self.assertTrue(expected_result_one in result)

        self.search_first_name_field('e')
        self.submit_form()
        search_results = self.get_search_results()
        result = self.get_results_list(search_results)
        self.assertEqual(len(result), 2)

        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        self.search_first_name_field('vol-')
        self.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = self.get_search_results()

        self.search_first_name_field('volunteer-fail-test')
        self.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = self.get_search_results()

        self.search_first_name_field('!@#$%^&*()_')
        self.submit_form()
        self.assertNotEqual(self.driver.find_element_by_class_name('help-block'),
                None)

    def test_volunteer_last_name_field(self):            
        credentials_1 = ['volunteer-username', 'volunteer-first-name', 'VOLUNTEER-LAST-NAME',
                'volunteer-address', 'volunteer-city', 'volunteer-state', 'volunteer-country',
                '9999999999', 'volunteer-email@systers.org','volunteer-organization']
        v1 = create_volunteer_with_details(credentials_1)

        credentials_2 = ['volunteer-usernameq', 'volunteer-first-nameq', 'volunteer-last-name',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq', 'volunteer-countryq',
                '9999999999', 'volunteer-email2@systers.orgq', 'volunteer-organizationq']
        v2 = create_volunteer_with_details(credentials_2)

        self.login_admin()
        self.driver.get(self.live_server_url + self.volunteer_search)

        expected_result_one = credentials_1[1:-1]
        expected_result_two = credentials_2[1:-1]

        self.search_last_name_field('volunteer')
        self.submit_form()

        search_results = self.get_search_results()
        result = self.get_results_list(search_results)

        self.assertTrue(expected_result_two in result)
        self.assertTrue(expected_result_one in result)

        self.search_last_name_field('v')
        self.submit_form()
        search_results = self.get_search_results()
        result = self.get_results_list(search_results)
        self.assertEqual(len(result), 2)

        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        self.search_last_name_field('vol-')
        self.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = self.get_search_results()

        self.search_last_name_field('volunteer-fail-test')
        self.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = self.get_search_results()

        self.search_last_name_field('!@#$%^&*()_')
        self.submit_form()
        self.assertNotEqual(self.driver.find_element_by_class_name('help-block'),
                None)

    def test_volunteer_city_field(self):            
        credentials_1 = ['volunteer-username', 'volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'VOLUNTEER-CITY', 'volunteer-state', 'volunteer-country',
                '9999999999', 'volunteer-email@systers.org', 'volunteer-organization']

        v1 = create_volunteer_with_details(credentials_1)

        credentials_2 = ['volunteer-usernameq', 'volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-city', 'volunteer-stateq', 'volunteer-countryq',
                '9999999999', 'volunteer-email2@systers.orgq','volunteer-organizationq']

        v2 = create_volunteer_with_details(credentials_2)

        self.login_admin()
        self.driver.get(self.live_server_url + self.volunteer_search)

        expected_result_one = credentials_1[1:-1]
        expected_result_two = credentials_2[1:-1]

        self.search_city_field('volunteer')
        self.submit_form()
        search_results = self.get_search_results()
        result = self.get_results_list(search_results)
        self.assertEqual(len(result), 2)
        
        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        self.search_city_field('v')
        self.submit_form()
        search_results = self.get_search_results()
        result = self.get_results_list(search_results)
        self.assertEqual(len(result), 2)

        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        self.search_city_field('vol-')
        self.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = self.get_search_results()

        self.search_city_field('volunteer-fail-test')
        self.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = self.get_search_results()

        self.search_city_field('!@#$%^&*()_')
        self.submit_form()
        self.assertNotEqual(self.driver.find_element_by_class_name('help-block'),
                None)

    def test_volunteer_state_field(self):            
        credentials_1 = ['volunteer-username', 'volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'VOLUNTEER-STATE', 'volunteer-country',
                '9999999999', 'volunteer-email@systers.org', 'volunteer-organization']

        v1 = create_volunteer_with_details(credentials_1)

        credentials_2 = ['volunteer-usernameq', 'volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-state', 'volunteer-countryq',
                '9999999999', 'volunteer-email2@systers.orgq', 'volunteer-organizationq']

        v2 = create_volunteer_with_details(credentials_2)

        self.login_admin()
        self.driver.get(self.live_server_url + self.volunteer_search)

        expected_result_one = credentials_1[1:-1]
        expected_result_two = credentials_2[1:-1]

        self.search_state_field('volunteer')
        self.submit_form()
        search_results = self.get_search_results()
        result = self.get_results_list(search_results)

        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_two in result)
        self.assertTrue(expected_result_one in result)

        self.search_state_field('v')
        self.submit_form()
        search_results = self.get_search_results()
        result = self.get_results_list(search_results)
        
        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_two in result)
        self.assertTrue(expected_result_one in result)

        self.search_state_field('vol-')
        self.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = self.get_search_results()

        self.search_state_field('volunteer-fail-test')
        self.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = self.get_search_results()

        self.search_state_field('!@#$%^&*()_')
        self.submit_form()
        self.assertNotEqual(self.driver.find_element_by_class_name('help-block'),
                None)

    def test_volunteer_country_field(self):            
        credentials_1 = ['volunteer-username', 'volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'volunteer-state', 'VOLUNTEER-COUNTRY',
                '9999999999', 'volunteer-email@systers.org', 'volunteer-organization']

        v1 = create_volunteer_with_details(credentials_1)

        credentials_2 = ['volunteer-usernameq', 'volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq', 'volunteer-country',
                '9999999999', 'volunteer-email2@systers.orgq', 'volunteer-organizationq']

        v2 = create_volunteer_with_details(credentials_2)

        self.login_admin()
        self.driver.get(self.live_server_url + self.volunteer_search)

        expected_result_one = credentials_1[1:-1]
        expected_result_two = credentials_2[1:-1]

        self.search_country_field('volunteer')
        self.submit_form()
        search_results = self.get_search_results()
        result = self.get_results_list(search_results)
        
        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_two in result)
        self.assertTrue(expected_result_one in result)

        self.search_country_field('v')
        self.submit_form()
        search_results = self.get_search_results()
        result = self.get_results_list(search_results)

        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_two in result)
        self.assertTrue(expected_result_one in result)

        self.search_country_field('vol-')
        self.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = self.get_search_results()

        self.search_country_field('volunteer-fail-test')
        self.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = self.get_search_results()

        self.search_country_field('!@#$%^&*()_')
        self.submit_form()
        self.assertNotEqual(self.driver.find_element_by_class_name('help-block'),
                None)

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

        self.login_admin()
        self.driver.get(self.live_server_url + self.volunteer_search)

        expected_result_one = ['volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-cityq', 'volunteer-stateq',
                'volunteer-countryq', 'volunteer-organization', '9999999999',
                'volunteer-email2@systers.orgq']

        expected_result_two = ['volunteer-first-name', 'volunteer-last-name',
                'volunteer-address', 'volunteer-city', 'volunteer-state',
                'volunteer-country', 'VOLUNTEER-ORGANIZATION', '9999999999',
                'volunteer-email@systers.org']

        self.search_organization_field('volunteer')
        self.submit_form()
        search_results = self.get_search_results()
        result = self.get_results_list(search_results)

        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        self.search_organization_field('v')
        self.submit_form()
        search_results = self.get_search_results()
        result = self.get_results_list(search_results)

        self.assertEqual(len(result), 2)
        self.assertTrue(expected_result_one in result)
        self.assertTrue(expected_result_two in result)

        self.search_organization_field('vol-')
        self.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = self.get_search_results()

        self.search_organization_field('volunteer-fail-test')
        self.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = self.get_search_results()

        self.search_organization_field('!@#$%^&*()_')
        self.submit_form()
        self.assertNotEqual(self.driver.find_element_by_class_name('help-block'),
                None)

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

        self.login_admin()
        self.driver.get(self.live_server_url + self.volunteer_search)

        self.search_first_name_field('volunteer')
        self.search_last_name_field('volunteer')
        self.search_city_field('volunteer')
        self.search_state_field('volunteer')
        self.search_country_field('volunteer')
        self.search_organization_field('volunteer')
        self.submit_form()

        search_results = self.get_search_results()
        result = self.get_results_list(search_results)

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

        self.search_first_name_field('volunteer')
        self.search_country_field('wrong-country')
        self.search_organization_field('org')
        self.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = self.get_search_results()
        
        self.search_last_name_field('volunteer')
        self.search_city_field('wrong-city')
        self.submit_form()

        with self.assertRaises(NoSuchElementException):
            search_results = self.get_search_results()
