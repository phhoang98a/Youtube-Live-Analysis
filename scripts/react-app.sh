#!/bin/bash

cd youtube-stream-analysis || {
  echo "Failed to navigate to React project folder. Check the path and try again."
  exit 1
}

if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install
fi

echo "Starting React development server..."
npm start