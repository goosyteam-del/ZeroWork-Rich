#!/usr/bin/env python3
"""
PyInstaller Build Script for Linux/Codespaces
Builds standalone binary that doesn't expose source code
"""

import PyInstaller.__main__
import os
import sys

# PyInstaller configuration
PyInstaller.__main__.run([
    'ZeroWorkRich.py',
    '--onefile',                    # Single executable file
    '--name=ZeroWorkRich',          # Output binary name
    '--clean',                      # Clean cache
    '--noconfirm',                  # Overwrite without asking
    '--log-level=WARN',             # Less verbose
    
    # Hidden imports (modules not auto-detected)
    '--hidden-import=main',
    '--hidden-import=src.balance_checker',
    '--hidden-import=src.config',
    '--hidden-import=src.logger_config',
    '--hidden-import=src.price_fetcher',
    '--hidden-import=src.trading_engine',
    '--hidden-import=src.wallet_manager',
    '--hidden-import=eth_account',
    '--hidden-import=web3',
    '--hidden-import=mnemonic',
    '--hidden-import=colorlog',
    '--hidden-import=colorama',
    '--hidden-import=requests',
    '--hidden-import=aiohttp',
    '--hidden-import=dotenv',
    
    # Collect all necessary packages
    '--collect-all=eth_account',
    '--collect-all=web3',
    '--collect-all=colorlog',
    
    # Optimization
    '--strip',                      # Strip symbols (smaller size)
    '--optimize=2',                 # Bytecode optimization
])

print("\n✅ Build complete!")
print(f"Binary location: dist/ZeroWorkRich")
