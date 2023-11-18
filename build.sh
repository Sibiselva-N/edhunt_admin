#!/bin/bash

# Navigate to the Django project directory
cd edhunt

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Exit the script
exit 0
