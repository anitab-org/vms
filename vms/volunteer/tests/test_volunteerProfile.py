from django.contrib.staticfiles.testing import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from volunteer.models import Volunteer
from shift.utils import create_volunteer_with_details

import re

class VolunteerProfile(LiveServerTestCase):
    '''
    '''
    @classmethod
    def setUpClass(cls):
        cls.homepage = '/'
        cls.authentication_page = '/authentication/login/'
        cls.profile_first_name_path = '//input[@name = "first_name"]'
        cls.profile_last_name_path = '//input[@name = "last_name"]'
        cls.profile_email_path = '//input[@name = "email"]'
        cls.profile_address_path = '//input[@name = "address"]'
        cls.profile_city_path = '//input[@name = "city"]'
        cls.profile_state_path = '//input[@name = "state"]'
        cls.profile_country_path = '//input[@name = "country"]'
        cls.profile_phone_path = '//input[@name = "phone_number"]'
        cls.select_organization_path = '//select[@name = "organization_name"]'
        cls.unlisted_organization_path = '//input[@name = "unlisted_organization"]'
        cls.resume_file_path = '//input[@name = "resume_file"]'
        cls.download_resume_path = './/*[@id="collapseResumeFile"]/div/form/button'
        
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        super(VolunteerProfile, cls).setUpClass()

    def setUp(self):
        vol = ['Sherlock',"Sherlock","Holmes","221-B Baker Street","London","London-State","UK","9999999999","idonthave@gmail.com"]
        self.v1 = create_volunteer_with_details(vol)
        self.v1.unlisted_organization = 'Detective'
        self.v1.save()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(VolunteerProfile, cls).tearDownClass()

    def login(self, credentials):
        self.driver.get(self.live_server_url + self.authentication_page)
        self.driver.find_element_by_id('id_login').send_keys(credentials['username'])
        self.driver.find_element_by_id('id_password').send_keys(credentials['password'])
        self.driver.find_element_by_xpath('//form[1]').submit()

    def login_correctly(self):
        self.login({ 'username' : "Sherlock", 'password' : "volunteer"})

    def navigate_to_profile(self):
        self.driver.find_element_by_link_text('Profile').send_keys("\n")

    def edit_profile(self):
        self.driver.find_element_by_link_text('Edit Profile').send_keys("\n")

    def fill_field(self, xpath, value):
        self.driver.find_element_by_xpath(xpath).clear()
        self.driver.find_element_by_xpath(xpath).send_keys(value)

    def test_details_tab(self):
        self.login_correctly()
        self.navigate_to_profile()
        page_source = self.driver.page_source

        found_email = re.search(self.v1.email, page_source)
        self.assertNotEqual(found_email, None)

        found_city = re.search(self.v1.city, page_source)
        self.assertNotEqual(found_city, None)

        found_state = re.search(self.v1.state, page_source)
        self.assertNotEqual(found_state, None)

        found_country = re.search(self.v1.country, page_source)
        self.assertNotEqual(found_country, None)

        found_org = re.search(self.v1.unlisted_organization, page_source)
        self.assertNotEqual(found_org, None)

    def test_edit_profile(self):
        self.login_correctly()
        self.navigate_to_profile()
        self.edit_profile()

        new_details = ['Harvey', 'Specter', 'hspecter@ps.com', 'Empire State Building', 'NYC', 'New York', 'USA', '9999999998', 'None', 'Lawyer']

        self.fill_field(self.profile_first_name_path, new_details[0])
        self.fill_field(self.profile_last_name_path, new_details[1])
        self.fill_field(self.profile_email_path, new_details[2])
        self.fill_field(self.profile_address_path, new_details[3])
        self.fill_field(self.profile_city_path, new_details[4])
        self.fill_field(self.profile_state_path, new_details[5])
        self.fill_field(self.profile_country_path, new_details[6])
        self.fill_field(self.profile_phone_path, new_details[7])
        self.driver.find_element_by_xpath(
                self.select_organization_path).send_keys(new_details[8])
        self.fill_field(self.unlisted_organization_path, new_details[9])
        self.driver.find_element_by_xpath('//form').submit()

        page_source = self.driver.page_source

        found_email = re.search(self.v1.email, page_source)
        self.assertEqual(found_email, None)

        found_city = re.search(self.v1.city, page_source)
        self.assertEqual(found_city, None)

        found_state = re.search(self.v1.state, page_source)
        self.assertEqual(found_state, None)

        found_country = re.search(self.v1.country, page_source)
        self.assertEqual(found_country, None)

        found_org = re.search(self.v1.unlisted_organization, page_source)
        self.assertEqual(found_org, None)

        found_email = re.search(new_details[2], page_source)
        self.assertNotEqual(found_email, None)

        found_city = re.search(new_details[4], page_source)
        self.assertNotEqual(found_city, None)

        found_state = re.search(new_details[5], page_source)
        self.assertNotEqual(found_state, None)

        found_country = re.search(new_details[6], page_source)
        self.assertNotEqual(found_country, None)

        found_org = re.search(new_details[9], page_source)
        self.assertNotEqual(found_org, None)

    def test_upload_resume(self):
        pass
        '''
        #Tested locally
        self.login_correctly()
        self.navigate_to_profile()
        self.edit_profile()

        self.driver.find_element_by_xpath(
                self.resume_file_path).send_keys('/home/jlahori/Downloads/water.pdf')

        self.driver.find_element_by_xpath('//form').submit()
        self.assertEqual(self.driver.find_element_by_xpath(
            self.download_resume_path).text,
            'Download Resume')
        '''

    def test_invalid_resume_format(self):
        pass
        '''
        #Tested locally
        self.login_correctly()
        self.navigate_to_profile()
        self.edit_profile()

        self.driver.find_element_by_xpath(
                self.resume_file_path).send_keys('/home/jlahori/Downloads/ca.crt')

        self.driver.find_element_by_xpath('//form').submit()
        self.assertEqual(self.driver.find_element_by_xpath(
            'html/body/div[2]/div[2]/form/fieldset/div[13]/div/p/strong').text,
            'Uploaded file is invalid.')
        '''
        