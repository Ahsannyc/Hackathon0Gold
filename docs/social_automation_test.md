---
title: AI Social Media Manager - Full Workflow Test Guide
date: 2026-03-29
status: PRODUCTION TEST READY
version: 1.0
---

# AI Social Media Manager - Full Workflow Test Guide

## 📋 Overview

This guide validates the complete AI Social Media Manager workflow end-to-end:

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────┐
│ Trigger Posts   │────→│ Pending_Approval │────→│ Master Orchestrator│────→│ Executor │────→ /Done
│  (Draft Gen)    │     │  (Manual Review) │     │  (Auto Monitor)   │     │ (Post)   │
└─────────────────┘     └──────────────────┘     └──────────────────┘     └──────────┘
                              │
                              ├─ HITL Approval
                              │
                         /Approved
```

**Time to Complete:** 15-30 minutes (depending on platform speed)
**Platforms Supported:** LinkedIn, Facebook, Twitter, Instagram, WhatsApp, Gmail

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites Check
```bash
# 1. Verify directory structure exists
ls -la Pending_Approval Approved Done Logs

# 2. Verify Python dependencies
python -c "import playwright; print('✓ Playwright')"
python -c "import yaml; print('✓ PyYAML')"
python -c "import watchdog; print('✓ Watchdog')"

# 3. Verify scripts exist
ls -la scripts/trigger_posts.py scripts/master_orchestrator.py scripts/social_media_executor_v2.py
```

### Quick Single Test (5 minutes)
```bash
# Terminal 1: Start orchestrator
python scripts/master_orchestrator.py

# Terminal 2: Create a draft post (waits for approval)
python scripts/trigger_posts.py -p facebook -c "Test post from automation!" --preview

# Terminal 3: Approve and move to orchestrator
mv Pending_Approval/POST_*.md Approved/

# Watch Terminal 1 for success message (should complete in 10-30 seconds)
# Verify: ls Done/processed_POST_*.md
```

---

## 📖 Full Workflow Test (Step-by-Step)

### Phase 1: Setup & Preparation (5 minutes)

#### Step 1.1: Clean Environment
```bash
# Clear old test files (optional)
rm -f Pending_Approval/POST_test_*.md
rm -f Approved/POST_test_*.md
rm -f Done/processed_POST_test_*.md

# Create fresh test directory structure
mkdir -p Pending_Approval Approved Done Logs session

# Verify directories are clean
ls Pending_Approval  # Should be empty or only have old files
ls Approved         # Should be empty
ls Done            # Should be empty or have previous test files
```

#### Step 1.2: Check Browser Sessions (Critical for Playwright)
```bash
# If first time or browser login issues, ensure session folder exists
mkdir -p session

# List existing sessions (optional)
ls -la session/

# Note: Session folder contains persistent browser state
# If browser login fails, clear sessions and re-login manually once
```

#### Step 1.3: Verify Log Files
```bash
# Create Logs directory if missing
mkdir -p Logs

# Check today's logs (optional)
ls -la Logs/

# Tip: Logs/trigger_posts_*.log tracks draft creation
# Tip: Logs/orchestrator_*.log tracks orchestrator monitoring
# Tip: Logs/executor_*.log tracks executor posting
```

---

### Phase 2: Start Monitoring (2 minutes)

#### Terminal 1: Start Master Orchestrator
```bash
# This is the "brain" - monitors /Approved folder continuously
python scripts/master_orchestrator.py

# Expected output:
# ======================================================================
# Master Orchestrator v1.0 initialized
# Monitoring: /path/to/Approved
# Check interval: 5 seconds
# Max retries: 3
# Retry cooldown: 300 seconds
# 🔍 Starting orchestrator monitoring loop...
```

**⚠️ Keep this running - don't close this terminal!**

#### Terminal 2: Start Real-Time Log Monitoring
```bash
# Watch logs in real-time (useful for debugging)
tail -f Logs/orchestrator_*.log

# This shows:
# - When files are detected
# - When executor is called
# - Success/failure status
# - Retry scheduling if needed
```

#### Terminal 3: Real-Time JSON Status Watching
```bash
# Watch status updates (optional, shows pretty JSON)
watch -n 1 'cat Logs/status_*.json | python -m json.tool | tail -20'

# Or simpler - just cat the status file
cat Logs/status_*.json | python -m json.tool

# Shows:
# - Latest events
# - File processing status
# - Retry attempts
```

---

### Phase 3: Create Draft Posts (3 minutes)

#### Test 3.1: Single Platform Test (Facebook)
```bash
# Terminal 4: Create a test post for Facebook
python scripts/trigger_posts.py \
    -p facebook \
    -c "🚀 Testing AI Social Media Manager!" \
    -t "Test Post 1" \
    --preview

# Expected output:
# ✅ Post created: POST_20260329_101534_fac_abc123.md
# Platform: Facebook
# Content length: 42 chars
# Path: /absolute/path/to/Pending_Approval/POST_*.md
#
# ======================================================================
# 📝 POST PREVIEW
# ======================================================================
# [YAML frontmatter displayed]
# # Test Post 1
# 🚀 Testing AI Social Media Manager!
# ======================================================================
# ✅ Saved to: /path/to/Pending_Approval/POST_*.md
# ======================================================================
```

**Key Verification:**
- ✅ File created in `Pending_Approval/`
- ✅ Filename starts with `POST_`
- ✅ Contains YAML frontmatter
- ✅ Platform set to `facebook`
- ✅ Custom content preserved
- ✅ Status shows `pending_approval`

#### Test 3.2: Multi-Platform Test (5 posts)
```bash
# Create posts for multiple platforms to test orchestrator batch processing
python scripts/trigger_posts.py -p linkedin -c "LinkedIn test" -t "Test LI 1" --preview
python scripts/trigger_posts.py -p twitter -c "Twitter test" -t "Test TW 1" --preview
python scripts/trigger_posts.py -p instagram -c "Instagram test" -t "Test IG 1" --preview
python scripts/trigger_posts.py -p gmail -c "Email test body" -t "Test Email" --preview
python scripts/trigger_posts.py -p whatsapp -c "WhatsApp test" -t "Test WA 1" --preview

# All should appear in Pending_Approval/
ls -la Pending_Approval/POST_*.md | wc -l
# Should show: 5

# Verify each file
for f in Pending_Approval/POST_*.md; do
    echo "=== $(basename $f) ==="
    grep "^platform:" "$f"
done
```

---

### Phase 4: Human-In-The-Loop Approval (1 minute)

#### Test 4.1: Review Draft (Optional - for testing HITL workflow)
```bash
# Review the draft post before approval
cat Pending_Approval/POST_20260329_101534_fac_abc123.md

# Check:
# - Platform correct?
# - Content looks good?
# - Metadata complete?
# - Title appropriate?

# If rejected, move to Rejected/ folder instead:
# mkdir -p Rejected
# mv Pending_Approval/POST_*.md Rejected/
# (Orchestrator won't process rejected files)
```

#### Test 4.2: Approve and Move to Orchestrator
```bash
# Move ALL pending posts to Approved for orchestrator to process
mv Pending_Approval/POST_*.md Approved/

# Verify they moved
ls -la Approved/POST_*.md
# Should show: 5 files

# Verify Pending_Approval is now empty
ls Pending_Approval/
# Should be empty or show only non-POST files
```

**⚠️ CRITICAL:** Master Orchestrator only processes files in `/Approved/`

---

### Phase 5: Orchestrator Processing (10-30 seconds per file)

#### Terminal 1 Output (Master Orchestrator)
```
Watch Terminal 1 (where orchestrator is running) for:

======================================================================
📋 Processing: POST_20260329_101534_fac_abc123.md
Platform: facebook
Attempt: 1/4
======================================================================
🚀 Executing: POST_20260329_101534_fac_abc123.md

# [Waiting 10-30 seconds for executor to complete]

✅ Executor succeeded: POST_20260329_101534_fac_abc123.md
✅ SUCCESS: Moved to Done: processed_POST_20260329_101534_fac_abc123.md
```

#### Monitor 5 Files Processing
```bash
# Expected sequence (if you approved 5 files):
# 1. POST_*_fac_*.md → Processing → Done ✅ (1-2 min)
# 2. POST_*_lin_*.md → Processing → Done ✅ (1-2 min)
# 3. POST_*_tw_*.md  → Processing → Done ✅ (1-2 min)
# 4. POST_*_ig_*.md  → Processing → Done ✅ (1-2 min)
# 5. POST_*_wa_*.md  → Processing → Done ✅ (1-2 min)
#
# Total time: ~5-10 minutes for all 5

# Watch progress in Terminal 3
watch -n 2 'ls -la Done/processed_POST_*.md | wc -l'
# Should increment from 0 → 5
```

---

### Phase 6: Verification & Success (2 minutes)

#### Test 6.1: Check Successful Posts
```bash
# Files should move from Approved → Done automatically
ls -la Done/processed_POST_*.md

# Expected output: 5 files (or number you approved)
# processed_POST_20260329_101534_fac_abc123.md
# processed_POST_20260329_101540_lin_def456.md
# processed_POST_20260329_101545_tw_ghi789.md
# processed_POST_20260329_101551_ig_jkl012.md
# processed_POST_20260329_101556_wa_mno345.md

# Verify file count
ls Done/processed_POST_*.md | wc -l
# Should equal number you moved to Approved
```

#### Test 6.2: Verify No Files Left in Approved
```bash
# Approved should be empty (all processed)
ls Approved/POST_*.md

# Should show: "No such file or directory" or be empty
# If files remain, check:
# 1. Are they still being processed? (check Terminal 1)
# 2. Did they fail? (check Terminal 2 logs)
# 3. In retry cooldown? (check Logs/status_*.json)
```

#### Test 6.3: Check Executor Logs
```bash
# View executor output and platform-specific logs
ls -la Logs/

# Expected files:
# trigger_posts_2026-03-29.log
# orchestrator_2026-03-29.log
# executor_2026-03-29.log (if executor created its own log)

# Check for errors
grep -i "error\|failed\|exception" Logs/*.log | head -20

# Check for successes
grep -i "success\|completed\|✓" Logs/*.log | tail -20
```

#### Test 6.4: Verify Audit Trail
```bash
# Check audit logging for skill actions
cat Logs/audit_2026-03-29.json | python -m json.tool

# Should show entries for:
# - trigger_posts: skill_end with posts_created
# - master_orchestrator: file processing events
# - social_media_executor: posting attempts

# Count total logged actions
cat Logs/audit_2026-03-29.json | python -c "import json,sys; data=json.load(sys.stdin); print(f'Total actions: {len(data)}')"
```

---

## 🔄 Testing Error Scenarios

### Scenario 1: Browser Login Issue

**Symptom:** Executor fails on all platforms with "Unable to login" or timeout

**Root Cause:** Browser session expired or first-time login required

**Resolution:**
```bash
# Option 1: Clear session and re-login manually
rm -rf session/*

# Then run one simple test to trigger manual login:
python scripts/social_media_executor_v2.py test_file.md

# Browser will open, wait for manual login to complete
# Once logged in, session is saved for future runs

# Option 2: Check browser compatibility
# Verify Playwright browsers are installed
python -m playwright install

# Option 3: Check screen resolution
# Some platforms need minimum 1024x768
# Headless mode may fail on some sites - check code in social_media_executor_v2.py
```

### Scenario 2: Orchestrator Not Detecting Files

**Symptom:** Files in /Approved but orchestrator doesn't process them

**Root Cause:** Orchestrator not running, or check interval missed

**Resolution:**
```bash
# 1. Verify orchestrator is running
ps aux | grep master_orchestrator

# 2. Check if it's stuck
# Kill and restart
pkill -f master_orchestrator
sleep 2
python scripts/master_orchestrator.py

# 3. Manually move file AFTER orchestrator starts
mv Pending_Approval/POST_*.md Approved/

# 4. Check check interval (default 5 seconds)
# Edit scripts/master_orchestrator.py line 120:
# self.check_interval = 5  # Change if needed
```

### Scenario 3: Executor Timeout (Files Stuck in Approved)

**Symptom:** Files in /Approved for >30 seconds, no movement to Done

**Root Cause:** Browser interaction too slow, timeout exceeded

**Resolution:**
```bash
# Check logs for timeout error
grep -i "timeout" Logs/orchestrator_*.log

# Option 1: Increase timeout
# Edit scripts/master_orchestrator.py line 180:
# timeout=300  # Change from 300 to 600 (10 min)

# Option 2: Restart with more verbose logging
export DEBUG=1
python scripts/master_orchestrator.py

# Option 3: Manual intervention
# Kill executor if stuck
pkill -f social_media_executor

# Move file back to Pending for retest
mv Approved/POST_*.md Pending_Approval/
```

### Scenario 4: Post Format Error (YAML Invalid)

**Symptom:** "YAML parsing error" in logs

**Root Cause:** Trigger Posts generated invalid YAML

**Resolution:**
```bash
# Check YAML syntax
python -c "
import yaml
with open('Pending_Approval/POST_*.md') as f:
    content = f.read()
    # Extract YAML (between --- markers)
    yaml_part = content.split('---')[1]
    try:
        yaml.safe_load(yaml_part)
        print('✓ YAML valid')
    except Exception as e:
        print(f'✗ YAML error: {e}')
"

# Fix: Recreate post with proper title/content
python scripts/trigger_posts.py -p facebook -c "Test" --preview

# Verify file structure
head -20 Pending_Approval/POST_*.md
```

### Scenario 5: Retry Loop (File keeps failing)

**Symptom:** Same file appears in /Approved repeatedly, attempts increment

**Root Cause:** Platform interaction issue (selector changed, login expired, etc.)

**Resolution:**
```bash
# Check retry status
cat Logs/status_*.json | python -m json.tool | grep -A 5 "attempts"

# View error details
grep -B 5 "Attempt 2" Logs/orchestrator_*.log

# Option 1: Manual screenshot for debugging
# Check if error screenshots exist
ls -la Logs/error_*.png

# Option 2: Disable retry and move to manual
rm Approved/POST_*.md
echo "Moved to manual processing"

# Option 3: Fix the platform-specific selector
# Edit scripts/social_media_executor_v2.py
# Find the platform method (post_to_facebook, etc.)
# Update selectors based on current website structure
# Restart test
```

---

## 📊 Real-Time Monitoring Dashboard

### Setup Multi-Terminal View (Recommended)

```bash
# This command opens a tmux session with all monitors:
# Terminal 1: Orchestrator
# Terminal 2: Live logs
# Terminal 3: File count tracking
# Terminal 4: Manual commands

tmux new-session -d -s test \
  -x 200 -y 50

# Create 4 panes
tmux split-window -t test -h
tmux split-window -t test:0.0 -v
tmux split-window -t test:0.1 -v

# Panel 0 (top-left): Orchestrator
tmux send-keys -t test:0.0 "cd '$(pwd)' && python scripts/master_orchestrator.py" C-m

# Panel 1 (bottom-left): Live logs
tmux send-keys -t test:0.1 "tail -f Logs/orchestrator_*.log" C-m

# Panel 2 (top-right): File tracking
tmux send-keys -t test:0.2 "while true; do clear; echo '=== Workflow Status ==='; echo 'Pending:'; ls Pending_Approval/POST_*.md 2>/dev/null | wc -l; echo 'Approved:'; ls Approved/POST_*.md 2>/dev/null | wc -l; echo 'Done:'; ls Done/processed_POST_*.md 2>/dev/null | wc -l; sleep 2; done" C-m

# Panel 3 (bottom-right): Command input
tmux send-keys -t test:0.3 "cd '$(pwd)' && bash" C-m

# Attach to session
tmux attach -t test

# In bottom-right panel, you can run commands:
# python scripts/trigger_posts.py -p facebook -c "Test"
# mv Pending_Approval/POST_*.md Approved/
```

### Manual Monitoring (Without tmux)

```bash
# Terminal 1: Orchestrator
python scripts/master_orchestrator.py

# Terminal 2: Live log tail
tail -f Logs/orchestrator_*.log

# Terminal 3: File counter script
cat > watch_files.sh << 'EOF'
#!/bin/bash
while true; do
    clear
    echo "=== WORKFLOW STATUS ==="
    echo "Pending Approval:"
    ls Pending_Approval/POST_*.md 2>/dev/null | wc -l
    echo ""
    echo "Approved (processing):"
    ls Approved/POST_*.md 2>/dev/null | wc -l
    echo ""
    echo "Done (completed):"
    ls Done/processed_POST_*.md 2>/dev/null | wc -l
    echo ""
    echo "Last update: $(date '+%H:%M:%S')"
    sleep 2
done
EOF

chmod +x watch_files.sh
./watch_files.sh

# Terminal 4: Command line for manual operations
# Ready to run trigger_posts or move files
```

---

## ✅ Complete Test Checklist

Run through this checklist for comprehensive validation:

### Pre-Test Setup
- [ ] Directories exist: Pending_Approval, Approved, Done, Logs, session
- [ ] Python packages installed: playwright, pyyaml, watchdog
- [ ] Scripts exist: trigger_posts.py, master_orchestrator.py, social_media_executor_v2.py
- [ ] Browser sessions cleared (if first time): `rm -rf session/*`

### Phase 1: Orchestrator Running
- [ ] Master Orchestrator started with `python scripts/master_orchestrator.py`
- [ ] Terminal shows "Starting orchestrator monitoring loop..."
- [ ] Check interval: 5 seconds (shown in output)
- [ ] Max retries: 3 (shown in output)
- [ ] Watching for POST_*.md files

### Phase 2: Draft Creation
- [ ] Trigger Posts runs without errors
- [ ] File created in Pending_Approval/
- [ ] Filename format: POST_YYYYMMDD_HHMMSS_[platform]_[hash].md
- [ ] YAML frontmatter present and valid
- [ ] Platform set correctly
- [ ] Custom content preserved exactly
- [ ] Status shows "pending_approval"
- [ ] Preview displays correctly

### Phase 3: Human Approval
- [ ] Draft reviewed (optional, just for demo)
- [ ] File moved from Pending_Approval/ to Approved/
- [ ] Orchestrator should detect within 5 seconds
- [ ] Log shows "📋 Processing: POST_*"

### Phase 4: Executor Processing
- [ ] Orchestrator shows "🚀 Executing: POST_*"
- [ ] Browser opens (visible or headless)
- [ ] Platform login successful (or uses saved session)
- [ ] Post content filled in correctly
- [ ] Posting action initiated
- [ ] Executor completes (status shows ✅)
- [ ] File moved from Approved/ to Done/

### Phase 5: Success Verification
- [ ] File in Done/ folder: processed_POST_*
- [ ] No errors in Logs/orchestrator_*.log
- [ ] Logs/audit_*.json has entries for skill actions
- [ ] Pending_Approval/ is empty
- [ ] Approved/ is empty
- [ ] Done/ has all processed files

### Error Handling
- [ ] If browser fails: Session cleared, re-login attempted ✅
- [ ] If executor timeout: File stays in Approved for retry ✅
- [ ] If YAML invalid: Clear error message in logs ✅
- [ ] If network issue: Automatic retry after cooldown ✅

---

## 📈 Expected Performance

| Component | Time | Notes |
|-----------|------|-------|
| Trigger Posts creation | 1-2 sec | File I/O + YAML generation |
| File detection | 5 sec | Check interval default |
| Executor startup | 2-3 sec | Browser launch + connection |
| Platform login | 5-10 sec | First time or session expired |
| Post content interaction | 5-10 sec | Fill form + click buttons |
| File movement | <1 sec | File system operation |
| **Total per post** | **20-35 sec** | Typical end-to-end |
| **Batch (5 posts)** | **100-175 sec** | Sequential processing |

---

## 🎯 Test Scenarios by Use Case

### Use Case 1: Quick Single Post Test
**Time:** 5 minutes
```bash
# Terminal 1
python scripts/master_orchestrator.py

# Terminal 2 (wait 3 seconds, then run)
python scripts/trigger_posts.py -p facebook -c "Quick test" && \
mv Pending_Approval/POST_*.md Approved/

# Watch Terminal 1 for completion
```

### Use Case 2: Multi-Platform Batch Test
**Time:** 15-20 minutes
```bash
# Terminal 1
python scripts/master_orchestrator.py

# Terminal 2
for platform in linkedin facebook twitter instagram; do
    python scripts/trigger_posts.py -p "$platform" -c "Batch test $platform"
    sleep 1
done

# Terminal 3
mv Pending_Approval/POST_*.md Approved/

# Watch all 4 posts process sequentially
```

### Use Case 3: Error Recovery Test
**Time:** 20-30 minutes
```bash
# Test retry logic and error handling
python scripts/master_orchestrator.py

# Simulate platform unavailable (stop browser manually mid-post)
python scripts/trigger_posts.py -p facebook -c "Test with intentional failure"
mv Pending_Approval/POST_*.md Approved/

# Monitor retry attempts in logs
# After ~5 minutes cooldown, retry automatically
# Should succeed on retry
```

### Use Case 4: Continuous Operation Test
**Time:** 60+ minutes
```bash
# Test system stability over extended period
python scripts/master_orchestrator.py

# Generate posts randomly over 1 hour
for i in {1..10}; do
    sleep 360  # Every 6 minutes
    platform=$(shuf -e linkedin facebook twitter instagram | head -1)
    python scripts/trigger_posts.py -p "$platform" -c "Post #$i"
    mv Pending_Approval/POST_*.md Approved/
done

# Monitor for:
# - All posts succeed
# - No memory leaks
# - No connection resets
# - Consistent processing time
```

---

## 🔧 Troubleshooting Tips

### Issue: "Permission denied" on script files
```bash
chmod +x scripts/trigger_posts.py scripts/master_orchestrator.py scripts/social_media_executor_v2.py
```

### Issue: "Module not found" errors
```bash
pip install playwright pyyaml watchdog
python -m playwright install
```

### Issue: "Port already in use" or "Address already in use"
```bash
# Kill existing process
pkill -f master_orchestrator
pkill -f trigger_posts

# Wait 3 seconds
sleep 3

# Restart
python scripts/master_orchestrator.py
```

### Issue: Files not moving to Done
```bash
# Check executor is working
python scripts/social_media_executor_v2.py Approved/POST_test.md

# Check file permissions
ls -la Approved/
chmod 755 Done/

# Check disk space
df -h

# Restart orchestrator
pkill -f master_orchestrator
python scripts/master_orchestrator.py
```

### Issue: Stale Session (Browser Won't Login)
```bash
# Clear all saved browser sessions
rm -rf session/*

# On next run, browser will prompt for manual login
# Complete login, then session is saved for future use

# Verify session saved
ls -la session/
```

### Issue: "Timeout waiting for browser"
```bash
# Increase timeout in master_orchestrator.py
# Find line with: timeout=300
# Change to: timeout=600  (10 minutes)

# Or increase in social_media_executor_v2.py:
# Find: await page.goto(..., wait_until="networkidle")
# Ensure page load strategies are optimized
```

---

## 📝 Log Analysis Guide

### Check for Success
```bash
grep "SUCCESS\|✓\|Moved to Done" Logs/orchestrator_*.log
```

### Check for Failures
```bash
grep "FAILED\|✗\|Error\|Exception" Logs/orchestrator_*.log
```

### Check Retry Activity
```bash
grep "retry\|cooldown\|Attempt" Logs/orchestrator_*.log
```

### Check Skill Audit Trail
```bash
cat Logs/audit_*.json | python -m json.tool | grep -A 3 "skill_end"
```

### Check Executor Logs
```bash
grep "Executing\|Platform\|screenshot" Logs/*.log
```

---

## ✨ Success Indicators

✅ **Full Workflow Success:**
1. ✅ Draft created with `trigger_posts.py`
2. ✅ File moved from Pending_Approval → Approved (manual)
3. ✅ Orchestrator detected within 5 seconds
4. ✅ Executor launched and posted to platform
5. ✅ File moved from Approved → Done
6. ✅ No errors in logs
7. ✅ Audit trail recorded

**Sample Success Log:**
```
2026-03-29 10:15:34 - INFO - ✅ Post created: POST_20260329_101534_fac_abc123.md
2026-03-29 10:15:35 - INFO - 🔍 Starting orchestrator monitoring loop...
2026-03-29 10:15:40 - INFO - 📋 Processing: POST_20260329_101534_fac_abc123.md
2026-03-29 10:15:40 - INFO - 🚀 Executing: POST_20260329_101534_fac_abc123.md
2026-03-29 10:15:50 - INFO - ✅ Executor succeeded: POST_20260329_101534_fac_abc123.md
2026-03-29 10:15:50 - INFO - ✅ SUCCESS: Moved to Done: processed_POST_20260329_101534_fac_abc123.md
```

---

## 📞 Quick Reference

### Start Full System
```bash
# Terminal 1: Orchestrator
python scripts/master_orchestrator.py

# Terminal 2: Create post
python scripts/trigger_posts.py -p [platform] -c "[content]" --preview

# Terminal 3: Approve post
mv Pending_Approval/POST_*.md Approved/

# Terminal 1: Watch success
# (Check logs and /Done folder)
```

### Monitor Status
```bash
# Check pending approvals
ls Pending_Approval/ | wc -l

# Check approved posts (processing)
ls Approved/ | wc -l

# Check completed posts
ls Done/ | wc -l

# Check errors
grep -i error Logs/*.log | tail -10
```

### Reset Everything
```bash
# Clear all test files
rm -f Pending_Approval/POST_test_*.md
rm -f Approved/POST_test_*.md
rm -f Done/processed_POST_test_*.md

# Keep logs for analysis (optional)
# rm -f Logs/*

# Restart system
pkill -f master_orchestrator
sleep 2
python scripts/master_orchestrator.py
```

---

## 🎓 Learning Outcomes

After completing this test, you understand:

1. **Trigger Posts** - How draft generation works with YAML metadata
2. **Manual Approval** - HITL workflow (Pending_Approval → Approved)
3. **Auto Orchestration** - How Master Orchestrator monitors /Approved
4. **Async Execution** - How Social Media Executor posts to platforms
5. **Error Handling** - Retry logic, cooldown, and recovery
6. **Logging & Audit** - How to track actions and troubleshoot
7. **Performance** - Expected timing for each step
8. **Troubleshooting** - How to diagnose and fix issues

---

## 🚀 Next Steps

### After Successful Test
1. ✅ Deploy to production (or PM2 scheduler)
2. ✅ Set up monitoring alerts
3. ✅ Run end-of-week validation
4. ✅ Review audit logs for patterns
5. ✅ Optimize slow platforms

### Production Deployment
```bash
# Add to PM2 (process manager)
pm2 start scripts/master_orchestrator.py --name orchestrator
pm2 start scripts/trigger_posts.py --name trigger_posts --cron "0 9 * * *"

# Save PM2 config
pm2 save

# Enable auto-restart on reboot
pm2 startup
```

### Continuous Monitoring
```bash
# Watch orchestrator status
pm2 monit

# View logs
pm2 logs orchestrator

# Check health
pm2 status
```

---

## 📋 Test Report Template

```markdown
# Test Report - AI Social Media Manager Workflow

**Date:** 2026-03-29
**Tester:** [Your Name]
**System:** [Your Machine]

## Test Results

### Pre-Test
- [ ] All directories ready
- [ ] All scripts executable
- [ ] All dependencies installed

### Test Execution
- [ ] Orchestrator started successfully
- [ ] Draft created successfully
- [ ] File approved and moved
- [ ] Executor detected and ran
- [ ] Post created/delivered
- [ ] File moved to Done

### Success Metrics
- Total posts tested: __
- Successful posts: __ / __ (__ %)
- Failed posts: __
- Average time per post: __ seconds
- Total time: __ minutes

### Issues Found
- [ ] None
- [ ] Browser login failed (resolved: ___)
- [ ] Executor timeout (resolved: ___)
- [ ] File format issue (resolved: ___)
- [ ] Other: ___

### Recommendations
- [ ] Ready for production
- [ ] Need optimization
- [ ] More testing needed

**Signed:** ___________
```

---

**Last Updated:** 2026-03-29
**Status:** PRODUCTION TEST READY
**Next Review:** After first live deployment
