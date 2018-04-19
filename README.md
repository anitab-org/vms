Systers Portal - VMS project
============================

[![Build Status](https://travis-ci.org/systers/vms.svg?branch=develop)](https://travis-ci.org/systers/vms) [![Coverage Status](https://coveralls.io/repos/github/systers/vms/badge.svg?branch=develop)](https://coveralls.io/github/systers/vms?branch=develop) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)


Systers has many volunteers that offer their skills, time, and commitment to
our vision and projects. The **Volunteer Management System** (VMS) will
be useful for volunteer coordinators, volunteer sign-up, tracking hours, and
reporting.

**This project is under active development.**

VMS is live [here](http://52.8.110.63/).

If you are an Outreachy Applicant, start with reading [this](https://github.com/systers/ossprojects/wiki/Volunteer-Management-System).

Features
--------

The VMS will be developed in phases. The initial implementation will track
volunteers' contact information, enable administrators to track volunteer
hours, and allow reporting of useful information.

The [requirements document](docs/Systers_GSoC14_VMS_Requirements.pdf) gives
additional detail on the project's scope.


Installation
------------

The VMS project uses the [Django](https://www.djangoproject.com/) web
framework and [Python](https://www.python.org/).

To get started, read the [Installation Guide](https://github.com/systers/vms/blob/develop/docs/Installation_Guide.md).

If you face some issues while installing and making VMS up in your local, have a look at issues labelled as [While Setting up VMS](https://github.com/systers/vms/labels/While%20Setting%20up%20VMS).


Run VMS in a Docker Container
-----------------------------

If you wish to view a sneak peek of the Systers VMS, you may use Docker to
preview the VMS.
Note: The following Docker configuration is not intended to be run in
production at the moment. It may be configured to do so in the future.

1. Install [Docker](https://docs.docker.com/installation/).
   Follow the installation steps for your specific operating system:
     * Docker runs natively on a Linux-based system.
     * For Windows and Mac OS X, you should follow instructions for installing
       boot2docker which also installs VirtualBox.
1. Install [docker-compose](http://docs.docker.com/compose/install/).
   Note: fig has been deprecated. Docker-compose replaces fig.
1. Create a new directory on your local system.
1. Enter `git clone git@github.com:systers/vms.git` to clone the Systers
   VMS repository. After the clone is done, change directory (cd) to the
   `vms` directory.
1. Run `docker-compose build`. This pulls the Docker images required to run the
   project and installs the necessary dependencies.
1. Run `docker run -e SECRET_KEY=foobarbaz vms_web`
1. Run `docker-compose run web python vms/manage.py migrate`.
1. Run `docker-compose run web python vms/manage.py cities_light` for downloading and importing data for django-cities-light.
1. *Optional:*
   Run `docker-compose run web python vms/manage.py createsuperuser`
   if you wish to create a superuser to access the admin panel.
1. Run `docker-compose up` to start the webserver for the Django Systers VMS
   project.
1. Systers VMS should be running on port 8000.
     * If you are on Linux, enter `http://0.0.0.0:8000` in your browser.
     * If you are using boot2docker on Windows or Mac OS X, enter
       `http://192.168.59.103:8000/` in your browser. If this IP address
       doesn't work, run `boot2docker ip` from the command line and replace
       the previous IP address in the HTTP request with the IP returned by
       boot2docker.


Contribute
----------

- Issue Tracker: [vms/issues](http://github.com/systers/vms/issues)
- Source Code: [vms](http://github.com/systers/vms/)
- Linking pull request to an issue

  When you create a pull request, use closes #id_of_issue or fixes #id_of_issue. It will link the issue with your pull request. It also
  automatically closes the issue if your pull request gets merged.


Documentation
-------------

User and developer documentation for Systers Portal VMS project is generated
using [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
and available online for convenient reading at
[VMS Website](http://vms.readthedocs.org/).


Google Summer of Code (GSoC) Development
----------------------------------------

We are pleased to participate in the Google Summer of Code and are grateful
for the contributions from our GSoC developers.

* Completed features during GSoC 2016
       * [Development](https://github.com/systers/vms/wiki/GSoC'16---Migrating-VMS-from-Function-based-views-to-Class-based-views)
       * [Testing](https://github.com/systers/vms/wiki/GSOC-16--Work-:-AUT-VMS-%5Bvatsala%5D)
* [Completed features during GSoC 2015](https://docs.google.com/document/d/1bzKjyxWIXeqW45UjhsbM4wtlyNagiyueZTqxhtmD_A0/edit)
* [Completed features during GSoC 2014](https://docs.google.com/document/d/1wIHGmqTbufyGW9nKYt3vV-zZhdJEPfdxaOjegQ9qKEk/edit)


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: systers-dev@systers.org

Communicate
-----------

The best way to connect with the maintainers is through GitHub comments. Feel free to discuss more about an issue by commenting on it or asking questions. We also have Systers Slack channel, you can request an invite [here](http://systers.io/slack-systers-opensource/). If there is something you want to discuss privately with the maintainer and you are being hesitant to discuss it on above mediums, then drop an email. For Systers VMS join #vms on Slack.


License
-------

The project is licensed under the [GNU GENERAL PUBLIC LICENSE](https://github.com/systers/vms/blob/master/LICENSE).



A heartfelt thank you to all wonderful contributors of software, guidance, and
encouragement.
