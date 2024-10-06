#!/bin/bash

# Set the path to your Python interpreter
PYTHON_PATH=$(which python3)

# Set the path to your project directory
PROJECT_DIR="$HOME/Development/football-app/football-data-warehouse"

# Change to the project directory
cd "$PROJECT_DIR"

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <script> [additional arguments...]"
    echo "You entered $# arguments"
    echo "They were $@"
    exit 1
fi

SCRIPT=$1
shift  # Remove the first argument from the argument list

echo "Running $SCRIPT crawler..."

# Run the scraper with remaining arguments
$PYTHON_PATH -m src.extractors.$SCRIPT "$@"

# Print a message when done
echo "Crawler run complete!"
