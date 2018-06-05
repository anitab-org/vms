# third party
import json

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
                         register_volunteer_for_shift_utility, create_volunteer_with_details_dynamic_password)


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
        pass

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

    def verify_shift_details(self, total_shifts, hours):
        total_no_of_shifts = self.report_page.get_shift_summary().split(' ')[10].strip('\nTotal')
        total_no_of_hours = self.report_page.get_shift_summary().split(' ')[-1].strip('\n')
        self.assertEqual(total_no_of_shifts, total_shifts)
        self.assertEqual(total_no_of_hours, hours)

    def test_null_values_with_dataset(self):
        self.report_page.go_to_admin_report()
        # Register dataset
        org = create_organization_with_details('organization-one')
        volunteer = create_volunteer()
        volunteer.organization = org
        volunteer.save()

        # Create Shift and Log hours
        # Create Event
        event = ['Hackathon', '2050-05-24', '2050-05-28']
        created_event = create_event_with_details(event)

        # Create Job
        job = ['Developer', '2050-05-24', '2050-05-28', '', created_event]
        created_job = create_job_with_details(job)

        # Create Shift
        shift = ['2050-05-24', '09:00', '15:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        log_hours_with_details(volunteer, created_shift, "09:00", "12:00")

        report_page = self.report_page
        report_page.get_page(self.live_server_url, PageUrls.administrator_report_page)

        # Check admin report with null fields, should return the above shift
        report_page.fill_report_form(['', '', '', '', ''])
        self.verify_shift_details('1', '3.0')

        self.assertEqual(report_page.element_by_xpath(self.elements.NAME).text, created_event.name)
        self.assertEqual(report_page.element_by_xpath(self.elements.DATE).text, 'May 24, 2050')
        self.assertEqual(report_page.element_by_xpath(self.elements.START_TIME).text, '9 a.m.')
        self.assertEqual(report_page.element_by_xpath(self.elements.END_TIME).text, 'noon')
        self.assertEqual(report_page.element_by_xpath(self.elements.HOURS).text, '3.0')

    def test_null_values_with_empty_dataset(self):
        # Should return no entries
        self.report_page.go_to_admin_report()
        report_page = self.report_page
        report_page.get_page(self.live_server_url, PageUrls.administrator_report_page)

        report_page.fill_report_form(['', '', '', '', ''])
        self.assertEqual(report_page.get_alert_box_text(), report_page.no_results_message)

    def test_only_logged_shifts_are_reported(self):
        report_page = self.report_page
        # Register dataset
        org = create_organization_with_details('organization-one')
        volunteer = create_volunteer()
        volunteer.organization = org
        volunteer.save()

        # Create Event
        event = ['Hackathon', '2050-05-24', '2050-05-28']
        created_event = create_event_with_details(event)

        # Create Job
        job = ['Developer', '2050-05-24', '2050-05-28', '', created_event]
        created_job = create_job_with_details(job)

        # Create Shift
        shift = ['2050-05-24', '09:00', '15:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        # Shift is assigned to volunteer-one, but hours have not been logged
        report_page.go_to_admin_report()
        register_volunteer_for_shift_utility(created_shift, volunteer)
        report_page.get_page(self.live_server_url, PageUrls.administrator_report_page)
        # Check admin report with null fields, should not return the above shift
        # Using multiple tries so to cater to late loading of page.
        for _ in range(3):
            try:
                report_page.fill_report_form(['', '', '', '', ''])
                break
            except NoSuchElementException:
                pass
        self.assertEqual(report_page.get_alert_box_text(), report_page.no_results_message)

    @staticmethod
    def register_dataset(parameters):
        # Register dataset
        # Register dataset
        volunteer = create_volunteer_with_details_dynamic_password(parameters['volunteer'])
        volunteer.organization = parameters['org']
        volunteer.save()

        # Create Event
        event = parameters['event']
        created_event = create_event_with_details(event)

        # Create Job
        job = parameters['job'] + [created_event]
        created_job = create_job_with_details(job)

        # Create Shift
        shift = parameters['shift'] + [created_job]
        created_shift = create_shift_with_details(shift)

        # Create VolunteerShift
        log_hours_with_details(volunteer, created_shift, parameters['vshift'][0], parameters['vshift'][0])

    def create_dataset(self):
        orgs = Organization.create_multiple_organizations(4)

        test_data = open('test_data.json').read()
        parameters = json.loads(test_data)

        parameters[0]["org"] = orgs[0]
        self.register_dataset(parameters[0])

        parameters[1]["org"] = orgs[0]
        self.register_dataset(parameters[1])

        parameters[2]["org"] = orgs[0]
        self.register_dataset(parameters[2])

        parameters[3]["org"] = orgs[1]
        self.register_dataset(parameters[3])

        parameters[4]["org"] = orgs[1]
        self.register_dataset(parameters[4])

        parameters[5]["org"] = orgs[2]
        self.register_dataset(parameters[5])

        parameters[6]["org"] = orgs[3]
        self.register_dataset(parameters[6])

        parameters[7]["org"] = orgs[3]
        self.register_dataset(parameters[7])

    """
    Test giving inconsistent results for log hours and total shifts
    For log hours: Possibly https://github.com/systers/vms/issues/327 wasn't fixed correctly.

    def test_check_intersection_of_fields(self):
        self.create_dataset()

        report_page = self.report_page
        time.sleep(0.5)

        report_page.get_page(self.live_server_url, PageUrls.administrator_report_page)
        search_parameters_1 = ['tom-fname', '', '', '', '']
        report_page.fill_report_form(search_parameters_1)
        self.verify_shift_details('2','2.0')

        report_page.get_page(self.live_server_url, PageUrls.administrator_report_page)
        search_parameters_2 = ['', '', '', '', 'org-one']
        report_page.fill_report_form(search_parameters_2)
        self.verify_shift_details('3','3.0')

        report_page.get_page(self.live_server_url, PageUrls.administrator_report_page)
        search_parameters_3 = ['', '', 'event-four', 'Two', '']
        report_page.fill_report_form(search_parameters_3)
        self.verify_shift_details('1','1.5')

        report_page.get_page(self.live_server_url, PageUrls.administrator_report_page)
        search_parameters_4 = ['', '', 'one', '', '']
        report_page.fill_report_form(search_parameters_4)
        self.verify_shift_details('3','2.5')

        report_page.get_page(self.live_server_url, PageUrls.administrator_report_page)
        search_parameters_5 = ['', 'sherlock', 'two', '', '']
        report_page.fill_report_form(search_parameters_5)
        self.verify_shift_details('1','2.0')
    """
