#!/usr/bin/env python3
"""
Full bot test with mock seed phrase
Tests the complete flow without real wallet
"""

import os
import sys

# Set mock mode
os.environ['ENABLE_MOCK_TRADING'] = 'true'
os.environ['LOG_LEVEL'] = 'INFO'

print("="*70)
print("FULL BOT TEST - Mock Mode")
print("="*70)
print()

# Mock seed phrase input
mock_seed = "test wallet seed phrase with twelve words total for testing purpose only"

try:
    # Temporarily replace input
    import builtins
    original_getpass = None
    
    def mock_getpass(prompt=""):
        print(prompt + " [using mock seed]")
        return mock_seed
    
    # Patch getpass
    import getpass as gp_module
    original_getpass = gp_module.getpass
    gp_module.getpass = mock_getpass
    
    print("Starting bot with mock seed phrase...")
    print()
    
    # Import and run main
    import main
    
    print()
    print("="*70)
    print("✅ Bot completed execution successfully!")
    print("="*70)
    
except KeyboardInterrupt:
    print("\n\n⚠️  Test interrupted by user")
    sys.exit(0)
    
except Exception as e:
    print()
    print("="*70)
    print(f"❌ Error during execution: {e}")
    print("="*70)
    import traceback
    traceback.print_exc()
    sys.exit(1)
    
finally:
    # Restore original getpass
    if original_getpass:
        gp_module.getpass = original_getpass
