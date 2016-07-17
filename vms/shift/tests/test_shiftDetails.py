from django.contrib.staticfiles.testing import LiveServerTestCase
from shift.models import VolunteerShift

from shift.utils import (
    create_volunteer_with_details,
    create_admin,
    create_event_with_details,
    create_job_with_details,
    create_shift_with_details,
    log_hours_with_details,
    register_volunteer_for_shift_utility
    )

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class ShiftDetails(LiveServerTestCase):
    '''
    Contains Tests for View Shift Details Page

    Status of shift page is checked for following cases -
    - No Volunteer is registered
    - Volunteer registered but no hours logged
    - Volunteer with logged shift hours
    '''

    @classmethod
    def setUpClass(cls):
        cls.homepage = '/'
        cls.authentication_page = '/authentication/login/'
        cls.shift_list_page = '/shift/list_jobs/'

        cls.vol_email = '//table[2]//tr//td[9]'
        cls.shift_max_vol = '//table[1]//tr//td[9]'
        cls.shift_job_path = '//table[1]//tr//td[1]'
        cls.shift_date_path = '//table[1]//tr//td[3]'
        cls.shift_stime_path = '//table[1]//tr//td[4]'
        cls.shift_etime_path = '//table[1]//tr//td[5]'
        cls.logged_volunteer = '//table[3]//tr//td[1]'
        cls.logged_stime_path = '//table[3]//tr//td[4]'
        cls.logged_etime_path = '//table[3]//tr//td[5]'

        cls.view_shift = '//table//tbody//tr[1]/td[5]//a'
        cls.view_details = '//table//tbody//tr[1]//td[7]'
        cls.logged_volunteer_list = '//table[3]//tbody//tr'

        cls.registered_volunteer_name = '//table[2]//tr//td[1]'
        cls.registered_volunteer_list = '//table[2]//tbody//tr'

        cls.volunteer_detail = ['volunteer-usernameq', 'Michael', 'Reed',
                'address', 'city', 'state', 'country', '9999999999',
                'volunteer@volunteer.com', 'organization']

        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        super(ShiftDetails, cls).setUpClass()

    def setUp(self):
        self.admin = create_admin()
        self.login_admin()
        self.shift = self.register_dataset()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(ShiftDetails, cls).tearDownClass()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys(credentials['username'])
        self.driver.find_element_by_id('id_password').send_keys(credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def login_admin(self):
        self.login({'username': 'admin', 'password': 'admin'})

    def register_dataset(self):
        e1 = create_event_with_details(['event', '2017-06-15', '2017-06-17'])
        j1 = create_job_with_details(['job', '2017-06-15', '2017-06-15', 'job description', e1])
        s1 = create_shift_with_details(['2017-06-15', '09:00', '15:00', '6', j1])
        return s1

    def navigate_to_shift_details_view(self):
        self.driver.get(self.live_server_url + self.shift_list_page)
        self.driver.find_element_by_xpath(self.view_shift).click()
        self.assertEqual(self.driver.find_element_by_xpath(
            self.view_details).text, 'View')
        self.driver.find_element_by_xpath(self.view_details + '//a').click()

    def test_view_with_unregistered_volunteers(self):
        self.navigate_to_shift_details_view()

        # verify details and slots remaining
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_job_path).text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_date_path).text, 'June 15, 2017')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_max_vol).text, '6')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_stime_path).text, '9 a.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_etime_path).text, '3 p.m.')

        # verify that there are no registered shifts or logged hours
        self.assertEqual(
            self.driver.find_element_by_class_name('alert-success').text,
            'There are currently no volunteers assigned to this shift. Please assign volunteers to view more details')

    def test_view_with_only_registered_volunteers(self):

        volunteer = create_volunteer_with_details(self.volunteer_detail)
        volunteer_shift = register_volunteer_for_shift_utility(
            self.shift, volunteer)
        self.navigate_to_shift_details_view()

        # verify that the shift slot is decreased by 1
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_job_path).text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_max_vol).text, '5')

        # verify that assigned volunteers shows up but no logged hours yet
        self.assertEqual(
            len(self.driver.find_elements_by_xpath(self.registered_volunteer_list)), 1)
        self.assertEqual(self.driver.find_element_by_xpath(
            self.registered_volunteer_name).text, 'Michael')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.vol_email).text, 'volunteer@volunteer.com')
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-success').text, 'There are no logged hours at the moment')

    def test_view_with_logged_hours(self):
        volunteer = create_volunteer_with_details(self.volunteer_detail)
        log_hours_with_details(volunteer, self.shift, '13:00', '14:00')
        self.navigate_to_shift_details_view()

        # verify that the shift slot is decreased by 1
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_job_path).text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_max_vol).text, '5')

        # verify that assigned volunteers shows up
        self.assertEqual(
            len(self.driver.find_elements_by_xpath(self.registered_volunteer_list)), 1)
        self.assertEqual(self.driver.find_element_by_xpath(
            self.vol_email).text, 'volunteer@volunteer.com')

        # verify that hours are logged by volunteer
        self.assertEqual(
            len(self.driver.find_elements_by_xpath(self.logged_volunteer_list)), 1)
        self.assertEqual(self.driver.find_element_by_xpath(
            self.registered_volunteer_name).text, 'Michael')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.logged_stime_path).text, '1 p.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.logged_etime_path).text, '2 p.m.')
