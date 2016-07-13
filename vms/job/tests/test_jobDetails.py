from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User
from administrator.models import Administrator
from event.models import Event
from job.models import Job

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class JobDetails(LiveServerTestCase):
    '''
    Contains Tests for View Job Details Page
    '''

    def setUp(self):
        admin_user = User.objects.create_user(
            username='admin',
            password='admin')

        Administrator.objects.create(
            user=admin_user,
            address='address',
            city='city',
            state='state',
            country='country',
            email='admin@admin.com',
            phone_number='9999999999',
            unlisted_organization='organization')

        self.homepage = '/'
        self.authentication_page = '/authentication/login/'
        self.job_list_page = '/job/list/'
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

    def register_job_utility(self, ):

        # create shift and log hours
        event = Event.objects.create(
            name='event',
            start_date='2017-06-15',
            end_date='2017-06-17')

        job = Job.objects.create(
            name='job',
            start_date='2017-06-15',
            end_date='2017-06-18',
            event=event)

        return job

    def navigate_to_job_details_view(self):
        self.driver.get(self.live_server_url + self.job_list_page)

    def test_job_details_view(self):
        self.login({'username': 'admin', 'password': 'admin'})
        shift = self.register_job_utility()
        self.navigate_to_job_details_view()

        # verify details
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[1]//tr//td[1]').text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[1]//tr//td[3]').text, 'June 15, 2017')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[1]//tr//td[4]').text, 'June 18, 2017')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[1]//tr//td[2]').text, 'event')
