from django.contrib.staticfiles.testing import LiveServerTestCase

from shift.utils import (
    create_admin,
    create_event_with_details,
    create_job_with_details
    )

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class JobDetails(LiveServerTestCase):
    '''
    Contains Tests for View Job Details Page
    '''
    def setUp(self):
        create_admin()
        self.homepage = '/'
        self.authentication_page = '/authentication/login/'
        self.job_list_page = '/job/list/'
        self.job_name_path = '//table[1]//tr//td[1]'
        self.job_event_path = '//table[1]//tr//td[2]'
        self.job_start_date_path = '//table[1]//tr//td[3]'
        self.job_end_date_path = '//table[1]//tr//td[4]'

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        super(JobDetails, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(JobDetails, self).tearDown()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id(
            'id_login').send_keys(credentials['username'])
        self.driver.find_element_by_id(
            'id_password').send_keys(credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def register_job(self):

        # create shift and log hours
        created_event = create_event_with_details(['event', '2017-06-15', '2017-06-17'])
        created_job = create_job_with_details(['job', '2017-06-15', '2017-06-18', '', created_event])

        return created_job

    def login_admin(self):
        self.login({'username': 'admin', 'password': 'admin'})

    def navigate_to_job_details_view(self):
        self.driver.get(self.live_server_url + self.job_list_page)

    def test_job_details_view(self):
        self.login_admin()
        job = self.register_job()
        self.navigate_to_job_details_view()

        # verify details
        self.assertEqual(self.driver.find_element_by_xpath(
            self.job_name_path).text, job.name)
        self.assertEqual(self.driver.find_element_by_xpath(
            self.job_start_date_path).text, 'June 15, 2017')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.job_end_date_path).text, 'June 18, 2017')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.job_event_path).text, job.event.name)
