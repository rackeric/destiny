Destiny
=======

The API for the Manifest web app.  Control servers via a web interface using Ansible and Salt.

- destiny is a django project
- dcelery was the original (no longer used) django-celery app but ran in to issues with Celery 3.1.11 not allowing daemons to spawn child processes
- destinyCelery is the new app requiring Celery 3.0.24

Requirements:
- django
- celery
- RabbitMQ
- Ansible
- python-firebase

--------

You will need to set a couple of bash environment variables which are referenced in the settings.py file.  SECRET is for firebase authentication and SECRET_KEY is for django which you can generate at the following URL.

export SECRET=XXXXXXXX

export SECRET_KEY=XXXXXXXX

http://www.miniwebtool.com/django-secret-key-generator/

--------

To run:

python ./manage.py celeryd -l info (old using django-celery)

NEW:

celery -A destinyCelery worker --loglevel=info (using stand alone celery)

python manage.py runserver 0.0.0.0:8000

Updates to Come...
