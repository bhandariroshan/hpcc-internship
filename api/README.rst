api
===

Behold My Awesome Project!

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

:License: MIT

Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy api

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html


Setup Instructions
------------------------------------------
1.  Update the linux machine using the following (optional if using windows):
     ``sudo apt update``
    
2.  Install Python3 on your machine

3.  Install pip3 on your machine using following command (if it is missing)
     ``sudo apt-get install python3-pip``

4.  Upgrade your pip using following command
     ``sudo python3 -m pip install -u pip``

5.  Install postgres database using the following command 
     ``sudo apt install postgresql postgresql-contrib``

6. Loginto the postges and create database using:
    ``sudo -u postgres `` and ``createdb spotinstances``

7.  Set password for user "postgres" using:
     ``ALTER USER postgres WITH PASSWORD 'admin';``

8. Clone the repository

9. Change directory into api folder.

10.  Install the requirements using the following instructions
      ``python3 -m pip install -r requirements.txt``

11.  Migrate the app using: 
      ``python3 manage.py migrate``

12.  Create super user using the following:
      ``python3 manage.py createsuperuser``

13.  Run the server using the following command
      ``python3 manage.py runserver 0.0.0.0:8080``

Deployment
----------
1. In the server setup using setup instructions
2. Open port 80 using web admin portal
3. Run the following command to run the server
    ``sudo nohup python3 manage.py runserver 0.0.0.0:80 &``
4. Run the cheapest operation on the browser using:
    ``http://<public_ip_address>/price/?operation=cheapest&size=Standard_DS1_v2``
5. Run the average price analysis using the following on the browser
    ``http://<public_ip_address>/price/?operation=average&size=Standard_DS1_v2&region=eastus``
