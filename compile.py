#!/usr/bin/env python3
"""
Compile Python files to bytecode (.pyc) for basic obfuscation
This works on all Python versions without external dependencies
"""

import py_compile
import os
import shutil
import sys

def compile_file(filepath):
    """Compile a single Python file to .pyc"""
    try:
        py_compile.compile(filepath, cfile=filepath + 'c', doraise=True)
        print(f"  ✓ Compiled: {filepath}")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {filepath} - {e}")
        return False

def main():
    print("=" * 60)
    print("  Compiling Python files to bytecode...")
    print("=" * 60)
    
    # Files to compile
    files = [
        'main.py',
        'src/__init__.py',
        'src/balance_checker.py',
        'src/config.py',
        'src/logger_config.py',
        'src/price_fetcher.py',
        'src/trading_engine.py',
        'src/wallet_manager.py'
    ]
    
    success_count = 0
    for file in files:
        if os.path.exists(file):
            if compile_file(file):
                success_count += 1
        else:
            print(f"  ⚠ Not found: {file}")
    
    print("")
    print(f"✓ Compiled {success_count}/{len(files)} files")
    print("")
    print("Note: Source files (.py) are still readable.")
    print("For full obfuscation, PyArmor requires a paid license.")
    print("")

if __name__ == "__main__":
    main()
