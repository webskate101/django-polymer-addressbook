#! /bin/bash

. "$(dirname "$0")/common.sh"

# Turn off fast-fail so early failing tests don't prevent later tests running
set +e

python manage.py test
npm test
