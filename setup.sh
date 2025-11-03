#!/bin/bash#!/bin/bash



set -eset -e



echo "=================================================================="echo "=================================================================="

echo "        ZeroWork-Rich - Setup                                    "echo "        ZeroWork-Rich - Setup                                    "

echo "=================================================================="echo "=================================================================="

echo ""echo ""



# Check Python# Check if binary already exists

if ! command -v python3 &> /dev/null; thenif [ -f "ZeroWorkRich" ]; then

    echo "❌ Python3 not found. Installing..."    echo "✓ Binary already built!"

    sudo apt update    echo ""

    sudo apt install python3 python3-pip -y    echo "Run: ./ZeroWorkRich"

fi    exit 0

fi

echo "✓ Python found: $(python3 --version)"

# Check Python

# Install dependenciesif ! command -v python3 &> /dev/null; then

echo ""    echo "❌ Python3 not found. Installing..."

echo "📦 Installing dependencies..."    sudo apt update

pip3 install -r requirements.txt    sudo apt install python3 python3-pip -y

fi

echo ""

echo "=================================================================="echo "✓ Python found: $(python3 --version)"

echo "✅ Setup complete!"

echo "=================================================================="# Install dependencies

echo ""echo ""

echo "Run: python3 ZeroWorkRich.py"echo "📦 Installing dependencies..."

echo ""pip3 install -r requirements.txt


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

