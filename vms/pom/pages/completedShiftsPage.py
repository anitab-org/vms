# local Django
from pom.pages.basePage import BasePage
from pom.locators.completedShiftsPageLocators import CompletedShiftsPageLocators
from pom.pages.homePage import HomePage
from pom.pageUrls import PageUrls


class CompletedShiftsPage(BasePage):

    view_hours_page = PageUrls.completed_shifts_page

    def __init__(self, driver):
        self.driver = driver
        self.home_page = HomePage(self.driver)
        self.elements = CompletedShiftsPageLocators()
        super(CompletedShiftsPage, self).__init__(driver)

    def go_to_completed_shifts(self):
        self.home_page.get_completed_shifts_link().click()

    def edit_hours(self, stime, etime):
        self.element_by_xpath(self.elements.SHIFT_EDIT_PATH + '//a').click()
        self.log_shift_timings(stime, etime)

    def log_shift_timings(self, stime, etime):
        self.element_by_xpath(self.elements.START_TIME_FORM).clear()
        self.send_value_to_xpath(self.elements.START_TIME_FORM, stime)
        self.element_by_xpath(self.elements.END_TIME_FORM).clear()
        self.send_value_to_xpath(self.elements.END_TIME_FORM, etime)
        self.submit_form()

    def submit_form(self):
        self.element_by_xpath(self.elements.SUBMIT_PATH).submit()

    def get_info_box(self):
        return self.element_by_class_name(self.elements.INFO_BOX).text

    def get_danger_box(self):
        return self.element_by_class_name(self.elements.DANGER_BOX)

    def get_shift_job(self):
        return self.element_by_xpath(self.elements.SHIFT_JOB_PATH).text

    def get_shift_date(self):
        return self.element_by_xpath(self.elements.SHIFT_DATE_PATH).text

    def get_shift_start_time(self):
        return self.element_by_xpath(self.elements.SHIFT_STIME_PATH).text

    def get_shift_end_time(self):
        return self.element_by_xpath(self.elements.SHIFT_ETIME_PATH).text

    def get_clear_shift_hours(self):
        return self.element_by_xpath(self.elements.SHIFT_CLEAR_PATH).text

    def get_edit_shift_hours(self):
        return self.element_by_xpath(self.elements.SHIFT_EDIT_PATH).text

    def get_clear_shift_hours_text(self):
        return self.element_by_xpath(self.elements.CLEAR_SHIFT_HOURS_TEXT).text

    def click_to_clear_hours(self):
        self.element_by_xpath(self.elements.SHIFT_CLEAR_PATH + '//a').click()
