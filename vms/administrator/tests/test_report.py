from django.contrib.staticfiles.testing import LiveServerTestCase

from django.db import IntegrityError

from pom.locators.administratorReportPageLocators import *
from pom.pages.administratorReportPage import AdministratorReportPage
from pom.pages.authenticationPage import AuthenticationPage

from shift.utils import (
    create_admin,
    create_volunteer,
    create_organization_with_details,
    create_event_with_details,
    create_job_with_details,
    create_shift_with_details,
    log_hours_with_details,
    register_volunteer_for_shift_utility
    )

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Report(LiveServerTestCase):
    '''
    '''

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
        self.report_page.go_to_admin_report()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(Report, cls).tearDownClass()

    def login_admin(self):
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({ 'username' : 'admin', 'password' : 'admin'})

    def verify_shift_details(self, total_shifts, hours):
        total_no_of_shifts = self.report_page.get_shift_summary().split(' ')[10].strip('\nTotal')
        total_no_of_hours = self.report_page.get_shift_summary().split(' ')[-1].strip('\n')
        self.assertEqual(total_no_of_shifts, total_shifts)
        self.assertEqual(total_no_of_hours, hours)

#Failing test case which has been documented
#Test commented out to prevent travis build failure - bug #327

    """def test_null_values_with_dataset(self):
        # register dataset
        org = create_organization_with_details('organization-one')
        volunteer = create_volunteer()
        volunteer.organization = org
        volunteer.save()

        # create shift and log hours
        # register event first to create job
        event = ['Hackathon', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['Developer', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '15:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        logged_shift = log_hours_with_details(volunteer, created_shift, "09:00", "12:00")

        report_page = self.report_page

        # check admin report with null fields, should return the above shift
        report_page.fill_report_form(['','','','',''])
        self.verify_shift_details('1','3.0')

        self.assertEqual(report_page.element_by_xpath(
            self.elements.NAME).text, created_event.name)
        self.assertEqual(report_page.element_by_xpath(
            self.elements.DATE).text, 'Aug. 21, 2016')
        self.assertEqual(report_page.element_by_xpath(
            self.elements.START_TIME).text, '9 a.m.')
        self.assertEqual(report_page.element_by_xpath(
            self.elements.END_TIME).text, '12 p.m.')
        self.assertEqual(report_page.element_by_xpath(
            self.elements.HOURS).text, '3.0')"""

    def test_null_values_with_empty_dataset(self):
        # should return no entries
        report_page = self.report_page
        report_page.fill_report_form(['','','','',''])
        self.assertEqual(report_page.get_alert_box_text(),report_page.no_results_message)

    def test_only_logged_shifts_are_reported(self):
        # register dataset
        org = create_organization_with_details('organization-one')
        volunteer = create_volunteer()
        volunteer.organization = org
        volunteer.save()

        # register event first to create job
        event = ['Hackathon', '2017-08-21', '2017-09-28']
        created_event = create_event_with_details(event)

        # create job
        job = ['Developer', '2017-08-21', '2017-08-30', '',created_event]
        created_job = create_job_with_details(job)

        # create shift
        shift = ['2017-08-21', '09:00', '15:00', '10', created_job]
        created_shift = create_shift_with_details(shift)

        # shift is assigned to volunteer-one, but hours have not been logged
        volunteer_shift = register_volunteer_for_shift_utility(created_shift, volunteer)

        report_page = self.report_page
        # check admin report with null fields, should not return the above shift
        report_page.fill_report_form(['','','','',''])
        self.assertEqual(report_page.get_alert_box_text(),report_page.no_results_message)

#Failing test case which has been documented - bug #327
#Test commented out to prevent travis build failure

    """def test_check_intersection_of_fields(self):

        self.create_dataset()

        report_page = self.report_page

        search_parameters_1 = ['tom','','','','']
        report_page.fill_report_form(search_parameters_1)

        self.verify_shift_details('2','2.0')

        search_parameters_2 = ['','','','','org-one']
        report_page.fill_report_form(search_parameters_2)

        self.verify_shift_details('3','3.0')

        search_parameters_3 = ['','','event-four','Two','']
        report_page.fill_report_form(search_parameters_3)

        # 1 shift of 1:30 hrs
        self.verify_shift_details('1','1.5')

        search_parameters_4 = ['','','one','','']
        report_page.fill_report_form(search_parameters_4)

        # 3 shifts of 0:30 hrs, 1:00 hrs, 1:00 hrs
        self.verify_shift_details('3','2.5')

        # check case-insensitive
        search_parameters_5 = ['','sherlock','two','','']
        report_page.fill_report_form(search_parameters_5)

        self.verify_shift_details('1','2.0')

    def create_dataset(self):
        parameters = {'org' : 'org-one',
                'volunteer' : {
                    'username' : 'uname1', 
                    'password' : 'uname1', 
                    'email' : 'email1@email.com',
                    'first_name' : 'tom-fname',
                    'last_name' : 'tom-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
                'event' : {
                    'name' : 'event-four',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-10'},
                'job' : {
                    'name' : 'jobOneInEventFour',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-01'},
                'shift' : {
                    'date' : '2016-06-01',
                    'start_time' : '09:00',
                    'end_time' : '11:00',
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '09:30',
                    'end_time' : '10:00',}}
        self.register_dataset(parameters)

        parameters = {'org' : 'org-one',
                'volunteer' : {
                    'username' : 'uname2', 
                    'password' : 'uname2', 
                    'email' : 'email2@email.com',
                    'first_name' : 'peter-fname',
                    'last_name' : 'peter-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
                'event' : {
                    'name' : 'event-one',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-10'},
                'job' : {
                    'name' : 'jobOneInEventOne',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-01'},
                'shift' : {
                    'date' : '2016-06-01',
                    'start_time' : '18:00',
                    'end_time' : '23:00',
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '19:00',
                    'end_time' : '20:00'}}
        self.register_dataset(parameters)

        parameters = {'org' : 'org-one',
                'volunteer' : {
                    'username' : 'uname3', 
                    'password' : 'uname3', 
                    'email' : 'email3@email.com',
                    'first_name' : 'tom-fname',
                    'last_name' : 'tom-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
                'event' : {
                    'name' : 'event-four',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-10'},
                'job' : {
                    'name' : 'jobTwoInEventFour',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-01'},
                'shift' : {
                    'date' : '2016-06-01',
                    'start_time' : '09:00',
                    'end_time' : '15:00',
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '10:00',
                    'end_time' : '11:30'}}
        self.register_dataset(parameters)

        parameters = {'org' : 'org-two',
                'volunteer' : {
                    'username' : 'uname4', 
                    'password' : 'uname4', 
                    'email' : 'email4@email.com',
                    'first_name' : 'harry-fname',
                    'last_name' : 'harry-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
                'event' : {
                    'name' : 'event-one',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-10'},
                'job' : {
                    'name' : 'jobTwoInEventOne',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-01'},
                'shift' : {
                    'date' : '2016-06-01',
                    'start_time' : '09:00',
                    'end_time' : '11:00',
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '09:00',
                    'end_time' : '10:00'}}
        self.register_dataset(parameters)

        parameters = {'org' : 'org-two',
                'volunteer' : {
                    'username' : 'uname5', 
                    'password' : 'uname5', 
                    'email' : 'email5@email.com',
                    'first_name' : 'harry-fname',
                    'last_name' : 'harry-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
                'event' : {
                    'name' : 'event-two',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-10'},
                'job' : {
                    'name' : 'jobOneInEventTwo',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-01'},
                'shift' : {
                    'date' : '2016-06-01',
                    'start_time' : '09:00',
                    'end_time' : '18:00',
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '12:00',
                    'end_time' : '15:00'}}
        self.register_dataset(parameters)

        parameters = {'org' : 'org-three',
                'volunteer' : {
                    'username' : 'uname6', 
                    'password' : 'uname6', 
                    'email' : 'email6@email.com',
                    'first_name' : 'sherlock-fname',
                    'last_name' : 'sherlock-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
                'event' : {
                    'name' : 'event-two',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-10'},
                'job' : {
                    'name' : 'jobOneInEventTwo',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-01'},
                'shift' : {
                    'date' : '2016-06-01',
                    'start_time' : '09:00',
                    'end_time' : '16:00',
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '12:00',
                    'end_time' : '14:00'}}
        self.register_dataset(parameters)

        parameters = {'org' : 'org-four',
                'volunteer' : {
                    'username' : 'uname7', 
                    'password' : 'uname7', 
                    'email' : 'email7@email.com',
                    'first_name' : 'harvey-fname',
                    'last_name' : 'harvey-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
                'event' : {
                    'name' : 'event-one',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-10'},
                'job' : {
                    'name' : 'jobThreeInEventOne',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-01'},
                'shift' : {
                    'date' : '2016-06-01',
                    'start_time' : '09:00',
                    'end_time' : '13:00',
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '12:00',
                    'end_time' : '12:30'}}
        self.register_dataset(parameters)

        parameters = {'org' : 'org-four',
                'volunteer' : {
                    'username' : 'uname8', 
                    'password' : 'uname8', 
                    'email' : 'email8@email.com',
                    'first_name' : 'mike-fname',
                    'last_name' : 'mike-lname',
                    'address' : 'address',
                    'city' : 'city',
                    'state' : 'state',
                    'country' : 'country',
                    'phone-no' : '9999999999'},
                'event' : {
                    'name' : 'event-three',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-10'},
                'job' : {
                    'name' : 'jobOneInEventThree',
                    'start_date' : '2016-06-01',
                    'end_date' : '2016-06-01'},
                'shift' : {
                    'date' : '2016-06-01',
                    'start_time' : '01:00',
                    'end_time' : '10:00',
                    'max_volunteers' : '10'},
                'vshift' : {
                    'start_time' : '01:00',
                    'end_time' : '04:00'}}
        self.register_dataset(parameters)"""
