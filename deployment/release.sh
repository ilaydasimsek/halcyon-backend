#!/bin/sh
python manage.py collectstatic
python manage.py migrate
