# third party

# local Django
from pom.pages.basePage import BasePage
from pom.locators.eventsPageLocators import EventsPageLocators
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
    FIELD_REQUIRED = 'This field is required.'
    NO_EVENT_PRESENT = 'No event found.'
    START_BEFORE_END = 'Start date must be before the end date'

    def __init__(self, driver):
        self.driver = driver
        self.home_page = HomePage(self.driver)
        self.elements = EventsPageLocators()
        super(EventsPage, self).__init__(driver)

    def fill_event_form(self, event):
        self.element_by_xpath(self.elements.CREATE_EVENT_NAME).clear()
        self.element_by_xpath(self.elements.CREATE_EVENT_START_DATE).clear()
        self.element_by_xpath(self.elements.CREATE_EVENT_END_DATE).clear()
        self.element_by_xpath(self.elements.CREATE_EVENT_ADDRESS).clear()
        self.element_by_xpath(self.elements.CREATE_EVENT_VENUE).clear()
        self.send_value_to_xpath(self.elements.CREATE_EVENT_NAME, event['name'])
        self.send_value_to_xpath(
            self.elements.CREATE_EVENT_START_DATE,
            event['start_date']
        )
        self.send_value_to_xpath(
            self.elements.CREATE_EVENT_END_DATE,
            event['end_date']
        )
        self.send_value_to_xpath(
            self.elements.CREATE_EVENT_ADDRESS,
            event['address']
        )
        self.send_value_to_xpath(
            self.elements.CREATE_EVENT_VENUE,
            event['venue']
        )
        self.submit_form()

    def fill_job_form(self, job):
        self.element_by_xpath(self.elements.CREATE_JOB_NAME).clear()
        self.element_by_xpath(self.elements.CREATE_JOB_DESCRIPTION).clear()
        self.element_by_xpath(self.elements.CREATE_JOB_START_DATE).clear()
        self.element_by_xpath(self.elements.CREATE_JOB_END_DATE).clear()

        self.send_value_to_xpath(self.elements.CREATE_EVENT_ID, job['event'])
        self.send_value_to_xpath(self.elements.CREATE_JOB_NAME, job['name'])
        self.send_value_to_xpath(
            self.elements.CREATE_JOB_DESCRIPTION,
            job['description']
        )
        self.send_value_to_xpath(
            self.elements.CREATE_JOB_START_DATE,
            job['start_date']
        )
        self.send_value_to_xpath(
            self.elements.CREATE_JOB_END_DATE,
            job['end_date']
        )
        self.submit_form()

    def fill_shift_form(self, shift):
        self.element_by_xpath(self.elements.CREATE_SHIFT_DATE).clear()
        self.element_by_xpath(self.elements.CREATE_SHIFT_START_TIME).clear()
        self.element_by_xpath(self.elements.CREATE_SHIFT_END_TIME).clear()
        self.element_by_xpath(self.elements.CREATE_SHIFT_MAX_VOLUNTEER).clear()
        self.element_by_xpath(self.elements.CREATE_SHIFT_ADDRESS).clear()
        self.element_by_xpath(self.elements.CREATE_SHIFT_VENUE).clear()

        self.send_value_to_xpath(self.elements.CREATE_SHIFT_DATE, shift['date'])
        self.send_value_to_xpath(
            self.elements.CREATE_SHIFT_START_TIME,
            shift['start_time']
        )
        self.send_value_to_xpath(
            self.elements.CREATE_SHIFT_END_TIME,
            shift['end_time']
        )
        self.send_value_to_xpath(
            self.elements.CREATE_SHIFT_MAX_VOLUNTEER,
            shift['max_volunteers']
        )
        self.send_value_to_xpath(
            self.elements.CREATE_SHIFT_ADDRESS,
            shift['address']
        )
        self.send_value_to_xpath(
            self.elements.CREATE_SHIFT_VENUE,
            shift['venue']
        )
        self.submit_form()

    def fill_organization_form(self, org):
        self.element_by_xpath(self.elements.ORG_NAME).clear()
        self.send_value_to_xpath(self.elements.ORG_NAME, org)
        self.submit_form()

    def submit_form(self):
        self.element_by_xpath(self.elements.GENERAL_SUBMIT_PATH).submit()

    def go_to_events_page(self):
        self.home_page.get_events_link().click()

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

    def go_to_details_event_page(self):
        self.element_by_xpath(self.elements.VIEW_EVENT).click()

    def get_event_description(self):
        return self.element_by_xpath('//div[@class="panel-body"]').text

    def go_to_edit_event_page(self):
        self.element_by_xpath(self.elements.EDIT_EVENT).click()

    def go_to_create_job_page(self):
        self.click_link('Create Job')

    def go_to_edit_job_page(self):
        self.element_by_xpath(self.elements.EDIT_JOB).click()

    def go_to_create_shift_page(self):
        self.click_link('Create Shift')

    def go_to_edit_shift_page(self):
        self.element_by_xpath(self.elements.EDIT_SHIFT).click()

    def go_to_create_organization_page(self):
        self.click_link('Create Organization')

    def go_to_edit_organization_page(self):
        self.element_by_xpath(self.elements.EDIT_ORG).click()

    def get_deletion_box(self):
        return self.element_by_class_name(self.elements.DELETION_BOX)

    def get_delete_event_element(self, relative):
        return self.element_by_xpath(self.elements.DELETE_EVENT + relative)

    def get_deletion_context(self):
        return self.element_by_class_name(self.elements.DELETION_TOPIC).text

    def get_message_context(self):
        return self.element_by_class_name(self.elements.MESSAGE_BOX).text

    def get_event_name(self):
        return self.element_by_xpath(self.elements.EVENT_NAME).text

    def get_event_start_date(self):
        return self.element_by_xpath(self.elements.EVENT_START_DATE).text

    def get_event_end_date(self):
        return self.element_by_xpath(self.elements.EVENT_END_DATE).text

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

    def get_unlisted_org_name(self):
        return self.element_by_xpath(self.elements.UNLISTED_ORG_NAME).text

    def get_rejection_context(self):
        return self.element_by_xpath(self.elements.REJECT_ORG).text

    def reject_org(self):
        self.element_by_xpath(self.elements.REJECT_ORG + '//a').click()

    def get_approval_context(self):
        return self.element_by_xpath(self.elements.APPROVE_ORG).text

    def approve_org(self):
        self.element_by_xpath(self.elements.APPROVE_ORG + '//a').click()

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
        return self.driver.find_element_by_xpath(
            self.elements.SHIFT_END_TIME_ERROR
        ).text

    def get_shift_max_volunteer_error(self):
        return self.element_by_xpath(
            self.elements.SHIFT_MAX_VOLUNTEER_ERROR
        ).text

    def get_shift_address_error(self):
        return self.element_by_xpath(self.elements.SHIFT_ADDRESS_ERROR).text

    def get_shift_venue_error(self):
        return self.element_by_xpath(self.elements.SHIFT_VENUE_ERROR).text

    def get_organization_name_error(self):
        return self.element_by_xpath(self.elements.ORGANIZATION_NAME_ERROR).text

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
        return self.get_value_for_xpath(
            self.elements.CREATE_SHIFT_MAX_VOLUNTEER
        )

    def get_help_blocks(self):
        blocks = self.elements_by_class_name(self.elements.HELP_BLOCK)
        return blocks
