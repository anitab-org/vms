from django.contrib.staticfiles.testing import LiveServerTestCase

from shift.utils import (
    create_volunteer,
    create_event_with_details,
    create_job_with_details,
    create_shift_with_details,
    create_volunteer_with_details,
    register_volunteer_for_shift_utility
    )

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import re

class ViewVolunteerShift(LiveServerTestCase):
    '''
    '''
    @classmethod
    def setUpClass(cls):
        cls.homepage = '/'
        cls.authentication_page = '/authentication/login/'
        cls.view_shift_page = '/shift/view_volunteer_shifts/'     
        
        cls.shift_job_path = '//table//tbody//tr[1]//td[1]'
        cls.shift_date_path = '//table//tbody//tr[1]//td[2]'
        cls.shift_stime_path = '//table//tbody//tr[1]//td[3]'
        cls.shift_etime_path = '//table//tbody//tr[1]//td[4]'
        cls.shift_cancel_path = '//table//tbody//tr[1]//td[6]'
        cls.log_shift_hours_path = '//table//tbody//tr[1]//td[5]'

        cls.start_time_form = '//input[@name = "start_time"]'
        cls.end_time_form = '//input[@name = "end_time"]'

        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        super(ViewVolunteerShift, cls).setUpClass()

    def setUp(self):
        self.v1 = create_volunteer()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(ViewVolunteerShift, cls).tearDownClass()

    def view_upcoming_shifts(self):
        self.driver.find_element_by_link_text('Upcoming Shifts').send_keys("\n")

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys(credentials['username'])
        self.driver.find_element_by_id('id_password').send_keys(credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def login_volunteer(self):
        credentials = {'username' : 'volunteer', 'password' : 'volunteer'}
        self.login(credentials)

    def test_access_another_existing_volunteer_view(self):
        '''
        details = ['test_volunteer', 'volunteer-first-nameq', 'volunteer-last-nameq',
                'volunteer-addressq', 'volunteer-city', 'volunteer-stateq', 'volunteer-countryq',
                '9999999999', 'volunteer-email2@systers.orgq','volunteer-organizationq']

        test_volunteer = create_volunteer_with_details(details)

        self.login_volunteer()
        self.driver.get(self.live_server_url + self.view_shift_page + str(test_volunteer_id))
        '''
        pass

    def test_access_another_nonexisting_volunteer_view(self):
        self.login_volunteer()
        self.driver.get(self.live_server_url + self.view_shift_page + '65459')
        found = re.search('Not Found', self.driver.page_source)
        self.assertNotEqual(found, None)

    def test_view_without_any_assigned_shift(self):
        self.login_volunteer()
        self.view_upcoming_shifts()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text, 'You do not have any upcoming shifts.')

    def register_dataset(self):

        created_event = create_event_with_details(['event-four', '2017-06-01', '2017-06-10'])
        created_job = create_job_with_details(
            ['jobOneInEventFour', '2017-06-01', '2017-06-10', 'job description', created_event]
            )
        created_shift = create_shift_with_details(['2017-06-01', '09:00', '15:00', '10', created_job])
        registered_shift = register_volunteer_for_shift_utility(created_shift, self.v1)

    def test_view_with_assigned_and_unlogged_shift(self):

        self.register_dataset()
        self.login_volunteer()
        self.view_upcoming_shifts()

        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_job_path).text, 'jobOneInEventFour')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_date_path).text, 'June 1, 2017')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_stime_path).text, '9 a.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_etime_path).text, '3 p.m.')

    def test_log_hours_and_logged_shift_does_not_appear_in_upcoming_shifts(self):

        self.register_dataset()
        self.login_volunteer()
        self.view_upcoming_shifts()

        self.assertEqual(self.driver.find_element_by_xpath(
                self.log_shift_hours_path).text, 'Log Hours')
        self.driver.find_element_by_xpath(
                self.log_shift_hours_path + "//a").click()

        self.driver.find_element_by_xpath(
                self.start_time_form).send_keys('09:00')
        self.driver.find_element_by_xpath(
                self.end_time_form).send_keys('12:00')
        self.driver.find_element_by_xpath('//form').submit()

        # check logged shift does not appear in Upcoming Shifts
        self.view_upcoming_shifts()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text, 'You do not have any upcoming shifts.')
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_xpath('//table')

    def test_cancel_shift_registration(self):

        self.register_dataset()
        self.login_volunteer()
        self.view_upcoming_shifts()

        self.assertEqual(self.driver.find_element_by_xpath(
                self.shift_cancel_path).text, 'Cancel Shift Registration')
        self.driver.find_element_by_xpath(
                self.shift_cancel_path + '//a').click()

        self.assertEqual(self.driver.find_element_by_class_name(
            'panel-title').text, 'Cancel Shift Confirmation')
        self.assertEqual(self.driver.find_element_by_class_name('btn-danger').text,
                'Yes, Cancel this Shift')
        self.driver.find_element_by_xpath('//form').submit()

        # check shift removed from upcoming shifts
        self.driver.find_element_by_link_text('Upcoming Shifts').click()
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text, 'You do not have any upcoming shifts.')
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_xpath('//table')
