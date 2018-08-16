# third party
from selenium.webdriver.support.ui import Select

# local Django
from pom.pages.basePage import BasePage
from pom.locators.volunteerReportPageLocators import VolunteerReportPageLocators
from pom.pages.homePage import HomePage
from pom.pageUrls import PageUrls


class VolunteerReportPage(BasePage):
    volunteer_history_page = PageUrls.volunteer_history_page
    volunteer_report_page = PageUrls.volunteer_report_page
    no_results_message = 'Your criteria did not return any results.'
    live_server_url = ''

    def __init__(self, driver):
        self.driver = driver
        self.home_page = HomePage(self.driver)
        self.elements = VolunteerReportPageLocators()
        super(VolunteerReportPage, self).__init__(driver)

    def navigate_to_report_page(self):
        self.home_page.get_volunteer_report_link().click()

    def get_event_job_selectors(self):
        select1 = Select(
            self.element_by_xpath(self.elements.REPORT_EVENT_SELECTOR))
        select2 = Select(
            self.element_by_xpath(self.elements.REPORT_JOB_SELECTOR))
        return select1, select2

    def fill_report_form(self, dates):
        self.element_by_xpath(self.elements.REPORT_START_DATE).clear()
        self.element_by_xpath(self.elements.REPORT_END_DATE).clear()
        self.send_value_to_xpath(self.elements.REPORT_START_DATE,
                                 dates['start'])
        self.send_value_to_xpath(self.elements.REPORT_END_DATE, dates['end'])
        self.submit_form()

    def submit_form(self):
        self.element_by_xpath(self.elements.SUBMIT_PATH).submit()

    def get_alert_box_text(self):
        return self.element_by_class_name(self.elements.NO_RESULT_BOX).text

    def get_report_hours(self):
        return self.element_by_xpath(self.elements.REPORT_HOURS_PATH).text

