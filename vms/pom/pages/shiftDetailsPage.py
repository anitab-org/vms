# local Django
from pom.pages.basePage import BasePage
from pom.locators.shiftDetailsPageLocators import ShiftDetailsPageLocators 
from pom.pages.eventsPage import EventsPage
from pom.pageUrls import PageUrls


class ShiftDetailsPage(BasePage):

    shift_list_page = PageUrls.shift_list_page
    live_server_url = ''

    def __init__(self, driver):
        self.driver = driver
        self.elements = ShiftDetailsPageLocators()
        self.events_page = EventsPage(self.driver)
        super(ShiftDetailsPage, self).__init__(driver)

    def navigate_to_shift_details_view(self):
        self.events_page.live_server_url = self.live_server_url
        self.events_page.navigate_to_shift_list_view()
        self.element_by_xpath(self.elements.VIEW_DETAILS + '//a').click()

    def get_shift_job(self):
        return self.element_by_xpath(self.elements.JOB).text

    def get_shift_date(self):
        return self.element_by_xpath(self.elements.DATE).text

    def get_max_shift_volunteer(self):
        return self.element_by_xpath(self.elements.MAX_VOL).text

    def get_shift_start_time(self):
        return self.element_by_xpath(self.elements.START_TIME).text

    def get_shift_end_time(self):
        return self.element_by_xpath(self.elements.END_TIME).text

    def get_registered_volunteers(self):
        return self.elements_by_xpath(self.elements.REGISTERED_VOLUNTEER_LIST)

    def get_registered_volunteer_name(self):
        return self.element_by_xpath(
            self.elements.REGISTERED_VOLUNTEER_NAME).text

    def get_registered_volunteer_email(self):
        return self.element_by_xpath(self.elements.VOL_EMAIL).text

    def get_logged_volunteers(self):
        return self.elements_by_xpath(self.elements.LOGGED_VOLUNTEER_LIST)

    def get_logged_volunteer_name(self):
        return self.element_by_xpath(self.elements.LOGGED_VOLUNTEER).text

    def get_logged_start_time(self):
        return self.element_by_xpath(self.elements.LOGGED_START_TIME).text

    def get_logged_end_time(self):
        return self.element_by_xpath(self.elements.LOGGED_END_TIME).text

    def get_message_box(self):
        return self.element_by_class_name(self.elements.ALERT_BOX).text
