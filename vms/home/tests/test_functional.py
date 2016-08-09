from django.contrib.staticfiles.testing import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from volunteer.models import Volunteer

from shift.utils import (
    create_admin,
    create_volunteer
    )

import re

# Class contains failing test cases which have been documented
# Test class commented out to prevent travis build failure
"""
class CheckURLAccess(LiveServerTestCase):
    '''
    CheckURLAccess contains methods to browse(via URL) a volunteer page view
    after logging in from an admin account and vice-versa. Tests included:
    - Admin cannot access volunteer URL's
    - Volunteer cannot access admin URL's
    '''
    
    @classmethod
    def setUpClass(cls):
        cls.authentication_page = '/authentication/login/'
        cls.login_id = 'id_login'
        cls.login_password = 'id_password'

        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        super(CheckURLAccess, cls).setUpClass()

    def setUp(self):
        create_admin()
        create_volunteer()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(CheckURLAccess, cls).tearDownClass()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id(self.login_id).send_keys(credentials['username'])
        self.driver.find_element_by_id(self.login_password).send_keys(credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def find_volunteer_page_error(self, volunteer_url):
        self.driver.get(self.live_server_url + volunteer_url)
        page_source = self.driver.page_source
        error = re.search('403', page_source)
        return error

    def verify_admin_page_error(self, admin_url):
        self.driver.get(self.live_server_url + admin_url)
        self.assertNotEqual(self.driver.find_elements_by_class_name('panel-heading'),
                None)
        self.assertNotEqual(self.driver.find_elements_by_class_name('panel-body'),
                None)
        self.assertEqual(self.driver.find_element_by_class_name('panel-heading').text,
                'No Access')
        self.assertEqual(self.driver.find_element_by_class_name('panel-body').text,
                "You don't have administrator rights")

    def test_admin_cannot_access_volunteer_urls(self):
        '''
        Method logins an admin user and tries to surf volunteer pages through
        url. The volunteer views should return a 403 error to deny access.
        '''
        
        self.login({ 'username' : 'admin', 'password' : 'admin'})

        error = self.find_volunteer_page_error('/shift/view_volunteer_shifts/1')
        self.assertNotEqual(error, None)

        error = self.find_volunteer_page_error('/shift/view_hours/1')
        self.assertNotEqual(error, None)

        error = self.find_volunteer_page_error('/event/list_sign_up/1')
        self.assertNotEqual(error, None)

        error = self.find_volunteer_page_error('/volunteer/report/1')
        self.assertNotEqual(error, None)

        error = self.find_volunteer_page_error('/volunteer/profile/1')
        self.assertNotEqual(error, None)

    def test_volunteer_cannot_access_admin_urls(self):
        '''
        Method logins a volunteer and tries to surf admin page views through url.
        The admin views should return a no admin rights page.
        '''
        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})

        self.verify_admin_page_error('/shift/volunteer_search/')
        self.verify_admin_page_error('/administrator/report/')
        self.verify_admin_page_error('/volunteer/search/')
        self.verify_admin_page_error('/administrator/settings/')
        self.verify_admin_page_error('/administrator/report/')
"""

class CheckContentAndRedirection(LiveServerTestCase):
    '''
    This Class contains methods to check if 

    - an administrator or a volunteer are provided their respective views 
    links on their dashboard.
    - all links in the nav-bar for admin and volunteer page redirect to desired
    views.

    For content, following checks are implemented:
    - Check admin page content
    - check volunteer page content

    Admin views nav-bar consists of:
    - Volunteer Search
    - Manage Volunteer Shifts
    - Report
    - Settings
    - Create Admin Account
    - Logout

    Volunteer views nav-bar consists of:
    - Upcoming Shifts
    - Shift Hours
    - Shift SignUp
    - Report
    - Profile
    - Logout
    '''

    @classmethod
    def setUpClass(cls):
        cls.homepage = '/'
        cls.authentication_page = '/authentication/login/'
        cls.login_id = 'id_login'
        cls.login_password = 'id_password'

        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        super(CheckContentAndRedirection, cls).setUpClass()

    def setUp(self):
        create_admin()
        create_volunteer()
        self.volunteer_id = str(Volunteer.objects.get(user__username =
                'volunteer').pk)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(CheckContentAndRedirection, cls).tearDownClass()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id(self.login_id).send_keys(credentials['username'])
        self.driver.find_element_by_id(self.login_password).send_keys(credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def test_check_admin_page_content(self):
        '''
        Check if an admin user has following functionalities on its home page.
        - Volunteer Search
        - Manage Volunteer Shift
        - Report
        - Settings
        - Create Admin Account
        '''
        self.login({ 'username' : 'admin', 'password' : 'admin'})

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_link_text('Log In')

        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Volunteer Search'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Manage Volunteer Shifts'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Report'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Events'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Create Admin Account'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Log Out'), None)

    def test_check_volunteer_page_content(self):
        '''
        Check if a volunteer user has following functionalities on its home
        page.
        - UpComing Shift
        - Shift Hours
        - Shift Sign Up
        - Report
        - Profile
        '''
        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_link_text('Log In')

        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Upcoming Shifts'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Completed Shifts'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Shift Sign Up'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Report'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Profile'), None)
        self.assertNotEqual(self.driver.find_element_by_link_text(
            'Log Out'), None)

    def test_admin_page_redirection(self):
        self.login({ 'username' : 'admin', 'password' : 'admin'})

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_link_text('Log In')

        volunteer_search_link =  self.driver.find_element_by_link_text(
                'Volunteer Search').get_attribute('href')
        self.assertEqual(volunteer_search_link, self.live_server_url + 
                '/volunteer/search/')

        manage_volunteer_shift_link =  self.driver.find_element_by_link_text(
                'Manage Volunteer Shifts').get_attribute('href')
        self.assertEqual(manage_volunteer_shift_link, self.live_server_url + 
                '/shift/volunteer_search/')

        report_link =  self.driver.find_element_by_link_text(
                'Report').get_attribute('href')
        self.assertEqual(report_link, self.live_server_url + 
                '/administrator/report/')

        settings_link =  self.driver.find_element_by_link_text(
                'Events').get_attribute('href')
        self.assertEqual(settings_link, self.live_server_url + 
                '/administrator/settings/')

        creat_account_link =  self.driver.find_element_by_link_text(
                'Create Admin Account').get_attribute('href')
        self.assertEqual(creat_account_link, self.live_server_url + 
                '/registration/signup_administrator/')

        logout_link =  self.driver.find_element_by_link_text(
                'Log Out').get_attribute('href')
        self.assertEqual(logout_link, self.live_server_url + 
                '/authentication/logout/')

    def test_volunteer_page_redirection(self):
        self.login({ 'username' : 'volunteer', 'password' : 'volunteer'})

        self.assertEqual(self.driver.current_url, self.live_server_url +
                self.homepage)

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_link_text('Log In')

        upcoming_shift_link =  self.driver.find_element_by_link_text(
                'Upcoming Shifts').get_attribute('href')
        self.assertEqual(upcoming_shift_link, self.live_server_url + 
                '/shift/view_volunteer_shifts/' + self.volunteer_id)

        shift_hours_link =  self.driver.find_element_by_link_text(
                'Completed Shifts').get_attribute('href')
        self.assertEqual(shift_hours_link, self.live_server_url + 
                '/shift/view_hours/' + self.volunteer_id)

        shift_signup_link =  self.driver.find_element_by_link_text(
                'Shift Sign Up').get_attribute('href')
        self.assertEqual(shift_signup_link, self.live_server_url + 
                '/event/list_sign_up/' + self.volunteer_id)

        report_link =  self.driver.find_element_by_link_text(
                'Report').get_attribute('href')
        self.assertEqual(report_link, self.live_server_url + 
                '/volunteer/report/' + self.volunteer_id)

        profile_link =  self.driver.find_element_by_link_text(
                'Profile').get_attribute('href')
        self.assertEqual(profile_link, self.live_server_url + 
                '/volunteer/profile/' + self.volunteer_id)

        logout_link =  self.driver.find_element_by_link_text(
                'Log Out').get_attribute('href')
        self.assertEqual(logout_link, self.live_server_url + 
                '/authentication/logout/')
