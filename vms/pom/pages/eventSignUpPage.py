# local Django
from pom.pages.basePage import BasePage
from pom.locators.eventSignUpPageLocators import EventSignUpPageLocators
from pom.pages.homePage import HomePage


class EventSignUpPage(BasePage):

    no_event_message = 'There are no events.'
    live_server_url = ''
    SHIFT_UNAVAILABLE_FOR_JOB = 'There are currently no shifts for the job {0}.'

    def __init__(self, driver):
        self.driver = driver
        self.home_page = HomePage(self.driver)
        self.elements = EventSignUpPageLocators()
        super(EventSignUpPage, self).__init__(driver)

    def submit_search_form(self):
        self.element_by_id(self.elements.SEARCH_SUBMIT_PATH).click()

    def submit_form(self):
        self.element_by_xpath(self.elements.SUBMIT_PATH).submit()

    def click_to_view_jobs(self):
        self.element_by_xpath(self.elements.VIEW_JOBS_PATH + "//a").click()

    def click_to_view_shifts(self):
        self.element_by_xpath(self.elements.VIEW_SHIFTS_PATH + "//a").click()

    def click_to_sign_up(self):
        self.element_by_xpath(self.elements.SHIFT_SIGNUP_PATH + "//a").click()

    def go_to_sign_up_page(self):
        element = self.element_by_xpath(self.elements.SHIFT_SIGNUP_PAGE + '//a')
        self.execute_script('arguments[0].click();', element)

    def get_view_jobs(self):
        return self.element_by_xpath(self.elements.VIEW_JOBS_PATH).text

    def get_view_shifts(self):
        return self.element_by_xpath(self.elements.VIEW_SHIFTS_PATH).text

    def get_sign_up(self):
        return self.element_by_xpath(self.elements.SHIFT_SIGNUP_PATH).text

    def navigate_to_sign_up(self):
        self.get_page(self.get_sign_up_link(), '')

    def get_sign_up_link(self):
        return self.home_page.get_shift_signup_link().get_attribute('href')

    def fill_search_form(self, parameters):
        self.element_by_id(self.elements.SEARCH_EVENT_NAME).clear()
        self.element_by_id(self.elements.START_DATE_FROM).clear()
        self.element_by_id(self.elements.START_DATE_TO).clear()
        self.element_by_id(self.elements.EVENT_CITY).clear()
        self.element_by_id(self.elements.EVENT_STATE).clear()
        self.element_by_id(self.elements.EVENT_COUNTRY).clear()

        self.send_value_to_element_id(
            self.elements.SEARCH_EVENT_NAME,
            parameters['name']
        )
        self.send_value_to_element_id(
            self.elements.START_DATE_FROM,
            parameters['date_from']
        )
        self.send_value_to_element_id(
            self.elements.START_DATE_TO,
            parameters['date_to']
        )
        self.send_value_to_element_id(
            self.elements.EVENT_CITY,
            parameters['city']
        )
        self.send_value_to_element_id(
            self.elements.EVENT_STATE,
            parameters['state']
        )
        self.send_value_to_element_id(
            self.elements.EVENT_COUNTRY,
            parameters['country']
        )
        self.submit_search_form()

    def fill_job_search_form(self, parameters):
        self.element_by_id(self.elements.SEARCH_JOB_NAME).clear()
        self.element_by_id(self.elements.JOB_START_DATE_FROM).clear()
        self.element_by_id(self.elements.JOB_START_DATE_TO).clear()
        self.element_by_id(self.elements.JOB_CITY).clear()
        self.element_by_id(self.elements.JOB_STATE).clear()
        self.element_by_id(self.elements.JOB_COUNTRY).clear()
        self.send_value_to_element_id(
            self.elements.SEARCH_JOB_NAME,
            parameters['name']
        )
        self.send_value_to_element_id(
            self.elements.JOB_START_DATE_FROM,
            parameters['date_from']
        )
        self.send_value_to_element_id(
            self.elements.JOB_START_DATE_TO,
            parameters['date_to']
        )
        self.send_value_to_element_id(
            self.elements.JOB_CITY,
            parameters['city']
        )
        self.send_value_to_element_id(
            self.elements.JOB_STATE,
            parameters['state']
        )
        self.send_value_to_element_id(
            self.elements.JOB_COUNTRY,
            parameters['country']
        )
        self.submit_search_form()

    def get_job_name(self):
        return self.element_by_xpath(self.elements.EVENT_JOB_NAME).text

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

    def get_message_shift_not_available_for_job(self, job):
        return self.SHIFT_UNAVAILABLE_FOR_JOB.format(job)
