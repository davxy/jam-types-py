#!/usr/bin/env bash
#
# Dependencies:
# - python3
# - python3-pip
# - python3-venv

set -euo pipefail

INSTALLED_PACKAGE_NAME=${INSTALLED_PACKAGE_NAME:-"jam-types"}

PYTHON=python3

# Check if Python is available
if ! command -v $PYTHON &> /dev/null; then
    echo "Error: Python is not installed or not in PATH" >&2
    exit 1
fi

# Set default virtual environment location
if [ -z "${PIP_LOCAL_VENV:-}" ]; then
    PIP_LOCAL_VENV="$HOME/.local/pip"
    echo "Setting default local venv: $PIP_LOCAL_VENV"
fi

env_dir="$PIP_LOCAL_VENV/$INSTALLED_PACKAGE_NAME"

echo "Installing jam-types to $env_dir"

# Create parent directory if it doesn't exist
mkdir -p "$(dirname "$env_dir")"

# Create virtual environment if it doesn't exist
if [ ! -f "$env_dir/bin/activate" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv "$env_dir"
else
    echo "Virtual environment already exists, using existing one..."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$env_dir/bin/activate"

# Install the package
echo "Installing jam-types package..."
pip install .

echo "Installation completed successfully!"
echo "To activate the environment manually, run:"
echo "  source $env_dir/bin/activate"

