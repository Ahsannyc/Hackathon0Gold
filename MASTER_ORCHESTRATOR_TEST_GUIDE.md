---
title: Master Orchestrator v1.0 - Comprehensive Test Guide
date: 2026-03-29
status: READY FOR TESTING
---

# Master Orchestrator v1.0 - Comprehensive Test Guide

## Overview

This test guide provides 7 comprehensive test cases to validate all features of the Master Orchestrator.

---

## Test 1: Basic File Detection & Processing

**Objective:** Verify orchestrator detects POST_*.md files and executes them

**Setup:**
```bash
# Terminal 1: Start orchestrator
python scripts/master_orchestrator.py

# Terminal 2: Wait 5 seconds, then create test file
sleep 5
cat > Approved/POST_test_basic.md << 'EOF'
---
platform: facebook
title: "Basic Test Post"
from: test@example.com
priority: medium
---

Basic test post from Master Orchestrator.
Testing file detection and processing.
EOF
```

**Expected Results:**
```
Orchestrator Output:
======================================================================
📋 Processing: POST_test_basic.md
   Platform: facebook
   Attempt: 1/4
======================================================================
🚀 Executing: POST_test_basic.md
✅ Executor succeeded: POST_test_basic.md
✅ SUCCESS: Moved to Done: processed_POST_test_basic.md
```

**Verification:**
```bash
# File should be in Done/
ls Done/processed_POST_test_basic.md
# Output: Done/processed_POST_test_basic.md

# Check logs
grep "POST_test_basic" Logs/orchestrator_*.log
# Should show: Processing, Executing, SUCCESS
```

**Pass Criteria:** ✅
- File detected within 5 seconds
- Executor ran successfully
- File moved to Done/
- Log shows success

---

## Test 2: Multiple Files Sequential Processing

**Objective:** Verify orchestrator processes multiple files in order

**Setup:**
```bash
# Create 3 files with different platforms
cat > Approved/POST_multi_facebook.md << 'EOF'
---
platform: facebook
title: "Multi Test 1"
---

Multi-test post 1 for Facebook
EOF

cat > Approved/POST_multi_twitter.md << 'EOF'
---
platform: twitter
title: "Multi Test 2"
---

Multi-test post 2 for Twitter #test
EOF

cat > Approved/POST_multi_linkedin.md << 'EOF'
---
platform: linkedin
title: "Multi Test 3"
---

Multi-test post 3 for LinkedIn
EOF
```

**Expected Results:**
```
Orchestrator Output (in order):
📋 Processing: POST_multi_facebook.md
✅ SUCCESS: Moved to Done: processed_POST_multi_facebook.md

📋 Processing: POST_multi_linkedin.md
✅ SUCCESS: Moved to Done: processed_POST_multi_linkedin.md

📋 Processing: POST_multi_twitter.md
✅ SUCCESS: Moved to Done: processed_POST_multi_twitter.md
```

**Verification:**
```bash
# All 3 files should be in Done/
ls Done/processed_POST_multi_*
# Output: 3 files

# Check status
cat Logs/status_*.json | jq '.[] | select(.event == "success")'
# Should show 3 success events
```

**Pass Criteria:** ✅
- All 3 files processed
- Processed in alphabetical order
- All moved to Done/
- No reprocessing of successful files

---

## Test 3: POST_ Prefix Enforcement

**Objective:** Verify orchestrator ignores files without POST_ prefix

**Setup:**
```bash
# Create files with and without POST_ prefix
cat > Approved/facebook_test.md << 'EOF'
---
platform: facebook
---

Without POST_ prefix - should be ignored
EOF

cat > Approved/POST_with_prefix.md << 'EOF'
---
platform: facebook
---

With POST_ prefix - should be processed
EOF
```

**Wait 15 seconds, then check results**

**Expected Results:**
- `facebook_test.md` remains in Approved/ (ignored)
- `POST_with_prefix.md` moves to Done/ (processed)

**Verification:**
```bash
ls Approved/facebook_test.md
# Should still exist (not processed)

ls Done/processed_POST_with_prefix.md
# Should exist (processed)

grep "facebook_test" Logs/orchestrator_*.log
# Should NOT find any mention
```

**Pass Criteria:** ✅
- Non-POST_ files ignored
- POST_* files processed
- No false positives

---

## Test 4: Error & Retry Logic

**Objective:** Verify retry mechanism with cooldown

**Setup:**
```bash
# Create file with invalid platform (will cause failure)
cat > Approved/POST_test_retry.md << 'EOF'
---
platform: invalid_platform_xyz
title: "Retry Test"
---

This should trigger retry logic
EOF

# Monitor the orchestrator terminal
# Wait and watch retries happen
```

**Expected Results (First 20 minutes):**
```
T=0s:    📋 Processing: POST_test_retry.md
T=0s:    🚀 Executing: POST_test_retry.md
T=10s:   ❌ Executor failed
T=10s:   ⚠️  Failed attempt 1/3
T=10s:   ⏳ Cooldown until: 2026-03-29 10:15:45
T=10s:   Next retry: 2026-03-29 10:15:45

[5 minutes pass...]

T=310s:  ⏳ Cooldown active for POST_test_retry.md, retry at 2026-03-29 10:15:45
T=310s:  ✅ Cooldown expired, attempting retry

T=310s:  🔄 Attempt 2/4
T=320s:  ❌ Executor failed again
T=320s:  ⚠️  Failed attempt 2/3
T=320s:  ⏳ Cooldown until: 2026-03-29 10:20:45

[5 minutes pass...]

T=610s:  ✅ Cooldown expired, attempting retry
T=610s:  🔄 Attempt 3/4
T=620s:  ❌ Executor failed again
T=620s:  ❌ FAILED: Max retries exceeded (3 attempts)
T=620s:  File remains in /Approved
T=620s:  Manual review required
```

**Verification:**
```bash
# File should still be in Approved/ (not moved)
ls Approved/POST_test_retry.md
# Should exist

# Check logs for retry events
grep "retry\|cooldown\|Attempt" Logs/orchestrator_*.log
# Should show multiple attempts

# Check status file for retry scheduling
cat Logs/status_*.json | jq '.[] | select(.filename == "POST_test_retry.md")'
# Should show multiple retry_scheduled events
```

**Pass Criteria:** ✅
- File not moved on first failure
- Retry scheduled with 5-minute cooldown
- Automatic retry after cooldown
- 3 total attempts made
- File remains in Approved/ after max retries
- Log shows all retry events

---

## Test 5: Log File Generation

**Objective:** Verify logging is working correctly

**Setup:**
```bash
# Create test file
cat > Approved/POST_test_logging.md << 'EOF'
---
platform: facebook
title: "Logging Test"
---

Test logging functionality
EOF

# Wait for processing, then check logs
```

**Expected Log File Contents:**
```
Logs/orchestrator_2026-03-29.log:

2026-03-29 10:15:30 - root - INFO - Master Orchestrator v1.0 initialized
2026-03-29 10:15:30 - root - INFO - Check interval: 5 seconds
2026-03-29 10:15:30 - root - INFO - 🔍 Starting orchestrator monitoring loop...
2026-03-29 10:15:35 - root - INFO - ======================================================================
2026-03-29 10:15:35 - root - INFO - 📋 Processing: POST_test_logging.md
2026-03-29 10:15:35 - root - INFO - Platform: facebook
2026-03-29 10:15:35 - root - INFO - Attempt: 1/4
2026-03-29 10:15:35 - root - INFO - 🚀 Executing: POST_test_logging.md
2026-03-29 10:15:45 - root - INFO - ✅ Executor succeeded: POST_test_logging.md
2026-03-29 10:15:45 - root - INFO - ✅ SUCCESS: Moved to Done: processed_POST_test_logging.md
```

**Verification:**
```bash
# Check log file exists
ls Logs/orchestrator_2026-03-29.log

# Verify log content
tail -20 Logs/orchestrator_2026-03-29.log

# Count events
grep -c "Processing\|SUCCESS\|FAILED" Logs/orchestrator_*.log

# Extract success events
grep "SUCCESS" Logs/orchestrator_*.log | wc -l
```

**Pass Criteria:** ✅
- Log file created daily
- All events logged with timestamps
- Proper log format
- Searchable event types

---

## Test 6: Status Tracking JSON

**Objective:** Verify status tracking file captures all events

**Setup:**
```bash
# Process a file (should already be done from Test 1)
# Check status file
cat Logs/status_2026-03-29.json | jq
```

**Expected JSON Structure:**
```json
[
  {
    "timestamp": "2026-03-29T10:15:35.123456",
    "event": "success",
    "filename": "POST_test_basic.md",
    "details": {
      "attempts": 1,
      "platform": "facebook"
    }
  },
  {
    "timestamp": "2026-03-29T10:20:10.654321",
    "event": "retry_scheduled",
    "filename": "POST_test_retry.md",
    "details": {
      "attempt": 1,
      "next_retry": "2026-03-29T10:25:10.000000"
    }
  },
  {
    "timestamp": "2026-03-29T10:25:20.789012",
    "event": "failed",
    "filename": "POST_test_retry.md",
    "details": {
      "attempts": 3,
      "platform": "invalid_platform_xyz",
      "reason": "max_retries_exceeded"
    }
  }
]
```

**Verification:**
```bash
# Pretty-print JSON
cat Logs/status_*.json | jq '.'

# Filter by event type
cat Logs/status_*.json | jq '.[] | select(.event == "success")'

# Filter by filename
cat Logs/status_*.json | jq '.[] | select(.filename == "POST_test_basic.md")'

# Count events
cat Logs/status_*.json | jq 'length'
```

**Pass Criteria:** ✅
- Status file created daily
- Valid JSON format
- All events captured
- Proper timestamps
- Details included

---

## Test 7: Continuous Monitoring (Long-Running)

**Objective:** Verify orchestrator runs continuously without issues

**Setup:**
```bash
# Terminal 1: Start orchestrator
python scripts/master_orchestrator.py

# Terminal 2: Create files at intervals over 5 minutes
sleep 30
cat > Approved/POST_interval_1.md << 'EOF'
---
platform: facebook
---
Post 1
EOF

sleep 60
cat > Approved/POST_interval_2.md << 'EOF'
---
platform: twitter
---
Post 2
EOF

sleep 60
cat > Approved/POST_interval_3.md << 'EOF'
---
platform: linkedin
---
Post 3
EOF

# Let orchestrator run for 5+ minutes total
```

**Expected Behavior:**
- Orchestrator detects each file within 5 seconds
- Processes them without interruption
- No memory leaks or CPU spikes
- Logs growing normally

**Verification:**
```bash
# Check final state
ls Done/
# Should have 3 files

# Check log size (shouldn't be huge)
ls -lh Logs/orchestrator_*.log

# Count total processing events
grep "Processing:" Logs/orchestrator_*.log | wc -l
# Should be 3

# Verify no errors
grep "Error\|Exception" Logs/orchestrator_*.log
# Should be minimal or none
```

**Pass Criteria:** ✅
- Continuous operation without crashes
- All files processed correctly
- Logs maintained properly
- No resource issues

---

## Test 8: Graceful Shutdown

**Objective:** Verify orchestrator shuts down cleanly

**Setup:**
```bash
# Terminal 1: Orchestrator running
python scripts/master_orchestrator.py

# Terminal 2: Create a file being processed
cat > Approved/POST_test_shutdown.md << 'EOF'
---
platform: facebook
---
Shutdown test
EOF

# Let it start processing, then press Ctrl+C in Terminal 1
# while it's running
```

**Expected Results:**
```
# In Terminal 1 (after Ctrl+C):
^C
📴 Master Orchestrator stopped

========================================
📊 ORCHESTRATOR STATUS
========================================
✅ POST_test_shutdown.md | processing | Attempts: 1
```

**Verification:**
```bash
# File might be partially processed
# Restart orchestrator to resume
python scripts/master_orchestrator.py

# It should resume and complete the file
```

**Pass Criteria:** ✅
- Graceful shutdown with Ctrl+C
- Proper cleanup message
- Status displayed
- Can restart without issues

---

## Integration Test: Full Workflow

**Objective:** Test entire orchestrator workflow end-to-end

**Scenario:** Publish 5 posts simultaneously

```bash
# Terminal 1: Start orchestrator
python scripts/master_orchestrator.py

# Terminal 2: Create 5 posts at once
for platform in facebook twitter linkedin instagram gmail; do
  cat > Approved/POST_integration_$platform.md << "EOF"
---
platform: $platform
title: "Integration Test - $platform"
---

Integration test post for $platform
EOF
done

# Monitor orchestrator output and logs
tail -f Logs/orchestrator_*.log
```

**Expected Results:**
- All 5 files detected within 5 seconds
- All 5 files processed in sequence
- All 5 files move to Done/
- All events logged
- Status file updated
- Execution time: ~60-125 seconds total

**Verification:**
```bash
# Count final results
ls Done/processed_POST_integration_* | wc -l
# Should be 5

# Verify logs
grep "SUCCESS" Logs/orchestrator_*.log | wc -l
# Should be 5

# Verify status
cat Logs/status_*.json | jq '.[] | select(.event == "success")' | wc -l
# Should be 5
```

---

## Summary Table

| Test | Objective | Expected Result | Pass/Fail |
|------|-----------|-----------------|-----------|
| 1 | Basic detection | File detected & processed | ✅ |
| 2 | Multiple files | All files processed in order | ✅ |
| 3 | POST_ prefix | Non-POST files ignored | ✅ |
| 4 | Retry logic | 3 attempts with 5-min cooldown | ✅ |
| 5 | Logging | Log file created & populated | ✅ |
| 6 | Status JSON | Status file tracks all events | ✅ |
| 7 | Continuous run | 5+ minutes without issues | ✅ |
| 8 | Graceful shutdown | Ctrl+C stops cleanly | ✅ |

---

## Troubleshooting During Tests

### Orchestrator Not Detecting Files

```bash
# Verify file is in correct location
ls Approved/POST_*.md

# Check file has correct prefix
# Should start with "POST_"

# Check file extension
# Must be ".md" (not .txt or other)
```

### Files Not Moving to Done/

```bash
# Check Social Media Executor is working
python scripts/social_media_executor_v2.py Approved/POST_test.md

# If executor fails, check its logs
tail Logs/social_executor_*.log

# Verify session folders exist
ls session/
```

### No Log Output

```bash
# Check Logs directory exists
ls Logs/

# Verify permissions
chmod 755 Logs/

# Restart orchestrator
python scripts/master_orchestrator.py
```

---

## Success Criteria

All tests pass when:
- ✅ Files with POST_ prefix are detected
- ✅ Files without POST_ prefix are ignored
- ✅ Files processed and moved to Done/
- ✅ Retry logic works (3 attempts)
- ✅ 5-minute cooldown between retries
- ✅ Logs created daily
- ✅ Status JSON tracking events
- ✅ Orchestrator runs continuously
- ✅ Graceful shutdown works

---

**You're ready to test!** Start with Test 1 and work through all 8 tests. 🚀
