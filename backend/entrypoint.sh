#!/bin/bash

python manage.py makemigrations --merge --noinput
python manage.py migrate || exit 1
python manage.py collectstatic --noinput || exit 1
cp -r /app/static/. /backend_static/ || exit 1
exec "$@"
