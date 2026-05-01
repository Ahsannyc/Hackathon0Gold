# Weekly Audit Briefer - Gold Tier Setup & Integration

**Status:** ✅ READY
**Date:** 2026-03-27
**Component:** 7th Gold Tier System Component
**Version:** 1.0

---

## 📋 Quick Start

### 1. Verify Integration
```bash
# Check scheduler is running
pm2 list | grep task-scheduler

# Expected: task-scheduler (ID 0) - ONLINE
```

### 2. Generate Manual Briefing (Anytime)
```bash
python skills/weekly_audit_briefer.py
# Output: Briefings/ceo_briefing_YYYY-MM-DD.md
```

### 3. Check Latest Briefing
```bash
ls -la Briefings/
cat Briefings/ceo_briefing_*.md | head -50
```

---

## 🔐 Automatic Weekly Run (Integrated)

### When Runs
- **Day:** Monday (0=Monday, 6=Sunday)
- **Time:** 8:00 AM - 9:00 AM
- **Frequency:** Once per week
- **Handler:** task-scheduler process (ID 0)

### How It Works
```
Monday 8 AM
    ↓
task-scheduler checks (every 60 seconds)
    ↓
Detects: is_monday AND hour >= 8 AND hour < 9
    ↓
Calls: weekly_audit_briefer.run()
    ↓
Generates: Briefings/ceo_briefing_2026-03-31.md (example)
    ↓
Logs: skills/logs/weekly_audit_briefer.log
```

---

## 📊 What Gets Audited

### 1. System Metrics (from `/Logs`)
- Total messages processed (6 platforms)
- Business vs Personal item split
- Classification confidence average
- Items successfully routed
- Platform breakdown (Gmail, WhatsApp, LinkedIn, Instagram, Facebook, Twitter)

### 2. Completed Tasks (from `/Done`)
- Count of tasks completed this week
- File names and modification dates
- Top 10 tasks listed

### 3. Revenue Indicators (Pattern Matching)
- Subscription mentions
- Payment mentions
- Invoice mentions
- High-value leads (>$500 per Company_Handbook.md)
- Expense mentions

### 4. Company Goals (from `Business_Goals.md`)
- Q1 2026 targets
- Key metrics tracked
- Success criteria

### 5. Handbook Compliance (from `Company_Handbook.md`)
- Active rules & policies
- Payment approval thresholds
- Operational guidelines

### 6. Bottleneck Analysis
- Low task completion detection
- HITL approval delays
- Classification accuracy issues
- Limited platform sources
- Item type imbalance

---

## 📁 File Locations

| Component | Location |
|-----------|----------|
| **Skill Script** | `skills/weekly_audit_briefer.py` (11 KB) |
| **Scheduler** | `scheduler.py` (6 KB) |
| **PM2 Config** | `ecosystem.config.js` (includes task-scheduler) |
| **Business Goals** | `Business_Goals.md` |
| **Company Rules** | `Company_Handbook.md` |
| **Generated Briefings** | `Briefings/ceo_briefing_[date].md` |
| **Skill Logs** | `skills/logs/weekly_audit_briefer.log` |
| **Scheduler Logs** | `.pm2/logs/task-scheduler-*.log` |
| **Data Sources** | `/Done/`, `/Logs/` |

---

## 🧪 Test Manual Generation

### Test 1: Generate Briefing Now
```bash
python skills/weekly_audit_briefer.py
```

**Expected Output:**
```
2026-03-27 21:31:19 - WEEKLY AUDIT BRIEFER STARTED
2026-03-27 21:31:19 - Found X completed tasks
2026-03-27 21:31:19 - Extracted metrics from Y log files
2026-03-27 21:31:19 - Briefing saved: Briefings/ceo_briefing_2026-03-27.md
```

**Verify:**
```bash
ls -la Briefings/ceo_briefing_*.md
cat Briefings/ceo_briefing_2026-03-27.md | grep -E "Executive Summary|Performance Metrics"
```

---

### Test 2: Verify Scheduler Integration
```bash
# Check scheduler process
pm2 list | grep task-scheduler

# Check logs
pm2 logs task-scheduler --lines 50

# Expected: "SCHEDULER STARTED" and "Check interval: 60 seconds"
```

**Test Weekly Run:**
- Wait until next Monday 8:00 AM, OR
- Manually test by:
  1. Setting system clock to Monday 8 AM
  2. Running: `python scheduler.py`
  3. Should detect Monday 8 AM and trigger briefer

---

### Test 3: Verify Briefing Content
Open generated briefing and check sections:

```bash
cat Briefings/ceo_briefing_2026-03-27.md
```

Expected sections:
- ✅ Executive Summary (with Key Numbers)
- ✅ Performance Metrics (Processing stats)
- ✅ Active Platforms (Gmail, WhatsApp, etc.)
- ✅ Revenue Indicators (Pattern matches)
- ✅ Completed Tasks This Week
- ✅ Bottleneck Analysis
- ✅ Business Goals Progress
- ✅ Company Handbook Compliance
- ✅ Recommendations
- ✅ System Status Summary

---

## 🛠️ Troubleshooting

### Problem: Scheduler Not Running
```bash
# Check PM2 status
pm2 list | grep task-scheduler

# If not online, restart:
pm2 restart task-scheduler

# Check logs for errors:
pm2 logs task-scheduler --lines 100
```

### Problem: Briefing Not Generated on Monday
```bash
# Verify scheduler is running:
pm2 status task-scheduler

# Check logs for Monday detection:
pm2 logs task-scheduler | grep "Monday\|8:00\|audit"

# Manual test (set system clock to Monday 8 AM):
python skills/weekly_audit_briefer.py
```

### Problem: Missing Data in Briefing
1. Check `/Done` folder has completed task files
2. Check `/Logs` folder has cross_domain_*.md files
3. Verify `Company_Handbook.md` exists
4. Verify `Business_Goals.md` exists

```bash
ls Done/
ls Logs/
cat Company_Handbook.md
cat Business_Goals.md
```

### Problem: Low Confidence Score in Briefing
- Indicates message classification accuracy is below 80%
- Check recent logs in `/Logs/`
- May indicate need to tune keyword filters

---

## 📊 System Architecture

```
GOLD TIER SYSTEM (7 Components):
├─ 6 Watchers (Gmail, WhatsApp, LinkedIn, Instagram, Facebook, Twitter)
├─ Task-Scheduler Process (ID 0)
│  ├─ Runs continuously (check every 60 seconds)
│  ├─ Detects: Monday 8:00 AM
│  └─ Triggers: weekly_audit_briefer.py
├─ Weekly Audit Briefer Skill
│  ├─ Reads: /Done, /Logs, Company_Handbook.md, Business_Goals.md
│  ├─ Audits: Metrics, Revenue, Bottlenecks, Compliance
│  └─ Outputs: Briefings/ceo_briefing_[date].md
└─ PM2 Ecosystem Configuration
   └─ Manages: All 7 processes with auto-restart
```

---

## 📋 Briefing Template Structure

Each weekly briefing includes:

1. **Header**: Date, generation timestamp, status
2. **Executive Summary**: Overall status + key numbers
3. **Performance Metrics**: Table with processing stats
4. **Active Platforms**: Breakdown by source
5. **Revenue Indicators**: Financial pattern matches
6. **Completed Tasks**: List of done items this week
7. **Bottleneck Analysis**: Issues & constraints
8. **Business Goals**: Progress vs targets
9. **Handbook Compliance**: Policy adherence
10. **Recommendations**: Action items for week
11. **System Status**: Health summary

---

## 🔄 Weekly Maintenance

### Monday Morning (After Briefing)
```bash
# Read briefing
cat Briefings/ceo_briefing_$(date +%Y-%m-%d).md

# Note any bottlenecks
# Plan week around recommendations
```

### Throughout Week
```bash
# Check for new high-value leads
grep -r "payment\|invoice" Needs_Action/

# Monitor task completion
ls Done/ | wc -l

# Track platform activity
ls Logs/cross_domain_*.md | tail -1 | xargs cat
```

### End of Week
- Review metrics trend vs previous week
- Update Business_Goals.md if targets change
- Update Company_Handbook.md if policies change

---

## ✅ Success Indicators

**Weekly Briefer Working When:**
1. ✅ task-scheduler shows "online" in `pm2 list`
2. ✅ Briefings folder contains `ceo_briefing_*.md` files
3. ✅ Briefing generated automatically on Monday 8 AM
4. ✅ Log shows "Weekly Audit Briefer" execution
5. ✅ Briefing contains populated metrics tables

---

## 📞 Quick Commands

```bash
# Start everything
pm2 start ecosystem.config.js

# Check status
pm2 list

# Generate briefing manually (any time)
python skills/weekly_audit_briefer.py

# View latest briefing
cat Briefings/ceo_briefing_*.md | tail -50

# View scheduler logs
pm2 logs task-scheduler

# Save state
pm2 save

# Monitor messages in real-time
python monitor-messages.py
```

---

## 🎯 Next Steps

1. **Verify Scheduler Running**: `pm2 list | grep task-scheduler`
2. **Generate Test Briefing**: `python skills/weekly_audit_briefer.py`
3. **Review Output**: Check `Briefings/ceo_briefing_*.md`
4. **Wait for Monday 8 AM**: Automatic generation will trigger
5. **Check Logs**: Verify successful generation in scheduler logs

---

**Weekly Audit Briefer is now integrated into your Gold Tier 7-component system!** 📊✨
