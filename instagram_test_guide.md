---
title: Instagram Testing Guide - Complete Test Cases
date: 2026-03-29
status: PRODUCTION READY
version: 2.0
---

# Instagram Testing Guide

Complete test cases for validating Instagram posting workflow in the AI Social Media Manager system.

---

## Test 1: Basic Instagram Post Creation

**Objective:** Create an Instagram post draft and verify metadata

**Step-by-Step Instructions:**

### Step 1a: Run Instagram Watcher (First Time Only)
```bash
# This opens a browser for login setup
python watchers/instagram_watcher.py
```

**What happens:**
- Browser opens automatically
- Log in to Instagram with your credentials
- Wait for homepage to load
- Close the browser when done
- Session is saved to ./session/instagram

### Step 1b: Create Instagram Post Draft
```bash
# This creates an Instagram post draft for you to review
python trigger_instagram_post.py
```

**Expected Output:**
```
✅ Instagram Draft Creator Successfully!
======================================================================
📝 POST PREVIEW
======================================================================
---
platform: instagram
title: Instagram Post
from: trigger_posts
type: instagram_post
priority: medium
status: pending_approval
created_at: 2026-03-29T10:15:34.123456
requires_approval: true
---

# Instagram Post

Creating something beautiful ✨

---
📁 File saved to: Pending_Approval/POST_20260329_101534_ig_abc123.md
```

### Step 1b: Verify File Creation
```bash
ls Pending_Approval/ | grep "_ig_"
# Expected: POST_20260329_101534_ig_abc123.md

cat Pending_Approval/POST_20260329_101534_ig_abc123.md
```

**Verification Checklist:**
- [ ] File exists in `Pending_Approval/`
- [ ] Filename contains `_ig_` (Instagram platform code)
- [ ] Content preserved exactly
- [ ] Emoji (✨) preserved
- [ ] YAML valid
- [ ] `platform: instagram` set

**Pass Criteria:** ✅ File created successfully

---

## Test 2: Instagram Default Content

**Objective:** Verify default Instagram caption template

**Step-by-Step Instructions:**

### Step 2a: Create Without Content
```bash
python scripts/trigger_posts.py -p instagram --preview
```

**Expected Output:**
```
---
platform: instagram
title: Instagram Post
---

# Instagram Post

Creating something beautiful ✨

Stay inspired and keep creating!

#Inspiration #Creative #Growth
```

### Step 2b: Verify Template
```bash
cat Pending_Approval/POST_*_ig_*.md | grep -A 10 "# Instagram Post"
```

**Verification Checklist:**
- [ ] Default caption loaded
- [ ] Emoji included (✨)
- [ ] Hashtags present
- [ ] Inspirational tone
- [ ] Multiple lines

**Pass Criteria:** ✅ Default template applied

---

## Test 3: Instagram Orchestrator Detection

**Objective:** Verify Master Orchestrator detects Instagram posts

**Step-by-Step Instructions:**

### Step 3a: Start Orchestrator (Terminal 1)
```bash
python scripts/master_orchestrator.py
```

### Step 3b: Create Post (Terminal 2)
```bash
python scripts/trigger_posts.py -p instagram -c "Test post for detection"
```

### Step 3c: Move to Approved
```bash
mv Pending_Approval/POST_*_ig_*.md Approved/
```

### Step 3d: Monitor Detection (Terminal 1)
```
[2026-03-29 10:15:39] 📋 Processing: POST_*_ig_*.md
[2026-03-29 10:15:39] Platform: instagram
[2026-03-29 10:15:39] 🚀 Executing...
```

**Verification Checklist:**
- [ ] Detected within 5 seconds
- [ ] Platform identified as `instagram`
- [ ] Executor launched
- [ ] No errors

**Pass Criteria:** ✅ Orchestrator detects posts

---

## Test 4: Instagram Executor Processing

**Objective:** Verify posting to Instagram

**Step-by-Step Instructions:**

### Step 4a: Watch Execution (Terminal 1)
```
[2026-03-29 10:15:40] 🚀 Executing...
[2026-03-29 10:15:45] Launching browser for Instagram...
[2026-03-29 10:15:55] Finding create button...
[2026-03-29 10:16:00] Filling caption...
[2026-03-29 10:16:05] Posting to Instagram...
[2026-03-29 10:16:10] ✅ SUCCESS: Post created!
[2026-03-29 10:16:10] ✅ Moved to Done
```

### Step 4b: Verify Completion (Terminal 2)
```bash
ls Done/ | grep "_ig_"
# Expected: processed_POST_*_ig_*.md

ls Approved/ | grep "_ig_" | wc -l
# Expected: 0
```

**Verification Checklist:**
- [ ] Browser opened
- [ ] Instagram loaded
- [ ] Create flow initiated
- [ ] Caption filled
- [ ] Post published
- [ ] File moved to Done
- [ ] Time: 20-35 seconds

**Pass Criteria:** ✅ Post successful

---

## Test 5: Instagram Visual Content & Emojis

**Objective:** Verify emoji rendering and visual content handling

**Step-by-Step Instructions:**

### Step 5a: Create Post with Emojis
```bash
python scripts/trigger_posts.py -p instagram \
  -c "Beautiful capture 📸 Amazing moment 🌟 Love this 💕 Nature 🌿" \
  --preview
```

### Step 5b: Verify Emojis in File
```bash
cat Pending_Approval/POST_*_ig_*.md | grep -o "📸\|🌟\|💕\|🌿"

# Expected output:
# 📸
# 🌟
# 💕
# 🌿
```

### Step 5c: Post and Verify Display
```bash
mv Pending_Approval/POST_*_ig_*.md Approved/

# Wait for posting
# Manually check Instagram.com that all emojis display correctly
```

**Verification Checklist:**
- [ ] All emojis preserved in file
- [ ] All emojis display on Instagram
- [ ] No emoji corruption
- [ ] Visual rendering correct

**Pass Criteria:** ✅ Visual content handled correctly

---

## Test 6: Instagram Performance Timing

**Objective:** Verify posting timing

**Step-by-Step Instructions:**

### Step 6a: Create with Timestamp
```bash
date "+%H:%M:%S"
python scripts/trigger_posts.py -p instagram -c "Perf test"
# Created: 10:15:34
```

### Step 6b: Approve and Time
```bash
date "+%H:%M:%S"
mv Pending_Approval/POST_*_ig_*.md Approved/
# Approved: 10:15:35
```

### Step 6c: Monitor Processing (Terminal 1)
```
10:15:39 - Detected
10:15:40 - Executor started
10:15:55 - Posted
10:16:00 - Done

Total: 25 seconds ✓
```

**Verification Checklist:**
- [ ] Detection: < 5 seconds
- [ ] Posting: < 25 seconds
- [ ] Total: 20-35 seconds

**Pass Criteria:** ✅ Performance acceptable

---

## Test 7: Instagram Batch Processing

**Objective:** Test multiple posts processed sequentially

**Step-by-Step Instructions:**

### Step 7a: Create 4 Posts
```bash
python scripts/trigger_posts.py -p instagram -c "Post 1: First" && sleep 10
python scripts/trigger_posts.py -p instagram -c "Post 2: Second" && sleep 10
python scripts/trigger_posts.py -p instagram -c "Post 3: Third" && sleep 10
python scripts/trigger_posts.py -p instagram -c "Post 4: Fourth"

# Verify all created
ls Pending_Approval/ | grep "_ig_" | wc -l
# Expected: 4
```

### Step 7b: Approve All
```bash
mv Pending_Approval/POST_*_ig_*.md Approved/

ls Approved/ | grep "_ig_" | wc -l
# Expected: 4
```

### Step 7c: Monitor Processing (Terminal 1)
```
[10:16:00] 📋 Post 1... → ✅ Done (30s)
[10:16:30] 📋 Post 2... → ✅ Done (30s)
[10:17:00] 📋 Post 3... → ✅ Done (30s)
[10:17:30] 📋 Post 4... → ✅ Done (30s)

Total: ~120 seconds ✓
```

### Step 7d: Verify Completion
```bash
ls Done/ | grep "_ig_" | wc -l
# Expected: 4

ls Approved/ | grep "_ig_" | wc -l
# Expected: 0
```

**Verification Checklist:**
- [ ] All 4 created
- [ ] All approved
- [ ] All processed
- [ ] Total time: 80-140 seconds
- [ ] All in Done/

**Pass Criteria:** ✅ Batch successful

---

## Test 8: Instagram Error Recovery

**Objective:** Test retry after failure

**Step-by-Step Instructions:**

### Step 8a: Create and Approve
```bash
python scripts/trigger_posts.py -p instagram -c "Error test"
mv Pending_Approval/POST_*_ig_*.md Approved/
```

### Step 8b: Close Browser During Posting
**Watch Terminal 1, close browser when execution starts**

### Step 8c: Monitor Retry (Terminal 1)
```
[10:16:00] 🚀 Executing...
[10:16:10] ❌ Failed: BrowserClosed
[10:16:10] 🔄 Retry scheduled (5 min)
[10:21:15] 🚀 Retrying... (Attempt 2/4)
[10:21:45] ✅ SUCCESS
```

**Verification Checklist:**
- [ ] First attempt fails
- [ ] Error logged
- [ ] Cooldown timer starts
- [ ] Automatic retry after 5 min
- [ ] Success on retry
- [ ] File moved to Done

**Pass Criteria:** ✅ Retry succeeds

---

## Test 9: Instagram Caption Formatting

**Objective:** Verify special formatting preserved

**Step-by-Step Instructions:**

### Step 9a: Create with Special Formatting
```bash
python scripts/trigger_posts.py -p instagram \
  -c "Amazing shot 📸 #instagram @friends \"Love this\"" \
  --preview
```

### Step 9b: Check File
```bash
cat Pending_Approval/POST_*_ig_*.md | grep -A 5 "# Instagram"

# Should show all special chars
```

### Step 9c: Post and Verify
```bash
mv Pending_Approval/POST_*_ig_*.md Approved/

# Wait for completion
# Verify on Instagram.com all formatting displays
```

**Verification Checklist:**
- [ ] Emoji preserved (📸)
- [ ] Hashtag preserved (#instagram)
- [ ] Mention preserved (@friends)
- [ ] Quotes preserved ("Love this")
- [ ] All display correctly on Instagram

**Pass Criteria:** ✅ Formatting preserved

---

## Test 10: Instagram Session Persistence

**Objective:** Verify session persists across posts

**Step-by-Step Instructions:**

### Step 10a: Post 1 - Login
```bash
python scripts/trigger_posts.py -p instagram -c "Post 1"
mv Pending_Approval/POST_*_ig_001.md Approved/
```

**Terminal 1 shows:**
```
[10:16:00] Logging into Instagram...
[10:16:15] Account logged in ✅
[10:16:20] Posting...
[10:16:30] ✅ SUCCESS
```

### Step 10b: Post 2 - Reuse Session
```bash
python scripts/trigger_posts.py -p instagram -c "Post 2"
mv Pending_Approval/POST_*_ig_002.md Approved/
```

**Terminal 1 shows:**
```
[10:16:35] Using saved session ✅
[10:16:40] Posting...
[10:16:50] ✅ SUCCESS
```

### Step 10c: Post 3 - Still Using Session
```bash
python scripts/trigger_posts.py -p instagram -c "Post 3"
mv Pending_Approval/POST_*_ig_003.md Approved/
```

**Terminal 1 shows:**
```
[10:17:00] Using saved session ✅
[10:17:05] Posting...
[10:17:15] ✅ SUCCESS
```

### Step 10d: Verify Session
```bash
ls -la session/
# Should have browser profile data
```

**Verification Checklist:**
- [ ] Post 1: Shows login
- [ ] Post 2: Shows "Using saved session"
- [ ] Post 3: Shows "Using saved session"
- [ ] Session folder has data
- [ ] Posts 2 & 3 faster (no login overhead)

**Pass Criteria:** ✅ Session persists

---

## Troubleshooting

### Browser Issues
```bash
playwright install chromium
pkill -f social_media_executor
python scripts/master_orchestrator.py
```

### Post Stuck in Approved
```bash
ps aux | grep master_orchestrator
# Restart if needed

tail -20 Logs/orchestrator_*.log
```

### Missing Directories
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
| Visual content | ✅ |
| Performance | ✅ |
| Batch (4 posts) | ✅ |
| Error recovery | ✅ |
| Caption format | ✅ |
| Session persist | ✅ |

**Status:** ✅ PRODUCTION READY
**Last Updated:** 2026-03-30
**Version:** 2.0 (Enhanced with detailed instructions)
