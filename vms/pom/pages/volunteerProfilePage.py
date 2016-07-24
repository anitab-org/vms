from basePage import *
from pom.locators.volunteerProfilePageLocators import *
from pom.pages.homePage import HomePage

class VolunteerProfilePage(BasePage):

    def __init__(self, driver):
        self.driver = driver
        self.home_page = HomePage(self.driver)
        self.elements = VolunteerProfilePageLocators()
        super(VolunteerProfilePage, self).__init__(driver)

    def navigate_to_profile(self):
        self.home_page.get_volunteer_profile_link().send_keys("\n")

    def edit_profile(self):
        self.find_link(self.elements.EDIT_PROFILE_TEXT).send_keys("\n")

    def fill_values(self, new_details):
        elements = self.elements
        self.fill_field(elements.PROFILE_FIRST_NAME, new_details[0])
        self.fill_field(elements.PROFILE_LAST_NAME, new_details[1])
        self.fill_field(elements.PROFILE_EMAIL, new_details[2])
        self.fill_field(elements.PROFILE_ADDRESS, new_details[3])
        self.fill_field(elements.PROFILE_CITY, new_details[4])
        self.fill_field(elements.PROFILE_STATE, new_details[5])
        self.fill_field(elements.PROFILE_COUNTRY, new_details[6])
        self.fill_field(elements.PROFILE_PHONE, new_details[7])
        self.send_value_to_xpath(elements.SELECT_ORGANIZATION, new_details[8])
        self.fill_field(elements.UNLISTED_ORGANIZATION, new_details[9])
        self.submit_form()

    def fill_field(self, xpath, value):
        field = self.element_by_xpath(xpath)
        field.clear()
        field.send_keys(value)

    def upload_resume(self, path):
        self.send_value_to_xpath(self.elements.RESUME_FILE, path)

    def download_resume_text(self):
        return self.element_by_xpath(self.elements.DOWNLOAD_RESUME).text

    def get_invalid_format_error(self):
        return self.element_by_xpath(self.elements.INVALID_FORMAT_MESSAGE).text

    def submit_form(self):
        self.element_by_xpath(self.elements.SUBMIT_PATH).submit()   
