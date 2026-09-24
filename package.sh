#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Target mode: "exe" (only executable) or "package" (executable + zip archive)
MODE="${1:-package}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "=========================================================="
echo " Pac-Man 42 - Build & Packaging Script (Mode: $MODE)"
echo "=========================================================="

# 1. Detect PyInstaller executable
if command -v uv >/dev/null 2>&1; then
    echo "[1/4] Using uv to run PyInstaller..."
    PYINSTALLER_BIN="uv run pyinstaller"
elif [ -f ".venv/bin/pyinstaller" ]; then
    echo "[1/4] Using .venv/bin/pyinstaller..."
    PYINSTALLER_BIN=".venv/bin/pyinstaller"
elif command -v pyinstaller >/dev/null 2>&1; then
    echo "[1/4] Using system pyinstaller..."
    PYINSTALLER_BIN="pyinstaller"
else
    echo "Error: PyInstaller not found. Please install dependencies with 'uv sync'." >&2
    exit 1
fi

# 2. Build executable using pac-man.spec
echo "[2/4] Building standalone executable with PyInstaller..."
$PYINSTALLER_BIN --noconfirm --clean pac-man.spec

# 3. Assemble distribution folder (assets, config, instructions)
echo "[3/4] Assembling distribution bundle in dist/pac-man/..."
mkdir -p dist/pac-man

# Ensure assets are directly accessible alongside the executable for double-click
cp -r assets dist/pac-man/
cp config.json dist/pac-man/
cp INSTRUCTIONS.txt dist/pac-man/
chmod +x dist/pac-man/pac-man

echo "-> Standalone executable created successfully at: dist/pac-man/pac-man"
echo "-> You can launch it by double-clicking 'pac-man' or via terminal: ./dist/pac-man/pac-man"

# 4. Packaging archive if requested
if [ "$MODE" = "package" ]; then
    echo "[4/4] Creating distribution archive for Itch.io / Public platform..."
    cd dist
    rm -f pac-man-linux.zip

    if command -v zip >/dev/null 2>&1; then
        zip -r pac-man-linux.zip pac-man
    else
        python3 -c "import shutil; shutil.make_archive('pac-man-linux', 'zip', '.', 'pac-man')"
    fi
    cd "$ROOT_DIR"

    echo "=========================================================="
    echo " Packaging complete!"
    echo " Archive ready for upload: dist/pac-man-linux.zip"
    echo "=========================================================="
else
    echo "=========================================================="
    echo " Build complete (Mode: exe)!"
    echo " Executable ready in: dist/pac-man/"
    echo "=========================================================="
fi