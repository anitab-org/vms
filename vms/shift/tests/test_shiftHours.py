from django.contrib.staticfiles.testing import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from shift.utils import (
    create_volunteer,
    create_event_with_details,
    create_job_with_details,
    create_shift_with_details,
    log_hours_with_details
    )

class ShiftHours(LiveServerTestCase):
    '''
    '''

    @classmethod
    def setUpClass(cls):
        cls.homepage = '/'
        cls.authentication_page = '/authentication/login/'
        cls.view_hours_page = '/shift/view_hours/'
        cls.shift_job_path = '//table//tbody//tr[1]//td[1]'
        cls.shift_date_path = '//table//tbody//tr[1]//td[2]'
        cls.shift_stime_path = '//table//tbody//tr[1]//td[3]'
        cls.shift_etime_path = '//table//tbody//tr[1]//td[4]'
        cls.shift_edit_path = '//table//tbody//tr[1]//td[5]'
        cls.shift_clear_path = '//table//tbody//tr[1]//td[6]'
        cls.start_time_form = '//input[@name = "start_time"]'
        cls.end_time_form = '//input[@name = "end_time"]'

        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        super(ShiftHours, cls).setUpClass()

    def setUp(self):
        self.v1 = create_volunteer()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(ShiftHours, cls).tearDownClass()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys(credentials['username'])
        self.driver.find_element_by_id('id_password').send_keys(credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def login_volunteer_and_navigate(self):
        self.login({'username' : 'volunteer', 'password' : 'volunteer'})
        self.driver.find_element_by_link_text('Completed Shifts').click()

    def register_dataset(self, ):
        
        # create shift and log hours
        e1 = create_event_with_details(['event', '2017-06-15', '2017-06-17'])
        j1 = create_job_with_details(['job', '2017-06-15', '2017-06-15', 'job description', e1])
        s1 = create_shift_with_details(['2017-06-15', '09:00', '15:00', '6', j1])
        log_hours_with_details(self.v1, s1, '12:00', '13:00')

    def edit_hours(self, stime, etime):
        self.driver.find_element_by_xpath(
                self.shift_edit_path + '//a').click()

        self.assertEqual(self.driver.find_element_by_xpath(
            'html/body/div[2]/div[2]/form/fieldset/legend').text,
            'Edit Shift Hours')
        self.driver.find_element_by_xpath(self.start_time_form).clear()
        self.driver.find_element_by_xpath(
                self.start_time_form).send_keys(stime)

        self.driver.find_element_by_xpath(self.end_time_form).clear()
        self.driver.find_element_by_xpath(
                self.end_time_form).send_keys(
                        etime)
        self.driver.find_element_by_xpath('//form[1]').submit()

    def test_view_with_unlogged_shift(self):
        self.login_volunteer_and_navigate()

        self.assertEqual(self.driver.current_url, self.live_server_url + 
                self.view_hours_page + str(self.v1.id))

        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text, 'You have not logged any hours.')

    def test_view_with_logged_shift(self):
        self.register_dataset()
        self.login_volunteer_and_navigate()

        self.assertEqual(self.driver.current_url, self.live_server_url + 
                self.view_hours_page + str(self.v1.id))

        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_job_path).text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_date_path).text, 'June 15, 2017')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_stime_path).text, 'noon')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_etime_path).text, '1 p.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_edit_path).text, 'Edit Hours')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_clear_path).text, 'Clear Hours')

    def test_edit_hours(self):
        self.register_dataset()
        self.login_volunteer_and_navigate()

        self.assertEqual(self.driver.current_url, self.live_server_url + 
                self.view_hours_page + str(self.v1.id))

        self.edit_hours('10:00','13:00')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_stime_path).text, '10 a.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_etime_path).text, '1 p.m.')

    def test_end_hours_less_than_start_hours(self):
        self.register_dataset()
        self.login_volunteer_and_navigate()

        self.assertEqual(self.driver.current_url, self.live_server_url + 
                self.view_hours_page + str(self.v1.id))

        self.edit_hours('14:00', '12:00')

        try:
            self.driver.find_element_by_class_name('alert-danger')
        except NoSuchElementException:
            raise Exception("End hours greater than start hours")

    def test_logged_hours_between_shift_hours(self):
        self.register_dataset()
        self.login_volunteer_and_navigate()

        self.assertEqual(self.driver.current_url, self.live_server_url +
                         self.view_hours_page + str(self.v1.id))

        self.edit_hours('10:00','16:00')
        self.assertEqual(
            self.driver.find_element_by_class_name('alert-danger').text,
            'Logged hours should be between shift hours')

    def test_cancel_hours(self):
        self.register_dataset()
        self.login_volunteer_and_navigate()

        self.assertEqual(self.driver.current_url, self.live_server_url + 
                self.view_hours_page + str(self.v1.id))

        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_job_path).text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.shift_clear_path).text, 'Clear Hours')
        self.driver.find_element_by_xpath(
                self.shift_clear_path + '//a').click()

        self.assertEqual(self.driver.find_element_by_xpath(
            'html/body/div[2]/form/div/div[1]/h3').text,
            'Clear Shift Hours')
        self.driver.find_element_by_xpath('//form[1]').submit()

        with self.assertRaises(NoSuchElementException):
            self.assertEqual(self.driver.find_element_by_xpath(
                self.shift_job_path).text, 'job')
