
class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

    def send_value_to_element_id(self, key, value):
    	self.driver.find_element_by_id(key).send_keys(value)

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

    def element_by_class_name(self,class_name):
        return self.driver.find_element_by_class_name(class_name)

    def get_value_for(self, field):
        return self.driver.find_element_by_id(field).get_attribute('value')

    def click_link(self, link_text):
        self.driver.find_element_by_link_text(link_text).click()

    def find_link(self, link_text):
        element = self.driver.find_element_by_link_text(link_text)
        return element if element else None
