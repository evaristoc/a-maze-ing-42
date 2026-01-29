#!/usr/bin/env bash
set -e # Exit immediately if a command fails

VENV=".venv"
MLX_WHEEL="./external/mlx-2.2-py3-ubuntu-any.whl"

# 1. Environment Creation
if [ ! -d "$VENV" ]; then
    echo "==> Creating virtual environment..."
    python3 -m venv "$VENV"
fi

# 2. Upgrade pip
echo "==> Upgrading pip..."
"$VENV/bin/pip" install --upgrade pip

# 3. Local Wheel Handshake
if [ -f "$MLX_WHEEL" ]; then
    echo "==> Installing local MLX dependency..."
    "$VENV/bin/pip" install "$MLX_WHEEL"
else
    echo "ERROR: $MLX_WHEEL not found. Check the /external folder."
    exit 1
fi

# 4. Project Setup
echo "==> Installing project in editable mode..."
"$VENV/bin/pip" install -e .

# Detection for the user's current shell
CURRENT_SHELL=$(basename "$SHELL")
echo "==> Setup Complete!"
echo "==> To activate, run: source $VENV/bin/activate"