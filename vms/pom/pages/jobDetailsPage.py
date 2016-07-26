from basePage import *
from pom.locators.jobDetailsPageLocators import *
from pom.pages.eventsPage import EventsPage

class JobDetailsPage(BasePage):

    live_server_url = ''

    def __init__(self, driver):
        self.driver = driver
        self.elements = JobDetailsPageLocators()
        self.events_page = EventsPage(self.driver)
        super(JobDetailsPage, self).__init__(driver)

    def navigate_to_job_details_view(self):
        self.events_page.live_server_url = self.live_server_url
        self.events_page.navigate_to_job_list_view()
        self.element_by_xpath(self.elements.VIEW_DETAILS).click()

    def get_start_date(self):
        return self.element_by_xpath(self.elements.JOB_START_DATE).text

    def get_end_date(self):
        return self.element_by_xpath(self.elements.JOB_END_DATE).text

    def get_name(self):
        return self.element_by_xpath(self.elements.JOB_NAME).text

    def get_event_name(self):
        return self.element_by_xpath(self.elements.JOB_EVENT).text
