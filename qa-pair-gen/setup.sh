#!/bin/bash

# Check if Python 3.11 is installed
if ! command -v python3.11 &> /dev/null
then
    echo "Python 3.11 could not be found. Please install Python 3.11 and try again."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3.11 -m venv venv
    echo "Created virtual environment."
fi

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip and install setuptools
pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt

echo "Setup complete. Virtual environment is activated and packages are installed."