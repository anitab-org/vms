class CompletedShiftsPageLocators(object):

    UNLOGGED_SHIFT_JOB_PATH = '//*[@id="unlogged"]/tbody/tr/td[1]'
    UNLOGGED_SHIFT_DATE_PATH = '//*[@id="unlogged"]/tbody/tr/td[2]'
    UNLOGGED_SHIFT_STIME_PATH = '//*[@id="unlogged"]/tbody/tr/td[3]'
    UNLOGGED_SHIFT_ETIME_PATH = '//*[@id="unlogged"]/tbody/tr/td[4]'
    LOGGED_SHIFT_JOB_PATH = '//*[@id="logged"]/tbody/tr/td[1]'
    LOGGED_SHIFT_DATE_PATH = '//*[@id="logged"]/tbody/tr/td[2]'
    LOGGED_SHIFT_STIME_PATH = '//*[@id="logged"]/tbody/tr/td[3]'
    LOGGED_SHIFT_ETIME_PATH = '//*[@id="logged"]/tbody/tr/td[4]'
    SHIFT_EDIT_PATH = '//*[@id="logged"]/tbody/tr/td[5]'
    START_TIME_FORM = '//input[@name = "start_time"]'
    END_TIME_FORM = '//input[@name = "end_time"]'
    LOG_SHIFT_HOURS_PATH = '//*[@id="unlogged"]//tbody//tr//td[5]'
    CONTAINER = '//*[@id="unlogged"]'

    UNLOGGED_INFO_BOX = 'unlogged_alert'
    LOGGED_INFO_BOX = 'logged_alert'
    DANGER_BOX = 'alert-danger'
    SUBMIT_PATH = '//form[1]'

