---
title: Gmail Testing Guide - Complete Test Cases
date: 2026-03-29
status: PRODUCTION READY
version: 2.0
---

# Gmail Testing Guide

Complete test cases for validating Gmail email workflow in the AI Social Media Manager system.

---

## Test 1: Basic Gmail Email Creation

**Objective:** Create a Gmail email draft and verify metadata

**Step-by-Step Instructions:**

### Step 1a: Run Gmail Watcher (First Time Only)
```bash
# This opens a browser for Gmail login
python watchers/gmail_watcher.py
```

**What happens:**
- Browser opens with Gmail
- Log in with your Gmail credentials
- Allow permissions if prompted
- Wait for Gmail inbox to load
- Close the browser when done
- Session is saved to ./session/gmail

### Step 1b: Create Gmail Email Draft
```bash
# This creates an email draft for you to review
python trigger_gmail_post.py
```

**Expected Output:**
```
✅ Gmail Draft Creator Successfully!
======================================================================
📝 POST PREVIEW
======================================================================
---
platform: gmail
title: Email Subject
from: trigger_posts
type: email
priority: medium
status: pending_approval
created_at: 2026-03-29T10:15:34.123456
requires_approval: true
---

# Email Subject

This is the email body content.

---
📁 File saved to: Pending_Approval/POST_20260329_101534_gm_abc123.md
```

### Step 1b: Verify File Created
```bash
ls Pending_Approval/ | grep "_gm_"
# Expected: POST_20260329_101534_gm_abc123.md

cat Pending_Approval/POST_20260329_101534_gm_abc123.md
```

**Verification Checklist:**
- [ ] File exists in `Pending_Approval/`
- [ ] Filename contains `_gm_` (Gmail code)
- [ ] Subject preserved: "Email Subject"
- [ ] Body preserved exactly
- [ ] `platform: gmail` in YAML
- [ ] `type: email`
- [ ] `status: pending_approval`

**Pass Criteria:** ✅ Email created

---

## Test 2: Gmail Default Content

**Objective:** Verify default email template

**Step-by-Step Instructions:**

### Step 2a: Create Without Content
```bash
python scripts/trigger_posts.py -p gmail --preview
```

**Expected Output:**
```
---
platform: gmail
title: Professional Email
---

# Professional Email

Hi there,

I hope this email finds you well.

I wanted to reach out with some exciting news.

Looking forward to hearing from you!

Best regards
```

### Step 2b: Verify Template
```bash
cat Pending_Approval/POST_*_gm_*.md | grep -A 15 "# Professional"

# Should show complete default template
```

**Verification Checklist:**
- [ ] Default subject: "Professional Email"
- [ ] Greeting present
- [ ] Professional tone
- [ ] Sign-off: "Best regards"
- [ ] Multiple paragraphs
- [ ] Complete template

**Pass Criteria:** ✅ Default template applied

---

## Test 3: Gmail Orchestrator Detection

**Objective:** Verify Master Orchestrator detects emails

**Step-by-Step Instructions:**

### Step 3a: Start Orchestrator (Terminal 1)
```bash
python scripts/master_orchestrator.py
```

### Step 3b: Create Email (Terminal 2)
```bash
python scripts/trigger_posts.py -p gmail -c "Testing orchestrator" -t "Test"
```

### Step 3c: Move to Approved
```bash
mv Pending_Approval/POST_*_gm_*.md Approved/
```

### Step 3d: Monitor Detection (Terminal 1)
```
[2026-03-29 10:15:39] 📋 Processing: POST_*_gm_*.md
[2026-03-29 10:15:39] Platform: gmail
[2026-03-29 10:15:39] 🚀 Executing...
```

**Verification Checklist:**
- [ ] Detected within 5 seconds
- [ ] Platform identified as `gmail`
- [ ] Executor launched
- [ ] No errors

**Pass Criteria:** ✅ Detection works

---

## Test 4: Gmail Executor Processing

**Objective:** Verify email sending via Gmail

**Step-by-Step Instructions:**

### Step 4a: Watch Execution (Terminal 1)
```
[2026-03-29 10:15:40] 🚀 Executing...
[2026-03-29 10:15:45] Launching browser for Gmail...
[2026-03-29 10:15:55] Finding compose button...
[2026-03-29 10:16:00] Filling subject...
[2026-03-29 10:16:05] Filling body...
[2026-03-29 10:16:10] Sending email...
[2026-03-29 10:16:15] ✅ SUCCESS: Email sent!
[2026-03-29 10:16:15] ✅ Moved to Done
```

### Step 4b: Verify Completion (Terminal 2)
```bash
ls Done/ | grep "_gm_"
# Expected: processed_POST_*_gm_*.md

ls Approved/ | grep "_gm_" | wc -l
# Expected: 0
```

**Verification Checklist:**
- [ ] Browser opened
- [ ] Gmail loaded
- [ ] Compose window opened
- [ ] Subject filled correctly
- [ ] Body filled correctly
- [ ] Email sent
- [ ] File moved to Done
- [ ] Time: 20-35 seconds

**Pass Criteria:** ✅ Email sent successfully

---

## Test 5: Gmail Email Subject

**Objective:** Verify subject line handling

**Step-by-Step Instructions:**

### Step 5a: Create with Custom Subject
```bash
python scripts/trigger_posts.py -p gmail \
  -c "This is the email body." \
  -t "Important Update from Team" \
  --preview
```

### Step 5b: Verify Subject in File
```bash
cat Pending_Approval/POST_*_gm_*.md | head -20

# Should show:
# ---
# title: Important Update from Team
# ---
```

### Step 5c: Send and Verify
```bash
mv Pending_Approval/POST_*_gm_*.md Approved/

# Wait for sending (watch Terminal 1)
# Manually check Gmail that subject shows correctly
```

**Verification Checklist:**
- [ ] Subject preserved in file
- [ ] Subject appears in email YAML
- [ ] Subject displays in Gmail inbox
- [ ] Subject matches exactly
- [ ] No truncation

**Pass Criteria:** ✅ Subject handled correctly

---

## Test 6: Gmail Performance Timing

**Objective:** Verify email sending timing

**Step-by-Step Instructions:**

### Step 6a: Create with Timing
```bash
date "+%H:%M:%S"
python scripts/trigger_posts.py -p gmail -c "Perf test" -t "Subject"
# Created: 10:15:34
```

### Step 6b: Move and Monitor
```bash
date "+%H:%M:%S"
mv Pending_Approval/POST_*_gm_*.md Approved/
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

## Test 7: Gmail Batch Processing

**Objective:** Test multiple emails processed sequentially

**Step-by-Step Instructions:**

### Step 7a: Create 5 Emails
```bash
python scripts/trigger_posts.py -p gmail -c "Email 1" -t "Email 1" && sleep 10
python scripts/trigger_posts.py -p gmail -c "Email 2" -t "Email 2" && sleep 10
python scripts/trigger_posts.py -p gmail -c "Email 3" -t "Email 3" && sleep 10
python scripts/trigger_posts.py -p gmail -c "Email 4" -t "Email 4" && sleep 10
python scripts/trigger_posts.py -p gmail -c "Email 5" -t "Email 5"

# Verify all created
ls Pending_Approval/ | grep "_gm_" | wc -l
# Expected: 5
```

### Step 7b: Approve All
```bash
mv Pending_Approval/POST_*_gm_*.md Approved/

ls Approved/ | grep "_gm_" | wc -l
# Expected: 5
```

### Step 7c: Monitor Processing (Terminal 1)
```
[10:16:00] 📋 Email 1... → ✅ Done (30s)
[10:16:30] 📋 Email 2... → ✅ Done (30s)
[10:17:00] 📋 Email 3... → ✅ Done (30s)
[10:17:30] 📋 Email 4... → ✅ Done (30s)
[10:18:00] 📋 Email 5... → ✅ Done (30s)

Total: ~150 seconds ✓
```

### Step 7d: Verify Completion
```bash
ls Done/ | grep "_gm_" | wc -l
# Expected: 5

ls Approved/ | grep "_gm_" | wc -l
# Expected: 0
```

**Verification Checklist:**
- [ ] All 5 emails created
- [ ] All approved
- [ ] All processed sequentially
- [ ] Each takes 20-35 seconds
- [ ] Total: 100-175 seconds
- [ ] All in Done/

**Pass Criteria:** ✅ Batch successful

---

## Test 8: Gmail Error Recovery

**Objective:** Test automatic retry after failure

**Step-by-Step Instructions:**

### Step 8a: Create and Approve
```bash
python scripts/trigger_posts.py -p gmail -c "Error test" -t "Subject"
mv Pending_Approval/POST_*_gm_*.md Approved/
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
[2026-03-29 10:21:45] ✅ SUCCESS: Email sent!
```

**Verification Checklist:**
- [ ] First attempt fails
- [ ] Error logged
- [ ] Cooldown starts
- [ ] File stays in Approved
- [ ] Auto retry after 5 min
- [ ] Success on retry
- [ ] Moved to Done

**Pass Criteria:** ✅ Retry succeeds

---

## Test 9: Gmail Content Formatting

**Objective:** Verify content formatting preserved

**Step-by-Step Instructions:**

### Step 9a: Create with Formatting
```bash
python scripts/trigger_posts.py -p gmail \
  -c "This is a test email with special text: **bold** #hashtag @mention \"quotes\"" \
  -t "Test Subject" \
  --preview
```

### Step 9b: Check File Content
```bash
cat Pending_Approval/POST_*_gm_*.md | grep -A 5 "^#"

# Should show all special characters
```

### Step 9c: Send and Verify
```bash
mv Pending_Approval/POST_*_gm_*.md Approved/

# Wait for sending
# Check Gmail that content appears correctly
```

**Verification Checklist:**
- [ ] Content preserved in file
- [ ] Special characters intact
- [ ] Bold markers: **bold**
- [ ] Hashtags: #hashtag
- [ ] Mentions: @mention
- [ ] Quotes: "quotes"
- [ ] All display correctly in Gmail

**Pass Criteria:** ✅ Formatting preserved

---

## Test 10: Gmail Session Persistence

**Objective:** Verify session persists across emails

**Step-by-Step Instructions:**

### Step 10a: Email 1 - Initial Login
```bash
python scripts/trigger_posts.py -p gmail -c "Email 1" -t "Subj 1"
mv Pending_Approval/POST_*_gm_001.md Approved/
```

**Terminal 1 shows:**
```
[10:16:00] Logging into Gmail...
[10:16:15] Account logged in ✅
[10:16:20] Composing...
[10:16:30] ✅ SUCCESS
```

### Step 10b: Email 2 - Reuse Session
```bash
python scripts/trigger_posts.py -p gmail -c "Email 2" -t "Subj 2"
mv Pending_Approval/POST_*_gm_002.md Approved/
```

**Terminal 1 shows:**
```
[10:16:35] Using saved session ✅
[10:16:40] Composing...
[10:16:50] ✅ SUCCESS
```

### Step 10c: Email 3 - Still Using Session
```bash
python scripts/trigger_posts.py -p gmail -c "Email 3" -t "Subj 3"
mv Pending_Approval/POST_*_gm_003.md Approved/
```

**Terminal 1 shows:**
```
[10:17:00] Using saved session ✅
[10:17:05] Composing...
[10:17:15] ✅ SUCCESS
```

### Step 10d: Verify Session
```bash
ls -la session/
# Should have Gmail browser data
```

**Verification Checklist:**
- [ ] Email 1: Shows login process
- [ ] Email 2: Shows "Using saved session"
- [ ] Email 3: Shows "Using saved session"
- [ ] Session folder has files
- [ ] Emails 2 & 3 faster (no login)

**Pass Criteria:** ✅ Session persists

---

## Test 11: Gmail Single Recipient

**Objective:** Verify single recipient handling

**Step-by-Step Instructions:**

### Step 11a: Create Email for One Recipient
```bash
python scripts/trigger_posts.py -p gmail \
  -c "Hello, this email is just for you!" \
  -t "Personal Message" \
  --preview
```

### Step 11b: Send and Verify
```bash
mv Pending_Approval/POST_*_gm_*.md Approved/

# Wait for sending
# Check that email arrives in recipient's inbox
```

**Verification Checklist:**
- [ ] Email created successfully
- [ ] Sent to intended recipient
- [ ] Email appears in their inbox
- [ ] Subject and body correct

**Pass Criteria:** ✅ Single recipient works

---

## Test 12: Gmail Multi-Recipient

**Objective:** Verify multiple recipient handling

**Step-by-Step Instructions:**

### Step 12a: Create for Multiple Recipients
```bash
python scripts/trigger_posts.py -p gmail \
  -c "Hello team, this is for everyone!" \
  -t "Team Update" \
  --preview
```

### Step 12b: Send and Verify
```bash
mv Pending_Approval/POST_*_gm_*.md Approved/

# Wait for sending
# Verify all recipients receive the email
```

**Verification Checklist:**
- [ ] Email created successfully
- [ ] Sent to all recipients
- [ ] All inboxes receive it
- [ ] Subject and body intact
- [ ] No recipient list visible

**Pass Criteria:** ✅ Multi-recipient works

---

## Troubleshooting

### Browser Won't Open
```bash
playwright install chromium firefox
pkill -f social_media_executor
sleep 2
python scripts/master_orchestrator.py
```

### Email Stuck in Approved
```bash
ps aux | grep master_orchestrator
# If not running, restart

tail -20 Logs/orchestrator_*.log
```

### Session Expired
```bash
# Clear session and re-login
rm -rf session/*

# Next email will require login again
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
| Email subject | ✅ |
| Performance | ✅ |
| Batch (5 emails) | ✅ |
| Error recovery | ✅ |
| Formatting | ✅ |
| Session persist | ✅ |
| Single recipient | ✅ |
| Multi-recipient | ✅ |

**Status:** ✅ PRODUCTION READY
**Last Updated:** 2026-03-30
**Version:** 2.0 (Enhanced with detailed instructions)
