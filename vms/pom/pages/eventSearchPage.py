# Django
from pom.pages.basePage import BasePage

# local Django
from pom.locators.eventSearchPageLocators import EventSearchPageLocators
from pom.pages.authenticationPage import AuthenticationPage
from pom.pageUrls import PageUrls


class EventSearchPage(BasePage):

    event_search_page = PageUrls.event_list_page

    def __init__(self, driver):
        self.driver = driver
        self.authentication_page = AuthenticationPage(self.driver)
        self.elements = EventSearchPageLocators()
        super(EventSearchPage, self).__init__(driver)

    def navigate_to_event_search_page(self):
        self.get_page(self.live_server_url, self.event_search_page)

    def submit_form(self):
        self.element_by_id(self.elements.SUBMIT_PATH).click()

    def send_to_field(self, field, value):
        text_box = self.find_element_by_css_selector(field)
        text_box.clear()
        text_box.send_keys(value)

    def search_name_field(self, search_text):
        self.send_to_field(self.elements.NAME_FIELD, search_text)

    def search_start_date_field(self, search_text):
        self.send_to_field(self.elements.START_DATE_FIELD, search_text)

    def search_end_date_field(self, search_text):
        self.send_to_field(self.elements.END_DATE_FIELD, search_text)

    def search_city_field(self, search_text):
        self.send_to_field(self.elements.CITY_FIELD, search_text)

    def search_state_field(self, search_text):
        self.send_to_field(self.elements.STATE_FIELD, search_text)

    def search_country_field(self, search_text):
        self.send_to_field(self.elements.COUNTRY_FIELD, search_text)

    def search_job_field(self, search_text):
        self.send_to_field(self.elements.JOB_FIELD, search_text)

    def get_help_block(self):
        return self.element_by_class_name(self.elements.HELP_BLOCK)

    def get_search_results(self):
        search_results = self.element_by_xpath(self.elements.RESULT_BODY)
        return search_results

    def get_results_list(self, search_results):

        result = []
        for tr in search_results.find_elements_by_tag_name('tr'):
            row = tr.text.split()
            result.append(row)

        return result
