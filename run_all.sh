#!/bin/bash

echo "============================"
echo "Starting All Services"
echo "============================"

# Define script paths
REACT_SCRIPT="$(pwd)/scripts/react-app.sh"
SERVER_SCRIPT="$(pwd)/scripts/server.sh"
VIDEO_SCRAPE_SCRIPT="$(pwd)/scripts/video-scrape.sh"
SENTIMENT_ANALYSIS_SCRIPT="$(pwd)/scripts/sentiment-analysis.sh"
COMMENTS_SCRAPE_SCRIPT="$(pwd)/scripts/comments-scrape.sh"

# Display all paths to verify they are correct
echo "Script paths:"
echo "React Script: $REACT_SCRIPT"
echo "Server Script: $SERVER_SCRIPT"
echo "Video Scrape Script: $VIDEO_SCRAPE_SCRIPT"
echo "Sentiment Analysis Script: $SENTIMENT_ANALYSIS_SCRIPT"
echo "Comments Scrape Script: $COMMENTS_SCRAPE_SCRIPT"
echo "============================"

# Function to run a script and check if it succeeded
run_script() {
    local script_path=$1
    local script_name=$2

    # Check if the script exists and is executable
    if [ ! -f "$script_path" ]; then
        echo "Error: $script_name script not found at $script_path"
        exit 1
    elif [ ! -x "$script_path" ]; then
        echo "Error: $script_name script is not executable. Attempting to make it executable..."
        chmod +x "$script_path"
        if [ $? -ne 0 ]; then
            echo "Failed to make $script_name executable. Exiting."
            exit 1
        fi
    fi

    # Run the script in the background
    echo "Running $script_name..."
    "$script_path" &
    if [ $? -ne 0 ]; then
        echo "$script_name failed to execute. Exiting."
        exit 1
    fi
    echo "$script_name started successfully."
}

# Run each script in the background
run_script "$VIDEO_SCRAPE_SCRIPT" "Video Scrape"
run_script "$REACT_SCRIPT" "React"
run_script "$SERVER_SCRIPT" "Go Server"
run_script "$SENTIMENT_ANALYSIS_SCRIPT" "Sentiment Analysis"
run_script "$COMMENTS_SCRAPE_SCRIPT" "Comment Scrape"

# Wait for all background processes to complete
wait

echo "============================"
echo "All Services Started Successfully"
echo "============================"
