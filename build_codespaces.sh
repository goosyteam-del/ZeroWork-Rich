#!/bin/bash
# Build script for GitHub Codespaces
# Run this after uploading source files

echo "🔧 Building PyArmor on Linux..."
echo ""

# Install PyArmor
echo "📦 Installing PyArmor..."
pip3 install pyarmor==9.2.0 --break-system-packages

# Verify source files
if [ ! -f "main_source.py" ]; then
    echo "❌ Error: main_source.py not found!"
    echo "Please upload source files first:"
    echo "  - main_source.py"
    echo "  - src_source/"
    exit 1
fi

# Clean old obfuscated files
echo ""
echo "🧹 Cleaning old files..."
rm -rf main.py src/ pyarmor_runtime_000000/

# Copy source to build
echo "📋 Preparing source files..."
cp main_source.py main.py
cp -r src_source src

# Build with PyArmor
echo ""
echo "🔒 Obfuscating with PyArmor..."
pyarmor gen -O . -r --platform linux.x86_64 main.py src/

# Verify
if [ -f "pyarmor_runtime_000000/pyarmor_runtime.so" ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "Generated files:"
    ls -lh pyarmor_runtime_000000/pyarmor_runtime.so
    file pyarmor_runtime_000000/pyarmor_runtime.so
    echo ""
    echo "📤 Ready to commit and push:"
    echo "  git add main.py src/ pyarmor_runtime_000000/"
    echo "  git commit -m 'build: PyArmor Linux build'"
    echo "  git push"
else
    echo "❌ Build failed!"
    exit 1
fi
