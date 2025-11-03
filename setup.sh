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
    sudo apt install python3 python3-pip -y
fi

echo "✓ Python found: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Install PyArmor runtime
echo ""
echo "📦 Installing PyArmor..."
pip3 install pyarmor

echo ""
echo "=================================================================="
echo "✅ Setup complete!"
echo "=================================================================="
echo ""
echo "Run: python3 ZeroWorkRich.py"
echo ""
