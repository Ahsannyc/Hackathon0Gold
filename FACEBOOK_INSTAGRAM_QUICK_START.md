# Facebook/Instagram Watcher - Quick Start

## TL;DR - Just Get Started

### 1. Start the Watcher (One Command)

```bash
pm2 start watchers/facebook_instagram_watcher.py \
  --name facebook-instagram-watcher \
  --interpreter python3

# Verify it's running
pm2 status
```

**First run only:** Browser opens for manual login. Log in within 60 seconds.

### 2. Send Test Message

Open Facebook Messenger or Instagram DMs and send yourself:
```
Hi, I have a **sales** opportunity for you
```

(Must include keyword: `sales`, `client`, or `project`)

### 3. Check if Message Was Captured

```bash
ls Needs_Action/facebook_*.md
# or
ls Needs_Action/instagram_*.md

# View the captured message
cat Needs_Action/facebook_*.md
```

### 4. Generate Response Draft

```bash
python3 skills/social_summary_generator.py --process
```

### 5. Review Draft & Approve

```bash
# View the draft
cat Pending_Approval/facebook_draft_*.md

# Approve it
mv Pending_Approval/facebook_draft_*.md Approved/
```

---

## Essential PM2 Commands

```bash
# Start watcher
pm2 start watchers/facebook_instagram_watcher.py --name facebook-instagram-watcher --interpreter python3

# View logs
pm2 logs facebook-instagram-watcher

# Stop watcher
pm2 stop facebook-instagram-watcher

# Restart watcher
pm2 restart facebook-instagram-watcher

# Check status
pm2 status

# Remove from PM2
pm2 delete facebook-instagram-watcher

# Save config
pm2 save
```

---

## Essential File Locations

```
Needs_Action/           ← Captured messages appear here
Plans/                  ← Draft responses appear here
Pending_Approval/       ← Move here for HITL review
Approved/               ← Move here to authorize sending
Done/                   ← Completed messages

session/facebook/       ← Browser session (created automatically)
session/facebook_authenticated.txt  ← Auth timestamp

watchers/logs/facebook_instagram_watcher.log  ← Watcher logs
skills/logs/social_summary_generator.log      ← Skill logs
```

---

## Keywords Detected

The watcher looks for these words in messages:
- `sales`
- `client`
- `project`

To add more keywords, edit line 48 in `watchers/facebook_instagram_watcher.py`:
```python
KEYWORDS = ['sales', 'client', 'project', 'opportunity', 'partnership']
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No messages captured | Send message with keyword: `sales`, `client`, or `project` |
| Watcher stops | Check logs: `pm2 logs facebook-instagram-watcher` |
| Authentication fails | Delete session: `rm -rf session/facebook/*` then restart |
| Draft not created | Run skill: `python3 skills/social_summary_generator.py --process` |
| Browser doesn't open | Run manually first: `python3 watchers/facebook_instagram_watcher.py` |

---

## Workflow Overview

```
Message arrives on FB/IG
        ↓
Watcher detects keyword
        ↓
Needs_Action/facebook_*.md
        ↓
Run Social Summary Generator
        ↓
Pending_Approval/facebook_draft_*.md
        ↓
[YOU REVIEW & EDIT]
        ↓
Approved/facebook_draft_*.md
        ↓
[SEND VIA HITL HANDLER]
```

---

## 3-Step Setup

```bash
# 1. Start watching
pm2 start watchers/facebook_instagram_watcher.py --name facebook-instagram-watcher --interpreter python3

# 2. Send test message (in Facebook Messenger or Instagram DM):
# "Hi, I have a sales opportunity"

# 3. Check and approve
ls Needs_Action/facebook_*.md
python3 skills/social_summary_generator.py --process
cat Pending_Approval/facebook_draft_*.md
mv Pending_Approval/facebook_draft_*.md Approved/
```

Done! 🎉

---

## Schedule Skill to Run Hourly

```bash
pm2 start skills/social_summary_generator.py \
  --name social_summary_generator \
  --interpreter python3 \
  --cron "0 * * * *"

pm2 save
```

---

**Need more details?** See `FACEBOOK_INSTAGRAM_SETUP_GUIDE.md`
