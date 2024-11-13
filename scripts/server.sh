#!/bin/bash

echo "============================"
echo "Starting Go Server"
echo "============================"

echo "Navigating to server directory..."
cd server || {
    echo "Directory 'server' not found!"
    exit 1
}

echo "Running Go server on port 3000..."
go run main.go
