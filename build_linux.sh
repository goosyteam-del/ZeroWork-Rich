#!/bin/bash

# ZeroWork-Rich - Linux Build Script
# This script must be run on Linux to generate platform-specific PyArmor runtime

set -e

echo "=================================================================="
echo "        ZeroWork-Rich - Building for Linux                       "
echo "=================================================================="
echo ""

# Check if source files exist
if [ ! -f "main_source.py" ]; then
    echo "❌ Error: Source files not found!"
    echo "This script requires original source files to build."
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.9+"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Install PyArmor
echo ""
echo "📦 Installing PyArmor..."
pip3 install pyarmor

# Clean old files
echo ""
echo "🧹 Cleaning old obfuscated files..."
rm -f main.py
rm -rf src/*.py 2>/dev/null || true
rm -rf pyarmor_runtime_* 2>/dev/null || true

# Obfuscate
echo ""
echo "🔒 Obfuscating source code for $(uname -m) platform..."
echo ""

# Rename source files to target names temporarily
cp main_source.py main.py
cp -r src_source/ src/

# Obfuscate
pyarmor gen -O . -r main.py src/

# Clean temporary source files
rm -f main_source.py
rm -rf src_source/

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================================="
    echo "✅ Build successful!"
    echo "=================================================================="
    echo ""
    echo "Obfuscated files:"
    echo "  - main.py"
    echo "  - src/*.py"
    echo "  - pyarmor_runtime_000000/"
    echo ""
    echo "To run: python3 ZeroWorkRich.py"
    echo ""
else
    echo ""
    echo "❌ Build failed"
    exit 1
fi
