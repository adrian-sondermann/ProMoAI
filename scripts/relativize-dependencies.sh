#!/bin/bash

# Define the base directory where ProMoAI folder is located
BASE_DIR=$(pwd)

# Path to your pyproject.toml
PYPROJECT_TOML="pyproject.toml"

# Check if the file exists
if [ ! -f "$PYPROJECT_TOML" ]; then
  echo "File pyproject.toml not found!"
  exit 1
fi

# Use sed to replace the absolute path with relative paths
sed -i -E "s|file://$BASE_DIR/|./|g" "$PYPROJECT_TOML"

echo "Absolute paths have been replaced with relative paths."

# Only for the first time you have to run:  chmod +x scripts/relativize-dependencies.sh
# Run with:  scripts/relativize-dependencies.sh
