#!/bin/bash

# Use the Python interpreter available in the container's PATH
PYTHON="python"

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
$PYTHON -m src.extractors.$SCRIPT "$@"

echo "Crawler run complete!"

# DVC operations
echo "Starting DVC operations..."

# Add new data to DVC
dvc add data/raw/transfermarkt/

# Commit changes to DVC
dvc commit

# Push to remote storage
dvc push

# Git operations (optional, but recommended)
echo "Starting Git operations..."

# Stage DVC file changes
git add data/raw/transfermarkt/

# Commit DVC file changes
git commit -m "Update data: $SCRIPT crawler run on $(date)"

# Push Git changes (if you want to push to a Git remote)
git push -u origin master

echo "DVC operations complete!"
