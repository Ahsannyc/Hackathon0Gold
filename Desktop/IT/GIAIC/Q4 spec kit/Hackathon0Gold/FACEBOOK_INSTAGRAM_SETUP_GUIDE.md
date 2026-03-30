# Facebook/Instagram Watcher + Social Summary Generator Setup Guide

## Overview

This guide walks through setting up the Facebook/Instagram watcher (Gold Tier) and the social summary generator skill. These components monitor Facebook Messenger and Instagram DMs 24/7 for business keywords, capture messages, and generate draft responses.

## Files Created

1. **`watchers/facebook_instagram_watcher.py`** - Persistent browser watcher
2. **`skills/social_summary_generator.py`** - Response draft generator

## Prerequisites

- Python 3.11+
- Playwright (already installed in project)
- PM2 process manager
- Facebook account with Messenger access
- Instagram account with DM access
- Meta account (same login for both platforms)

## Installation & Setup

### Step 1: Install Dependencies (if needed)

```bash
pip install playwright pyyaml
```

### Step 2: Verify File Locations

Ensure both files exist:

```bash
ls -la watchers/facebook_instagram_watcher.py
ls -la skills/social_summary_generator.py
```

### Step 3: Create Required Directories

The watcher will create these automatically on first run:

```
session/facebook/                  # Persistent browser session
Needs_Action/                       # Captured messages
Plans/                             # Draft responses
Pending_Approval/                  # Awaiting HITL approval
Approved/                          # Approved responses
Done/                              # Completed messages
```

## Running the Watcher

### Option A: Manual Start (Testing)

```bash
# Start watcher in foreground
python3 watchers/facebook_instagram_watcher.py
```

**First Run:** Browser will open. Manually log in within 60 seconds.
- Navigate to Facebook if needed
- Complete any 2FA/verification
- Watcher will detect authentication and start monitoring

### Option B: PM2 Start (Production)

```bash
# Start watcher with PM2
pm2 start watchers/facebook_instagram_watcher.py \
  --name facebook-instagram-watcher \
  --interpreter python3

# Save PM2 config
pm2 save

# View logs
pm2 logs facebook-instagram-watcher
```

### Option C: PM2 with Auto-Restart

```bash
pm2 start watchers/facebook_instagram_watcher.py \
  --name facebook-instagram-watcher \
  --interpreter python3 \
  --max-memory-restart 500M \
  --max-restarts 10

pm2 save
```

## Testing the Watcher

### Test Scenario 1: Facebook Messenger

1. **Start watcher:**
   ```bash
   python3 watchers/facebook_instagram_watcher.py
   ```

2. **Manual login** (first run only):
   - Browser opens to Facebook Messenger
   - Complete login/2FA within 60 seconds
   - Watcher will detect and continue

3. **Send test message to yourself:**
   - Open Facebook Messenger in another tab
   - Send yourself: "Hi, I have a **sales** project for you"
   - Include at least one keyword: `sales`, `client`, or `project`

4. **Monitor watcher output:**
   - Watch console for: `[OK] Captured Facebook message from...`
   - Check logs: `tail -f watchers/logs/facebook_instagram_watcher.log`

5. **Verify capture:**
   ```bash
   ls -la Needs_Action/facebook_*.md
   cat Needs_Action/facebook_*.md
   ```

### Test Scenario 2: Instagram DMs

1. **Watcher is running**

2. **Send test DM on Instagram:**
   - Open Instagram in another tab
   - Send yourself a DM: "Hey, interested in a **client** opportunity"
   - Include at least one keyword: `sales`, `client`, or `project`

3. **Monitor output:**
   - Watch for: `[OK] Captured Instagram message from...`

4. **Verify capture:**
   ```bash
   ls -la Needs_Action/instagram_*.md
   cat Needs_Action/instagram_*.md
   ```

### Test Scenario 3: Social Summary Generator

1. **Ensure messages captured:**
   ```bash
   ls Needs_Action/facebook_*.md Needs_Action/instagram_*.md
   ```

2. **Run skill (dry-run first):**
   ```bash
   python3 skills/social_summary_generator.py --dry-run
   ```

3. **Check dry-run output:**
   - Should show: `Found X social media messages with keywords`
   - Should show paths where drafts _would_ be saved
   - No files created yet

4. **Run with real processing:**
   ```bash
   python3 skills/social_summary_generator.py --process
   ```

5. **Verify drafts created:**
   ```bash
   ls -la Plans/facebook_draft_*.md
   ls -la Plans/instagram_draft_*.md
   cat Plans/facebook_draft_*.md
   ```

6. **Verify moved to approval:**
   ```bash
   ls -la Pending_Approval/facebook_draft_*.md
   ls -la Pending_Approval/instagram_draft_*.md
   ```

## Workflow: From Capture to Approval

### Message Flow Diagram

```
Facebook Messenger / Instagram DM
           ↓
    Watcher detects keyword
           ↓
Needs_Action/facebook_*.md (or instagram_*.md)
           ↓
   Run Social Summary Generator
           ↓
    Plans/facebook_draft_*.md
           ↓
Pending_Approval/facebook_draft_*.md  ← HITL checks here
           ↓
[HUMAN REVIEWS AND EDITS]
           ↓
Approved/facebook_draft_*.md
           ↓
[Send via HITL Handler or manual action]
           ↓
Done/facebook_*.md
```

### Manual Approval Process

1. **Check Pending_Approval:**
   ```bash
   ls Pending_Approval/
   cat Pending_Approval/facebook_draft_*.md
   ```

2. **Review the draft response:**
   - Read original message (in "Original Message Context")
   - Read drafted response (in "Drafted Response")
   - Edit if needed

3. **Approve:**
   ```bash
   # Move to /Approved to mark approved
   mv Pending_Approval/facebook_draft_*.md Approved/
   ```

4. **Reject (optional):**
   ```bash
   # Move to /Rejected to discard
   mkdir -p Rejected
   mv Pending_Approval/facebook_draft_*.md Rejected/
   ```

## Configuration

### Keywords

Edit the `KEYWORDS` list in either file to change detection:

**In `watchers/facebook_instagram_watcher.py` (line 48):**
```python
KEYWORDS = ['sales', 'client', 'project']  # Add more keywords here
```

**In `skills/social_summary_generator.py` (line 43):**
```python
KEYWORDS = ['sales', 'client', 'project']  # Must match watcher
```

### Check Interval

Adjust how often watcher polls for messages (seconds):

**`watchers/facebook_instagram_watcher.py` (line 49):**
```python
CHECK_INTERVAL = 60  # Change to 30 for faster polling, 120 for slower
```

### Session Refresh

Adjust how often watcher validates authentication (seconds):

**`watchers/facebook_instagram_watcher.py` (line 50):**
```python
SESSION_REFRESH_INTERVAL = 5400  # 90 minutes (in seconds)
```

## Logging & Monitoring

### Watcher Logs

```bash
# Real-time logs
pm2 logs facebook-instagram-watcher

# Or directly:
tail -f watchers/logs/facebook_instagram_watcher.log
```

### Skill Logs

```bash
tail -f skills/logs/social_summary_generator.log
```

### PM2 Status

```bash
pm2 status
pm2 show facebook-instagram-watcher
```

## Troubleshooting

### Issue: "Feed area not visible" after login

**Cause:** Page didn't fully load or authentication check failed

**Solution:**
1. Wait 15 seconds for page to fully load
2. Check if 2FA is required manually
3. Restart watcher: `pm2 restart facebook-instagram-watcher`

### Issue: No messages captured

**Cause:** Keywords don't match or message format unexpected

**Solution:**
1. Check message content has exact keyword: `sales`, `client`, or `project`
2. Try: "I have a **sales** opportunity"
3. Verify keywords in both files match
4. Check logs: `pm2 logs facebook-instagram-watcher`

### Issue: Watcher crashes after 60+ minutes

**Cause:** Session timeout or memory leak

**Solution:**
1. PM2 will auto-restart (check `pm2 logs`)
2. Watcher refreshes every 90 minutes with `refresh_session()`
3. If persistent, increase PM2 restart attempts:
   ```bash
   pm2 start watchers/facebook_instagram_watcher.py \
     --name facebook-instagram-watcher \
     --interpreter python3 \
     --max-memory-restart 500M
   pm2 save
   ```

### Issue: "Authentication failed" in logs

**Cause:** Session cookies expired or 2FA triggered

**Solution:**
1. Stop watcher: `pm2 stop facebook-instagram-watcher`
2. Delete session: `rm -rf session/facebook/*`
3. Restart: `pm2 start facebook-instagram-watcher`
4. Complete login manually again

### Issue: Draft not created despite capturing message

**Cause:** Keywords in draft check differ from watcher

**Solution:**
1. Verify `KEYWORDS` list in both files match
2. Check message was actually captured: `ls Needs_Action/facebook_*.md`
3. Check logs: `tail -f skills/logs/social_summary_generator.log`
4. Run with verbose: `python3 skills/social_summary_generator.py --process`

## Verification Checklist

- [ ] `watchers/facebook_instagram_watcher.py` exists and is executable
- [ ] `skills/social_summary_generator.py` exists and is executable
- [ ] Session directory created: `ls session/facebook/Default/Network/`
- [ ] Auth marker written: `ls session/facebook_authenticated.txt`
- [ ] Test message captured: `ls Needs_Action/facebook_*.md`
- [ ] Draft created: `ls Plans/facebook_draft_*.md`
- [ ] Draft moved to approval: `ls Pending_Approval/facebook_draft_*.md`
- [ ] Handbook loaded: Logs show `✓ Loaded Company_Handbook.md`
- [ ] YAML frontmatter valid: `head -20 Needs_Action/facebook_*.md`
- [ ] Response includes keywords: `grep -i "sales\|client\|project" Plans/facebook_*.md`

## PM2 Management

### Start

```bash
pm2 start watchers/facebook_instagram_watcher.py --name facebook-instagram-watcher --interpreter python3
pm2 save
```

### Stop

```bash
pm2 stop facebook-instagram-watcher
```

### Restart

```bash
pm2 restart facebook-instagram-watcher
```

### Remove

```bash
pm2 delete facebook-instagram-watcher
pm2 save
```

### Monitor

```bash
pm2 monit
```

## Next Steps

1. **Start watcher:** `pm2 start watchers/facebook_instagram_watcher.py --name facebook-instagram-watcher --interpreter python3`
2. **Send test message** with keywords (sales, client, project)
3. **Run skill:** `python3 skills/social_summary_generator.py --process`
4. **Review draft** in `/Pending_Approval`
5. **Move to `/Approved`** once reviewed
6. **Schedule skill** with PM2 cron (hourly):
   ```bash
   pm2 start skills/social_summary_generator.py --name social_summary_generator --interpreter python3 --cron "0 * * * *"
   pm2 save
   ```

## Integration with Existing System

This watcher integrates with:
- **Ralph Loop Runner** (`tools/ralph_loop_runner.py`) - for iterative task completion
- **HITL Handler** (`skills/hitl_approval_handler.py`) - for action execution
- **Daily Briefing** (`schedulers/daily_briefing_generator.py`) - for summary reports
- **LinkedIn Watcher** (`watchers/linkedin_persistent.py`) - parallel monitoring

All share the same directory structure and workflow patterns.

---

**Last Updated:** 2026-03-19
**Version:** 1.0
**Status:** Production Ready
