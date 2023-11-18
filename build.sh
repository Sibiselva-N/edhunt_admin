#!/bin/bash

# Navigate to the Django project directory
cd edhunt

# Activate the virtual environment (if you're using one)
# source path/to/your/venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Exit the script
exit 0
