# 🎯 GUIDE TO RUN - STEP BY STEP

**For Beginners: Complete Baby Steps to Get the Project Running**

---

## 📋 BEFORE YOU START - CHECKLIST

Check these things first (takes 2 minutes):

- [ ] Do you have Docker installed? (Check: Open terminal, type: `docker --version`)
- [ ] Do you have Python installed? (Check: Open terminal, type: `python --version`)
- [ ] Do you have Node.js installed? (Check: Open terminal, type: `node --version`)
- [ ] Do you have 8GB RAM available?
- [ ] Do you have 20GB free disk space?
- [ ] Do you have internet connection?

**If all checked:** You're ready! Continue below.

**If some unchecked:** Install them first:
- Docker: https://www.docker.com/products/docker-desktop
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/

---

## 🚀 STEP 1: OPEN THE PROJECT FOLDER

### Baby Step 1.1: Open Terminal/Command Prompt

**On Windows:**
- Press `Windows Key + R`
- Type: `cmd`
- Press Enter

**On Mac:**
- Press `Cmd + Space`
- Type: `terminal`
- Press Enter

**On Linux:**
- Press `Ctrl + Alt + T`

### Baby Step 1.2: Navigate to Project Directory

In terminal, copy and paste this command:

```bash
cd "C:\Users\14loa\Desktop\IT\GIAIC\Q4 spec kit\Hackathon0Gold"
```

Press Enter.

**What you should see:**
```
C:\Users\14loa\Desktop\IT\GIAIC\Q4 spec kit\Hackathon0Gold>
```

✅ **Step 1 Complete!**

---

## 🔑 STEP 2: CREATE THE .ENV FILE

The `.env` file is where you put your passwords and secret keys.

### Baby Step 2.1: Copy the Template File

In terminal, copy and paste this command:

```bash
copy .env.example .env
```

Press Enter.

**What you should see:**
```
        1 file(s) copied.
```

✅ **This created a file named `.env` with default values**

### Baby Step 2.2: Open the .env File to Edit It

**Option A: Using Notepad (Easiest)**

Copy and paste this command:

```bash
notepad .env
```

Press Enter.

**Notepad will open with the file content.**

**Option B: Using VS Code (If you have it)**

```bash
code .env
```

**Option C: Using any text editor**
- Find the `.env` file in the project folder
- Right-click it
- Select "Open with" and choose your text editor

✅ **Step 2.1 Complete!**

### Baby Step 2.3: Find and Edit These 4 Lines

Inside the `.env` file, find these lines:

```
POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD_HERE
POSTGRES_USER=odoo
POSTGRES_DB=hackathon0_business
ODOO_MASTER_PASSWORD=YOUR_SECURE_MASTER_PASSWORD_HERE
```

**Change them to (you decide the passwords):**

```
POSTGRES_PASSWORD=MySecurePassword123!
POSTGRES_USER=odoo
POSTGRES_DB=hackathon0_business
ODOO_MASTER_PASSWORD=MyMasterPassword456!
```

**⚠️ Important:** 
- Replace `MySecurePassword123!` with any password you want (you choose!)
- Replace `MyMasterPassword456!` with any password you want (you choose!)
- Keep everything else the same

### Baby Step 2.4: Save the File

- Press `Ctrl + S` (or use File → Save menu)
- Close the text editor

✅ **Step 2 Complete! You now have passwords set.**

---

## 🐳 STEP 3: START DOCKER

### Baby Step 3.1: Make Sure Docker is Running

**On Windows:**
1. Look for Docker icon in taskbar (bottom right)
2. If not there, open Start Menu
3. Search for "Docker Desktop"
4. Click it to start Docker

**Wait:** It takes 30 seconds to start. You'll see:
```
Docker is running
```

**On Mac:**
1. Open Applications folder
2. Find and double-click "Docker.app"
3. Wait for whale icon to appear in menu bar

**On Linux:**
```bash
sudo systemctl start docker
```

### Baby Step 3.2: Verify Docker is Running

In terminal, copy and paste:

```bash
docker --version
```

Press Enter.

**What you should see:**
```
Docker version 20.x.x, build xxxxx
```

✅ **Docker is running!**

---

## 🚀 STEP 4: START THE PROJECT

### Baby Step 4.1: Start All Services

In terminal (make sure you're in the project folder), copy and paste:

```bash
docker-compose up -d
```

Press Enter.

**What you should see (it may take 1-2 minutes first time):**
```
Creating network "hackathon0gold_default" with the default driver
Creating hackathon0gold_postgres_1 ... done
Creating hackathon0gold_odoo_1 ... done
```

✅ **The services are starting!**

### Baby Step 4.2: Wait for Everything to Start

**Wait 30-60 seconds** for containers to fully start.

You can check status with:

```bash
docker ps
```

Press Enter.

**What you should see:**
```
CONTAINER ID   IMAGE          STATUS
abc123def456   postgres:15    Up 2 minutes
def456ghi789   odoo:latest    Up 1 minute
```

✅ **If you see containers with "Up X minutes" - They're running!**

---

## ✅ STEP 5: VERIFY EVERYTHING IS WORKING

### Baby Step 5.1: Test Backend API

Open a web browser (Chrome, Firefox, Safari, Edge)

Go to: `http://localhost:8000/health`

**What you should see:**
```json
{"status": "ok"}
```

✅ **Backend is working!**

### Baby Step 5.2: Test Frontend

In the same browser, go to: `http://localhost:3000`

**What you should see:**
- A web page loads
- You see the frontend interface

✅ **Frontend is working!**

### Baby Step 5.3: Test Database

In browser, go to: `http://localhost:8000/database-status`

**What you should see:**
```json
{"status": "connected"}
```

✅ **Database is working!**

---

## 🎉 STEP 6: YOUR PROJECT IS RUNNING!

### What's Working Now?

✅ **Backend API** at `http://localhost:8000`
- API endpoints for all features
- Admin panel at `http://localhost:8000/docs`

✅ **Frontend** at `http://localhost:3000`
- Web interface
- Form submissions
- Real-time updates

✅ **Database** (PostgreSQL)
- All data storage
- User information
- Transaction logs

✅ **Odoo** Accounting System
- Business accounting
- Invoice management
- Financial tracking

✅ **All Internal Features**
- Ralph Wiggum loop
- Audit logging
- Error handling

---

## 📧 OPTIONAL STEP 7: ADD EMAIL (GMAIL)

**Do you want email integration?** (Optional - project works without it)

### Baby Step 7.1: Run Gmail Authentication Script

In terminal (same folder), copy and paste:

```bash
python authenticate_gmail.py
```

Press Enter.

**What happens:**
1. Your web browser opens automatically
2. You're asked to log into Google
3. You're asked to allow access to Gmail
4. It automatically creates the credentials files

### Baby Step 7.2: Wait for Authentication

The script will print:
```
SUCCESS! Token saved and ready to use.
Token location: /path/to/watchers/.gmail_token.json
```

### Baby Step 7.3: Restart Backend

In terminal, copy and paste:

```bash
docker-compose restart
```

Press Enter.

**What you should see:**
```
Restarting hackathon0gold_odoo_1 ... done
Restarting hackathon0gold_postgres_1 ... done
```

Wait 30 seconds.

✅ **Gmail is now integrated!**

---

## 💬 OPTIONAL STEP 8: ADD WHATSAPP

**Do you want WhatsApp integration?** (Optional)

### Baby Step 8.1: Get Twilio Credentials

1. Go to: https://www.twilio.com/console
2. Sign up (free account)
3. Find your "Account SID" - copy it
4. Find your "Auth Token" - copy it
5. Set up WhatsApp Sandbox

### Baby Step 8.2: Add to .env File

Open `.env` file again (like Step 2):

```bash
notepad .env
```

Find these lines:
```
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
```

Replace with your actual credentials:
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155552671
```

Save the file (Ctrl + S).

### Baby Step 8.3: Restart Backend

```bash
docker-compose restart
```

Wait 30 seconds.

✅ **WhatsApp is now integrated!**

---

## 🐦 OPTIONAL STEP 9: ADD TWITTER/FACEBOOK

**Do you want Twitter or Facebook?** (Optional)

### Baby Step 9.1: Get API Keys

**For Twitter:**
1. Go to: https://developer.twitter.com/
2. Create an app
3. Get API Key, Secret, and Bearer Token

**For Facebook:**
1. Go to: https://developers.facebook.com/
2. Create an app
3. Get Access Token and Page ID

### Baby Step 9.2: Add to .env File

Open `.env` file:

```bash
notepad .env
```

Find these lines:
```
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
FACEBOOK_ACCESS_TOKEN=your_access_token_here
FACEBOOK_PAGE_ID=your_page_id_here
```

Replace with your actual credentials.

Save the file (Ctrl + S).

### Baby Step 9.3: Restart Backend

```bash
docker-compose restart
```

Wait 30 seconds.

✅ **Twitter/Facebook are now integrated!**

---

## 🛑 HOW TO STOP THE PROJECT

When you're done, stop everything:

```bash
docker-compose down
```

**What you should see:**
```
Stopping hackathon0gold_odoo_1 ... done
Stopping hackathon0gold_postgres_1 ... done
Removing hackathon0gold_odoo_1 ... done
Removing hackathon0gold_postgres_1 ... done
Removing network hackathon0gold_default
```

✅ **Everything stopped safely!**

---

## 🔄 HOW TO START AGAIN LATER

When you want to run again:

```bash
docker-compose up -d
```

That's it! Everything starts again.

---

## 🆘 TROUBLESHOOTING - IF SOMETHING GOES WRONG

### Problem: "docker: command not found"
**Solution:** Docker is not installed or not in PATH
- Install Docker Desktop: https://www.docker.com/products/docker-desktop
- Restart terminal after installing

### Problem: "port 3000 already in use"
**Solution:** Another application is using port 3000
```bash
docker-compose down
docker-compose up -d
```

### Problem: "Cannot connect to docker"
**Solution:** Docker is not running
- Open Docker Desktop
- Wait for it to fully start (whale icon in taskbar)
- Try again

### Problem: "POSTGRES_PASSWORD is required"
**Solution:** You didn't set password in `.env` file
- Open `.env` file
- Find `POSTGRES_PASSWORD`
- Replace with actual password (don't leave "YOUR_SECURE_PASSWORD_HERE")
- Save and restart: `docker-compose restart`

### Problem: "Frontend shows blank page"
**Solution:** Frontend is still loading
- Wait 30 seconds
- Hard refresh browser: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)

### Problem: "API returns error"
**Solution:** Backend may not be fully started
- Wait 60 seconds
- Check Docker: `docker ps`
- Check logs: `docker logs hackathon0gold_backend_1`

---

## ✨ QUICK REFERENCE COMMANDS

**Keep these handy:**

```bash
# Start the project
docker-compose up -d

# Stop the project
docker-compose down

# Check status
docker ps

# View logs (backend)
docker logs -f hackathon0gold_backend_1

# View logs (database)
docker logs -f hackathon0gold_postgres_1

# Restart everything
docker-compose restart

# Add Gmail integration
python authenticate_gmail.py

# Edit configuration
notepad .env
```

---

## 📍 WHERE TO ACCESS YOUR PROJECT

| Component | URL | What You See |
|-----------|-----|---|
| Frontend | http://localhost:3000 | Web interface |
| Backend API | http://localhost:8000 | Raw API responses |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Database Status | http://localhost:8000/database-status | Connection status |
| Health Check | http://localhost:8000/health | Backend status |

---

## 📚 NEXT STEPS AFTER RUNNING

1. **Explore the Frontend**
   - Go to http://localhost:3000
   - Click around, test features
   - Submit a form if available

2. **Try the API**
   - Go to http://localhost:8000/docs
   - Try out different API endpoints
   - See real responses

3. **Add Integrations** (Optional)
   - Follow Steps 7, 8, 9 above
   - Add Gmail, WhatsApp, Twitter, Facebook

4. **Review Documentation**
   - Read `FINAL_VERIFICATION_AND_RUN_GUIDE.md`
   - Read `README_GOLD_TIER.md`
   - Understand the architecture

5. **Start Using Features**
   - Create tasks
   - Set up automation
   - Run autonomous operations

---

## 🎓 UNDERSTANDING WHAT YOU HAVE

**This project has:**

✅ **Frontend** - A web interface you can interact with
✅ **Backend** - An API that handles all operations
✅ **Database** - PostgreSQL storing all your data
✅ **Odoo** - Business accounting system
✅ **Watchers** - Scripts monitoring Gmail, WhatsApp, etc.
✅ **MCP Servers** - Tools for external integrations
✅ **Automation** - Ralph Wiggum loop for autonomous tasks
✅ **Logging** - Audit trail of everything

**All running at the same time in Docker containers.**

---

## 🎯 YOU'RE READY!

Follow these steps in order, and you'll have a fully running project in **5 minutes**.

**Any questions?** Check the error messages - they usually tell you what's wrong and how to fix it.

**Need more help?** Read:
- `FINAL_VERIFICATION_AND_RUN_GUIDE.md` - Detailed setup
- `QUICK_START_SETUP.md` - Quick reference
- `README_GOLD_TIER.md` - Full documentation

---

**Good luck! 🚀**
