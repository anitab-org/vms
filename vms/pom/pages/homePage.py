# local Django
from pom.pages.basePage import BasePage
from pom.locators.homePageLocators import HomePageLocators


class HomePage(BasePage):
    def __init__(self, driver):
        self.elements = HomePageLocators()
        super(HomePage, self).__init__(driver)

    def get_admin_report_link(self):
        return self.find_link(self.elements.ADMIN_REPORT_TEXT)

    def get_manage_shifts_link(self):
        return self.find_link(self.elements.MANAGE_SHIFT_TEXT)

    def get_volunteer_search_link(self):
        return self.find_link(self.elements.VOLUNTEER_SEARCH_TEXT)

    def get_login_link(self):
        return self.find_link(self.elements.LOGIN_TEXT)

    def get_events_link(self):
        return self.find_link(self.elements.ADMIN_EVENTS_TEXT)

    def get_create_admin_link(self):
        return self.find_link(self.elements.CREATE_ADMIN_TEXT)

    def get_change_password_link(self):
        return self.find_link(self.elements.CHANGE_PASSWORD_TEXT)

    def go_to_change_password_page(self):
        self.get_change_password_link().click()

    def get_logout_link(self):
        return self.find_link(self.elements.LOGOUT_TEXT)

    def get_upcoming_shifts_link(self):
        return self.find_link(self.elements.UPCOMING_SHIFT_TEXT)

    def get_completed_shifts_link(self):
        return self.find_link(self.elements.COMPLETED_SHIFT_TEXT)

    def get_shift_signup_link(self):
        return self.find_link(self.elements.SHIFT_SIGN_UP_TEXT)

    def get_volunteer_report_link(self):
        return self.find_link(self.elements.VOLUNTEER_REPORT_TEXT)

    def get_volunteer_profile_link(self):
        return self.find_link(self.elements.VOLUNTEER_PROFILE_TEXT)

    def get_no_admin_right(self):
        return self.element_by_class_name(self.elements.NO_ADMIN_RIGHT_HEAD)

    def get_no_admin_right_content(self):
        return self.element_by_class_name(self.elements.NO_ADMIN_RIGHT_CONTENT)

    def get_no_volunteer_right(self):
        return self.element_by_class_name(self.elements.NO_VOLUNTEER_RIGHT_HEAD)

    def get_no_volunteer_right_content(self):
        return self.element_by_class_name(
            self.elements.NO_VOLUNTEER_RIGHT_CONTENT
        )

    def submit_form(self):
        self.element_by_id(self.elements.SUBMIT).click()

    def fill_password_change_form(self, password):
        self.send_value_to_xpath(
            self.elements.OLD_PASSWORD,
            password['old_password']
        )
        self.send_value_to_xpath(
            self.elements.NEW_PASSWORD,
            password['new_password']
        )
        self.send_value_to_xpath(
            self.elements.CONFIRM_NEW_PASSWORD,
            password['confirm_new_password']
        )
        self.submit_form()
