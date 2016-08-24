
class EventSignUpPageLocators(object):

	SHIFT_JOB_PATH = '//table//tbody//tr[1]//td[1]'
	SHIFT_DATE_PATH = '//table//tbody//tr[1]//td[2]'
	SHIFT_STIME_PATH = '//table//tbody//tr[1]//td[3]'
	SHIFT_ETIME_PATH = '//table//tbody//tr[1]//td[4]'
	VIEW_JOBS_PATH = '//table//tbody//tr[1]//td[4]'
	VIEW_SHIFTS_PATH = '//table//tbody//tr[1]//td[4]'
	EVENT_NAME = '//table//tbody//tr[1]//td[1]'
	UPCOMING_SHIFT_SECTION = 'html/body/div[2]/h3'
	SLOTS_REMAINING_PATH = '//table//tbody//tr[1]//td[5]'

	# search form locators
	START_DATE_FROM = 'from'
	START_DATE_TO = 'to'

	# Two choices depending on whether volunteer or admin
	ASSIGN_SHIFTS_PATH = '//table//tbody//tr[1]//td[4]'
	SHIFT_SIGNUP_PATH = '//table//tbody//tr[1]//td[4]'

	INFO_BOX = 'alert-info'
	DANGER_BOX = 'alert-danger'
	SUBMIT_PATH = '//form[1]'
