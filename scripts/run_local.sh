#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status


# Pull the latest data
echo "Pulling the latest data from DVC"
dvc pull --force

# Run the Dagster pipeline
echo "Running the Dagster pipeline"
poetry run dagster job execute -m orchestrator.orchestrator -j transfermarkt

# Add and push updated data to DVC
echo "Adding and pushing updated data to DVC"
dvc add data/raw/transfermarkt/
dvc push

# Commit and push .dvc file changes to Git
echo "Committing and pushing .dvc file changes to Git"
git add data/raw/transfermarkt.dvc data/raw/.gitignore
git commit -m "Update transfermarkt data"
git push -u origin master

echo "Dagster pipeline complete"

