#!/bin/bash

# Trading Bot Setup Script (Obfuscated Version)

echo "=================================================================="
echo "        TRADING BOT - SETUP (OBFUSCATED)                        "
echo "=================================================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "X Python3 not found. Installing..."
    sudo apt update
    sudo apt install python3 python3-pip -y
fi

echo "OK Python found: $(python3 --version)"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "OK Setup complete"
    echo ""
    echo "Run: python3 main.py"
else
    echo "X Setup failed"
    exit 1
fi
