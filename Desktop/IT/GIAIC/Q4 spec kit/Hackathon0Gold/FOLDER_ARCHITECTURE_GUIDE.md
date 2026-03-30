---
title: Semi-Autonomous AI Social Media Manager - Unified Folder Architecture
date: 2026-03-29
status: VERIFIED & COMPLETE
---

# Unified Folder Architecture for Semi-Autonomous AI Social Media Manager

## Required Folders Status

✅ **Pending_Approval** (exists)
✅ **Approved** (exists)
✅ **Done** (exists)
✅ **session** (exists)
✅ **Logs** (exists)

All required folders for the Semi-Autonomous AI Social Media Manager are already created in your project directory.

---

## Folder Descriptions

### 1. **Pending_Approval** - Drafted Posts Awaiting Review
**Purpose:** Holds AI-generated draft posts waiting for human approval
**File Format:** Markdown with YAML frontmatter metadata
**Content Example:**
```yaml
---
platform: facebook
from: automation@system
timestamp: 2026-03-29T10:00:00
priority: medium
status: pending_approval
---

# Draft: New Product Launch

Check out our latest innovation...
```
**Workflow:** AI creates draft → Stored here → Human reviews → Moves to Approved or Rejected

**Current Status:** 65 files pending review

---

### 2. **Approved** - Human-Approved Posts Ready for Publishing
**Purpose:** Posts that have been manually approved by human operator
**Action:** Human moves files here from Pending_Approval after review
**Next Step:** AI monitors this folder and publishes posts to social platforms
**Automation:**
- AI reads files
- Posts to Facebook, Instagram, Twitter, LinkedIn
- Moves completed files to Done/

**Current Status:** 32 files ready to publish

---

### 3. **Done** - Successfully Published Posts
**Purpose:** Archive of posts that have been successfully published
**Action:** AI automatically moves files here after successful posting
**Contains:**
- Published posts with confirmation timestamps
- Engagement metrics (if captured)
- Platform-specific post IDs
- Success confirmation metadata

**File Movement:** Approved/ → Done/ (after successful platform posting)

**Current Status:** 2 files archived

---

### 4. **session** - Persistent Browser Session Data
**Purpose:** Maintains authenticated browser sessions for social platforms
**Content:**
- Playwright session files for Facebook, Instagram, Twitter, LinkedIn
- Persistent login tokens and cookies
- Browser profile data
- User authentication state

**Platforms Managed:**
- 📱 Facebook Messenger
- 📷 Instagram Direct Messages
- 🐦 Twitter/X
- 💼 LinkedIn

**Use Case:** Keeps 24/7 monitoring watchers logged in without re-authentication
**Maintenance:** Auto-recovered on watcher restart via exponential backoff

**Current Status:** 12 session files

---

### 5. **Logs** - Error Screenshots & Event Logging
**Purpose:** Centralized logging for debugging, errors, and audit trail
**Log Types:**

#### a) **Audit Trail** (`audit_YYYY-MM-DD.json`)
- Centralized JSON log of all system actions
- Every skill start/end, file moved, error logged
- 90-day automatic retention cleanup
- Format: `[{timestamp, action_type, actor, status, details}, ...]`

#### b) **Error Logs** (`error_*.log`)
- Watcher error logs: `error_[watcher-name]_YYYY-MM-DD.log`
- Skill error logs: `skill_error_YYYY-MM-DD.md`
- Includes exception type, message, traceback
- Screenshots of failures (for UI debugging)

#### c) **Event Logs**
- System events (startup, shutdown, recovery)
- Skill execution logs
- Message capture logs

**Examples:**
```
Logs/
├── audit_2026-03-29.json          (central action trail)
├── error_facebook_2026-03-29.log  (watcher errors)
├── error_twitter_2026-03-29.log   (watcher errors)
├── skill_error_2026-03-29.md      (skill exceptions)
├── facebook_screenshot_001.png    (failure screenshot)
└── system_events_2026-03-29.log   (startup/recovery)
```

**Current Status:** 8 log files

---

## Complete Workflow Pipeline

```
Message Capture (6 Watchers)
        ↓
  Needs_Action/
        ↓
  Plans/ (AI analysis)
        ↓
Pending_Approval/ ← HUMAN REVIEW POINT
        ↓
  Approved/ ← HUMAN APPROVAL REQUIRED
        ↓
  Publishing (AI posts to platforms)
        ↓
   Done/ (Archive)
        ↓
Logs/ (Audit trail + Error tracking)
```

---

## Folder Structure Overview

```
Hackathon0Gold/
│
├── Pending_Approval/       (65 files) → AI-drafted posts waiting review
├── Approved/               (32 files) → Approved posts ready for publishing
├── Done/                   (2 files)  → Successfully published posts
├── session/                (12 files) → Persistent browser sessions
└── Logs/                   (8 files)  → Error logs & audit trail
```

---

## Key Metrics

| Folder | Files | Purpose |
|--------|-------|---------|
| **Pending_Approval** | 65 | Awaiting human review |
| **Approved** | 32 | Ready for publication |
| **Done** | 2 | Published & archived |
| **session** | 12 | Active sessions |
| **Logs** | 8 | Audit & error tracking |
| **TOTAL** | **119** | **Complete workflow** |

---

## HITL (Human-In-The-Loop) Checkpoint

**Critical Point:** Approved folder

```
⚠️ Manual Action Required Here:
  1. Review draft in Pending_Approval/
  2. Edit if needed
  3. Move to Approved/ (manual file move or tool)
  4. ✅ AI automatically posts within 5 minutes
```

---

## Verification Status

✅ All 5 required folders exist
✅ Correct permissions set
✅ 119 files in active workflow
✅ Session persistence active
✅ Logging operational

**System Status:** READY FOR PRODUCTION

---

**Last Verified:** 2026-03-29
**Architecture Version:** 1.0
**Status:** COMPLETE
