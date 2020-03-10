## Installation Guide

### A one-time setup:

- Install python
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
  Note: If you face a PATH error, using the full path will address the issue. For Ubuntu, try using:
    ```bash
      virtualenv --python=/usr/bin/python3 venv
    ```
    
### To start a testing session:

- Activate virtual environment
    ```bash
      source venv/bin/activate
    ```
    
- Change directory to VMS code
    ```bash
      cd vms/
    ```
    
- Run the following commands
    ```bash
      sudo apt-get install libpq-dev
      sudo apt install python-dev
      sudo apt install python3-dev
    ```
    
- Install all python dependencies
    ```bash
      pip install -r requirements.txt
    ```
    
  Note: If you face any errors, do not open a new issue and ask for help on slack with full error logs.

### Install Postgresql

- Run the command
    ```bash
      sudo apt install postgresql postgresql-contrib
    ```
    
### Setup PostgreSQL

- Run the postgres client as root
    ```bash
      sudo -u postgres psql
    ```
    Note: In case you get an error `postgres: invalid argument: "psql"`, then run the command
    ```bash
      sudo -u <insert postgres username here> psql
    ```
    
- Create a user called `vmsadmin` with password `0xdeadbeef` with the permissions to be able to create roles, databases and to login with a password. Wherever prompted in the below steps, use the password `0xdeadbeef`.
    ```
        create role vmsadmin with createrole createdb login password '0xdeadbeef';
    ```
- Exit the postgres client using 
    ```
        \q
    ```        

- Change the **pg_hba.conf** file to indicate that users will be authenticated by md5 as opposed to peer authentication. To do this open the **pg_hba.conf** file by running the command
    ```bash
      sudo nano /etc/postgresql/11/main/pg_hba.conf
    ```
    
    Note: In case you find a file not found error or an empty file, then the postgresql installation has probably taken place in a different directory. Find the file using the following command
    ```bash
      sudo find / -type f -iname pg_hba\.conf
     ```
     
    and open the pg_hba.conf file using this path after "sudo nano ".

- Change the line `local all postgres peer` to `local all postgres md5` and the line `local all all peer` to `local all all md5` and save the file.

    Note: In case you dont find the entries, just add the entries as mentioned above.

- Restart the postgresql client
    ```bash
      sudo service postgresql restart
    ```
    
- Login to the postgres client with user `vmsadmin` by running the following command
    ```
        psql -U vmsadmin -d postgres -h localhost -W
    ```
    
- Exit the postgres client using 
    ```
        \q
    ```

- Create a database called `vms`
    ```    
        createdb -U vmsadmin vms;
    ```
    
- Login to the postgres client for the `vms` database
    ```
        psql -U vmsadmin -d vms -h localhost -W
    ```
    
- To view a list of tables for the `vms` database, run this command under the postgres client
    ```
        \dt
    ```        
    We can now manipulate the database by running the appropriate sql commands under this postgres client.

- Exit the postgres client using
    ```
        \q
    ```

- Use the secret_key by running this command
    ```
        export DJANGO_SECRET_KEY='foobarbaz'
    ```
    
### Setting up the database

- Create migrations for the database
    ```bash
      python manage.py makemigrations auth volunteer administrator organization event job shift registration
    ```
    
- Apply migrations to database
    ```bash
      python manage.py migrate --noinput --traceback --settings=vms.settings
    ```
    
- Populate the database for django-cities-light
    ```bash
      python manage.py cities_light
    ```
    
- After running the command
    ```bash
      python manage.py runserver
    ```
    
    Check that the project is running correctly by browsing to
    ```
      http://127.0.0.1:8000
    ```
    
### Steps to run tests

- Automated tests in VMS require you to setup geckodriver in your path. For that, either run this command in root of project
    ```bash
      bash setup-geckodriver.sh
    ```
    
    OR run these commands
    ```bash
      wget https://github.com/mozilla/geckodriver/releases/download/v0.20.1/geckodriver-v0.20.1-linux64.tar.gz
      tar -xzvf geckodriver-v0.20.1-linux64.tar.gz
      sudo mv geckodriver /usr/local/bin
    ```
    Note: If you are using Windows then see this link to configure geckodriver in your environment https://stackoverflow.com/a/40208762

- To execute all tests VMS, use this command
    ```bash
      python manage.py test -v 2
    ```

- To execute tests in a particular file use
    ```bash
      python manage.py test <app_name> -v 2 
    ```

- To execute a test file inside a app use
    ```bash
      python manage.py test <app_name>.tests.<test_file_name> -v 2
    ```

- For the automated tests, if geckodriver has been configured correctly then during simulation of tests the firefox browser will automatically open up and perform the actions and close at the end of the test.

- If all tests pass, `OK` will be received at the end.

- For automated tests, if any of the tests fail its not necessary that there is something wrong. To confirm if the the test is actually wrong you have to test it in headless mode.

    Note: For automated testing, currently VMS uses the Firefox version 60, selenium version 3.4.0 and geckodriver version 0.20.1

    Note : Some of the test may be failing due to the incorrect permission given to the media folder, If media folder(srv directory) is already created on your system , then change its permissions by the following command:
   ```bash
     sudo chmod -R 740 /srv
   ```
- In case you can the error `/srv: No such file or directory` while running the above comment do the following `sudo mkdir /srv`

- After creating the directory, then try to change the permissions i.e., run the following command `sudo chmod 740 /srv`
