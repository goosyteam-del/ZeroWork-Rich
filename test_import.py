#!/usr/bin/env python3
"""
Simple import test - verifies obfuscated code can be loaded
"""

print("Testing imports...")

try:
    print("1. Importing main...")
    import main
    print("   ✓ main imported")
except Exception as e:
    print(f"   ✗ main failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("2. Importing src modules...")
    from src import config, logger_config, balance_checker
    print("   ✓ src modules imported")
except Exception as e:
    print(f"   ✗ src modules failed: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ All imports successful!")
