
class CompletedShiftsPageLocators(object):

    SHIFT_JOB_PATH = '//table//tbody//tr[1]//td[1]'
    SHIFT_DATE_PATH = '//table//tbody//tr[1]//td[2]'
    SHIFT_STIME_PATH = '//table//tbody//tr[1]//td[3]'
    SHIFT_ETIME_PATH = '//table//tbody//tr[1]//td[4]'
    SHIFT_EDIT_PATH = '//table//tbody//tr[1]//td[5]'
    SHIFT_CLEAR_PATH = '//table//tbody//tr[1]//td[6]'
    START_TIME_FORM = '//input[@name = "start_time"]'
    END_TIME_FORM = '//input[@name = "end_time"]'
    CLEAR_SHIFT_HOURS_TEXT = 'html/body/div[2]/form/div/div[1]/h3'

    INFO_BOX = 'alert-info'
    DANGER_BOX = 'alert-danger'
    SUBMIT_PATH = '//form[1]'
