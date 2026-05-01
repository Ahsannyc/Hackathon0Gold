# Hackathon0Gold - Quick Reference Checklist

**Print this page for easy access!**

---

## ✅ System Verification

```bash
# Verify Python
python --version
# Expected: Python 3.11+

# Verify PM2
pm2 --version
# Expected: 5.0.0+

# Validate complete setup
python validate-setup.py
# Expected: 26+ checks passed
```

---

## 🚀 START SYSTEM

```bash
# Open Terminal and run:
cd "C:\Users\14loa\Desktop\IT\GIAIC\Q4 spec kit\Hackathon0Gold"

# Start all 5 watchers
pm2 start ecosystem.config.js

# Verify online
pm2 list

# Monitor messages (in separate terminal)
python monitor-messages.py
```

---

## 🛑 STOP SYSTEM

```bash
# Stop all watchers
pm2 stop all

# Stop and remove all
pm2 delete all

# Emergency kill
pm2 kill
```

---

## 📊 CHECK STATUS

```bash
# View all processes
pm2 list

# View specific logs
pm2 logs facebook-watcher
pm2 logs gmail-watcher --lines 50

# View all logs
pm2 logs

# Watch in real-time
pm2 logs -f
```

---

## 📬 CHECK MESSAGES

```bash
# List all captured messages
ls -la Needs_Action/

# Count messages
ls Needs_Action/*.md | wc -l

# View latest message
ls -t Needs_Action/*.md | head -1 | xargs cat

# Monitor in real-time
python monitor-messages.py
```

---

## 🔧 COMMON FIXES

**Watcher keeps crashing:**
```bash
pm2 logs <watcher-name> --lines 100
```

**Browser won't login:**
```bash
rm -rf session/facebook_js_extract/
pm2 restart facebook-watcher
# Then manually log in when browser appears
```

**Install missing packages:**
```bash
pip install -r requirements.txt
```

**PM2 not found:**
```bash
npm install -g pm2
```

**Delete all messages (⚠️ careful!):**
```bash
rm Needs_Action/*
```

---

## 📂 FOLDER MAP

| Folder | Purpose |
|--------|---------|
| `watchers/` | All 5 monitoring scripts |
| `session/` | Browser sessions & auth tokens |
| `Needs_Action/` | **AUTO-CAPTURED MESSAGES** |
| `Pending_Approval/` | Awaiting human review |
| `Approved/` | Ready to execute |
| `Done/` | Completed tasks |

---

## 🎯 5 ACTIVE WATCHERS

1. **gmail_watcher.py** - Email (Gmail API)
2. **whatsapp_persistent.py** - Messages (Playwright)
3. **linkedin_persistent.py** - Posts/DMs (Playwright)
4. **instagram_watcher_fixed.py** - DMs (Playwright)
5. **facebook_watcher_js_extract.py** - Messenger (Undetected Chrome + JavaScript)

---

## 🔑 KEYWORDS CAPTURED

```
'sales', 'client', 'project', 'urgent', 'invoice', 'payment',
'deal', 'opportunity', 'partnership', 'lead', 'inquiry'
```

---

## 📚 DOCUMENTATION

| File | Read For |
|------|----------|
| `README.md` | System overview |
| `STARTUP_GUIDE.md` | Detailed startup instructions |
| `SYSTEM_REQUIREMENTS.md` | Installation & setup |
| `PROJECT_STRUCTURE.md` | Architecture & design |
| `FACEBOOK_WATCHER_FIX_SUMMARY.md` | Facebook fix details |
| `ecosystem.config.js` | PM2 configuration |

---

## ⏱️ CHECK INTERVALS

| Platform | Interval |
|----------|----------|
| Gmail | 60 seconds |
| WhatsApp | 90 seconds |
| LinkedIn | 90 seconds |
| Instagram | 90 seconds |
| Facebook | 60 seconds |

---

## 💾 MEMORY LIMITS

Each watcher restarts if it exceeds:
- Gmail: 200 MB
- Others: 300 MB each

Edit `ecosystem.config.js` to change.

---

## 🔐 FIRST-TIME AUTHENTICATION

**First run requires login for each platform:**

- **Gmail:** OAuth pop-up (browser)
- **WhatsApp:** Scan QR code with phone
- **LinkedIn:** Login manually in browser
- **Instagram:** Login manually in browser (may need code)
- **Facebook:** Login manually in browser

Sessions persist after first login (no re-login on restart).

---

## 🆘 EMERGENCY PROCEDURES

**System won't start:**
```bash
pm2 kill
pm2 start ecosystem.config.js
```

**Browser crashed:**
```bash
pm2 restart <watcher-name>
```

**Out of memory:**
```bash
pm2 delete all
rm -rf session/*/
pm2 start ecosystem.config.js
```

**Complete reset:**
```bash
pm2 delete all
rm -rf session/*/
rm -rf Needs_Action/*
rm -rf ~/.pm2/*
npm install -g pm2
pm2 start ecosystem.config.js
```

---

## 🎮 DAILY OPERATIONS

### Morning
```bash
pm2 list                    # Check all 5 online
python monitor-messages.py  # Watch new messages
```

### Review Captured Messages
```bash
ls Needs_Action/            # See new messages
cat Needs_Action/facebook_*.md | head -30
```

### Process Messages
```bash
# Move processed messages
mv Needs_Action/facebook_*.md Pending_Approval/
# Or delete if not needed
rm Needs_Action/facebook_*.md
```

### Evening
```bash
pm2 logs --lines 100        # Check for errors
pm2 list                    # Verify all online
```

---

## 📊 EXAMPLE WORKFLOW

```
1. User receives Facebook message: "urgent invoice due"
   ↓
2. facebook-watcher captures (60 second check)
   ↓
3. Message saved to: Needs_Action/facebook_20260324T06560_8892709d_message.md
   ↓
4. You see it: python monitor-messages.py
   ↓
5. Review & process: Move to Pending_Approval/
   ↓
6. Approve & execute: Move to Approved/
   ↓
7. Done: Move to Done/
```

---

## 🔗 USEFUL COMMANDS

```bash
# Restart single watcher
pm2 restart facebook-watcher

# Stop single watcher
pm2 stop facebook-watcher

# View watcher details
pm2 desc facebook-watcher

# Clear logs
pm2 flush

# Save configuration
pm2 save

# Resurrect saved config
pm2 resurrect

# View process memory
pm2 monit

# Export as JSON
pm2 jlist > processes.json
```

---

## 🌐 EXTERNAL RESOURCES

- **Playwright:** https://playwright.dev/python/
- **PM2:** https://pm2.keymetrics.io/
- **Gmail API:** https://developers.google.com/gmail
- **GitHub:** https://github.com/

---

## ✅ FINAL CHECKLIST

- [ ] All 5 watcher files exist
- [ ] ecosystem.config.js exists
- [ ] requirements.txt installed (`pip install -r requirements.txt`)
- [ ] PM2 installed globally (`npm install -g pm2`)
- [ ] Validation passes (`python validate-setup.py`)
- [ ] Can start watchers (`pm2 start ecosystem.config.js`)
- [ ] All 5 show as "online" in `pm2 list`
- [ ] Messages appear in `Needs_Action/` folder

---

**System Ready for 24/7 Operation!** 🚀

Keep this page handy for quick reference during daily operations.
