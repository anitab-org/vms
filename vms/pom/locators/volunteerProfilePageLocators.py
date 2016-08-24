
class VolunteerProfilePageLocators(object):

	PROFILE_FIRST_NAME = '//input[@name = "first_name"]'
	PROFILE_LAST_NAME = '//input[@name = "last_name"]'
	PROFILE_EMAIL = '//input[@name = "email"]'
	PROFILE_ADDRESS = '//input[@name = "address"]'
	PROFILE_CITY = '//input[@name = "city"]'
	PROFILE_STATE = '//input[@name = "state"]'
	PROFILE_COUNTRY = '//input[@name = "country"]'
	PROFILE_PHONE = '//input[@name = "phone_number"]'
	SELECT_ORGANIZATION = '//select[@name = "organization_name"]'
	UNLISTED_ORGANIZATION = '//input[@name = "unlisted_organization"]'
	RESUME_FILE = '//input[@name = "resume_file"]'
	DOWNLOAD_RESUME = './/*[@id="collapseResumeFile"]/div/form/button'
	EDIT_PROFILE_TEXT = 'Edit Profile'
	INVALID_FORMAT_MESSAGE = 'html/body/div[2]/div[2]/form/fieldset/div[13]/div/p/strong'
	SUBMIT_PATH = '//form[1]'
