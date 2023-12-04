#!/bin/bash

# Delete the "workshop" folder if it exists
if [ -d "workshop" ]; then
    echo "Deleting existing 'workshop' folder..."
    rm -rf workshop
    echo "Deleted 'workshop' folder successfully."
fi

# Create and activate a virtual environment named "workshop"
echo "Creating and activating virtual environment..."
python3 -m venv --prompt=workshop workshop
source workshop/bin/activate

# Verify that the correct Python version is activated
python3 --version

# Install dependencies from requirements.txt
if [ -f requirements.txt ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    echo "Dependencies installed successfully."
else
    echo "Error: requirements.txt file not found."
fi

# Deactivate virtual environment
deactivate
echo "Deactivated virtual environment... Activate it again with 'source workshop/bin/activate'"

echo "Script completed."
