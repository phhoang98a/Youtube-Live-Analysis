#!/bin/bash

echo "============================"
echo "Starting Sentiment Analysis"
echo "============================"


cd process || {
    echo "Failed to navigate to the project directory!"
    exit 1
}

echo "Running sentiment analysis script..."
python3 sentiment-analysis.py

