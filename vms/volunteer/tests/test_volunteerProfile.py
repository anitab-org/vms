# standard library
import re
from urllib.request import urlretrieve
import os
# import PyPDF2
# from PyPDF2.utils import PdfReadError

# third party
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Django
from django.contrib.staticfiles.testing import LiveServerTestCase

# local Django
from pom.pages.authenticationPage import AuthenticationPage
from pom.pages.volunteerProfilePage import VolunteerProfilePage
from shift.utils import (create_country, create_state,
                         create_city, create_other_city,
                         create_volunteer_with_details,
                         create_organization_with_details)


class VolunteerProfile(LiveServerTestCase):
    """
    Contains tests for:
    - Details of volunteer on profile.
    - Edit volunteer profile.
    - Upload of invalid resume format.
    - Upload of valid resume format.
    - Checks for resume corrupt uploaded in profile.
    """

    @classmethod
    def setUpClass(cls):
        """Method to initiate class level objects.

        This method initiates Firefox WebDriver, WebDriverWait and
        the corresponding POM objects for this Test Class
        """
        firefox_options = Options()
        firefox_options.add_argument('-headless')
        cls.driver = webdriver.Firefox(firefox_options=firefox_options)
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        cls.profile_page = VolunteerProfilePage(cls.driver)
        cls.authentication_page = AuthenticationPage(cls.driver)
        cls.wait = WebDriverWait(cls.driver, 20)
        cls.download_from_internet()
        super(VolunteerProfile, cls).setUpClass()

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        country = create_country()
        state = create_state()
        city = create_city()
        vol = {
            'username': 'Goku',
            'first_name': "Son",
            'last_name': "Goku",
            'address': "Kame House",
            'city': city,
            'state': state,
            'country': country,
            'phone_number': "9999999999",
            'email': "idonthave@gmail.com"
        }
        org_name = 'Detective'
        org_obj = create_organization_with_details(org_name)
        self.volunteer_1 = create_volunteer_with_details(vol, org_obj)
        self.login_correctly()

    def tearDown(self):
        """
        Method consists of statements to be executed at
        end of each test.
        """
        self.authentication_page.logout()

    @classmethod
    def tearDownClass(cls):
        """
        Class method to quit the Firefox WebDriver session after
        execution of all tests in class.
        """
        cls.driver.quit()
        os.remove(os.getcwd() + '/DummyResume.pdf')
        os.remove(os.getcwd() + '/DummyZip.zip')
        super(VolunteerProfile, cls).tearDownClass()

    def login_correctly(self):
        """
        Utility function to login as volunteer user to perform all tests.
        """
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({
            'username': "Goku",
            'password': "volunteer"
        })

    def wait_for_profile_load(self, profile_name):
        """
        Utility function to perform explicit wait for volunteer profile page.
        """
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), '" + profile_name + "')]")
            )
        )

    def wait_for_home_page(self):
        """
        Utility function to perform explicit wait for home page.
        """
        self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//h1[contains(text(),"
                    " 'Volunteer Management System')]"
                )
            )
        )

    @staticmethod
    def download_from_internet():
        """
        Utility functions to download dummy resume uploaded to dropbox.
        """
        urlretrieve(
            'https://dl.dropboxusercontent.com/s/'
            '08wpfj4n9f9jdnk/DummyResume.pdf',
            'DummyResume.pdf'
        )
        urlretrieve(
            'https://dl.dropboxusercontent.com/s/uydlhww0ekdy6j7/DummyZip.zip',
            'DummyZip.zip'
        )

    def test_details_tab(self):
        """
        Test volunteer details on profile page.
        """
        profile_page = self.profile_page
        profile_page.navigate_to_profile()
        self.wait_for_profile_load('Son Goku')
        page_source = self.driver.page_source

        found_email = re.search(self.volunteer_1.email, page_source)
        self.assertNotEqual(found_email, None)

        found_city = re.search(self.volunteer_1.city.name, page_source)
        self.assertNotEqual(found_city, None)

        found_state = re.search(self.volunteer_1.state.name, page_source)
        self.assertNotEqual(found_state, None)

        found_country = re.search(self.volunteer_1.country.name, page_source)
        self.assertNotEqual(found_country, None)

        found_org = re.search(self.volunteer_1.organization.name, page_source)
        self.assertNotEqual(found_org, None)

    def test_edit_profile(self):
        """
        Test profile edit in volunteer profile.
        """
        create_other_city()
        profile_page = self.profile_page
        profile_page.navigate_to_profile()
        self.wait_for_profile_load('Son Goku')
        profile_page.edit_profile()

        new_details = {
            'first_name': 'Harvey',
            'last_name': 'Specter',
            'email': 'hspecter@ps.com',
            'address': 'Empire State Building',
            'city': 'Mussoorie',
            'state': 'Uttarakhand',
            'country': 'India',
            'phone_number': '9999999998',
            'organization': 'Lawyer'
        }
        profile_page.fill_values(new_details)
        self.wait_for_profile_load('Harvey Specter')

        page_source = self.driver.page_source

        found_email = re.search(self.volunteer_1.email, page_source)
        self.assertEqual(found_email, None)

        found_city = re.search(self.volunteer_1.city.name, page_source)
        self.assertEqual(found_city, None)

        found_org = re.search(self.volunteer_1.organization.name, page_source)
        self.assertEqual(found_org, None)

        found_email = re.search(new_details['email'], page_source)
        self.assertNotEqual(found_email, None)

        found_city = re.search(new_details['city'], page_source)
        self.assertNotEqual(found_city, None)

        found_state = re.search(new_details['state'], page_source)
        self.assertNotEqual(found_state, None)

        found_country = re.search(new_details['country'], page_source)
        self.assertNotEqual(found_country, None)

        found_org = re.search(new_details['organization'], page_source)
        self.assertNotEqual(found_org, None)

    def test_invalid_resume_format(self):
        """
        Test upload of invalid resume to profile.
        """
        self.wait_for_home_page()

        path = os.getcwd() + '/DummyZip.zip'
        profile_page = self.profile_page
        profile_page.navigate_to_profile()
        self.wait_for_profile_load('Son Goku')
        profile_page.edit_profile()
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//legend[contains(text(), 'Edit Profile')]")
            )
        )

        profile_page.upload_resume(path)
        profile_page.submit_form()
        self.assertEqual(
            profile_page.get_invalid_format_error(),
            'Uploaded file is invalid.'
        )

# Resume Upload is buggy, it is taking too long to be uploaded on travis.
# https://github.com/systers/vms/issues/776


'''
    def test_valid_upload_resume(self):
        """
        Test upload of valid resume to profile.
        """
        self.wait_for_home_page()

        path = os.getcwd() + '/DummyResume.pdf'
        profile_page = self.profile_page
        profile_page.navigate_to_profile()
        self.wait_for_profile_load('Son Goku')
        profile_page.edit_profile()
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//legend[contains(text(), 'Edit Profile')]")
            )
        )
        self.assertEqual(os.path.exists(path), True)

        profile_page.upload_resume(path)
        profile_page.submit_form()
        self.wait_for_profile_load('Son Goku')
        self.assertEqual(profile_page.download_resume_text(), 'Download Resume')

    def test_corrupt_resume_uploaded(self):
        """
        Test uploaded resume is not corrupt by performing a few checks on it.
        """
        self.wait_for_home_page()
        path = os.getcwd() + '/DummyResume.pdf'
        size_before_upload = os.stat(path).st_size
        profile_page = self.profile_page
        profile_page.navigate_to_profile()
        self.wait_for_profile_load('Son Goku')
        profile_page.edit_profile()
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//legend[contains(text(), 'Edit Profile')]")
            )
        )
        self.assertEqual(os.path.exists(path), True)

        profile_page.upload_resume(path)
        profile_page.submit_form()

        self.wait_for_profile_load('Son Goku')
        self.assertEqual(profile_page.download_resume_text(), 'Download Resume')
        path = os.getcwd() + '/srv/vms/resume/DummyResume.pdf'
        size_after_upload = os.stat(path).st_size

        # Check via size
        self.assertEqual(size_after_upload, size_before_upload)

        # Check via open
        try:
            PyPDF2.PdfFileReader(open(path, 'rb'))
        except PdfReadError:
            print('Some error while upload/download')
        else:
            pass
'''
