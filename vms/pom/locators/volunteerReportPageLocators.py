class VolunteerReportPageLocators(object):

    REPORT_START_DATE = '//input[@name = "start_date"]'
    REPORT_END_DATE = '//input[@name = "end_date"]'
    REPORT_EVENT_SELECTOR = '//select[@name = "event_name"]'
    REPORT_JOB_SELECTOR = '//select[@name = "job_name"]'
    NO_RESULT_BOX = 'alert-danger'
    SUBMIT_PATH = '//form[1]'
    REPORT_HOURS_PATH = '//div[2]/div[4]/table/tbody/tr/td[2]'

