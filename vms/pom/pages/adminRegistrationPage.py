from basePage import *
from pom.locators.adminRegistrationPageLocators import *
from pom.pageUrls import PageUrls

class AdminRegistrationPage(BasePage):
    """Admin Registration page action methods here"""

    live_server_url = ''
    admin_registration_page = PageUrls.admin_registration_page
    success_message = "You have successfully registered!"

    def __init__(self, driver):
        self.elements = AdminRegistrationPageLocators()
        super(AdminRegistrationPage, self).__init__(driver)

    def fill_registration_form(self, info):
        elements = self.elements
        self.send_value_to_element_id(elements.USERNAME, info[0])
        self.send_value_to_element_id(elements.PASSWORD, info[1])
        self.send_value_to_element_id(elements.FIRST_NAME, info[2])
        self.send_value_to_element_id(elements.LAST_NAME, info[3])
        self.send_value_to_element_id(elements.EMAIL, info[4])
        self.send_value_to_element_id(elements.ADDRESS, info[5])
        self.send_value_to_element_id(elements.CITY, info[6])
        self.send_value_to_element_id(elements.STATE, info[7])
        self.send_value_to_element_id(elements.COUNTRY, info[8])
        self.send_value_to_element_id(elements.PHONE, info[9])
        self.send_value_to_element_id(elements.ORGANIZATION, info[10])
        self.submit_form()

    def get_field_values(self):
        values = {}
        elements = self.elements
        values['username'] = self.get_value_for(elements.USERNAME)
        values['first_name'] = self.get_value_for(elements.FIRST_NAME)
        values['last_name'] = self.get_value_for(elements.LAST_NAME)
        values['email'] = self.get_value_for(elements.EMAIL)
        values['address'] = self.get_value_for(elements.ADDRESS)
        values['city'] = self.get_value_for(elements.CITY)
        values['state'] = self.get_value_for(elements.STATE)
        values['country'] = self.get_value_for(elements.COUNTRY)
        values['phone'] = self.get_value_for(elements.PHONE)
        values['organization'] = self.get_value_for(elements.ORGANIZATION)
        return values

    def submit_form(self):
        self.element_by_xpath(self.elements.SUBMIT_PATH).submit()   

    def get_admin_registration_page(self):
        self.get_page(self.live_server_url, self.admin_registration_page)

    def get_help_blocks(self):
        blocks = self.elements_by_class_name(self.elements.HELP_BLOCK)
        return blocks

    def get_message_box_text(self):
        return self.element_by_class_name(self.elements.MESSAGES).text

    def get_message_box(self):
        return self.element_by_class_name(self.elements.MESSAGES)

    def get_username_error_text(self):
        return self.element_by_xpath(self.elements.USERNAME_ERROR).text

    def get_first_name_error_text(self):
        return self.element_by_xpath(self.elements.FIRST_NAME_ERROR).text

    def get_last_name_error_text(self):
        return self.element_by_xpath(self.elements.LAST_NAME_ERROR).text

    def get_address_error_text(self):
        return self.element_by_xpath(self.elements.ADDRESS_ERROR).text

    def get_city_error_text(self):
        return self.element_by_xpath(self.elements.CITY_ERROR).text

    def get_state_error_text(self):
        return self.element_by_xpath(self.elements.STATE_ERROR).text

    def get_country_error_text(self):
        return self.element_by_xpath(self.elements.COUNTRY_ERROR).text

    def get_email_error_text(self):
        return self.element_by_xpath(self.elements.EMAIL_ERROR).text

    def get_phone_error_text(self):
        return self.element_by_xpath(self.elements.PHONE_ERROR).text

    def get_organization_error_text(self):
        return self.element_by_xpath(self.elements.ORGANIZATION_ERROR ).text

    def register_valid_details(self):
        self.get_admin_registration_page()
        entry = ['admin-username','admin-password!@#$%^&*()_','admin-first-name','admin-last-name','admin-email@systers.org','admin-address','admin-city','admin-state','admin-country','9999999999','admin-org']
        self.fill_registration_form(entry)
