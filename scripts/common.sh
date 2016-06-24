VIRTUALENV_DIR='venv'

# Force shell to fail on any errors.
set -e

function require() {
  type $1 >/dev/null 2>&1 || { echo "$1 required but not found."; exit 1; }
}

require 'pip'
require 'virtualenv'
require 'npm'

if [ ! -d "$VIRTUALENV_DIR" ]; then
  virtualenv venv
fi

. ./venv/bin/activate
