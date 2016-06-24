#! /bin/bash

. "$(dirname "$0")/common.sh"

pip install -r requirements.txt
npm install

python manage.py migrate
