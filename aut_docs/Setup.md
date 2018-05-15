## Steps to run tests:

- Currently, used `python 2.7`
- Clone project: `git clone https://github.com/systers/vms.git`
- In the root folder of the project, startup a new virtual environment
  `virtualenv -p /usr/bin/python2.7 venv`
- Activate virtualenv, `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- `cd vms`
- To run, `python manage.py runserver`. Browse 
  `http://127.0.0.1:8000`
- Before running tests, make sure to download the latest geckodriver. Unpack and move the binary to `/usr/local/bin`
- To execute tests `python manage.py test`. This will run all selenium tests, unit-tests and
  all functional-tests across all apps. To execute tests of only a particular
  app, run `python manage.py test <app_name>`
- If all tests pass, `OK` will be received at the end.
- For functional tests, a firefox window for each test will open up
  automatically and close after simulation of tests.

Note: The current setup uses one of the latest versions of Selenium. You will run into errors if the this version is incompatible with your firefox version and does not support it. In that case, follow [this](https://support.mozilla.org/en-US/kb/find-what-version-firefox-you-are-using) guide to find out your browser version and accordingly install a Selenium version compatible with it.
