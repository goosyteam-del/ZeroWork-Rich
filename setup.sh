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

# Install PyArmor and rebuild for current platform
echo ""
echo "Installing PyArmor..."
pip3 install pyarmor

echo ""
echo "Detecting platform and Python version..."
PLATFORM=$(uname -m)
if [ "$PLATFORM" = "x86_64" ]; then
    PLATFORM="linux.x86_64"
elif [ "$PLATFORM" = "aarch64" ]; then
    PLATFORM="linux.aarch64"
else
    PLATFORM="linux.x86_64"
fi

echo "Platform: $PLATFORM"
echo "Python: $(python3 --version)"

echo ""
echo "Rebuilding PyArmor for your system..."
cd "$(dirname "$0")"
pyarmor gen --platform "$PLATFORM" -O . -r main.py src/ 2>/dev/null || pyarmor gen -O . -r main.py src/

if [ $? -eq 0 ]; then
    echo ""
    echo "OK Setup complete"
    echo ""
    echo "Run: python3 main.py"
else
    echo "X Setup failed"
    exit 1
fi
