from basePage import *
from pom.locators.volunteerReportPageLocators import *
from selenium.webdriver.support.ui import Select
from pom.pageUrls import PageUrls
from pom.pages.homePage import HomePage
from pom.pages.authenticationPage import AuthenticationPage

class VolunteerReportPage(BasePage):

    no_results_message = 'Your criteria did not return any results.'
    live_server_url = ''

    def __init__(self, driver):
        self.driver = driver
        self.authentication_page = AuthenticationPage(self.driver)
        self.home_page = HomePage(self.driver)
        self.elements = VolunteerReportPageLocators()
        super(VolunteerReportPage, self).__init__(driver)

    def login_and_navigate_to_report_page(self):
        self.authentication_page.server_url = self.live_server_url
        self.authentication_page.login({ 'username' : 'volunteer', 'password' : 'volunteer'})
        self.home_page.get_volunteer_report_link().send_keys("\n")

    def get_event_job_selectors(self):
        select1 = Select(self.element_by_xpath(self.elements.REPORT_EVENT_SELECTOR))
        select2 = Select(self.element_by_xpath(self.elements.REPORT_JOB_SELECTOR))
        return (select1, select2)

    def fill_report_form(self, dates):
        self.element_by_xpath(self.elements.REPORT_START_DATE).clear()
        self.element_by_xpath(self.elements.REPORT_END_DATE).clear()
        self.send_value_to_xpath(self.elements.REPORT_START_DATE, dates['start'])
        self.send_value_to_xpath(self.elements.REPORT_END_DATE, dates['end'])
        self.submit_form()

    def submit_form(self):
        self.element_by_xpath(self.elements.SUBMIT_PATH).submit()   

    def get_alert_box_text(self):
        return self.element_by_class_name(self.elements.NO_RESULT_BOX).text

    def get_shift_summary(self):
        return self.element_by_xpath(self.elements.REPORT_SHIFT_SUMMARY_PATH).text
