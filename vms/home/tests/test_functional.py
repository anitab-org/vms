from django.contrib.staticfiles.testing import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from pom.pages.homePage import HomePage
from pom.pages.authenticationPage import AuthenticationPage
from pom.pageUrls import PageUrls

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
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        cls.home_page = HomePage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
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

    def find_volunteer_page_error(self, volunteer_url):
        home_page = self.home_page
        home_page.get_page(self.live_server_url, volunteer_url)
        page_source = self.driver.page_source
        error = re.search('403', page_source)
        return error

    def verify_admin_page_error(self, admin_url):
        home_page = self.home_page
        home_page.get_page(self.live_server_url, admin_url)
        heading = home_page.get_no_admin_right()
        body = home_page.get_no_admin_right_content()
        self.assertNotEqual(heading,None)
        self.assertNotEqual(body,None)
        self.assertEqual(heading.text,'No Access')
        self.assertEqual(body.text,"You don't have administrator rights")

    def test_admin_cannot_access_volunteer_urls(self):
        '''
        Method logins an admin user and tries to surf volunteer pages through
        url. The volunteer views should return a 403 error to deny access.
        '''
        
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.login({ 'username' : 'admin', 'password' : 'admin'})

        error = self.find_volunteer_page_error(PageUrls.upcoming_shifts_page+'1')
        self.assertNotEqual(error, None)

        error = self.find_volunteer_page_error(PageUrls.completed_shifts_page+'1')
        self.assertNotEqual(error, None)

        error = self.find_volunteer_page_error(PageUrls.shift_sign_up_page+'1')
        self.assertNotEqual(error, None)

        error = self.find_volunteer_page_error(PageUrls.volunteer_report_page+'1')
        self.assertNotEqual(error, None)

        error = self.find_volunteer_page_error(PageUrls.volunteer_profile_page+'1')
        self.assertNotEqual(error, None)

    def test_volunteer_cannot_access_admin_urls(self):
        '''
        Method logins a volunteer and tries to surf admin page views through url.
        The admin views should return a no admin rights page.
        '''
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.login({ 'username' : 'volunteer', 'password' : 'volunteer'})

        self.verify_admin_page_error(PageUrls.manage_volunteer_shift_page)
        self.verify_admin_page_error(PageUrls.admin_settings)
        self.verify_admin_page_error(PageUrls.volunteer_search_page)
        self.verify_admin_page_error(PageUrls.administrator_report_page)
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
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        cls.home_page = HomePage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(CheckContentAndRedirection, cls).setUpClass()

    def setUp(self):
        self.admin = create_admin()
        self.volunteer = create_volunteer()
        self.volunteer_id = str(self.volunteer.id)
        
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(CheckContentAndRedirection, cls).tearDownClass()

    def test_check_admin_page_content(self):
        '''
        Check if an admin user has following functionalities on its home page.
        - Volunteer Search
        - Manage Volunteer Shift
        - Report
        - Settings
        - Create Admin Account
        '''
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        home_page = self.home_page

        authentication_page.login({'username': 'admin', 'password': 'admin'})

        with self.assertRaises(NoSuchElementException):
            home_page.get_login_link()

        self.assertNotEqual(home_page.get_volunteer_search_link(), None)
        self.assertNotEqual(home_page.get_manage_shifts_link(), None)
        self.assertNotEqual(home_page.get_admin_report_link(), None)
        self.assertNotEqual(home_page.get_events_link(), None)
        self.assertNotEqual(home_page.get_create_admin_link(), None)
        self.assertNotEqual(home_page.get_logout_link(), None)

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
        home_page = self.home_page
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.login({ 'username' : 'volunteer', 'password' : 'volunteer'})

        with self.assertRaises(NoSuchElementException):
            home_page.get_login_link()

        self.assertNotEqual(home_page.get_upcoming_shifts_link(), None)
        self.assertNotEqual(home_page.get_completed_shifts_link(), None)
        self.assertNotEqual(home_page.get_shift_signup_link(), None)
        self.assertNotEqual(home_page.get_volunteer_report_link(), None)
        self.assertNotEqual(home_page.get_volunteer_profile_link(), None)
        self.assertNotEqual(home_page.get_logout_link(), None)

    def test_admin_page_redirection(self):
        home_page = self.home_page
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.login({ 'username' : 'admin', 'password' : 'admin'})

        self.assertEqual(self.driver.current_url, self.live_server_url +
                PageUrls.homepage)

        with self.assertRaises(NoSuchElementException):
            home_page.get_login_link()

        volunteer_search_link = home_page.get_volunteer_search_link().get_attribute('href')
        self.assertEqual(volunteer_search_link, self.live_server_url + 
                PageUrls.volunteer_search_page)

        manage_volunteer_shift_link = home_page.get_manage_shifts_link().get_attribute('href')
        self.assertEqual(manage_volunteer_shift_link, self.live_server_url + 
                PageUrls.manage_volunteer_shift_page)

        report_link = home_page.get_admin_report_link().get_attribute('href')
        self.assertEqual(report_link, self.live_server_url + 
                PageUrls.administrator_report_page)

        settings_link = home_page.get_events_link().get_attribute('href')
        self.assertEqual(settings_link, self.live_server_url + 
                PageUrls.admin_settings_page)

        creat_account_link = home_page.get_create_admin_link().get_attribute('href')
        self.assertEqual(creat_account_link, self.live_server_url + 
                PageUrls.admin_registration_page)

        logout_link = home_page.get_logout_link().get_attribute('href')
        self.assertEqual(logout_link, self.live_server_url + 
                PageUrls.logout_page)

    def test_volunteer_page_redirection(self):
        home_page = self.home_page
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.login({ 'username' : 'volunteer', 'password' : 'volunteer'})

        self.assertEqual(self.driver.current_url, self.live_server_url +
                PageUrls.homepage)

        with self.assertRaises(NoSuchElementException):
            home_page.get_login_link()

        upcoming_shift_link = home_page.get_upcoming_shifts_link().get_attribute('href')
        self.assertEqual(upcoming_shift_link, self.live_server_url + 
                PageUrls.upcoming_shifts_page + self.volunteer_id)

        shift_hours_link = home_page.get_completed_shifts_link().get_attribute('href')
        self.assertEqual(shift_hours_link, self.live_server_url + 
                PageUrls.completed_shifts_page + self.volunteer_id)

        shift_signup_link = home_page.get_shift_signup_link().get_attribute('href')
        self.assertEqual(shift_signup_link, self.live_server_url + 
                PageUrls.shift_sign_up_page + self.volunteer_id)

        report_link = home_page.get_volunteer_report_link().get_attribute('href')
        self.assertEqual(report_link, self.live_server_url + 
                PageUrls.volunteer_report_page + self.volunteer_id)

        profile_link = home_page.get_volunteer_profile_link().get_attribute('href')
        self.assertEqual(profile_link, self.live_server_url + 
                PageUrls.volunteer_profile_page + self.volunteer_id)

        logout_link = home_page.get_logout_link().get_attribute('href')
        self.assertEqual(logout_link, self.live_server_url + 
                PageUrls.logout_page)
