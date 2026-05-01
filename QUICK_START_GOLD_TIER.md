# Gold Tier Quick Start (5 Minutes)
**Status:** Production Ready ✅  
**Difficulty:** Moderate (setup) → Easy (use)  
**Time to First Task:** ~30 minutes

---

## 🚀 The 5-Minute Summary

**What you have:**
- Autonomous task execution (Ralph Wiggum)
- Full accounting (Odoo integration)
- Social media automation (Facebook, Instagram, Twitter)
- Weekly business intelligence (CEO Briefing)
- Enterprise reliability (error recovery, audit logging)

**One command to start everything:**
```bash
# In Hackathon0Gold directory

# 1. Start Odoo (background)
docker-compose up -d

# 2. Start Odoo MCP Server (new terminal)
cd mcp_servers/odoo-mcp && npm install && npm start

# 3. Start Social MCP Server (new terminal)
cd mcp_servers/social-mcp && npm install && npm start

# 4. Run your first autonomous task
./tools/run_ralph_loop.sh invoice_batch_001 "Process all invoices in Needs_Action"

# 5. Check results
cat Briefings/CEO_Briefing_*.md
cat .ralph-state/invoice_batch_001.json
```

---

## ⚡ Core Commands

### Ralph Wiggum (Autonomous Tasks)
```bash
# Simple task
./tools/run_ralph_loop.sh task_001 "Your task description"

# Complex task (more iterations)
./tools/run_ralph_loop.sh task_002 "Complex task" --max-iterations 20

# Windows
tools\run_ralph_loop.bat task_001 "Your task description"
```

### Odoo (Accounting)
```bash
# Start Odoo
docker-compose up -d

# Access web UI
open http://localhost:8069

# Check Odoo logs
docker logs hackathon0_odoo

# Stop Odoo
docker-compose down
```

### Audit Logs
```bash
# View today's actions
python tools/audit_logger.py view

# View specific date
python tools/audit_logger.py view --date 2026-04-30

# Filter by actor
python tools/audit_logger.py view --actor claude_code

# Cleanup old logs
python tools/audit_logger.py cleanup
```

### CEO Briefing
```bash
# Generate briefing manually
python tools/ceo_briefing_generator.py

# Check latest briefing
cat Briefings/CEO_Briefing_*.md | sort | tail -1
```

### Error Handling
```bash
# View recent errors
python tools/error_handler.py errors --limit 10

# Process recovery queue
python tools/error_handler.py recovery email
python tools/error_handler.py recovery odoo
python tools/error_handler.py recovery social
```

---

## 📊 Key Directories

| Path | Purpose | Files |
|------|---------|-------|
| `tools/` | Core utilities | ralph, audit, error, odoo_sync, ceo_briefing |
| `mcp_servers/` | External integrations | odoo-mcp, social-mcp, email-mcp |
| `skills/` | Agent skill definitions | ralph_wiggum_skill.md |
| `Logs/` | Audit trail & system logs | audit_*.json, errors.json |
| `.ralph-state/` | Task state files | *.json per task |
| `Briefings/` | Generated reports | CEO_Briefing_*.md |
| `Accounting/` | Financial data | Monthly summaries |

---

## 🔄 Typical Workflows

### Invoice Processing (Fully Autonomous)
```
1. Email arrives with invoice request
2. Gmail Watcher detects it
3. Ralph Wiggum loop starts:
   - Read invoice details
   - Create in Odoo (draft)
   - Create approval request
   - Send to user
4. User approves in /Approved/
5. Ralph posts invoice
6. Dashboard updates
7. Customer gets invoice email
All logged in audit trail
```

### Social Media Posts (Fully Autonomous)
```
1. Content calendar updated
2. Ralph loop reads calendar
3. Generates posts for each platform:
   - Facebook: Long, conversational
   - Instagram: Visual-focused
   - Twitter: Short, threads
4. Posts simultaneously
5. Tracks engagement
6. Updates summary in Dashboard
All logged
```

### Weekly CEO Briefing (Fully Automated)
```
1. Every Monday 7 AM (scheduled)
2. CEO Briefing Generator runs:
   - Collects revenue data
   - Analyzes tasks/bottlenecks
   - Checks social metrics
   - Identifies cost anomalies
   - Generates recommendations
3. Saved to Briefings/
4. Email to user
5. Dashboard updated
```

---

## 🧪 Test Everything (5 Minutes)

```bash
# Test 1: Ralph Wiggum Loop (1 min)
./tools/run_ralph_loop.sh test_basic "Move this task to /Done"
# Check: File in /Done, state in .ralph-state/

# Test 2: Audit Logging (1 min)
python tools/audit_logger.py view --date $(date +%Y-%m-%d)
# Check: Entries showing tasks, MCPs, approvals

# Test 3: Odoo Integration (1 min)
curl http://localhost:3001/health
curl http://localhost:3001/summary
# Check: JSON responses with financial data

# Test 4: Error Handler (1 min)
python tools/error_handler.py errors
# Check: Error log format and entries

# Test 5: CEO Briefing (1 min)
python tools/ceo_briefing_generator.py
cat Briefings/CEO_Briefing_*.md | tail -50
# Check: Comprehensive report generated
```

**All passing?** ✅ System is working!

---

## ⚙️ Configuration

### Environment Variables (.env)
```bash
# Odoo
ODOO_URL=http://localhost:8069
ODOO_DB=hackathon0_business
ODOO_PASSWORD=admin

# Social Media (add real credentials)
FACEBOOK_TOKEN=your_token
INSTAGRAM_TOKEN=your_token
TWITTER_API_KEY=your_key

# Logging
RALPH_MAX_ITERATIONS=10
AUDIT_RETENTION_DAYS=90
```

### Scheduling (Cron/Task Scheduler)

**Linux/Mac (crontab):**
```bash
# Daily Odoo sync at 6 AM
0 6 * * * cd /path/to/vault && python tools/odoo_sync.py

# Weekly CEO briefing at Monday 7 AM
0 7 * * 1 cd /path/to/vault && python tools/ceo_briefing_generator.py

# Daily audit cleanup at 2 AM
0 2 * * * cd /path/to/vault && python tools/audit_logger.py cleanup
```

**Windows (Task Scheduler):**
```powershell
# Similar setup with powershell scripts
# See DEPLOYMENT_GUIDE.md for details
```

---

## 📚 Documentation Map

| Document | Purpose | Time |
|----------|---------|------|
| This file | Quick reference | 5 min |
| GOLD_TIER_COMPLETE.md | What you have | 10 min |
| RALPH_WIGGUM_GUIDE.md | Autonomous tasks | 15 min |
| DEPLOYMENT_GUIDE.md | Full setup | 30 min |
| GOLD_TIER_ARCHITECTURE.md | How it works | 20 min |

---

## 🆘 Troubleshooting

**Q: Ralph loop doesn't complete**
```bash
# Check state
cat .ralph-state/task_id.json

# Check logs
tail Logs/ralph_wiggum.log

# Check task file exists
ls -la Plans/TASK_task_id.md
```

**Q: Odoo not accessible**
```bash
# Verify running
docker ps | grep odoo

# Check port
lsof -i :8069

# Restart
docker-compose restart
```

**Q: MCP server not responding**
```bash
# Check if running
lsof -i :3001

# Check logs
npm logs

# Restart
npm start
```

**Q: Audit logs not being created**
```bash
# Check Logs dir exists
ls -la Logs/

# Check permissions
chmod 755 Logs/

# Check format
cat Logs/audit_*.json | python -m json.tool
```

---

## 💡 Pro Tips

1. **Monitor Dashboard.md** - Always current with financial data
2. **Review Briefings/ weekly** - CEO briefings have recommendations
3. **Check Logs/ralph_wiggum.log** - See what tasks completed
4. **Use ralph loops for anything** - Not just invoices
5. **Set up monitoring** - Watch Logs/ folder for issues
6. **Start small** - Test with simple tasks first
7. **Increase complexity** - Gradually use for more tasks

---

## 🎯 First Task: Email to Invoice

```bash
# 1. Create test task file
mkdir -p Plans
cat > Plans/TASK_email_to_invoice.md << 'EOF'
---
task_id: email_to_invoice
---

# Email to Invoice Task

Read emails from Needs_Action folder, create invoices in Odoo.

When done with all emails, move this file to /Done/
EOF

# 2. Run Ralph loop
./tools/run_ralph_loop.sh email_to_invoice \
  "Read all emails in Needs_Action. Create invoice in Odoo for each. Move task to /Done when complete."

# 3. Watch it work
tail -f Logs/ralph_wiggum.log

# 4. Check results
cat .ralph-state/email_to_invoice.json
```

---

## 📞 Getting Help

1. **Check logs first** - Most answers are there
2. **Read DEPLOYMENT_GUIDE.md** - Common issues
3. **Review RALPH_WIGGUM_GUIDE.md** - Task execution
4. **Check Logs/errors.json** - Error details
5. **Verify audit trail** - See what happened

---

## ✅ Verification Checklist

- [ ] Docker running: `docker ps`
- [ ] Odoo accessible: `curl http://localhost:8069`
- [ ] Odoo MCP responding: `curl http://localhost:3001/health`
- [ ] Social MCP responding: `curl http://localhost:3002/health`
- [ ] Audit logs exist: `ls Logs/audit_*.json`
- [ ] Ralph loop works: Test task completed
- [ ] CEO briefing generates: Check Briefings/ folder
- [ ] Error handler configured: Check error_handler.py
- [ ] Watchers running: PM2 list shows active
- [ ] Dashboard updates daily: Check for recent timestamps

All checked? ✅ **You're ready to go!**

---

## 🚀 Next Steps

1. **Read:** GOLD_TIER_COMPLETE.md (understand what you have)
2. **Setup:** DEPLOYMENT_GUIDE.md (full installation)
3. **Test:** Run the verification checklist above
4. **Use:** Run your first Ralph loop task
5. **Monitor:** Watch Logs/ and Dashboard.md for updates
6. **Refine:** Adjust as needed based on your workflow

---

**Status:** ✅ Ready to Deploy  
**Quality:** Production-Grade  
**Time to Value:** < 1 hour  
**Support:** See documentation links above

**Let your AI Employee start working!** 🤖⚙️
