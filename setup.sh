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

# Install PyArmor
echo ""
echo "📦 Installing PyArmor..."
pip3 install pyarmor

# Clean and rebuild for this platform
echo ""
echo "🔄 Rebuilding for $(uname -m) platform..."
echo ""

# Remove old obfuscated files
rm -f main.py
rm -rf src/*.py 2>/dev/null || true
rm -rf pyarmor_runtime_* 2>/dev/null || true

# Copy source and obfuscate
cp main_source.py main.py
cp -r src_source/ src/

echo "🔒 Obfuscating..."
pyarmor gen -O . -r main.py src/

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================================="
    echo "✅ Setup complete!"
    echo "=================================================================="
    echo ""
    echo "Run: python3 ZeroWorkRich.py"
    echo ""
else
    echo ""
    echo "❌ Setup failed"
    exit 1
fi
