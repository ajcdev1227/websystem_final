#!/usr/bin/env bash

# === Config ===

PYTHON="python3"
PIP="pip3"

# === Code ===

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR"

echo "Creating venv..."
$PYTHON -m venv env

LIBDIR="$( realpath env/lib/python*/site-packages/ )"

source env/bin/activate

echo "Installing depencencies inside venv..."
$PIP install -r requirements.txt

echo "Symlinking wagtail libraries..."
rm -r "$LIBDIR"/wagtail*
ln -s "$SCRIPT_DIR"/wagtail* "$LIBDIR"

echo "Running migrations..."
$PYTHON manage.py migrate_schemas --shared

echo "Creating seed data..."
$PYTHON manage.py loaddata "$SCRIPT_DIR/seed/multi.json"

echo "=================================================================================="
echo "Packages have been installed through pip, and custom versions have been symlinked."
echo "Run the following to launch an interactive Bash prompt inside the venv:"
echo "$SCRIPT_DIR/venv-prompt-linux.sh"
