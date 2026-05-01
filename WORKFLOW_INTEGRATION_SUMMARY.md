---
title: AI Social Media Manager - Complete Workflow Integration
date: 2026-03-29
status: PRODUCTION READY
version: 1.0
---

# AI Social Media Manager - Complete Workflow Integration

## 📋 System Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    AI SOCIAL MEDIA MANAGER WORKFLOW                      │
└──────────────────────────────────────────────────────────────────────────┘

  DRAFT CREATION           HUMAN APPROVAL          AUTO EXECUTION           COMPLETION
  ──────────────          ──────────────          ──────────────           ──────────

┌─────────────────┐      ┌─────────────┐      ┌──────────────────┐      ┌────────────┐
│ Trigger Posts   │ ──→  │   HITL      │ ──→  │ Master           │ ──→  │ Social     │
│  script         │      │ Approval    │      │ Orchestrator     │      │ Media      │
│                 │      │ (Manual)    │      │ (Auto Monitor)   │      │ Executor   │
└─────────────────┘      └─────────────┘      └──────────────────┘      └────────────┘
        │                      │                      │                        │
        │                      │                      │                        │
        ↓                      ↓                      ↓                        ↓
   /Pending_         /Approved                  /Approved                  /Done/
   Approval/         (after approval)           (detecting files)          processed_*

   Platform-        User reviews        5-second check     Posts to Facebook
   specific          content and         interval           LinkedIn
   templates         manually moves      Executes executor  Twitter
                     to Approved                            Instagram
                                                            WhatsApp
                                                            Gmail

Time: 1-2s          Time: Manual         Time: <5s          Time: 10-30s per post
      (creation)         (review)         (detection)        (posting)
```

---

## 🏗️ Architecture & Components

### 1. Trigger Posts Script
**File:** `scripts/trigger_posts.py`

**Purpose:** Generate draft posts with YAML metadata

**Features:**
- Command-line interface for easy post creation
- 6 platform support (linkedin, facebook, twitter, instagram, whatsapp, gmail)
- YAML frontmatter generation with metadata
- Automatic filename generation (timestamp + platform + hash)
- Optional --move flag for auto-approval
- Default content templates for each platform

**Usage:**
```bash
python scripts/trigger_posts.py \
    --platform facebook \
    --content "Your post content" \
    --title "Post Title" \
    --preview
```

**Output:** `/Pending_Approval/POST_YYYYMMDD_HHMMSS_[platform]_[hash].md`

**Integration Points:**
- Reads from: Company_Handbook.md (optional tone guidelines)
- Writes to: Pending_Approval/ folder
- Logs to: Logs/trigger_posts_YYYY-MM-DD.log
- Records in: Logs/audit_YYYY-MM-DD.json

---

### 2. Master Orchestrator
**File:** `scripts/master_orchestrator.py`

**Purpose:** Autonomous monitoring and workflow orchestration

**Key Features:**
- Watchdog-based folder monitoring (5-second check interval)
- Detects POST_*.md files in /Approved folder
- Launches Social Media Executor with proper parameters
- Retry logic (3 attempts + 5-minute cooldown)
- File state tracking (pending, processing, success, failed, retry, cooldown)
- Moves successful files to /Done/
- Automatic logging and status tracking

**Workflow:**
```
1. Monitor /Approved/ continuously
2. Detect POST_*.md file
3. Extract metadata (platform, etc.) from YAML
4. Launch executor: python social_media_executor_v2.py <file>
5. Wait for completion (timeout: 300 seconds)
6. If success: move to /Done/ (rename to processed_POST_*.md)
7. If failure: check retry attempts
   - If < 3: schedule cooldown (5 min)
   - If >= 3: mark failed, stay in /Approved
8. Next retry: automatic after cooldown expires
```

**Output Files:**
- `/Done/processed_POST_*.md` - Successfully executed
- `/Logs/orchestrator_YYYY-MM-DD.log` - Activity log
- `/Logs/status_YYYY-MM-DD.json` - Status tracking

**Configuration (lines 120-122):**
```python
self.check_interval = 5          # Check every 5 seconds
self.max_retries = 3            # Max 3 retry attempts
self.retry_cooldown = 300       # 5-minute cooldown between retries
```

---

### 3. Social Media Executor v2.0
**File:** `scripts/social_media_executor_v2.py`

**Purpose:** Automated posting to social platforms

**Key Features:**
- Playwright async/await for browser automation
- Persistent session management (no re-login)
- 6 platform support with platform-specific posting logic
- Retry logic with exponential backoff (2s → 4s → 8s)
- Error screenshot capture for debugging
- YAML + Markdown file format parsing
- File movement workflow (Approved → Done)

**Platform-Specific Logic:**
- **LinkedIn**: Detect "Start a post" button → fill contenteditable div → click Post
- **Facebook**: "What's on your mind" → Next → Post/Share buttons
- **Twitter**: Tweet compose → fill content → Tweet button
- **Instagram**: New post workflow → photo/content → Share
- **WhatsApp**: Contact search → message field → send
- **Gmail**: Compose → to/subject/body → send

**Session Management:**
- Sessions stored in `/session/` folder
- Browser data persists between runs
- If login fails: clear `/session/*` and re-login manually once

**Error Handling:**
```python
# On error:
1. Screenshot saved: Logs/error_[platform]_[timestamp]_attempt[n].png
2. Retry attempted: up to 3 times with backoff
3. If all fail: file stays in /Approved, orchestrator schedules cooldown
```

---

## 📊 Data Flow & File Formats

### Trigger Posts Output
**File:** `/Pending_Approval/POST_20260329_101534_fac_abc123.md`

```yaml
---
platform: facebook
title: LinkedIn Professional Post
from: trigger_posts
type: facebook_post
priority: medium
status: pending_approval
created_at: 2026-03-29T10:15:34.123456
requires_approval: true
---

# LinkedIn Professional Post

Your post content goes here.

---

## Status
- **Platform:** Facebook
- **Status:** Pending Approval
- **Created:** 2026-03-29 10:15:34

**Next Step:** Move to /Approved to trigger publishing via Master Orchestrator
```

### Orchestrator Status Tracking
**File:** `/Logs/status_YYYY-MM-DD.json`

```json
[
  {
    "timestamp": "2026-03-29T10:15:34.123456",
    "event": "file_detected",
    "filename": "POST_20260329_101534_fac_abc123.md",
    "details": {
      "platform": "facebook",
      "attempts": 1
    }
  },
  {
    "timestamp": "2026-03-29T10:15:49.654321",
    "event": "success",
    "filename": "POST_20260329_101534_fac_abc123.md",
    "details": {
      "platform": "facebook",
      "attempts": 1,
      "processing_time_sec": 15
    }
  }
]
```

### Audit Trail
**File:** `/Logs/audit_YYYY-MM-DD.json`

```json
[
  {
    "timestamp": "2026-03-29T10:15:34.123456",
    "action_type": "skill_start",
    "actor": "social_media_executor",
    "target": "Approved/POST_*.md",
    "status": "started",
    "details": {"platform": "facebook"}
  },
  {
    "timestamp": "2026-03-29T10:15:49.654321",
    "action_type": "skill_end",
    "actor": "social_media_executor",
    "target": "Done/processed_POST_*.md",
    "status": "completed",
    "details": {"duration_ms": 15000, "platform": "facebook"}
  }
]
```

---

## 🚀 Complete Workflow Example

### Scenario: Post Company Announcement

#### Step 1: Create Draft (Trigger Posts)
```bash
python scripts/trigger_posts.py \
    -p linkedin \
    -c "Excited to announce our new AI-powered social media manager! 🚀" \
    -t "Announcing Our Latest Innovation" \
    --preview
```

**Output:**
- File created: `Pending_Approval/POST_20260329_101534_lin_abc123.md`
- Log entry: `Logs/trigger_posts_2026-03-29.log`
- Audit entry: `Logs/audit_2026-03-29.json`

#### Step 2: Human Approval
Marketing Manager reviews the draft:
- ✓ Content looks good
- ✓ Grammar correct
- ✓ Brand-aligned

Approves by moving file:
```bash
mv Pending_Approval/POST_20260329_101534_lin_abc123.md Approved/
```

#### Step 3: Auto Orchestration (Master Orchestrator)
```
[10:15:39] 🔍 File detected: POST_20260329_101534_lin_abc123.md
[10:15:39] 📋 Processing: POST_*.md
[10:15:39] Platform: linkedin
[10:15:39] 🚀 Executing: social_media_executor_v2.py ...
[10:15:49] ✅ Executor succeeded
[10:15:49] ✅ SUCCESS: Moved to Done: processed_POST_20260329_101534_lin_abc123.md
```

#### Step 4: Completion
- File moved to: `Done/processed_POST_20260329_101534_lin_abc123.md`
- Post visible on LinkedIn within seconds
- Audit trail complete with timestamps

**Total Time:** ~30 seconds (after approval)

---

## 🧪 Testing the Complete Workflow

### Quick Test (5 minutes)
```bash
# Start orchestrator
python scripts/master_orchestrator.py

# In another terminal: create, approve, and monitor
python scripts/run_workflow_test.py --platform facebook --count 1
```

### Full Test (15 minutes)
```bash
# Test all 6 platforms
python scripts/run_workflow_test.py --batch
```

### Manual Step-by-Step
```bash
# Terminal 1: Start orchestrator
python scripts/master_orchestrator.py

# Terminal 2: Create draft
python scripts/trigger_posts.py -p facebook -c "Test" --preview

# Terminal 3: Monitor logs
tail -f Logs/orchestrator_*.log

# Terminal 4: Approve file
mv Pending_Approval/POST_*.md Approved/

# Watch Terminal 2 for success message
```

**See:** `TEST_QUICK_START.md` and `docs/social_automation_test.md`

---

## 📈 Performance Metrics

| Operation | Time | Notes |
|-----------|------|-------|
| Draft creation | 1-2s | File I/O + YAML |
| File detection | 5s | Default check interval |
| Executor startup | 2-3s | Browser launch |
| Platform login | 5-10s | First time or session expired |
| Content interaction | 5-10s | Form filling + button clicks |
| File movement | <1s | File system |
| **Total per post** | **20-35s** | Typical end-to-end |

### Batch Processing
- **5 posts:** 100-175 seconds
- **10 posts:** 200-350 seconds
- Sequential processing (one at a time)

---

## 🔒 Error Handling & Recovery

### Scenario 1: Browser Login Fails
**Recovery:**
1. Clear session: `rm -rf session/*`
2. Run executor again
3. Browser prompts for manual login
4. Session automatically saved for future use

### Scenario 2: Platform Selector Changed
**Recovery:**
1. Check error screenshot: `Logs/error_[platform]_*.png`
2. Update platform method in `social_media_executor_v2.py`
3. Rerun test

### Scenario 3: Timeout (File Stuck in Approved)
**Recovery:**
1. Check logs for error details
2. Manually clear session if needed
3. Orchestrator automatically retries after 5-minute cooldown
4. Automatic retry up to 3 times total

### Scenario 4: Network Failure
**Recovery:**
1. Automatically retried (3 attempts)
2. 5-minute cooldown between attempts
3. After max retries, file stays in Approved for manual intervention

---

## 📊 System Status Indicators

### Healthy System
✅ Orchestrator running (check: `ps aux | grep master_orchestrator`)
✅ New files appear in `/Done/` within 30s of approval
✅ No errors in logs
✅ Audit trail shows completed actions
✅ Session folder has browser data

### Problem Indicators
❌ Files stuck in `/Approved/` for >60 seconds
❌ Orchestrator not running
❌ Browser login fails repeatedly
❌ Errors in logs (grep "✗" or "FAILED")
❌ Empty session folder

---

## 🎯 Integration Points

### With Existing Systems
- **Ralph Wiggum Loop**: Can call trigger_posts to generate drafts
- **HITL Approval Handler**: Reviews files in Pending_Approval
- **Email MCP Server**: Can notify on completion
- **PM2 Scheduler**: Cron jobs can trigger posting schedule
- **Audit Logger**: Records all skill actions automatically

### With External Platforms
- **LinkedIn**: API + Playwright automation
- **Facebook**: Playwright automation
- **Twitter**: Playwright automation
- **Instagram**: Playwright automation
- **WhatsApp**: Playwright automation (Web)
- **Gmail**: Playwright automation

### Monitoring & Logging
- **Trigger Posts Log**: `Logs/trigger_posts_*.log`
- **Orchestrator Log**: `Logs/orchestrator_*.log`
- **Executor Log**: `Logs/executor_*.log` (if created)
- **Audit Trail**: `Logs/audit_*.json`
- **Status Tracking**: `Logs/status_*.json`
- **Error Screenshots**: `Logs/error_*.png`

---

## 📝 Configuration & Customization

### Trigger Posts
- Default content templates: `SUPPORTED_PLATFORMS` dict (line 45)
- File naming format: `POST_[timestamp]_[platform]_[hash]`
- Output directory: `Pending_Approval/`

### Master Orchestrator
- Check interval: `self.check_interval = 5` (line 120)
- Max retries: `self.max_retries = 3` (line 121)
- Retry cooldown: `self.retry_cooldown = 300` (line 122, 300s = 5min)
- Executor timeout: `timeout=300` (line 180, 300s = 5min)

### Social Media Executor
- Browser headless mode: `headless=True` (default)
- Timeout for page loads: `wait_until="networkidle"`
- Retry backoff: 2s → 4s → 8s
- Screenshot on error: `Logs/error_[platform]_*.png`

---

## 🚀 Deployment

### Development
```bash
# Run all 3 components in separate terminals
python scripts/trigger_posts.py -p facebook -c "test"
python scripts/master_orchestrator.py
python scripts/social_media_executor_v2.py file.md
```

### Production (PM2)
```bash
# Register orchestrator as service
pm2 start scripts/master_orchestrator.py --name orchestrator
pm2 start scripts/trigger_posts.py --name trigger_posts --cron "0 9 * * *"

# Save and enable auto-restart
pm2 save
pm2 startup
```

### Docker (Future)
```dockerfile
# Would mount /Approved, /Logs volumes
# Run orchestrator + executor together
```

---

## 📞 Quick Reference

### Check System Status
```bash
# Is orchestrator running?
ps aux | grep master_orchestrator

# How many posts pending/approved/done?
echo "Pending: $(ls Pending_Approval/POST_*.md 2>/dev/null | wc -l)"
echo "Approved: $(ls Approved/POST_*.md 2>/dev/null | wc -l)"
echo "Done: $(ls Done/processed_POST_*.md 2>/dev/null | wc -l)"

# Any errors?
grep "✗\|FAILED\|Error" Logs/*.log | tail -10
```

### Common Commands
```bash
# Start orchestrator
python scripts/master_orchestrator.py

# Create post
python scripts/trigger_posts.py -p facebook -c "Post content"

# Run tests
python scripts/run_workflow_test.py

# Clear test files
rm -f Pending_Approval/POST_test_*.md Approved/POST_test_*.md Done/processed_POST_test_*.md

# Reset and restart
pkill -f master_orchestrator
rm -rf session/*
python scripts/master_orchestrator.py
```

### Monitoring
```bash
# Real-time logs
tail -f Logs/orchestrator_*.log

# Status JSON
cat Logs/status_*.json | python -m json.tool

# Audit trail
cat Logs/audit_*.json | python -m json.tool
```

---

## 📚 Documentation

| Document | Purpose | When to Read |
|----------|---------|--------------|
| `TEST_QUICK_START.md` | Quick test commands | Getting started |
| `docs/social_automation_test.md` | Detailed test guide | Full testing, troubleshooting |
| `TRIGGER_POSTS_QUICK_START.md` | Draft creation | Creating posts |
| `MASTER_ORCHESTRATOR_README.md` | Orchestrator details | Understanding monitoring |
| `SOCIAL_MEDIA_EXECUTOR_README.md` | Posting details | Platform-specific posting |
| `WORKFLOW_INTEGRATION_SUMMARY.md` | This file | Architecture overview |

---

## ✅ Success Criteria

✅ Complete workflow successful when:
1. Draft created with `trigger_posts.py`
2. File moves to `/Pending_Approval/`
3. User reviews and approves (manual)
4. File moves to `/Approved/`
5. Orchestrator detects within 5 seconds
6. Executor posts to platform
7. File moves to `/Done/`
8. No errors in logs
9. Audit trail complete

---

## 🎓 Learning Path

1. **Read:** This document (architecture overview)
2. **Test:** `TEST_QUICK_START.md` (5-minute test)
3. **Deep Dive:** `docs/social_automation_test.md` (detailed guide)
4. **Troubleshoot:** Find your issue in test guide
5. **Deploy:** Use PM2 or Docker for production
6. **Monitor:** Watch `Logs/` folder for activity

---

## 🏁 Status

**Project:** AI Social Media Manager - Complete Workflow
**Version:** 1.0
**Date:** 2026-03-29
**Status:** ✅ PRODUCTION READY

All components implemented, tested, and documented. Ready for deployment and 24/7 operation.

---

**Last Updated:** 2026-03-29
**Next Review:** After first week of production monitoring
