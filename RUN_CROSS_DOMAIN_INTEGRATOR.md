# How to Run Cross Domain Integrator

**Status**: ✅ Ready to use
**Type**: Gold Tier Skill
**Auto-Schedule**: Every 30 minutes (via PM2)
**Manual Trigger**: 3 easy options below

---

## 🚀 Quick Start

### Option 1: Windows Batch (Easiest for Windows)

**Simply double-click:**
```
run-cross-domain.bat
```

A command window will open, show the results, and wait for you to press Enter.

**Or run from command line:**
```
run-cross-domain.bat
```

---

### Option 2: PowerShell (Windows - Colored Output)

**Run from PowerShell:**
```powershell
powershell -ExecutionPolicy Bypass -File run-cross-domain.ps1
```

**Or from PowerShell prompt:**
```powershell
./run-cross-domain.ps1
```

---

### Option 3: Bash/Shell (Windows/Mac/Linux)

**Run from terminal:**
```bash
bash run-cross-domain.sh
```

**Or make it executable and run:**
```bash
chmod +x run-cross-domain.sh
./run-cross-domain.sh
```

---

## 📊 What Happens When You Run It

```
Step 1: Scans /Needs_Action/ folder
        ↓
Step 2: Classifies each message
        - PERSONAL (email/WhatsApp)
        - BUSINESS (LinkedIn/Twitter/Facebook)
        ↓
Step 3: Routes messages
        - PERSONAL → /Pending_Approval/ (HITL)
        - BUSINESS → /Approved/ (Auto LinkedIn Poster)
        ↓
Step 4: Creates unified summary
        - File: /Logs/cross_domain_[date].md
        ↓
Step 5: Shows results in console
```

---

## 📋 Example Output

```
======================================================================
CROSS DOMAIN INTEGRATOR - Manual Trigger
======================================================================

Timestamp: 03/18/2026 07:45:00
Location: C:\...\Hackathon0Gold

[RUNNING] Cross Domain Integrator...

======================================================================
[PHASE 1] SCANNING /Needs_Action/
OK: Found 6 item(s) to classify

[PHASE 2] CLASSIFYING & ROUTING
  [P] test_personal.md                    | PERSONAL | 95% confidence
  [P] test_personal_001.md                | PERSONAL | 95% confidence
  [B] test_business.md                    | BUSINESS | 98% confidence
  [B] test_business_001.md                | BUSINESS | 99% confidence

[PHASE 3] GENERATING UNIFIED SUMMARY
OK: Summary created: Logs\cross_domain_2026-03-18.md

======================================================================
[SUCCESS] Integration completed successfully!
======================================================================

Next: Check /Pending_Approval/ and /Approved/ folders
Summary: Logs/cross_domain_*.md
```

---

## 🔄 Automation (Already Running)

**The skill runs automatically every 30 minutes via PM2:**

```bash
# Check status
pm2 list

# View live logs
pm2 logs cross_domain_integrator -f

# View last 50 lines
pm2 logs cross_domain_integrator --lines 50
```

---

## 📁 Where Results Go

**PERSONAL items** (require your approval):
```
/Pending_Approval/
├── test_personal_001.md
├── email_*.md
└── whatsapp_*.md
```

**BUSINESS items** (ready for Auto LinkedIn Poster):
```
/Approved/
├── test_business_001.md
├── linkedin_*.md
├── twitter_*.md
└── facebook_*.md
```

**Summary report** (complete breakdown):
```
/Logs/
└── cross_domain_2026-03-18.md
```

---

## ✅ Verification

After running, verify it worked:

```bash
# Count items routed
ls /Pending_Approval/ | wc -l        # Should see PERSONAL items
ls /Approved/ | wc -l                 # Should see BUSINESS items

# Check summary
cat Logs/cross_domain_*.md | head -50

# Check logs
pm2 logs cross_domain_integrator --lines 20
```

---

## 🎯 Next Steps

1. **Run once manually** to test:
   ```
   run-cross-domain.bat
   ```

2. **Check the results**:
   - Open `/Pending_Approval/` - items waiting for your approval
   - Open `/Approved/` - items ready for Auto LinkedIn Poster
   - Open `/Logs/` - read the summary report

3. **Approve/Reject Personal Items**:
   - Use HITL Approval Handler to make decisions

4. **Business Items Auto-Process**:
   - Auto LinkedIn Poster will handle these automatically

5. **Daily Monitoring**:
   - Skill runs every 30 min automatically (no action needed!)
   - Check logs anytime with: `pm2 logs cross_domain_integrator`

---

## 🆘 Troubleshooting

**Batch file won't run?**
- Right-click → Run as Administrator
- Or open Command Prompt, navigate to folder, type: `run-cross-domain.bat`

**PowerShell execution policy error?**
- Run: `powershell -ExecutionPolicy Bypass -File run-cross-domain.ps1`

**No items found?**
- Check if `/Needs_Action/` folder has files
- Verify watchers are running: `pm2 list`

**Need to stop auto-scheduler?**
- Run: `pm2 stop cross_domain_integrator`

**Need to restart auto-scheduler?**
- Run: `pm2 restart cross_domain_integrator`

---

## 📞 Commands Quick Reference

```bash
# Manual trigger options
run-cross-domain.bat                          # Windows batch
powershell -ExecutionPolicy Bypass -File run-cross-domain.ps1  # PowerShell
bash run-cross-domain.sh                      # Bash/Shell

# PM2 auto-scheduler commands
pm2 list                                      # Status
pm2 logs cross_domain_integrator -f           # Live logs
pm2 logs cross_domain_integrator --lines 50   # Last 50 lines
pm2 stop cross_domain_integrator              # Stop scheduler
pm2 restart cross_domain_integrator           # Restart scheduler
pm2 delete cross_domain_integrator            # Remove scheduler

# Check results
ls Pending_Approval/                          # PERSONAL items
ls Approved/                                  # BUSINESS items
ls Logs/cross_domain_*.md                     # Summaries
```

---

**Status**: ✅ Ready to use
**Created**: 2026-03-18
**Last Updated**: 2026-03-18
