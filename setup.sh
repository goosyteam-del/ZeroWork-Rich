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

# Compile to bytecode and remove source
echo ""
echo "🔒 Compiling to bytecode..."
python3 -m compileall -q main.py src/

echo "🗑️  Removing source files..."
rm -f main.py src/*.py

echo "📦 Deploying bytecode..."
python3 << 'PYTHON_SCRIPT'
import os, shutil, glob, sys
py_ver = f"cpython-{sys.version_info.major}{sys.version_info.minor}"
main_pyc = f"__pycache__/main.{py_ver}.pyc"
if os.path.exists(main_pyc):
    shutil.copy2(main_pyc, "main.pyc")
src_cache = "src/__pycache__"
if os.path.exists(src_cache):
    for f in glob.glob(f"{src_cache}/*.pyc"):
        shutil.copy2(f, f"src/{os.path.basename(f).replace(f'.{py_ver}', '')}")
shutil.rmtree("__pycache__", ignore_errors=True)
shutil.rmtree("src/__pycache__", ignore_errors=True)
print("✓ Bytecode ready")
PYTHON_SCRIPT

echo ""
echo "=================================================================="
echo "✅ Setup complete!"
echo "=================================================================="
echo ""
echo "Run: python3 ZeroWorkRich.py"
echo ""

