#!/bin/bash

# Set the path to your Python interpreter
PYTHON_PATH=$(which python3)

# Set the path to your project directory
PROJECT_DIR="$HOME/Development/football-app/football-data-warehouse"

# Change to the project directory
cd "$PROJECT_DIR"

# Run the scraper
$PYTHON_PATH -m extractors.transfermarkt.extract

# Print a message when done
echo "Scraper run complete!"
