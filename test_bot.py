#!/usr/bin/env python3
"""
Simple test to verify bot runs on Linux/Codespaces
Tests that obfuscated code executes without AttributeError
"""

print("Testing ZeroWork-Rich bot...")
print()

try:
    print("1. Testing main import...")
    import main
    print("   ✓ Main module imported successfully")
    print()
    
    print("2. Testing src modules...")
    from src import config, logger_config, balance_checker, wallet_manager
    print("   ✓ All src modules imported successfully")
    print()
    
    print("3. Checking configurations...")
    print(f"   - Networks: {len(config.NETWORKS)} chains configured")
    print(f"   - Min balance: ${config.MIN_BALANCE_USD}")
    print(f"   - Mock trading: {config.ENABLE_MOCK_TRADING}")
    print()
    
    print("="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70)
    print()
    print("The bot is properly configured and ready to run.")
    print()
    print("To start the bot:")
    print("  python3 ZeroWorkRich.py")
    print()
    print("Note: The bot will prompt for your 12-word seed phrase.")
    print("      Make sure you have at least $5 in any supported network.")
    print()
    
except AttributeError as e:
    print(f"✗ AttributeError: {e}")
    print()
    print("This error indicates obfuscation issue.")
    print("Please run: git pull")
    print("Then try again.")
    exit(1)
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
