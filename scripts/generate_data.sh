#!/bin/bash
# filepath: /c:/Users/User/Documents/ersilia-outreachy/outreachy-contributions/scripts/generate_data.sh

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Construct the path to the Python file relative to this script
PYTHON_FILE="$SCRIPT_DIR/../data/get_tdc_data.py"

# Execute the Python script
python3 "$PYTHON_FILE"