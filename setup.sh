#!/bin/bash

set -e

echo "=================================================================="
echo "        ZeroWork-Rich - Setup                                    "
echo "=================================================================="
echo ""

# Check if binary already exists
if [ -f "ZeroWorkRich" ]; then
    echo "✓ Binary already built!"
    echo ""
    echo "Run: ./ZeroWorkRich"
    exit 0
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Installing..."
    sudo apt update
    sudo apt install python3 python3-pip -y
fi

echo "✓ Python found: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Install PyInstaller
echo ""
echo "📦 Installing PyInstaller..."
pip3 install pyinstaller

# Build binary
echo ""
echo "� Building standalone binary..."
python3 build_binary.py

# Move binary to root
if [ -f "dist/ZeroWorkRich" ]; then
    mv dist/ZeroWorkRich ./
    chmod +x ZeroWorkRich
    
    # Clean up
    rm -rf build/ dist/ *.spec
    
    echo ""
    echo "=================================================================="
    echo "✅ Build complete!"
    echo "=================================================================="
    echo ""
    echo "Run: ./ZeroWorkRich"
else
    echo "❌ Build failed!"
    exit 1
fi

