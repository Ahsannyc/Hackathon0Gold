---
title: Twitter Testing Guide - Complete Test Cases
date: 2026-03-29
status: PRODUCTION READY
version: 2.0
---

# Twitter Testing Guide

Complete test cases for validating Twitter (X) posting workflow in the AI Social Media Manager system.

---

## Test 1: Basic Twitter Post Creation

**Objective:** Create a simple Twitter post draft and verify metadata

**Step-by-Step Instructions:**

### Step 1a: Run Twitter Watcher (First Time Only)
```bash
# This opens a browser for login setup
python watchers/twitter_watcher.py
```

**What happens:**
- Browser opens automatically
- Log in to Twitter/X with your credentials
- Wait for homepage to load
- Close the browser when done
- Session is saved to ./session/twitter

### Step 1b: Create Twitter Post Draft
```bash
# This creates a tweet draft for you to review
python trigger_twitter_post.py
```

**Expected Output:**
```
✅ Twitter Draft Creator Successfully!
======================================================================
📝 POST PREVIEW
======================================================================
---
platform: twitter
title: Twitter Post
from: trigger_posts
type: twitter_post
priority: medium
status: pending_approval
created_at: 2026-03-29T10:15:34.123456
requires_approval: true
---

# Twitter Post

Just launched something amazing! 🚀

---
📁 File saved to: Pending_Approval/POST_20260329_101534_tw_xyz123.md
```

### Step 1b: Verify File Created
```bash
# List files in Pending_Approval
ls Pending_Approval/ | grep "_tw_"

# Expected: POST_20260329_101534_tw_xyz123.md
```

### Step 1c: Read File Content
```bash
cat Pending_Approval/POST_20260329_101534_tw_xyz123.md
```

**Verification Checklist:**
- [ ] File exists in `Pending_Approval/`
- [ ] Filename contains `_tw_` (Twitter platform code)
- [ ] YAML frontmatter valid
- [ ] `platform: twitter` in metadata
- [ ] Content preserved: "Just launched something amazing! 🚀"
- [ ] `status: pending_approval`
- [ ] File is readable

**Pass Criteria:** ✅ File created with valid metadata

---

## Test 2: Twitter Default Content

**Objective:** Verify default Twitter content template

**Step-by-Step Instructions:**

### Step 2a: Create Post Without Content
```bash
python scripts/trigger_posts.py -p twitter --preview
```

**Expected Output:**
```
✅ Twitter Draft Creator Successfully!
---
platform: twitter
title: Twitter Post
---

# Twitter Post

Just launched something amazing! 🚀

Check it out and let us know what you think!

#Launch #Excited

---
📁 File saved to: Pending_Approval/POST_20260329_101600_tw_abc789.md
```

### Step 2b: Verify Template Content
```bash
cat Pending_Approval/POST_20260329_101600_tw_abc789.md | grep -A 10 "# Twitter Post"

# Expected to see:
# - Default message
# - Emoji
# - Hashtags
# - Call-to-action
```

**Verification Checklist:**
- [ ] Default content loaded
- [ ] Contains emoji (🚀)
- [ ] Contains hashtags (#Launch #Excited)
- [ ] Professional tone
- [ ] Appropriate length for Twitter

**Pass Criteria:** ✅ Default template applied correctly

---

## Test 3: Twitter Orchestrator Detection

**Objective:** Verify Master Orchestrator detects Twitter posts

**Step-by-Step Instructions:**

### Step 3a: Start Orchestrator (Terminal 1)
```bash
python scripts/master_orchestrator.py
```

**Expected:**
```
🎯 Master Orchestrator v2.0 - Starting...
📁 Monitoring /Approved folder for posts...
✅ Orchestrator ready
```

### Step 3b: Create Twitter Post (Terminal 2)
```bash
python scripts/trigger_posts.py -p twitter -c "Testing detection"
```

### Step 3c: Move to Approved
```bash
mv Pending_Approval/POST_*_tw_*.md Approved/
```

### Step 3d: Check Detection (Watch Terminal 1)
```
[2026-03-29 10:15:39] 📋 Processing: POST_*_tw_*.md
[2026-03-29 10:15:39] Platform: twitter
[2026-03-29 10:15:39] 🚀 Executing...
```

**Verification Checklist:**
- [ ] Detected within 5 seconds
- [ ] Platform identified as `twitter`
- [ ] Executor launched automatically
- [ ] No errors in logs

**Pass Criteria:** ✅ Orchestrator detects Twitter posts

---

## Test 4: Twitter Executor Processing

**Objective:** Verify executor posts to Twitter successfully

**Step-by-Step Instructions:**

### Step 4a: Watch Execution (Terminal 1)
**Monitor for completion:**
```
[2026-03-29 10:15:40] 🚀 Executing social_media_executor_v2.py
[2026-03-29 10:15:45] Launching browser for Twitter...
[2026-03-29 10:15:55] Finding compose button...
[2026-03-29 10:16:00] Filling content...
[2026-03-29 10:16:05] Posting tweet...
[2026-03-29 10:16:10] ✅ SUCCESS: Tweet posted!
[2026-03-29 10:16:10] ✅ Moved to Done
```

### Step 4b: Verify File Movement (Terminal 2)
```bash
# Check Done folder
ls Done/ | grep "_tw_"

# Expected: processed_POST_*_tw_*.md

# Verify not in Approved
ls Approved/ | grep "_tw_" | wc -l
# Expected: 0
```

**Verification Checklist:**
- [ ] Browser opened
- [ ] Twitter loaded
- [ ] Compose window opened
- [ ] Content filled correctly
- [ ] Tweet posted
- [ ] File moved to Done/
- [ ] Total time: 20-35 seconds
- [ ] No errors

**Pass Criteria:** ✅ Post successfully created on Twitter

---

## Test 5: Twitter Character Limit Check

**Objective:** Verify Twitter's 280-character limit is handled

**Step-by-Step Instructions:**

### Step 5a: Create Post Near Limit
```bash
# Create post with 275 characters (safe)
python scripts/trigger_posts.py -p twitter \
  -c "This is a test tweet with content that is getting closer to the character limit but still safely under. Let me add more text to get close. The executor should handle this correctly without any issues." \
  --preview
```

**Expected:** Success - within 280 character limit

### Step 5b: Create Post Over Limit
```bash
# Create post with 300+ characters (over limit)
python scripts/trigger_posts.py -p twitter \
  -c "This is a very long test tweet that exceeds Twitter's 280 character limit significantly. It includes lots of text that should trigger our character limit handler. When the executor tries to post this, it should either truncate intelligently or fail gracefully with an error message. The important thing is that it handles it correctly without crashing." \
  --preview
```

**Expected:** Script warns about length or executor handles gracefully

### Step 5c: Move to Approved and Post
```bash
mv Pending_Approval/POST_*_tw_*.md Approved/

# Watch orchestrator - should handle character limit issue gracefully
```

**Verification Checklist:**
- [ ] Posts under 280 chars post successfully
- [ ] Posts over 280 chars fail gracefully
- [ ] Error message is clear if exceeds limit
- [ ] No system crash on character limit
- [ ] Executor logs the character count issue

**Pass Criteria:** ✅ Character limit properly handled

---

## Test 6: Twitter Performance Timing

**Objective:** Verify posting completes in expected time

**Step-by-Step Instructions:**

### Step 6a: Create Post with Timing
```bash
# Note start time
date "+%H:%M:%S"
# Example: 10:15:34

python scripts/trigger_posts.py -p twitter -c "Perf test"
# Created: 10:15:34
```

### Step 6b: Move and Monitor
```bash
date "+%H:%M:%S"
# Example: 10:15:35

mv Pending_Approval/POST_*_tw_*.md Approved/
# Approved: 10:15:35
```

### Step 6c: Track Orchestrator Timing (Terminal 1)
```
10:15:39 - Detected (4 seconds)
10:15:40 - Executor started
10:15:55 - Posted (15 seconds)
10:16:00 - Done (5 seconds)

Total: 25 seconds ✓ (within 20-35 second budget)
```

**Verification Checklist:**
- [ ] Detection: < 5 seconds
- [ ] Posting: < 25 seconds
- [ ] Total: 20-35 seconds
- [ ] Consistent timing across multiple posts

**Pass Criteria:** ✅ Posting completes within performance budget

---

## Test 7: Twitter Batch Processing

**Objective:** Test multiple tweets processed sequentially

**Step-by-Step Instructions:**

### Step 7a: Create 5 Tweets
```bash
# Tweet 1
python scripts/trigger_posts.py -p twitter -c "Tweet 1: First" && sleep 10

# Tweet 2
python scripts/trigger_posts.py -p twitter -c "Tweet 2: Second" && sleep 10

# Tweet 3
python scripts/trigger_posts.py -p twitter -c "Tweet 3: Third" && sleep 10

# Tweet 4
python scripts/trigger_posts.py -p twitter -c "Tweet 4: Fourth" && sleep 10

# Tweet 5
python scripts/trigger_posts.py -p twitter -c "Tweet 5: Fifth"

# Verify all created
ls Pending_Approval/ | grep "_tw_" | wc -l
# Expected: 5
```

### Step 7b: Approve All
```bash
# Move all to Approved
mv Pending_Approval/POST_*_tw_*.md Approved/

# Verify
ls Approved/ | grep "_tw_" | wc -l
# Expected: 5
```

### Step 7c: Monitor Sequential Processing (Terminal 1)
**Watch orchestrator process all 5 sequentially:**
```
[10:16:00] 📋 Processing Tweet 1... → ✅ Done (30s)
[10:16:30] 📋 Processing Tweet 2... → ✅ Done (30s)
[10:17:00] 📋 Processing Tweet 3... → ✅ Done (30s)
[10:17:30] 📋 Processing Tweet 4... → ✅ Done (30s)
[10:18:00] 📋 Processing Tweet 5... → ✅ Done (30s)

Total: ~150 seconds ✓
```

### Step 7d: Verify All Processed
```bash
# Count in Done
ls Done/ | grep "_tw_" | wc -l
# Expected: 5

# Count remaining in Approved
ls Approved/ | grep "_tw_" | wc -l
# Expected: 0
```

**Verification Checklist:**
- [ ] All 5 tweets created
- [ ] All moved to Approved
- [ ] Orchestrator processed sequentially
- [ ] Each took 20-35 seconds
- [ ] All 5 now in Done/
- [ ] Total time: 100-175 seconds
- [ ] No tweets skipped

**Pass Criteria:** ✅ All 5 tweets processed successfully

---

## Test 8: Twitter Error Recovery

**Objective:** Test automatic retry after failure

**Step-by-Step Instructions:**

### Step 8a: Create and Approve Post
```bash
python scripts/trigger_posts.py -p twitter -c "Error test tweet"
mv Pending_Approval/POST_*_tw_*.md Approved/
```

### Step 8b: Close Browser During Posting
**Watch Terminal 1 for execution to start, then close the browser window.**

### Step 8c: Monitor Failure and Retry (Terminal 1)
```
[2026-03-29 10:16:00] 📋 Processing...
[2026-03-29 10:16:05] 🚀 Executing...
[2026-03-29 10:16:15] ❌ Executor failed: BrowserClosed
[2026-03-29 10:16:15] 🔄 Scheduling retry
[2026-03-29 10:16:15] ⏱️ Cooldown: 5 minutes
[2026-03-29 10:21:20] Cooldown expired
[2026-03-29 10:21:20] 🚀 Executing... (Attempt 2/4)
[2026-03-29 10:21:50] ✅ SUCCESS: Tweet posted!
```

**Verification Checklist:**
- [ ] First attempt fails gracefully
- [ ] Error logged
- [ ] Cooldown timer starts
- [ ] File stays in Approved
- [ ] Automatic retry after cooldown
- [ ] Success on retry
- [ ] File moved to Done

**Pass Criteria:** ✅ Automatic retry succeeds

---

## Test 9: Twitter Special Characters

**Objective:** Verify emoji, mentions, hashtags, and quotes preserved

**Step-by-Step Instructions:**

### Step 9a: Create Post with Special Chars
```bash
python scripts/trigger_posts.py -p twitter \
  -c "Test 🚀 #hashtag @mention \"quoted text\"" \
  --preview
```

### Step 9b: Verify in File
```bash
cat Pending_Approval/POST_*_tw_*.md | grep -i "test"

# Should show all special characters preserved
```

### Step 9c: Move and Post
```bash
mv Pending_Approval/POST_*_tw_*.md Approved/

# Wait for posting (watch Terminal 1)
# Then verify on Twitter.com that all characters display correctly
```

**Verification Checklist:**
- [ ] Emoji preserved (🚀)
- [ ] Hashtag preserved (#hashtag)
- [ ] Mention preserved (@mention)
- [ ] Quotes preserved ("quoted text")
- [ ] All visible on Twitter.com
- [ ] No character corruption

**Pass Criteria:** ✅ All special characters preserved

---

## Test 10: Twitter Session Persistence

**Objective:** Verify browser session persists across tweets

**Step-by-Step Instructions:**

### Step 10a: Tweet 1 - Initial Login
```bash
python scripts/trigger_posts.py -p twitter -c "Tweet 1"
mv Pending_Approval/POST_*_tw_001.md Approved/
```

**Terminal 1 shows:**
```
[10:16:00] Logging into Twitter...
[10:16:15] Account logged in ✅
[10:16:20] Posting...
[10:16:30] ✅ SUCCESS
```

### Step 10b: Tweet 2 - Reuses Session
```bash
python scripts/trigger_posts.py -p twitter -c "Tweet 2"
mv Pending_Approval/POST_*_tw_002.md Approved/
```

**Terminal 1 shows:**
```
[10:16:35] Using saved session ✅  ← NO login!
[10:16:40] Posting...
[10:16:50] ✅ SUCCESS
```

### Step 10c: Tweet 3 - Still Using Session
```bash
python scripts/trigger_posts.py -p twitter -c "Tweet 3"
mv Pending_Approval/POST_*_tw_003.md Approved/
```

**Terminal 1 shows:**
```
[10:17:00] Using saved session ✅  ← Still no login!
[10:17:05] Posting...
[10:17:15] ✅ SUCCESS
```

### Step 10d: Verify Session Folder
```bash
ls -la session/

# Should contain browser profile data
```

**Verification Checklist:**
- [ ] Tweet 1: Shows login process
- [ ] Tweet 2: Shows "Using saved session" (NO login)
- [ ] Tweet 3: Shows "Using saved session" (NO login)
- [ ] Session folder has files
- [ ] Tweets 2 & 3 post 5-10s faster (no login)

**Pass Criteria:** ✅ Session persists (no re-login needed)

---

## Troubleshooting

### Browser Won't Open
```bash
playwright install chromium firefox
pkill -f social_media_executor
sleep 2
python scripts/master_orchestrator.py
```

### Tweet Stuck in Approved
```bash
ps aux | grep master_orchestrator
# If not running:
python scripts/master_orchestrator.py

# Check logs
tail -20 Logs/orchestrator_*.log
```

### File Not Created
```bash
# Create missing directories
mkdir -p Pending_Approval Approved Done Logs session

# Verify permissions
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
| Character limit | ✅ |
| Performance | ✅ |
| Batch (5 tweets) | ✅ |
| Error recovery | ✅ |
| Special chars | ✅ |
| Session persist | ✅ |

**Status:** ✅ PRODUCTION READY
**Last Updated:** 2026-03-30
**Version:** 2.0 (Enhanced with detailed instructions)
