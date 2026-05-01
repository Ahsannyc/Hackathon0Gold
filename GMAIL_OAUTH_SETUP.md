---
title: Gmail OAuth Setup Guide
tier: Gold Tier
status: Setup Required
date: 2026-03-29
version: 1.0
---

# Gmail OAuth Setup Guide - Gold Tier

The Gmail Watcher requires OAuth 2.0 credentials from Google Cloud Console to access your Gmail account securely.

## ⚠️ Current Status

Gmail watcher is **FAILING** with error:
```
credentials.json not found
[ERROR] Gmail authentication failed: Place credentials.json in project root
```

## Step-by-Step Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a Project"** → **"NEW PROJECT"**
3. Enter name: `Hackathon0Gold`
4. Click **"CREATE"**
5. Wait for project to be created (1-2 minutes)

### 2. Enable Gmail API

1. In Google Cloud Console, go to **APIs & Services** → **Library**
2. Search for **"Gmail API"**
3. Click on **Gmail API** result
4. Click **"ENABLE"**
5. Wait for confirmation (shows "API enabled")

### 3. Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
3. If prompted: Click **"Configure OAuth consent screen"** first
4. On OAuth consent screen:
   - Choose **"External"** (unless you have a Google Workspace)
   - Click **"CREATE"**
5. Fill in consent screen:
   - **App name:** `Hackathon0Gold`
   - **User support email:** Your email address
   - **Developer contact info:** Your email address
   - Click **"SAVE AND CONTINUE"**
6. Skip scopes and test users screens (click "SAVE AND CONTINUE")
7. Go back to **Credentials** → **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
8. For **Application type**, select **"Desktop application"**
9. Click **"CREATE"**
10. Click **"DOWNLOAD JSON"** (saves `client_secret_*.json`)

### 4. Place Credentials in Project

1. Rename downloaded file to `credentials.json`
2. Copy to project root:
   ```
   C:\Users\14loa\Desktop\IT\GIAIC\Q4 spec kit\Hackathon0Gold\credentials.json
   ```

### 5. Test Gmail Watcher

Run the watcher:
```bash
cd "C:\Users\14loa\Desktop\IT\GIAIC\Q4 spec kit\Hackathon0Gold"
python3 watchers/gmail_watcher.py
```

**First run**: A browser will open asking for authorization. Click **"Allow"** to grant permissions.

**Expected output**:
```
✓ [OK] Directories verified
✓ [OK] Connected to Gmail API
✓ [MONITOR] Starting Gmail watcher (120s check interval)
✓ [OK] Gmail watching
```

### 6. Run with PM2 (Continuous Operation)

Once working, run with PM2:
```bash
pm2 start watchers/gmail_watcher.py --name gmail_watcher --interpreter python3
pm2 logs gmail_watcher
```

## Permissions Requested

Gmail Watcher requests:
- **`https://www.googleapis.com/auth/gmail.modify`** - Can read and label emails (NOT delete or send)

This is the minimum safe scope needed to:
- ✅ Read unread emails
- ✅ Extract email metadata
- ✅ Apply labels
- ❌ NOT delete emails
- ❌ NOT send emails

## Troubleshooting

### Error: "credentials.json not found"

**Solution**:
1. Verify file exists at: `C:\Users\14loa\Desktop\IT\GIAIC\Q4 spec kit\Hackathon0Gold\credentials.json`
2. Make sure filename is exactly `credentials.json` (not `client_secret_*.json`)

### Error: "Access denied - insufficient permissions"

**Solution**:
1. Delete `watchers/.gmail_token.json` (revokes cached access)
2. Run `python3 watchers/gmail_watcher.py` again
3. Click **"Allow"** when browser opens

### Gmail only captures some messages

**Expected behavior**:
- Only messages with keywords are captured: `urgent, invoice, payment, sales, client, project, deal, opportunity, partnership, lead, inquiry`
- This is intentional to reduce noise

To add keywords, edit `watchers/gmail_watcher.py` line 77:
```python
KEYWORDS = ['sales', 'client', 'project', 'urgent', 'invoice', 'payment', ...]
```

## OAuth Token Storage

After first run, a token file is created:
```
watchers/.gmail_token.json
```

This file stores your refresh token (allows offline access).
- **Keep this file secure** - it can access your Gmail account
- **NEVER commit this file to git** - it's in `.gitignore`
- If compromised, delete and re-run the watcher to get a new token

## Next Steps

Once Gmail is working:
1. Test with an email containing keywords
2. Check `/Needs_Action/` for captured messages
3. Verify workflow processes them correctly
4. Run with PM2 for continuous monitoring

## Support

If stuck:
1. Check logs: `watchers/logs/gmail_watcher.log`
2. Verify credentials.json exists and is readable
3. Make sure Gmail API is enabled in Google Cloud Console
4. Check Google Cloud Console quota hasn't been exceeded
