from django.contrib.staticfiles.testing import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

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
        cls.homepage = '/'
        cls.shift_page = '/shift/volunteer_search/'
        cls.authentication_page = '/authentication/login/'
        cls.settings_page = '/event/list/'

        cls.volunteer_1 = ['volunteer-one', 'volunteer-one', 'volunteer-one',
                'volunteer-one', 'volunteer-one', 'volunteer-one', 'volunteer-one',
                '9999999999', 'volunteer-email@systers.org', 'volunteer-one']
        cls.volunteer_2 = ['volunteer-two', 'volunteer-two', 'volunteer-two',
                'volunteer-two', 'volunteer-two', 'volunteer-two', 'volunteer-two',
                '9999999999', 'volunteer-email2@systers.org', 'volunteer-two']

        cls.job_name_path = '//table//tbody//tr[1]//td[1]'
        cls.job_date_path = '//table//tbody//tr[1]//td[2]'
        cls.job_stime_path = '//table//tbody//tr[1]//td[3]'
        cls.job_etime_path = '//table//tbody//tr[1]//td[4]'
        cls.view_jobs_path = '//table//tbody//tr[1]//td[4]'
        cls.view_shifts_path = '//table//tbody//tr[1]//td[4]'
        cls.assign_shifts_path = '//table//tbody//tr[1]//td[4]'
        cls.slots_remaining_path = '//table//tbody//tr[1]//td[5]'
        cls.cancel_shift_path = '//table//tbody//tr[1]//td[5]'

        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        super(ManageVolunteerShift, cls).setUpClass()

    def setUp(self):
        create_admin()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(ManageVolunteerShift, cls).tearDownClass()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys(credentials['username'])
        self.driver.find_element_by_id('id_password').send_keys(credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def navigate_to_manage_shift_page(self):
        self.driver.find_element_by_link_text('Manage Volunteer Shifts').click()
        self.assertEqual(self.driver.current_url,
                self.live_server_url + self.shift_page)

    def login_admin(self):
        self.login({ 'username' : 'admin', 'password' : 'admin'})

    def select_volunteer(self, number):
        link_path = '//table//tbody//tr[' + str(number) + ']//td[10]//a'
        self.driver.find_element_by_xpath(link_path).click()

    def navigate_to_shift_assignment_page(self):
        self.driver.find_element_by_xpath(
                self.view_jobs_path + "//a").click()
        self.driver.find_element_by_xpath(
                self.view_shifts_path + "//a").click()
        self.driver.find_element_by_xpath(
                self.assign_shifts_path + "//a").click()

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
        self.assertEqual(self.driver.find_element_by_xpath(
            self.job_name_path).text, details[0])
        self.assertEqual(self.driver.find_element_by_xpath(
            self.job_date_path).text, details[1])
        self.assertEqual(self.driver.find_element_by_xpath(
            self.job_stime_path).text, details[2])
        self.assertEqual(self.driver.find_element_by_xpath(
            self.job_etime_path).text, details[3])

    def assign_shift(self):
        self.driver.find_element_by_link_text('Assign Shift').click()

    def test_table_layout(self):
        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)

        shift = ['09:00', '15:00', '1']
        s1 = self.create_shift(shift)

        self.login_admin()
        # open manage volunteer shift
        self.navigate_to_manage_shift_page()

        # volunteer-one does not have any registered shifts
        self.select_volunteer(1)
        self.assign_shift()

        # events shown in table
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-info')
        self.assertEqual(self.driver.find_element_by_xpath(
            self.view_jobs_path).text, 'View Jobs')
        self.driver.find_element_by_xpath(
                self.view_jobs_path + "//a").click()

        # arrived on page2 with jobs
        self.assertEqual(self.driver.find_element_by_xpath(
            self.view_shifts_path).text, 'View Shifts')
        self.driver.find_element_by_xpath(
                self.view_shifts_path + "//a").click()

        # arrived on page3 with shifts, assign shift to volunteer one
        self.assertEqual(self.driver.find_element_by_xpath(
            self.assign_shifts_path).text, 'Assign Shift')

    def test_landing_page_without_any_registered_volunteers(self):
        self.login_admin()
        self.navigate_to_manage_shift_page()
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_tag_name('tr')

    def test_landing_page_with_registered_volunteers(self):
        # register volunteer
        v1 = create_volunteer_with_details(self.volunteer_1)

        # login admin user
        self.login_admin()
        self.navigate_to_manage_shift_page()

        self.assertNotEqual(self.driver.find_element_by_tag_name('tr'), None)
        self.select_volunteer(1)
        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text,
               'This volunteer does not have any upcoming shifts.')

    def test_events_page_with_no_events(self):
        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)

        # login admin user
        self.login_admin()
        self.navigate_to_manage_shift_page()

        self.select_volunteer(1)
        self.assign_shift()

        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text,
               'There are no events.')

    def test_jobs_page_with_no_jobs(self):
        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)

        # create events
        event = ['event-name', '2017-05-20', '2017-05-20']
        e1 = create_event_with_details(event)

        # login admin
        self.login_admin()
        # open manage volunteer shift
        self.navigate_to_manage_shift_page()
        self.select_volunteer(1)
        self.assign_shift()

        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text,'There are no events.')

    def test_assign_shifts_with_no_shifts(self):
        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)

        # create events
        event = ['event-name', '2017-05-20', '2017-05-20']
        e1 = create_event_with_details(event)

        # create jobs
        job = ['job name', '2017-05-20', '2017-05-20', 'job description', e1]
        j1 = create_job_with_details(job)

        # login admin
        self.login_admin()
        # open manage volunteer shift
        self.navigate_to_manage_shift_page()
        self.select_volunteer(1)
        self.assign_shift()

        # no events shown in table
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text,'There are no events.')

    def test_assign_shifts_with_registered_shifts(self):
        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)

        shift = ['09:00', '15:00', '1']
        s1 = self.create_shift(shift)

        self.login_admin()
        # open manage volunteer shift
        self.navigate_to_manage_shift_page()

        # volunteer-one does not have any registered shifts
        self.select_volunteer(1)
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text, 
            'This volunteer does not have any upcoming shifts.')

        self.assign_shift()

        # events shown in table
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-info')
        self.navigate_to_shift_assignment_page()

        # confirm on shift assignment to volunteer-one
        self.driver.find_element_by_xpath('//form[1]').submit()
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-danger')

        # check shift assignment to volunteer-one
        self.navigate_to_manage_shift_page()
        self.select_volunteer(1)
        self.check_job_details(['job name', 'May 20, 2017', '9 a.m.', '3 p.m.'])

    def test_slots_remaining_in_shift(self):
        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)
        v2 = create_volunteer_with_details(self.volunteer_2)

        shift = ['09:00', '15:00', '1']
        s1 = self.create_shift(shift)

        self.login_admin()
        # open manage volunteer shift
        self.navigate_to_manage_shift_page()

        # volunteer-one does not have any registered shifts
        self.select_volunteer(1)
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text, 
            'This volunteer does not have any upcoming shifts.')

        self.assign_shift()

        # events shown in table
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-info')
        self.navigate_to_shift_assignment_page()

        # confirm on shift assignment to volunteer-one
        self.driver.find_element_by_xpath('//form[1]').submit()
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-danger')

        # check shift assignment to volunteer-one
        self.navigate_to_manage_shift_page()
        self.select_volunteer(1)
        self.check_job_details(['job name', 'May 20, 2017', '9 a.m.', '3 p.m.'])

        # open manage volunteer shift again to assign shift to volunteer two
        self.navigate_to_manage_shift_page()

        # volunteer-two does not have any registered shifts
        self.select_volunteer(2)
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text, 
            'This volunteer does not have any upcoming shifts.')

        self.assign_shift()

        #no events shown in table
        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text,
            'There are no events.')
            
    def test_cancel_assigned_shift(self):
        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)

        shift = ['09:00', '15:00', '1']
        s1 = self.create_shift(shift)

        self.login_admin()
        # open manage volunteer shift
        self.navigate_to_manage_shift_page()

        # volunteer-one does not have any registered shifts
        self.select_volunteer(1)
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text, 
            'This volunteer does not have any upcoming shifts.')

        self.assign_shift()

        # events shown in table
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-info')
        self.driver.find_element_by_xpath(
                self.view_jobs_path + "//a").click()
        self.driver.find_element_by_xpath(
                self.view_shifts_path + "//a").click()

        # arrived on shifts page, assign shift to volunteer one
        slots_remaining_before_assignment = self.driver.find_element_by_xpath(
                self.slots_remaining_path).text
        self.driver.find_element_by_xpath(
                self.assign_shifts_path + "//a").click()

        # confirm on shift assignment to volunteer-one
        self.driver.find_element_by_xpath('//form[1]').submit()
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-danger')

        # check shift assignment to volunteer-one
        self.navigate_to_manage_shift_page()
        self.select_volunteer(1)
        self.check_job_details(['job name', 'May 20, 2017', '9 a.m.', '3 p.m.'])

        # cancel assigned shift
        self.assertEqual(self.driver.find_element_by_xpath(
            self.cancel_shift_path).text, 'Cancel Shift Registration')
        self.driver.find_element_by_xpath(
                self.cancel_shift_path + "//a").click()
        self.assertNotEqual(self.driver.find_element_by_class_name(
            'panel-danger'), None)
        self.assertEqual(self.driver.find_element_by_class_name(
            'btn-danger').text, 'Yes, Cancel this Shift')
        self.driver.find_element_by_xpath('//form[1]').submit()

        # check cancelled shift reflects in volunteer shift details
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text,
            'This volunteer does not have any upcoming shifts.')

        # check slots remaining increases by one, after cancellation of
        # assigned shift
        self.assign_shift()
        self.driver.find_element_by_xpath(
                self.view_jobs_path + "//a").click()
        self.driver.find_element_by_xpath(
                self.view_shifts_path + "//a").click()
        slots_after_cancellation = self.driver.find_element_by_xpath(
                self.slots_remaining_path).text
        self.assertEqual(slots_remaining_before_assignment,
                slots_after_cancellation)

    def test_assign_same_shift_to_volunteer_twice(self):
        # register volunteers
        v1 = create_volunteer_with_details(self.volunteer_1)

        shift = ['09:00', '15:00', '1']
        s1 = self.create_shift(shift)

        self.login_admin()
        # open manage volunteer shift
        self.navigate_to_manage_shift_page()

        # volunteer-one does not have any registered shifts
        self.select_volunteer(1)
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-info').text, 
            'This volunteer does not have any upcoming shifts.')

        self.assign_shift()

        # events shown in table
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-info')
        self.navigate_to_shift_assignment_page()

        # confirm on shift assignment to volunteer-one
        self.driver.find_element_by_xpath('//form[1]').submit()
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('alert-danger')

        # assign same shift to voluteer-one again
        # Check volunteer-one has one registered shift now
        self.assertEqual(self.driver.find_element_by_xpath(
            self.job_name_path).text, 'job name')
        self.assign_shift()

        # events page
        self.assertEqual(self.driver.find_element_by_class_name('alert-info').text, 'There are no events.')
