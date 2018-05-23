# Third Party Imports
from selenium import webdriver

# Django imports
from django.contrib.staticfiles.testing import LiveServerTestCase

# Local Project Imports
from selenium.webdriver.common.keys import Keys


class DummyTesting(LiveServerTestCase):
    """
    Dummy Test Class to check the selenium is working correctly.
    Delete this file after uncommenting the selenium tests
    currently present.
    """

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        super(DummyTesting, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(DummyTesting, cls).tearDownClass()

    def test_working(self):
        """
        Dummy Test function to check working of selenium
        Delete this function after the first test for this
        Class is added.
        """
        self.driver.get("http://www.python.org")
        self.assertIn('Python', self.driver.title)
        element = self.driver.find_element_by_name('q')
        element.clear()
        element.send_keys('pycon')
        element.send_keys(Keys.RETURN)
        self.assertNotIn('No results found.', self.driver.page_source)

