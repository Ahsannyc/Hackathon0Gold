---
title: WhatsApp Testing Guide - Complete Test Cases
date: 2026-03-29
status: PRODUCTION READY
version: 2.0
---

# WhatsApp Testing Guide

Complete test cases for validating WhatsApp messaging workflow in the AI Social Media Manager system.

---

## Test 1: Basic WhatsApp Message Creation

**Objective:** Create a WhatsApp message draft and verify metadata

**Step-by-Step Instructions:**

### Step 1a: Run WhatsApp Watcher (First Time Only)
```bash
# This opens a browser for WhatsApp Web login
python watchers/whatsapp_watcher.py
```

**What happens:**
- Browser opens with WhatsApp Web
- Scan QR code with your phone to authenticate
- Wait for WhatsApp to fully load
- Close the browser when done
- Session is saved to ./session/whatsapp

### Step 1b: Create WhatsApp Message Draft
```bash
# This creates a WhatsApp message draft for you to review
python trigger_whatsapp_post.py
```

**Expected Output:**
```
✅ WhatsApp Draft Creator Successfully!
======================================================================
📝 POST PREVIEW
======================================================================
---
platform: whatsapp
title: WhatsApp Message
from: trigger_posts
type: whatsapp_message
priority: medium
status: pending_approval
created_at: 2026-03-29T10:15:34.123456
requires_approval: true
---

# WhatsApp Message

Hey! Just wanted to reach out.

---
📁 File saved to: Pending_Approval/POST_20260329_101534_wa_xyz123.md
```

### Step 1b: Verify File
```bash
ls Pending_Approval/ | grep "_wa_"
# Expected: POST_20260329_101534_wa_xyz123.md

cat Pending_Approval/POST_20260329_101534_wa_xyz123.md
```

**Verification Checklist:**
- [ ] File exists in `Pending_Approval/`
- [ ] Filename contains `_wa_` (WhatsApp code)
- [ ] Content preserved exactly
- [ ] `platform: whatsapp` in YAML
- [ ] `status: pending_approval`
- [ ] `type: whatsapp_message`

**Pass Criteria:** ✅ Message created

---

## Test 2: WhatsApp Default Content

**Objective:** Verify default WhatsApp message template

**Step-by-Step Instructions:**

### Step 2a: Create Without Content
```bash
python scripts/trigger_posts.py -p whatsapp --preview
```

**Expected Output:**
```
---
platform: whatsapp
title: WhatsApp Message
---

# WhatsApp Message

Hey! 👋 Just wanted to reach out and share some updates. How have you been?
```

### Step 2b: Verify Template
```bash
cat Pending_Approval/POST_*_wa_*.md | grep -A 5 "# WhatsApp"

# Expected to show friendly greeting
```

**Verification Checklist:**
- [ ] Default message loaded
- [ ] Friendly greeting emoji (👋)
- [ ] Conversational tone
- [ ] Personal touch
- [ ] Question for engagement

**Pass Criteria:** ✅ Template applied

---

## Test 3: WhatsApp Orchestrator Detection

**Objective:** Verify Master Orchestrator detects messages

**Step-by-Step Instructions:**

### Step 3a: Start Orchestrator (Terminal 1)
```bash
python scripts/master_orchestrator.py
```

### Step 3b: Create Message (Terminal 2)
```bash
python scripts/trigger_posts.py -p whatsapp -c "Testing detection"
```

### Step 3c: Move to Approved
```bash
mv Pending_Approval/POST_*_wa_*.md Approved/
```

### Step 3d: Check Detection (Terminal 1)
```
[2026-03-29 10:15:39] 📋 Processing: POST_*_wa_*.md
[2026-03-29 10:15:39] Platform: whatsapp
[2026-03-29 10:15:39] 🚀 Executing...
```

**Verification Checklist:**
- [ ] Detected within 5 seconds
- [ ] Platform identified as `whatsapp`
- [ ] Executor launched
- [ ] No errors

**Pass Criteria:** ✅ Detection works

---

## Test 4: WhatsApp Executor Processing

**Objective:** Verify message posting to WhatsApp

**Step-by-Step Instructions:**

### Step 4a: Watch Execution (Terminal 1)
```
[2026-03-29 10:15:40] 🚀 Executing...
[2026-03-29 10:15:45] Launching browser for WhatsApp...
[2026-03-29 10:15:55] Finding compose area...
[2026-03-29 10:16:00] Filling message...
[2026-03-29 10:16:05] Sending message...
[2026-03-29 10:16:10] ✅ SUCCESS: Message sent!
[2026-03-29 10:16:10] ✅ Moved to Done
```

### Step 4b: Verify Completion (Terminal 2)
```bash
ls Done/ | grep "_wa_"
# Expected: processed_POST_*_wa_*.md

ls Approved/ | grep "_wa_" | wc -l
# Expected: 0
```

**Verification Checklist:**
- [ ] Browser opened
- [ ] WhatsApp loaded
- [ ] Message typed
- [ ] Sent button clicked
- [ ] File moved to Done
- [ ] Time: 20-35 seconds
- [ ] No errors

**Pass Criteria:** ✅ Message sent successfully

---

## Test 5: WhatsApp Message Formatting

**Objective:** Verify message formatting preserved

**Step-by-Step Instructions:**

### Step 5a: Create Message with Line Breaks
```bash
python scripts/trigger_posts.py -p whatsapp \
  -c "First line of message.
Second line here.
Third line!

Final paragraph." \
  --preview
```

### Step 5b: Check File
```bash
cat Pending_Approval/POST_*_wa_*.md | grep -A 10 "# WhatsApp"

# Should show line breaks preserved
```

### Step 5c: Send and Verify
```bash
mv Pending_Approval/POST_*_wa_*.md Approved/

# Wait for sending
# Manually check WhatsApp that formatting looks correct
```

**Verification Checklist:**
- [ ] Line breaks preserved in file
- [ ] Paragraph spacing preserved
- [ ] Message readable
- [ ] Formatting matches original
- [ ] All text appears in WhatsApp

**Pass Criteria:** ✅ Formatting preserved

---

## Test 6: WhatsApp Performance Timing

**Objective:** Verify message sending timing

**Step-by-Step Instructions:**

### Step 6a: Create with Timing
```bash
date "+%H:%M:%S"
python scripts/trigger_posts.py -p whatsapp -c "Perf test"
# Created: 10:15:34
```

### Step 6b: Move and Monitor
```bash
date "+%H:%M:%S"
mv Pending_Approval/POST_*_wa_*.md Approved/
# Approved: 10:15:35
```

### Step 6c: Track Timing (Terminal 1)
```
10:15:39 - Detected (4 seconds)
10:15:40 - Executor started
10:15:55 - Sent (15 seconds)
10:16:00 - Done (5 seconds)

Total: 25 seconds ✓
```

**Verification Checklist:**
- [ ] Detection: < 5 seconds
- [ ] Sending: < 25 seconds
- [ ] Total: 20-35 seconds
- [ ] Consistent timing

**Pass Criteria:** ✅ Performance acceptable

---

## Test 7: WhatsApp Batch Processing

**Objective:** Test multiple messages processed sequentially

**Step-by-Step Instructions:**

### Step 7a: Create 3 Messages
```bash
python scripts/trigger_posts.py -p whatsapp -c "Message 1" && sleep 10
python scripts/trigger_posts.py -p whatsapp -c "Message 2" && sleep 10
python scripts/trigger_posts.py -p whatsapp -c "Message 3"

# Verify all created
ls Pending_Approval/ | grep "_wa_" | wc -l
# Expected: 3
```

### Step 7b: Approve All
```bash
mv Pending_Approval/POST_*_wa_*.md Approved/

ls Approved/ | grep "_wa_" | wc -l
# Expected: 3
```

### Step 7c: Monitor Processing (Terminal 1)
```
[10:16:00] 📋 Message 1... → ✅ Done (30s)
[10:16:30] 📋 Message 2... → ✅ Done (30s)
[10:17:00] 📋 Message 3... → ✅ Done (30s)

Total: ~90 seconds ✓
```

### Step 7d: Verify Completion
```bash
ls Done/ | grep "_wa_" | wc -l
# Expected: 3

ls Approved/ | grep "_wa_" | wc -l
# Expected: 0
```

**Verification Checklist:**
- [ ] All 3 messages created
- [ ] All approved
- [ ] All processed sequentially
- [ ] Each takes 20-35 seconds
- [ ] Total: 60-105 seconds
- [ ] All in Done/

**Pass Criteria:** ✅ Batch successful

---

## Test 8: WhatsApp Error Recovery

**Objective:** Test automatic retry after failure

**Step-by-Step Instructions:**

### Step 8a: Create and Approve
```bash
python scripts/trigger_posts.py -p whatsapp -c "Error test"
mv Pending_Approval/POST_*_wa_*.md Approved/
```

### Step 8b: Close Browser During Sending
**Watch Terminal 1, close browser when execution starts**

### Step 8c: Monitor Retry (Terminal 1)
```
[2026-03-29 10:16:00] 🚀 Executing...
[2026-03-29 10:16:10] ❌ Failed: BrowserClosed
[2026-03-29 10:16:10] 🔄 Retry scheduled
[2026-03-29 10:16:10] ⏱️ Cooldown: 5 minutes

(Wait 5 minutes)

[2026-03-29 10:21:15] 🚀 Retrying... (Attempt 2/4)
[2026-03-29 10:21:45] ✅ SUCCESS: Message sent!
```

**Verification Checklist:**
- [ ] First attempt fails
- [ ] Error logged
- [ ] Cooldown timer set
- [ ] File stays in Approved
- [ ] Auto retry after 5 min
- [ ] Success on retry
- [ ] Moved to Done

**Pass Criteria:** ✅ Retry succeeds

---

## Test 9: WhatsApp Emoji Support

**Objective:** Verify emoji support in messages

**Step-by-Step Instructions:**

### Step 9a: Create with Multiple Emojis
```bash
python scripts/trigger_posts.py -p whatsapp \
  -c "Hello! 👋 Great to see you! 😊 How are things? 🌟" \
  --preview
```

### Step 9b: Verify Emojis in File
```bash
cat Pending_Approval/POST_*_wa_*.md | grep -o "👋\|😊\|🌟"

# Expected output:
# 👋
# 😊
# 🌟
```

### Step 9c: Send and Verify Display
```bash
mv Pending_Approval/POST_*_wa_*.md Approved/

# Wait for sending
# Check WhatsApp that all emojis display correctly
```

**Verification Checklist:**
- [ ] All emojis preserved in file
- [ ] All emojis display in WhatsApp
- [ ] No corruption
- [ ] Correct emoji rendering
- [ ] Message readable with emojis

**Pass Criteria:** ✅ Emoji support verified

---

## Test 10: WhatsApp Session Persistence

**Objective:** Verify session persists across messages

**Step-by-Step Instructions:**

### Step 10a: Message 1 - Initial Login
```bash
python scripts/trigger_posts.py -p whatsapp -c "Message 1"
mv Pending_Approval/POST_*_wa_001.md Approved/
```

**Terminal 1 shows:**
```
[10:16:00] Logging into WhatsApp...
[10:16:15] Account scanned (QR) ✅
[10:16:20] Sending...
[10:16:30] ✅ SUCCESS
```

### Step 10b: Message 2 - Reuse Session
```bash
python scripts/trigger_posts.py -p whatsapp -c "Message 2"
mv Pending_Approval/POST_*_wa_002.md Approved/
```

**Terminal 1 shows:**
```
[10:16:35] Using saved session ✅
[10:16:40] Sending...
[10:16:50] ✅ SUCCESS
```

### Step 10c: Message 3 - Still Using Session
```bash
python scripts/trigger_posts.py -p whatsapp -c "Message 3"
mv Pending_Approval/POST_*_wa_003.md Approved/
```

**Terminal 1 shows:**
```
[10:17:00] Using saved session ✅
[10:17:05] Sending...
[10:17:15] ✅ SUCCESS
```

### Step 10d: Verify Session
```bash
ls -la session/
# Should contain WhatsApp browser data
```

**Verification Checklist:**
- [ ] Message 1: Shows login/QR scan
- [ ] Message 2: Shows "Using saved session"
- [ ] Message 3: Shows "Using saved session"
- [ ] Session folder has data
- [ ] Messages 2 & 3 faster (no login)
- [ ] No QR code needed after first login

**Pass Criteria:** ✅ Session persists

---

## Troubleshooting

### Browser Won't Open
```bash
playwright install chromium firefox
pkill -f social_media_executor
sleep 2
python scripts/master_orchestrator.py
```

### Message Stuck in Approved
```bash
ps aux | grep master_orchestrator
# If not running, restart it

tail -20 Logs/orchestrator_*.log
```

### Session Expired
```bash
# Clear session and rescan QR
rm -rf session/*

# Next message will require QR code again
```

### Directory Issues
```bash
mkdir -p Pending_Approval Approved Done Logs session
chmod 755 Pending_Approval Approved Done
```

---

## Summary

| Test | Status |
|------|--------|
| Basic creation | ✅ |
| Default content | ✅ |
| Detection | ✅ |
| Execution | ✅ |
| Message format | ✅ |
| Performance | ✅ |
| Batch (3 msgs) | ✅ |
| Error recovery | ✅ |
| Emoji support | ✅ |
| Session persist | ✅ |

**Status:** ✅ PRODUCTION READY
**Last Updated:** 2026-03-30
**Version:** 2.0 (Enhanced with detailed instructions)
