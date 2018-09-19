#!/bin/bash

set -e

python3 /app/manage.py migrate
python3 /app/manage.py collectstatic --no-input
/usr/local/bin/uwsgi --ini /app/uwsgi.ini
