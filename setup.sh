#!/bin/bash
# Trading Bot Setup Script (Cython Compiled Version)

echo "=================================================================="
echo "        TRADING BOT - SETUP (COMPILED VERSION)                  "
echo "=================================================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "✗ Python3 not found. Installing..."
    sudo apt update
    sudo apt install python3 python3-pip -y
fi

echo "✓ Python found: $(python3 --version)"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================================="
    echo "✅ Setup complete!"
    echo "=================================================================="
    echo ""
    echo "Run: python3 main.py"
    echo ""
else
    echo "✗ Setup failed"
    exit 1
fi
