# local Django
from pom.pages.basePage import BasePage
from pom.locators.completedShiftsPageLocators import CompletedShiftsPageLocators
from pom.pages.homePage import HomePage
from pom.pageUrls import PageUrls


class CompletedShiftsPage(BasePage):

    view_hours_page = PageUrls.completed_shifts_page
    live_server_url = ''

    def __init__(self, driver):
        self.driver = driver
        self.home_page = HomePage(self.driver)
        self.elements = CompletedShiftsPageLocators()
        super(CompletedShiftsPage, self).__init__(driver)

    def go_to_completed_shifts(self):
        link = self.home_page.get_completed_shifts_link().get_attribute('href')
        self.get_page('', link)

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

    def get_unlogged_info_box(self):
        return self.element_by_id(self.elements.UNLOGGED_INFO_BOX).text

    def get_logged_info_box(self):
        return self.element_by_id(self.elements.LOGGED_INFO_BOX).text

    def get_danger_box(self):
        return self.element_by_class_name(self.elements.DANGER_BOX)

    def get_unlogged_shift_job(self):
        return self.element_by_xpath(self.elements.UNLOGGED_SHIFT_JOB_PATH).text

    def get_unlogged_shift_date(self):
        return self.element_by_xpath(
            self.elements.UNLOGGED_SHIFT_DATE_PATH
        ).text

    def get_unlogged_shift_start_time(self):
        return self.element_by_xpath(
            self.elements.UNLOGGED_SHIFT_STIME_PATH
        ).text

    def get_unlogged_shift_end_time(self):
        return self.element_by_xpath(
            self.elements.UNLOGGED_SHIFT_ETIME_PATH
        ).text

    def get_logged_shift_job(self):
        return self.element_by_xpath(self.elements.LOGGED_SHIFT_JOB_PATH).text

    def get_logged_shift_date(self):
        return self.element_by_xpath(self.elements.LOGGED_SHIFT_DATE_PATH).text

    def get_logged_shift_start_time(self):
        return self.element_by_xpath(self.elements.LOGGED_SHIFT_STIME_PATH).text

    def get_logged_shift_end_time(self):
        return self.element_by_xpath(self.elements.LOGGED_SHIFT_ETIME_PATH).text

    def get_log_hours(self):
        return self.element_by_xpath(self.elements.LOG_SHIFT_HOURS_PATH).text

    def get_edit_hours(self):
        return self.element_by_xpath(self.elements.SHIFT_EDIT_PATH).text

    def click_to_log_hours(self):
        self.element_by_xpath(
            self.elements.LOG_SHIFT_HOURS_PATH + "//a").click()

    def get_edit_shift_hours(self):
        return self.element_by_xpath(self.elements.SHIFT_EDIT_PATH).text

    def get_result_container(self):
        return self.element_by_xpath(self.elements.CONTAINER)

