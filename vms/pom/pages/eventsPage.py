from basePage import *
from pom.locators.eventsPageLocators import *
from selenium.webdriver.support.ui import Select
from pom.pages.homePage import HomePage
from pom.pageUrls import PageUrls

class EventsPage(BasePage):

    event_list_page = PageUrls.event_list_page
    job_list_page = PageUrls.job_list_page
    shift_list_page = PageUrls.shift_list_page
    organization_list_page = PageUrls.organization_list_page
    create_organization_page = '/organization/create/'
    create_job_page = '/job/create/'
    create_event_page = '/event/create/'
    jobs_tab = 'Jobs'
    shift_tab = 'Shifts'
    organization_tab = 'Organizations'
    live_server_url = ''

    def __init__(self, driver):
        self.driver = driver
        self.home_page = HomePage(self.driver)
        self.elements = EventsPageLocators()
        super(EventsPage, self).__init__(driver)

    def fill_event_form(self, event):
        self.element_by_xpath(self.elements.CREATE_EVENT_NAME).clear()
        self.element_by_xpath(self.elements.CREATE_EVENT_START_DATE).clear()
        self.element_by_xpath(self.elements.CREATE_EVENT_END_DATE).clear()
        self.send_value_to_xpath(self.elements.CREATE_EVENT_NAME, event[0])
        self.send_value_to_xpath(self.elements.CREATE_EVENT_START_DATE, event[1])
        self.send_value_to_xpath(self.elements.CREATE_EVENT_END_DATE, event[2])
        self.submit_form()

    def fill_job_form(self, job):
        self.element_by_xpath(self.elements.CREATE_JOB_NAME).clear()
        self.element_by_xpath(self.elements.CREATE_JOB_DESCRIPTION).clear()
        self.element_by_xpath(self.elements.CREATE_JOB_START_DATE).clear()
        self.element_by_xpath(self.elements.CREATE_JOB_END_DATE).clear()

        self.send_value_to_xpath(self.elements.CREATE_EVENT_ID,job[0])
        self.send_value_to_xpath(self.elements.CREATE_JOB_NAME,job[1])
        self.send_value_to_xpath(self.elements.CREATE_JOB_DESCRIPTION,job[2])
        self.send_value_to_xpath(self.elements.CREATE_JOB_START_DATE,job[3])
        self.send_value_to_xpath(self.elements.CREATE_JOB_END_DATE,job[4])
        self.submit_form()

    def fill_shift_form(self, shift):
        self.element_by_xpath(self.elements.CREATE_SHIFT_DATE).clear()
        self.element_by_xpath(self.elements.CREATE_SHIFT_START_TIME).clear()
        self.element_by_xpath(self.elements.CREATE_SHIFT_END_TIME).clear()
        self.element_by_xpath(self.elements.CREATE_SHIFT_MAX_VOLUNTEER).clear()

        self.send_value_to_xpath(self.elements.CREATE_SHIFT_DATE,shift[0])
        self.send_value_to_xpath(self.elements.CREATE_SHIFT_START_TIME,shift[1])
        self.send_value_to_xpath(self.elements.CREATE_SHIFT_END_TIME,shift[2])
        self.send_value_to_xpath(self.elements.CREATE_SHIFT_MAX_VOLUNTEER,shift[3])
        self.submit_form()

    def fill_organization_form(self, org):
        self.element_by_xpath(self.elements.ORG_NAME).clear()
        self.send_value_to_xpath(self.elements.ORG_NAME,org)
        self.submit_form()

    def submit_form(self):
        self.element_by_xpath(self.elements.GENERAL_SUBMIT_PATH).submit()

    def go_to_events_page(self):
        self.home_page.get_events_link().send_keys('\n')

    def navigate_to_event_list_view(self):
        self.get_page(self.live_server_url, self.event_list_page)

    def navigate_to_job_list_view(self):
        self.get_page(self.live_server_url, self.job_list_page)

    def navigate_to_shift_list_view(self):
        self.get_page(self.live_server_url, self.shift_list_page)
        self.element_by_xpath(self.elements.VIEW_SHIFT).click()

    def navigate_to_organization_view(self):
        self.get_page(self.live_server_url, self.organization_list_page)

    def go_to_create_event_page(self):
        self.click_link('Create Event')

    def go_to_edit_event_page(self):
        self.element_by_xpath(self.elements.EDIT_EVENT).click()

    def go_to_create_job_page(self):
        self.get_page(self.live_server_url, self.create_job_page)

    def go_to_edit_job_page(self):
        self.element_by_xpath(self.elements.EDIT_JOB).click()

    def go_to_create_shift_page(self):
        self.click_link('Create Shift')

    def go_to_edit_shift_page(self):
        self.element_by_xpath(self.elements.EDIT_SHIFT).click()

    def go_to_create_organization_page(self):
        self.get_page(self.live_server_url, self.create_organization_page)

    def get_deletion_box(self):
        return self.element_by_class_name(self.elements.DELETION_BOX)

    def get_deletion_context(self):
        return self.element_by_class_name(self.elements.DELETION_TOPIC).text

    def get_message_context(self):
        return self.element_by_class_name(self.elements.MESSAGE_BOX).text

    def get_event_name(self):
        return self.element_by_xpath(self.elements.EVENT_NAME).text

    def get_warning_context(self):
        return self.element_by_class_name(self.elements.WARNING_CONTEXT).text

    def get_danger_message(self):
        return self.element_by_class_name(self.elements.DANGER_BOX)

    def get_job_name(self):
        return self.element_by_xpath(self.elements.JOB_NAME).text

    def get_job_event(self):
        return self.element_by_xpath(self.elements.JOB_EVENT).text

    def get_template_error_message(self):
        return self.element_by_xpath(self.elements.TEMPLATE_ERROR_MESSAGE).text

    def get_results(self):
        return self.element_by_xpath(self.elements.RESULTS)

    def get_shift_date(self):
        return self.element_by_xpath(self.elements.SHIFT_DATE).text

    def get_help_block(self):
        return self.element_by_class_name(self.elements.HELP_BLOCK)

    def get_org_name(self):
        return self.element_by_xpath(self.elements.CREATED_ORG_NAME).text

    def get_help_blocks(self):
        return self.elements_by_class_name(self.elements.HELP_BLOCK)

    def get_event_name_error(self):
        return self.element_by_xpath(self.elements.EVENT_NAME_ERROR).text

    def get_event_start_date_error(self):
        return self.element_by_xpath(self.elements.EVENT_START_DATE_ERROR).text

    def get_event_end_date_error(self):
        return self.element_by_xpath(self.elements.EVENT_END_DATE_ERROR).text

    def get_job_name_error(self):
        return self.element_by_xpath(self.elements.JOB_NAME_ERROR).text

    def get_job_start_date_error(self):
        return self.element_by_xpath(self.elements.JOB_START_DATE_ERROR).text

    def get_job_end_date_error(self):
        return self.element_by_xpath(self.elements.JOB_END_DATE_ERROR).text

    def get_shift_date_error(self):
        return self.element_by_xpath(self.elements.SHIFT_DATE_ERROR).text

    def get_shift_start_time_error(self):
        return self.element_by_xpath(self.elements.SHIFT_START_TIME_ERROR).text

    def get_shift_end_time_error(self):
        return self.driver.find_element_by_xpath(self.elements.SHIFT_END_TIME_ERROR).text

    def get_shift_max_volunteer_error(self):
        return self.element_by_xpath(self.elements.SHIFT_MAX_VOLUNTEER_ERROR).text

    def get_shift_job(self):
        return self.element_by_xpath(self.elements.SHIFT_JOB).text

    def get_shift_job_start_date(self):
        return self.element_by_xpath(self.elements.SHIFT_JOB_START_DATE).text

    def get_shift_job_end_date(self):
        return self.element_by_xpath(self.elements.SHIFT_JOB_END_DATE).text

    def get_job_event_start_date(self):
        return self.element_by_id(self.elements.JOB_EVENT_START_DATE).text

    def get_job_event_end_date(self):
        return self.element_by_id(self.elements.JOB_EVENT_END_DATE).text

    def get_event_name_value(self):
        return self.get_value_for_xpath(self.elements.CREATE_EVENT_NAME)

    def get_event_start_date_value(self):
        return self.get_value_for_xpath(self.elements.CREATE_EVENT_START_DATE)

    def get_event_end_date_value(self):
        return self.get_value_for_xpath(self.elements.CREATE_EVENT_END_DATE)

    def get_job_name_value(self):
        return self.get_value_for_xpath(self.elements.CREATE_JOB_NAME)

    def get_job_start_date_value(self):
        return self.get_value_for_xpath(self.elements.CREATE_JOB_START_DATE)

    def get_job_end_date_value(self):
        return self.get_value_for_xpath(self.elements.CREATE_JOB_END_DATE)

    def get_job_description_value(self):
        return self.get_value_for_xpath(self.elements.CREATE_JOB_DESCRIPTION)

    def get_shift_date_value(self):
        return self.get_value_for_xpath(self.elements.CREATE_SHIFT_DATE)

    def get_shift_start_time_value(self):
        return self.get_value_for_xpath(self.elements.CREATE_SHIFT_START_TIME)

    def get_shift_end_time_value(self):
        return self.get_value_for_xpath(self.elements.CREATE_SHIFT_END_TIME)

    def get_shift_max_volunteers(self):
        return self.get_value_for_xpath(self.elements.CREATE_SHIFT_MAX_VOLUNTEER)
