# ⚡ Facebook Watcher - Quick Fix (5 minutes)

## The Fix
✅ Browser crashes fixed
✅ Both Facebook & Instagram watchers now running
✅ Ready to capture messages

## What You Need To Do

### 1️⃣ Login (2 minutes)
```bash
python setup_facebook_login.py
```
A browser will open. Log in to Facebook and press Ctrl+C.

### 2️⃣ Restart (1 minute)
```bash
pm2 restart facebook-watcher
pm2 list
```
Verify status: facebook-watcher should show ✅ ONLINE

### 3️⃣ Test (2 minutes)
Send yourself a Facebook message with word "sales" or "invoice"
```bash
sleep 65
ls Needs_Action/ | grep facebook
```

## Done! 🎉

Your watchers are now capturing:
- ✅ Gmail
- ✅ WhatsApp  
- ✅ LinkedIn
- ✅ Facebook (after login)
- ✅ Instagram (after login)

Questions? See: `FACEBOOK_INSTAGRAM_LOGIN_SETUP.md`
