api
===

Python and Django application to find cheapest region in Azure Spot and find average prirce of a azure instance.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

:License: MIT

Setup Instructions
------------------------------------------
To update the linux machine using the following (optional if using windows):

```
sudo apt update
```

Install Python3 on your machine

Install pip3 on your machine using following command (if it is missing)
 ```
 sudo apt-get install python3-pip
 ```

Upgrade your pip using following command
```
sudo python3 -m pip install -u pip
```

5. Install postgres database using the following command 
```
sudo apt install postgresql postgresql-contrib
```

6. Loginto the postges using:
```
sudo -u postgres
``` 

7. Create database using:
```
createdb spotinstances
```

8. Set password for user "postgres" using:
```
ALTER USER postgres WITH PASSWORD 'admin';
```

9. Clone the repository

10. Change directory into api folder.

11. Install the requirements using the following instructions
```
python3 -m pip install -r requirements.txt
```

12. Migrate the app using: 
```
python3 manage.py migrate
```

13. Create super user using the following:
```
python3 manage.py createsuperuser
```

14.  Run the server using the following command
```
python3 manage.py runserver 0.0.0.0:8080
```

Deployment
----------
1. In the server setup using setup instructions

2. Open port 80 using web admin portal

3. Run the following command to run the server
```
sudo nohup python3 manage.py runserver 0.0.0.0:80 &
```

4. Run the cheapest operation on the browser using:
```
http://<public_ip_address>/price/?operation=cheapest&size=Standard_DS1_v2
```

5. Run the average price analysis using the following on the browser
```
http://<public_ip_address>/price/?operation=average&size=Standard_DS1_v2&region=eastus
```
