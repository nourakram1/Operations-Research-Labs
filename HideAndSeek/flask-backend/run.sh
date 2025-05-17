#!/bin/bash

# Create virtual environment
# Activate virtual environment

# for linux/wsl
python3 -m venv venv
source venv/bin/activate

# for windows
# python -m venv venv
# venv\Scripts\activate.bat

# Install dependencies
pip install flask numpy jsonschema scipy

# Run Flask app
flask run --port=8080
