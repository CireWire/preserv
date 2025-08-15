#!/bin/bash
# Preserv Archive Integrity Checker - Unix/Linux Launcher
# ======================================================

echo
echo "Preserv - Archive Integrity Checker"
echo "==================================="
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "ERROR: Python 3.8 or higher is required"
    echo "Current version: $python_version"
    exit 1
fi

echo "Python $python_version detected"

# Check if virtual environment exists
if [ -f "venv/bin/activate" ]; then
    echo "Found virtual environment, activating..."
    source venv/bin/activate
else
    echo "No virtual environment found."
    echo "Installing dependencies globally..."
    pip3 install -r requirements.txt
fi

# Run Preserv
echo
echo "Starting Preserv..."
python3 main.py

# Check exit status
if [ $? -ne 0 ]; then
    echo
    echo "Preserv exited with an error."
    exit 1
fi
