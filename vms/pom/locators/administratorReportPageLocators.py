class AdministratorReportPageLocators(object):

    REPORT_SHIFT_SUMMARY_PATH = '//div[2]/div[4]'
    REPORT_START_DATE = '//input[@name = "start_date"]'
    REPORT_END_DATE = '//input[@name = "end_date"]'
    REPORT_EVENT_SELECTOR = '//select[@name = "event_name"]'
    REPORT_JOB_SELECTOR = '//select[@name = "job_name"]'
    REPORT_ORG_SELECTOR = '//select[@name = "organization"]'
    FIRST_NAME_SELECTOR = '//input[@name = "first_name"]'
    LAST_NAME_SELECTOR = '//input[@name = "last_name"]'

    NAME = '//table//tbody//tr[1]//td[4]'
    DATE = '//table//tbody//tr[1]//td[6]'
    START_TIME = '//table//tbody//tr[1]//td[7]'
    END_TIME = '//table//tbody//tr[1]//td[8]'
    HOURS = '//table//tbody//tr[1]//td[9]'

    SUBMIT_PATH = '//form[1]'
    NO_RESULT_BOX = 'alert-danger'
