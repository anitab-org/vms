## Steps to run tests:

A one-time setup requires the following four steps:

- Install python,
    ```bash
      sudo apt-get install python3.6
    ```

- Install virtual environment
    ```bash
      sudo apt-get install virtualenv
    ```

- Clone the VMS project
    ```bash
      git clone https://github.com/systers/vms.git
    ```

- Create python3.6 virtual environment
    ```bash
      virtualenv -p python3.6 venv
    ```

Following points are needed to start a testing session:

- Activate virtual environment
    ```bash
      source venv/bin/activate
    ```
- Install all python dependencies
    ```bash
      pip install -r requirements.txt
    ```
  
  :Note: If you face any errors, do not open a new issue and ask for help on slack with full error logs.

- Change directory to VMS code
    ```bash
      cd vms/
    ```

- Create migrations for database
    ```bash
      python manage.py makemigrations auth volunteer administrator organization event job shift registration
    ```

- Apply migrations to database
    ```bash
      python manage.py migrate --noinput --traceback --settings=vms.settings
    ```

- Check that the project is running correctly by browsing to
    ```
      http://127.0.0.1:8000
    ```
    after running the command
    ```bash
      python manage.py runserver
    ```

- Automated tests in VMS require you to setup geckodriver in your path. For that, either run this command in root of project:
    ```bash
      bash setup-geckodriver.sh
    ```
    OR run these commands:
    ```bash
      wget https://github.com/mozilla/geckodriver/releases/download/v0.20.1/geckodriver-v0.20.1-linux64.tar.gz
      tar -xzvf geckodriver-v0.20.1-linux64.tar.gz
      sudo mv geckodriver /usr/local/bin
    ```
  :Note: If you are using Windows then see this link to configure geckodriver in your environment https://stackoverflow.com/a/40208762

- To execute all tests VMS, use this command:
    ```bash
      python manage.py test -v 2
    ```

- To execute tests in a particular file use:
    ```bash
      python manage.py test <app_name> -v 2 
    ```

- To execute a test file inside a app use:
    ```bash
      python manage.py test <app_name>.tests.<test_file_name> -v 2
    ```

- For the automated tests, f geckodriver has been configured correctly then during simulation of tests the firefox browser will automatically open up and perform the actions and close at the end of the test.

- If all tests pass, `OK` will be received at the end.

- For automated tests, if any of the tests fail its not necessary that there is something wrong. To confirm if the the test is actually wrong you have to test it in headless mode.

:Note: For automated testing, currently VMS uses the Firefox version 60, selenium version 3.4.0 and geckodriver version 0.20.1
