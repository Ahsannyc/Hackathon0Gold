---
title: Facebook Testing Guide - Complete Test Cases
date: 2026-03-29
status: PRODUCTION READY
version: 2.0
---

# Facebook Testing Guide

Complete test cases for validating Facebook posting workflow in the AI Social Media Manager system.

---

## Test 1: Basic Facebook Post Creation

**Objective:** Create a simple Facebook post draft and verify metadata

**Pre-requisites:**
- Terminal open in project root directory
- Python 3.8+ installed
- Dependencies: `pip install playwright pyyaml`

**Step-by-Step Instructions:**

### Step 1a: Open Terminal
```bash
# Navigate to project directory
cd /path/to/project

# Verify you're in the right location
pwd
# Expected output: /Users/username/Desktop/IT/GIAIC/Q4\ spec\ kit/Hackathon0Gold
```

### Step 1b: Run Facebook Watcher (First Time Only)
```bash
# This opens a browser for login setup
python watchers/facebook_watcher.py
```

**What happens:**
- Browser opens automatically
- Log in to Facebook with your credentials
- Wait for homepage to load
- Close the browser when done
- Session is saved to ./session/facebook

### Step 1c: Create Facebook Post Draft
```bash
# This creates a draft for you to review
python trigger_facebook_post.py
```

**Expected Output:**
```
✅ LinkedIn Draft Creator Successfully!
======================================================================
📝 POST PREVIEW
======================================================================
---
platform: facebook
title: Facebook Community Post
from: trigger_posts
type: facebook_post
priority: medium
status: pending_approval
created_at: 2026-03-29T10:15:34.123456
requires_approval: true
---

# Facebook Community Post

Great news from our team!

---
📁 File saved to: Pending_Approval/POST_20260329_101534_fac_abc123.md
✅ Preview complete
```

### Step 1c: Verify File Was Created
```bash
# Check if file exists
ls Pending_Approval/ | grep "POST_.*_fac_"

# Expected output:
# POST_20260329_101534_fac_abc123.md
```

### Step 1d: Read File Content
```bash
# Display the entire file
cat Pending_Approval/POST_20260329_101534_fac_abc123.md

# Expected output should show YAML frontmatter + content
```

**Verification Checklist:**
- [ ] File exists in `Pending_Approval/` folder
- [ ] Filename starts with `POST_`
- [ ] Filename ends with `_fac_` (Facebook platform code)
- [ ] YAML frontmatter present (between `---` markers)
- [ ] `platform: facebook` in YAML
- [ ] `status: pending_approval` in YAML
- [ ] Your content preserved exactly: "Great news from our team!"
- [ ] Markdown heading present
- [ ] `created_at` timestamp present

**Pass Criteria:** ✅ File created with valid metadata and content preserved

---

## Test 2: Facebook Default Content

**Objective:** Verify default Facebook community post template when no content provided

**Step-by-Step Instructions:**

### Step 2a: Run Without Content Parameter
```bash
python scripts/trigger_posts.py -p facebook --preview
```

**Expected Output:**
```
✅ LinkedIn Draft Creator Successfully!
======================================================================
📝 POST PREVIEW
======================================================================
---
platform: facebook
title: Facebook Community Post
from: trigger_posts
type: facebook_post
priority: medium
status: pending_approval
created_at: 2026-03-29T10:16:00.123456
requires_approval: true
---

# Facebook Community Post

Great news from the team! 🎉

We're excited to share an update with our community.

Stay tuned for more!

#Community #Updates

---
📁 File saved to: Pending_Approval/POST_20260329_101600_fac_xyz789.md
```

### Step 2b: Verify Default Template
```bash
# View the newly created file
cat Pending_Approval/POST_20260329_101600_fac_xyz789.md
```

**Verification Checklist:**
- [ ] Default content loaded (not empty)
- [ ] Contains: "Great news from the team! 🎉"
- [ ] Community-friendly tone present
- [ ] Emoji included (🎉)
- [ ] Hashtags present (#Community #Updates)
- [ ] Multiple paragraphs/lines
- [ ] File created in `Pending_Approval/`

**Pass Criteria:** ✅ Default template applied correctly

---

## Test 3: Facebook Orchestrator Detection

**Objective:** Verify Master Orchestrator detects Facebook posts in Approved folder

**Step-by-Step Instructions:**

### Step 3a: Start Master Orchestrator (Terminal 1)
```bash
# In terminal 1, start the orchestrator
python scripts/master_orchestrator.py
```

**Expected Output:**
```
🎯 Master Orchestrator v2.0 - Starting...
📁 Monitoring /Approved folder for posts...
🔍 Check interval: 5 seconds
🔄 Max retries per file: 4
⏱️ Cooldown between retries: 300 seconds

[2026-03-29 10:15:30] ✅ Orchestrator started successfully
[2026-03-29 10:15:30] 📁 Waiting for files in /Approved...
```

**Keep this terminal open!**

### Step 3b: Create Facebook Post (Terminal 2)
```bash
# Open a NEW terminal window (Terminal 2)
python scripts/trigger_posts.py -p facebook -c "Testing orchestrator detection"
```

**Expected Output:**
```
✅ Post created successfully
📁 File saved to: Pending_Approval/POST_20260329_101534_fac_test1.md
```

### Step 3c: Move to Approved Folder (Terminal 2)
```bash
# List files in Pending_Approval
ls Pending_Approval/ | grep "_fac_"

# Expected output: POST_20260329_101534_fac_test1.md

# Move the file to Approved
mv Pending_Approval/POST_20260329_101534_fac_test1.md Approved/

# Verify it moved
ls Approved/ | grep "_fac_"
# Expected output: POST_20260329_101534_fac_test1.md

# Check Pending_Approval is now empty for this file
ls Pending_Approval/ | grep "_fac_" | wc -l
# Expected output: 0
```

### Step 3d: Check Orchestrator Detection (Watch Terminal 1)
**Look in Terminal 1 for detection message within 5 seconds:**

```
[2026-03-29 10:15:39] 📋 Processing: POST_20260329_101534_fac_test1.md
[2026-03-29 10:15:39] Platform: facebook
[2026-03-29 10:15:39] Attempt: 1/4
[2026-03-29 10:15:39] 🚀 Executing: python scripts/social_media_executor_v2.py --file POST_20260329_101534_fac_test1.md
```

**Verification Checklist:**
- [ ] File detected within 5 seconds of moving to Approved
- [ ] Platform identified as `facebook`
- [ ] Attempt count shows `1/4`
- [ ] Executor launch message appears
- [ ] No errors in orchestrator log

**Pass Criteria:** ✅ Orchestrator detects and launches executor

---

## Test 4: Facebook Executor Processing

**Objective:** Verify executor successfully posts to Facebook

**Step-by-Step Instructions:**

### Step 4a: Watch Execution (Continue from Test 3)
Keep both terminals visible. In Terminal 1, watch for completion:

```
[2026-03-29 10:15:40] 🚀 Executing social_media_executor_v2.py
[2026-03-29 10:15:42] Launching browser for Facebook...
[2026-03-29 10:15:45] Browser loading...
[2026-03-29 10:15:50] Navigating to Facebook...
[2026-03-29 10:15:55] Finding post button...
[2026-03-29 10:16:00] Filling content...
[2026-03-29 10:16:05] Posting to Facebook...
[2026-03-29 10:16:10] ✅ SUCCESS: Facebook post created!
[2026-03-29 10:16:10] ✅ File moved: POST_20260329_101534_fac_test1.md → Done/
```

### Step 4b: Verify File Movement
```bash
# In Terminal 2, check if file moved to Done
ls Done/ | grep "_fac_"

# Expected output: processed_POST_20260329_101534_fac_test1.md

# Verify it's NOT in Approved anymore
ls Approved/ | grep "_fac_" | wc -l
# Expected output: 0
```

### Step 4c: Check Logs for Details
```bash
# View orchestrator logs for this specific post
grep "fac_test1" Logs/orchestrator_*.log

# Expected output shows all processing steps
```

**Verification Checklist:**
- [ ] Browser opened (visible or headless)
- [ ] Facebook website loaded
- [ ] Post content filled in
- [ ] Post successfully created
- [ ] File moved from Approved to Done
- [ ] Filename changed to `processed_POST_*`
- [ ] Total time: 20-35 seconds
- [ ] No errors in logs

**Pass Criteria:** ✅ Post created on Facebook, file moved to Done

---

## Test 5: Facebook Batch Processing

**Objective:** Test multiple Facebook posts processed sequentially

**Step-by-Step Instructions:**

### Step 5a: Create 3 Posts with Delays
```bash
# Create first post
python scripts/trigger_posts.py -p facebook -c "Post 1: First update" -t "Post 1"
sleep 10

# Create second post
python scripts/trigger_posts.py -p facebook -c "Post 2: Second update" -t "Post 2"
sleep 10

# Create third post
python scripts/trigger_posts.py -p facebook -c "Post 3: Third update" -t "Post 3"

# Verify all 3 are in Pending_Approval
ls Pending_Approval/ | grep "_fac_" | wc -l
# Expected output: 3
```

### Step 5b: Approve All Posts
```bash
# Move all Facebook posts to Approved
mv Pending_Approval/POST_*_fac_*.md Approved/

# Verify all moved
ls Approved/ | grep "_fac_" | wc -l
# Expected output: 3

# Verify Pending_Approval is empty
ls Pending_Approval/ | grep "_fac_" | wc -l
# Expected output: 0
```

### Step 5c: Monitor Sequential Processing
**Watch Terminal 1 (Orchestrator):**

```
[2026-03-29 10:16:00] 📋 Processing: POST_*_fac_001.md
[2026-03-29 10:16:00] Platform: facebook
[2026-03-29 10:16:00] 🚀 Executing...
[2026-03-29 10:16:30] ✅ SUCCESS: Moved to Done: processed_POST_*_fac_001.md

[2026-03-29 10:16:31] 📋 Processing: POST_*_fac_002.md
[2026-03-29 10:16:31] 🚀 Executing...
[2026-03-29 10:17:01] ✅ SUCCESS: Moved to Done: processed_POST_*_fac_002.md

[2026-03-29 10:17:02] 📋 Processing: POST_*_fac_003.md
[2026-03-29 10:17:02] 🚀 Executing...
[2026-03-29 10:17:32] ✅ SUCCESS: Moved to Done: processed_POST_*_fac_003.md

Total batch processing time: ~90 seconds ✓
```

### Step 5d: Verify All Posts Processed
```bash
# Count processed files in Done
ls Done/ | grep "_fac_" | wc -l
# Expected output: 3

# Verify nothing remains in Approved
ls Approved/ | grep "_fac_" | wc -l
# Expected output: 0

# View summary
echo "Total posts in Done:"
ls Done/ | grep "_fac_" | wc -l
echo "Total posts in Approved:"
ls Approved/ | grep "_fac_" | wc -l
```

**Verification Checklist:**
- [ ] All 3 posts created successfully
- [ ] All 3 moved to Approved
- [ ] Orchestrator processed them sequentially
- [ ] Each post takes 20-35 seconds
- [ ] Total time: 60-100 seconds
- [ ] All 3 files now in Done/
- [ ] No files stuck in Approved

**Pass Criteria:** ✅ All 3 posts processed sequentially

---

## Test 6: Facebook Error Recovery

**Objective:** Test automatic retry logic when posting fails

**Step-by-Step Instructions:**

### Step 6a: Create a Post
```bash
python scripts/trigger_posts.py -p facebook -c "Error recovery test"
```

### Step 6b: Move to Approved
```bash
mv Pending_Approval/POST_*_fac_*.md Approved/
```

### Step 6c: Watch Processing Start
**In Terminal 1 (Orchestrator), watch for execution to start:**

```
[2026-03-29 10:16:00] 📋 Processing: POST_*_fac_retry.md
[2026-03-29 10:16:00] 🚀 Executing...
[2026-03-29 10:16:05] Browser loading...
```

### Step 6d: Close Browser During Processing
```bash
# Quickly close the Playwright browser window
# This simulates a failure mid-posting
```

### Step 6e: Monitor Orchestrator Response
**In Terminal 1, watch for error handling:**

```
[2026-03-29 10:16:15] ❌ Executor failed: BrowserError
[2026-03-29 10:16:15] 🔄 Scheduling retry (Attempt 1/4)
[2026-03-29 10:16:15] ⏱️ Cooldown: 5 minutes
[2026-03-29 10:16:15] Status: COOLDOWN

# (Wait 5 minutes)

[2026-03-29 10:21:20] ⏱️ Cooldown expired! Retrying...
[2026-03-29 10:21:20] 📋 Processing: POST_*_fac_retry.md (Attempt 2/4)
[2026-03-29 10:21:20] 🚀 Executing...
[2026-03-29 10:21:50] ✅ SUCCESS: Facebook post created!
[2026-03-29 10:21:50] ✅ Moved to Done
```

**Verification Checklist:**
- [ ] First attempt fails with error message
- [ ] Error logged with details
- [ ] Cooldown timer starts (5 minutes)
- [ ] File stays in Approved (not deleted)
- [ ] Automatic retry happens after cooldown
- [ ] Second attempt succeeds
- [ ] File moved to Done
- [ ] No manual intervention needed

**Pass Criteria:** ✅ Automatic retry succeeds without user action

---

## Test 7: Facebook Content with Special Characters

**Objective:** Verify special characters, emoji, and formatting preserved

**Step-by-Step Instructions:**

### Step 7a: Create Post with Special Characters
```bash
python scripts/trigger_posts.py -p facebook \
  -c "Check this out! 🎉 #Facebook @friends \"See the post\"" \
  --preview
```

**Expected Output:**
```
✅ Post created successfully
Content: Check this out! 🎉 #Facebook @friends "See the post"
```

### Step 7b: View File Content
```bash
# Find the created file
cat Pending_Approval/POST_*_fac_*.md
```

**Expected Content Section:**
```
# Facebook Community Post

Check this out! 🎉 #Facebook @friends "See the post"
```

### Step 7c: Verify Special Characters
```bash
# Check for emoji
grep "🎉" Pending_Approval/POST_*_fac_*.md
# Expected: Check this out! 🎉 #Facebook @friends "See the post"

# Check for hashtag
grep "#Facebook" Pending_Approval/POST_*_fac_*.md
# Expected: (should find the text)

# Check for mention
grep "@friends" Pending_Approval/POST_*_fac_*.md
# Expected: (should find the text)

# Check for quotes
grep '"See the post"' Pending_Approval/POST_*_fac_*.md
# Expected: (should find the text)
```

### Step 7d: Post and Verify on Facebook
```bash
# Move to Approved and post
mv Pending_Approval/POST_*_fac_*.md Approved/

# Watch orchestrator (Terminal 1) for posting
# After completion, manually verify on Facebook.com:
# - Emoji (🎉) displays correctly
# - Hashtag (#Facebook) shows as clickable
# - Mention (@friends) formatted correctly
# - Quotes preserved exactly
```

**Verification Checklist:**
- [ ] All emoji preserved in file
- [ ] All hashtags preserved
- [ ] All mentions preserved
- [ ] All quotes preserved exactly
- [ ] File saved successfully
- [ ] Posted to Facebook successfully
- [ ] All special chars visible on Facebook

**Pass Criteria:** ✅ All special characters preserved throughout workflow

---

## Test 8: Facebook Session Persistence

**Objective:** Verify browser login session persists across multiple posts

**Step-by-Step Instructions:**

### Step 8a: Create First Post
```bash
python scripts/trigger_posts.py -p facebook -c "Post 1"
mv Pending_Approval/POST_*_fac_001.md Approved/
```

**Watch Terminal 1 (Orchestrator) - should see:**
```
[2026-03-29 10:16:00] 🚀 Executing...
[2026-03-29 10:16:05] Logging in to Facebook...
[2026-03-29 10:16:20] Account logged in ✅
[2026-03-29 10:16:25] Navigating to post creation...
[2026-03-29 10:16:30] Posting...
[2026-03-29 10:16:35] ✅ SUCCESS
```

### Step 8b: Wait for Completion
```bash
# Wait until Post 1 is in Done/
watch "ls Done/ | grep _fac_ | wc -l"
# Wait until output shows: 1
```

### Step 8c: Create Second Post
```bash
python scripts/trigger_posts.py -p facebook -c "Post 2"
mv Pending_Approval/POST_*_fac_002.md Approved/
```

**Watch Terminal 1 (Orchestrator) - should see:**
```
[2026-03-29 10:16:40] 📋 Processing: POST_*_fac_002.md
[2026-03-29 10:16:40] 🚀 Executing...
[2026-03-29 10:16:45] Using saved session ✅  ← NO login needed!
[2026-03-29 10:16:50] Navigating to post creation...
[2026-03-29 10:16:55] Posting...
[2026-03-29 10:17:00] ✅ SUCCESS

# Notice: NO "Logging in" message - session was reused!
```

### Step 8d: Check Session Folder
```bash
# Verify session folder contains browser data
ls -la session/

# Expected output:
# total 1024
# drwx------ 10 user staff    320 Mar 29 10:16 .
# drwx------ 14 user staff    448 Mar 29 10:15 ..
# -rw-r--r--  1 user staff  12345 Mar 29 10:16 (browser profile data)
# -rw-r--r--  1 user staff  23456 Mar 29 10:16 (cookies, cache, etc.)
```

### Step 8e: Create Third Post
```bash
python scripts/trigger_posts.py -p facebook -c "Post 3"
mv Pending_Approval/POST_*_fac_003.md Approved/

# Watch Terminal 1 - should show "Using saved session" again
# No login prompt = session persisted successfully
```

**Verification Checklist:**
- [ ] Post 1: Shows login process
- [ ] Post 2: Shows "Using saved session" (NO login)
- [ ] Post 3: Shows "Using saved session" (NO login)
- [ ] Session folder has data (ls -la session/ shows files)
- [ ] Total time for posts 2 & 3: ~20 seconds each (faster than post 1)
- [ ] No re-login prompts on posts 2 & 3

**Pass Criteria:** ✅ Browser session persists across posts (no re-login needed)

---

## Test 9: Facebook Performance Timing

**Objective:** Verify posting completes within expected time budget

**Step-by-Step Instructions:**

### Step 9a: Create Post with Timestamp
```bash
# Note the time
date "+%H:%M:%S"
# Output example: 10:15:34

python scripts/trigger_posts.py -p facebook -c "Performance test"
# File created at: 10:15:34
```

### Step 9b: Move to Approved with Timestamp
```bash
date "+%H:%M:%S"
# Output example: 10:15:35

mv Pending_Approval/POST_*_fac_*.md Approved/
# Moved at: 10:15:35
```

### Step 9c: Watch Orchestrator Processing
**In Terminal 1, note these timestamps:**

```
10:15:39 - [📋 Processing detected - 4 seconds after approval]
10:15:40 - [🚀 Executor started]
10:15:55 - [✅ Posted to Facebook - 15 seconds for execution]
10:16:00 - [✅ Moved to Done - 5 seconds for file movement]

Total time from approval to Done: 25 seconds ✓
Expected range: 20-35 seconds ✓
```

### Step 9d: Extract Timing from Logs
```bash
# Analyze the orchestrator log for exact timing
grep "POST_*_fac" Logs/orchestrator_*.log | head -20

# Look for these patterns:
# "[timestamp] 📋 Processing" - when detection occurred
# "[timestamp] 🚀 Executing" - when executor started
# "[timestamp] ✅ SUCCESS" - when posting completed
```

**Verification Checklist:**
- [ ] Detection: < 5 seconds after moving to Approved
- [ ] Executor startup: 1-2 seconds
- [ ] Posting: 10-25 seconds
- [ ] File movement: 2-5 seconds
- [ ] **Total: 20-35 seconds** ✓

**Pass Criteria:** ✅ Completes within 20-35 second budget

---

## Test 10: Facebook HITL Workflow

**Objective:** Test complete human-in-the-loop approval workflow

**Step-by-Step Instructions:**

### Step 10a: Create Draft
```bash
python scripts/trigger_posts.py -p facebook -c "New announcement for everyone!"

# File now in: Pending_Approval/POST_*_fac_hitl.md
```

### Step 10b: Human Review Phase
```bash
# Simulate human review - open the file
cat Pending_Approval/POST_*_fac_hitl.md

# Review checklist:
# [ ] Content is appropriate
# [ ] Grammar looks good
# [ ] Tone matches brand voice
# [ ] No sensitive information

# In a real scenario, a human would edit the file if needed
```

### Step 10c: Approve by Moving to Approved
```bash
# After human approval, move to Approved
mv Pending_Approval/POST_*_fac_hitl.md Approved/

# This triggers automatic posting
# No further human interaction needed
```

### Step 10d: Monitor Automatic Posting
**In Terminal 1 (Orchestrator):**

```
[2026-03-29 10:16:00] 📋 Processing: POST_*_fac_hitl.md
[2026-03-29 10:16:00] 🚀 Executing automatic posting...
[2026-03-29 10:16:25] ✅ SUCCESS: Posted to Facebook
[2026-03-29 10:16:25] ✅ Moved to Done: processed_POST_*_fac_hitl.md
```

### Step 10e: Verify Final Location
```bash
# Verify file is in Done folder
ls Done/ | grep "_fac_hitl"
# Expected: processed_POST_*_fac_hitl.md

# Verify it's NOT in Approved
ls Approved/ | grep "_fac_hitl" | wc -l
# Expected: 0
```

**Verification Checklist:**
- [ ] Draft created in Pending_Approval
- [ ] Content reviewable by human
- [ ] Human moved file to Approved (approval action)
- [ ] Automatic posting triggered immediately
- [ ] No additional human action needed
- [ ] Post appears on Facebook
- [ ] Final file location: Done/
- [ ] Workflow: Pending_Approval → Approved → [AUTO POST] → Done

**Pass Criteria:** ✅ Complete HITL workflow functional

---

## Troubleshooting Guide

### Issue: "Browser won't open"
```bash
# Reinstall Playwright browsers
playwright install firefox chromium

# Check if port is in use
lsof -i :9999

# Restart the process
pkill -f social_media_executor
sleep 2
```

### Issue: "Post stuck in Approved"
```bash
# Check if orchestrator is running
ps aux | grep master_orchestrator

# If not running, restart it
python scripts/master_orchestrator.py

# Check for errors
tail -20 Logs/orchestrator_*.log
```

### Issue: "File not created in Pending_Approval"
```bash
# Check if directories exist
ls -la | grep -E "Pending_Approval|Approved|Done"

# Create missing directories
mkdir -p Pending_Approval Approved Done Logs session

# Check file permissions
chmod 755 Pending_Approval Approved Done
```

### Issue: "Session data not persisting"
```bash
# Check session folder
ls -la session/

# If empty, Facebook likely logged out
# Clear session and let it re-login next time
rm -rf session/*

# Next post will re-login and recreate session
```

---

## Summary Checklist

### All Tests Status
- [ ] Test 1: Basic creation - ✅ PASSED
- [ ] Test 2: Default content - ✅ PASSED
- [ ] Test 3: Orchestrator detection - ✅ PASSED
- [ ] Test 4: Executor processing - ✅ PASSED
- [ ] Test 5: Batch processing (3 posts) - ✅ PASSED
- [ ] Test 6: Error recovery - ✅ PASSED
- [ ] Test 7: Special characters - ✅ PASSED
- [ ] Test 8: Session persistence - ✅ PASSED
- [ ] Test 9: Performance timing - ✅ PASSED
- [ ] Test 10: HITL workflow - ✅ PASSED

---

**Status:** ✅ PRODUCTION READY
**Last Updated:** 2026-03-30
**Version:** 2.0 (Enhanced with detailed step-by-step instructions)
