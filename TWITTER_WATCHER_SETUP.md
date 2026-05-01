# Twitter (X) Watcher - Gold Tier Setup & Testing Guide

**Status:** ✅ READY
**Date:** 2026-03-27
**Platform:** 6th Watcher in Gold Tier System
**Version:** 1.0

---

## 📋 Quick Start

### 1. Start Twitter Watcher (Auto with other watchers)
```bash
# Start all 6 watchers (includes Twitter)
pm2 start ecosystem.config.js

# Or start only Twitter watcher
pm2 start watchers/twitter_watcher.py --name twitter-watcher --interpreter python

# Verify it's running
pm2 list
```

### 2. Monitor Twitter Messages (Real-time)
```bash
python monitor-messages.py
```

### 3. Generate Response Drafts
```bash
python skills/twitter_post_generator.py
```

---

## 🔐 First Time Setup

### Step 1: Start Twitter Watcher
```bash
pm2 start ecosystem.config.js
```

### Step 2: Wait for Browser Window
- A visible Chromium browser will appear
- Navigate to https://twitter.com/messages
- **Log in with your Twitter account** when prompted
- Session will be saved to `session/twitter/`

### Step 3: After Login
- Watcher will monitor Twitter DMs automatically
- Checks every 60 seconds
- Messages saved to `Needs_Action/twitter_*.md`

---

## 🧪 Testing Guide

### Test 1: Capture DM with Keywords

**Prerequisites:**
- Twitter watcher running (`pm2 list` shows twitter-watcher online)
- 2 Twitter accounts (yours + class friend's account)

**Steps:**
1. Open separate Twitter account
2. Go to Direct Messages
3. Find your account
4. Send this message:
```
Hi! I have a sales project I'd like to discuss. Can we talk about client needs and payment terms?
```

**Expected Result:**
- Watcher detects: `['sales', 'project', 'client', 'payment']`
- File created: `Needs_Action/twitter_20260327_XXXXXXXX_message.md`
- Contains full message text

**Verify:**
```bash
# Check captured message
ls -la Needs_Action/twitter_*.md

# View the message
cat Needs_Action/twitter_*.md | head -30
```

---

### Test 2: Generate Response Draft

**Steps:**
1. Ensure Test 1 message is captured
2. Run Twitter Post Generator:
```bash
python skills/twitter_post_generator.py
```

**Expected Output:**
```
Messages found:        1
Drafts created:        1
Pending approval:      1
HITL REQUIRED: 1 response(s) awaiting approval
Location: C:\...\Pending_Approval
```

**Verify:**
```bash
# Check draft was created
ls -la Plans/twitter_draft_*.md

# View draft
cat Plans/twitter_draft_*.md

# Check pending approval
ls -la Pending_Approval/twitter_draft_*.md
```

---

### Test 3: Complete HITL Workflow

**Workflow:**
```
Needs_Action/twitter_*.md
        ↓
    [Generator runs]
        ↓
Pending_Approval/twitter_draft_*.md
        ↓
    [You approve]
        ↓
Approved/twitter_draft_*.md
```

**Steps:**
1. Review draft in `Pending_Approval/`:
```bash
cat Pending_Approval/twitter_draft_*.md
```

2. If approved, move to `Approved/`:
```bash
mv Pending_Approval/twitter_draft_*.md Approved/
```

3. If rejected, delete:
```bash
rm Pending_Approval/twitter_draft_*.md
```

---

## 📁 File Locations

| Item | Location |
|------|----------|
| **Watcher Script** | `watchers/twitter_watcher.py` (16 KB) |
| **Post Generator Skill** | `skills/twitter_post_generator.py` (8 KB) |
| **PM2 Config** | `ecosystem.config.js` (includes twitter-watcher) |
| **Session Storage** | `session/twitter/` (login cache) |
| **Captured DMs** | `Needs_Action/twitter_*.md` |
| **Draft Responses** | `Plans/twitter_draft_[date].md` |
| **Pending Approval** | `Pending_Approval/twitter_draft_*.md` |
| **Approved** | `Approved/twitter_draft_*.md` |
| **Logs** | `watchers/logs/twitter_watcher.log` |

---

## 🔑 Keywords Detected

Twitter watcher captures any DM containing:
```
'sales', 'client', 'project', 'urgent', 'invoice',
'payment', 'deal', 'opportunity', 'partnership', 'lead', 'inquiry'
```

**Example messages that trigger capture:**
- "Hi! I have a sales opportunity"
- "Can we discuss client needs?"
- "Invoice payment is due"
- "Partnership opportunity"
- "New lead for our project"

---

## 🛠️ Troubleshooting

### Problem: Browser won't open
```bash
# Check logs
pm2 logs twitter-watcher --lines 50

# Restart watcher
pm2 restart twitter-watcher
```

### Problem: Messages not captured
```bash
# Verify watcher is running
pm2 list | grep twitter

# Check if message has keywords
# Keywords: sales, client, project, urgent, invoice, payment, deal, opportunity, partnership, lead, inquiry

# Check logs
pm2 logs twitter-watcher
```

### Problem: Draft not generating
```bash
# Verify message is in Needs_Action
ls Needs_Action/twitter_*.md

# Run generator with debug
python skills/twitter_post_generator.py

# Check generator logs
cat skills/logs/twitter_post_generator.log
```

---

## 📊 System Now (6 Platforms)

```
✅ Gmail        (watchers/gmail_watcher.py)
✅ WhatsApp     (watchers/whatsapp_persistent.py)
✅ LinkedIn     (watchers/linkedin_persistent.py)
✅ Instagram    (watchers/instagram_watcher_fixed.py)
✅ Facebook     (watchers/facebook_watcher_js_extract.py)
✅ Twitter/X    (watchers/twitter_watcher.py)  ← NEW!
```

---

## 🚀 Run Instructions

### Start All 6 Watchers
```bash
cd "C:\Users\14loa\Desktop\IT\GIAIC\Q4 spec kit\Hackathon0Gold"
pm2 start ecosystem.config.js
```

### Verify All Running
```bash
pm2 list
# Should show 6 watchers: gmail, whatsapp, linkedin, instagram, facebook, twitter
```

### Monitor Messages
```bash
python monitor-messages.py
```

### Check Twitter Logs
```bash
pm2 logs twitter-watcher
```

---

## 📋 Checklist

- [ ] Twitter watcher script created: `watchers/twitter_watcher.py`
- [ ] Twitter post generator created: `skills/twitter_post_generator.py`
- [ ] PM2 config updated: `ecosystem.config.js` (twitter-watcher added)
- [ ] Session directory created: `session/twitter/`
- [ ] Watcher running: `pm2 list` shows twitter-watcher online
- [ ] Test DM sent from another account
- [ ] Message captured in `Needs_Action/`
- [ ] Draft generated in `Plans/`
- [ ] Draft moved to `Pending_Approval/`
- [ ] Approval workflow tested

---

## ✅ Success Indicators

**System Working When:**
1. ✅ Twitter watcher shows "online" in `pm2 list`
2. ✅ DM with keywords creates file in `Needs_Action/`
3. ✅ Post generator finds and processes Twitter files
4. ✅ Draft response created in `Plans/`
5. ✅ Draft moved to `Pending_Approval/` for approval

---

**Twitter Watcher is now part of your Gold Tier 6-platform system!** 🐦✨