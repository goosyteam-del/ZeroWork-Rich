#!/usr/bin/env python3
"""
Cython Build Configuration
Compiles Python modules to C extensions (.pyd on Windows, .so on Linux)
"""

from setuptools import setup, Extension
from Cython.Build import cythonize
import sys
import os

# Define modules to compile
modules_to_compile = [
    "main.py",
    "src/balance_checker.py",
    "src/config.py",
    "src/logger_config.py",
    "src/price_fetcher.py",
    "src/trading_engine.py",
    "src/wallet_manager.py",
]

# Create Extension objects
extensions = [
    Extension(
        name=module.replace("/", ".").replace("\\", ".").replace(".py", ""),
        sources=[module],
        language="c"
    )
    for module in modules_to_compile
]

# Compiler directives for optimization and security
compiler_directives = {
    'language_level': "3",           # Python 3
    'embedsignature': False,         # Don't embed signatures (harder to reverse)
    'boundscheck': False,            # Disable bounds checking (faster)
    'wraparound': False,             # Disable negative indexing (faster)
    'initializedcheck': False,       # Disable initialization checks (faster)
    'cdivision': True,               # Use C division (faster)
    'nonecheck': False,              # Disable None checks (faster)
}

# Setup configuration
setup(
    name="ZeroWorkRich",
    ext_modules=cythonize(
        extensions,
        compiler_directives=compiler_directives,
        build_dir="build",
        language_level=3,
    ),
    zip_safe=False,
)
