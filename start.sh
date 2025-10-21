#!/bin/bash
# Startup script for Blood Sugar Monitor Web Application

echo "Starting Blood Sugar Monitor..."
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed!"
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run the application
echo ""
echo "Starting application on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo "================================"
echo ""

python run.py
