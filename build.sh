#!/usr/bin/env bash
set -o errexit

# Render creates a .venv via Poetry - install packages into it
if [ -f ".venv/bin/pip" ]; then
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r requirements.txt
else
    pip install --upgrade pip
    pip install -r requirements.txt
fi

python manage.py collectstatic --no-input
python manage.py migrate
