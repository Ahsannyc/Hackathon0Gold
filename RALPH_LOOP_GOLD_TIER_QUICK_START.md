# Ralph Wiggum Loop - Gold Tier Quick Start

## Run Commands

### 1️⃣ Full Multi-Step Processing (Recommended)
```bash
python3 tools/ralph_loop_runner.py "Process multi-step task in Needs_Action" --max-iterations 20
```

### 2️⃣ Convenience Mode (Auto-detect all)
```bash
python3 tools/ralph_loop_runner.py --process-needs-action --max-iterations 20
```

### 3️⃣ Custom Prompt
```bash
python3 tools/ralph_loop_runner.py "Your task description here" --max-iterations 20
```

### 4️⃣ Wrapper Script (if available)
```bash
./ralph:loop "Process multi-step task in Needs_Action" --max-iterations
```

---

## Testing (Fast Setup)

### Step 1: Sample files already created!
```bash
ls -la Needs_Action/test_multistep_*.md
```

Two test files ready:
- ✅ `test_multistep_sales_lead.md` (BUSINESS domain)
- ✅ `test_multistep_invoice.md` (PERSONAL domain)

### Step 2: Run the loop
```bash
python3 tools/ralph_loop_runner.py --process-needs-action --max-iterations 20
```

### Step 3: Monitor output
```
🎯 RALPH WIGGUM LOOP - GOLD TIER (Multi-Step Tasks)
🔄 ITERATION 1/20
📄 Processing: test_multistep_sales_lead.md
   🌟 Multi-step task detected: sales_workflow
   📋 Workflow: scan → draft → hitl → approve → publish
✓ Plan created: plan_20260329_*.md
🌐 GOLD TIER: Cross Domain Integration
⏳ Iteration 1 complete - 1 task(s) remaining
```

### Step 4: Verify completion
```bash
# Check audit logs
tail -20 Logs/audit_2026-03-29.json

# Check plans created
ls -la Plans/plan_*.md

# Check cross domain summary
cat Logs/cross_domain_2026-03-29.md

# When done, verify Done folder
ls -la Done/
```

---

## What Happens at Each Step

### 🔄 Iteration 1: Scan & Plan
- Scans `/Needs_Action/` for all files
- Detects multi-step workflows (sales, payment, communication)
- Creates detailed Plan.md in `/Plans/`
- Classifies task domain: BUSINESS or PERSONAL
- Logs to audit trail

### 🌐 Iteration 2: Cross Domain Integration
- Runs Cross Domain Integrator
- Routes BUSINESS → Auto LinkedIn Poster (draft)
- Routes PERSONAL → /Pending_Approval (HITL)
- Creates unified summary in `/Logs/cross_domain_*.md`

### 📋 Iteration 3+: HITL Processing
- Waits for human approval in `/Pending_Approval/`
- Once approved (moved to `/Approved/`):
  - BUSINESS: Auto-publishes via MCP
  - PERSONAL: Executes action via MCP
- Logs completion with full workflow history

### ✅ Final: Completion
- All files moved to `/Done/`
- Outputs: `<promise>TASK_COMPLETE</promise>`
- Audit trail complete with timestamps

---

## File Movements

### Sales Lead (BUSINESS)
```
/Needs_Action/test_multistep_sales_lead.md
    ↓ (Iteration 1: Create Plan)
/Plans/plan_*.md
    ↓ (Iteration 2: Auto LinkedIn Poster creates draft)
/Pending_Approval/linkedin_post_*.md
    ↓ (Human approves)
/Approved/linkedin_post_*.md
    ↓ (Publish to LinkedIn)
/Done/processed_*.md + /Done/plan_*.md
    + Audit log entry
```

### Invoice (PERSONAL)
```
/Needs_Action/test_multistep_invoice.md
    ↓ (Iteration 1: Create Plan)
/Plans/plan_*.md
    ↓ (Iteration 2: Cross Domain routes to HITL)
/Pending_Approval/plan_*.md
    ↓ (Human approves payment)
/Approved/plan_*.md
    ↓ (MCP processes payment)
/Done/processed_*.md + /Done/plan_*.md
    + Audit log entry
```

---

## Key Enhancements

| Feature | Silver Tier | Gold Tier |
|---------|-------------|-----------|
| Max Iterations | 10 | **20** |
| Multi-step detection | Basic | **Advanced** |
| Domain classification | No | **Yes (BUSINESS/PERSONAL)** |
| Audit logging | No | **Full trail** |
| Cross Domain Integration | No | **Yes** |
| Workflow types | 1 | **3+** |
| HITL integration | Basic | **Full workflow** |
| MCP automation | No | **Yes** |

---

## Expected Output

```
✅ SUCCESS: All tasks completed!

<promise>TASK_COMPLETE</promise>
```

With audit trail entries like:

```json
{
  "timestamp": "2026-03-29T01:24:15.123456",
  "action_type": "loop_end",
  "actor": "ralph_loop_runner",
  "status": "completed",
  "details": {
    "iterations": 3,
    "tasks_processed": 2,
    "multi_step_tasks": 2,
    "complete": true
  }
}
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Loop hits max iterations | Increase `--max-iterations 30` |
| Tasks stuck in /Pending_Approval | Manually approve or increase iterations |
| No Plans created | Check `/Needs_Action/` has proper YAML frontmatter |
| Audit logs missing | Verify AuditLogger import: `python -c "from skills.audit_logger import AuditLogger; print('OK')"` |
| Cross Domain fails | Check keywords in task content (sales, client, invoice, payment) |

---

## Files Updated/Created

```
✅ tools/ralph_loop_runner.py (UPDATED)
   - Extended to 20 iterations
   - Multi-step workflow detection
   - Cross Domain Integrator integration
   - Full audit logging
   - Domain classification (BUSINESS/PERSONAL)

✅ Needs_Action/test_multistep_sales_lead.md (NEW)
   - Sample sales workflow for testing

✅ Needs_Action/test_multistep_invoice.md (NEW)
   - Sample payment workflow for testing

✅ RALPH_LOOP_GOLD_TIER_GUIDE.md (NEW)
   - Complete guide with detailed testing

✅ RALPH_LOOP_GOLD_TIER_QUICK_START.md (THIS FILE)
   - Quick reference
```

---

## Next: Deploy to PM2

```bash
# Start loop runner as PM2 process (every 30 minutes)
pm2 start tools/ralph_loop_runner.py --name ralph-loop \
  --interpreter python3 --cron "*/30 * * * *"

# Or continuous monitoring
pm2 start "python3 tools/ralph_loop_runner.py --process-needs-action --max-iterations 20" \
  --name ralph-loop --max-memory-restart 500M
```

---

**Status:** ✅ Production Ready
**Last Updated:** 2026-03-29
**Version:** Gold Tier v1.0
