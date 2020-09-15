AnitaB.org Portal - VMS project
=============================

[![Build Status](https://img.shields.io/travis/anitab-org/vms/develop?logo=travis)](https://travis-ci.org/anitab-org/vms)
[![Coverage Status](https://coveralls.io/repos/github/anitab-org/vms/badge.svg)](https://coveralls.io/github/anitab-org/vms?branch=develop) 
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com) 
[![project chat](https://img.shields.io/badge/zulip-join_chat-brightgreen.svg?logo=zulip)](https://anitab-org.zulipchat.com/#narrow/stream/222539-vms)
[![Python Version](https://img.shields.io/badge/python-3.6-blue.svg?logo=python)](https://www.python.org/downloads/release/python-360/)

AnitaB.org has many volunteers that offer their skills, time, and commitment to
our vision and projects. The **Volunteer Management System** (VMS) will
be useful for volunteer coordinators, volunteer sign-up, tracking hours, and
reporting.

**This project is under active development.**

VMS is live [here](http://ec2-52-53-177-18.us-west-1.compute.amazonaws.com/en-us/).

If you are an Outreachy Applicant, start with reading [this](https://www.outreachy.org/communities/cfp/systers/).

Features
--------

The VMS is developed in phases. The initial implementation tracks
volunteers' contact information, enables administrators to track volunteer
hours, and allows reporting of useful information.


Installation
------------

The VMS project uses the [Django](https://www.djangoproject.com/) web
framework and [Python](https://www.python.org/).

To get started, read the [Installation Guide](aut_docs/Installation_Setup.md).


Run VMS in a Docker Container
-----------------------------

If you wish to view a sneak peek of the AnitaB.org VMS, you may use Docker to
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
1. Enter `git clone git@github.com:anitab-org/vms.git` to clone the AnitaB.org
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
1. Run `docker-compose up` to start the webserver for the Django AnitaB.org VMS
   project.
1. AnitaB.org VMS should be running on port 8000.
     * If you are on Linux, enter `http://0.0.0.0:8000` in your browser.
     * If you are using boot2docker on Windows or Mac OS X, enter
       `http://192.168.59.103:8000/` in your browser. If this IP address
       doesn't work, run `boot2docker ip` from the command line and replace
       the previous IP address in the HTTP request with the IP returned by
       boot2docker.


Contribute
----------

- Please read our [Contributing guidelines](CONTRIBUTING.md), [Code of Conduct](code_of_conduct.md) and [Reporting Guidelines](reporting_guidelines.md)
- Please follow our [Commit Message Style Guide](https://github.com/anitab-org/mentorship-android/wiki/Commit-Message-Style-Guide) while sending PRs.
- Issue Tracker: [vms/issues](http://github.com/anitab-org/vms/issues)
- Source Code: [vms](http://github.com/anitab-org/vms/)
- Linking pull request to an issue

  When you create a pull request, use closes #id_of_issue or fixes #id_of_issue. It will link the issue with your pull request. It also
  automatically closes the issue if your pull request gets merged.


## Branches

The repository has the following permanent branches:

 * **master** This contains the code which has been released.

 * **develop** This contains the latest code. All the contributing PRs must be sent to this branch. When we want to release the next version of the app, this branch is merged into the `master` branch.

 * **aws** This is the branch through which the project is deployed.


Documentation
-------------

User and developer documentation for AnitaB.org Portal VMS project is generated
using [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
and available online for convenient reading at
[VMS Website](http://vms.readthedocs.org/).


Google Summer of Code (GSoC) Development
----------------------------------------

We are pleased to participate in the Google Summer of Code and are grateful
for the contributions from our GSoC developers.

* [Completed features during GSoC 2018](https://github.com/anitab-org/vms/blob/develop/docs/GSoC18.md)
* Completed features during GSoC 2016
       * [Development](https://github.com/anitab-org/vms/wiki/GSoC'16---Migrating-VMS-from-Function-based-views-to-Class-based-views)
       * [Testing](https://github.com/anitab-org/vms/wiki/GSOC-16--Work-:-AUT-VMS-%5Bvatsala%5D)
* [Completed features during GSoC 2015](https://docs.google.com/document/d/1bzKjyxWIXeqW45UjhsbM4wtlyNagiyueZTqxhtmD_A0/edit)
* [Completed features during GSoC 2014](https://docs.google.com/document/d/1wIHGmqTbufyGW9nKYt3vV-zZhdJEPfdxaOjegQ9qKEk/edit)


Communicate
-----------

The best way to connect with the maintainers is through Github comments. Communicate with our community on [AnitaB.org Open Source Zulip](https://anitab-org.zulipchat.com/). For queries regarding VMS Project join, [#vms](https://anitab-org.zulipchat.com/#narrow/stream/222539-vms) and newcomers can join, [#newcomers](https://anitab-org.zulipchat.com/#narrow/stream/223071-newcomers).



License
-------

The project is licensed under the [GNU GENERAL PUBLIC LICENSE](https://github.com/anitab-org/vms/blob/master/LICENSE).



A heartfelt thank you to all wonderful contributors of software, guidance, and
encouragement.
