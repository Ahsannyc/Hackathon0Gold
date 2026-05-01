---
title: Prompt 6 - Gold Tier Error Recovery - Complete Implementation Summary
date: 2026-03-29
status: Phase 2 Complete, Phase 3 Ready
version: 1.0
---

# Prompt 6: Gold Tier Error Recovery - Implementation Summary

**Current Status: Phase 2 COMPLETE ✅ | Phase 3 READY FOR IMPLEMENTATION**

---

## STEP 1: Watchers Error Recovery - COMPLETE ✅

### Updated Watcher Files (All 4)

| File | Path | Changes | Status |
|---|---|---|---|
| **gmail_watcher.py** | `watchers/gmail_watcher.py` | ✅ Import error_recovery ✅ Init in `__init__` ✅ Error logging in cycle handler ✅ Exponential backoff | DONE |
| **whatsapp_persistent.py** | `watchers/whatsapp_persistent.py` | ✅ Import error_recovery ✅ Init in `__init__` ✅ Error logging + backoff in cycle handler ✅ Retry logic | DONE |
| **linkedin_persistent.py** | `watchers/linkedin_persistent.py` | ✅ Import error_recovery ✅ Init in `__init__` ✅ Error logging + backoff in cycle handler ✅ Retry logic | DONE |
| **instagram_watcher_fixed.py** | `watchers/instagram_watcher_fixed.py` | ✅ Import error_recovery ✅ Init in `__init__` ✅ Error logging + backoff in exception handler | DONE |

**Plus Previously Updated (2):**
- `watchers/facebook_watcher_js_extract.py` ✅
- `watchers/twitter_watcher.py` ✅

**All 6 Platform Watchers Now Have Error Recovery! ✅**

---

## STEP 2: Skills Error Recovery - IMPLEMENTATION GUIDE PROVIDED

### Implementation Status

**Utility Modules (Ready to Use):**
```
✅ watchers/error_recovery.py (159 lines) - Exponential backoff + error logging
✅ skills/error_handler.py (223 lines) - Skill error logging + manual fallback
```

**Skills Ready for Implementation (10 Total):**

All 10 skills need error_handler integration following this template:

```python
from skills.error_handler import SkillErrorHandler

class MySkill:
    def __init__(self):
        self.error_handler = SkillErrorHandler("skill_name", ".")

    def execute(self):
        try:
            # Main logic
        except Exception as e:
            self.error_handler.write_error(e, context="operation")
            if "api" in str(e).lower():
                self.error_handler.write_manual_fallback("Manual action needed", ...)
```

**See PROMPT_6_SKILLS_ERROR_RECOVERY_GUIDE.md for detailed per-skill instructions.**

---

## STEP 3: Updated File Paths

### Phase 2: Watcher Files Updated

```
watchers/
├── error_recovery.py ........................ ✅ Error recovery utility (159 lines)
├── gmail_watcher.py ......................... ✅ UPDATED - Error logging added
├── whatsapp_persistent.py .................. ✅ UPDATED - Error logging + backoff
├── linkedin_persistent.py .................. ✅ UPDATED - Error logging + backoff
├── instagram_watcher_fixed.py .............. ✅ UPDATED - Error logging + backoff
├── facebook_watcher_js_extract.py ......... ✅ UPDATED - Error logging
├── twitter_watcher.py ...................... ✅ UPDATED - Error logging
└── logs/
    ├── error_gmail_watcher_YYYY-MM-DD.log
    ├── error_whatsapp_persistent_YYYY-MM-DD.log
    ├── error_linkedin_persistent_YYYY-MM-DD.log
    ├── error_instagram_watcher_fixed_YYYY-MM-DD.log
    └── ... (created at runtime)
```

### Phase 3: Skills Files (Ready for Update)

```
skills/
├── error_handler.py ......................... ✅ Error handler utility (223 lines)
├── auto_linkedin_poster.py ................. ⚠️ NEEDS UPDATE (good try-except)
├── hitl_approval_handler.py ............... ⚠️ NEEDS UPDATE (good try-except)
├── basic_file_handler.py .................. ⚠️ NEEDS UPDATE (no error handling)
├── task_analyzer.py ........................ ⚠️ NEEDS UPDATE (bare except)
├── gmail_label_organizer.py ............... ⚠️ NEEDS UPDATE (print only)
├── cross_domain_scheduler.py .............. ⚠️ NEEDS UPDATE (minimal handling)
├── cross_domain_integrator.py ............. ⚠️ NEEDS UPDATE (bare except)
├── social_summary_generator.py ........... ⚠️ NEEDS UPDATE (needs fallback)
├── twitter_post_generator.py ............. ⚠️ NEEDS UPDATE (needs fallback)
├── weekly_audit_briefer.py ............... ⚠️ NEEDS UPDATE (partial handling)
└── logs/
    └── skill_error_YYYY-MM-DD.md .......... (created at runtime)
```

### Output Directories (Auto-Created)

```
Logs/
├── audit_YYYY-MM-DD.json .................. (Audit logging)
├── error_gmail_watcher_YYYY-MM-DD.log ... (Watcher errors)
├── error_whatsapp_persistent_YYYY-MM-DD.log
├── error_linkedin_persistent_YYYY-MM-DD.log
└── error_instagram_watcher_fixed_YYYY-MM-DD.log

Errors/
└── skill_error_YYYY-MM-DD.md ............. (Skill errors - auto-created)

Plans/
└── manual_SKILL_NAME_YYYYMMDD_HHMMSS.md . (Manual fallback actions)
```

---

## STEP 4: Comprehensive Test Guide

### Test 1: Verify Watcher Error Logging

**Gmail Watcher Error Test:**
```bash
# 1. Start watcher in foreground
python watchers/gmail_watcher.py

# 2. In another terminal, trigger error by killing OAuth token
rm watchers/.gmail_token.json

# 3. Watch for backoff messages in watcher output:
#    "[BACKOFF] Waiting 2.0s before retry..."
#    "[BACKOFF] Waiting 3.0s before retry..."
#    etc.

# 4. Verify error log created:
cat Logs/error_gmail_watcher_2026-03-29.log

# Expected output:
# [2026-03-29 HH:MM:SS.mmm] [gmail_watcher] [RETRY=1/3] [CONTEXT=cycle_X]
# Error Type: FileNotFoundError
# Error Message: ...
# Traceback: ...
```

**WhatsApp Watcher Error Test:**
```bash
# 1. Start watcher
pm2 start watchers/whatsapp_persistent.py --name test-whatsapp --interpreter python3

# 2. Trigger error by closing browser
pkill -f "Chromium\|chromium"

# 3. Watch PM2 logs
pm2 logs test-whatsapp --lines 30

# Expected:
# [BACKOFF] Retry 1/3 in 1.0s...
# [BACKOFF] Retry 2/3 in 2.0s...
# [BACKOFF] Retry 3/3 in 4.0s...
# [RESTART] Max retries reached, restarting browser...

# 4. Check error log
cat Logs/error_whatsapp_persistent_2026-03-29.log
```

### Test 2: Verify Skill Error Logging (Template)

Once skills are updated with error_handler:

```bash
# 1. Break a required dependency
mv Company_Handbook.md Company_Handbook.md.bak

# 2. Run skill
python skills/auto_linkedin_poster.py

# 3. Verify error file created
ls Errors/skill_error_*.md
cat Errors/skill_error_2026-03-29.md

# Expected format:
# ---
# date: 2026-03-29
# type: skill_error_log
# ---
#
# # Skill Error Log - 2026-03-29
#
# ## AUTO_LINKEDIN_POSTER - 2026-03-29 HH:MM:SS
# **Severity:** error
# **Error Type:** FileNotFoundError
# **Context:** handbook_loading
# **Error Message:**
# ```
# [Errno 2] No such file or directory: 'Company_Handbook.md'
# ```

# 4. Restore file
mv Company_Handbook.md.bak Company_Handbook.md
```

### Test 3: Verify Manual Fallback Creation

**For skills with MCP/API calls (social_summary_generator, twitter_post_generator):**

```bash
# 1. Simulate MCP failure by disconnecting network
# (or comment out MCP call to force exception)

# 2. Run skill
python skills/social_summary_generator.py

# 3. Check for manual fallback file
ls Plans/manual_social_summary_generator_*.md
cat Plans/manual_social_summary_generator_*.md

# Expected format:
# ---
# date: 2026-03-29
# time: HH:MM:SS
# skill: social_summary_generator
# type: manual_fallback
# priority: high
# ---
#
# # Manual Fallback Action Required
#
# **Skill:** social_summary_generator
# **Priority:** high
# **Time:** 2026-03-29 HH:MM:SS
#
# ## What Needs to be Done
#
# Review social media message and draft response manually
#
# ## Context Details
#
# **Source File:** facebook_20260329_abc123.md
# **Error:** MCP connection failed
#
# ## Action Checklist
#
# - [ ] Review the details above
# - [ ] Complete the required action manually
# - [ ] Move completed item to /Done/ folder
# - [ ] Delete this file once action is complete
```

### Test 4: Directory Auto-Creation

```bash
# 1. Remove /Errors directory if it exists
rm -rf Errors/

# 2. Run any skill
python skills/weekly_audit_briefer.py

# 3. Verify /Errors/ was auto-created
ls -la Errors/
# Should show: drwxr-xr-x ... Errors/

# 4. If error occurred, should see:
ls Errors/skill_error_*.md
```

### Test 5: Exponential Backoff Verification

**For watchers - check backoff delay sequence:**

```bash
# 1. Simulate continuous failures
python watchers/gmail_watcher.py

# 2. Kill the Gmail service or network to trigger errors
# Watch the watcher output for backoff sequence:

# Expected delays (exponential):
# Retry 1: ~1 second (BACKOFF_BASE * 2^0 = 1 * 1 = 1s)
# Retry 2: ~2 seconds (BACKOFF_BASE * 2^1 = 1 * 2 = 2s)
# Retry 3: ~4 seconds (BACKOFF_BASE * 2^2 = 1 * 4 = 4s)
# Retry 4: ~8 seconds (BACKOFF_BASE * 2^3 = 1 * 8 = 8s)
# ... capped at 60 seconds max

# Verify in logs:
grep "\[BACKOFF\]" watchers/logs/gmail_watcher.log
```

### Test 6: Full Recovery Cycle

**End-to-end test:**

```bash
# 1. Start all watchers with PM2
pm2 start ecosystem.config.js

# 2. Verify all running
pm2 list
# Should show: gmail-watcher, whatsapp-watcher, linkedin-watcher, instagram-watcher, facebook-watcher, twitter-watcher

# 3. Simulate errors on one watcher
pkill -f "facebook_watcher"

# 4. Monitor recovery
pm2 logs facebook-watcher --lines 50

# Expected sequence:
# [ERROR] Cycle X failed: ...
# [BACKOFF] Retry 1/3 in 1.0s...
# [CYCLE X+1] Checking for new messages...
# (if successful, error counter resets)

# 5. Check error logs
ls Logs/error_facebook_watcher_js_extract_*.log
wc -l Logs/error_facebook_watcher_js_extract_*.log

# 6. Verify PM2 auto-restart worked
pm2 list | grep facebook
# Should show status: online (auto-restarted)
```

---

## File Summary - What's Been Done

### Implemented ✅
```
Phase 1: Utility Modules
  ✅ watchers/error_recovery.py (159 lines)
  ✅ skills/error_handler.py (223 lines)

Phase 2: Watcher Updates (All 6)
  ✅ watchers/gmail_watcher.py - Error logging + backoff
  ✅ watchers/whatsapp_persistent.py - Error logging + backoff
  ✅ watchers/linkedin_persistent.py - Error logging + backoff
  ✅ watchers/instagram_watcher_fixed.py - Error logging + backoff
  ✅ watchers/facebook_watcher_js_extract.py - Error logging (prev)
  ✅ watchers/twitter_watcher.py - Error logging (prev)
```

### Ready for Implementation (Phase 3)
```
See PROMPT_6_SKILLS_ERROR_RECOVERY_GUIDE.md for:
  □ skills/basic_file_handler.py
  □ skills/task_analyzer.py
  □ skills/auto_linkedin_poster.py
  □ skills/hitl_approval_handler.py
  □ skills/gmail_label_organizer.py
  □ skills/cross_domain_scheduler.py
  □ skills/cross_domain_integrator.py
  □ skills/social_summary_generator.py
  □ skills/twitter_post_generator.py
  □ skills/weekly_audit_briefer.py
```

---

## Next Steps

1. **Quick Win (5 min):** Verify watcher error logs with Test 1 & 2
2. **Phase 3 (30-45 min):** Update all 10 skills using the guide (3-5 min per skill)
3. **Full Testing (10 min):** Run Test Suite 3-6 to verify all systems working
4. **Production:** Monitor `/Logs/` and `/Errors/` directories for issues

---

## Recovery Strategy Summary

```
WATCHERS:
  First failure → Log error + exponential backoff (1s, 2s, 4s, 8s... max 60s)
  After 3 retries → Reset and try fresh state
  After 3 restarts → Pause 60s, let PM2 handle

SKILLS:
  Error occurs → Log to /Errors/skill_error_YYYY-MM-DD.md
  If API/MCP fails → Generate manual action in /Plans/manual_*
  Human operator → Reviews /Plans/, completes action, moves to /Done/
```

All error information preserved in logs for debugging and monitoring.

