---
title: Master Orchestrator v1.0 - Quick Start Guide
date: 2026-03-29
status: READY TO RUN
---

# Master Orchestrator v1.0 - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Watchdog

```bash
pip install watchdog pyyaml
```

### Step 2: Start the Orchestrator

```bash
python scripts/master_orchestrator.py
```

**Expected Output:**
```
╔════════════════════════════════════════════════════════════════╗
║        MASTER ORCHESTRATOR v1.0 - STARTUP                      ║
║   Autonomous Social Media Publishing Orchestrator              ║
╚════════════════════════════════════════════════════════════════╝

Master Orchestrator v1.0 initialized
Approved folder: /path/to/Approved
Done folder: /path/to/Done
Logs folder: /path/to/Logs
Check interval: 5 seconds
Max retries: 3
Retry cooldown: 300 seconds

🔍 Starting orchestrator monitoring loop...
   Checking every 5 seconds

2026-03-29 10:15:34 - root - INFO - Monitoring: /path/to/Approved
2026-03-29 10:15:34 - root - INFO - File pattern: POST_*.md
```

### Step 3: Create Test File

In another terminal (don't stop the orchestrator):

```bash
cat > Approved/POST_facebook_test.md << 'EOF'
---
platform: facebook
title: "Test Post from Orchestrator"
from: test@example.com
priority: medium
---

Testing Master Orchestrator! 🎉

This post is being published autonomously by the orchestrator system.
EOF
```

### Step 4: Watch It Work

Back in orchestrator terminal, you'll see:

```
======================================================================
📋 Processing: POST_facebook_test.md
   Platform: facebook
   Attempt: 1/4
======================================================================
🚀 Executing: POST_facebook_test.md
✅ Executor succeeded: POST_facebook_test.md
✅ SUCCESS: Moved to Done: processed_POST_facebook_test.md
```

### Step 5: Verify Success

```bash
# File moved to Done
ls Done/processed_POST_facebook_test.md

# Check logs
tail -30 Logs/orchestrator_2026-03-29.log

# Check status tracking
cat Logs/status_2026-03-29.json | jq
```

---

## 📋 File Naming Convention

The orchestrator **only processes files starting with `POST_`**:

```
✅ Accepted:
- POST_facebook_test.md
- POST_twitter_announcement.md
- POST_linkedin_thought_leadership.md
- POST_20260329_123456.md

❌ Rejected:
- facebook_test.md (missing POST_ prefix)
- test_post.md
- POST_draft.txt (wrong extension)
```

**Remember:** Add `POST_` prefix to activate orchestrator processing

---

## 🔄 Monitoring Details

### Check Interval
- **Default:** 5 seconds
- Orchestrator checks `/Approved/` every 5 seconds for new POST_*.md files

### What Gets Checked
```
Approved/
├── POST_facebook_test.md      ← CHECKED
├── POST_twitter_post.md       ← CHECKED
├── draft_post.md              ← IGNORED (no POST_ prefix)
└── linkedin_campaign.md       ← IGNORED (no POST_ prefix)
```

### Processing Order
- Processes files in alphabetical order
- Each file processed once
- Successful files don't reprocess

---

## 🔁 Retry Logic

### Success Path
```
POST_file.md (in /Approved/)
    ↓ (Orchestrator detects)
Run Social Media Executor
    ↓ Success
Move to /Done/processed_POST_file.md
    ✅ DONE
```

### Failure & Retry Path
```
POST_file.md (in /Approved/)
    ↓ (Orchestrator detects)
Run Social Media Executor
    ↓ FAILS (Attempt 1/3)
    ↓ 5-minute cooldown
    ↓
Run Social Media Executor
    ↓ FAILS (Attempt 2/3)
    ↓ 5-minute cooldown
    ↓
Run Social Media Executor
    ↓ FAILS (Attempt 3/3)
    ↓
❌ FAILED - Max retries exceeded
File stays in /Approved/ for manual review
```

### Cooldown Behavior
- After each failure: **5-minute cooldown**
- During cooldown: File stays in /Approved/
- After cooldown expires: **Automatically retries**
- Max retries: **3 attempts total**

---

## 📊 Real-World Example

### Scenario: Publish 3 Posts

```bash
# Terminal 1: Start orchestrator
python scripts/master_orchestrator.py

# Terminal 2: Create 3 test files
cat > Approved/POST_facebook_launch.md << 'EOF'
---
platform: facebook
title: "Product Launch"
---

Excited to announce our new product! 🚀
EOF

cat > Approved/POST_twitter_update.md << 'EOF'
---
platform: twitter
title: "Update"
---

Just shipped new features! #development
EOF

cat > Approved/POST_linkedin_article.md << 'EOF'
---
platform: linkedin
title: "Thought Leadership"
---

Here's what we learned this quarter...
EOF
```

### Orchestrator Output

```
2026-03-29 10:15:34 - 🔍 Starting orchestrator monitoring loop...
2026-03-29 10:15:39 - 📋 Processing: POST_facebook_launch.md
2026-03-29 10:15:39 - 🚀 Executing: POST_facebook_launch.md
2026-03-29 10:15:49 - ✅ SUCCESS: Moved to Done: processed_POST_facebook_launch.md

2026-03-29 10:15:54 - 📋 Processing: POST_linkedin_article.md
2026-03-29 10:15:54 - 🚀 Executing: POST_linkedin_article.md
2026-03-29 10:16:04 - ✅ SUCCESS: Moved to Done: processed_POST_linkedin_article.md

2026-03-29 10:16:09 - 📋 Processing: POST_twitter_update.md
2026-03-29 10:16:09 - 🚀 Executing: POST_twitter_update.md
2026-03-29 10:16:19 - ✅ SUCCESS: Moved to Done: processed_POST_twitter_update.md

2026-03-29 10:16:24 - 📊 ORCHESTRATOR STATUS
✅ POST_facebook_launch.md      | success      | Attempts: 1
✅ POST_linkedin_article.md     | success      | Attempts: 1
✅ POST_twitter_update.md       | success      | Attempts: 1
```

### Result

```bash
ls Done/
# processed_POST_facebook_launch.md
# processed_POST_linkedin_article.md
# processed_POST_twitter_update.md
```

---

## 📝 Log Files

### Daily Orchestrator Log
```
Logs/orchestrator_2026-03-29.log
```

**Contains:**
- All events (startup, file detection, processing, success, failure)
- Timestamps for each action
- Attempt counts
- Platform information
- Error messages

### Status Tracking File
```
Logs/status_2026-03-29.json
```

**JSON format with:**
- Timestamp
- Event type (success, retry_scheduled, failed)
- Filename
- Details (attempts, platform, next_retry)

### View Logs

```bash
# Real-time (last 50 lines)
tail -50 Logs/orchestrator_2026-03-29.log

# Follow in real-time
tail -f Logs/orchestrator_2026-03-29.log

# View status tracking
cat Logs/status_2026-03-29.json | jq

# Count events
grep "success\|failed\|retry" Logs/orchestrator_2026-03-29.log | wc -l
```

---

## 🛑 Stopping the Orchestrator

```bash
# Press Ctrl+C in the terminal running the orchestrator
^C

# Output:
# 📴 Master Orchestrator stopped
```

### Files in Progress

If orchestrator is stopped:
- Files being processed stay in `/Approved/`
- Restart orchestrator to resume
- Retries continue from where it left off

---

## ⚙️ Configuration

### Check Interval (default: 5 seconds)

To change check interval:
```python
# In master_orchestrator.py, line ~120:
self.check_interval = 5  # Change to 10 for 10 seconds
```

### Max Retries (default: 3)

```python
# In master_orchestrator.py, line ~121:
self.max_retries = 3  # Change to 5 for 5 retries
```

### Cooldown Time (default: 300 seconds = 5 minutes)

```python
# In master_orchestrator.py, line ~122:
self.retry_cooldown = 300  # Change to 600 for 10 minutes
```

---

## 🧪 Test Cases

### Test 1: Single File Success

```bash
# Terminal 1: Start orchestrator
python scripts/master_orchestrator.py

# Terminal 2: Create single file
cat > Approved/POST_test_single.md << 'EOF'
---
platform: facebook
title: "Test"
---

Single test post
EOF

# Expected: File moves to Done/ within 10-20 seconds
```

### Test 2: Multiple Files

```bash
# Create 3 files at once
for i in {1..3}; do
  cat > Approved/POST_test_$i.md << "EOF"
---
platform: facebook
title: "Test $i"
---

Test post number $i
EOF
done

# Expected: All 3 files processed in order, all move to Done/
```

### Test 3: Monitor Logs in Real-Time

```bash
# Terminal 1: Start orchestrator
python scripts/master_orchestrator.py

# Terminal 2: Watch logs
tail -f Logs/orchestrator_2026-03-29.log

# Terminal 3: Add files
cat > Approved/POST_test_with_logs.md << 'EOF'
---
platform: twitter
title: "Log Test"
---

Test with live logging
EOF

# Expected: See events in real-time in Terminal 2
```

---

## 📂 File Locations

```
scripts/
└── master_orchestrator.py                (Main orchestrator)

Approved/
├── POST_facebook_test.md                (Input files)
├── POST_twitter_test.md
└── [other POST_*.md files]

Done/
└── processed_POST_*.md                  (Processed files)

Logs/
├── orchestrator_2026-03-29.log          (Daily log)
└── status_2026-03-29.json               (Status tracking)
```

---

## 🔑 Key Features

✅ **Autonomous:** No manual intervention needed
✅ **Resilient:** Retries 3 times before giving up
✅ **Monitored:** Checks every 5 seconds
✅ **Logged:** Complete audit trail in logs
✅ **Smart:** Tracks state and retry cooldowns
✅ **Reliable:** Graceful error handling

---

## 🚀 Next Steps

1. ✅ Install watchdog: `pip install watchdog`
2. ✅ Start orchestrator: `python scripts/master_orchestrator.py`
3. ✅ Create test file with `POST_` prefix
4. ✅ Watch it get processed automatically
5. ✅ Verify in /Done folder
6. ✅ Check logs for confirmation

**Ready to go!** 🎉

---

## 💡 Tips

- **Add POST_ prefix** to activate orchestrator processing
- **Check /Approved/ folder** before creating files
- **Monitor logs** for real-time status: `tail -f Logs/orchestrator_*.log`
- **Restart orchestrator** after configuration changes
- **Status file** tracks all events: `Logs/status_*.json`

---

**You're ready!** Run the orchestrator now:

```bash
python scripts/master_orchestrator.py
```
