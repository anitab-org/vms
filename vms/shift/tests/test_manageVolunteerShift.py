# Django
from django.contrib.staticfiles.testing import LiveServerTestCase
import datetime
from django.urls import reverse
from django.core import mail

# third party
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.eventSignUpPage import EventSignUpPage
from pom.pages.manageShiftPage import ManageShiftPage
from shift.utils import (create_admin, create_volunteer_with_details,
                         create_event_with_details, create_job_with_details,
                         create_volunteer, create_shift_with_details,
                         create_organization_with_details, get_city_by_name,
                         create_edit_request_with_details, get_state_by_name,
                         log_hours_with_details, get_country_by_name)


class ManageVolunteerShift(LiveServerTestCase):
    """
    Admin users have ManageVolunteerShift View which has the following
    functionalities:
    - Filter Volunteers according to certain criteriras
    - Click on `Manage Shift` to check assigned shifts to a volunteer
    - Click on `Assign Shift` lists registered events
    - Click on `View Jobs` to list jobs in selected event
    - Click on `View Shift` to list shifts in the selected job
    - Click on `Assign Shift` and confirm to assign shift.
    - Cancel assigned shift by clicking on `Cancel Shift Assignment`

    ManageVolunteerShift Class contains UI tests for ManageVolunteerShift
    View of Admin Profile. Tests Included.

    - Test View with/without any registered volunteers
    - Test Redirection to events view on clicking `Manage Shifts`
    - Test Jobs page without jobs
    - Test assign shifts without any registered shifts
    - Test assign shifts with registered shifts
    - Test if shift can be assigned to more number of volunteers than slots
      in a shift
    - Test no of slots remaining increases by one when an admin cancels an
      assigned shift
    - Test if a shift can be assigned to a volunteer who has already been
      assigned the same shift
    """

    @classmethod
    def setUpClass(cls):
        """Method to initiate class level objects.

        This method initiates Firefox WebDriver, WebDriverWait and
        the corresponding POM objects for this Test Class
        """
        firefox_options = Options()
        firefox_options.add_argument('-headless')
        cls.driver = webdriver.Firefox(firefox_options=firefox_options)
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.sign_up_page = EventSignUpPage(cls.driver)
        cls.manage_shift_page = ManageShiftPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        cls.wait = WebDriverWait(cls.driver, 10)
        super(ManageVolunteerShift, cls).setUpClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        create_admin()
        self.login_admin()

    def tearDown(self):
        """
        Method consists of statements to be executed at
        end of each test.
        """
        self.authentication_page.logout()

    @classmethod
    def tearDownClass(cls):
        """
        Class method to quit the Firefox WebDriver session after
        execution of all tests in class.
        """
        cls.driver.quit()
        super(ManageVolunteerShift, cls).tearDownClass()

    def login_admin(self):
        """
        Utility function to login as administrator.
        """
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({
            'username': 'admin',
            'password': 'admin'
        })

    @staticmethod
    def create_shift(shift):
        """
        Utility function to create a valid shift.
        :param shift: Iterable containing details of shift.
        :return: Shift type object.
        """
        # Register event to create job
        event = {
            'name': 'event-name',
            'start_date': '2050-05-20',
            'end_date': '2050-05-20',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        e1 = create_event_with_details(event)

        # Create job to create shift
        job = {
            'name': 'job name',
            'start_date': '2050-05-20',
            'end_date': '2050-05-20',
            'description': 'job description',
            'event': e1
        }
        j1 = create_job_with_details(job)

        # Create shift to assign
        shift['job'] = j1
        s1 = create_shift_with_details(shift)

        return s1

    def check_shift_details(self, details):
        """
        Utility function to perform assertions on
        shift detailsreceived as param.
        :param details: Iterable consisting details of job to check.
        """
        sign_up_page = self.sign_up_page
        self.assertEqual(sign_up_page.get_shift_job(), details['job'])
        self.assertEqual(sign_up_page.get_shift_date(), details['date'])
        self.assertEqual(
            sign_up_page.get_shift_start_time(),
            details['start_time']
        )
        self.assertEqual(sign_up_page.get_shift_end_time(), details['end_time'])

    def wait_for_home_page(self):
        """
        Utility function to perform explicit wait for home page.
        """
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//h1[contains(text(), 'Volunteer Management System')]"
                 )
            )
        )

    def test_table_layout(self):
        """
        Test the shift table has details displayed correctly.
        """
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page
        manage_shift_page.live_server_url = self.live_server_url

        # Register volunteers
        volunteer_1 = create_volunteer()

        shift = {
            'date': '2050-05-20',
            'start_time': '09:00',
            'end_time': '15:00',
            'max_volunteers': '1',
            'address': 'shift-address',
            'venue': 'venue-address',
        }
        shift_1 = self.create_shift(shift)

        self.wait_for_home_page()

        # Open manage volunteer shift
        self.manage_shift_page.navigate_to_manage_shift_page()

        # Volunteer-one does not have any registered shifts
        manage_shift_page.select_volunteer(1)
        manage_shift_page.assign_shift()

        # Events shown in table
        self.assertRaisesRegexp(NoSuchElementException,
                                'Message: Unable to locate element: '
                                '.alert-info',
                                sign_up_page.get_info_box)
        self.assertEqual(sign_up_page.get_view_jobs(),
                         manage_shift_page.VIEW_JOB)
        sign_up_page.click_to_view_jobs()

        # Arrived on page2 with jobs
        self.assertEqual(sign_up_page.get_view_shifts(),
                         manage_shift_page.VIEW_SHIFT)
        sign_up_page.click_to_view_shifts()

        # Arrived on page3 with shifts, assign shift to volunteer one
        self.assertEqual(sign_up_page.get_sign_up(),
                         manage_shift_page.shift_assignment_text)

    def test_landing_page_without_any_registered_volunteers(self):
        """
        Test manage shifts page with no registered data.
        """
        manage_shift_page = self.manage_shift_page
        manage_shift_page.live_server_url = self.live_server_url

        self.wait_for_home_page()

        # Open manage volunteer shift
        manage_shift_page.navigate_to_manage_shift_page()

        self.assertRaisesRegexp(NoSuchElementException,
                                'Message: Unable to locate element: tr',
                                manage_shift_page.find_table_row)

    def test_landing_page_with_registered_volunteers(self):
        """
        Test details on manage shifts page with data registered.
        """
        manage_shift_page = self.manage_shift_page
        manage_shift_page.live_server_url = self.live_server_url

        # Register volunteer
        volunteer_1 = create_volunteer()

        self.wait_for_home_page()

        manage_shift_page.navigate_to_manage_shift_page()

        self.assertNotEqual(manage_shift_page.find_table_row(), None)
        manage_shift_page.select_volunteer(1)
        self.assertEqual(manage_shift_page.get_info_box(),
                         manage_shift_page.no_volunteer_shift_message)

    def test_events_page_with_no_events(self):
        """
        Test no event present at shifts sign up page
        for volunteer to sign up for.
        """
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page

        # Register volunteers
        volunteer_1 = create_volunteer()

        manage_shift_page.live_server_url = self.live_server_url

        self.wait_for_home_page()

        # Open manage volunteer shift
        self.manage_shift_page.navigate_to_manage_shift_page()

        manage_shift_page.select_volunteer(1)
        manage_shift_page.assign_shift()

        self.assertEqual(sign_up_page.get_info_box().text,
                         sign_up_page.no_event_message)

    def test_jobs_page_with_no_jobs(self):
        """
        Test no job present at shifts sign up page for volunteer to sign up for.
        """
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page
        manage_shift_page.live_server_url = self.live_server_url

        # Register volunteers
        volunteer_1 = create_volunteer()

        # Create events
        event = {
            'name': 'event-name',
            'start_date': '2017-05-20',
            'end_date': '2017-05-20',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        event_1 = create_event_with_details(event)

        self.wait_for_home_page()

        # Open manage volunteer shift
        manage_shift_page.navigate_to_manage_shift_page()
        manage_shift_page.select_volunteer(1)
        manage_shift_page.assign_shift()

        self.assertEqual(sign_up_page.get_info_box().text,
                         sign_up_page.no_event_message)

    def test_assign_shifts_with_no_shifts(self):
        """
        Test no shift present at shifts sign up page
        for volunteer to sign up for.
        """
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page
        manage_shift_page.live_server_url = self.live_server_url

        # Register volunteers
        volunteer_1 = create_volunteer()

        # Create events
        event = {
            'name': 'event-name',
            'start_date': '2017-05-20',
            'end_date': '2017-05-20',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        event_1 = create_event_with_details(event)

        # Create jobs
        job = {
            'name': 'job name',
            'start_date': '2017-05-20',
            'end_date': '2017-05-20',
            'description': 'job description',
            'event': event_1
        }
        job_1 = create_job_with_details(job)

        self.wait_for_home_page()

        # Open manage volunteer shift
        manage_shift_page.navigate_to_manage_shift_page()
        manage_shift_page.select_volunteer(1)
        manage_shift_page.assign_shift()

        # No events shown in table
        self.assertEqual(sign_up_page.get_info_box().text,
                         sign_up_page.no_event_message)

    def test_assign_shifts_with_registered_shifts(self):
        """
        Test assignment of shift present at shifts sign up page
        for volunteer to sign up for.
        """
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page
        manage_shift_page.live_server_url = self.live_server_url

        # Register volunteers
        volunteer_1 = create_volunteer()

        shift = {
            'date': '2050-05-20',
            'start_time': '09:00',
            'end_time': '15:00',
            'max_volunteers': '1',
            'address': 'shift-address',
            'venue': 'venue-address',
        }
        shift_1 = self.create_shift(shift)

        self.wait_for_home_page()

        # Volunteer-one does not have any registered shifts
        manage_shift_page.navigate_to_manage_shift_page()
        manage_shift_page.select_volunteer(1)
        self.assertEqual(manage_shift_page.get_info_box(),
                         manage_shift_page.no_volunteer_shift_message)

        manage_shift_page.assign_shift()

        # Events shown in table
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: .alert-info',
                                sign_up_page.get_info_box)
        manage_shift_page.navigate_to_shift_assignment_page()

        # Confirm on shift assignment to volunteer-one
        manage_shift_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: .alert-danger',
                                sign_up_page.get_danger_box)

        # Check shift assignment to volunteer-one
        manage_shift_page.navigate_to_manage_shift_page()
        manage_shift_page.select_volunteer(1)
        self.check_shift_details({
            'job': 'job name',
            'date': 'May 20, 2050',
            'start_time': '9 a.m.',
            'end_time': '3 p.m.'
        })

        # check shift assignment email
        mail.outbox = []
        mail.send_mail(
            "Shift Assigned", "message",
            "messanger@localhost.com", [volunteer_1.email]
        )
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.subject, 'Shift Assigned')
        self.assertEqual(msg.to, ['volunteer@volunteer.com'])

    def test_slots_remaining_in_shift(self):
        """
        Test correct display of the remaining number of slots for shift.
        """
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page
        manage_shift_page.live_server_url = self.live_server_url

        # Register volunteers
        volunteer_1 = create_volunteer()
        city_name = 'Bothell'
        state_name = 'Washington'
        country_name = 'United States'
        city = get_city_by_name(city_name)
        state = get_state_by_name(state_name)
        country = get_country_by_name(country_name)
        volunteer_2 = {
            'username': 'volunteer-two',
            'first_name': 'volunteer-two',
            'last_name': 'volunteer-two',
            'address': 'volunteer-two',
            'city': city,
            'state': state,
            'country': country,
            'phone_number': '9999999999',
            'email': 'volunteer-email2@systers.org',
        }
        org_name = 'Google'
        org_obj = create_organization_with_details(org_name)
        volunteer_2 = create_volunteer_with_details(volunteer_2, org_obj)

        shift = {
            'date': '2050-05-20',
            'start_time': '09:00',
            'end_time': '15:00',
            'max_volunteers': '1',
            'address': 'shift-address',
            'venue': 'venue-address',
        }
        shift_1 = self.create_shift(shift)

        # Open manage volunteer shift
        manage_shift_page.navigate_to_manage_shift_page()

        # Volunteer-one does not have any registered shifts
        manage_shift_page.select_volunteer(1)
        self.assertEqual(manage_shift_page.get_info_box(),
                         manage_shift_page.no_volunteer_shift_message)

        manage_shift_page.assign_shift()

        # Events shown in table
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: .alert-info',
                                sign_up_page.get_info_box)
        manage_shift_page.navigate_to_shift_assignment_page()

        # Confirm on shift assignment to volunteer-one
        manage_shift_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: .alert-danger',
                                sign_up_page.get_danger_box)

        # Check shift assignment to volunteer-one
        manage_shift_page.navigate_to_manage_shift_page()
        manage_shift_page.select_volunteer(1)
        self.check_shift_details({
            'job': 'job name',
            'date': 'May 20, 2050',
            'start_time': '9 a.m.',
            'end_time': '3 p.m.'
        })

        # Open manage volunteer shift again to assign shift to volunteer two
        manage_shift_page.navigate_to_manage_shift_page()

        # Volunteer-two does not have any registered shifts
        manage_shift_page.select_volunteer(2)
        self.assertEqual(manage_shift_page.get_info_box(),
                         manage_shift_page.no_volunteer_shift_message)

        manage_shift_page.assign_shift()

        # No events shown in table
        self.assertEqual(sign_up_page.get_info_box().text,
                         sign_up_page.no_event_message)

    def test_cancel_assigned_shift(self):
        """
        Test successful cancellation of shift.
        """
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page
        self.manage_shift_page.live_server_url = self.live_server_url

        self.wait_for_home_page()

        # Register volunteers
        volunteer_1 = create_volunteer()

        shift = {
            'date': '2050-05-20',
            'start_time': '09:00',
            'end_time': '15:00',
            'max_volunteers': '1',
            'address': 'shift-address',
            'venue': 'venue-address',
        }
        shift_1 = self.create_shift(shift)

        # Open manage volunteer shift
        manage_shift_page.navigate_to_manage_shift_page()

        # Volunteer-one does not have any registered shifts
        manage_shift_page.select_volunteer(1)
        self.assertEqual(manage_shift_page.get_info_box(),
                         manage_shift_page.no_volunteer_shift_message)

        manage_shift_page.assign_shift()

        # Events shown in table
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: .alert-info',
                                sign_up_page.get_info_box)

        sign_up_page.click_to_view_jobs()
        sign_up_page.click_to_view_shifts()

        # Arrived on shifts page, assign shift to volunteer one
        slots_remaining_before_assignment = sign_up_page.get_remaining_slots()
        sign_up_page.click_to_sign_up()

        # Confirm on shift assignment to volunteer-one
        sign_up_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: .alert-danger',
                                sign_up_page.get_danger_box)

        # Check shift assignment to volunteer-one
        manage_shift_page.navigate_to_manage_shift_page()
        manage_shift_page.select_volunteer(1)
        self.check_shift_details({
            'job': 'job name',
            'date': 'May 20, 2050',
            'start_time': '9 a.m.',
            'end_time': '3 p.m.'
        })

        # Cancel assigned shift
        self.assertEqual(manage_shift_page.get_cancel_shift().text,
                         'Cancel Shift Registration')
        manage_shift_page.cancel_shift()
        self.assertNotEqual(manage_shift_page.get_cancellation_box(), None)
        self.assertEqual(manage_shift_page.get_cancellation_message(),
                         'Yes, Cancel this Shift')
        manage_shift_page.submit_form()

        self.wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'alert-info')
            )
        )

        # Check cancellation email
        mail.outbox = []
        mail.send_mail(
            "Shift Cancelled", "message",
            "messanger@localhost.com", [volunteer_1.email]
        )
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.subject, 'Shift Cancelled')
        self.assertEqual(msg.to, ['volunteer@volunteer.com'])

        # Check cancelled shift reflects in volunteer shift details
        self.assertEqual(manage_shift_page.get_info_box(),
                         manage_shift_page.no_volunteer_shift_message)

        # Check slots remaining increases by one, after cancellation of
        # assigned shift
        manage_shift_page.assign_shift()
        sign_up_page.click_to_view_jobs()
        sign_up_page.click_to_view_shifts()
        slots_after_cancellation = sign_up_page.get_remaining_slots()
        self.assertEqual(slots_remaining_before_assignment,
                         slots_after_cancellation)

    def test_shift_edit_request(self):
        """
        checks the edit request link received by admin
        """

        volunteer_1 = create_volunteer()

        shift = {
            'date': '2050-05-20',
            'start_time': '09:00',
            'end_time': '15:00',
            'max_volunteers': '1',
            'address': 'shift-address',
            'venue': 'venue-address',
        }
        shift_1 = self.create_shift(shift)
        start = datetime.time(hour=10, minute=0)
        end = datetime.time(hour=14, minute=0)
        logged_shift = log_hours_with_details(volunteer_1, shift_1, start, end)
        start_time = datetime.time(hour=9, minute=30)
        end_time = datetime.time(hour=14, minute=0)
        edit_request = \
            create_edit_request_with_details(start_time, end_time, logged_shift)
        response = self.client.get(
            reverse(
                'shift:edit_request_manager',
                args=[
                    shift_1.id,
                    volunteer_1.id,
                    edit_request.id
                ]
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_edit_request_email_volunteer(self):
        """
        checks if the volunteer gets an email when his hours are edited
        by admin upon his request
        """

        volunteer_1 = create_volunteer()

        shift = {
            'date': '2050-05-20',
            'start_time': '09:00',
            'end_time': '15:00',
            'max_volunteers': '1',
            'address': 'shift-address',
            'venue': 'venue-address',
        }
        shift_1 = self.create_shift(shift)
        start = datetime.time(hour=10, minute=0)
        end = datetime.time(hour=14, minute=0)
        logged_shift = log_hours_with_details(volunteer_1, shift_1, start, end)
        start_time = datetime.time(hour=9, minute=30)
        end_time = datetime.time(hour=14, minute=0)
        edit_request = \
            create_edit_request_with_details(start_time, end_time, logged_shift)
        vol_email = volunteer_1.email
        mail.outbox = []
        mail.send_mail(
            "Log Hours Edited", "message",
            "messanger@localhost.com", [vol_email]
        )
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.subject, "Log Hours Edited")
        self.assertEqual(msg.to, ['volunteer@volunteer.com'])

    def test_clear_hours(self):
        """
        Test clearing of shift hours.
        """
        manage_shift_page = self.manage_shift_page
        self.manage_shift_page.live_server_url = self.live_server_url

        volunteer_1 = create_volunteer()

        shift = {
            'date': '2050-05-20',
            'start_time': '09:00',
            'end_time': '15:00',
            'max_volunteers': '1',
            'address': 'shift-address',
            'venue': 'venue-address',
        }
        shift_1 = self.create_shift(shift)
        start = datetime.time(hour=10, minute=0)
        end = datetime.time(hour=14, minute=0)
        logged_shift = log_hours_with_details(volunteer_1, shift_1, start, end)

        self.wait_for_home_page()

        # Open manage volunteer shift
        manage_shift_page.navigate_to_manage_shift_page()

        manage_shift_page.select_volunteer(1)

        self.assertEqual(
            manage_shift_page.get_clear_shift_hours_text(),
            'Clear Hours'
        )
        manage_shift_page.click_to_clear_hours()
        manage_shift_page.submit_form()
        self.assertEqual(
            manage_shift_page.get_logged_info_box(),
            "This volunteer does not have any shifts with logged hours."
        )

    def test_assign_same_shift_to_volunteer_twice(self):
        """
        Test errors while assignment of same shift
        to volunteer to which they are already assigned.
        """
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page
        self.manage_shift_page.live_server_url = self.live_server_url

        # Register volunteers
        volunteer_1 = create_volunteer()

        shift = {
            'date': '2050-05-20',
            'start_time': '09:00',
            'end_time': '15:00',
            'max_volunteers': '1',
            'address': 'shift-address',
            'venue': 'venue-address',
        }
        shift_1 = self.create_shift(shift)

        self.wait_for_home_page()

        # Open manage volunteer shift
        manage_shift_page.navigate_to_manage_shift_page()

        # Volunteer-one does not have any registered shifts
        manage_shift_page.select_volunteer(1)
        self.assertEqual(manage_shift_page.get_info_box(),
                         manage_shift_page.no_volunteer_shift_message)

        manage_shift_page.assign_shift()

        # Events shown in table
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: .alert-info',
                                sign_up_page.get_info_box)
        manage_shift_page.navigate_to_shift_assignment_page()

        # Confirm on shift assignment to volunteer-one
        manage_shift_page.submit_form()
        self.assertRaisesRegexp(NoSuchElementException,
                                'Unable to locate element: .alert-danger',
                                sign_up_page.get_danger_box)

        # Assign same shift to voluteer-one again
        # Check volunteer-one has one registered shift now
        self.assertEqual(sign_up_page.get_shift_job(), 'job name')
        manage_shift_page.assign_shift()

        # Events page
        self.assertEqual(
            sign_up_page.get_info_box().text,
            sign_up_page.no_event_message
        )

