---
title: AI Social Media Manager - Quick Test Start
date: 2026-03-29
status: READY
---

# Quick Test Start Guide

## 🚀 5-Minute Test (Fastest Way)

### Option 1: Python (Windows/Mac/Linux)
```bash
# Simply run:
python scripts/run_workflow_test.py

# Then select option 1 (Single Platform Test)
# Follow the prompts
```

### Option 2: Bash (Linux/Mac)
```bash
# Make executable (first time only)
chmod +x scripts/run_workflow_test.sh

# Run interactive menu
./scripts/run_workflow_test.sh

# Or run specific platform
./scripts/run_workflow_test.sh --platform facebook --count 1
```

---

## 🎯 Common Test Commands

### Single Platform (Facebook)
```bash
# Python
python scripts/run_workflow_test.py --platform facebook

# Bash
./scripts/run_workflow_test.sh --platform facebook --count 1
```

### All 6 Platforms
```bash
# Python
python scripts/run_workflow_test.py --batch

# Bash
./scripts/run_workflow_test.sh --batch
```

### Manual Step-by-Step (Most Control)
```bash
# Terminal 1: Start orchestrator
python scripts/master_orchestrator.py

# Terminal 2: Create draft
python scripts/trigger_posts.py -p facebook -c "Test!" --preview

# Terminal 3: Approve (wait 3 seconds first)
mv Pending_Approval/POST_*.md Approved/

# Watch Terminal 1 for success (10-30 seconds)
ls Done/processed_POST_*.md
```

---

## ✅ What Each Test Does

### Single Platform Test (3-5 min)
1. ✅ Starts orchestrator
2. ✅ Creates 1 draft post
3. ✅ Approves it
4. ✅ Monitors processing
5. ✅ Verifies success

**Good for:** Testing one platform, quick validation

### Batch Test (10-15 min)
1. ✅ Starts orchestrator
2. ✅ Creates 6 draft posts (all platforms)
3. ✅ Approves all
4. ✅ Monitors all processing
5. ✅ Generates report

**Good for:** Full system validation, seeing all platforms work

### Custom Test (Flexible)
1. ✅ Pick platform(s)
2. ✅ Pick number of posts
3. ✅ Creates, approves, monitors

**Good for:** Testing specific scenarios

---

## 📊 Checking Results

### Quick Status Check
```bash
# View file counts
echo "Pending: $(ls Pending_Approval/POST_*.md 2>/dev/null | wc -l)"
echo "Approved: $(ls Approved/POST_*.md 2>/dev/null | wc -l)"
echo "Done: $(ls Done/processed_POST_*.md 2>/dev/null | wc -l)"

# View latest logs
tail -20 Logs/orchestrator_*.log

# View status JSON
cat Logs/status_*.json | python -m json.tool
```

### Watch in Real-Time
```bash
# Terminal 1: Orchestrator
python scripts/master_orchestrator.py

# Terminal 2: Watch files change
watch -n 1 'echo "Pending: $(ls Pending_Approval/POST_*.md 2>/dev/null | wc -l) | Approved: $(ls Approved/POST_*.md 2>/dev/null | wc -l) | Done: $(ls Done/processed_POST_*.md 2>/dev/null | wc -l)"'

# Terminal 3: Watch logs
tail -f Logs/orchestrator_*.log
```

---

## 🔧 Troubleshooting

### "Module not found" Error
```bash
pip install playwright pyyaml watchdog
python -m playwright install
```

### "Browser failed to login"
```bash
# Clear saved sessions and re-login manually once
rm -rf session/*

# Then run test again - browser will prompt for login
python scripts/run_workflow_test.py --platform facebook
```

### "Orchestrator not running"
```bash
# Make sure no other instance is running
pkill -f master_orchestrator

# Restart
python scripts/master_orchestrator.py
```

### "Files stuck in Approved"
```bash
# Check if orchestrator is running
ps aux | grep master_orchestrator

# Check logs
grep -i "error" Logs/orchestrator_*.log

# Restart orchestrator
pkill -f master_orchestrator
sleep 2
python scripts/master_orchestrator.py
```

---

## 📈 Expected Times

| Component | Time |
|-----------|------|
| Draft creation | 1-2 sec |
| File detection | 5 sec |
| Browser startup | 2-3 sec |
| Platform login | 5-10 sec |
| Post interaction | 5-10 sec |
| **Total per post** | **20-35 sec** |

---

## ✨ Success Indicators

✅ **Test Passed When:**
- Draft created in Pending_Approval/
- File moved to Approved/
- Orchestrator detected within 5 sec
- Executor posted to platform
- File moved to Done/
- No errors in logs
- Status shows "PASSED"

❌ **Test Failed When:**
- Files stuck in Approved/
- Errors in logs
- Timeout waiting for completion
- Browser login failed
- Status shows "FAILED"

---

## 🎓 Full Documentation

For detailed test guide with troubleshooting:
→ See **`docs/social_automation_test.md`**

For workflow architecture:
→ See **`MASTER_ORCHESTRATOR_README.md`**

For executor details:
→ See **`SOCIAL_MEDIA_EXECUTOR_README.md`**

---

## 💡 Pro Tips

1. **Use Python** (`run_workflow_test.py`) on Windows - it's more reliable
2. **Keep 3 terminals open** during manual testing:
   - Orchestrator running
   - Logs tailing
   - Command input
3. **Start fresh** - rm old test files before new test:
   ```bash
   rm -f Pending_Approval/POST_test_*.md
   rm -f Approved/POST_test_*.md
   rm -f Done/processed_POST_test_*.md
   ```
4. **Check session folder** if browser keeps failing:
   ```bash
   ls -la session/
   # Should have browser data files
   ```
5. **Monitor audit logs** to see what system did:
   ```bash
   cat Logs/audit_*.json | python -m json.tool
   ```

---

**Status:** ✅ READY FOR TESTING
**Last Updated:** 2026-03-29
