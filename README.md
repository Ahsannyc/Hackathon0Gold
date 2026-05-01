# Hackathon0Gold - Multi-Platform Autonomous Message Monitoring System

**Tier:** Gold (5 Platforms)
**Status:** ✅ PRODUCTION READY
**Last Updated:** 2026-03-24
**System Uptime:** 24/7 with auto-restart

---

## 📊 System Overview

Autonomous AI system monitoring **5 communication platforms simultaneously** capturing business-critical messages 24/7.

| Platform | Tech | Status | Check Interval |
|----------|------|--------|---|
| **Gmail** 📧 | API | ✅ Online | 60 seconds |
| **WhatsApp** 💬 | Browser | ✅ Online | 90 seconds |
| **LinkedIn** 💼 | Browser | ✅ Online | 90 seconds |
| **Instagram** 📸 | Browser | ✅ Online | 90 seconds |
| **Facebook** 🔵 | Chrome+JS | ✅ Online (NEW!) | 60 seconds |

**All messages with keywords automatically captured to `Needs_Action/` folder**

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start All Watchers
```bash
cd "C:\Users\14loa\Desktop\IT\GIAIC\Q4 spec kit\Hackathon0Gold"
pm2 start ecosystem.config.js
```

### Step 2: Verify All Online
```bash
pm2 list
# Should show 5 watchers as "online"
```

### Step 3: Monitor Messages
```bash
python monitor-messages.py
# Watch messages arrive in real-time
```

**That's it! System now captures messages 24/7** ✨

---

## 📁 Quick Folder Reference

```
Needs_Action/         ← AUTO-CAPTURED MESSAGES (Process these!)
Pending_Approval/     ← Awaiting human review
Approved/             ← Ready for execution
Done/                 ← Completed tasks
session/              ← Browser sessions & auth tokens
watchers/             ← All 5 monitoring scripts
```

---

## 🎯 Keywords Captured

System captures ANY message containing these 11 business keywords:

```
['sales', 'client', 'project', 'urgent', 'invoice', 'payment',
 'deal', 'opportunity', 'partnership', 'lead', 'inquiry']
```

Example: Facebook Messenger message gets captured → Saved to `Needs_Action/`

---

## 📂 What to Read

**For First-Time Setup:**
1. `SYSTEM_REQUIREMENTS.md` - Install guide
2. `STARTUP_GUIDE.md` - Detailed startup instructions
3. `validate-setup.py` - Verify everything is OK

**For Architecture & Design:**
4. `PROJECT_STRUCTURE.md` - Complete system design
5. `FACEBOOK_WATCHER_FIX_SUMMARY.md` - How Facebook monitoring was fixed

**For Configuration:**
6. `ecosystem.config.js` - PM2 master configuration (5 watchers)
7. `requirements.txt` - Python dependencies

---

## ✅ Pre-Flight Checklist

Before starting, verify:

```bash
# Check Python
python --version
# Expected: 3.11 or higher

# Check PM2
pm2 --version
# Expected: 5.0.0 or higher

# Validate setup
python validate-setup.py
# Expected: 26+ checks passed

# Verify watcher files exist
ls watchers/{gmail,whatsapp,linkedin,instagram,facebook}*.py
# Expected: 5 files found
```

---

## 🎮 Basic Commands

```bash
# Start all 5 watchers
pm2 start ecosystem.config.js

# Check status
pm2 list

# View logs (all watchers)
pm2 logs

# View specific watcher logs
pm2 logs facebook-watcher --lines 50

# Stop all watchers
pm2 stop all

# Restart all watchers
pm2 restart all

# Monitor messages real-time
python monitor-messages.py

# List captured messages
ls -la Needs_Action/

# Count messages
ls Needs_Action/*.md | wc -l
```

---

## 🔧 Customization

### Change Check Interval
Edit each watcher file, find `CHECK_INTERVAL`:
```python
CHECK_INTERVAL = 60  # seconds
```

### Add/Remove Keywords
Edit `KEYWORDS` list in each watcher:
```python
KEYWORDS = ['sales', 'urgent', 'invoice', ...]
```

### Adjust Memory Limit
Edit `ecosystem.config.js`:
```javascript
max_memory_restart: "300M"  // Watchers restart if exceed
```

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | `pip install -r requirements.txt` |
| "Watcher keeps crashing" | `pm2 logs <watcher> --lines 100` |
| "No messages captured" | Check keywords in message; verify `pm2 logs` |
| "Browser won't login" | Delete `session/<platform>/` folder |
| "PM2 not found" | `npm install -g pm2` |
| "Out of memory" | Increase `max_memory_restart` in ecosystem.config.js |

For more help: See `STARTUP_GUIDE.md` troubleshooting section

---

## 📊 Current Status

```
WATCHERS:
  ✅ Gmail Watcher       - 205+ restarts (token refresh)
  ✅ WhatsApp Watcher    - 5 restarts
  ✅ LinkedIn Watcher    - 3 restarts
  ✅ Instagram Watcher   - 3 restarts
  ✅ Facebook Watcher    - 0 restarts (NEW!)

MESSAGES:
  Total Captured: 12+
  Latest:         facebook_20260324T06560_8892709d_message.md

SYSTEM:
  Uptime:         6+ hours
  Memory Usage:   ~1.5 GB total
  Disk Usage:     ~300 MB project + logs
  Check Interval: 60-90 seconds
```

---

## 📋 File Organization

**Essential Configuration:**
- `ecosystem.config.js` ⭐ PM2 master config
- `requirements.txt` ⭐ Python dependencies
- `validate-setup.py` ⭐ Setup verification

**Active Watchers:**
- `watchers/gmail_watcher.py`
- `watchers/whatsapp_persistent.py`
- `watchers/linkedin_persistent.py`
- `watchers/instagram_watcher_fixed.py`
- `watchers/facebook_watcher_js_extract.py` (NEW - JavaScript extraction)

**Documentation:**
- `STARTUP_GUIDE.md` - Complete startup guide
- `SYSTEM_REQUIREMENTS.md` - Installation requirements
- `PROJECT_STRUCTURE.md` - Detailed architecture
- `FACEBOOK_WATCHER_FIX_SUMMARY.md` - Facebook fix details
- `FACEBOOK_FIX_QUICK_STEPS.md` - Quick reference

**Message Folders:**
- `Needs_Action/` - Auto-captured messages
- `Pending_Approval/` - Awaiting human review
- `Approved/` - Ready for execution
- `Done/` - Completed tasks

---

## 🎯 What Happens Next

1. **Watchers capture** message with keywords → `Needs_Action/`
2. **Ralph Loop analyzes** the message (iterative AI processing)
3. **Proposes actions** → Moves to `Pending_Approval/`
4. **You review & approve** → Moves to `Approved/`
5. **Skills execute** → Moves to `Done/`

---

## 🔐 Authentication

Each platform stores session differently:

- **Gmail:** OAuth token in `session/gmail_session/` (auto-refreshed)
- **WhatsApp:** Browser context in `session/whatsapp_session/`
- **LinkedIn:** Browser context in `session/linkedin_session/`
- **Instagram:** Browser context in `session/instagram_session/`
- **Facebook:** Browser profile in `session/facebook_js_extract/`

**First login required** for each platform. Sessions persist on restart (no re-login).

---

## 🌟 Key Features

✅ **5 Platform Monitoring** - Gmail, WhatsApp, LinkedIn, Instagram, Facebook
✅ **24/7 Operation** - Continuous with auto-restart on crash
✅ **Persistent Sessions** - No re-login on restart (except Gmail)
✅ **Keyword Filtering** - 11 business-critical keywords
✅ **Auto-Queue** - Messages saved to `Needs_Action/` automatically
✅ **PM2 Managed** - Process monitoring & auto-restart
✅ **JavaScript Extraction** - Facebook uses smart DOM extraction
✅ **Multi-Browser** - Playwright + Undetected Chrome
✅ **Human-In-Loop** - Approval workflow for actions
✅ **Well Documented** - 6+ comprehensive guides

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Platforms | 5 |
| Check Frequency | 60-90 seconds |
| Memory Usage | ~1.5 GB |
| Disk Space | ~300 MB project |
| Captured Messages | 12+ |
| Uptime | 24/7 with auto-restart |
| Auto-Recovery | Every 60 min (Gmail), 90 min (browsers) |

---

## 🚀 Next Steps

**Choose one:**

### Option A: Start Now
```bash
pm2 start ecosystem.config.js
pm2 list
python monitor-messages.py
```

### Option B: Verify First
```bash
python validate-setup.py
# Then start if all checks pass
pm2 start ecosystem.config.js
```

### Option C: Read Documentation
1. `STARTUP_GUIDE.md` - Detailed guide
2. `SYSTEM_REQUIREMENTS.md` - Setup requirements
3. `PROJECT_STRUCTURE.md` - Architecture details

---

## 📞 Support Resources

- **Playwright Docs:** https://playwright.dev/python/
- **Selenium Docs:** https://www.selenium.dev/
- **PM2 Docs:** https://pm2.keymetrics.io/
- **Gmail API:** https://developers.google.com/gmail

---

## 🎓 Learning the System

**Understand the full system by reading (in order):**
1. This README.md (overview)
2. STARTUP_GUIDE.md (how to start)
3. PROJECT_STRUCTURE.md (architecture)
4. FACEBOOK_WATCHER_FIX_SUMMARY.md (how Facebook fix works)

---

## ✨ System Ready!

**Your autonomous multi-platform message monitoring system is production-ready.**

All 5 watchers are configured, tested, and verified to work.
Messages are being captured automatically.

```bash
# Start monitoring now:
pm2 start ecosystem.config.js
python monitor-messages.py
```

**Enjoy 24/7 autonomous message monitoring!** 🚀

---

*Hackathon0Gold - Gold Tier (5 Platforms)*
*Autonomous AI Employee System*
*Ready for continuous production operation*

**Status: ✅ ALL SYSTEMS GO**
