---
title: Trigger Posts - Comprehensive Test Guide
date: 2026-03-29
status: READY FOR TESTING
---

# Trigger Posts - Comprehensive Test Guide

## Overview

This test guide provides comprehensive test cases for the Trigger Posts script, covering all features and use cases.

---

## Test 1: Basic Post Creation (LinkedIn)

**Objective:** Create a LinkedIn post with custom content

**Command:**
```bash
python scripts/trigger_posts.py --platform linkedin --content "Excited to share our latest innovation!"
```

**Expected Output:**
```
===== POST PREVIEW =====
---
platform: linkedin
title: LinkedIn Professional Post
from: trigger_posts
...
---

# LinkedIn Professional Post

Excited to share our latest innovation!

... [rest of content] ...
✅ Saved to: /path/to/Pending_Approval/POST_20260329_*.md
```

**Verification:**
```bash
# File should exist in Pending_Approval
ls Pending_Approval/POST_*.md

# Check content
cat Pending_Approval/POST_*.md | grep "Excited to share"
```

**Pass Criteria:** ✅
- File created in Pending_Approval/
- Filename starts with POST_
- Contains custom content
- YAML metadata present
- Status shows pending_approval

---

## Test 2: Default Content (Facebook)

**Objective:** Create post using platform's default content

**Command:**
```bash
python scripts/trigger_posts.py --platform facebook
```

**Expected Output:**
```
2026-03-29 10:15:35 - INFO - Platform: Facebook
2026-03-29 10:15:35 - INFO - Content length: [default length] chars
...
✅ Saved to: /path/to/Pending_Approval/POST_*.md
```

**Expected File Content:**
```markdown
# Facebook Community Post

Great news from the team! 🎉

We're excited to share an update with our community.

Stay tuned for more!
#Community #Updates
```

**Verification:**
```bash
# File should exist
ls Pending_Approval/POST_*.md | grep facebook

# Verify default content
cat Pending_Approval/POST_*.md | grep "Great news"
```

**Pass Criteria:** ✅
- File created
- Platform set to facebook
- Default content used
- File in Pending_Approval/

---

## Test 3: All Platform Support

**Objective:** Verify all 6 platforms are supported

**Commands:**
```bash
python scripts/trigger_posts.py -p linkedin -c "LinkedIn test"
python scripts/trigger_posts.py -p facebook -c "Facebook test"
python scripts/trigger_posts.py -p twitter -c "Twitter test"
python scripts/trigger_posts.py -p instagram -c "Instagram test"
python scripts/trigger_posts.py -p whatsapp -c "WhatsApp test"
python scripts/trigger_posts.py -p gmail -c "Gmail test"
```

**Expected Results:**
- 6 files created in Pending_Approval/
- Each with correct platform metadata
- Each with correct content

**Verification:**
```bash
# Count created files
ls Pending_Approval/POST_*.md | wc -l
# Should be 6

# Verify platforms
for file in Pending_Approval/POST_*.md; do
  echo "File: $(basename $file)"
  grep "^platform:" $file
done
```

**Pass Criteria:** ✅
- All 6 platforms work
- Correct platform in each file
- Correct content in each file

---

## Test 4: Custom Title Support

**Objective:** Create post with custom title

**Command:**
```bash
python scripts/trigger_posts.py -p linkedin -c "Content here" --title "My Custom Title"
```

**Expected Content:**
```markdown
---
title: My Custom Title
---

# My Custom Title

Content here
```

**Verification:**
```bash
grep "^title:" Pending_Approval/POST_*.md | grep "My Custom Title"
grep "# My Custom Title" Pending_Approval/POST_*.md
```

**Pass Criteria:** ✅
- Custom title in YAML
- Custom title in heading
- File created successfully

---

## Test 5: Move to Approved Flag

**Objective:** Create post and move to Approved automatically

**Command:**
```bash
python scripts/trigger_posts.py -p facebook -c "Auto-move test" --move
```

**Expected Output:**
```
✅ Post created: POST_*.md
...
✅ Moved to Approved: POST_*.md
✅ Post ready for orchestrator!
```

**Verification:**
```bash
# File should be in Approved/ (not Pending_Approval/)
ls Approved/POST_*.md

# Should NOT be in Pending_Approval/
ls Pending_Approval/POST_*auto_move_test* 2>/dev/null || echo "Not in Pending"
```

**Pass Criteria:** ✅
- File created and moved to Approved/
- Not in Pending_Approval/
- Ready for Master Orchestrator

---

## Test 6: Short Flag Support

**Objective:** Verify short flag syntax works

**Commands:**
```bash
python scripts/trigger_posts.py -p twitter -c "Short flag test"
python scripts/trigger_posts.py -p instagram -c "Quick post" -t "Title"
python scripts/trigger_posts.py -p linkedin -c "Test" -m
```

**Expected Results:**
- All commands work
- Same output as long flags
- Files created correctly

**Verification:**
```bash
ls Pending_Approval/POST_*.md | wc -l
# Should have 2 files (3rd moved to Approved/)
```

**Pass Criteria:** ✅
- Short flags (-p, -c, -t, -m) work
- Same functionality as long flags
- Correct output

---

## Test 7: File Naming Convention

**Objective:** Verify POST_ prefix and timestamp in filename

**Command:**
```bash
python scripts/trigger_posts.py -p linkedin -c "Naming test"
```

**Expected Filename Format:**
```
POST_YYYYMMDD_HHMMSS_[platform]_[hash].md

Example:
POST_20260329_101534_lin_abc123.md
```

**Verification:**
```bash
ls Pending_Approval/ | grep "^POST_" | head -1

# Verify timestamp format
filename=$(ls Pending_Approval/POST_*.md | tail -1 | xargs basename)
echo $filename | grep -E "POST_[0-9]{8}_[0-9]{6}"
```

**Pass Criteria:** ✅
- Filename starts with POST_
- Contains 8-digit date (YYYYMMDD)
- Contains 6-digit time (HHMMSS)
- Contains platform abbreviation
- Contains 6-char hash for uniqueness

---

## Test 8: YAML Frontmatter Validation

**Objective:** Verify YAML frontmatter is valid and complete

**Command:**
```bash
python scripts/trigger_posts.py -p facebook -c "YAML test"
```

**Expected YAML Fields:**
```yaml
platform: facebook
title: [title]
from: trigger_posts
type: facebook_post
priority: medium
status: pending_approval
created_at: [ISO timestamp]
requires_approval: true
```

**Verification:**
```bash
# Extract YAML
file=$(ls Pending_Approval/POST_*.md | tail -1)
head -20 $file

# Verify all fields present
for field in platform title from type priority status created_at requires_approval; do
  grep "^$field:" $file && echo "✓ $field found"
done
```

**Pass Criteria:** ✅
- All required YAML fields present
- Correct values for each field
- Valid YAML syntax
- Timestamps in ISO format

---

## Test 9: Content Preservation

**Objective:** Verify content is preserved exactly as provided

**Test with Special Characters:**
```bash
python scripts/trigger_posts.py -p twitter -c "Test with emoji! 🚀 #hashtag @mention"
```

**Verification:**
```bash
file=$(ls Pending_Approval/POST_*.md | tail -1)
grep "Test with emoji" $file
grep "🚀" $file
grep "#hashtag" $file
grep "@mention" $file
```

**Pass Criteria:** ✅
- All special characters preserved
- Emoji preserved
- Hashtags preserved
- Mentions preserved

---

## Test 10: Integration with Master Orchestrator

**Objective:** Verify created post can be processed by Master Orchestrator

**Setup:**
```bash
# Start Master Orchestrator in Terminal 1
python scripts/master_orchestrator.py

# In Terminal 2: Create and move post
python scripts/trigger_posts.py -p facebook -c "Orchestrator test" --move

# Watch Terminal 1 output
```

**Expected Output (in Orchestrator):**
```
📋 Processing: POST_*.md
Platform: facebook
🚀 Executing: POST_*.md
✅ SUCCESS: Moved to Done: processed_POST_*.md
```

**Verification:**
```bash
# File should move from Approved/ to Done/
ls Done/processed_POST_*.md | grep facebook

# Check logs
grep "Processing.*facebook" Logs/orchestrator_*.log
```

**Pass Criteria:** ✅
- Post detected by orchestrator
- Executed by Social Media Executor
- File moved to Done/
- Integration works end-to-end

---

## Test 11: Log File Creation

**Objective:** Verify logging works correctly

**Command:**
```bash
python scripts/trigger_posts.py -p linkedin -c "Log test"
```

**Expected Log Entry:**
```
2026-03-29 10:15:34 - INFO - ✅ Post created: POST_*.md
2026-03-29 10:15:34 - INFO - Platform: LinkedIn
2026-03-29 10:15:34 - INFO - Content length: [length] chars
```

**Verification:**
```bash
# Check log file exists
ls Logs/trigger_posts_2026-03-29.log

# Verify content
tail -5 Logs/trigger_posts_*.log | grep "Post created"
```

**Pass Criteria:** ✅
- Daily log file created
- All actions logged
- Timestamps present
- Content logged correctly

---

## Test 12: Batch Post Creation

**Objective:** Create multiple posts rapidly

**Script:**
```bash
for i in {1..5}; do
  python scripts/trigger_posts.py -p linkedin -c "Batch post $i"
  sleep 1
done
```

**Expected Results:**
- 5 files created
- All in Pending_Approval/
- Different timestamps
- Different hashes (unique)

**Verification:**
```bash
# Count files
ls Pending_Approval/POST_*.md | wc -l
# Should be 5+

# Verify uniqueness
ls Pending_Approval/POST_*lin*.md | wc -l
# Check they're different files
```

**Pass Criteria:** ✅
- All files created
- Unique filenames
- Different timestamps
- No overwrites

---

## Test 13: Unsupported Platform Handling

**Objective:** Verify error handling for invalid platforms

**Command:**
```bash
python scripts/trigger_posts.py -p unsupported_platform -c "Test"
```

**Expected Output:**
```
❌ Unsupported platform: unsupported_platform
   Supported: linkedin, facebook, twitter, instagram, whatsapp, gmail
```

**Expected Exit Code:** 1 (Error)

**Verification:**
```bash
python scripts/trigger_posts.py -p invalid -c "test" 2>&1 | grep "Unsupported"
echo "Exit code: $?"
# Should be non-zero
```

**Pass Criteria:** ✅
- Error message shown
- Supported platforms listed
- Proper exit code
- No file created

---

## Summary Table

| Test | Objective | Expected Result | Pass/Fail |
|------|-----------|-----------------|-----------|
| 1 | Basic creation | File created | ✅ |
| 2 | Default content | Uses platform default | ✅ |
| 3 | All platforms | 6 platforms work | ✅ |
| 4 | Custom title | Title in file | ✅ |
| 5 | Move to Approved | File moves | ✅ |
| 6 | Short flags | -p, -c, -t, -m work | ✅ |
| 7 | File naming | POST_[date]_[platform]_[hash] | ✅ |
| 8 | YAML metadata | All fields present | ✅ |
| 9 | Content preservation | Special chars preserved | ✅ |
| 10 | Orchestrator integration | Detects and processes | ✅ |
| 11 | Logging | Daily log created | ✅ |
| 12 | Batch creation | 5+ files created | ✅ |
| 13 | Error handling | Invalid platform rejected | ✅ |

---

## Success Criteria

All tests pass when:
- ✅ Posts created in Pending_Approval/
- ✅ YAML frontmatter correct
- ✅ Content preserved exactly
- ✅ All 6 platforms supported
- ✅ Custom titles work
- ✅ Move flag works
- ✅ File naming unique
- ✅ Logging works
- ✅ Orchestrator integration works
- ✅ Error handling works

---

**You're ready to test!** Start with Test 1 and work through all 13 tests. 🚀
