from basePage import *
from pom.locators.authenticationPageLocators import *
from pom.locators.homePageLocators import *
from pom.pageUrls import PageUrls

class AuthenticationPage(BasePage):

    url = PageUrls.authentication_page
    homepage = PageUrls.homepage
    server_url = ''

    def __init__(self, driver):
        self.elements = AuthenticationPageLocators()
        self.home = HomePageLocators()
        super(AuthenticationPage, self).__init__(driver)

    def login(self,credentials):
        self.get_page(self.server_url, self.url)
        self.send_value_to_element_id(self.elements.LOGIN_ID,credentials['username'])
        self.send_value_to_element_id(self.elements.LOGIN_PASSWORD,credentials['password'])
        self.element_by_xpath(self.elements.SUBMIT_PATH).submit()

    def go_to_authentication_page(self):
        self.click_link(self.home.LOGIN_TEXT)

    def logout(self):
        self.click_link(self.home.LOGOUT_TEXT)

    def get_incorrect_login_message(self):
        return self.element_by_class_name(self.elements.INCORRECT_LOGIN_ERROR)
