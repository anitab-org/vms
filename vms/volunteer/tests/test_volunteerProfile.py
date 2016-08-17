from django.contrib.staticfiles.testing import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from volunteer.models import Volunteer
from shift.utils import create_volunteer_with_details

from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.volunteerProfilePage import VolunteerProfilePage

import re

class VolunteerProfile(LiveServerTestCase):
    '''
    '''
    @classmethod
    def setUpClass(cls):       
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.profile_page = VolunteerProfilePage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        super(VolunteerProfile, cls).setUpClass()

    def setUp(self):
        vol = ['Sherlock',"Sherlock","Holmes","221-B Baker Street","London","London-State","UK","9999999999","idonthave@gmail.com"]
        self.v1 = create_volunteer_with_details(vol)
        self.v1.unlisted_organization = 'Detective'
        self.v1.save()
        self.login_correctly()
        self.profile_page.navigate_to_profile()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(VolunteerProfile, cls).tearDownClass()

    def login_correctly(self):
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({ 'username' : "Sherlock", 'password' : "volunteer"})

    def test_details_tab(self):
        profile_page = self.profile_page
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
        profile_page = self.profile_page
        profile_page.edit_profile()

        new_details = ['Harvey', 'Specter', 'hspecter@ps.com', 'Empire State Building', 'NYC', 'New York', 'USA', '9999999998', 'None', 'Lawyer']
        profile_page.fill_values(new_details)

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

        # database check to ensure that profile has been updated
        self.assertEqual(len(Volunteer.objects.all()), 1)
        self.assertNotEqual(len(Volunteer.objects.filter(
            first_name = new_details[0],
            last_name = new_details[1],
            email=new_details[2],
            address = new_details[3],
            city = new_details[4],
            state = new_details[5],
            country = new_details[6],
            phone_number = new_details[7])), 0)

    def test_upload_resume(self):
        pass
        '''
        #Tested locally
        profile_page = self.profile_page
        profile_page.edit_profile()
        profile_page.upload_resume('/home/jlahori/Downloads/water.pdf')
        profile_page.submit_form()
        self.assertEqual(profile_page.download_resume_text(),'Download Resume')
        '''

    def test_invalid_resume_format(self):
        pass
        '''
        #Tested locally
        profile_page = self.profile_page
        profile_page.edit_profile()
        profile_page.upload_resume('/home/jlahori/Downloads/ca.crt')
        profile_page.submit_form()
        self.assertEqual(profile_page.get_invalid_format_error(),'Uploaded file is invalid.')
        '''
        