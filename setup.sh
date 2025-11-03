#!/bin/bash

set -e

echo "=================================================================="
echo "        ZeroWork-Rich - Setup                                    "
echo "=================================================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Installing..."
    sudo apt update
    sudo apt install python3 python3-pip python3-dev -y
fi

echo "✓ Python found: $(python3 --version)"

# Check GCC compiler (required for Cython)
if ! command -v gcc &> /dev/null; then
    echo "📦 Installing build tools..."
    sudo apt update
    sudo apt install build-essential -y
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Install Cython
echo ""
echo "📦 Installing Cython..."
pip3 install Cython

# Compile to C extensions (.so files)
echo ""
echo "🔒 Compiling to C extensions (.so files)..."
python3 cython_setup.py build_ext --inplace

# Remove source files
echo ""
echo "🗑️  Removing source Python files..."
rm -f main.py src/*.py

# Clean up build artifacts
echo "🧹 Cleaning build artifacts..."
rm -rf build/
find . -name "*.c" -delete

echo ""
echo "=================================================================="
echo "✅ Setup complete!"
echo "=================================================================="
echo ""
echo "Run: python3 ZeroWorkRich.py"
echo ""

