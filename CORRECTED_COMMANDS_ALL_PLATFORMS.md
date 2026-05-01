---
title: Corrected Terminal Commands - All 6 Platforms
date: 2026-03-30
status: UPDATED
version: 3.0
---

# ✅ CORRECTED Terminal Commands - All 6 Platforms

All 6 test guides have been updated to use the **correct command structure** matching your class fellow's implementation.

---

## 🔴 LINKEDIN

### Step 1: Login Setup (First Time Only)
```bash
python watchers/linkedin_watcher.py
```
- Opens browser automatically
- You log in manually once
- Session saved to `./session/linkedin`

### Step 2: Create Post Draft
```bash
python trigger_linkedin_post.py
```
- Creates post draft in `/Pending_Approval/`
- File name: `POST_LINKEDIN_YYYYMMDD_HHMMSS.md`

### Step 3: Approve & Move
```bash
mv Pending_Approval/POST_LINKEDIN_* Approved/
```

### Step 4: Watch Automation
```bash
python master_orchestrator.py
```
- Detects file in `/Approved/`
- Automatically posts to LinkedIn
- Moves completed file to `/Done/`

---

## 🔵 FACEBOOK

### Step 1: Login Setup (First Time Only)
```bash
python watchers/facebook_watcher.py
```
- Opens browser automatically
- You log in manually once
- Session saved to `./session/facebook`

### Step 2: Create Post Draft
```bash
python trigger_facebook_post.py
```
- Creates post draft in `/Pending_Approval/`
- File name: `POST_FACEBOOK_YYYYMMDD_HHMMSS.md`

### Step 3: Approve & Move
```bash
mv Pending_Approval/POST_FACEBOOK_* Approved/
```

### Step 4: Watch Automation
```bash
python master_orchestrator.py
```

---

## 🐦 TWITTER

### Step 1: Login Setup (First Time Only)
```bash
python watchers/twitter_watcher.py
```
- Opens browser automatically
- You log in manually once
- Session saved to `./session/twitter`

### Step 2: Create Tweet Draft
```bash
python trigger_twitter_post.py
```
- Creates tweet draft in `/Pending_Approval/`
- File name: `POST_TWITTER_YYYYMMDD_HHMMSS.md`

### Step 3: Approve & Move
```bash
mv Pending_Approval/POST_TWITTER_* Approved/
```

### Step 4: Watch Automation
```bash
python master_orchestrator.py
```

---

## 📷 INSTAGRAM

### Step 1: Login Setup (First Time Only)
```bash
python watchers/instagram_watcher.py
```
- Opens browser automatically
- You log in manually once
- Session saved to `./session/instagram`

### Step 2: Create Post Draft
```bash
python trigger_instagram_post.py
```
- Creates post draft in `/Pending_Approval/`
- File name: `POST_INSTAGRAM_YYYYMMDD_HHMMSS.md`

### Step 3: Approve & Move
```bash
mv Pending_Approval/POST_INSTAGRAM_* Approved/
```

### Step 4: Watch Automation
```bash
python master_orchestrator.py
```

---

## 💬 WHATSAPP

### Step 1: Login Setup (First Time Only)
```bash
python watchers/whatsapp_watcher.py
```
- Opens WhatsApp Web in browser
- Scan QR code with phone to authenticate
- Session saved to `./session/whatsapp`

### Step 2: Create Message Draft
```bash
python trigger_whatsapp_post.py
```
- Creates message draft in `/Pending_Approval/`
- File name: `POST_WHATSAPP_YYYYMMDD_HHMMSS.md`

### Step 3: Approve & Move
```bash
mv Pending_Approval/POST_WHATSAPP_* Approved/
```

### Step 4: Watch Automation
```bash
python master_orchestrator.py
```

---

## 📧 GMAIL

### Step 1: Login Setup (First Time Only)
```bash
python watchers/gmail_watcher.py
```
- Opens Gmail in browser
- You log in manually once
- Session saved to `./session/gmail`

### Step 2: Create Email Draft
```bash
python trigger_gmail_post.py
```
- Creates email draft in `/Pending_Approval/`
- File name: `POST_GMAIL_YYYYMMDD_HHMMSS.md`

### Step 3: Approve & Move
```bash
mv Pending_Approval/POST_GMAIL_* Approved/
```

### Step 4: Watch Automation
```bash
python master_orchestrator.py
```

---

## 📊 Command Pattern Summary

### For ALL 6 Platforms:

**Step 1 (Setup):** `python watchers/[platform]_watcher.py`
**Step 2 (Create):** `python trigger_[platform]_post.py`
**Step 3 (Move):** `mv Pending_Approval/POST_[PLATFORM]_* Approved/`
**Step 4 (Automate):** `python master_orchestrator.py`

---

## ✅ What Changed in Test Guides

### BEFORE (Incorrect):
```bash
python scripts/trigger_posts.py -p linkedin -c "content" --preview
python scripts/trigger_posts.py -p facebook -c "content" --preview
```

### AFTER (Corrected):
```bash
# LinkedIn
python watchers/linkedin_watcher.py
python trigger_linkedin_post.py

# Facebook
python watchers/facebook_watcher.py
python trigger_facebook_post.py

# Twitter
python watchers/twitter_watcher.py
python trigger_twitter_post.py

# Instagram
python watchers/instagram_watcher.py
python trigger_instagram_post.py

# WhatsApp
python watchers/whatsapp_watcher.py
python trigger_whatsapp_post.py

# Gmail
python watchers/gmail_watcher.py
python trigger_gmail_post.py
```

---

## 📋 File Structure

```
project/
├── watchers/
│   ├── linkedin_watcher.py      ← Step 1 (Login setup)
│   ├── facebook_watcher.py      ← Step 1 (Login setup)
│   ├── twitter_watcher.py       ← Step 1 (Login setup)
│   ├── instagram_watcher.py     ← Step 1 (Login setup)
│   ├── whatsapp_watcher.py      ← Step 1 (Login setup)
│   └── gmail_watcher.py         ← Step 1 (Login setup)
├── trigger_linkedin_post.py     ← Step 2 (Create draft)
├── trigger_facebook_post.py     ← Step 2 (Create draft)
├── trigger_twitter_post.py      ← Step 2 (Create draft)
├── trigger_instagram_post.py    ← Step 2 (Create draft)
├── trigger_whatsapp_post.py     ← Step 2 (Create draft)
├── trigger_gmail_post.py        ← Step 2 (Create draft)
├── master_orchestrator.py       ← Step 4 (Watch automation)
├── Pending_Approval/            ← Where drafts go
├── Approved/                    ← Where you approve
└── Done/                        ← Where completed posts go
```

---

## 🎯 Updated Test Guides

All 6 test guides now use the corrected commands:

✅ **facebook_test_guide.md** - Updated
✅ **twitter_test_guide.md** - Updated
✅ **instagram_test_guide.md** - Updated
✅ **whatsapp_test_guide.md** - Updated
✅ **gmail_test_guide.md** - Updated
✅ **linkedin_test_guide.md** - Updated

---

**Status:** ✅ COMPLETE - All commands corrected
**Date:** 2026-03-30
**Version:** 3.0 (Command Structure Corrected)
