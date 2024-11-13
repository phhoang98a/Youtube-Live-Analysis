#!/bin/bash

echo "============================"
echo "Starting video scrape"
echo "============================"


cd scrape || {
    echo "Failed to navigate to the project directory!"
    exit 1
}

python3 video.py
