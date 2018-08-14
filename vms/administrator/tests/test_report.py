# third party
import datetime

from selenium import webdriver

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.core import mail

# local Django
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from pom.locators.administratorReportPageLocators import\
    AdministratorReportPageLocators
from pom.pages.administratorReportPage import AdministratorReportPage
from pom.pages.authenticationPage import AuthenticationPage
from pom.pageUrls import PageUrls
from shift.utils import (create_admin, create_country, create_state,
                         create_city, create_volunteer,
                         create_organization_with_details,
                         log_hours_with_details, register_past_event_utility,
                         register_past_job_utility, register_past_shift_utility,
                         create_report_with_details,
                         create_volunteer_with_details)


class Report(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        firefox_options = Options()
        firefox_options.add_argument('-headless')
        cls.driver = webdriver.Firefox(firefox_options=firefox_options)
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
        :param hours: Total number of hours as filled in form.
        """
        total_no_of_hours = \
            self.report_page.get_shift_summary().split(' ')[-1].strip('\n')
        self.assertEqual(total_no_of_hours, hours)

    def test_check_report_hours(self):
        self.report_page.go_to_admin_report()
        vol = create_volunteer()
        register_past_event_utility()
        register_past_job_utility()
        shift = register_past_shift_utility()
        start = datetime.time(hour=10, minute=0)
        end = datetime.time(hour=11, minute=0)
        logged_shift = log_hours_with_details(vol, shift, start, end)
        create_report_with_details(vol, logged_shift)
        report_page = self.report_page
        report_page.get_page(
            self.live_server_url,
            PageUrls.administrator_report_page
        )
        self.assertEqual(report_page.get_hours(), '1.00')

    def test_check_report_volunteer(self):
        self.report_page.go_to_admin_report()
        country = create_country()
        state = create_state()
        city = create_city()
        credentials = {
            'username': 'volunteer-username',
            'first_name': 'VOLUNTEER-FIRST-NAME',
            'last_name': 'volunteer-last-name',
            'address': 'volunteer-address',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email@systers.org'
        }
        org_name = 'volunteer-organization'
        org_obj = create_organization_with_details(org_name)
        vol = create_volunteer_with_details(credentials, org_obj)
        register_past_event_utility()
        register_past_job_utility()
        shift = register_past_shift_utility()
        start = datetime.time(hour=10, minute=0)
        end = datetime.time(hour=11, minute=0)
        logged_shift = log_hours_with_details(vol, shift, start, end)
        create_report_with_details(vol, logged_shift)
        report_page = self.report_page
        report_page.get_page(
            self.live_server_url,
            PageUrls.administrator_report_page
        )
        self.assertEqual(
            report_page.get_volunteer_name(),
            'VOLUNTEER-FIRST-NAME volunteer-last-name'
        )

    def test_reject_report(self):
        self.report_page.go_to_admin_report()
        vol = create_volunteer()
        register_past_event_utility()
        register_past_job_utility()
        shift = register_past_shift_utility()
        start = datetime.time(hour=10, minute=0)
        end = datetime.time(hour=11, minute=0)
        logged_shift = log_hours_with_details(vol, shift, start, end)
        create_report_with_details(vol, logged_shift)
        report_page = self.report_page
        report_page.get_page(
            self.live_server_url,
            PageUrls.administrator_report_page
        )
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
        start = datetime.time(hour=10, minute=0)
        end = datetime.time(hour=11, minute=0)
        logged_shift = log_hours_with_details(vol, shift, start, end)
        create_report_with_details(vol, logged_shift)
        report_page = self.report_page
        report_page.get_page(
            self.live_server_url,
            PageUrls.administrator_report_page
        )
        report_page.go_to_view_report_page()
        self.verify_shift_details('1.00')

    def test_approve_report(self):
        self.report_page.go_to_admin_report()
        vol = create_volunteer()
        register_past_event_utility()
        register_past_job_utility()
        shift = register_past_shift_utility()
        start = datetime.time(hour=10, minute=0)
        end = datetime.time(hour=11, minute=0)
        logged_shift = log_hours_with_details(vol, shift, start, end)
        create_report_with_details(vol, logged_shift)
        report_page = self.report_page
        report_page.get_page(
            self.live_server_url,
            PageUrls.administrator_report_page
        )
        report_page.go_to_view_report_page()
        self.assertEqual(report_page.get_approval_context(), 'Approve Report')
        report_page.approve_report()
        self.assertEqual(
            report_page.remove_i18n(self.driver.current_url),
            self.live_server_url + report_page.administrator_report_page
        )
        with self.assertRaises(NoSuchElementException):
            report_page.get_report()

    def test_email_on_report_approval(self):
        vol = create_volunteer()
        register_past_event_utility()
        register_past_job_utility()
        shift = register_past_shift_utility()
        start = datetime.time(hour=10, minute=0)
        end = datetime.time(hour=11, minute=0)
        logged_shift = log_hours_with_details(vol, shift, start, end)
        report = create_report_with_details(vol, logged_shift)
        mail.send_mail(
            "Report Approved", "message",
            "messanger@localhost.com", [vol.email]
        )
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.subject, 'Report Approved')
        self.assertEqual(msg.to, ['volunteer@volunteer.com'])
        response = self.client.get(
            '/administrator/report/approve/%s' % report.id
        )
        self.assertEqual(response.status_code, 302)

    def test_email_on_reject_report(self):
        self.report_page.go_to_admin_report()
        vol = create_volunteer()
        register_past_event_utility()
        register_past_job_utility()
        shift = register_past_shift_utility()
        start = datetime.time(hour=10, minute=0)
        end = datetime.time(hour=11, minute=0)
        logged_shift = log_hours_with_details(vol, shift, start, end)
        create_report_with_details(vol, logged_shift)
        report_page = self.report_page
        report_page.get_page(
            self.live_server_url,
            PageUrls.administrator_report_page
        )
        self.assertEqual(report_page.get_rejection_context(), 'Reject')
        report_page.reject_report()
        mail.outbox = []
        mail.send_mail(
            "Report Rejected", "message",
            "messanger@localhost.com", [vol.email]
        )
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.subject, 'Report Rejected')
        self.assertEqual(msg.to, ['volunteer@volunteer.com'])

