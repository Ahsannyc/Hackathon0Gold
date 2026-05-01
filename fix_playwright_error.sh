#!/bin/bash
# Facebook/Instagram Watcher - Playwright Browser Error Fix
# Run this bash script to fix "Browser has been closed" errors

echo "================================================"
echo "Facebook/Instagram Watcher - Troubleshooting"
echo "================================================"

# Step 1: Kill any existing Chrome processes
echo ""
echo "[STEP 1] Killing existing Chrome/Chromium processes..."
pkill -f chrome 2>/dev/null || true
pkill -f chromium 2>/dev/null || true
echo "[OK] Chrome processes killed"

# Step 2: Delete session folder
echo ""
echo "[STEP 2] Clearing session folder..."
SESSION_PATH="session/facebook"
if [ -d "$SESSION_PATH" ]; then
    rm -rf "$SESSION_PATH"
    echo "[OK] Session folder cleared: $SESSION_PATH"
else
    echo "[INFO] Session folder doesn't exist yet"
fi

# Step 3: Check if Playwright is installed
echo ""
echo "[STEP 3] Verifying Playwright installation..."
PLAYWRIGHT_VERSION=$(python3 -c "import playwright; print(playwright.__version__)" 2>/dev/null)
if [ -n "$PLAYWRIGHT_VERSION" ]; then
    echo "[OK] Playwright is installed: v$PLAYWRIGHT_VERSION"
else
    echo "[WARN] Could not determine Playwright version"
fi

# Step 4: Install Playwright browsers if needed
echo ""
echo "[STEP 4] Installing/reinstalling Playwright browsers..."
python3 -m playwright install chromium
echo "[OK] Playwright browsers installed"

# Step 5: Verify Python and dependencies
echo ""
echo "[STEP 5] Verifying Python dependencies..."
PYTHON_VERSION=$(python3 --version 2>&1)
echo "[OK] $PYTHON_VERSION"

for dep in "playwright" "pyyaml"; do
    python3 -c "import $dep" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "[OK] $dep is installed"
    else
        echo "[WARN] $dep may not be installed"
    fi
done

# Step 6: Clear any lock files
echo ""
echo "[STEP 6] Clearing lock files..."
LOCK_COUNT=$(find session -name "lock" 2>/dev/null | wc -l)
if [ "$LOCK_COUNT" -gt 0 ]; then
    find session -name "lock" -delete 2>/dev/null
    echo "[OK] Removed $LOCK_COUNT lock files"
else
    echo "[INFO] No lock files found"
fi

# Final summary
echo ""
echo "================================================"
echo "Cleanup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Run: python3 watchers/facebook_instagram_watcher.py"
echo "2. Browser will open - manually log into Facebook"
echo "3. Complete 2FA if prompted"
echo "4. Watcher will detect auth and start monitoring"
echo ""
echo "If you still get errors:"
echo "- Check for remaining chrome processes: ps aux | grep chrome"
echo "- Kill them: pkill -f chrome"
echo "- Try: rm -rf session/facebook"
echo "- Try: pm2 start watchers/facebook_instagram_watcher.py --name facebook-instagram-watcher --interpreter python3"
echo ""
