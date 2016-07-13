from django.contrib.staticfiles.testing import LiveServerTestCase

from django.contrib.auth.models import User
from administrator.models import Administrator
from volunteer.models import Volunteer
from event.models import Event
from job.models import Job
from shift.models import Shift, VolunteerShift

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
        self.shift_list_page = '/shift/list_jobs/'
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        super(ShiftDetails, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(ShiftDetails, self).tearDown()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id(
            'id_login').send_keys(credentials['username'])
        self.driver.find_element_by_id('id_password').send_keys(
            credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def register_volunteer_utility(self, name):
        volunteer_user = User.objects.create_user(
            username=name,
            password='volunteer')

        volunteer = Volunteer.objects.create(
            user=volunteer_user,
            first_name='Michael',
            last_name='Reed',
            address='address',
            city='city',
            state='state',
            country='country',
            phone_number='9999999999',
            email='volunteer@volunteer.com',
            unlisted_organization='organization')

        return volunteer

    def register_shift_utility(self, ):

        # create shift and log hours
        event = Event.objects.create(
            name='event',
            start_date='2017-06-15',
            end_date='2017-06-17')

        job = Job.objects.create(
            name='job',
            start_date='2017-06-15',
            end_date='2017-06-15',
            event=event)

        shift = Shift.objects.create(
            date='2017-06-15',
            start_time='09:00',
            end_time='15:00',
            max_volunteers='6',
            job=job)

        return shift

    def log_hours_utility(self, shift, volunteer, s_time, e_time):
        VolunteerShift.objects.create(
            shift=shift,
            volunteer=volunteer,
            start_time=s_time,
            end_time=e_time)

    def register_volunteer_for_shift_utility(self, shift, volunteer):
        vol_shift = VolunteerShift.objects.create(
            shift=shift,
            volunteer=volunteer)
        return vol_shift

    def navigate_to_shift_details_view(self):
        self.driver.get(self.live_server_url + self.shift_list_page)
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]/td[5]//a').click()
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[7]').text, 'View')
        self.driver.find_element_by_xpath(
            '//table//tbody//tr[1]//td[7]//a').click()

    def test_view_with_unregistered_volunteers(self):
        self.login({'username': 'admin', 'password': 'admin'})
        shift = self.register_shift_utility()
        self.navigate_to_shift_details_view()

        # verify details and slots remaining
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[1]//tr//td[1]').text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[1]//tr//td[3]').text, 'June 15, 2017')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[1]//tr//td[9]').text, '6')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[1]//tr//td[4]').text, '9 a.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[1]//tr//td[5]').text, '3 p.m.')

        # verify that there are no registered shifts or logged hours
        self.assertEqual(
            self.driver.find_element_by_class_name('alert-success').text,
            'There are currently no volunteers assigned to this shift. Please assign volunteers to view more details')

    def test_view_with_only_registered_volunteers(self):
        self.login({'username': 'admin', 'password': 'admin'})
        shift = self.register_shift_utility()
        volunteer = self.register_volunteer_utility('volunteer')
        volunteer_shift = self.register_volunteer_for_shift_utility(
            shift, volunteer)
        self.navigate_to_shift_details_view()

        # verify that the shift slot is decreased by 1
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[1]//tr//td[1]').text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[1]//tr//td[9]').text, '5')

        # verify that assigned volunteers shows up but no logged hours yet
        self.assertEqual(
            len(self.driver.find_elements_by_xpath('//table[2]//tbody//tr')), 1)
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[2]//tr//td[1]').text, 'Michael')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[2]//tr//td[9]').text, 'volunteer@volunteer.com')
        self.assertEqual(self.driver.find_element_by_class_name(
            'alert-success').text, 'There are no logged hours at the moment')

    def test_view_with_logged_hours(self):
        self.login({'username': 'admin', 'password': 'admin'})
        shift = self.register_shift_utility()
        volunteer = self.register_volunteer_utility('volunteer')
        self.log_hours_utility(shift, volunteer, '13:00', '14:00')
        self.navigate_to_shift_details_view()

        # verify that the shift slot is decreased by 1
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[1]//tr//td[1]').text, 'job')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[1]//tr//td[9]').text, '5')

        # verify that assigned volunteers shows up
        self.assertEqual(
            len(self.driver.find_elements_by_xpath('//table[2]//tbody//tr')), 1)
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[2]//tr//td[9]').text, 'volunteer@volunteer.com')

        # verify that hours are logged by volunteer
        self.assertEqual(
            len(self.driver.find_elements_by_xpath('//table[3]//tbody//tr')), 1)
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[3]//tr//td[1]').text, 'Michael')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[3]//tr//td[4]').text, '1 p.m.')
        self.assertEqual(self.driver.find_element_by_xpath(
            '//table[3]//tr//td[5]').text, '2 p.m.')
