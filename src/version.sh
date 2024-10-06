DATA_DIR = $1

# DVC operations
echo "Starting DVC operations..."

# Add new data to DVC
dvc add data/raw/$DATA_DIR/

# Commit changes to DVC
dvc commit

# Push to remote storage
dvc push

# Git operations (optional, but recommended)
echo "Starting Git operations..."

# Stage DVC file changes
git add data/raw/$DATA_DIR/

# Commit DVC file changes
git commit -m "Update data: $SCRIPT crawler run on $(date)"

# Push Git changes (if you want to push to a Git remote)
git push -u origin master

echo "DVC operations complete!"
