# Automated Testing for VMS

The QA process is divided as follows:

- Continuous Integration: Used travis to setup CI for VMS Project
- Functional Testing: Used Selenium to write UI tests from an end-users perspective.(black-box tests)
- Unit Testing: Unit-tests have been written for services in the codebase.(white-box tests)

## Few important points regarding CI:

- `.travis.yml` is the config file to run the travis build
- Build can be viewed at `https://travis-ci.org/systers/vms`
- Status would be reflected in the badge in `README.md`

## Few important points regarding Functional Testing:

- Selenium, a browser automation tool is used to simulate the functionality.
  python APIs for selenium are used in the tests.

- Django provides a class `LiveServerTestCase`. What this does is that, It
  setups a Virtual Django Sever in the background which can be used by 
  selenium to run tests.

- So, each testcase Class inherits `LiveServerTestCase`, Contains a `setUp`
  and `tearDown` method to instantiate and end live-server respectively.
  Each testcase in the class begins with `test`.

- Each Test Class covers a view. Class name represents the name of the view
  in nav-bar. Test suite for a view is contained in `tests` folder of the app
  containing the view. For Ex: `Volunteer Search` tab in the nav-bar of an
  admin user redirects to `http://127.0.0.1:8000/volunteer/search/`, so 
  the corresponding tests for this view would be in `VolunteerSearch` class
  in `tests` folder of `volunteer` app.

- Each app contains a `tests` folder containing the unit-tests and functional
  tests and an `__init__.py` to let django consider it as a package.

## Few important points regarding design pattern for Selenium tests:

- The tests follow the page object model design. Pages in vms have been broken into 
  objects which model their behaviour. The `pom` folder contains the architecture setup
  for this design.

- Each test file interacts with respective page objects and reuses their methods.
  To locate elements on the page both pages and tests use static locators defined in 
  `pom/locators` folder. `pom/pages` folder contains the pages mapping to vms.

- To follow up changes in UI with changes in tests, the modifications need to be made only
  in the relevant locators/urls/page file.

- Addition of any new view implies that a pom `page` and `locator` need to be created.

- Similarly, modifying any view implies that the corresponding `page` and `locator` will
  also need to be modified.
  
## Important points regarding creation of new Test Class:

- As mentioned earlier, each test class corresponds to a view which has a corresponding
  pom page and locator.

- When creating a new test class, first identify the view the class is being created for,
  and create corresponding pom page and locator.
  
- Similarly, if you are modifying the existing templates make sure you update the corresponding
  pom page and locators.

- Each Test Class has `setUpClass` and `tearDownClass` class methods which should initiate and
  quit the WebDriver objects respectively.

- POM page should be linked to the Test Class in the `setUpClass` method itself and WebDriverWait
  if needed in the tests should also be initiated in this method only.

- If in the tests you are logging in as admin or volunteer make sure to `logout` in the `tearDown`
  method of the Test Class.

- Use of implicit waits should always be avoided unless needed in an extreme case and has the
  approval of a maintainer. If wait is needed use explicit waits instead.

- Tests in normal mode might fail if all are executed at once, but if a test is fails in
  `HEADLESS` mode then the test is wrong and should be corrected accordingly.
