# System Requirements & Setup
**Hackathon0Gold - Multi-Platform Message Monitoring System**

---

## 💻 System Requirements

### Operating System
- **Primary:** Windows 10/11 (Tested on Windows 11 Home)
- **Alternative:** macOS or Linux (with some path adjustments)

### Hardware
- **Processor:** Intel i5/i7 or equivalent (8+ cores)
- **RAM:** 8 GB minimum, 16 GB recommended
- **Storage:** 2 GB for project + dependencies
- **Network:** Stable internet connection (24/7 operation)

### Disk Space
```
Python packages:        ~1.5 GB
Chromium browsers:      ~500 MB (per browser, shared via undetected-chromedriver)
Project code:           ~50 MB
Session data:           ~100 MB
Logs:                   ~100 MB (grows over time)
Total:                  ~2-3 GB
```

---

## 📦 Software Prerequisites

### Python
```bash
# Required: Python 3.11+ (3.13 recommended)
python --version
# Expected: Python 3.13.x or higher

# Download: https://www.python.org/downloads/
```

### Node.js & NPM
```bash
# Required: Node.js 18+ with npm
node --version     # Expected: v18.0.0 or higher
npm --version      # Expected: 9.0.0 or higher

# Download: https://nodejs.org/
```

### PM2 (Process Manager)
```bash
# Install globally
npm install -g pm2

# Verify installation
pm2 --version
```

### Git (Optional, for version control)
```bash
# Recommended but not required
git --version

# Download: https://git-scm.com/
```

---

## 📚 Python Dependencies

### Core Browser Automation
- **Playwright** - Modern browser automation framework
- **Selenium** - WebDriver protocol (legacy, for Undetected-Chromedriver)
- **Undetected-Chromedriver** - Bypasses anti-bot detection on Facebook

### Google APIs (Gmail)
- **google-auth** - Authentication
- **google-auth-oauthlib** - OAuth2 flow
- **google-auth-httplib2** - HTTP integration
- **google-api-python-client** - Gmail API client

### Utilities
- **requests** - HTTP library for APIs
- **python-dotenv** - Environment variable management
- **pyyaml** - YAML file parsing
- **colorama** - Colored terminal output
- **tqdm** - Progress bars
- **pytz** - Timezone handling

### Install All Dependencies
```bash
# Navigate to project directory
cd /path/to/Hackathon0Gold

# Install from requirements.txt
pip install -r requirements.txt

# Verify key packages
python -c "import playwright; import selenium; import undetected_chromedriver; print('✅ All imports successful')"
```

---

## 🌐 Network & External Services

### Required
- **Gmail OAuth** - Gmail account with 2FA (optional but recommended)
- **Facebook Account** - Personal account (not business)
- **WhatsApp Account** - Active WhatsApp account
- **LinkedIn Account** - LinkedIn profile
- **Instagram Account** - Instagram account

### Internet Requirements
- **Bandwidth:** 1+ Mbps upload/download
- **Latency:** < 200ms ideal (< 1000ms acceptable)
- **Uptime:** 99%+ (for 24/7 monitoring)
- **No Firewall Restrictions:** Allow outbound connections to:
  - gmail.com
  - facebook.com
  - whatsapp.com
  - linkedin.com
  - instagram.com
  - google.com

---

## 🔑 Authentication & Accounts

### Gmail
1. Enable 2-Step Verification (recommended)
2. Create App Password: https://myaccount.google.com/apppasswords
3. First run will prompt for OAuth login
4. Token automatically saved to `session/gmail_session/`

### Facebook Messenger
1. Create/use personal Facebook account
2. First run will show browser window
3. Manually log in when prompted
4. Session saved to `session/facebook_js_extract/`

### WhatsApp Web
1. Have WhatsApp installed on phone
2. First run will show browser window
3. Scan QR code with phone
4. Session saved to `session/whatsapp_session/`

### LinkedIn
1. Active LinkedIn account (free or premium)
2. First run will show browser window
3. Manually log in when prompted
4. Session saved to `session/linkedin_session/`

### Instagram
1. Active Instagram account
2. First run will show browser window
3. Manually log in when prompted (may require code from phone)
4. Session saved to `session/instagram_session/`

---

## 📋 Pre-Installation Checklist

Run this before starting:

```bash
# Check Python
python --version
# Should be 3.11 or higher

# Check Node.js
node --version
npm --version
# Should be Node 18+ and npm 9+

# Check internet
ping google.com
# Should get responses

# Create project directory if needed
mkdir -p "C:\Users\14loa\Desktop\IT\GIAIC\Q4 spec kit\Hackathon0Gold"
cd "C:\Users\14loa\Desktop\IT\GIAIC\Q4 spec kit\Hackathon0Gold"

# Clone or verify project files exist
ls -la | grep -E "(watchers|ecosystem|STARTUP)"
# Should show: watchers/, ecosystem.config.js, STARTUP_GUIDE.md
```

---

## 🚀 Installation Steps

### Step 1: Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt

# This may take 5-10 minutes
```

### Step 2: Install Node.js Packages (PM2)
```bash
npm install -g pm2
pm2 --version
```

### Step 3: Create Session Directories
```bash
mkdir -p session/{gmail_session,facebook_js_extract,whatsapp_session,linkedin_session,instagram_session}
mkdir -p Needs_Action Pending_Approval Approved Done
mkdir -p watchers/logs
```

### Step 4: Verify Watcher Files
```bash
# Verify all 5 watchers exist
ls -lh watchers/{gmail_watcher,whatsapp_persistent,linkedin_persistent,instagram_watcher_fixed,facebook_watcher_js_extract}.py

# Should show all 5 files (no errors)
```

### Step 5: Start Watchers
```bash
pm2 start ecosystem.config.js

# Verify they started
pm2 list
```

### Step 6: Test Message Capture
```bash
# Monitor in separate terminal
python monitor-messages.py

# Send test messages to each platform
# Should see them appear in Needs_Action/ folder
```

---

## 🛠️ Troubleshooting Installation

### Problem: "Python not found"
```bash
# Verify Python is in PATH
python --version

# If not found, add Python to PATH:
# 1. Go to Control Panel → System → Environment Variables
# 2. Edit PATH variable
# 3. Add: C:\Users\14loa\AppData\Local\Programs\Python\Python314
# 4. Restart terminal
```

### Problem: "pip install fails"
```bash
# Try upgrading pip first
python -m pip install --upgrade pip

# Then try requirements again
pip install -r requirements.txt --user

# Or install packages individually
pip install playwright
pip install selenium
# etc.
```

### Problem: "undetected-chromedriver not found"
```bash
# Install explicitly
pip install undetected-chromedriver

# Verify
python -c "import undetected_chromedriver; print('✅ OK')"
```

### Problem: "PM2 not found"
```bash
# Verify Node.js is installed
node --version

# If missing, download from https://nodejs.org/

# Then install PM2
npm install -g pm2

# Verify
pm2 --version
```

### Problem: "Playwright browser not found"
```bash
# Playwright downloads browsers automatically
# But you can pre-download them:
python -m playwright install

# This downloads Chromium, Firefox, WebKit
```

---

## ✅ Post-Installation Verification

After installation, run these checks:

```bash
# 1. Python packages
python -c "import playwright; import selenium; import undetected_chromedriver; import google_auth_oauthlib; print('✅ All packages OK')"

# 2. PM2
pm2 --version

# 3. Watcher files
ls watchers/*.py | wc -l
# Should show 7+ files

# 4. Folders
ls -d Needs_Action Pending_Approval session watchers
# Should show all folders

# 5. Start watchers
pm2 start ecosystem.config.js

# 6. Verify running
pm2 list
# Should show 5 watchers as "online"

# 7. Check logs
pm2 logs --lines 5
```

---

## 🔄 Maintenance

### Weekly
- [ ] Check disk space: `df -h`
- [ ] Review logs: `pm2 logs --lines 100`
- [ ] Verify all 5 watchers online: `pm2 list`

### Monthly
- [ ] Clear old logs: `rm ~/.pm2/logs/*.log`
- [ ] Archive captured messages: `cp -r Needs_Action/ backups/`
- [ ] Update dependencies: `pip install --upgrade -r requirements.txt`

### Quarterly
- [ ] Delete old session data if buggy: `rm -rf session/*/`
- [ ] Update Python/Node.js if major versions available
- [ ] Review and update keywords if needed

---

## 📞 Support Resources

- **Python Issues:** https://stackoverflow.com/questions/tagged/python
- **Playwright:** https://playwright.dev/python/
- **Selenium:** https://www.selenium.dev/
- **PM2:** https://pm2.keymetrics.io/
- **Facebook API:** https://developers.facebook.com/
- **Gmail API:** https://developers.google.com/gmail

---

**System is ready for installation and deployment!** ✨
