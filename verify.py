#!/usr/bin/env python3
"""
Quick verification script - Test if code was obfuscated correctly
"""

import os

def check_file_obfuscated(filepath):
    """Check if a Python file is obfuscated (single-line base64)"""
    if not os.path.exists(filepath):
        return False, "File not found"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Obfuscated files should be exactly 1 line
    if len(lines) != 1:
        return False, f"Not obfuscated ({len(lines)} lines)"
    
    # Should start with import base64,zlib,marshal;exec(
    if not lines[0].startswith('import base64,zlib,marshal;exec('):
        return False, "Not in obfuscated format"
    
    # Should be reasonably long (compressed code)
    if len(lines[0]) < 500:
        return False, "Too short to be real obfuscated code"
    
    return True, f"OK ({len(lines[0])} chars)"

print("="*70)
print("VERIFICATION: Check if files are properly obfuscated")
print("="*70)
print()

files_to_check = [
    'main.py',
    'src/__init__.py',
    'src/config.py',
    'src/logger_config.py',
    'src/balance_checker.py',
    'src/wallet_manager.py',
    'src/price_fetcher.py',
    'src/trading_engine.py'
]

all_ok = True
for filepath in files_to_check:
    ok, msg = check_file_obfuscated(filepath)
    status = "✓" if ok else "✗"
    print(f"{status} {filepath:30} {msg}")
    if not ok:
        all_ok = False

print()
print("="*70)
if all_ok:
    print("✅ All files are properly obfuscated!")
    print()
    print("You can now run: python3 ZeroWorkRich.py")
else:
    print("❌ Some files are not obfuscated correctly!")
    print()
    print("Please run: git pull")
    print("Then try again: python3 verify.py")
print("="*70)
