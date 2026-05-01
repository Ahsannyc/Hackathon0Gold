---
title: Trigger Posts - Quick Start Guide
date: 2026-03-29
status: READY TO USE
---

# Trigger Posts - Quick Start Guide

## 🚀 Get Started in 2 Minutes

### Step 1: Basic Usage

```bash
python scripts/trigger_posts.py --platform linkedin --content "Excited to share!"
```

**Output:**
```
2026-03-29 10:15:34 - INFO - ✅ Post created: POST_20260329_101534_lin_abc123.md
2026-03-29 10:15:34 - INFO - Platform: LinkedIn
2026-03-29 10:15:34 - INFO - Content length: 24 chars
2026-03-29 10:15:34 - INFO - Path: /path/to/Pending_Approval/POST_*.md

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

Excited to share!

---

## Status
- **Platform:** LinkedIn
- **Status:** Pending Approval
- **Created:** 2026-03-29 10:15:34

**Next Step:** Move to /Approved to trigger publishing via Master Orchestrator
======================================================================
✅ Saved to: /path/to/Pending_Approval/POST_*.md
======================================================================
```

### Step 2: Verify File Created

```bash
ls Pending_Approval/POST_*.md
# Output: Pending_Approval/POST_20260329_101534_lin_abc123.md
```

### Step 3: View Created File

```bash
cat Pending_Approval/POST_20260329_101534_lin_abc123.md
```

### Step 4: Move to Approved for Publishing

```bash
# Option A: Use --move flag (automatic)
python scripts/trigger_posts.py --platform linkedin --content "My post" --move

# Option B: Manual move
mv Pending_Approval/POST_*.md Approved/
```

**Result:** Master Orchestrator detects and publishes automatically! ✨

---

## 📋 Command Reference

### Minimal Command (Uses Default Content)

```bash
python scripts/trigger_posts.py --platform linkedin
```

### With Custom Content

```bash
python scripts/trigger_posts.py --platform facebook --content "Great news!"
```

### Short Flags

```bash
python scripts/trigger_posts.py -p twitter -c "New update!"
```

### With Custom Title

```bash
python scripts/trigger_posts.py -p linkedin -c "Post text" --title "My Custom Title"
```

### Create and Move to Approved (Auto-Publish)

```bash
python scripts/trigger_posts.py -p facebook -c "Launch announcement" --move
```

---

## 🎯 Supported Platforms

```
✅ linkedin    - Professional posts
✅ facebook    - Community posts
✅ twitter     - Tweets
✅ instagram   - Visual posts
✅ whatsapp    - Messages
✅ gmail       - Emails
```

**Example:**
```bash
python scripts/trigger_posts.py --platform instagram --content "Beautiful moment"
```

---

## 📝 YAML Frontmatter Generated

Every post includes standard metadata:

```yaml
platform: linkedin              # Platform name
title: "LinkedIn Professional Post"
from: trigger_posts            # Creator
type: linkedin_post            # Post type
priority: medium               # Priority level
status: pending_approval       # Status
created_at: 2026-03-29T...    # Timestamp
requires_approval: true        # Requires review
```

---

## 🔄 Workflow

### With Orchestrator Integration

```
trigger_posts.py
    ↓ (Creates POST_*.md)
Pending_Approval/
    ↓ (Manual review)
Approved/
    ↓ (Master Orchestrator detects)
Social Media Executor v2.0
    ↓ (Publishes)
Done/
```

### Direct Auto-Publish

```bash
# Create and move in one command
python scripts/trigger_posts.py -p linkedin -c "Post text" --move

# File goes directly to Approved/
# Master Orchestrator publishes within 5-30 seconds
ls Done/processed_POST_*.md
```

---

## 💡 Usage Examples

### Example 1: Quick LinkedIn Post

```bash
python scripts/trigger_posts.py -p linkedin -c "Proud to announce our new feature!"
```

### Example 2: Facebook with Auto-Move

```bash
python scripts/trigger_posts.py -p facebook -c "Join us for a live event!" --move
```

### Example 3: Twitter with Custom Title

```bash
python scripts/trigger_posts.py -p twitter -c "Breaking news!" -t "Latest Update"
```

### Example 4: Instagram Default Content

```bash
python scripts/trigger_posts.py --platform instagram
# Uses default Instagram content
```

### Example 5: Batch Creation

```bash
# Create multiple posts
python scripts/trigger_posts.py -p linkedin -c "Post 1"
python scripts/trigger_posts.py -p facebook -c "Post 2"
python scripts/trigger_posts.py -p twitter -c "Post 3"

# All saved to Pending_Approval/
ls Pending_Approval/
# Output: 3 POST_*.md files
```

---

## 📂 File Locations

```
scripts/trigger_posts.py          (Script location)

Pending_Approval/                 (Draft posts - manual review)
├── POST_20260329_101534_lin_abc123.md
├── POST_20260329_102015_fac_def456.md
└── [other drafts]

Approved/                         (Ready for publishing)
├── POST_20260329_101534_lin_abc123.md
├── POST_20260329_102015_fac_def456.md
└── [other posts to publish]

Done/                             (Published posts)
├── processed_POST_*.md

Logs/
├── trigger_posts_2026-03-29.log  (Activity log)
```

---

## 🔧 Available Options

```
--platform, -p          (Required) Platform: linkedin, facebook, twitter, instagram, whatsapp, gmail
--content, -c           (Optional) Post content (uses default if not provided)
--title, -t             (Optional) Post title (auto-generated if not provided)
--move, -m              (Optional) Move to Approved after creation (auto-publish)
--preview               (Optional) Show post preview (default: True)
```

---

## ✅ Verification Checklist

After running the command:

- [ ] File created in `/Pending_Approval/`
- [ ] Filename starts with `POST_` and has timestamp
- [ ] File has YAML frontmatter
- [ ] Platform set correctly
- [ ] Content shows in post
- [ ] Status shows `pending_approval`
- [ ] Log file updated in `/Logs/`

---

## 🚀 Next Steps

1. ✅ Create post: `python scripts/trigger_posts.py -p linkedin -c "Your content"`
2. ✅ View file: `cat Pending_Approval/POST_*.md`
3. ✅ Move to Approved: `mv Pending_Approval/POST_*.md Approved/`
4. ✅ Master Orchestrator publishes automatically (within 5-30s)
5. ✅ Verify in Done/: `ls Done/processed_POST_*.md`

---

**Ready to create posts!** 🎉

```bash
python scripts/trigger_posts.py --platform linkedin --content "Your post text here"
```
