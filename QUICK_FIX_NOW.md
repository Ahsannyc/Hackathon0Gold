# Quick Fix - Do This Right Now

## What Happened

The Playwright browser crashed with error code 21. This usually means Chrome processes are stuck or the session folder is corrupted.

---

## Fix (Pick One Below)

### **FASTEST - Run 3 Commands**

```powershell
# 1. Kill Chrome
taskkill /F /IM chrome.exe

# 2. Delete bad session
rm -r session/facebook

# 3. Run watcher
python watchers/facebook_instagram_watcher.py
```

That's it! Browser should open now.

---

### **AUTOMATIC - Run Script**

Open PowerShell as Administrator and run:

```powershell
.\FIX_PLAYWRIGHT_ERROR.ps1
```

Then:
```powershell
python watchers/facebook_instagram_watcher.py
```

---

### **SAFEST - Use PM2**

```powershell
# 1. Delete session
rm -r session/facebook

# 2. Start with PM2 (more stable)
pm2 start watchers/facebook_instagram_watcher.py --name facebook-instagram-watcher --interpreter python3

# 3. Watch logs
pm2 logs facebook-instagram-watcher
```

---

## What Should Happen Next

When you run the watcher:

1. ✅ A browser window opens
2. ✅ It shows Facebook login page
3. ✅ You manually log in (within 60 seconds)
4. ✅ Logs show: `[OK] AUTHENTICATED - Facebook Messenger detected!`
5. ✅ Watcher starts monitoring: `[CYCLE 1] Checking Facebook Messenger...`

---

## If It Still Fails

1. **Check Task Manager** - Kill any remaining `chrome.exe` processes
2. **Check logs** - `pm2 logs facebook-instagram-watcher`
3. **Reinstall Playwright** - `python -m playwright install chromium`
4. **See detailed guide** - `PLAYWRIGHT_ERROR_FIX.md`

---

## Key Changes Made to Fix It

✅ Added critical browser args: `--no-sandbox`, `--disable-gpu`
✅ Added lock file cleanup on startup
✅ Added retry logic (tries up to 3 times)
✅ Better error messages with solutions
✅ Created automatic cleanup scripts

---

## Test After Fix

Once watcher is running:

1. **Send test message:**
   - Facebook Messenger: "Hi, I have a **sales** opportunity"
   - Or Instagram DM: "Interested in a **client** project"

2. **Check if captured:**
   ```bash
   ls Needs_Action/facebook_*.md
   ```

3. **Run skill:**
   ```bash
   python skills/social_summary_generator.py --process
   ```

4. **Check draft:**
   ```bash
   cat Pending_Approval/facebook_draft_*.md
   ```

---

**Try the 3-command fix now!** 👆
