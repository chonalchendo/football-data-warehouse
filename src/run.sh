#!/bin/bash

# Set the path to your Python interpreter
PYTHON_PATH=$(which python3)

# Set the path to your project directory
PROJECT_DIR="$HOME/Development/football-app/football-data-warehouse"

# Change to the project directory
cd "$PROJECT_DIR"

if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <script>"
    echo "You entered $# arguments"
    echo "They were $@"
    exit 1
fi

SCRIPT=$1


echo "Running $SCRIPT scraper..."

# Run the scraper
$PYTHON_PATH -m src.extractors.$SCRIPT $2 $3 $4 $5

# Print a message when done
echo "Scraper run complete!"
