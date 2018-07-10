# third party
import json
import datetime

from selenium import webdriver

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from selenium.common.exceptions import NoSuchElementException

from organization.models import Organization
from pom.locators.administratorReportPageLocators import AdministratorReportPageLocators
from pom.pages.administratorReportPage import AdministratorReportPage
from pom.pages.authenticationPage import AuthenticationPage
from pom.pageUrls import PageUrls
from shift.utils import (create_admin, create_volunteer,
                         create_organization_with_details,
                         create_event_with_details, create_job_with_details,
                         create_shift_with_details, log_hours_with_details,
                         register_volunteer_for_shift_utility, create_volunteer_with_details_dynamic_password,
                         register_past_event_utility, register_past_job_utility, register_past_shift_utility,
                         create_report_with_details, create_volunteer_with_details)

class Report(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.authentication_page = AuthenticationPage(cls.driver)
        cls.report_page = AdministratorReportPage(cls.driver)
        cls.elements = AdministratorReportPageLocators()
        super(Report, cls).setUpClass()

    def setUp(self):
        create_admin()
        self.login_admin()

    def tearDown(self):
        self.authentication_page.logout()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(Report, cls).tearDownClass()

    def login_admin(self):
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({
            'username': 'admin',
            'password': 'admin'
        })

    def verify_shift_details(self, hours):
        """
        Utility function to verify the shift details.
        :param total_shifts: Total number of shifts as filled in form.
        :param hours: Total number of hours as filled in form.
        """
        total_no_of_hours = self.report_page.get_shift_summary().split(' ')[-1].strip('\n')
        self.assertEqual(total_no_of_hours, hours)


    def test_check_report_hours(self):
        self.report_page.go_to_admin_report()
        vol = create_volunteer()
        register_past_event_utility()
        register_past_job_utility()
        shift = register_past_shift_utility()
        start=datetime.time(hour=10, minute=0)
        end=datetime.time(hour=11, minute=0)
        logged_shift = log_hours_with_details(vol, shift, start, end)
        create_report_with_details(vol, logged_shift)
        report_page = self.report_page
        report_page.get_page(self.live_server_url, PageUrls.administrator_report_page)
        self.assertEqual(report_page.get_hours(), '1.00')


    def test_check_report_volunteer(self):
        self.report_page.go_to_admin_report()
        credentials = [
            'volunteer-username', 'VOLUNTEER-FIRST-NAME',
            'volunteer-last-name', 'volunteer-address', 'volunteer-city',
            'volunteer-state', 'volunteer-country', '9999999999',
            'volunteer-email@systers.org', 'volunteer-organization'
        ]
        vol = create_volunteer_with_details(credentials)
        register_past_event_utility()
        register_past_job_utility()
        shift = register_past_shift_utility()
        start=datetime.time(hour=10, minute=0)
        end=datetime.time(hour=11, minute=0)
        logged_shift = log_hours_with_details(vol, shift, start, end)
        create_report_with_details(vol, logged_shift)
        report_page = self.report_page
        report_page.get_page(self.live_server_url, PageUrls.administrator_report_page)
        self.assertEqual(report_page.get_volunteer_name(), 'VOLUNTEER-FIRST-NAME volunteer-last-name')


    def test_reject_report(self):
        self.report_page.go_to_admin_report()
        vol = create_volunteer()
        register_past_event_utility()
        register_past_job_utility()
        shift = register_past_shift_utility()
        start=datetime.time(hour=10, minute=0)
        end=datetime.time(hour=11, minute=0)
        logged_shift = log_hours_with_details(vol, shift, start, end)
        create_report_with_details(vol, logged_shift)
        report_page = self.report_page
        report_page.get_page(self.live_server_url, PageUrls.administrator_report_page)
        self.assertEqual(report_page.get_rejection_context(), 'Reject')
        report_page.reject_report()
        with self.assertRaises(NoSuchElementException):
            report_page.get_report()

    def test_view_report(self):
        self.report_page.go_to_admin_report()
        vol = create_volunteer()
        register_past_event_utility()
        register_past_job_utility()
        shift = register_past_shift_utility()
        start=datetime.time(hour=10, minute=0)
        end=datetime.time(hour=11, minute=0)
        logged_shift = log_hours_with_details(vol, shift, start, end)
        create_report_with_details(vol, logged_shift)
        report_page = self.report_page
        report_page.get_page(self.live_server_url, PageUrls.administrator_report_page)
        report_page.go_to_view_report_page()
        self.verify_shift_details('1.00')

    def test_approve_report(self):
        self.report_page.go_to_admin_report()
        vol = create_volunteer()
        register_past_event_utility()
        register_past_job_utility()
        shift = register_past_shift_utility()
        start=datetime.time(hour=10, minute=0)
        end=datetime.time(hour=11, minute=0)
        logged_shift = log_hours_with_details(vol, shift, start, end)
        create_report_with_details(vol, logged_shift)
        report_page = self.report_page
        report_page.get_page(self.live_server_url, PageUrls.administrator_report_page)
        report_page.go_to_view_report_page()
        self.assertEqual(report_page.get_approval_context(), 'Approve Report')
        report_page.approve_report()
        self.assertEqual(report_page.remove_i18n(self.driver.current_url), self.live_server_url + report_page.administrator_report_page)
        with self.assertRaises(NoSuchElementException):
            report_page.get_report()
