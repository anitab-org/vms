
class EventsPageLocators(object):

	# locators for events, jobs, shifts  listed
	EVENT_NAME = '//table//tbody//tr[1]//td[1]'
	JOB_NAME = '//table//tbody//tr[1]//td[1]'
	JOB_EVENT = '//table//tbody//tr[1]//td[2]'
	SHIFT_DATE = '//table//tbody//tr[1]//td[1]'
	CREATED_ORG_NAME = '//table//tbody//tr[1]//td[1]'
	MESSAGE_BOX = 'alert-success'
	HELP_BLOCK = 'help-block'

	VIEW_SHIFT = '//table//tbody//tr[1]/td[5]//a'
	EDIT_EVENT = '//table//tbody//tr[1]//td[5]//a'
	EDIT_JOB = '//table//tbody//tr[1]//td[6]//a'
	EDIT_SHIFT = '//table//tbody//tr[1]//td[5]//a'
	EDIT_ORG = '//table//tbody//tr[1]//td[2]'
	DELETE_ORG = '//table//tbody//tr[1]//td[3]'
	DELETE_SHIFT = '//table//tbody//tr[1]//td[6]'
	DELETE_JOB = '//table//tbody//tr[1]//td[7]'
	DELETE_EVENT = '//table//tbody//tr[1]//td[6]'
	DELETION_BOX = 'panel-danger'
	DELETION_TOPIC = 'panel-heading'
	WARNING_CONTEXT = 'messages'
	TEMPLATE_ERROR_MESSAGE = '//div[2]/div[3]/p'
	DANGER_BOX = 'alert-danger'
	RESULTS = '//table//tbody'

	# locators for event, job and shift form
	JOB_EVENT_NAME = 'events'
	SHIFT_JOB = "//div[2]//div[1]/p"
	SHIFT_JOB_START_DATE = "//div[2]//div[2]/p"
	SHIFT_JOB_END_DATE = "//div[2]//div[3]/p"
	JOB_EVENT_START_DATE = 'start_date_here'
	JOB_EVENT_END_DATE = 'end_date_here'

	CREATE_EVENT_NAME ='//input[@placeholder = "Event Name"]'
	CREATE_EVENT_START_DATE = '//input[@name = "start_date"]'
	CREATE_EVENT_END_DATE = '//input[@name = "end_date"]'
	CREATE_EVENT_ID = '//select[@name = "event_id"]'
	CREATE_JOB_NAME = '//input[@placeholder = "Job Name"]'
	CREATE_JOB_DESCRIPTION = '//textarea[@name = "description"]'
	CREATE_JOB_START_DATE = '//input[@name = "start_date"]'
	CREATE_JOB_END_DATE = '//input[@name = "end_date"]'
	CREATE_SHIFT_DATE = '//input[@name = "date"]'
	CREATE_SHIFT_START_TIME = '//input[@name = "start_time"]'
	CREATE_SHIFT_END_TIME = '//input[@name = "end_time"]'
	CREATE_SHIFT_MAX_VOLUNTEER = '//input[@name = "max_volunteers"]'
	ORG_NAME = '//input[@name = "name"]'

	EVENT_NAME_ERROR = "//form//div[1]/div/p/strong"
	EVENT_START_DATE_ERROR = "//form//div[2]/div/p/strong"
	EVENT_END_DATE_ERROR = "//form//div[3]/div/p/strong"
	JOB_NAME_ERROR = "//form//div[3]/div/p/strong"
	JOB_START_DATE_ERROR = "//form//div[5]/div/p/strong"
	JOB_END_DATE_ERROR = "//form//div[6]/div/p/strong"
	SHIFT_DATE_ERROR = "//form//div[4]/div/p/strong"
	SHIFT_START_TIME_ERROR = "//form//div[5]/div/p/strong"
	SHIFT_END_TIME_ERROR = "//form//div[6]/div/p/strong"
	SHIFT_MAX_VOLUNTEER_ERROR = "//form//div[7]/div/p/strong"

	GENERAL_SUBMIT_PATH = '//form[1]'
