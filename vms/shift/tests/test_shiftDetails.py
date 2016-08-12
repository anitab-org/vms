from django.contrib.staticfiles.testing import LiveServerTestCase
from shift.models import VolunteerShift

from pom.pages.shiftDetailsPage import ShiftDetailsPage
from pom.pages.authenticationPage import AuthenticationPage

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
        cls.volunteer_detail = ['volunteer-usernameq', 'Michael', 'Reed',
                'address', 'city', 'state', 'country', '9999999999',
                'volunteer@volunteer.com', 'organization']

        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.shift_details_page = ShiftDetailsPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
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

    def login_admin(self):
        authentication_page = self.authentication_page
        authentication_page.server_url = self.live_server_url
        authentication_page.login({'username': 'admin', 'password': 'admin'})

    def register_dataset(self):
        e1 = create_event_with_details(['event', '2017-06-15', '2017-06-17'])
        j1 = create_job_with_details(['job', '2017-06-15', '2017-06-15', 'job description', e1])
        s1 = create_shift_with_details(['2017-06-15', '09:00', '15:00', '6', j1])
        return s1

    def test_view_with_unregistered_volunteers(self):
        shift_details_page = self.shift_details_page
        shift_details_page.live_server_url = self.live_server_url
        shift_details_page.navigate_to_shift_details_view()

        # verify details and slots remaining
        self.assertEqual(shift_details_page.get_shift_job(), 'job')
        self.assertEqual(shift_details_page.get_shift_date(), 'June 15, 2017')
        self.assertEqual(shift_details_page.get_max_shift_volunteer(), '6')
        self.assertEqual(shift_details_page.get_shift_start_time(), '9 a.m.')
        self.assertEqual(shift_details_page.get_shift_end_time(), '3 p.m.')

        # verify that there are no registered shifts or logged hours
        self.assertEqual(shift_details_page.get_message_box(),
            'There are currently no volunteers assigned to this shift. Please assign volunteers to view more details')

    def test_view_with_only_registered_volunteers(self):

        shift_details_page = self.shift_details_page
        shift_details_page.live_server_url = self.live_server_url
        volunteer = create_volunteer_with_details(self.volunteer_detail)
        volunteer_shift = register_volunteer_for_shift_utility(
            self.shift, volunteer)
        shift_details_page.navigate_to_shift_details_view()

        # verify that the shift slot is decreased by 1
        self.assertEqual(shift_details_page.get_shift_job(), 'job')
        self.assertEqual(shift_details_page.get_max_shift_volunteer(), '5')

        # verify that assigned volunteers shows up but no logged hours yet
        self.assertEqual(len(shift_details_page.get_registered_volunteers()), 1)
        self.assertEqual(shift_details_page.get_registered_volunteer_name(), 'Michael')
        self.assertEqual(shift_details_page.get_registered_volunteer_email(), 'volunteer@volunteer.com')
        self.assertEqual(shift_details_page.get_message_box(),'There are no logged hours at the moment')

    def test_view_with_logged_hours(self):
        shift_details_page = self.shift_details_page
        shift_details_page.live_server_url = self.live_server_url
        volunteer = create_volunteer_with_details(self.volunteer_detail)
        log_hours_with_details(volunteer, self.shift, '13:00', '14:00')
        shift_details_page.navigate_to_shift_details_view()

        # verify that the shift slot is decreased by 1
        self.assertEqual(shift_details_page.get_shift_job(), 'job')
        self.assertEqual(shift_details_page.get_max_shift_volunteer(), '5')

        # verify that assigned volunteers shows up
        self.assertEqual(len(shift_details_page.get_registered_volunteers()), 1)
        self.assertEqual(shift_details_page.get_registered_volunteer_email(), 'volunteer@volunteer.com')

        # verify that hours are logged by volunteer
        self.assertEqual(len(shift_details_page.get_logged_volunteers()), 1)
        self.assertEqual(shift_details_page.get_logged_volunteer_name(), 'Michael')
        self.assertEqual(shift_details_page.get_logged_start_time(), '1 p.m.')
        self.assertEqual(shift_details_page.get_logged_end_time(), '2 p.m.')
