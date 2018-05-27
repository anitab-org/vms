# third party
from selenium.webdriver.support.ui import Select

# local Django
from pom.pages.basePage import BasePage
from pom.locators.administratorReportPageLocators import AdministratorReportPageLocators
from pom.pages.homePage import HomePage


class AdministratorReportPage(BasePage):

    no_results_message = 'Your criteria did not return any results.'

    def __init__(self, driver):
        self.driver = driver
        self.home_page = HomePage(self.driver)
        self.elements = AdministratorReportPageLocators()
        super(AdministratorReportPage, self).__init__(driver)

    def go_to_admin_report(self):
        self.home_page.get_admin_report_link().click()

    def fill_report_form(self, info):
        first_name = self.element_by_xpath(self.elements.FIRST_NAME_SELECTOR)
        last_name = self.element_by_xpath(self.elements.LAST_NAME_SELECTOR)

        first_name.clear()
        last_name.clear()
        [select1, select2, select3] = self.get_event_job_organization_selectors()

        first_name.send_keys(info[0])
        last_name.send_keys(info[1])
        """select1.select_by_visible_text(info[2])
        select2.select_by_visible_text(info[3])
        select3.select_by_visible_text(info[4])"""

        self.submit_form()

    def get_event_job_organization_selectors(self):
        select1 = Select(self.element_by_xpath(self.elements.REPORT_EVENT_SELECTOR))
        select2 = Select(self.element_by_xpath(self.elements.REPORT_JOB_SELECTOR))
        select3 = Select(self.element_by_xpath(self.elements.REPORT_ORG_SELECTOR))
        return select1, select2, select3

    def submit_form(self):
        self.element_by_xpath(self.elements.SUBMIT_PATH).submit()

    def get_alert_box_text(self):
        return self.element_by_class_name(self.elements.NO_RESULT_BOX).text

    def get_shift_summary(self):
        return self.element_by_xpath(self.elements.REPORT_SHIFT_SUMMARY_PATH).text
