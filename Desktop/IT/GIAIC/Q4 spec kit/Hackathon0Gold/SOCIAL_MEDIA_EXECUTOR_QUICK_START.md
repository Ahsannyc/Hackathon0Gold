---
title: Social Media Executor v2.0 - Quick Start
date: 2026-03-29
status: READY TO RUN
---

# Quick Start: Social Media Executor v2.0

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install playwright pyyaml
playwright install chromium
```

### Step 2: Create Test File in /Approved

Create a dummy post file to test with:

```bash
cat > Approved/facebook_test_post_20260329.md << 'EOF'
---
platform: facebook
title: "Test Post - Facebook"
from: test@example.com
priority: medium
status: approved
---

# Test Post from Social Media Executor

This is a test post created by Social Media Executor v2.0!

Testing:
✅ Playwright persistent sessions
✅ Facebook multi-step posting
✅ Keyboard input for reliability
✅ File movement workflow
✅ Error handling & retry logic

#Test #Automation #SocialMedia
EOF
```

### Step 3: Run the Executor

```bash
python scripts/social_media_executor_v2.py Approved/facebook_test_post_20260329.md
```

### Step 4: Watch It Work

The script will:

1. ✅ Open Facebook in browser
2. ✅ Use persistent session (no login needed if already logged in)
3. ✅ Click "What's on your mind"
4. ✅ Type your post content
5. ✅ Click Post/Share
6. ✅ Move file to Done/
7. ✅ Log success to Logs/

### Step 5: Verify Success

```bash
# Check if file moved to Done/
ls -la Done/processed_facebook_test_post_20260329.md

# Check logs
tail -20 Logs/social_executor_2026-03-29.log
```

---

## 📋 Quick Test Scenarios

### Test A: Single Platform (Facebook)

```bash
cat > Approved/test_facebook.md << 'EOF'
---
platform: facebook
title: "Test Post"
from: test@example.com
priority: medium
---

Testing Social Media Executor on Facebook! 🎉
EOF

python scripts/social_media_executor_v2.py Approved/test_facebook.md
```

### Test B: Twitter

```bash
cat > Approved/test_twitter.md << 'EOF'
---
platform: twitter
title: "Test Tweet"
from: test@example.com
priority: medium
---

Just testing Social Media Executor v2.0! 🚀 #Automation
EOF

python scripts/social_media_executor_v2.py Approved/test_twitter.md
```

### Test C: LinkedIn

```bash
cat > Approved/test_linkedin.md << 'EOF'
---
platform: linkedin
title: "Test Post"
from: test@example.com
priority: medium
---

Testing Social Media Executor on LinkedIn.

Key features:
- Multi-platform posting
- Persistent sessions
- Retry logic
- Error handling
EOF

python scripts/social_media_executor_v2.py Approved/test_linkedin.md
```

### Test D: Process All Files

```bash
# Create multiple test files in /Approved
cat > Approved/multi_test_1.md << 'EOF'
---
platform: facebook
title: "Post 1"
---
This is test post 1
EOF

cat > Approved/multi_test_2.md << 'EOF'
---
platform: twitter
title: "Tweet 1"
---
This is test tweet 1
EOF

# Process all at once
python scripts/social_media_executor_v2.py --all-pending
```

---

## 🔍 Expected Output

### Success Output

```
======================================================================
Processing: facebook_test_post_20260329.md
======================================================================
Platform: facebook
Title: Test Post - Facebook
Content length: 156 chars

🔄 Attempt 1/3 - facebook
✅ Facebook post successful
✅ Moved to Done: processed_facebook_test_post_20260329.md
✅ Successfully posted and moved to Done
```

### Error Output (With Retry)

```
🔄 Attempt 1/3 - facebook
❌ Facebook posting failed: button not found
📸 Error screenshot saved: Logs/error_facebook_2026-03-29_10-15-45_attempt1.png
⏳ Waiting 2s before retry...

🔄 Attempt 2/3 - facebook
✅ Facebook post successful
✅ Moved to Done: processed_facebook_test_post_20260329.md
✅ Successfully posted and moved to Done
```

---

## 📁 File Locations

```
scripts/
└── social_media_executor_v2.py     ← Main script

session/
├── facebook/                        ← Persistent login
├── twitter/
├── linkedin/
├── instagram/
├── whatsapp/
└── gmail/

Approved/
├── facebook_test_post_20260329.md  ← Create test files here
├── twitter_test_*.md
└── linkedin_test_*.md

Done/
└── processed_*.md                   ← Files move here after success

Logs/
├── social_executor_2026-03-29.log  ← Execution log
└── error_facebook_*.png             ← Error screenshots
```

---

## 🎯 Common Commands

### Test Single File
```bash
python scripts/social_media_executor_v2.py Approved/my_post.md
```

### Test All Pending
```bash
python scripts/social_media_executor_v2.py --all-pending
```

### View Logs
```bash
tail -50 Logs/social_executor_2026-03-29.log
```

### Check Moved Files
```bash
ls -la Done/processed_*.md
```

### View Error Screenshots
```bash
ls -la Logs/error_*.png
```

---

## ✅ Verification Checklist

After running the test:

- [ ] Browser window opened
- [ ] Content was posted to platform
- [ ] File appeared in Done/ folder
- [ ] Log file created in Logs/
- [ ] No error screenshots in Logs/ (if success)
- [ ] Success message in log: "✅ Successfully posted and moved to Done"

---

## 🔧 Troubleshooting

### Issue: Browser doesn't open

```bash
# Install Playwright browser files
playwright install chromium

# Check Python can import playwright
python -c "from playwright.async_api import async_playwright; print('OK')"
```

### Issue: "Session not found"

```bash
# First run will create session folder
# If stuck, delete session folder and start fresh
rm -rf session/
python scripts/social_media_executor_v2.py Approved/test_post.md
# Will open browser for manual login
```

### Issue: Post didn't work but no error

```bash
# Check error screenshots
ls -la Logs/error_*.png

# Check detailed log
cat Logs/social_executor_2026-03-29.log | grep -A5 "Attempt"

# Check if file is still in Approved/ (not moved)
ls Approved/test_*.md
```

### Issue: "File not found"

```bash
# Verify file path is correct
ls -la Approved/facebook_test_post_20260329.md

# Use absolute path if relative doesn't work
python scripts/social_media_executor_v2.py /path/to/Approved/test_post.md
```

---

## 🎬 Next Steps

1. ✅ Run Quick Start test above
2. ✅ Verify file moves to Done/
3. ✅ Check logs for success message
4. ✅ Test with each platform (Facebook, Twitter, LinkedIn)
5. ✅ Test retry logic (disable buttons temporarily)
6. ✅ Integrate with Ralph Loop for automation

---

## 💡 Tips

- **First time setup:** Executor will open browser for you to log in once per platform
- **Sessions persist:** After first login, you don't need to log in again
- **Keyboard input:** Uses `keyboard.type()` not paste for better reliability
- **Retry smart:** Automatically retries 3 times with exponential backoff (2s, 4s)
- **Error proof:** Takes screenshots on every failure for debugging

---

**You're ready! Run the test now:** 🚀

```bash
python scripts/social_media_executor_v2.py Approved/facebook_test_post_20260329.md
```
