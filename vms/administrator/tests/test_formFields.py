from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User
from administrator.models import Administrator
from volunteer.models import Volunteer
from event.models import Event
from job.models import Job
from shift.models import Shift, VolunteerShift

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

    def setUp(self):
        admin_user = User.objects.create_user(
            username='admin',
            password='admin')

        Administrator.objects.create(
            user=admin_user,
            address='address',
            city='city',
            state='state',
            country='country',
            email='admin@admin.com',
            phone_number='9999999999',
            unlisted_organization='organization')

        self.homepage = '/'
        self.authentication_page = '/authentication/login/'
        self.event_list_page = '/event/list/'
        self.job_list_page = '/job/list/'
        self.shift_list_page = '/shift/list_jobs/'
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        super(FormFields, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(FormFields, self).tearDown()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id(
            'id_login').send_keys(credentials['username'])
        self.driver.find_element_by_id('id_password').send_keys(
            credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def register_volunteer_utility(self, name, number):
        volunteer_user = User.objects.create_user(
            username=name,
            password='volunteer')

        e_id = 'volunteer@volunteer' + str(number)

        volunteer = Volunteer.objects.create(
            user=volunteer_user,
            first_name='Michael',
            last_name='Reed',
            address='address',
            city='city',
            state='state',
            country='country',
            phone_number='9999999999',
            email=e_id,
            unlisted_organization='organization')

        return volunteer

    def register_event_utility(self, ):

        event = Event.objects.create(
            name='event',
            start_date='2017-06-15',
            end_date='2017-06-17')

        return event

    def register_job_utility(self, event):

        job = Job.objects.create(
            name='job',
            start_date='2017-06-15',
            end_date='2017-06-15',
            event=event)

        return job

    def register_shift_utility(self, job):

        shift = Shift.objects.create(
            date='2017-06-15',
            start_time='09:00',
            end_time='15:00',
            max_volunteers='6',
            job=job)

        return shift

    def register_volunteer_for_shift_utility(self, shift, volunteer):
        vol_shift = VolunteerShift.objects.create(
            shift=shift,
            volunteer=volunteer)
        return vol_shift

    def navigate_to_event_list_view(self):
        self.driver.get(self.live_server_url + self.event_list_page)

    def navigate_to_job_list_view(self):
        self.driver.get(self.live_server_url + self.job_list_page)

    def navigate_to_shift_list_view(self):
        self.driver.get(self.live_server_url + self.shift_list_page)
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]/td[5]//a').click()

    def fill_event_form(self, event):
        self.driver.find_element_by_xpath(
            '//input[@placeholder = "Event Name"]').send_keys(
            event[0])
        self.driver.find_element_by_xpath(
            '//input[@name = "start_date"]').send_keys(
            event[1])
        self.driver.find_element_by_xpath(
            '//input[@name = "end_date"]').send_keys(
            event[2])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def fill_job_form(self, job):
        self.driver.find_element_by_xpath(
            '//select[@name = "event_id"]').send_keys(
            job[0])
        self.driver.find_element_by_xpath(
            '//input[@placeholder = "Job Name"]').send_keys(
            job[1])
        self.driver.find_element_by_xpath(
            '//textarea[@name = "description"]').send_keys(
            job[2])
        self.driver.find_element_by_xpath(
            '//input[@name = "start_date"]').send_keys(
            job[3])
        self.driver.find_element_by_xpath(
            '//input[@name = "end_date"]').send_keys(
            job[4])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def fill_shift_form(self, shift):
        self.driver.find_element_by_xpath(
            '//input[@name = "date"]').send_keys(
            shift[0])
        self.driver.find_element_by_xpath(
            '//input[@name = "start_time"]').send_keys(
            shift[1])
        self.driver.find_element_by_xpath(
            '//input[@name = "end_time"]').send_keys(
            shift[2])
        self.driver.find_element_by_xpath(
            '//input[@name = "max_volunteers"]').send_keys(
            shift[3])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def test_field_value_retention_for_event(self):
        self.login({'username': 'admin', 'password': 'admin'})
        self.navigate_to_event_list_view()

        self.driver.find_element_by_link_text('Create Event').click()
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + '/event/create/')

        event = ['event-name!@', '07/21/2016', '09/28/2017']
        self.fill_event_form(event)

        # verify that event was not created and that field values are not
        # erased
        self.assertEqual(self.driver.current_url, self.live_server_url +
                         '/event/create/')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@placeholder = "Event Name"]').get_attribute('value'),
            'event-name!@')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "start_date"]').get_attribute('value'),
            '07/21/2016')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "end_date"]').get_attribute('value'),
            '09/28/2017')

        # now create an event and edit it
        # verify that event was not edited and that field values are not
        # erased
        event_1 = self.register_event_utility()
        self.navigate_to_event_list_view()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]').text, 'Edit')
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]//a').click()

        self.driver.find_element_by_xpath(
            '//input[@placeholder = "Event Name"]').clear()
        self.driver.find_element_by_xpath(
            '//input[@name = "start_date"]').clear()
        self.driver.find_element_by_xpath(
            '//input[@name = "end_date"]').clear()

        self.fill_event_form(event)
        self.assertNotEqual(self.driver.current_url, self.live_server_url +
                            '/event/create/')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@placeholder = "Event Name"]').get_attribute('value'),
            'event-name!@')
        """self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "start_date"]').get_attribute('value'),
            '07/21/2016')"""
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "end_date"]').get_attribute('value'),
            '09/28/2017')

    def test_field_value_retention_for_job(self):
        self.login({'username': 'admin', 'password': 'admin'})
        event_1 = self.register_event_utility()
        self.navigate_to_job_list_view()

        self.driver.find_element_by_link_text('Create Job').click()
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + '/job/create/')

        job = [
            'event',
            'job name#$',
            'job description',
            '05/29/2016',
            '09/11/2017']
        self.fill_job_form(job)

        # verify that job was not created and that field values are not
        # erased
        self.assertEqual(self.driver.current_url, self.live_server_url +
                         '/job/create/')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@placeholder = "Job Name"]').get_attribute('value'),
            'job name#$')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//textarea[@name = "description"]').get_attribute(
            'value'), 'job description')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "start_date"]').get_attribute(
            'value'), '05/29/2016')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "end_date"]').get_attribute(
            'value'), '09/11/2017')

        # now create job and edit it
        # verify that job was not edited and that field values are not
        # erased
        job_1 = self.register_job_utility(event_1)
        self.navigate_to_job_list_view()

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[6]').text, 'Edit')
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[6]//a').click()

        self.driver.find_element_by_xpath(
            '//input[@name = "name"]').clear()
        self.driver.find_element_by_xpath(
            '//textarea[@name = "description"]').clear()
        self.driver.find_element_by_xpath(
            '//input[@name = "start_date"]').clear()
        self.driver.find_element_by_xpath(
            '//input[@name = "end_date"]').clear()

        self.fill_job_form(job)
        # verify that job was not created and that field values are not
        # erased
        self.assertNotEqual(self.driver.current_url, self.live_server_url +
                            self.job_list_page)
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@placeholder = "Job Name"]').get_attribute('value'),
            'job name#$')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//textarea[@name = "description"]').get_attribute('value'),
            'job description')
        """self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "start_date"]').get_attribute('value'),
            '05/29/2016')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "end_date"]').get_attribute('value'),
            '09/11/2017')"""

    def test_field_value_retention_for_shift(self):
        self.login({'username': 'admin', 'password': 'admin'})
        event_1 = self.register_event_utility()
        job_1 = self.register_job_utility(event_1)

        self.navigate_to_shift_list_view()
        self.driver.find_element_by_link_text('Create Shift').click()

        shift = [
            '01/01/2016',
            '12:00',
            '11:00',
            '10']
        self.fill_shift_form(shift)

        # verify that shift was not created and that field values are not
        # erased
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "date"]').get_attribute('value'), '01/01/2016')
        """self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "start_time"]').get_attribute('value'), '12:00')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "end_time"]').get_attribute(
            'value'), '11:00')"""
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "max_volunteers"]').get_attribute(
            'value'), '10')

        # now create shift and edit it
        # verify that shift was not edited and that field values are not
        # erased
        shift_1 = self.register_shift_utility(job_1)
        self.navigate_to_shift_list_view()

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]').text, 'Edit')
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]//a').click()

        self.driver.find_element_by_xpath(
            '//input[@name = "date"]').clear()
        self.driver.find_element_by_xpath(
            '//input[@name = "start_time"]').clear()
        self.driver.find_element_by_xpath(
            '//input[@name = "end_time"]').clear()
        self.driver.find_element_by_xpath(
            '//input[@name = "max_volunteers"]').clear()

        self.fill_shift_form(shift)
        # verify that shift was not created and that field values are not
        # erased
        """self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "date"]').get_attribute('value'), '01/01/2016')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "start_time"]').get_attribute('value'), '12:00')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "end_time"]').get_attribute(
            'value'), '11:00')"""
        self.assertEqual(self.driver.find_element_by_xpath(
            '//input[@name = "max_volunteers"]').get_attribute(
            'value'), '10')

    def test_max_volunteer_field(self):
        self.login({'username': 'admin', 'password': 'admin'})
        event_1 = self.register_event_utility()
        job_1 = self.register_job_utility(event_1)

        self.navigate_to_shift_list_view()
        self.driver.find_element_by_link_text('Create Shift').click()

        shift = [
            '01/01/2016',
            '12:00',
            '11:00',
            '0']
        self.fill_shift_form(shift)

        # verify that error message displayed
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[7]/div/p/strong").text,
            'Ensure this value is greater than or equal to 1.')

        # Create shift and try editing it with 0 value
        shift_1 = self.register_shift_utility(job_1)
        self.navigate_to_shift_list_view()

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]').text, 'Edit')
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]//a').click()

        self.driver.find_element_by_xpath(
            '//input[@name = "date"]').clear()
        self.driver.find_element_by_xpath(
            '//input[@name = "start_time"]').clear()
        self.driver.find_element_by_xpath(
            '//input[@name = "end_time"]').clear()
        self.driver.find_element_by_xpath(
            '//input[@name = "max_volunteers"]').clear()

        self.fill_shift_form(shift)

        # verify that error message displayed
        self.assertEqual(self.driver.find_element_by_xpath(
            "//form//div[7]/div/p/strong").text,
            'Ensure this value is greater than or equal to 1.')

    def test_simplify_shift(self):
        self.login({'username': 'admin', 'password': 'admin'})
        event_1 = self.register_event_utility()
        job_1 = self.register_job_utility(event_1)

        self.navigate_to_shift_list_view()
        self.driver.find_element_by_link_text('Create Shift').click()

        # verify that the correct job name and date are displayed
        self.assertEqual(self.driver.find_element_by_xpath(
            "//div[2]//div[1]/p").text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//div[2]//div[2]/p").text, 'June 15, 2017')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//div[2]//div[3]/p").text, 'June 15, 2017')

        # Create shift and check job details in edit form
        shift_1 = self.register_shift_utility(job_1)
        self.navigate_to_shift_list_view()

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]').text, 'Edit')
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[5]//a').click()

        # verify that the correct job name and date are displayed
        self.assertEqual(self.driver.find_element_by_xpath(
            "//div[2]//div[1]/p").text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//div[2]//div[2]/p").text, 'June 15, 2017')
        self.assertEqual(self.driver.find_element_by_xpath(
            "//div[2]//div[3]/p").text, 'June 15, 2017')

    """def test_simplify_job(self):
        self.login({'username': 'admin', 'password': 'admin'})
        event_1 = self.register_event_utility()
        self.navigate_to_job_list_view()

        self.driver.find_element_by_link_text('Create Job').click()
        self.assertEqual(self.driver.current_url,
                         self.live_server_url + '/job/create/')

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

        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[6]').text, 'Edit')
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[6]//a').click()

        # verify that the correct event name and date are displayed
        select = Select(self.driver.find_element_by_id(
            'events'))
        select.select_by_visible_text('event')
        self.assertEqual(self.driver.find_element_by_id(
            'start_date_here').text, 'June 15, 2017')
        self.assertEqual(self.driver.find_element_by_id(
            'end_date_here').text, 'June 17, 2017')"""
