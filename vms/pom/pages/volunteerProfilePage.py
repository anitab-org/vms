# local Django
from pom.pages.basePage import BasePage
from pom.locators.volunteerProfilePageLocators import \
    VolunteerProfilePageLocators
from pom.pages.homePage import HomePage


class VolunteerProfilePage(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.home_page = HomePage(self.driver)
        self.elements = VolunteerProfilePageLocators()
        super(VolunteerProfilePage, self).__init__(driver)

    def navigate_to_profile(self):
        element = self.home_page.get_volunteer_profile_link()
        self.execute_script('arguments[0].click();', element)

    def edit_profile(self):
        self.find_link(self.elements.EDIT_PROFILE_TEXT).click()

    def fill_values(self, new_details):
        elements = self.elements
        self.fill_field(elements.PROFILE_FIRST_NAME, new_details['first_name'])
        self.fill_field(elements.PROFILE_LAST_NAME, new_details['last_name'])
        self.fill_field(elements.PROFILE_EMAIL, new_details['email'])
        self.fill_field(elements.PROFILE_ADDRESS, new_details['address'])
        self.send_value_to_xpath(
            elements.PROFILE_COUNTRY,
            new_details['country']
        )
        self.send_value_to_xpath(elements.PROFILE_STATE, new_details['state'])
        self.send_value_to_xpath(elements.PROFILE_CITY, new_details['city'])
        self.fill_field(elements.PROFILE_PHONE, new_details['phone_number'])
        self.element_by_xpath(self.elements.SELECT_NONE_ORGANIZATION).click()
        self.fill_field(
            elements.UNLISTED_ORGANIZATION,
            new_details['organization']
        )
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
