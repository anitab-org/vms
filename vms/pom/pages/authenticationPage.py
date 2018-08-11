# local Django
from pom.pages.basePage import BasePage
from pom.locators.authenticationPageLocators import AuthenticationPageLocators
from pom.locators.homePageLocators import HomePageLocators
from pom.pageUrls import PageUrls


class AuthenticationPage(BasePage):

    url = PageUrls.authentication_page
    homepage = PageUrls.homepage
    server_url = ''

    def __init__(self, driver):
        self.elements = AuthenticationPageLocators()
        self.home = HomePageLocators()
        super(AuthenticationPage, self).__init__(driver)

    def login(self, credentials):
        self.get_page(self.server_url, self.url)
        self.send_value_to_element_id(self.elements.LOGIN_ID,
                                      credentials['username'])
        self.send_value_to_element_id(self.elements.LOGIN_PASSWORD,
                                      credentials['password'])
        self.element_by_xpath(self.elements.SUBMIT_PATH).submit()

    def go_to_authentication_page(self):
        self.get_page(self.server_url, PageUrls.authentication_page)

    def logout(self):
        element = self.find_link(self.home.LOGOUT_TEXT)
        self.execute_script('arguments[0].click();', element)

    def get_incorrect_login_message(self):
        return self.element_by_class_name(self.elements.INCORRECT_LOGIN_ERROR)

    def go_to_forgot_password_page(self):
        self.click_link('Forgot password')

    def submit_form(self):
        self.element_by_id(self.elements.RESET_SUBMIT).click()

    def fill_email_form(self, email):
        self.element_by_id(self.elements.EMAIL).clear()
        self.send_value_to_element_id(self.elements.EMAIL, email)
        self.submit_form()

