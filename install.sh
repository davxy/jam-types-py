#!/usr/bin/env bash

if [ -z "$PIP_LOCAL_VENV" ]; then
    PIP_LOCAL_VENV="$HOME/.local/pip"
fi

env_dir="$PIP_LOCAL_VENV"
echo "Installing jam-types to $env_dir"
python -m venv "$env_dir/jam-types"
source "$env_dir/jam-types/bin/activate"
pip install .

