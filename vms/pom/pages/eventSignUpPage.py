from basePage import *
from pom.locators.eventSignUpPageLocators import EventSignUpPageLocators
from pom.pages.homePage import HomePage

class EventSignUpPage(BasePage):

    no_event_message = 'There are no events.'

    def __init__(self, driver):
        self.driver = driver
        self.home_page = HomePage(self.driver)
        self.elements = EventSignUpPageLocators()
        super(EventSignUpPage, self).__init__(driver)

    def submit_form(self):
        self.element_by_xpath(self.elements.SUBMIT_PATH).submit()

    def click_to_view_jobs(self):
        self.element_by_xpath(self.elements.VIEW_JOBS_PATH+ "//a").click()

    def click_to_view_shifts(self):
        self.element_by_xpath(self.elements.VIEW_SHIFTS_PATH + "//a").click()

    def click_to_sign_up(self):
        self.element_by_xpath(self.elements.SHIFT_SIGNUP_PATH + "//a").click()

    def get_view_jobs(self):
        return self.element_by_xpath(self.elements.VIEW_JOBS_PATH).text

    def get_view_shifts(self):
        return self.element_by_xpath(self.elements.VIEW_SHIFTS_PATH).text

    def get_sign_up(self):
        return self.element_by_xpath(self.elements.SHIFT_SIGNUP_PATH).text

    def navigate_to_sign_up(self):
        self.home_page.get_shift_signup_link().click()

    def fill_search_form(self, date):
        self.element_by_id(self.elements.START_DATE_FROM).clear()
        self.element_by_id(self.elements.START_DATE_TO).clear()
        self.send_value_to_element_id(self.elements.START_DATE_FROM,date[0])
        self.send_value_to_element_id(self.elements.START_DATE_TO,date[1])
        self.submit_form()

    def get_info_box(self):
        return self.element_by_class_name(self.elements.INFO_BOX)

    def get_danger_box(self):
        self.element_by_class_name(self.elements.DANGER_BOX)

    def get_shift_job(self):
        return self.element_by_xpath(self.elements.SHIFT_JOB_PATH).text

    def get_shift_date(self):
        return self.element_by_xpath(self.elements.SHIFT_DATE_PATH).text

    def get_shift_start_time(self):
        return self.element_by_xpath(self.elements.SHIFT_STIME_PATH).text

    def get_shift_end_time(self):
        return self.element_by_xpath(self.elements.SHIFT_ETIME_PATH).text

    def find_table_tag(self):
        return self.element_by_tag_name('table')

    def get_event_name(self):
        return self.element_by_xpath(self.elements.EVENT_NAME).text

    def get_signed_up_shift_text(self):
        return self.element_by_xpath(self.elements.UPCOMING_SHIFT_SECTION).text

    def get_remaining_slots(self):
        return self.element_by_xpath(self.elements.SLOTS_REMAINING_PATH).text
