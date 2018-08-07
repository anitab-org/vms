# local Django
from pom.pageUrls import PageUrls
from pom.pages.basePage import BasePage
from pom.locators.jobDetailsPageLocators import JobDetailsPageLocators
from pom.pages.eventsPage import EventsPage


class JobDetailsPage(BasePage):
    live_server_url = ''
    job_list_page = PageUrls.job_list_page
    create_job_page = '/job/create/'
    jobs_tab = 'Jobs'
    create_job_tab = 'Create Job'
    NO_JOBS_PRESENT = 'No jobs present.'
    ADD_EVENTS_TO_JOB = 'Please add events to associate with jobs first.'

    def __init__(self, driver):
        self.driver = driver
        self.elements = JobDetailsPageLocators()
        self.events_page = EventsPage(self.driver)
        super(JobDetailsPage, self).__init__(driver)

    def navigate_to_job_details_view(self):
        self.events_page.live_server_url = self.live_server_url
        self.events_page.navigate_to_job_list_view()
        self.element_by_xpath(self.elements.VIEW_DETAILS).click()

    def navigate_to_event_list_view(self):
        self.events_page.go_to_events_page()

    def navigate_to_job_list_view(self):
        self.events_page.live_server_url = self.live_server_url
        self.events_page.navigate_to_job_list_view()

    def go_to_edit_job_page(self):
        self.events_page.go_to_edit_job_page()

    def go_to_create_job_page(self):
        self.events_page.go_to_create_job_page()

    def get_help_blocks(self):
        return self.events_page.get_help_blocks()

    def get_job_name_error(self):
        return self.events_page.get_job_name_error()

    def get_job_start_date_error(self):
        return self.events_page.get_job_start_date_error()

    def get_job_end_date_error(self):
        return self.events_page.get_job_end_date_error()

    def fill_job_form(self, edit_job):
        self.events_page.fill_job_form(edit_job)

    def get_start_date(self):
        return self.element_by_xpath(self.elements.JOB_START_DATE).text

    def get_end_date(self):
        return self.element_by_xpath(self.elements.JOB_END_DATE).text

    def get_name(self):
        return self.element_by_xpath(self.elements.JOB_NAME).text

    def get_event_name(self):
        return self.element_by_xpath(self.elements.JOB_EVENT).text

    def get_description(self):
        self.element_by_xpath(self.elements.VIEW_DETAILS).click()
        return self.element_by_xpath('//div[@class="panel-body"]').text

    def get_delete_element(self, relative):
        return self.events_page.element_by_xpath(
            self.events_page.elements.DELETE_JOB +
            relative
        )

    def get_deletion_context(self):
        return self.events_page.get_deletion_context()

    def submit_form(self):
        self.events_page.submit_form()

    def get_message_context(self):
        return self.events_page.get_message_context()
