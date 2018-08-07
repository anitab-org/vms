class BasePage(object):
    """
    Base class to initialize the base page
    that will be called from all pages
    """
    ENTER_VALID_VALUE = 'Enter a valid value.'
    FIELD_REQUIRED = 'This field is required.'
    FIELD_CANNOT_LEFT_BLANK = 'This field cannot be blank.'
    START_BEFORE_END = 'Start date must be before the end date'
    ENTER_VALID_USERNAME = 'Enter a valid username. ' \
                           'This value may contain only letters, ' \
                           'numbers, and @/./+/-/_ characters.'

    def __init__(self, driver):
        self.driver = driver

    def send_value_to_element_id(self, key, value):
        self.driver.find_element_by_id(key).send_keys(value)

    def send_value_to_xpath(self, key, value):
        self.driver.find_element_by_xpath(key).send_keys(value)

    def element_by_xpath(self, path):
        return self.driver.find_element_by_xpath(path)

    def elements_by_xpath(self, path):
        elements = self.driver.find_elements_by_xpath(path)
        return elements if elements else None

    def get_page(self, base, relative_url):
        self.driver.get(base + relative_url)

    def elements_by_class_name(self, class_name):
        elements = self.driver.find_elements_by_class_name(class_name)
        return elements if elements else None

    def find_element_by_css_selector(self, selector):
        return self.driver.find_element_by_css_selector(selector)

    def element_by_class_name(self, class_name):
        return self.driver.find_element_by_class_name(class_name)

    def get_value_for(self, field):
        return self.driver.find_element_by_id(field).get_attribute('value')

    def click_link(self, link_text):
        self.driver.find_element_by_link_text(link_text).click()

    def find_link(self, link_text):
        element = self.driver.find_element_by_link_text(link_text)
        return element if element else None

    def element_by_id(self, id_name):
        return self.driver.find_element_by_id(id_name)

    def get_value_for_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath).get_attribute('value')

    def element_by_tag_name(self, tag):
        return self.driver.find_element_by_tag_name(tag)

    def execute_script(self, script, element):
        self.driver.execute_script(script, element)

    @staticmethod
    def remove_i18n(string):
        slashes = [pos for pos, char in enumerate(string) if char == '/']
        return string[:slashes[2]] + string[slashes[3]:]

