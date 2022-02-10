#!/bin/sh
python manage.py migrate
python3 manage.py runserver 0.0.0.0:80
gunicorn 'app.wsgi' -b 0.0.0.0:80 --access-logfile - --log-level info
