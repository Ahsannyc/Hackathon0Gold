---
title: LinkedIn Testing Guide - Complete Test Cases
date: 2026-03-29
status: PRODUCTION READY
version: 2.0
---

# LinkedIn Testing Guide

Complete test cases for validating LinkedIn posting workflow in the AI Social Media Manager system.

---

## Test 1: Basic LinkedIn Post Creation (Login Setup)

**Objective:** Log in to LinkedIn and set up session for automation

**Step-by-Step Instructions:**

### Step 1a: Open Terminal
```bash
# Navigate to project directory
cd /path/to/project

# Verify you're in the right location
pwd
```

### Step 1b: Run LinkedIn Watcher (First Time Only)
```bash
# This opens a real browser - log in manually once
python watchers/linkedin_watcher.py
```

**What happens:**
- A browser window opens automatically
- Navigate to LinkedIn and log in with your credentials
- Wait for your homepage to load completely
- Close the browser when done

**Expected Output:**
```
🔐 LinkedIn watcher starting...
🌐 Opening browser for LinkedIn login...
✅ Login session saved to ./session/linkedin
```

### Step 1c: Verify Session Was Created
```bash
# Check if session folder exists
ls -la session/

# Expected: You should see LinkedIn session files
```

### Step 1d: Create Your First LinkedIn Post Draft
```bash
# This creates a draft for you to review
python trigger_linkedin_post.py
```

**Expected Output:**
```
✅ LinkedIn Draft Creator Successfully!
======================================================================
📝 POST PREVIEW
======================================================================
---
platform: linkedin
title: LinkedIn Professional Post
from: trigger_posts
type: linkedin_post
priority: medium
status: pending_approval
created_at: 2026-03-29T10:15:34.123456
requires_approval: true
---

# LinkedIn Professional Post

Excited to share insights from our latest project! 🚀

---
📁 File saved to: Pending_Approval/POST_LINKEDIN_20260329_101534.md
✅ Preview complete
```

**Verification Checklist:**
- [ ] File exists in `Pending_Approval/` folder
- [ ] Filename starts with `POST_`
- [ ] Filename ends with `_lin_` (LinkedIn platform code)
- [ ] YAML frontmatter present (between `---` markers)
- [ ] `platform: linkedin` in YAML
- [ ] `status: pending_approval` in YAML
- [ ] Your content preserved exactly
- [ ] Markdown heading present
- [ ] `created_at` timestamp present

**Pass Criteria:** ✅ File created with valid metadata and content preserved

---

## Test 2: Create and Approve LinkedIn Post

**Objective:** Create a LinkedIn post draft and approve it for publishing

**Step-by-Step Instructions:**

### Step 2a: Create LinkedIn Post Draft
```bash
# Generate a new post draft
python trigger_linkedin_post.py
```

**Expected Output:**
```
✅ LinkedIn Draft Created Successfully!
📁 File saved to: Pending_Approval/POST_LINKEDIN_20260329_101600.md
```

### Step 2b: Open Pending_Approval Folder
```bash
# List files in Pending_Approval
ls Pending_Approval/

# You should see: POST_LINKEDIN_*
```

### Step 2c: Move File to Approved (Your Approval Action)
```bash
# Find and move the LinkedIn post file
mv Pending_Approval/POST_LINKEDIN_* Approved/

# Verify it moved
ls Approved/ | grep POST_LINKEDIN
# Expected: POST_LINKEDIN_20260329_101600.md
```

### Step 2d: Verify File is Ready for Automation
```bash
# Check that Approved folder has the file
ls Approved/ | grep POST_LINKEDIN

# Verify it's NOT in Pending_Approval anymore
ls Pending_Approval/ | grep POST_LINKEDIN | wc -l
# Expected: 0
```

**Verification Checklist:**
- [ ] File exists in `Pending_Approval/`
- [ ] Custom title in YAML metadata: "My Custom Title"
- [ ] Custom title in markdown heading: "# My Custom Title"
- [ ] Content preserved exactly: "Custom content here"
- [ ] File created with correct naming

**Pass Criteria:** ✅ Custom title applied correctly in both YAML and heading

---

## Test 3: Watch Automation Post to LinkedIn

**Objective:** Watch the orchestrator automatically post to LinkedIn

**Step-by-Step Instructions:**

### Step 3a: Start Master Orchestrator (Terminal 1)
```bash
# In first terminal, start the orchestrator
python master_orchestrator.py
```

**Expected Output:**
```
🎯 Master Orchestrator v2.0 - Starting...
📁 Monitoring /Approved folder for posts...
✅ Orchestrator ready and waiting...
```

**Expected Output:**
```
✅ LinkedIn Draft Creator Successfully!
======================================================================
📝 POST PREVIEW
======================================================================
---
platform: linkedin
title: LinkedIn Professional Post
---

# LinkedIn Professional Post

Excited to share insights from our latest project! 🚀

Key takeaways:
• Innovation drives results
• Collaboration is key
• Continuous learning matters

#Leadership #Professional #Growth

---
📁 File saved to: Pending_Approval/POST_20260329_101600_lin_xyz789.md
```

### Step 3b: Verify Default Template
```bash
# View the newly created file
cat Pending_Approval/POST_20260329_101600_lin_xyz789.md

# Should show the default professional template
```

**Verification Checklist:**
- [ ] Default content loaded (not empty)
- [ ] Contains: "Excited to share insights from our latest project! 🚀"
- [ ] Professional tone present
- [ ] Emoji included (🚀)
- [ ] Hashtags present (#Leadership #Professional #Growth)
- [ ] Multiple paragraphs
- [ ] Key takeaways listed

**Pass Criteria:** ✅ Default template applied correctly

---

## Test 4: LinkedIn File Format Validation

**Objective:** Verify YAML frontmatter is valid and contains all required fields

**Step-by-Step Instructions:**

### Step 4a: Create a LinkedIn Post
```bash
# Create a test post
python scripts/trigger_posts.py -p linkedin -c "Format validation test" -t "Test Title"
```

### Step 4b: Read the File
```bash
# List the created file
ls Pending_Approval/ | grep "_lin_" | tail -1
# Expected: POST_20260329_101534_lin_*.md

# Store filename in variable for easy access
FILENAME=$(ls Pending_Approval/ | grep "_lin_" | tail -1)
echo $FILENAME
```

### Step 4c: Extract and Verify YAML Section
```bash
# Display the entire file to see YAML
cat Pending_Approval/$FILENAME

# Expected format:
# ---
# platform: linkedin
# title: Test Title
# from: trigger_posts
# type: linkedin_post
# priority: medium
# status: pending_approval
# created_at: 2026-03-29T10:15:34.123456
# requires_approval: true
# ---
```

### Step 4d: Verify Each Required Field
```bash
# Check platform field
grep "^platform:" Pending_Approval/$FILENAME
# Expected output: platform: linkedin

# Check title field
grep "^title:" Pending_Approval/$FILENAME
# Expected output: title: Test Title

# Check type field
grep "^type:" Pending_Approval/$FILENAME
# Expected output: type: linkedin_post

# Check status field
grep "^status:" Pending_Approval/$FILENAME
# Expected output: status: pending_approval

# Check all required fields are present
echo "Checking all required fields..."
for field in "platform:" "title:" "from:" "type:" "priority:" "status:" "created_at:" "requires_approval:"; do
  if grep -q "^$field" Pending_Approval/$FILENAME; then
    echo "✓ $field present"
  else
    echo "✗ $field MISSING"
  fi
done
```

**Verification Checklist:**
- [ ] YAML section starts with `---`
- [ ] YAML section ends with `---`
- [ ] `platform: linkedin` present
- [ ] `title:` present with value
- [ ] `from: trigger_posts` present
- [ ] `type: linkedin_post` present
- [ ] `priority: medium` present
- [ ] `status: pending_approval` present
- [ ] `created_at:` present with ISO timestamp
- [ ] `requires_approval: true` present

**Pass Criteria:** ✅ All required YAML fields present and valid

---

## Test 5: LinkedIn Orchestrator Detection

**Objective:** Verify Master Orchestrator detects LinkedIn posts in Approved folder

**Step-by-Step Instructions:**

### Step 5a: Start Orchestrator (Terminal 1)
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

### Step 5b: Create LinkedIn Post (Terminal 2)
```bash
# Open a NEW terminal window (Terminal 2)
python scripts/trigger_posts.py -p linkedin -c "Testing orchestrator detection"
```

**Expected Output:**
```
✅ Post created successfully
📁 File saved to: Pending_Approval/POST_20260329_101534_lin_test1.md
```

### Step 5c: Move to Approved Folder (Terminal 2)
```bash
# List files in Pending_Approval
ls Pending_Approval/ | grep "_lin_"
# Expected output: POST_20260329_101534_lin_test1.md

# Move the file to Approved
mv Pending_Approval/POST_20260329_101534_lin_test1.md Approved/

# Verify it moved
ls Approved/ | grep "_lin_"
# Expected output: POST_20260329_101534_lin_test1.md

# Check Pending_Approval is now empty for this file
ls Pending_Approval/ | grep "_lin_" | wc -l
# Expected output: 0
```

### Step 5d: Check Orchestrator Detection (Watch Terminal 1)
**Look in Terminal 1 for detection message within 5 seconds:**

```
[2026-03-29 10:15:39] 📋 Processing: POST_20260329_101534_lin_test1.md
[2026-03-29 10:15:39] Platform: linkedin
[2026-03-29 10:15:39] Attempt: 1/4
[2026-03-29 10:15:39] 🚀 Executing: python scripts/social_media_executor_v2.py --file POST_20260329_101534_lin_test1.md
```

**Verification Checklist:**
- [ ] File detected within 5 seconds of moving to Approved
- [ ] Platform identified as `linkedin`
- [ ] Attempt count shows `1/4`
- [ ] Executor launch message appears
- [ ] No errors in orchestrator log

**Pass Criteria:** ✅ Orchestrator detects and launches executor

---

## Test 6: LinkedIn Executor Processing

**Objective:** Verify executor successfully posts to LinkedIn

**Step-by-Step Instructions:**

### Step 6a: Watch Execution (Terminal 1)
**In Terminal 1 (Orchestrator), watch for completion message:**

```
[2026-03-29 10:15:40] 🚀 Executing social_media_executor_v2.py
[2026-03-29 10:15:45] Launching browser for LinkedIn...
[2026-03-29 10:15:55] Finding "Start a post" button...
[2026-03-29 10:16:00] Navigating to post creation...
[2026-03-29 10:16:05] Filling content area...
[2026-03-29 10:16:10] Clicking post button...
[2026-03-29 10:16:15] ✅ SUCCESS: LinkedIn post created!
[2026-03-29 10:16:15] ✅ File moved: POST_* → Done/processed_POST_*
```

### Step 6b: Verify File Movement (Terminal 2)
```bash
# Check if file moved to Done folder
ls Done/ | grep "_lin_"
# Expected output: processed_POST_20260329_101534_lin_*.md

# Verify original filename doesn't exist in Approved
ls Approved/ | grep "_lin_" | wc -l
# Expected output: 0 (none should be there)

# Verify the processed file is in Done
ls Done/ | grep "processed_POST.*_lin_" | wc -l
# Expected output: 1 (should be exactly 1)
```

### Step 6c: Check Timing
```bash
# View the orchestrator log to see execution timing
grep "lin_" Logs/orchestrator_*.log | grep -E "Processing|SUCCESS"

# Expected output should show timestamps like:
# [2026-03-29 10:15:40] 📋 Processing: POST_*.md
# [2026-03-29 10:16:15] ✅ SUCCESS
```

### Step 6d: Verify in LinkedIn UI
```bash
# Manual verification:
# 1. Go to LinkedIn.com
# 2. Check your profile/posts
# 3. Verify the post appears with correct content
# 4. Verify timestamp shows recent post
```

**Verification Checklist:**
- [ ] Browser opened (visible or headless)
- [ ] LinkedIn loaded successfully
- [ ] Login completed without errors
- [ ] Post creation form displayed
- [ ] Content filled correctly
- [ ] Post button clicked
- [ ] File moved from Approved to Done
- [ ] Filename changed from `POST_*` to `processed_POST_*`
- [ ] Total execution time: 20-35 seconds
- [ ] No errors in orchestrator logs
- [ ] Post visible on LinkedIn.com

**Pass Criteria:** ✅ Post successfully created on LinkedIn

---

## Test 7: LinkedIn Batch Processing

**Objective:** Test multiple LinkedIn posts processed sequentially

**Step-by-Step Instructions:**

### Step 7a: Create 3 LinkedIn Posts with Delays
```bash
# Create first post
python scripts/trigger_posts.py -p linkedin -c "Post 1: First update" -t "Post 1" --preview
# Wait 10 seconds
sleep 10

# Create second post
python scripts/trigger_posts.py -p linkedin -c "Post 2: Second update" -t "Post 2" --preview
# Wait 10 seconds
sleep 10

# Create third post
python scripts/trigger_posts.py -p linkedin -c "Post 3: Third update" -t "Post 3" --preview

# Verify all 3 created
ls Pending_Approval/ | grep "_lin_" | wc -l
# Expected output: 3
```

### Step 7b: Approve All Posts
```bash
# Move all LinkedIn posts from Pending_Approval to Approved
mv Pending_Approval/POST_*_lin_*.md Approved/

# Verify all 3 moved
ls Approved/ | grep "_lin_" | wc -l
# Expected output: 3

# Verify Pending_Approval is empty for LinkedIn posts
ls Pending_Approval/ | grep "_lin_" | wc -l
# Expected output: 0
```

### Step 7c: Monitor Sequential Processing (Watch Terminal 1)
**In Terminal 1 (Orchestrator), watch for sequential processing:**

```
[2026-03-29 10:16:00] 📋 Processing: POST_20260329_*_lin_*.md (Post 1)
[2026-03-29 10:16:00] 🚀 Executing...
[2026-03-29 10:16:30] ✅ SUCCESS: Moved to Done (30 seconds)

[2026-03-29 10:16:31] 📋 Processing: POST_20260329_*_lin_*.md (Post 2)
[2026-03-29 10:16:31] 🚀 Executing...
[2026-03-29 10:17:01] ✅ SUCCESS: Moved to Done (30 seconds)

[2026-03-29 10:17:02] 📋 Processing: POST_20260329_*_lin_*.md (Post 3)
[2026-03-29 10:17:02] 🚀 Executing...
[2026-03-29 10:17:32] ✅ SUCCESS: Moved to Done (30 seconds)

Total batch processing time: ~90 seconds ✓
```

### Step 7d: Verify All Posts Processed
```bash
# Count processed files in Done folder
ls Done/ | grep "processed_POST.*_lin_" | wc -l
# Expected output: 3

# Verify nothing remains in Approved
ls Approved/ | grep "_lin_" | wc -l
# Expected output: 0

# List all processed files
echo "Processed LinkedIn posts:"
ls Done/ | grep "processed_POST.*_lin_"
# Expected: 3 files with processed_ prefix

# Check orchestrator logs for all 3 posts
grep "_lin_" Logs/orchestrator_*.log | grep "SUCCESS" | wc -l
# Expected output: 3
```

**Verification Checklist:**
- [ ] All 3 posts created successfully
- [ ] All 3 moved to Approved folder
- [ ] Orchestrator detected all 3
- [ ] Orchestrator processed them sequentially (not in parallel)
- [ ] Post 1 completed: ~30 seconds
- [ ] Post 2 completed: ~30 seconds
- [ ] Post 3 completed: ~30 seconds
- [ ] Total batch time: 60-100 seconds
- [ ] All 3 files now in Done/ folder
- [ ] No files stuck in Approved/

**Pass Criteria:** ✅ All 3 posts processed sequentially without issues

---

## Test 8: LinkedIn Error Recovery

**Objective:** Test automatic retry logic when posting fails

**Step-by-Step Instructions:**

### Step 8a: Create and Approve Post
```bash
# Terminal 2: Create a LinkedIn post
python scripts/trigger_posts.py -p linkedin -c "Error recovery test"
```

### Step 8b: Move to Approved
```bash
# Terminal 2: Move to Approved
mv Pending_Approval/POST_*_lin_*.md Approved/
```

### Step 8c: Watch Processing Start (Terminal 1)
**In Terminal 1 (Orchestrator), watch for execution to start:**

```
[2026-03-29 10:16:00] 📋 Processing: POST_*_lin_retry.md
[2026-03-29 10:16:00] 🚀 Executing...
[2026-03-29 10:16:05] Browser loading...
```

### Step 8d: Close Browser During Processing
```bash
# Quickly close the Playwright browser window
# This simulates a failure mid-posting
# (Do this when you see "Browser loading..." in Terminal 1)
```

### Step 8e: Monitor Orchestrator Response (Terminal 1)
**In Terminal 1, watch for error handling:**

```
[2026-03-29 10:16:15] ❌ Executor failed: BrowserError
[2026-03-29 10:16:15] 🔄 Scheduling retry (Attempt 1/4)
[2026-03-29 10:16:15] ⏱️ Cooldown: 5 minutes
[2026-03-29 10:16:15] Status: COOLDOWN

# (Wait 5 minutes)

[2026-03-29 10:21:20] ⏱️ Cooldown expired! Retrying...
[2026-03-29 10:21:20] 📋 Processing: POST_*_lin_retry.md (Attempt 2/4)
[2026-03-29 10:21:20] 🚀 Executing...
[2026-03-29 10:21:50] ✅ SUCCESS: LinkedIn post created!
[2026-03-29 10:21:50] ✅ Moved to Done
```

### Step 8f: Verify Success (Terminal 2)
```bash
# After retry succeeds, verify file moved
ls Done/ | grep "_lin_" | wc -l
# Expected: at least 1

# Verify nothing in Approved
ls Approved/ | grep "_lin_" | wc -l
# Expected: 0
```

**Verification Checklist:**
- [ ] First attempt fails with clear error message
- [ ] Error logged with details
- [ ] Cooldown timer starts (5 minutes)
- [ ] File stays in Approved (not deleted)
- [ ] Automatic retry happens after cooldown
- [ ] Second attempt succeeds
- [ ] File moved to Done
- [ ] No manual intervention needed

**Pass Criteria:** ✅ Automatic retry succeeds without user action

---

## Test 9: LinkedIn Session Persistence

**Objective:** Verify browser login session persists across multiple posts (no re-login needed)

**Step-by-Step Instructions:**

### Step 9a: Create and Post First LinkedIn Post
```bash
# Terminal 2: Create first post
python scripts/trigger_posts.py -p linkedin -c "Post 1" -t "Session Test 1"

# Move to Approved
mv Pending_Approval/POST_*_lin_*.md Approved/
```

**Terminal 1 (Orchestrator) shows:**
```
[2026-03-29 10:15:40] 🚀 Executing...
[2026-03-29 10:15:45] Launching browser for LinkedIn...
[2026-03-29 10:15:50] 🔐 Logging in to LinkedIn...
[2026-03-29 10:16:00] ✅ Account logged in
[2026-03-29 10:16:05] Navigating to post creation...
[2026-03-29 10:16:10] Filling content...
[2026-03-29 10:16:15] Posting...
[2026-03-29 10:16:20] ✅ SUCCESS: Post 1 created!
```

### Step 9b: Wait for Completion
```bash
# Wait until file moves to Done
watch "ls Done/ | grep '_lin_' | wc -l"
# Stop when count shows: 1
# (Press Ctrl+C to stop watching)
```

### Step 9c: Create and Post Second LinkedIn Post
```bash
# Terminal 2: Create second post
python scripts/trigger_posts.py -p linkedin -c "Post 2" -t "Session Test 2"

# Move to Approved
mv Pending_Approval/POST_*_lin_*.md Approved/
```

**Terminal 1 (Orchestrator) shows - NOTE: NO LOGIN THIS TIME!**
```
[2026-03-29 10:16:30] 🚀 Executing...
[2026-03-29 10:16:35] Launching browser...
[2026-03-29 10:16:40] 💾 Using saved session ✅ (NO re-login!)
[2026-03-29 10:16:45] Navigating to post creation...
[2026-03-29 10:16:50] Filling content...
[2026-03-29 10:16:55] Posting...
[2026-03-29 10:17:00] ✅ SUCCESS: Post 2 created!
```

### Step 9d: Create and Post Third LinkedIn Post
```bash
# Terminal 2: Create third post
python scripts/trigger_posts.py -p linkedin -c "Post 3" -t "Session Test 3"

# Move to Approved
mv Pending_Approval/POST_*_lin_*.md Approved/
```

**Terminal 1 (Orchestrator) shows:**
```
[2026-03-29 10:17:10] 🚀 Executing...
[2026-03-29 10:17:15] Launching browser...
[2026-03-29 10:17:20] 💾 Using saved session ✅ (STILL no re-login!)
[2026-03-29 10:17:25] Navigating to post creation...
[2026-03-29 10:17:30] Filling content...
[2026-03-29 10:17:35] Posting...
[2026-03-29 10:17:40] ✅ SUCCESS: Post 3 created!
```

### Step 9e: Verify Session Folder Has Data
```bash
# Check session folder contents
ls -la session/
# Expected output: Should show browser profile data files

# Count session files
ls session/ | wc -l
# Expected output: Multiple files (cache, cookies, data, etc.)

# Check logs confirm session reuse
grep "session" Logs/orchestrator_*.log | head -10
# Expected: Lines showing "Using saved session"
```

### Step 9f: Verify Timing Difference
```bash
# Post 1 should take longer (login overhead): ~35 seconds
# Posts 2 & 3 should be faster (no login): ~25 seconds each

grep "_lin_" Logs/orchestrator_*.log | grep "SUCCESS"
# Look at timestamps to calculate per-post timing
```

**Verification Checklist:**
- [ ] Post 1: Shows login process ("Logging in to LinkedIn...")
- [ ] Post 2: Shows "Using saved session ✅" (NO login)
- [ ] Post 3: Shows "Using saved session ✅" (NO login)
- [ ] Session folder exists and has files
- [ ] Post 1 timing: ~30-35 seconds (includes login)
- [ ] Post 2 timing: ~20-25 seconds (faster, no login)
- [ ] Post 3 timing: ~20-25 seconds (faster, no login)
- [ ] All 3 posts successfully created

**Pass Criteria:** ✅ Browser session persists across posts (no re-login needed after first post)

---

## Test 10: LinkedIn Content Preservation

**Objective:** Verify special characters, emoji, mentions, hashtags, and quotes are preserved throughout workflow

**Step-by-Step Instructions:**

### Step 10a: Create Post with Special Characters
```bash
# Create post with various special characters
python scripts/trigger_posts.py -p linkedin \
  -c "Testing with 🚀 emoji, @mentions, #hashtags and \"quotes\" and line
breaks too!" \
  -t "Special Content Test" \
  --preview
```

**Expected Output:**
```
✅ LinkedIn Draft Creator Successfully!
---
platform: linkedin
title: Special Content Test
---

# Special Content Test

Testing with 🚀 emoji, @mentions, #hashtags and "quotes" and line
breaks too!

---
📁 File saved to: Pending_Approval/POST_20260329_*.md
```

### Step 10b: Verify Content in File
```bash
# View the entire file
cat Pending_Approval/POST_*_lin_*.md

# Check each special character is preserved
echo "Checking special characters..."

# Check emoji preserved
grep "🚀" Pending_Approval/POST_*_lin_*.md
# Expected output: Testing with 🚀 emoji...

# Check mention preserved
grep "@mentions" Pending_Approval/POST_*_lin_*.md
# Expected output: @mentions

# Check hashtag preserved
grep "#hashtags" Pending_Approval/POST_*_lin_*.md
# Expected output: #hashtags

# Check quotes preserved
grep '"quotes"' Pending_Approval/POST_*_lin_*.md
# Expected output: "quotes"

# Check line breaks preserved
grep -A 2 "Special Content Test" Pending_Approval/POST_*_lin_*.md | grep "breaks"
# Expected output: should show line break preserved
```

### Step 10c: Move to Approved and Post
```bash
# Move to Approved for automatic posting
mv Pending_Approval/POST_*_lin_*.md Approved/

# Monitor orchestrator (Terminal 1) for posting completion
# Should see file move to Done/ within 20-35 seconds
```

### Step 10d: Verify Content on LinkedIn
```bash
# Manual verification on LinkedIn.com:
# 1. Go to linkedin.com
# 2. Navigate to your posts
# 3. Find the most recent post (Special Content Test)
# 4. Verify ALL of the following appear:
#    - Emoji: 🚀 displays correctly
#    - Mention: @mentions shows as clickable/formatted
#    - Hashtag: #hashtags shows as clickable/formatted
#    - Quotes: "quotes" appear exactly as typed
#    - Line break: appears between emoji line and "breaks" line
#    - All text displays correctly without corruption
```

**Verification Checklist:**
- [ ] File created with all special characters
- [ ] Emoji (🚀) in file content
- [ ] Mention (@mentions) in file content
- [ ] Hashtag (#hashtags) in file content
- [ ] Quotes ("quotes") in file content
- [ ] Line breaks preserved in file
- [ ] File posted successfully to LinkedIn
- [ ] Emoji displays correctly on LinkedIn
- [ ] Mention formatted correctly on LinkedIn
- [ ] Hashtag clickable on LinkedIn
- [ ] Quotes appear exactly as typed
- [ ] Line breaks appear on LinkedIn post

**Pass Criteria:** ✅ All special characters preserved throughout entire workflow

---

## Test 11: LinkedIn Performance Timing

**Objective:** Verify LinkedIn posting completes within expected time budget (20-35 seconds)

**Step-by-Step Instructions:**

### Step 11a: Create Post and Record Timestamp
```bash
# Get current time
date "+%H:%M:%S"
# Note this timestamp (Creation Time)

# Create LinkedIn post
python scripts/trigger_posts.py -p linkedin -c "Performance test" -t "Perf Test"

# Expected output timestamp in filename indicates creation time
```

### Step 11b: Move to Approved and Record Timestamp
```bash
# Get current time
date "+%H:%M:%S"
# Note this timestamp (Approval Time)

# Move to Approved
mv Pending_Approval/POST_*_lin_*.md Approved/

# Expected: Should take <1 second
```

### Step 11c: Monitor in Orchestrator (Terminal 1)
**Watch for these timestamps in Terminal 1:**

```
[10:15:34] Post created (noted from step 11a)
[10:15:35] Moved to Approved (noted from step 11b)

[10:15:39] 📋 Processing: POST_*.md (Detection timestamp)
             ↓ 4 seconds after approval ✓

[10:15:40] 🚀 Executing executor (Executor start timestamp)
             ↓ 1 second after detection ✓

[10:15:55] ✅ SUCCESS: Posted to LinkedIn (Posting complete timestamp)
             ↓ 15 seconds of execution ✓

[10:16:00] ✅ File moved to Done (Completion timestamp)
             ↓ 5 seconds for file movement ✓

Total time from Approval to Done: 25 seconds ✓ (within 20-35 second budget)
```

### Step 11d: Extract Timing from Logs
```bash
# View orchestrator log for your post
grep "_lin_" Logs/orchestrator_*.log | grep "Processing\|Executing\|SUCCESS"

# Example output:
# [2026-03-29 10:15:39] 📋 Processing: POST_20260329_101534_lin_*.md
# [2026-03-29 10:15:40] 🚀 Executing...
# [2026-03-29 10:16:00] ✅ SUCCESS

# Calculate timing:
# - Detection: 10:15:39
# - Start: 10:15:40 (1 second after detection)
# - Success: 10:16:00 (20 seconds of posting)
# - Total from Approval to Done: 25 seconds
```

### Step 11e: Verify Performance Budget
```bash
# Run performance test multiple times
for i in {1..5}; do
  echo "=== Performance Test $i ==="

  # Create and time the post
  START=$(date +%s)
  python scripts/trigger_posts.py -p linkedin -c "Perf Test $i"
  mv Pending_Approval/POST_*_lin_*.md Approved/

  # Wait for completion
  while [ ! -d "Done/processed_POST"* ]; do
    sleep 1
  done

  END=$(date +%s)
  DURATION=$((END - START))

  echo "Test $i completed in $DURATION seconds"

  # Reset for next test
  rm -rf Done/processed_POST*_lin_*
done

# Expected output:
# Test 1 completed in 28 seconds
# Test 2 completed in 26 seconds
# Test 3 completed in 24 seconds
# Test 4 completed in 27 seconds
# Test 5 completed in 25 seconds
# Average: ~26 seconds ✓
```

**Timing Breakdown:**
```
Detection:        < 5 seconds  (Orchestrator detects file in Approved)
Executor startup: 1-2 seconds  (Playwright launches browser)
Browser login:    5-10 seconds (Only on first post, then cached)
Navigation:       2-3 seconds  (Find post creation form)
Content fill:     2-3 seconds  (Type content)
Posting:          2-5 seconds  (Click post button, wait for confirmation)
File movement:    2-5 seconds  (Move from Approved to Done)
─────────────────────────────
Total:            20-35 seconds ✓
```

**Verification Checklist:**
- [ ] Detection time: < 5 seconds after moving to Approved
- [ ] Executor starts: 1-2 seconds after detection
- [ ] Posting completes: 10-20 seconds of execution
- [ ] File movement: < 5 seconds
- [ ] Total time: 20-35 seconds
- [ ] No timeouts or delays
- [ ] Consistent performance across multiple tests
- [ ] Performance within budget 5/5 times

**Pass Criteria:** ✅ All posts complete within 20-35 second budget

---

## Test 12: LinkedIn Integration with HITL (Human-In-The-Loop) Workflow

**Objective:** Test complete workflow with human review and approval before automatic posting

**Step-by-Step Instructions:**

### Step 12a: Create LinkedIn Draft
```bash
# Terminal 2: Create a draft
python scripts/trigger_posts.py -p linkedin \
  -c "Important announcement for our LinkedIn audience" \
  -t "Company Update"
```

**Expected Output:**
```
✅ Post created successfully
📁 File saved to: Pending_Approval/POST_20260329_*.md
```

### Step 12b: Human Review Phase (Simulate Manual Review)
```bash
# Open the file for review
cat Pending_Approval/POST_*_lin_*.md

# Contents to review:
# - Title: "Company Update"
# - Content: "Important announcement for our LinkedIn audience"
# - Format: Valid YAML + Markdown
# - Status: pending_approval

# Human reviews and verifies:
# [ ] Content is appropriate for LinkedIn
# [ ] Grammar and spelling correct
# [ ] Tone matches brand voice
# [ ] No sensitive information disclosed
# [ ] Links (if any) are valid
# [ ] Format is correct
```

### Step 12c: Human Approval - Move to Approved Folder
```bash
# After human review, APPROVE the post by moving it
# This is the human decision point - moving the file = approval

mv Pending_Approval/POST_*_lin_*.md Approved/

# Verify it moved
ls Approved/ | grep "_lin_"
# Expected: POST_20260329_*.md

# Verify it's NOT in Pending_Approval
ls Pending_Approval/ | grep "_lin_" | wc -l
# Expected: 0
```

### Step 12d: Monitor Automatic Posting (Terminal 1)
**In Terminal 1 (Orchestrator), watch for automatic posting:**

```
[2026-03-29 10:15:39] 📋 Processing: POST_*.md
[2026-03-29 10:15:40] 🚀 Executing automatic posting...
[2026-03-29 10:16:00] Filling content...
[2026-03-29 10:16:05] Posting...
[2026-03-29 10:16:15] ✅ SUCCESS: Post posted automatically!
[2026-03-29 10:16:15] ✅ File moved to Done
```

**Key Point:** Once file is in Approved, NO further human interaction needed!

### Step 12e: Verify Final Workflow
```bash
# Check file is now in Done folder
ls Done/ | grep "_lin_"
# Expected: processed_POST_20260329_*.md

# Check it left Approved folder
ls Approved/ | grep "_lin_" | wc -l
# Expected: 0

# View orchestrator log showing complete workflow
grep "_lin_.*Company Update" Logs/orchestrator_*.log
```

### Step 12f: Verify Post on LinkedIn
```bash
# Manual verification:
# 1. Visit linkedin.com
# 2. Check your posts/profile
# 3. Verify post appears with title "Company Update"
# 4. Verify content is posted
# 5. Verify timestamp shows recent post
```

**Workflow Diagram:**
```
HUMAN CREATES DRAFT (terminal)
    ↓
Pending_Approval/ [DRAFT REVIEW BY HUMAN]
    ↓
HUMAN DECIDES: APPROVE? Yes → Move file to Approved/
    ↓
Approved/ [AUTOMATIC POSTING STARTS]
    ↓
SYSTEM POSTS AUTOMATICALLY (no human needed)
    ↓
Done/ processed_POST_*
    ↓
✅ POST LIVE ON LINKEDIN
```

**Verification Checklist:**
- [ ] Draft created in Pending_Approval/
- [ ] Content fully reviewable by human
- [ ] Human can edit file if needed before approval
- [ ] File moved to Approved by human (approval action)
- [ ] NO further human action required after move
- [ ] Orchestrator automatically detects in Approved
- [ ] Orchestrator automatically executes posting
- [ ] Post appears on LinkedIn automatically
- [ ] File ends in Done/ folder
- [ ] Complete workflow: Create → Review → Approve → Auto-Post → Done

**Pass Criteria:** ✅ Complete HITL workflow functional - human controls approval, system automates posting

---

## Test 13: LinkedIn Multi-Platform Batch Testing

**Objective:** Test LinkedIn posting alongside all 6 platforms in a batch test run

**Step-by-Step Instructions:**

### Step 13a: Start Master Orchestrator (Terminal 1)
```bash
# In Terminal 1, start the orchestrator
python scripts/master_orchestrator.py

# Expected output:
# 🎯 Master Orchestrator v2.0 - Starting...
# 📁 Monitoring /Approved folder for posts...
# ✅ Orchestrator ready
```

### Step 13b: Run Automated Batch Test (Terminal 2)
```bash
# Run the automated batch testing script
python scripts/run_workflow_test.py --batch

# Expected output:
# 🚀 Batch Test Mode - Testing All 6 Platforms
# ═══════════════════════════════════════════════
#
# Creating test posts for all platforms...
# [✓] Facebook post created
# [✓] Twitter post created
# [✓] Instagram post created
# [✓] WhatsApp post created
# [✓] Gmail post created
# [✓] LinkedIn post created ← Your platform
#
# Moving all to Approved folder...
# [✓] All 6 files moved to Approved
#
# Monitoring orchestrator processing...
```

### Step 13c: Monitor Processing (Terminal 1)
**In Terminal 1, watch orchestrator process all 6 platforms:**

```
[2026-03-29 10:16:00] 📋 Processing: POST_*_fb_*.md (Facebook)
[2026-03-29 10:16:00] 🚀 Executing...
[2026-03-29 10:16:30] ✅ SUCCESS: Facebook posted

[2026-03-29 10:16:31] 📋 Processing: POST_*_lin_*.md (LinkedIn) ← Your focus
[2026-03-29 10:16:31] 🚀 Executing...
[2026-03-29 10:17:01] ✅ SUCCESS: LinkedIn posted

[2026-03-29 10:17:02] 📋 Processing: POST_*_tw_*.md (Twitter)
[2026-03-29 10:17:02] 🚀 Executing...
[2026-03-29 10:17:32] ✅ SUCCESS: Twitter posted

[2026-03-29 10:17:33] 📋 Processing: POST_*_ig_*.md (Instagram)
[2026-03-29 10:17:33] 🚀 Executing...
[2026-03-29 10:18:03] ✅ SUCCESS: Instagram posted

[2026-03-29 10:18:04] 📋 Processing: POST_*_wa_*.md (WhatsApp)
[2026-03-29 10:18:04] 🚀 Executing...
[2026-03-29 10:18:34] ✅ SUCCESS: WhatsApp posted

[2026-03-29 10:18:35] 📋 Processing: POST_*_gm_*.md (Gmail)
[2026-03-29 10:18:35] 🚀 Executing...
[2026-03-29 10:19:05] ✅ SUCCESS: Gmail posted

All 6 platforms processed sequentially!
Total batch time: ~180 seconds (3 minutes)
```

### Step 13d: Verify All Posts Processed (Terminal 2)
```bash
# Count files in Done folder
ls Done/ | grep "processed_POST" | wc -l
# Expected output: 6 (one for each platform)

# Verify LinkedIn specifically
ls Done/ | grep "processed_POST.*_lin_"
# Expected: 1 file with _lin_ code

# Verify all approved files are processed
ls Approved/ | grep "POST" | wc -l
# Expected: 0 (all should be moved out)

# Check for any errors
ls Logs/error_*.png 2>/dev/null | wc -l
# Expected: 0 (no error screenshots = success)
```

### Step 13e: Count Success by Platform
```bash
# Count each platform's processed files
echo "Platform Processing Summary:"
echo "Facebook:  $(ls Done/ | grep "_fb_" | wc -l) posts"
echo "LinkedIn:  $(ls Done/ | grep "_lin_" | wc -l) posts"
echo "Twitter:   $(ls Done/ | grep "_tw_" | wc -l) posts"
echo "Instagram: $(ls Done/ | grep "_ig_" | wc -l) posts"
echo "WhatsApp:  $(ls Done/ | grep "_wa_" | wc -l) posts"
echo "Gmail:     $(ls Done/ | grep "_gm_" | wc -l) posts"
echo "─────────────────────────"
echo "Total:     $(ls Done/ | grep "processed_POST" | wc -l) posts"

# Expected output:
# Facebook:  1 posts
# LinkedIn:  1 posts
# Twitter:   1 posts
# Instagram: 1 posts
# WhatsApp:  1 posts
# Gmail:     1 posts
# ─────────────────────────
# Total:     6 posts
```

### Step 13f: View Batch Test Report
```bash
# View the automated test report
cat Logs/orchestrator_*.log | grep -E "Processing:|SUCCESS:" | tail -20

# Expected to show all 6 platforms with SUCCESS messages
```

**Batch Processing Results:**
```
Platform Testing Summary:
╔════════════════════════════════════════════════╗
║ Platform   │ Status │ Time   │ File Moved │ ✓  ║
╠════════════════════════════════════════════════╣
║ Facebook   │ ✅     │ 30s    │ Approved→Done │ ✓ ║
║ LinkedIn   │ ✅     │ 30s    │ Approved→Done │ ✓ ║ ← Your test
║ Twitter    │ ✅     │ 30s    │ Approved→Done │ ✓ ║
║ Instagram  │ ✅     │ 30s    │ Approved→Done │ ✓ ║
║ WhatsApp   │ ✅     │ 30s    │ Approved→Done │ ✓ ║
║ Gmail      │ ✅     │ 30s    │ Approved→Done │ ✓ ║
╠════════════════════════════════════════════════╣
║ TOTAL      │ ✅✅✅ │ ~180s  │ 6/6 success   │✅✅║
╚════════════════════════════════════════════════╝
```

**Verification Checklist:**
- [ ] LinkedIn post created in Pending_Approval
- [ ] LinkedIn file moved to Approved
- [ ] Orchestrator detected LinkedIn post
- [ ] LinkedIn executor launched
- [ ] LinkedIn post completed
- [ ] LinkedIn file moved to Done/
- [ ] LinkedIn file renamed to processed_POST_*
- [ ] All 6 platforms processed sequentially
- [ ] No LinkedIn-specific errors
- [ ] Success rate: 100% (6/6 platforms)
- [ ] Total batch time: 150-200 seconds (2.5-3.5 minutes)

**Pass Criteria:** ✅ LinkedIn works correctly in batch with all 5 other platforms - 100% success rate

---

## Summary Checklist

### Pre-Testing
- [ ] Dependencies installed: `pip install playwright pyyaml watchdog`
- [ ] Directories exist: Pending_Approval, Approved, Done, Logs, session
- [ ] Python 3.8+
- [ ] Browser installed (Playwright)

### Basic Tests (1-4)
- [ ] Draft creation works
- [ ] Custom titles work
- [ ] Default content loads
- [ ] YAML valid

### Integration Tests (5-7)
- [ ] Orchestrator detects LinkedIn posts
- [ ] Executor posts to LinkedIn
- [ ] Multiple posts process sequentially

### Advanced Tests (8-13)
- [ ] Error recovery works
- [ ] Session persists
- [ ] Special characters preserved
- [ ] Performance acceptable
- [ ] HITL workflow complete
- [ ] Works in batch with other platforms

---

## Troubleshooting

### Issue: Browser Won't Login
```bash
# Clear session and try again
rm -rf session/*
# Re-run test - will prompt for manual login once
```

### Issue: Post Not Appearing on LinkedIn
```bash
# Check executor logs
grep -i "linkedin" Logs/orchestrator_*.log
# Check for error screenshots
ls -la Logs/error_*linkedin*.png
```

### Issue: File Stuck in Approved
```bash
# Restart orchestrator
pkill -f master_orchestrator
sleep 2
python scripts/master_orchestrator.py
```

### Issue: Timeout Error
```bash
# Increase timeout in orchestrator
# Edit line 180: timeout=300 → timeout=600
```

---

## Success Indicators

✅ **All Tests Passed When:**
- Drafts created in Pending_Approval
- Posts moved to Approved
- Orchestrator detected within 5s
- Executor posted successfully
- Files moved to Done
- No errors in logs
- All timing <35 seconds per post
- Session persisted correctly
- Content preserved exactly

---

## Performance Metrics

| Component | Expected Time |
|-----------|----------------|
| Draft creation | 1-2s |
| File detection | 5s |
| Executor startup | 2-3s |
| Browser login | 5-10s (first time only) |
| Post content fill | 3-5s |
| Posting | 2-5s |
| **Total per post** | **20-35s** |

---

## Status

**Test Suite:** ✅ COMPLETE
**Coverage:** ✅ COMPREHENSIVE (13 test cases)
**Platforms:** ✅ LINKEDIN FOCUSED
**Status:** ✅ PRODUCTION READY

Ready for LinkedIn posting validation!

---

**Last Updated:** 2026-03-29
**Version:** 1.0
**Status:** Production Ready
