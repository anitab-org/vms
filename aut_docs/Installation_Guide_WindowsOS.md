## Installation Guide for Windows OS

### Prerequisites

- Download [Python 3.6.5](https://www.python.org/downloads/release/python-365) (Windows x86-64 executable installer version 3.6.5) 
  
  **Note:** Don't forget to check **Add to path** while installing.

- Check the python version 
  ```
  python --version
  ```

- Check if pip (The python package installer) is already installed by running
  ```
  pip --version
  ```
- If installed then upgrade it using the command
  ```
  python -m pip install --upgrade pip
  ```
  **Note:** This will upgrade the pip version

- Install virtual environment
  ```
  pip install virtualenv
  ```
- Download [Git](https://git-scm.com/download/win) 
  
  **Note:** While installing select the option **Use Git and optional Unix Tools from the Windows Command Prompt** for using Git from the command prompt
 
- Clone the VMS project
  ```
  git clone https://github.com/anitab-org/vms
  ```

- Create python3.6 virtual environment
  ```
  virtualenv -p python3.6 venv
  ```
    
### Installing dependencies in the virtualenv

- Activate virtual environment
  ```
  .\venv\Scripts\activate
  ```
  **Note:** If you are using **Git Bash** then you can use the following command to activate the virtual environment
  ```
  source venv/Scripts/activate
  ```
    
- Change directory to VMS code
  ```
  cd vms
  ```

- Install all python dependencies
  ```
  pip install -r requirements.txt
  ```

### Install PostgreSQL

- If you are installing and running the project on your local machine, then you will need to download [PostgreSQL](http://www.postgresql.org/download/) (version >= 9.3.4) and install it (Remember the password that you have entered during the installation process):
  
  **Note:** Add bin & lib to path, Example: C:\Program Files\PostgreSQl\9.5\bin & C:\Program Files\PostgreSQl\9.5\lib

- Download [Firefox](https://www.mozilla.org/en-US/firefox/new/) web browser
  
  **Note:** Use Firefox (version 60)

### Setup PostgreSQL

To start the postgreSQL Server there are 3 ways

- **Command Prompt**
  ```
  pg_ctl -D "C:\Program Files\PostgreSQL\9.5\data" start
  ```
  **Note:** Quotes must include "The path where PostgreSQL\version\data is stored"

- **pgAdmin**
   * Click the Windows Start menu
   * Find PostgreSQL in which you will find pgAdmin 
   * Just open it you will find Servers there
   * Click on the PostgreSQl server, it asks for the password that was entered during the installation, just enter the password
   * Done the Server is connected.

- **Windows Key + R (Run App)**
   * Enter services.msc & click OK
   * Find PostgreSQL it should be in Automatic mode if not the right click & change the mode
   * Start the server by right clicking on PostgreSQL
   
  **Note:** You can use any one of the 3 ways, but the command prompt method takes time

- Run the postgres client
  ```
  psql -U postgres
  ``` 
  **Note:** It will ask you for the same password that you entered during the installation process, Enter the password & done
    
- Create a user called `vmsadmin` with password `0xdeadbeef` with the permissions to be able to create roles, databases and to login with a password. Wherever prompted in the below steps, use the password `0xdeadbeef`.
  ```
  create role vmsadmin with createrole createdb login password '0xdeadbeef';
  ```
- Exit the postgres client using 
  ```
  \q 
  ```

- No changes have to be made to the **pg_hba.conf** file, path (C:\Program Files\PostgreSQL\9.5\data\pg_hba.conf)
    
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
  createdb -U vmsadmin vms
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

- Create a .env file which must be of type **All Files** 
  * Note that you are in the directory vms\vms (you have to create the .env file here)
  * Just copy the contents of .env Example File to your created file
  * Save it.
    
### Setting up the database and starting the server

- Change directory to
  ```
  cd vms\vms
  ```

- Create migrations for the database
  ```
  python manage.py makemigrations auth volunteer administrator organization event job shift registration
  ```
    
- Apply migrations to database
  ```
  python manage.py migrate --noinput --traceback --settings=vms.settings
  ```
    
- Populate the database for django-cities-light
  ```
  python manage.py cities_light
  ```
    
- After running the command
  ```
  python manage.py runserver
  ```
    
- Check that the project is running correctly by browsing to
  [http://127.0.0.1:8000](http://127.0.0.1:8000)

  **Note:** The default web browser is Firefox
    
### Steps to run tests

- Automated tests in VMS require you to setup geckodriver in your path. For that, download [Geckodriver v0.20.0](https://github.com/mozilla/geckodriver/releases)
  
  * Move to Geckodriver v0.20.0
  * Then to Assets
  * Download **geckodriver-v0.20.0-win64.zip** or **geckodriver-v0.20.0-win32.zip** depending on your system
  * After downloading, copy & paste the downloaded geckodriver folder in the venv folder & add to path.

- To execute all tests VMS, use this command
  ```
  python manage.py test -v 2
  ```

- To execute tests in a particular file use
  ```
  python manage.py test <app_name> -v 2 
  ```

- To execute a test file inside an app use
  ```
  python manage.py test <app_name>.tests.<test_file_name> -v 2
  ```

- If all tests pass, `OK` will be received at the end.

- For automated tests, if any of the tests fail its not necessary that there is something wrong. To confirm if the the test is actually wrong you have to test it in headless mode.

  **Note:** For automated testing, currently VMS uses the Firefox version 60, selenium version 3.4.0 and geckodriver version 0.20.1

  **Note:** Some of the test may be failing due to the incorrect permission given to the media folder, If media folder (srv directory) is already created on your system , then make sure it has read, write & execute permission
   
- In case you do not find the directory make one in vms\vms.

- After creating the directory, make sure it has read, write & execute permission, you can check the **Properties** of the directory for checking the permission.

### Stop the PostgreSQl Server

To stop the postgreSQL Server there are 3 ways

- **Command Prompt**
  ```
  pg_ctl -D "C:\Program Files\PostgreSQL\9.5\data" stop
  ```
  **Note:** Quotes must include "The path where PostgreSQL\version\data is stored"

- **pgAdmin**
   * In the pgAdmin when the server is in the **start** status
   * Just right click on the PostgreSQL Server
   * Click Disconnect server
   * The Server has stopped.

- **Windows Key + R (Run App)**
   * Enter services.msc & click OK
   * Stop the server by right clicking on PostgreSQL.
   
  **Note:** You can use any one of the 3 ways, but the command prompt method takes time


