#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

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

# Remove the manual credential path setting as we're now using environment variables
dvc remote modify --local gcs credentialpath /app/service-account-key.json

# Add new data to DVC
dvc add data/raw/transfermarkt/

# Commit changes to DVC
dvc commit

# Push to remote storage
dvc push

# Git operations
echo "Starting Git operations..."

# Configure Git (in case environment variables weren't set)
if [ -z "$(git config --get user.name)" ]; then
    git config --global user.name "${GIT_AUTHOR_NAME:-Docker User}"
fi
if [ -z "$(git config --get user.email)" ]; then
    git config --global user.email "${GIT_AUTHOR_EMAIL:-docker@example.com}"
fi

# Stage DVC file changes
git add data/raw/transfermarkt.dvc

# Commit DVC file changes
git commit -m "Update data: $SCRIPT crawler run on $(date)"

# Push Git changes (if you want to push to a Git remote)
# Uncomment the next line if you want to automatically push to Git
# git push -u origin master

echo "Pipeline operations complete!"
