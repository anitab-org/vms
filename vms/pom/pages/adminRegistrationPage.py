# local Django
from pom.pages.basePage import BasePage
from pom.locators.adminRegistrationPageLocators import \
    AdminRegistrationPageLocators
from pom.pageUrls import PageUrls


class AdminRegistrationPage(BasePage):
    """Admin Registration page action methods here"""

    live_server_url = ''
    admin_registration_page = PageUrls.admin_registration_page
    success_message = 'You have successfully registered!'
    USER_EXISTS = 'A user with that username already exists.'
    INVALID_PHONE = 'Please enter a valid phone number'
    INVALID_PHONE_FOR_COUNTRY = 'This phone number isn\'t ' \
                                'valid for the selected country'
    NO_MATCH = 'Passwords don\'t match.'
    CONFIRM_EMAIL_MESSAGE = "Please confirm your email address before login."
    PASSWORD_ERROR = 'Password must have at least 6 characters, one ' \
                     'lowercase letter, one special character and one digit.'

    def __init__(self, driver):
        self.elements = AdminRegistrationPageLocators()
        super(AdminRegistrationPage, self).__init__(driver)

    def fill_registration_form(self, info):
        elements = self.elements
        self.send_value_to_element_id(elements.USERNAME, info['username'])
        self.send_value_to_element_id(elements.PASSWORD, info['password'])
        self.send_value_to_element_id(
            elements.CONFIRM_PASSWORD,
            info['confirm_password']
        )
        self.send_value_to_element_id(elements.FIRST_NAME, info['first_name'])
        self.send_value_to_element_id(elements.LAST_NAME, info['last_name'])
        self.send_value_to_element_id(elements.EMAIL, info['email'])
        self.send_value_to_element_id(elements.ADDRESS, info['address'])
        self.send_value_to_element_id(elements.COUNTRY, info['country'])
        self.send_value_to_element_id(elements.STATE, info['state'])
        self.send_value_to_element_id(elements.CITY, info['city'])
        self.send_value_to_element_id(elements.PHONE, info['phone_number'])
        self.send_value_to_element_id(
            elements.ORGANIZATION,
            info['organization']
        )
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

    def get_password_error_text(self):
        return self.element_by_xpath(self.elements.MATCH_ERROR).text

    def get_password_regex_error_text(self):
        return self.element_by_xpath(self.elements.PASSWORD_ERROR).text

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
        return self.element_by_xpath(self.elements.ORGANIZATION_ERROR).text

    def register_valid_details(self):
        self.get_admin_registration_page()
        entry = {
            'username': 'admin-username',
            'password': 'admin-password1!@#$%^&*()_',
            'confirm_password': 'admin-password1!@#$%^&*()_',
            'first_name': 'admin-first-name',
            'last_name': 'admin-last-name',
            'email': 'admin-email@systers.org',
            'address': 'admin-address',
            'city': 'Roorkee',
            'state': 'Uttarakhand',
            'country': 'India',
            'phone_number': '9999999999',
            'organization': 'admin-org'
        }
        self.fill_registration_form(entry)
