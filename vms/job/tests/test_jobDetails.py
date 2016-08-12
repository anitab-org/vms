from django.contrib.staticfiles.testing import LiveServerTestCase

from pom.pages.jobDetailsPage import JobDetailsPage
from pom.pages.authenticationPage import AuthenticationPage

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
        self.job_list_page = '/job/list/'

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        super(JobDetails, self).setUp()
        self.job_details_page = JobDetailsPage(self.driver)
        self.authentication_page = AuthenticationPage(self.driver)

    def tearDown(self):
        self.driver.quit()
        super(JobDetails, self).tearDown()

    def register_job(self):
        # create shift and log hours
        created_event = create_event_with_details(['event', '2017-06-15', '2017-06-17'])
        created_job = create_job_with_details(['job', '2017-06-15', '2017-06-18', '', created_event])
        return created_job

    def login_admin(self):
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.login({'username': 'admin', 'password': 'admin'})

    def test_job_details_view(self):
        self.login_admin()
        job = self.register_job()
        job_details_page = self.job_details_page
        job_details_page.live_server_url = self.live_server_url
        job_details_page.navigate_to_job_details_view()

        # verify details
        self.assertEqual(job_details_page.get_name(), job.name)
        self.assertEqual(job_details_page.get_start_date(), 'June 15, 2017')
        self.assertEqual(job_details_page.get_end_date(), 'June 18, 2017')
        self.assertEqual(job_details_page.get_event_name(), job.event.name)
