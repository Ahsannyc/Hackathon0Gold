# 🔧 Facebook & Instagram Watcher Setup

## Status: ✅ Fixed & Running

Both watchers were **crashing on launch** due to persistent context browser issues on Windows.

**✅ FIXED:** Now using headless-only mode - no more crashes!

---

## What's Running Now

| Watcher | Status | Check Interval | Mode |
|---------|--------|---|------|
| **facebook-watcher** | ✅ Online (ID 5) | Every 60 sec | Headless |
| **instagram-watcher** | ✅ Online (ID 6) | Every 60 sec | Headless |

---

## Initial Setup: Facebook Login

The watcher needs your Facebook session saved to authenticate. Do this once:

### Step 1: Run Login Setup
```bash
python setup_facebook_login.py
```

### Step 2: Browser Will Open
- A Chrome browser window will appear
- Navigate to **facebook.com** if not already there
- **LOG IN with your Facebook account**
- Go to your **Messages** inbox
- Verify you can see your conversations

### Step 3: Exit & Save
- Press **Ctrl+C** in the terminal when done
- Session cookies will be saved automatically
- Watcher will now use the saved session

### Step 4: Restart Watcher
```bash
pm2 restart facebook-watcher
```

---

## Initial Setup: Instagram Login

Similar process for Instagram:

### Step 1: Edit Login Script (if needed)
The current setup uses Facebook login. For Instagram-only, you'd need a separate script.

### Step 2: Manual First-Time Setup
For now, log in manually first time:
```bash
# Check Instagram logs
pm2 logs instagram-watcher
```

---

## Keywords Being Monitored

**Both Facebook & Instagram watch for:**
- `sales` - sales opportunities, deals
- `client` - client inquiries, messages
- `project` - project updates, requests
- `urgent` - urgent messages
- `invoice` - billing, payment requests
- `payment` - payment confirmations
- `deal` - deal opportunities
- `inquiry` - customer inquiries

---

## How It Works (Simplified)

```
Every 60 seconds:
  1. Launch Chrome in headless mode (no visible window)
  2. Navigate to messenger.com / instagram.com
  3. Scan for messages containing keywords
  4. Save matching messages to Needs_Action/
  5. Close browser gracefully
  6. Wait 60 seconds, repeat
```

**Why Headless?**
- ✅ More reliable on Windows
- ✅ No UI crashes
- ✅ Faster execution
- ✅ Runs in background silently

---

## Check Messages

```bash
# See all captured messages
ls Needs_Action/

# Count by source
echo "Facebook: $(ls -1 Needs_Action/facebook_* 2>/dev/null | wc -l)"
echo "Instagram: $(ls -1 Needs_Action/instagram_* 2>/dev/null | wc -l)"

# View a message
cat Needs_Action/facebook_*.md | head -30
```

---

## Troubleshooting

### "No messages being captured"
**Likely cause:** Not logged in yet

**Fix:**
```bash
python setup_facebook_login.py  # Do the login setup
pm2 restart facebook-watcher
```

### "Watcher keeps restarting"
Check the logs:
```bash
pm2 logs facebook-watcher
pm2 logs instagram-watcher
```

### "Can't find login script"
Make sure you're in the Hackathon0Gold directory:
```bash
cd "C:\Users\14loa\Desktop\IT\GIAIC\Q4 spec kit\Hackathon0Gold"
python setup_facebook_login.py
```

---

## Testing

Send yourself a test message on Facebook/Instagram with one of the keywords, then check:

```bash
sleep 65  # Wait for next check cycle
ls -lt Needs_Action/ | head -1  # See latest message
```

---

## Current Files

- `facebook_watcher_fixed.py` - Fixed watcher (no crashes!)
- `instagram_watcher_fixed.py` - Fixed Instagram watcher
- `setup_facebook_login.py` - One-time login setup script

---

**Next:** Run the login setup and restart the watchers!
