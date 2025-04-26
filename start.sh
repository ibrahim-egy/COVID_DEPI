#!/bin/bash

# Ensure we are using pip3 to install the dependencies
# echo "Installing dependencies from requirements.txt..."
# pip3 install --no-cache-dir -r requirements.txt

# Start the Flask app with Gunicorn
echo "Starting Flask app with Gunicorn..."
export PYTHONPATH=.
python3 -m gunicorn src.main:app -w 1 --bind 0.0.0.0:3000 --log-file -
