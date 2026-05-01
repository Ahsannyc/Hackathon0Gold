# Facebook/Instagram Watcher - Playwright Browser Error Fix
# Run this PowerShell script to fix "Browser has been closed" errors

Write-Host "================================================"
Write-Host "Facebook/Instagram Watcher - Troubleshooting"
Write-Host "================================================"

# Step 1: Kill any existing Chrome processes
Write-Host ""
Write-Host "[STEP 1] Killing existing Chrome/Chromium processes..."
try {
    Get-Process | Where-Object { $_.ProcessName -like "*chrome*" -or $_.ProcessName -like "*chromium*" } | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Chrome processes killed"
} catch {
    Write-Host "[INFO] No Chrome processes found (or already closed)"
}

# Step 2: Kill any Playwright-related processes
Write-Host ""
Write-Host "[STEP 2] Killing Playwright browser processes..."
try {
    taskkill /F /IM chrome.exe 2>$null
    taskkill /F /IM firefox.exe 2>$null
    taskkill /F /IM msedgedriver.exe 2>$null
    Write-Host "[OK] Playwright processes killed"
} catch {
    Write-Host "[INFO] No Playwright processes found"
}

# Step 3: Delete session folder
Write-Host ""
Write-Host "[STEP 3] Clearing session folder..."
$sessionPath = "session/facebook"
if (Test-Path $sessionPath) {
    try {
        Remove-Item -Path $sessionPath -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "[OK] Session folder cleared: $sessionPath"
    } catch {
        Write-Host "[WARN] Could not delete session folder - may need manual cleanup"
    }
} else {
    Write-Host "[INFO] Session folder doesn't exist yet"
}

# Step 4: Check if Playwright is installed
Write-Host ""
Write-Host "[STEP 4] Verifying Playwright installation..."
try {
    $playwrightVersion = python -c "import playwright; print(playwright.__version__)" 2>$null
    if ($playwrightVersion) {
        Write-Host "[OK] Playwright is installed: v$playwrightVersion"
    } else {
        Write-Host "[WARN] Could not determine Playwright version"
    }
} catch {
    Write-Host "[WARN] Playwright may not be properly installed"
}

# Step 5: Install Playwright browsers if needed
Write-Host ""
Write-Host "[STEP 5] Installing/reinstalling Playwright browsers..."
try {
    python -m playwright install chromium 2>&1 | Write-Host
    Write-Host "[OK] Playwright browsers installed"
} catch {
    Write-Host "[WARN] Could not install Playwright browsers"
}

# Step 6: Verify temp directories
Write-Host ""
Write-Host "[STEP 6] Checking temp directories..."
$tempDir = "$env:APPDATA\Local\ms-playwright"
if (Test-Path $tempDir) {
    Write-Host "[OK] Playwright cache exists: $tempDir"
    $cacheSize = (Get-ChildItem $tempDir -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "[INFO] Cache size: $([math]::Round($cacheSize, 2)) MB"
} else {
    Write-Host "[INFO] Playwright cache directory will be created on first run"
}

# Step 7: Clear any lock files
Write-Host ""
Write-Host "[STEP 7] Clearing lock files..."
$lockFiles = Get-ChildItem -Path "session" -Recurse -Filter "lock" -ErrorAction SilentlyContinue
if ($lockFiles) {
    $lockFiles | Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Removed $($lockFiles.Count) lock files"
} else {
    Write-Host "[INFO] No lock files found"
}

# Step 8: Verify Python and dependencies
Write-Host ""
Write-Host "[STEP 8] Verifying Python dependencies..."
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] $pythonVersion"

    $deps = @("playwright", "pyyaml")
    foreach ($dep in $deps) {
        python -c "import $dep" 2>$null
        if ($?) {
            Write-Host "[OK] $dep is installed"
        } else {
            Write-Host "[WARN] $dep may not be installed"
        }
    }
} catch {
    Write-Host "[ERROR] Python not found or not in PATH"
}

# Final summary
Write-Host ""
Write-Host "================================================"
Write-Host "Cleanup Complete!"
Write-Host "================================================"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Run: python watchers/facebook_instagram_watcher.py"
Write-Host "2. Browser will open - manually log into Facebook"
Write-Host "3. Complete 2FA if prompted"
Write-Host "4. Watcher will detect auth and start monitoring"
Write-Host ""
Write-Host "If you still get errors:"
Write-Host "- Check Task Manager for any remaining chrome.exe processes"
Write-Host "- Try: rm -r session/facebook"
Write-Host "- Try: pm2 start watchers/facebook_instagram_watcher.py --name facebook-instagram-watcher --interpreter python3"
Write-Host ""
