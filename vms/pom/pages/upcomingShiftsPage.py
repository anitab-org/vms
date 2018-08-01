# local Django
from pom.pages.basePage import BasePage
from pom.locators.upcomingShiftsPageLocators import UpcomingShiftsPageLocators
from pom.pages.completedShiftsPage import CompletedShiftsPage
from pom.pages.homePage import HomePage
from pom.pageUrls import PageUrls


class UpcomingShiftsPage(BasePage):

    view_shift_page = PageUrls.upcoming_shifts_page
    no_shift_message = 'You do not have any upcoming shifts.'
    live_server_url = ''

    def __init__(self, driver):
        self.driver = driver
        self.home_page = HomePage(self.driver)
        self.completed_shifts_page = CompletedShiftsPage(self.driver)
        self.elements = UpcomingShiftsPageLocators()
        super(UpcomingShiftsPage, self).__init__(driver)

    def view_upcoming_shifts(self):
        self.home_page.get_upcoming_shifts_link().click()

    def submit_form(self):
        self.element_by_xpath(self.elements.SUBMIT_PATH).submit()

    def get_info_box(self):
        return self.element_by_class_name(self.elements.INFO_BOX).text

    def get_result_container(self):
        return self.element_by_xpath(self.elements.CONTAINER)

    def get_shift_job(self):
        return self.element_by_xpath(self.elements.SHIFT_JOB_PATH).text

    def get_shift_date(self):
        return self.element_by_xpath(self.elements.SHIFT_DATE_PATH).text

    def get_shift_start_time(self):
        return self.element_by_xpath(self.elements.SHIFT_STIME_PATH).text

    def get_shift_end_time(self):
        return self.element_by_xpath(self.elements.SHIFT_ETIME_PATH).text

    def get_cancel_shift(self):
        return self.element_by_xpath(self.elements.SHIFT_CANCEL_PATH)

    def cancel_shift(self):
        self.element_by_xpath(self.elements.SHIFT_CANCEL_PATH + "//a").click()

