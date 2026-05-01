# Hackathon0Gold - Complete Startup Guide
**Last Updated:** 2026-03-24
**System Status:** ✅ All 5 Watchers Ready

## Overview
This system runs 5 autonomous message watchers 24/7:
1. **Gmail** - Email monitoring (OAuth)
2. **WhatsApp** - Message monitoring (Persistent browser)
3. **LinkedIn** - Post/message monitoring (Persistent browser)
4. **Instagram** - DM monitoring (Persistent browser)
5. **Facebook** - Messenger monitoring (JavaScript extraction)

Messages matching universal keywords are automatically saved to `Needs_Action/` folder.

---

## 🚀 Quick Start (First Time Setup)

### 1. Prerequisites
```bash
# Verify Python 3.13+ installed
python --version

# Verify Node.js/npm installed
node --version
npm --version

# Verify PM2 installed globally
npm install -g pm2
pm2 --version
```

### 2. Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Set Up Session Directories (One-Time)
```bash
# These will be created automatically by watchers
# But you can pre-create them:
mkdir -p session/gmail_session
mkdir -p session/facebook_js_extract
mkdir -p session/facebook_visible
mkdir -p session/whatsapp_session
mkdir -p session/linkedin_session
mkdir -p session/instagram_session
```

### 4. Start All Watchers
```bash
# Option A: Using ecosystem.config.js (RECOMMENDED)
pm2 start ecosystem.config.js

# Option B: Using pm2 resurrect (if configured before)
pm2 resurrect

# Verify they're running
pm2 list
```

### 5. Verify All Watchers Are Running
```bash
pm2 list

# Expected output:
# ✅ gmail-watcher       (ID 1) - online
# ✅ whatsapp-watcher    (ID 2) - online
# ✅ linkedin-watcher    (ID 3) - online
# ✅ instagram-watcher   (ID 4) - online
# ✅ facebook-watcher    (ID 12) - online
```

### 6. Monitor Messages in Real-Time
```bash
# In separate terminal, watch captured messages
python monitor-messages.py

# Or check folder directly
ls -la Needs_Action/
```

---

## 📋 Folder Structure

```
Hackathon0Gold/
├── watchers/                      # All monitoring scripts
│   ├── gmail_watcher.py           ✅ EMAIL monitoring
│   ├── whatsapp_persistent.py     ✅ WHATSAPP monitoring
│   ├── linkedin_persistent.py     ✅ LINKEDIN monitoring
│   ├── instagram_watcher_fixed.py ✅ INSTAGRAM monitoring
│   ├── facebook_watcher_js_extract.py ✅ FACEBOOK monitoring
│   └── logs/                      # Watcher logs
│
├── session/                       # Persistent browser sessions
│   ├── gmail_session/             # Gmail OAuth tokens
│   ├── facebook_js_extract/       # Facebook browser profile
│   ├── whatsapp_session/          # WhatsApp browser state
│   ├── linkedin_session/          # LinkedIn browser state
│   └── instagram_session/         # Instagram browser state
│
├── skills/                        # AI agent skills
│   └── logs/
│
├── Needs_Action/                  # ⭐ AUTO-SAVED MESSAGES HERE
├── Pending_Approval/              # Messages awaiting approval
├── Approved/                      # Approved for action
├── Done/                          # Completed tasks
├── history/                       # Documentation & logs
│   ├── adr/                       # Architecture Decision Records
│   └── prompts/                   # Prompt History Records (PHRs)
│
├── ecosystem.config.js            # ⭐ PM2 Configuration (Master)
├── STARTUP_GUIDE.md               # This file
├── SYSTEM_REQUIREMENTS.md         # Dependencies & setup
├── PROJECT_STRUCTURE.md           # Detailed architecture
└── requirements.txt               # Python dependencies
```

---

## 🔑 Key Files & Their Purpose

| File | Purpose | Managed By |
|------|---------|-----------|
| `ecosystem.config.js` | PM2 process configuration for all 5 watchers | Manual (version controlled) |
| `~/.pm2/dump.pm2` | PM2 runtime state & auto-restart config | PM2 (auto-updated) |
| `requirements.txt` | Python package dependencies | Manual (version controlled) |
| `session/*` | Persistent authentication tokens/cookies | Each watcher |
| `Needs_Action/` | **Auto-captured messages with keywords** | All watchers |
| `watchers/logs/` | Watcher execution logs | PM2 |

---

## 🔄 Daily Operations

### Start System
```bash
# Terminal 1: Start all watchers
pm2 start ecosystem.config.js

# Terminal 2: Monitor messages (optional but recommended)
python monitor-messages.py
```

### Check Status
```bash
# View all processes
pm2 list

# View specific watcher logs
pm2 logs facebook-watcher
pm2 logs gmail-watcher

# View all logs
pm2 logs
```

### Stop System
```bash
# Stop all watchers gracefully
pm2 stop all

# Kill and remove all watchers
pm2 delete all
```

### Check Captured Messages
```bash
# List all captured messages
ls Needs_Action/

# View a specific message
cat Needs_Action/facebook_*.md | head -50

# Monitor in real-time
python monitor-messages.py
```

---

## 🛠️ Configuration

### Universal Keywords (Detected Across All Platforms)
All 5 watchers use these keywords for message capture:
```python
['sales', 'client', 'project', 'urgent', 'invoice', 'payment',
 'deal', 'opportunity', 'partnership', 'lead', 'inquiry']
```
Edit in each watcher's `KEYWORDS` variable to customize.

### Watcher Check Intervals
| Watcher | Check Interval | Browser Type |
|---------|---|---|
| Gmail | 60 seconds | N/A (API) |
| WhatsApp | 90 seconds | Persistent Browser |
| LinkedIn | 90 seconds | Persistent Browser |
| Instagram | 90 seconds | Persistent Browser |
| Facebook | 60 seconds | Undetected Chromedriver |

Edit `CHECK_INTERVAL` in each watcher to adjust.

### Memory Limits
PM2 will restart watchers if they exceed memory limits:
- Gmail: 200 MB (API-based, lighter)
- Others: 300 MB each (browser-based, heavier)

Adjust `max_memory_restart` in `ecosystem.config.js` if needed.

---

## 🔐 Authentication & Sessions

### Gmail (OAuth)
- First time: Opens browser for OAuth login
- Saves token in `session/gmail_session/`
- Auto-refreshes token before expiry
- If token invalid: Delete session folder, watcher will request new login

### WhatsApp, LinkedIn, Instagram, Facebook
- First time: Browser window appears, user logs in manually
- Saves session state in respective `session/*/` folder
- Persists across restarts (no re-login needed)
- If session invalid: Delete session folder, watcher will request new login

---

## ⚠️ Troubleshooting

### Watcher keeps restarting
```bash
# Check logs
pm2 logs <watcher-name>

# Common issues:
# 1. Authentication failed → Delete session folder
# 2. Memory limit exceeded → Increase max_memory_restart
# 3. Browser crash → Check for GPU/display issues
```

### Messages not being captured
```bash
# 1. Check if watcher is running
pm2 list

# 2. Check logs for errors
pm2 logs facebook-watcher --lines 50

# 3. Verify keywords are in message
# Keywords: ['sales', 'client', 'project', 'urgent', 'invoice', 'payment', ...]

# 4. Check if message was saved
ls -la Needs_Action/ | tail -5
```

### Browser authentication issues
```bash
# Delete corrupted session
rm -rf session/facebook_js_extract

# Watcher will prompt for login on next restart
pm2 restart facebook-watcher
```

---

## 📊 Monitoring & Logging

### View Real-Time Logs
```bash
# Tail all logs
pm2 logs

# Tail specific watcher
pm2 logs facebook-watcher --lines 50

# Tail only errors
pm2 logs gmail-watcher --err
```

### Log Locations
```bash
~/.pm2/logs/gmail-watcher-out.log          # Gmail output
~/.pm2/logs/facebook-watcher-error.log     # Facebook errors
watchers/logs/facebook_watcher_js.log      # Facebook detailed log
```

### Monitor Message Capture
```bash
# Real-time message monitoring
python monitor-messages.py

# Or just watch folder
watch -n 5 'ls -la Needs_Action/ | tail -5'
```

---

## 🚨 Emergency Procedures

### Kill All Watchers Immediately
```bash
pm2 kill
```

### Force Restart All Watchers
```bash
pm2 restart all
```

### Reset Everything (Nuclear Option)
```bash
# Stop and delete all processes
pm2 delete all

# Delete all session data (requires re-login)
rm -rf session/*/

# Start fresh
pm2 start ecosystem.config.js
```

---

## ✅ Verification Checklist

- [ ] Python 3.13+ installed
- [ ] All dependencies in requirements.txt installed
- [ ] PM2 installed globally
- [ ] All 5 watcher files present in `watchers/`
- [ ] `ecosystem.config.js` in project root
- [ ] `Needs_Action/` folder exists
- [ ] `session/` folder structure created
- [ ] Can start watchers: `pm2 start ecosystem.config.js`
- [ ] All 5 watchers show as "online" in `pm2 list`
- [ ] Messages appear in `Needs_Action/` when received
- [ ] `monitor-messages.py` works for real-time monitoring

---

## 📞 Support

If a watcher isn't working:

1. **Check if process is online:** `pm2 list`
2. **Check logs:** `pm2 logs <watcher-name> --lines 100`
3. **Delete corrupted session:** `rm -rf session/<watcher>/`
4. **Restart watcher:** `pm2 restart <watcher-name>`
5. **If still failing:** Check `~/.pm2/logs/<watcher>-error.log`

---

## 🔄 Auto-Start on System Reboot

### Windows Task Scheduler Method
A batch file can start PM2 on system boot:

```batch
@echo off
cd C:\Users\14loa\Desktop\IT\GIAIC\Q4 spec kit\Hackathon0Gold
pm2 resurrect
```

Schedule this batch file to run at startup in Windows Task Scheduler.

### PM2 Startup (Linux/Mac Only)
```bash
pm2 startup
pm2 save
```

Windows does not support `pm2 startup` natively.

---

**System is ready for 24/7 autonomous message monitoring!** 🚀
