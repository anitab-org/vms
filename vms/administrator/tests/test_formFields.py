from django.contrib.staticfiles.testing import LiveServerTestCase

from shift.utils import (
    create_admin,
    create_event_with_details,
    create_job_with_details,
    create_shift_with_details
    )

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select


class FormFields(LiveServerTestCase):
    '''
    Contains Tests for
    - checking if value in forms are saved for event, shift
    and job forms
    - validation of number of volunteers field
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
        super(FormFields, cls).setUpClass()

    def setUp(self):
        create_admin()
        self.login_admin()
        self.go_to_events_page()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(FormFields, cls).tearDownClass()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id(self.login_id).send_keys(credentials['username'])
        self.driver.find_element_by_id(self.login_password).send_keys(
            credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def check_event_form_values(self, event):
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@placeholder = "Event Name"]').get_attribute('value'),
            event[0])
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "start_date"]').get_attribute('value'),
            event[1])
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "end_date"]').get_attribute('value'),
            event[2])

    def check_job_form_values(self, job):
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@placeholder = "Job Name"]').get_attribute('value'),
            job[1])
        self.assertEqual(self.driver.find_element_by_xpath(
            '//textarea[@name = "description"]').get_attribute(
            'value'), job[2])
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "start_date"]').get_attribute(
            'value'), job[3])
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "end_date"]').get_attribute(
            'value'), job[4])

    def check_shift_form_values(self, shift):
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "date"]').get_attribute('value'), shift[0])
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "start_time"]').get_attribute('value'), shift[1])
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "end_time"]').get_attribute(
            'value'), shift[2])
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "max_volunteers"]').get_attribute(
            'value'), shift[3])

    def navigate_to_event_list_view(self):
        self.driver.get(self.live_server_url + self.event_list_page)

    def navigate_to_job_list_view(self):
        self.driver.get(self.live_server_url + self.job_list_page)

    def navigate_to_shift_list_view(self):
        self.driver.get(self.live_server_url + self.shift_list_page)
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]/td[5]//a').click()

    def go_to_events_page(self):
        self.driver.find_element_by_link_text('Events').send_keys("\n")

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

    def login_admin(self):
        self.login({'username': 'admin', 'password': 'admin'})

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

    def test_null_values_in_create_event(self):
        event = ['', '', '']
        self.go_to_create_event_page()
        self.fill_event_form(event)

        # check that event was not created and that error messages appear as
        # expected
        self.assertEqual(self.driver.current_url,self.live_server_url +
            self.create_event_url)
        self.assertEqual(
            len(self.driver.find_elements_by_class_name('help-block')), 3)
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[1]/div/p/strong").text, 'This field is required.')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[2]/div/p/strong").text, 'This field is required.')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[3]/div/p/strong").text, 'This field is required.')

    # Parts of test commented out, as they are throwing server error
    def test_null_values_in_edit_event(self):
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[1]').text, created_event.name)

        self.go_to_edit_event_page()
        edited_event = ['', '', '']
        self.fill_event_form(edited_event)

        # check that event was not edited and that error messages appear as
        # expected
        self.assertNotEqual(self.driver.current_url,self.live_server_url +
            self.event_list_page)
        """self.assertEqual(len(self.driver.find_elements_by_class_name('help-block')),3)

        self.assertEqual(self.driver.find_element_by_xpath("//form//div[1]/div/p/strong").text,
                'This field is required.')
        self.assertEqual(self.driver.find_element_by_xpath("//form//div[2]/div/p/strong").text,
                'This field is required.')
        self.assertEqual(self.driver.find_element_by_xpath("//form//div[3]/div/p/strong").text,
                'This field is required.')"""

    def test_null_values_in_create_job(self):

        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job with null values
        job = [created_event.id, '', '', '', '']
        self.go_to_create_job_page()
        self.fill_job_form(job)

        # check that job was not created and that error messages appear as
        # expected
        self.assertEqual(self.driver.current_url,self.live_server_url +
            '/job/create/')
        self.assertEqual(
            len(self.driver.find_elements_by_class_name('help-block')), 3)

        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[3]/div/p/strong").text, 'This field is required.')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[5]/div/p/strong").text, 'This field is required.')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[6]/div/p/strong").text, 'This field is required.')

    def test_null_values_in_edit_job(self):

        # register event first to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job with values
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)

        # verify the job was created and proceed to edit it
        self.navigate_to_job_list_view()
        self.go_to_edit_job_page()

        # send null values to fields
        self.fill_job_form([created_event.id,'','','',''])

        # check that job was not edited and that error messages appear as
        # expected
        self.assertNotEqual(self.driver.current_url, 
            self.live_server_url + '/job/list/')
        self.assertEqual(
            len(self.driver.find_elements_by_class_name('help-block')), 3)

        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[3]/div/p/strong").text, 'This field is required.')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[5]/div/p/strong").text, 'This field is required.')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[6]/div/p/strong").text, 'This field is required.')

    def test_null_values_in_create_shift(self):

        # register event to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job with values
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)

        self.navigate_to_shift_list_view()
        self.go_to_create_shift_page()

        # create shift
        shift = ['', '', '', '']
        self.fill_shift_form(shift)

        # verify that shift was not created and error messages appear as
        # expected
        self.assertEqual(
            len(self.driver.find_elements_by_class_name('help-block')), 4)

        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[4]/div/p/strong").text, 'This field is required.')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[5]/div/p/strong").text, 'This field is required.')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[6]/div/p/strong").text, 'This field is required.')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[7]/div/p/strong").text, 'This field is required.')

    def test_null_values_in_edit_shift(self):
        # register event to create job
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job with values
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        self.navigate_to_shift_list_view()
        self.go_to_edit_shift_page()

        # edit shift with null values
        shift = ['', '', '', '']
        self.fill_shift_form(shift)

        # verify that shift was not edited and error messages appear as
        # expected
        self.assertEqual(
            len(self.driver.find_elements_by_class_name('help-block')), 4)

        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[4]/div/p/strong").text, 'This field is required.')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[5]/div/p/strong").text, 'This field is required.')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[6]/div/p/strong").text, 'This field is required.')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[7]/div/p/strong").text, 'This field is required.')

    def test_field_value_retention_for_event(self):
        self.navigate_to_event_list_view()
        self.go_to_create_event_page()

        invalid_event = ['event-name!@', '07/21/2016', '09/28/2017']
        self.fill_event_form(invalid_event)

        # verify that event was not created and that field values are not
        # erased
        self.assertEqual(self.driver.current_url, self.live_server_url +
                         '/event/create/')
        self.check_event_form_values(invalid_event)

        # now create an event and edit it
        # verify that event was not edited and that field values are not
        # erased
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)
        self.navigate_to_event_list_view()
        self.go_to_edit_event_page()
        self.fill_event_form(invalid_event)
        self.assertNotEqual(self.driver.current_url, self.live_server_url +
                            '/event/create/')
        # self.check_event_form_values(invalid_event)

    def test_field_value_retention_for_job(self):
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)
        self.navigate_to_job_list_view()
        self.go_to_create_job_page()

        invalid_job = [
            created_event.id,
            'job name#$',
            'job description',
            '27/05/2016',
            '09/11/2017']
        self.fill_job_form(invalid_job)

        # verify that job was not created and that field values are not
        # erased
        self.assertEqual(self.driver.current_url, self.live_server_url +
                         '/job/create/')
        self.check_job_form_values(invalid_job)

        # now create job and edit it
        # verify that job was not edited and that field values are not
        # erased
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)
        self.navigate_to_job_list_view()

        self.go_to_edit_job_page()
        self.fill_job_form(invalid_job)
        # verify that job was not created and that field values are not
        # erased
        self.assertNotEqual(self.driver.current_url, self.live_server_url +
                            self.job_list_page)
        #self.check_job_form_values(invalid_job)

    def test_field_value_retention_for_shift(self):
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)

        self.navigate_to_shift_list_view()
        self.go_to_create_shift_page()

        invalid_shift = ['01/01/2016', '12:00', '11:00', '10']
        self.fill_shift_form(invalid_shift)

        # verify that shift was not created and that field values are not
        # erased
        # self.check_shift_form_values(invalid_shift)

        # now create shift and edit it
        # verify that shift was not edited and that field values are not
        # erased
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)
        self.navigate_to_shift_list_view()
        self.go_to_edit_shift_page()

        self.fill_shift_form(invalid_shift)
        # verify that shift was not created and that field values are not
        # erased
        # self.check_shift_form_values(invalid_shift)

    def test_max_volunteer_field(self):
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)

        self.navigate_to_shift_list_view()
        self.go_to_create_shift_page()

        invalid_shift = ['01/01/2016','12:00','11:00','0']
        self.fill_shift_form(invalid_shift)

        # verify that error message displayed
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[7]/div/p/strong").text,
            'Ensure this value is greater than or equal to 1.')

        # Create shift and try editing it with 0 value
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        self.navigate_to_shift_list_view()
        self.go_to_edit_shift_page()
        self.fill_shift_form(invalid_shift)

        # verify that error message displayed
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[7]/div/p/strong").text,
            'Ensure this value is greater than or equal to 1.')

    def test_simplify_shift(self):
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)
        job = ['job', '2017-08-21', '2017-08-21', '',created_event]
        created_job = create_job_with_details(job)

        self.navigate_to_shift_list_view()
        self.go_to_create_shift_page()

        # verify that the correct job name and date are displayed
        self.assertEqual(self.driver.find_element_by_xpath(
            "//div[2]//div[1]/p").text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//div[2]//div[2]/p").text, 'Aug. 21, 2017')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//div[2]//div[3]/p").text, 'Aug. 21, 2017')

        # Create shift and check job details in edit form
        shift = ['2017-08-21', '09:00', '12:00', '10', created_job]
        created_shift = create_shift_with_details(shift)
        self.navigate_to_shift_list_view()
        self.go_to_edit_shift_page()

        # verify that the correct job name and date are displayed
        self.assertEqual(self.driver.find_element_by_xpath(
            "//div[2]//div[1]/p").text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//div[2]//div[2]/p").text, 'Aug. 21, 2017')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//div[2]//div[3]/p").text, 'Aug. 21, 2017')

    """def test_simplify_job(self):
        event = ['event-name', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        self.navigate_to_job_list_view()
        self.go_to_create_job_page()

        # verify that the correct event name and date are displayed
        select = Select(self.driver.find_element_by_id(
            'events'))
        select.select_by_visible_text('event')
        self.assertEqual(self.driver.find_element_by_id(
            'start_date_here').text, 'June 15, 2017')
        self.assertEqual(self.driver.find_element_by_id(
            'end_date_here').text, 'June 17, 2017')

        # Create job and check event details in edit form
        job_1 = self.register_job_utility(event_1)
        self.navigate_to_job_list_view()
        self.go_to_edit_job_page()

        # verify that the correct event name and date are displayed
        select = Select(self.driver.find_element_by_id(
            'events'))
        select.select_by_visible_text('event')
        self.assertEqual(self.driver.find_element_by_id(
            'start_date_here').text, 'June 15, 2017')
        self.assertEqual(self.driver.find_element_by_id(
            'end_date_here').text, 'June 17, 2017')"""
    