Destiny
=======

The API for the Manifest web app.  Control servers via a web interface using Ansible and Salt.

- django
- celery
- ansible.runner
- python firebase

--------

You will need to set a couple of bash environment variables which are referenced in the settings.py file.  SECRET is for firebase authentication and SECRET_KEY is for django which you cangenerate at the following URL.

export SECRET=XXXXXXXX
export SECRET_KEY=XXXXXXXX

http://www.miniwebtool.com/django-secret-key-generator/

--------

To run:

python ./manage.py celeryd -l info
python manage.py runserver 0.0.0.0:8000

Updates to Come...
