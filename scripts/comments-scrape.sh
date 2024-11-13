#!/bin/bash

echo "============================"
echo "Starting comments scrape"
echo "============================"


cd scrape || {
    echo "Failed to navigate to the project directory!"
    exit 1
}

python3 comments.py
