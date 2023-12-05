#!/bin/bash

# Check if an argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <message>"
    exit 1
fi

# Assign the first argument to a variable
message="$1"

# Call the Python script with the variable
python3 main.py "{\"user_id\": \"1121122\", \"messaged_us\": \"$message\"}"

