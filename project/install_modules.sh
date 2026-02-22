#!/usr/bin/env bash
set -e

# Variables
VENV=".venv"
MINILIBX_DIR="modules/minilibx"
MAZEGEN_DIR="modules/mazegen"
MAZEGEN="mazegen-1.0.tar.gz"
TARGET_WHEEL="mlx-2.2-py3-none-manylinux1_x86_64.whl"
TARGET_WHEEL_PATH="$MINILIBX_DIR/$TARGET_WHEEL"

# 1. Create virtual environment if missing
if [ ! -d "$VENV" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV"
fi

# 2. Identify and rename wheel
CURRENT_WHEEL=$(ls $MINILIBX_DIR/mlx-*.whl | head -n 1)

if [ -z "$CURRENT_WHEEL" ]; then
    echo "ERROR: No .whl file found in $MINILIBX_DIR"
    exit 1
fi

if [ "$CURRENT_WHEEL" != "$TARGET_WHEEL_PATH" ]; then
    echo "Renaming $(basename "$CURRENT_WHEEL") to $TARGET_WHEEL"
    cp "$CURRENT_WHEEL" "$TARGET_WHEEL_PATH"
fi

# 3. Install MiniLibX wheel
echo "Installing Python MiniLibX wrapper..."
"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install "$TARGET_WHEEL_PATH"

# 4. Verify installation
echo "Verifying MiniLibX installation..."
if "$VENV/bin/python" -c 'import mlx; m = mlx.Mlx(); print("Success:", m)'; then
    echo "MiniLibX installation verified."
else
    echo "ERROR: MiniLibX installation failed."
    exit 1
fi

echo "MiniLibX setup complete!"

echo "Installing Mazegen lib..."
if test -f $MAZEGEN
    echo $PWD
    cp  $MAZEGEN $PWD/modules/$MAZEGEN
    tar -xvf $PWD/modules/$MAZEGEN -C $PWD/modules
    mkdir $MAZEGEN_DIR
    "$VENV/bin/python" -m pip install -e "$MAZEGEN_DIR"
fi

# 4. Verify installation
echo "Verifying Mazegen installation..."
if "$VENV/bin/python" -c 'import mazegen; m = mazegen.__file__; print("Success:", m)'; then
    echo "Mazegen installation verified."
else
    echo "ERROR: Mazegen installation failed."
    exit 1
fi

echo "You can now install the project in editable mode via the Makefile."
