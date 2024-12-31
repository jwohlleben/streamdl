#!/bin/bash

# Check if virtual environment was created
if [ ! -d ".env" ]; then
  echo "Virtual environment not found. Please run setup_venv.sh first."
  exit 1
fi

source .env/bin/activate
python3 streamdl.py "$@"
