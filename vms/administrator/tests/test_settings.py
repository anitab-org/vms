from django.contrib.staticfiles.testing import LiveServerTestCase

from shift.utils import (
    create_admin,
    create_event_with_details,
    create_job_with_details,
    create_shift_with_details,
    create_volunteer,
    register_volunteer_for_shift_utility,
    create_organization
    )

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Settings(LiveServerTestCase):
    '''
    Settings Class contains UI testcases for `Events` tab in
    Administrator profile. This view consists of Events, Jobs, Shifts,
    Organization tabs.

    Event:
        - Null values in Create and edit event form
        - Create Event
        - Edit Event
        - Delete Event with No Associated Job
        - Delete event with Associated Job

    Job:
        - Null values in Create and edit job form
        - Create Job without any event
        - Edit Job
        - Create/Edit Job with invalid dates
        - Delete Job without Associated Shift
        - Delete Job with Shifts

    Shift:
        - Null values in Create and edit shift form
        - Create Shift without any Job
        - Edit Shift
        - Delete shift
        - Delete shift with volunteer
        - Create/Edit Shift with invalid timing
        - Create/Edit Shift with invalid date

    Organization:
        - Create Organization
        - Edit Organization
        - Replication of Organization
        - Delete Org's with registered volunteers
        - Delete Org without registered volunteers

    Additional Note:
    It needs to be ensured that the dates in the test functions
    given below are later than the current date so that there are no
    failures while creating an event. Due to this reason, the date
    at several places has been updated to 2017
    '''

    @classmethod
    def setUpClass(cls):
        cls.homepage = '/'
        cls.authentication_page = '/authentication/login/'
        cls.event_list_page = '/event/list/'

        cls.job_list_page = '/job/list/'
        cls.shift_list_page = '/shift/list_jobs/'
        cls.login_id = 'id_login'
        cls.login_password = 'id_password'

        cls.create_event_name ='//input[@placeholder = "Event Name"]'
        cls.create_event_start_date = '//input[@name = "start_date"]'
        cls.create_event_end_date = '//input[@name = "end_date"]'
        cls.create_event_id = '//select[@name = "event_id"]'
        cls.create_job_name = '//input[@placeholder = "Job Name"]'
        cls.create_job_description = '//textarea[@name = "description"]'
        cls.create_job_start_date = '//input[@name = "start_date"]'
        cls.create_job_end_date = '//input[@name = "end_date"]'
        cls.create_shift_date = '//input[@name = "date"]'
        cls.create_shift_start_time = '//input[@name = "start_time"]'
        cls.create_shift_end_time = '//input[@name = "end_time"]'
        cls.create_shift_max_volunteer = '//input[@name = "max_volunteers"]'

        cls.create_event_url = '/event/create/'

        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        super(Settings, cls).setUpClass()

    def setUp(self):
        create_admin()
        self.login_admin()
        self.go_to_events_page()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(Settings, cls).tearDownClass()

    def login_admin(self):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys('admin')
        self.driver.find_element_by_id('id_password').send_keys('admin')
        self.driver.find_element_by_xpath('//form[1]').submit()

    def delete_event_from_list(self):
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[6]').text, 'Delete')
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[6]//a').click()
        self.assertNotEqual(self.driver.find_element_by_class_name(
            'panel-danger'), None)
        self.assertEqual(self.driver.find_element_by_class_name(
            'panel-heading').text, 'Delete Event')
        self.driver.find_element_by_xpath('//form').submit()

    def delete_job_from_list(self):
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[7]').text, 'Delete')
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[7]//a').click()

        self.assertNotEqual(self.driver.find_element_by_class_name(
            'panel-danger'), None)
        self.assertEqual(self.driver.find_element_by_class_name(
            'panel-heading').text, 'Delete Job')
        self.driver.find_element_by_xpath('//form').submit()

    def delete_shift_from_list(self):
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[6]').text, 'Delete')
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[6]//a').click()

        # confirm on delete
        self.assertNotEqual(
            self.driver.find_element_by_class_name('panel-danger'), None)
        self.assertEqual(self.driver.find_element_by_class_name(
            'panel-heading').text, 'Delete Shift')
        self.driver.find_element_by_xpath('//form').submit()

    def delete_organization_from_list(self):
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[3]').text, 'Delete')
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[3]//a').click()

        # confirm on delete
        self.assertNotEqual(self.driver.find_element_by_class_name(
            'panel-danger'), None)
        self.assertEqual(self.driver.find_element_by_class_name(
            'panel-heading').text, 'Delete Organization')
        self.driver.find_element_by_xpath('//form').submit()

    def fill_event_form(self, event):
        self.driver.find_element_by_xpath(
            self.create_event_name).clear()
        self.driver.find_element_by_xpath(
            self.create_event_start_date).clear()
        self.driver.find_element_by_xpath(
            self.create_event_end_date).clear()
        self.driver.find_element_by_xpath(
            self.create_event_name).send_keys(
            event[0])
        self.driver.find_element_by_xpath(
            self.create_event_start_date).send_keys(
            event[1])
        self.driver.find_element_by_xpath(
            self.create_event_end_date).send_keys(
            event[2])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def fill_job_form(self, job):
        self.driver.find_element_by_xpath(
            self.create_job_name).clear()
        self.driver.find_element_by_xpath(
            self.create_job_description).clear()
        self.driver.find_element_by_xpath(
            self.create_job_start_date).clear()
        self.driver.find_element_by_xpath(
            self.create_job_end_date).clear()

        self.driver.find_element_by_xpath(
            self.create_event_id).send_keys(
            job[0])
        self.driver.find_element_by_xpath(
            self.create_job_name).send_keys(
            job[1])
        self.driver.find_element_by_xpath(
            self.create_job_description).send_keys(
            job[2])
        self.driver.find_element_by_xpath(
            self.create_job_start_date).send_keys(
            job[3])
        self.driver.find_element_by_xpath(
            self.create_job_end_date).send_keys(
            job[4])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def fill_shift_form(self, shift):
        self.driver.find_element_by_xpath(
            self.create_shift_date).clear()
        self.driver.find_element_by_xpath(
            self.create_shift_start_time).clear()
        self.driver.find_element_by_xpath(
            self.create_shift_end_time).clear()
        self.driver.find_element_by_xpath(
            self.create_shift_max_volunteer).clear()

        self.driver.find_element_by_xpath(
            self.create_shift_date).send_keys(
            shift[0])
        self.driver.find_element_by_xpath(
            self.create_shift_start_time).send_keys(
            shift[1])
        self.driver.find_element_by_xpath(
            self.create_shift_end_time).send_keys(
            shift[2])
        self.driver.find_element_by_xpath(
            self.create_shift_max_volunteer).send_keys(
            shift[3])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def fill_organization_form(self, org):
        self.driver.find_element_by_xpath(
            '//input[@name = "name"]').clear()
        self.driver.find_element_by_xpath('//input[@name = "name"]').send_keys(
            org)
        self.driver.find_element_by_xpath('//form[1]').submit()

    def go_to_events_page(self):
        self.driver.find_element_by_link_text('Events').send_keys("\n")

    def navigate_to_event_list_view(self):
        self.driver.get(self.live_server_url + self.event_list_page)

    def navigate_to_job_list_view(self):
        self.driver.get(self.live_server_url + self.job_list_page)

    def navigate_to_shift_list_view(self):
        self.driver.get(self.live_server_url + self.shift_list_page)
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]/td[5]//a').click()

    def navigate_to_organization_view(self):
        self.driver.get(self.live_server_url +'/organization/list/')

    def go_to_create_event_page(self):
        self.driver.find_element_by_link_text('Create Event').click()
        self.assertEqual(self.driver.current_url,self.live_server_url +
            '/event/create/')

    def go_to_edit_event_page(self):
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]').text, 'Edit')
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]//a').click()

    def go_to_create_job_page(self):
        self.driver.get(self.live_server_url +'/job/create/')

    def go_to_edit_job_page(self):
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[6]').text, 'Edit')
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[6]//a').click()

    def go_to_create_shift_page(self):
        self.driver.find_element_by_link_text('Create Shift').click()

    def go_to_edit_shift_page(self):
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]').text, 'Edit')
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]//a').click()

    def go_to_create_organization_page(self):
        self.driver.get(self.live_server_url + '/organization/create/')

    def test_event_tab(self):
        self.assertNotEqual(
            self.driver.find_element_by_link_text('Events'), None)
        self.assertEqual(
            self.driver.find_element_by_class_name('alert-success').text,
            'There are currently no events. Please create events first.')

    def test_job_tab_and_create_job_without_event(self):
        self.driver.find_element_by_link_text('Jobs').click()
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + '/job/list/')
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-success').text,
            'There are currently no jobs. Please create jobs first.')

        self.driver.find_element_by_link_text('Create Job').click()
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + '/job/create/')
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-success').text,
            'Please add events to associate with jobs first.')

    def test_shift_tab_and_create_shift_without_job(self):
        self.driver.find_element_by_link_text('Shifts').click()
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + '/shift/list_jobs/')
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-success').text,
            'There are currently no jobs. Please create jobs first.')

    def test_create_event(self):
        event = ['event-name', '2017-08-21', '2017-09-28']
        self.go_to_create_event_page()
        self.fill_event_form(event)

        # check event created
        self.assertEqual(self.driver.current_url,
            self.live_server_url + self.event_list_page)
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'event-name')

    # - commented out due to bug - desirable feature not yet implemented
    """def test_duplicate_event(self):
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # check event created
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + self.settings_page)
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'event-name')

        self.go_to_create_event_page()
        self.fill_event_form(event)

        # TBA here - more checks depending on behaviour that should be reflected
        # check event not created 
        self.assertNotEqual(self.driver.current_url,
                            self.live_server_url + self.settings_page)"""

    def test_edit_event(self):
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create event
        self.navigate_to_event_list_view()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, created_event.name)

        self.go_to_edit_event_page()

        edited_event = ['new-event-name', '2017-09-21', '2017-09-28']
        self.fill_event_form(edited_event)

        # check event edited
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + self.event_list_page)
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'new-event-name')

    def test_create_and_edit_event_with_invalid_start_date(self):
        
        self.go_to_create_event_page()
        invalid_event = ['event-name', '05/17/2016', '09/28/2016']
        self.fill_event_form(invalid_event)

        # check event not created and error message displayed
        self.assertNotEqual(self.driver.current_url,
            self.live_server_url + self.event_list_page)
        self.assertEqual(
            self.driver.find_element_by_class_name('messages').text,
            "Start date should be today's date or later.")

        self.navigate_to_event_list_view()
        self.go_to_create_event_page()
        valid_event = ['event-name', '2017-05-21', '2017-09-28']
        valid_event_created = create_event_with_details(valid_event)

        self.navigate_to_event_list_view()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, valid_event_created.name)

        self.go_to_edit_event_page()
        self.fill_event_form(invalid_event)

        # check event not edited and error message displayed
        self.assertNotEqual(self.driver.current_url,
            self.live_server_url +self.event_list_page)
        self.assertEqual(
            self.driver.find_element_by_class_name('messages').text,
            "Start date should be today's date or later.")

    def test_edit_event_with_elapsed_start_date(self):
        elapsed_event = ['event-name', '2016-05-21', '2017-08-09']

        # Create an event with elapsed start date
        created_event = create_event_with_details(elapsed_event)

        self.navigate_to_event_list_view()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, created_event.name)

        self.go_to_edit_event_page()

        # Try editing any one field - (event name in this case)
        self.driver.find_element_by_xpath(
            '//input[@placeholder = "Event Name"]').clear()
        self.driver.find_element_by_xpath(
            '//input[@placeholder = "Event Name"]').send_keys(
            'changed-event-name')

        self.driver.find_element_by_xpath('//form[1]').submit()

        # check event not edited
        self.assertNotEqual(self.driver.current_url,
            self.live_server_url + self.event_list_page)

        # Test for proper msg TBA later once it is implemented

    def test_edit_event_with_invalid_job_date(self):
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)

        self.navigate_to_event_list_view()

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, created_event.name)
        self.go_to_edit_event_page()

        # Edit event such that job is no longer in the new date range
        new_event = ['event-name', '2017-08-30', '2017-09-21']
        self.fill_event_form(new_event)

        # check event not edited and error message displayed
        self.assertNotEqual(self.driver.current_url,
            self.live_server_url + self.event_list_page)
        self.assertEqual(
            self.driver.find_element_by_xpath('//div[2]/div[3]/p').text,
            'You cannot edit this event as the following associated job no longer lies within the new date range :')

    def test_delete_event_with_no_associated_job(self):
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create event
        self.navigate_to_event_list_view()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, created_event.name)

        self.delete_event_from_list()

        # check event deleted
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + self.event_list_page)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_xpath('//table//tbody')

    def test_delete_event_with_associated_job(self):
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)

        # check event created
        self.navigate_to_event_list_view()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, created_event.name)

        # delete event
        self.delete_event_from_list()

        self.assertNotEqual(self.driver.find_element_by_class_name(
            'alert-danger'), None)
        self.assertEqual(
            self.driver.find_element_by_xpath('//div[2]/div[3]/p').text,
            'You cannot delete an event that a job is currently associated with.')

        # check event NOT deleted
        self.driver.get(self.live_server_url + self.event_list_page)
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'event-name')

    def test_create_job(self):

        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['event-name','job name','job description',
            '2017-08-21', '2017-08-28']
        self.go_to_create_job_page()
        self.fill_job_form(job)

        # check job created
        self.navigate_to_job_list_view()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'job name')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[2]').text, created_event.name)

    # - commented out due to bug - desirable feature not yet implemented
    """def test_duplicate_job(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['event-name','job name','job description',
            '2017-08-21', '2017-08-28']
        create_job_with_details(job))

        # check job created
        self.navigate_to_job_list_view()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'job name')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[2]').text, 'event-name')

        # Create another job with same details within the same event
        self.go_to_create_job_page()
        self.fill_job_form(job)

        # TBA here - more checks depending on logic that should be reflected
        # check job not created - commented out due to bug
        self.assertNotEqual(self.driver.current_url,
                            self.live_server_url + '/job/list/')"""

    def test_edit_job(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)

        edit_job = ['event-name','changed job name','job description',
            '2017-08-25', '2017-08-25']
        self.navigate_to_job_list_view()
        self.go_to_edit_job_page()
        self.fill_job_form(edit_job)

        # check job edited
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + '/job/list/')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'changed job name')

    def test_create_job_with_invalid_event_date(self):

        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job with start date outside range
        job = ['event-name','job name',
            'job description','08/10/2017',
            '09/11/2017']
        self.go_to_create_job_page()
        self.fill_job_form(job)

        # check job not created and proper error message displayed
        self.assertNotEqual(self.driver.current_url,
            self.live_server_url + '/job/list/')
        self.assertEqual(self.driver.find_element_by_class_name(
            'messages').text, 'Job dates should lie within Event dates')

        self.navigate_to_event_list_view()

        # create job with end date outside range
        job = [
            'event-name',
            'job name',
            'job description',
            '08/30/2017',
            '09/11/2018']
        self.go_to_create_job_page()
        self.fill_job_form(job)

        # check job not created and proper error message displayed
        self.assertNotEqual(self.driver.current_url,self.live_server_url +
            '/job/list/')
        self.assertEqual(self.driver.find_element_by_class_name(
            'messages').text, 'Job dates should lie within Event dates')

    def test_edit_job_with_invalid_event_date(self):

        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)

        invalid_job_one = ['event-name','changed job name','job description',
            '2017-05-03', '2017-11-09']

        # edit job with start date outside event start date
        self.navigate_to_job_list_view()
        self.go_to_edit_job_page()
        self.fill_job_form(invalid_job_one)

        # check job not edited and proper error message displayed
        self.assertNotEqual(self.driver.current_url,
            self.live_server_url +'/job/list/')
        self.assertEqual(self.driver.find_element_by_class_name(
            'messages').text, 'Job dates should lie within Event dates')

        invalid_job_two = ['event-name','changed job name','job description',
            '2017-09-14', '2017-12-31']
        self.navigate_to_job_list_view()
        self.go_to_edit_job_page()
        self.fill_job_form(invalid_job_two)

        # check job not edited and proper error message displayed
        self.assertNotEqual(self.driver.current_url,
            self.live_server_url +'/job/list/')
        self.assertEqual(self.driver.find_element_by_class_name(
            'messages').text, 'Job dates should lie within Event dates')

    def test_edit_job_with_invalid_shift_date(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        self.navigate_to_job_list_view()

        invalid_job_one = ['event-name','changed job name','job description',
            '2017-09-01', '2017-09-11']

        # edit job with date range such that the shift start date no longer
        # falls in the range
        self.go_to_edit_job_page()
        self.fill_job_form(invalid_job_one)

        # check job not edited and proper error message displayed
        self.assertNotEqual(self.driver.current_url,
            self.live_server_url +'/job/list/')
        self.assertEqual(
            self.driver.find_element_by_xpath('//div[2]/div[3]/p').text,
            'You cannot edit this job as 1 associated shift no longer lies within the new date range')

    def test_delete_job_without_associated_shift(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)

        # check job created
        self.navigate_to_job_list_view()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[2]').text, 'event-name')

        # delete job
        self.delete_job_from_list()

        # check event deleted
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + '/job/list/')
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_xpath('//table//tbody')

    def test_delete_job_with_associated_shifts(self):

        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        # delete job
        self.navigate_to_job_list_view()
        self.delete_job_from_list()

        self.assertNotEqual(self.driver.find_element_by_class_name(
            'alert-danger'), None)
        self.assertEqual(
            self.driver.find_element_by_xpath('//div[2]/div[3]/p').text,
            'You cannot delete a job that a shift is currently associated with.')

        # check job NOT deleted
        self.navigate_to_job_list_view()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'job')

    def test_create_shift(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        self.navigate_to_shift_list_view()
        self.go_to_create_shift_page()

        shift = ['08/30/2017', '09:00', '12:00', '10']
        self.fill_shift_form(shift)

        # verify that shift was created
        self.assertNotEqual(
            self.driver.find_elements_by_xpath('//table//tbody'), None)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('help-block')

    def test_create_shift_with_invalid_timings(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        self.navigate_to_shift_list_view()
        self.go_to_create_shift_page()

        # create shift where end hours is less than start hours
        shift = ['08/30/2017', '14:00', '12:00', '5']
        self.fill_shift_form(shift)

        # verify that shift was not created and error message displayed
        self.assertEqual(
            self.driver.find_element_by_class_name('messages').text,
            'Shift end time should be greater than start time')

    def test_edit_shift_with_invalid_timings(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        self.navigate_to_shift_list_view()
        self.go_to_edit_shift_page()

        # edit shift with end hours less than start hours
        invalid_shift = ['08/30/2017', '18:00', '13:00', '5']
        self.fill_shift_form(invalid_shift)

        # verify that shift was not edited and error message displayed
        self.assertEqual(
            self.driver.find_element_by_class_name('messages').text,
            'Shift end time should be greater than start time')

    def test_create_shift_with_invalid_date(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        self.navigate_to_shift_list_view()
        self.go_to_create_shift_page()

        shift = ['06/30/2017', '14:00', '18:00', '5']
        self.fill_shift_form(shift)

        # verify that shift was not created and error message displayed
        self.assertEqual(self.driver.find_element_by_class_name(
            'messages').text, 'Shift date should lie within Job dates')

    def test_edit_shift_with_invalid_date(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        self.navigate_to_shift_list_view()
        self.go_to_edit_shift_page()

        # edit shift with date not between job dates
        invalid_shift = ['02/05/2017', '04:00', '13:00', '2']
        self.fill_shift_form(invalid_shift)

        # verify that shift was not edited and error message displayed
        self.assertEqual(self.driver.find_element_by_class_name(
            'messages').text, 'Shift date should lie within Job dates')

    def test_edit_shift(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        self.navigate_to_shift_list_view()
        self.go_to_edit_shift_page()

        # edit shift with date not between job dates
        shift = ['08/25/2017', '10:00', '13:00', '2']
        self.fill_shift_form(shift)

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_class_name('help-block')

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'Aug. 25, 2017')

    def test_delete_shift(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        self.navigate_to_shift_list_view()
        self.assertNotEqual(
            self.driver.find_elements_by_xpath('//table//tbody'), None)

        # delete shift
        self.delete_shift_from_list()

        # check deletion of shift
        self.navigate_to_shift_list_view()
        self.assertEqual(
            self.driver.find_element_by_class_name('alert-success').text,
            'There are currently no shifts. Please create shifts first.')

    def test_delete_shift_with_volunteer(self):
        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['job', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        # create volunteer for shift
        volunteer = create_volunteer()
        shift_volunteer = register_volunteer_for_shift_utility(
            created_shift, volunteer)

        self.navigate_to_shift_list_view()

        # delete shift
        self.delete_shift_from_list()

        # check error message displayed and shift not deleted
        self.assertEqual(
            self.driver.find_element_by_xpath("//div[2]/div[3]/p").text,
            'You cannot delete a shift that a volunteer has signed up for.')

    def test_organization(self):

        self.driver.find_element_by_link_text('Organizations').click()
        self.assertEqual(self.driver.current_url,
            self.live_server_url +'/organization/list/')

        self.driver.find_element_by_link_text('Create Organization').click()
        self.assertEqual(self.driver.current_url,
            self.live_server_url +'/organization/create/')

        # Test all valid characters for organization
        # [(A-Z)|(a-z)|(0-9)|(\s)|(\-)|(:)]
        self.fill_organization_form('Org-name 92:4 CA')
        # tr[2] since one dummy org already created in Setup, due to code-bug
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'Org-name 92:4 CA')

    def test_replication_of_organization(self):
        self.navigate_to_organization_view()
        self.go_to_create_organization_page()

        self.fill_organization_form('Organization')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, 'Organization')

        # Create same orgnization again
        self.go_to_create_organization_page()
        self.fill_organization_form('Organization')

        self.assertEqual(self.driver.find_element_by_xpath(
            '//p[@class = "help-block"]').text,
            'Organization with this Name already exists.')

    def test_edit_org(self):
        # create org
        org = create_organization()
        self.navigate_to_organization_view()

        # edit org
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[2]').text, 'Edit')
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[2]//a').click()

        self.fill_organization_form('changed-organization')

        # check edited org
        org_list = []
        org_list.append(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text)

        self.assertTrue('changed-organization' in org_list)

    def test_delete_org_without_associated_users(self):
        # create org
        org = create_organization()
        self.navigate_to_organization_view()

        # delete org
        self.delete_organization_from_list()

        # check org deleted
        # There should only be one org entry in the table shown.
        # One, because of dummy-org inserted in setUp and not zero
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_xpath('//table//tbody//tr[1]')

    def test_delete_org_with_associated_users(self):
        # create org
        org = create_organization()
        volunteer = create_volunteer()

        volunteer.organization = org
        volunteer.save()

        # delete org
        self.navigate_to_organization_view()
        self.delete_organization_from_list()

        # check org not deleted message received
        self.assertNotEqual(self.driver.find_element_by_class_name(
            'alert-danger'), None)
        self.assertEqual(
            self.driver.find_element_by_xpath('//div[2]/div[3]/p').text,
            'You cannot delete an organization that users are currently associated with.')
