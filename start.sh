#!/bin/bash

# Start Flask Competitive Programming Platform

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Start the Flask server
echo "Starting Flask server on http://localhost:5000"
python run.py
