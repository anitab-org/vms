# third party

# local Django
from pom.pages.basePage import BasePage
from pom.locators.administratorReportPageLocators import \
    AdministratorReportPageLocators
from pom.pages.homePage import HomePage
from pom.pageUrls import PageUrls


class AdministratorReportPage(BasePage):
    administrator_report_page = PageUrls.administrator_report_page

    def __init__(self, driver):
        self.driver = driver
        self.home_page = HomePage(self.driver)
        self.elements = AdministratorReportPageLocators()
        super(AdministratorReportPage, self).__init__(driver)

    def go_to_admin_report(self):
        self.home_page.get_admin_report_link().click()

    def go_to_view_report_page(self):
        return self.element_by_xpath(self.elements.VIEW_REPORT).click()

    def get_volunteer_name(self):
        return self.element_by_xpath(self.elements.VOLUNTEER_NAME).text

    def get_hours(self):
        return self.element_by_xpath(self.elements.HOURS).text

    def get_shift_summary(self):
        return self.element_by_xpath(
            self.elements.REPORT_SHIFT_SUMMARY_PATH).text

    def get_rejection_context(self):
        return self.element_by_xpath(self.elements.REJECT_REPORT).text

    def reject_report(self):
        self.element_by_xpath(self.elements.REJECT_REPORT + '//a').click()

    def get_report(self):
        return self.element_by_xpath(self.elements.REPORT)

    def get_approval_context(self):
        return self.element_by_xpath(self.elements.APPROVE_REPORT).text

    def approve_report(self):
        self.element_by_xpath(self.elements.APPROVE_REPORT + '//a').click()

