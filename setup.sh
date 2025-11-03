#!/bin/bash
set -e

echo "=================================================================="
echo "        ZeroWork-Rich - Setup                                    "
echo "=================================================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "Installing Python3..."
    sudo apt update
    sudo apt install python3 python3-pip -y
fi

echo "Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "=================================================================="
echo "Setup complete!"
echo "=================================================================="
echo ""
echo "Run: python3 ZeroWorkRich.py"