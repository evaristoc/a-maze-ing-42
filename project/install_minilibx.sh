#!/usr/bin/env bash
set -e

VENV=".venv"
minilibx_DIR="third_party/minilibx"
minilibx_SRC_DIR="${minilibx_DIR}/mlx_CLXV"
# This is the "North Star" path we found earlier
PYTHON_BINDINGS_DIR="$(pwd)/${minilibx_SRC_DIR}/python/src"

# 1. Environment Creation
if [ ! -d "$VENV" ]; then
    echo "==> Creating virtual environment..."
    python3 -m venv "$VENV"
fi

# 2. Ensure third_party exists and Unpack
mkdir -p "third_party"
if [ ! -d "$minilibx_SRC_DIR" ]; then
    echo "==> Unpacking MiniLibX..."
    # Adjusting to your folder structure
    tar -xzf "third_party/minilibx/mlx_CLXV-2.2.tgz" -C third_party/
fi

# 3. Compile C++
echo "==> Compiling C++ library..."
make -C "$minilibx_SRC_DIR"

# 4. Locate site-packages
PYTHON_VERSION=$(python3 -c 'import sys; print(f"python{sys.version_info.major}.{sys.version_info.minor}")')
SITE_PACKAGES="$VENV/lib/$PYTHON_VERSION/site-packages"

# 5. Manual Handshake (Symlinking the .so into the package-to-be)
mkdir -p "$SITE_PACKAGES/mlx"
ln -sf "$(pwd)/${minilibx_CPP_DIR}/libmlx.so" "$SITE_PACKAGES/mlx/libmlx.so"

# 6. Identify and Install Wheel
# This assumes the Makefile in mlx_CLXV generates a .whl in the external dir
minilibx_WHEEL=$(ls $minilibx_DIR/mlx-*.whl | head -n 1)
if [ -z "$minilibx_WHEEL" ]; then
    echo "❌ ERROR: No .whl file found."
    exit 1
fi

GENERIC_minilibx_WHEEL="$minilibx_DIR/mlx-2.2-py3-none-any.whl"
if [ "$minilibx_WHEEL" != "$GENERIC_minilibx_WHEEL" ]; then
    echo "🏷️  Renaming $(basename "$minilibx_WHEEL") to $(basename "$GENERIC_minilibx_WHEEL")"
    mv "$minilibx_WHEEL" "$GENERIC_minilibx_WHEEL"
fi


# 3. Local Wheel Handshake
if [ -f "$GENERIC_minilibx_WHEEL" ]; then
    echo "==>🐍 Installing Python minilibx wrapper..."
    "$VENV/bin/pip" install "$GENERIC_minilibx_WHEEL" --force-reinstall
else
    echo "ERROR: $GENERIC_minilibx_WHEEL not found. Check the /external folder."

# 6. Quiet Test (No '!' to avoid Bash errors)
echo "🧪 Running Test..."
if "$VENV/bin/python3" -c 'import mlx; m = mlx.Mlx(); print("Success: " + str(m))' 2>/dev/null; then
    echo "🏁 Installation verified."
else
    echo "❌ Installation failed."
fi

# 1. Identify the project root (where this script sits)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 2. Force the context to the root before the final step
cd "$PROJECT_ROOT"

echo "📍 Current Directory: $(pwd)"
echo "📦 Installing project in editable mode..."

# 4. Project Setup
echo "==> Installing project in editable mode..."
"$VENV/bin/pip" install -e .

# Detection for the user's current shell
CURRENT_SHELL=$(basename "$SHELL")
echo "==> Setup Complete!"
echo "==> To activate, run: source $VENV/bin/activate"