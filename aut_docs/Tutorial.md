## This tutorial will guide you to get started with automated testing.

Consider this testcase for tutorial;

You are an administrator of an organization and want to create a new event
for your organization.
 
Before diving into the code, we need to first break any testcase into
sub-parts of actions. This testcase can be broken as follows:

- Initiate WebDriver to open Firefox session.
- Create an administrator.
- Redirect to login page.
- Login as administrator with correct credentials.
- Redirect to event's view page.
- Redirect to create events form.
- Fill and submit the event form.
- Retrieve the details of the event created.
- Assert the results.
- Quit the browser session.

Now, since the action map is planned, it just needs to be converted it into code statements now.

Before starting it is crucial to decide which test case to use. Django provides inbuilt testcase of which two are used a lot `LiveServerTestCase` and `StaticLiveServerTestCase`. Both work in the same manner which is they create a server for the test to run in but the difference is that the later one displays the CSS instead of just loading it. 

Lets start by importing this TestCase and a few other necessary imports.
```python
    from selenium import webdriver
    from django.contrib.staticfiles.testing import LiveServerTestCase
    from django.contrib.auth.models import User
    from administrator.models import Administrator
```

1. Initiate WebDriver to open Firefox session.

    Usually this is done only once per test suite i.e. at class level since all tests can be executed withing a single session.
    This can be done as follows:
    ```python
        class LearningAutomatedTesting(LiveServerTestCase):
            @classmethod
            def setUpClass(cls):
                cls.driver = webdriver.Firefox()
                cls.driver.implicitly_wait(5)
                cls.driver.maximize_window()
                # Initiate POM pages here
                super(LearningAutomatedTesting, cls).setUpClass()
    ```

2. Create an administrator.

    Next step is to create an administrator.
    
    ```python
        def test_learn_automated_testing(self):
            # Creating administrator
            user_1 = User.objects.create_user(username='admin', password='admin')
            Administrator.objects.create(user=user_1, address='address', city='city',
                                         state='state', country='country', phone_number='9999999999',
                                         email='admin@admin.com', unlisted_organization='organization')
    ```

3. Redirect to login page.

    After creating an administrator next step is to redirecting to login page to Log In.
    ```python
        def test_learn_automated_testing(self):
            # Earlier code...
            self.get_page(self.live_server_url, '/authentication/login/')
    ```

4. Login as administrator with correct credentials.

    Now after redirecting to login page, the credentials need to sent to the login form and submit the form to authorize and redirect to home page.
    ```python
        def test_learn_automated_testing(self):
            # Earlier code...
            self.send_value_to_element_id('id_login', 'admin')
            self.send_value_to_element_id('id_password', 'admin')
            self.element_by_xpath('//form[1]').submit()
    ```

5. Redirect to event's view page.
    
    After logging in with correct credentials, the home page will appear. The next task is to click on `Events` item present on the navbar to redirect to the event display view.
    ```python
       def test_learn_automated_testing(self):
           # Earlier code...
           element = self.driver.find_element_by_link_text('Events')
           element.click()
    ```

6. Redirect to create events form.
    
    Now from event details view next step is to click on `Create Event` button to redirect to the event creation form view.
    ```python
       def test_learn_automated_testing(self):
           # Earlier code...
           element = self.driver.find_element_by_link_text('Create Event')
           element.click()
    ```

7. Fill and submit the event form.
    
    After the form is open next task is to send valid values to the input fields and submit the form. Note that if any invalid value is submitted the form will raise errors.
    ```python
       def test_learn_automted_testing(self):
           # Earlier code...
           # Clear fields for values to be sent.
           self.driver.find_element_by_xpath('//input[@placeholder = "Event Name"]').clear()
           self.driver.find_element_by_xpath('//input[@name = "start_date"]').clear()
           self.driver.find_element_by_xpath('//input[@name = "end_date"]').clear()
           # Send values.
           self.driver.find_element_by_xpath('//input[@placeholder = "Event Name"]').send_keys('event-name')
           self.driver.find_element_by_xpath('//input[@name = "start_date"]').send_keys('2050-08-21')
           self.driver.find_element_by_xpath('//input[@name = "end_date"]').send_keys('2050-08-28')
           # Submit form.
           self.driver.find_element_by_xpath('//form[1]').submit()
    ```

8. Retrieve the details of the event created.
    
    The event is created and the values are visible in the view. Next is to retrieve those values from view.
    ```python
       def test_learn_automated_testing(self):
           # Earlier code...
           event_name = self.driver.find_element_by_xpath('//table//tbody//tr[1]//td[1]').text
           event_start_date = self.driver.find_element_by_xpath('//table//tbody//tr[1]//td[2]').text
           event_end_date = self.driver.find_element_by_xpath('//table//tbody//tr[1]//td[3]').text
    ```

9. Assert the results.
    
    Final step is to assert the results obtained from views against the values sent earlier to form.
    ```python
       def test_learn_automated_testing(self):
           # Earlier code...
           self.assertEqual(event_name, 'event-name')
           self.assertEqual(event_start_date, 'Aug. 21, 2050')
           self.assertEqual(event_end_date, 'Aug. 28, 2050')
    ```

10. Quit the browser session.

    Like initiation this step is also done at class level and only once for a test suite.
    ```python
        @classmethod
        def tearDownClass(cls):
            cls.driver.quit()
            super(LearningAutomatedTesting, cls).tearDownClass()
    ```

After compiling all the above code snippets the test finally will look like:

```python
    from selenium import webdriver
    from django.contrib.staticfiles.testing import LiveServerTestCase
    from django.contrib.auth.models import User
    from administrator.models import Administrator
    
    
    class LearningAutomatedTesting(LiveServerTestCase):
        @classmethod
        def setUpClass(cls):
            cls.driver = webdriver.Firefox()
            cls.driver.implicitly_wait(5)
            cls.driver.maximize_window()
            # Initiate POM pages here
            super(LearningAutomatedTesting, cls).setUpClass()
        
        @classmethod
        def tearDownClass(cls):
            cls.driver.quit()
            super(LearningAutomatedTesting, cls).tearDownClass()
        
        def test_learn_automated_testing(self):
            # Creating administrator
            user_1 = User.objects.create_user(username='admin', password='admin')
            Administrator.objects.create(user=user_1, address='address', city='city',
                                         state='state', country='country', phone_number='9999999999',
                                         email='admin@admin.com', unlisted_organization='organization')
            
            self.get_page(self.live_server_url, '/authentication/login/')
            
            self.send_value_to_element_id('id_login', 'admin')
            self.send_value_to_element_id('id_password', 'admin')
            self.element_by_xpath('//form[1]').submit()
            
            element = self.driver.find_element_by_link_text('Events')
            element.click()
            
            element = self.driver.find_element_by_link_text('Create Event')
            element.click()
            
            # Clear fields for values to be sent.
            self.driver.find_element_by_xpath('//input[@placeholder = "Event Name"]').clear()
            self.driver.find_element_by_xpath('//input[@name = "start_date"]').clear()
            self.driver.find_element_by_xpath('//input[@name = "end_date"]').clear()
            # Send values.
            self.driver.find_element_by_xpath('//input[@placeholder = "Event Name"]').send_keys('event-name')
            self.driver.find_element_by_xpath('//input[@name = "start_date"]').send_keys('2050-08-21')
            self.driver.find_element_by_xpath('//input[@name = "end_date"]').send_keys('2050-08-28')
            # Submit form.
            self.driver.find_element_by_xpath('//form[1]').submit()
            
            event_name = self.driver.find_element_by_xpath('//table//tbody//tr[1]//td[1]').text
            event_start_date = self.driver.find_element_by_xpath('//table//tbody//tr[1]//td[2]').text
            event_end_date = self.driver.find_element_by_xpath('//table//tbody//tr[1]//td[3]').text
            
            self.assertEqual(event_name, 'event-name')
            self.assertEqual(event_start_date, 'Aug. 21, 2050')
            self.assertEqual(event_end_date, 'Aug. 28, 2050')
```


For more information and resources related to automated testing in selenium visit [documentation](https://wiki.saucelabs.com/display/DOCS/Getting+Started+with+Selenium+for+Automated+Website+Testing) of [Sauce Labs]()
