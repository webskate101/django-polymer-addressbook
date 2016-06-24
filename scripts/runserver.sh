#! /bin/bash

. "$(dirname "$0")/common.sh"

PORT=8000

python manage.py runserver $PORT
