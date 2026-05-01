# Playwright Browser Error - "Target page, context or browser has been closed"

## Problem

You see this error when running the Facebook/Instagram watcher:
```
playwright._impl._errors.TargetClosedError: BrowserType.launch_persistent_context: Target page, context or browser has been closed
Browser logs: [pid=7896] <process did exit: exitCode=21, signal=null>
```

**What it means:** The browser launched but immediately crashed (exit code 21) before the watcher could connect.

---

## Quick Fix (Choose One)

### **Option 1: Run Automatic Cleanup (Recommended)**

**Windows (PowerShell):**
```powershell
# Right-click PowerShell and select "Run as Administrator"
.\FIX_PLAYWRIGHT_ERROR.ps1
```

**Linux/macOS/Git Bash:**
```bash
chmod +x fix_playwright_error.sh
./fix_playwright_error.sh
```

Then retry:
```bash
python watchers/facebook_instagram_watcher.py
```

---

### **Option 2: Manual Cleanup**

Run these commands in order:

```bash
# 1. Kill all Chrome processes
taskkill /F /IM chrome.exe
# (or on Linux/Mac: pkill -f chrome)

# 2. Delete session folder
rm -r session/facebook

# 3. Reinstall Playwright browsers
python -m playwright install chromium

# 4. Try again
python watchers/facebook_instagram_watcher.py
```

---

### **Option 3: Use PM2 Instead of Direct Run**

```bash
# Clean up
rm -r session/facebook

# Start with PM2 (sometimes more stable)
pm2 start watchers/facebook_instagram_watcher.py --name facebook-instagram-watcher --interpreter python3

# Check logs
pm2 logs facebook-instagram-watcher
```

---

## Root Causes

The browser crashes (exit code 21) due to:

1. **Leftover Chrome processes** - Previous runs didn't clean up properly
2. **Session folder corruption** - Bad cookies or cache
3. **Lock files** - Browser thinks it's already running
4. **Playwright version mismatch** - Old/outdated Chromium
5. **Windows permission issues** - Session folder not writable
6. **Antivirus interference** - Windows Defender blocking browser

---

## Detailed Troubleshooting

### Check 1: Kill Chrome Processes

Open Task Manager (`Ctrl+Shift+Esc`) and look for:
- `chrome.exe`
- `msedgedriver.exe`

If found, right-click → End Task

Or use command:
```bash
tasklist | find "chrome"  # Check if running
taskkill /F /IM chrome.exe  # Kill it
```

### Check 2: Delete Session Folder

```bash
# Delete the entire session folder (it will be recreated)
rm -r session/facebook

# Verify it's gone
ls session/  # Should not show "facebook" folder
```

### Check 3: Reinstall Playwright

```bash
# Uninstall and reinstall Playwright
pip uninstall playwright -y
pip install playwright

# Install Chromium browser
python -m playwright install chromium
```

### Check 4: Check Disk Space

Playwright needs ~500MB for browser cache:
```bash
# Windows: Check C:\ drive space
# Linux/Mac: df -h
```

### Check 5: Run with Verbose Logging

```bash
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from watchers.facebook_instagram_watcher import FacebookInstagramWatcher
w = FacebookInstagramWatcher()
w.run()
"
```

### Check 6: Try Headless Mode

Temporarily edit `watchers/facebook_instagram_watcher.py` line 94:
```python
# Change this:
headless=False,

# To this for testing:
headless=True,  # But you won't see the login browser
```

Then run. If it works in headless, there's a display issue.

---

## Updated Code

The watcher has been updated with:

✅ Added browser launch arguments:
- `--no-sandbox`
- `--disable-gpu`
- `--disable-web-resources`
- `--disable-component-update`

✅ Added session cleanup:
- Removes stale lock files on startup
- Better error messages with fixes

✅ Added retry logic:
- Retries browser launch up to 3 times
- 10-second delay between retries
- Better logging of what's happening

---

## Expected Behavior (Correct)

When working correctly, you should see:

```
[SETUP] Launching Chromium with persistent session...
[OK] Browser launched, navigating to Facebook Messenger...
[LOAD] Page loaded, waiting for messenger area...
[OK] AUTHENTICATED - Facebook Messenger detected!
[OK] Starting monitoring loop...
[CYCLE 1] Checking Facebook Messenger...
[CYCLE 1] Checking Instagram DMs...
```

And a browser window should open showing Facebook Messenger.

---

## If Still Failing

1. **Check Python version:**
   ```bash
   python --version  # Should be 3.11+
   ```

2. **Check Playwright installation:**
   ```bash
   python -c "import playwright; print(playwright.__version__)"
   ```

3. **Check if browsers installed:**
   ```bash
   ls %APPDATA%\Local\ms-playwright\  # Windows
   # or
   ls ~/.cache/ms-playwright/  # Linux
   ```

4. **Check file permissions:**
   - Right-click `session/facebook` folder
   - Properties → Security
   - Ensure your user has "Full Control"

5. **Disable antivirus temporarily:**
   - Some antivirus software blocks Chromium
   - Add `python.exe` to whitelist

6. **Try different Python installation:**
   - If using conda/virtualenv, try fresh virtual environment:
   ```bash
   python -m venv playwright_env
   playwright_env\Scripts\activate  # Windows
   source playwright_env/bin/activate  # Linux/Mac
   pip install playwright pyyaml
   python -m playwright install chromium
   python watchers/facebook_instagram_watcher.py
   ```

---

## Escalation

If none of the above works:

1. **Check PM2 ecosystem file:**
   ```bash
   pm2 describe facebook-instagram-watcher
   pm2 logs facebook-instagram-watcher --lines 100
   ```

2. **Check system resources:**
   ```bash
   tasklist /v  # See all processes and memory usage
   ```

3. **Try with other watcher (LinkedIn):**
   ```bash
   python watchers/linkedin_persistent.py
   ```
   If this works, the issue is specific to Facebook/Instagram watcher code.

4. **Update Playwright:**
   ```bash
   pip install --upgrade playwright
   python -m playwright install chromium
   ```

---

## Quick Reference

| Symptom | Fix |
|---------|-----|
| Browser closes immediately | Delete `session/facebook/`, kill chrome processes |
| "Target page has been closed" | Run `FIX_PLAYWRIGHT_ERROR.ps1` |
| Playwright not found | `pip install playwright` |
| Chromium not installed | `python -m playwright install chromium` |
| Permission denied on session | `rm -r session/facebook` |
| Still failing after fixes | Use PM2 instead: `pm2 start ...` |

---

## Files Included

- **`FIX_PLAYWRIGHT_ERROR.ps1`** - PowerShell cleanup script (Windows)
- **`fix_playwright_error.sh`** - Bash cleanup script (Linux/macOS)
- **Updated `watchers/facebook_instagram_watcher.py`** - Better args and retry logic

---

**Still stuck?** Check the logs:
```bash
tail -f watchers/logs/facebook_instagram_watcher.log
pm2 logs facebook-instagram-watcher
```

The logs usually indicate what went wrong.
