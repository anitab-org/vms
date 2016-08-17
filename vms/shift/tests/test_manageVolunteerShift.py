from django.contrib.staticfiles.testing import LiveServerTestCase

from pom.pages.eventSignUpPage import EventSignUpPage
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.manageShiftPage import ManageShiftPage

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from shift.models import VolunteerShift, Shift
from shift.utils import (
    create_admin,
    create_volunteer_with_details,
    create_event_with_details,
    create_job_with_details,
    create_shift_with_details
    )

class ManageVolunteerShift(LiveServerTestCase):
    '''
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
    '''
    @classmethod
    def setUpClass(cls):

        cls.volunteer_1 = ['volunteer-one', 'volunteer-one', 'volunteer-one',
                'volunteer-one', 'volunteer-one', 'volunteer-one', 'volunteer-one',
                '9999999999', 'volunteer-email@systers.org', 'volunteer-one']
        cls.volunteer_2 = ['volunteer-two', 'volunteer-two', 'volunteer-two',
                'volunteer-two', 'volunteer-two', 'volunteer-two', 'volunteer-two',
                '9999999999', 'volunteer-email2@systers.org', 'volunteer-two']

        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.sign_up_page = EventSignUpPage(cls.driver)
        cls.manage_shift_page = ManageShiftPage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(ManageVolunteerShift, cls).setUpClass()

    def setUp(self):
        create_admin()
        self.login_admin()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(ManageVolunteerShift, cls).tearDownClass()

    def login_admin(self):
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({ 'username' : 'admin', 'password' : 'admin'})

    def create_shift(self, shift):
        # register event to create job
        event = ['event-name', '2017-05-20', '2017-05-20']
        e1 = create_event_with_details(event)

        # create job to create shift
        job = ['job name', '2017-05-20', '2017-05-20', 'job description', e1]
        j1 = create_job_with_details(job)

        # create shift to assign
        shift_1 = ['2017-05-20', shift[0], shift[1], shift[2], j1]
        s1 = create_shift_with_details(shift_1)

        return s1

    def check_job_details(self, details):
        sign_up_page = self.sign_up_page
        self.assertEqual(sign_up_page.get_shift_job(), details[0])
        self.assertEqual(sign_up_page.get_shift_date(), details[1])
        self.assertEqual(sign_up_page.get_shift_start_time(), details[2])
        self.assertEqual(sign_up_page.get_shift_end_time(), details[3])

    def test_table_layout(self):
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page

        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)

        shift = ['09:00', '15:00', '1']
        s1 = self.create_shift(shift)

        self.manage_shift_page.live_server_url = self.live_server_url
        # open manage volunteer shift
        self.manage_shift_page.navigate_to_manage_shift_page()

        # volunteer-one does not have any registered shifts
        manage_shift_page.select_volunteer(1)
        manage_shift_page.assign_shift()

        # events shown in table
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_info_box()
        self.assertEqual(sign_up_page.get_view_jobs(), 'View Jobs')
        sign_up_page.click_to_view_jobs()

        # arrived on page2 with jobs
        self.assertEqual(sign_up_page.get_view_shifts(), 'View Shifts')
        sign_up_page.click_to_view_shifts()

        # arrived on page3 with shifts, assign shift to volunteer one
        self.assertEqual(sign_up_page.get_sign_up(), 'Assign Shift')

    def test_landing_page_without_any_registered_volunteers(self):
        manage_shift_page = self.manage_shift_page
        self.manage_shift_page.live_server_url = self.live_server_url
        # open manage volunteer shift
        self.manage_shift_page.navigate_to_manage_shift_page()
        manage_shift_page.navigate_to_manage_shift_page()
        
        with self.assertRaises(NoSuchElementException):
            manage_shift_page.find_table_row()

    def test_landing_page_with_registered_volunteers(self):
        manage_shift_page = self.manage_shift_page
        self.manage_shift_page.live_server_url = self.live_server_url

        # register volunteer
        v1 = create_volunteer_with_details(self.volunteer_1)

        manage_shift_page.navigate_to_manage_shift_page()

        self.assertNotEqual(manage_shift_page.find_table_row(), None)
        manage_shift_page.select_volunteer(1)
        self.assertEqual(manage_shift_page.get_info_box(),manage_shift_page.no_volunteer_shift_message)

    def test_events_page_with_no_events(self):
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page

        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)

        self.manage_shift_page.live_server_url = self.live_server_url
        # open manage volunteer shift
        self.manage_shift_page.navigate_to_manage_shift_page()

        manage_shift_page.select_volunteer(1)
        manage_shift_page.assign_shift()

        self.assertEqual(sign_up_page.get_info_box().text,sign_up_page.no_event_message)

    def test_jobs_page_with_no_jobs(self):
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page
        self.manage_shift_page.live_server_url = self.live_server_url

        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)

        # create events
        event = ['event-name', '2017-05-20', '2017-05-20']
        e1 = create_event_with_details(event)

        # open manage volunteer shift
        manage_shift_page.navigate_to_manage_shift_page()
        manage_shift_page.select_volunteer(1)
        manage_shift_page.assign_shift()

        self.assertEqual(sign_up_page.get_info_box().text,sign_up_page.no_event_message)

    def test_assign_shifts_with_no_shifts(self):
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page
        self.manage_shift_page.live_server_url = self.live_server_url

        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)

        # create events
        event = ['event-name', '2017-05-20', '2017-05-20']
        e1 = create_event_with_details(event)

        # create jobs
        job = ['job name', '2017-05-20', '2017-05-20', 'job description', e1]
        j1 = create_job_with_details(job)

        # open manage volunteer shift
        manage_shift_page.navigate_to_manage_shift_page()
        manage_shift_page.select_volunteer(1)
        manage_shift_page.assign_shift()

        # no events shown in table
        self.assertEqual(sign_up_page.get_info_box().text,sign_up_page.no_event_message)

    def test_assign_shifts_with_registered_shifts(self):
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page
        self.manage_shift_page.live_server_url = self.live_server_url

        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)

        shift = ['09:00', '15:00', '1']
        s1 = self.create_shift(shift)

        # volunteer-one does not have any registered shifts
        manage_shift_page.navigate_to_manage_shift_page()
        manage_shift_page.select_volunteer(1)
        self.assertEqual(manage_shift_page.get_info_box(), 
            manage_shift_page.no_volunteer_shift_message)

        manage_shift_page.assign_shift()

        # events shown in table
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_info_box()
        manage_shift_page.navigate_to_shift_assignment_page()

        # confirm on shift assignment to volunteer-one
        manage_shift_page.submit_form()
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_danger_box()

        # check shift assignment to volunteer-one
        manage_shift_page.navigate_to_manage_shift_page()
        manage_shift_page.select_volunteer(1)
        self.check_job_details(['job name', 'May 20, 2017', '9 a.m.', '3 p.m.'])

        # database check to ensure volunteer has been assigned the shift
        self.assertEqual(len(VolunteerShift.objects.all()), 1)
        self.assertNotEqual(len(VolunteerShift.objects.filter(
            volunteer_id=v1.id, shift_id = s1.id)), 0)

    def test_slots_remaining_in_shift(self):
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page
        self.manage_shift_page.live_server_url = self.live_server_url

        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)
        v2 = create_volunteer_with_details(self.volunteer_2)

        shift = ['09:00', '15:00', '1']
        s1 = self.create_shift(shift)

        # open manage volunteer shift
        manage_shift_page.navigate_to_manage_shift_page()

        # volunteer-one does not have any registered shifts
        manage_shift_page.select_volunteer(1)
        self.assertEqual(manage_shift_page.get_info_box(), 
            manage_shift_page.no_volunteer_shift_message)

        manage_shift_page.assign_shift()

        # events shown in table
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_info_box()
        manage_shift_page.navigate_to_shift_assignment_page()

        # confirm on shift assignment to volunteer-one
        manage_shift_page.submit_form()
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_danger_box()

        # check shift assignment to volunteer-one
        manage_shift_page.navigate_to_manage_shift_page()
        manage_shift_page.select_volunteer(1)
        self.check_job_details(['job name', 'May 20, 2017', '9 a.m.', '3 p.m.'])

        # open manage volunteer shift again to assign shift to volunteer two
        manage_shift_page.navigate_to_manage_shift_page()

        # volunteer-two does not have any registered shifts
        manage_shift_page.select_volunteer(2)
        self.assertEqual(manage_shift_page.get_info_box(), 
            manage_shift_page.no_volunteer_shift_message)

        manage_shift_page.assign_shift()

        #no events shown in table
        self.assertEqual(sign_up_page.get_info_box().text,sign_up_page.no_event_message)
            
    def test_cancel_assigned_shift(self):
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page
        self.manage_shift_page.live_server_url = self.live_server_url

        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)

        shift = ['09:00', '15:00', '1']
        s1 = self.create_shift(shift)

        # open manage volunteer shift
        manage_shift_page.navigate_to_manage_shift_page()

        # volunteer-one does not have any registered shifts
        manage_shift_page.select_volunteer(1)
        self.assertEqual(manage_shift_page.get_info_box(), 
            manage_shift_page.no_volunteer_shift_message)

        manage_shift_page.assign_shift()

        # events shown in table
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_info_box().text
        sign_up_page.click_to_view_jobs()
        sign_up_page.click_to_view_shifts()

        # arrived on shifts page, assign shift to volunteer one
        slots_remaining_before_assignment = sign_up_page.get_remaining_slots()
        sign_up_page.click_to_sign_up()

        # confirm on shift assignment to volunteer-one
        sign_up_page.submit_form()
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_danger_box()

        # check shift assignment to volunteer-one
        manage_shift_page.navigate_to_manage_shift_page()
        manage_shift_page.select_volunteer(1)
        self.check_job_details(['job name', 'May 20, 2017', '9 a.m.', '3 p.m.'])

        # database check to ensure volunteer is registered
        self.assertEqual(len(VolunteerShift.objects.all()), 1)

        # cancel assigned shift
        self.assertEqual(manage_shift_page.get_cancel_shift().text, 'Cancel Shift Registration')
        manage_shift_page.cancel_shift()
        self.assertNotEqual(manage_shift_page.get_cancellation_box(), None)
        self.assertEqual(manage_shift_page.get_cancellation_message(), 'Yes, Cancel this Shift')
        manage_shift_page.submit_form()

        # check cancelled shift reflects in volunteer shift details
        self.assertEqual(manage_shift_page.get_info_box(),
            manage_shift_page.no_volunteer_shift_message)

        # check slots remaining increases by one, after cancellation of
        # assigned shift
        manage_shift_page.assign_shift()
        sign_up_page.click_to_view_jobs()
        sign_up_page.click_to_view_shifts()
        slots_after_cancellation = sign_up_page.get_remaining_slots()
        self.assertEqual(slots_remaining_before_assignment,
                slots_after_cancellation)

        # database check to ensure registration is cancelled
        self.assertEqual(len(VolunteerShift.objects.all()), 0)

    def test_assign_same_shift_to_volunteer_twice(self):
        sign_up_page = self.sign_up_page
        manage_shift_page = self.manage_shift_page
        self.manage_shift_page.live_server_url = self.live_server_url

        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)

        shift = ['09:00', '15:00', '1']
        s1 = self.create_shift(shift)

        # open manage volunteer shift
        manage_shift_page.navigate_to_manage_shift_page()

        # volunteer-one does not have any registered shifts
        manage_shift_page.select_volunteer(1)
        self.assertEqual(manage_shift_page.get_info_box(),
            manage_shift_page.no_volunteer_shift_message)

        manage_shift_page.assign_shift()

        # events shown in table
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_info_box()
        manage_shift_page.navigate_to_shift_assignment_page()

        # confirm on shift assignment to volunteer-one
        manage_shift_page.submit_form()
        with self.assertRaises(NoSuchElementException):
            sign_up_page.get_danger_box()

        # assign same shift to voluteer-one again
        # Check volunteer-one has one registered shift now
        self.assertEqual(sign_up_page.get_shift_job(), 'job name')
        manage_shift_page.assign_shift()

        # events page
        self.assertEqual(sign_up_page.get_info_box().text,sign_up_page.no_event_message)
