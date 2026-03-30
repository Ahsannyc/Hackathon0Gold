---
name: Ralph Wiggum Loop - Gold Tier Multi-Step Task Runner
description: Complete guide for using the enhanced Ralph Loop with multi-step workflow support
type: reference
---

# Ralph Wiggum Loop - Gold Tier Multi-Step Task Runner

**Updated:** 2026-03-29
**Status:** Production Ready ✅

---

## Quick Start Commands

### Command 1: Run Multi-Step Task Processing (Full Loop)
```bash
python3 tools/ralph_loop_runner.py "Process multi-step task in Needs_Action" --max-iterations 20
```

### Command 2: Run Convenience Mode (Auto-detects all tasks)
```bash
python3 tools/ralph_loop_runner.py --process-needs-action --max-iterations 20
```

### Command 3: Wrapper Script (if configured)
```bash
./ralph:loop "Process multi-step task in Needs_Action" --max-iterations 20
```

---

## What's New in Gold Tier

### 1. Extended Iteration Limit
- **Silver Tier:** Max 10 iterations
- **Gold Tier:** Max 20 iterations (supports complex multi-step workflows)

### 2. Multi-Step Workflow Detection
The loop automatically detects and handles:
- **Sales Workflows** (5 steps): scan → draft → HITL → approve → publish
- **Financial Workflows** (6 steps): classify → extract → draft → HITL → approve → execute
- **Communication Workflows** (5 steps): extract → classify → draft → HITL → send
- **Simple Tasks** (3 steps): analyze → plan → execute

### 3. Cross Domain Integration
Automatically classifies tasks as:
- **BUSINESS** (Auto LinkedIn Poster, Twitter, etc.)
- **PERSONAL** (Requires HITL approval)

### 4. Full Audit Trail
Every step logged to `/Logs/audit_{date}.json`:
- Loop start/end
- Task processing
- Cross Domain Integration execution
- Errors and recovery
- Completion tracking

### 5. Intelligent File Movement
Tracks files through workflow:
- `/Needs_Action` → `/Plans` (draft created)
- → `/Pending_Approval` (awaiting human decision)
- → `/Approved` (human approved)
- → `/Done` (completed + logged)

---

## Testing: Create Multi-Step Files

### Test 1: Sales Lead (Business Workflow)
Create `/Needs_Action/sales_lead_demo.md`:

```markdown
---
type: task
from: John@acme.com
subject: Interested in our services
priority: high
source: email
---

Hi,

We've been following your company and are very interested in exploring a partnership.
We specifically need help with:
- Sales enablement solutions
- Client relationship management
- Project management expertise

Can we schedule a call to discuss this opportunity?

Thanks,
John Smith
ACME Corporation
```

**Expected Workflow:**
1. Loop detects: "sales" + "client" + "project" → BUSINESS domain
2. Creates: `Plans/plan_*.md` with multi-step workflow
3. Auto LinkedIn Poster: Creates draft post
4. Moves to: `/Pending_Approval/linkedin_post_*.md`
5. Human approves → moves to `/Approved/`
6. Publishes to LinkedIn (manual)
7. Complete: Files moved to `/Done/`

---

### Test 2: Payment Request (Personal/HITL Workflow)
Create `/Needs_Action/invoice_demo.md`:

```markdown
---
type: task
from: accounting@supplier.com
subject: Invoice for Q1 Services
priority: high
source: email
---

Dear Customer,

Please find attached invoice #INV-2026-0125 for Q1 2026 services.

**Amount Due:** $5,000
**Due Date:** April 15, 2026
**Payment Terms:** Net 30

Services rendered:
- Consultation (10 hours @ $200/hr)
- Implementation (20 hours @ $150/hr)
- Support (10 hours @ $100/hr)

Please remit payment to the details on the invoice.

Thanks,
Finance Team
```

**Expected Workflow:**
1. Loop detects: "invoice" + "payment" + "amount" → PERSONAL domain
2. Creates: `Plans/plan_*.md` with HITL checkpoints
3. Moves to: `/Pending_Approval/` (awaiting human approval)
4. Human reviews and approves
5. MCP processes payment (manual step)
6. Complete: Files moved to `/Done/` with full audit trail

---

### Test 3: Social Media Message (Communication Workflow)
Create `/Needs_Action/facebook_message_demo.md`:

```markdown
---
type: task
from: alice@contact.com
subject: Facebook Message - Client Inquiry
source: facebook
priority: medium
---

Hi there,

We saw your recent post about project management solutions.
We're currently working on a complex multi-team project and
could really use some expert guidance.

Are you available for a quick consultation call next week?

Thanks,
Alice
Client Success Team
```

**Expected Workflow:**
1. Loop detects: "project" + "client" + "project management" → BUSINESS domain
2. Creates: `Plans/plan_*.md` with social media response template
3. Social Summary Generator: Creates draft response
4. Moves to: `/Pending_Approval/` for human review
5. Human approves → `/Approved/`
6. Sends response (manual)
7. Complete: Files moved to `/Done/`

---

## Full Testing Workflow

### Step 1: Prepare Test Files
```bash
# Create test directory with sample multi-step tasks
cat > Needs_Action/test_sales_lead.md << 'EOF'
---
from: prospect@company.com
subject: Sales inquiry for enterprise solution
priority: high
source: email
---

Hi, interested in your enterprise solutions for managing complex projects.
Looking to discuss implementation timeline and pricing.

Thanks,
John Doe
EOF

cat > Needs_Action/test_payment.md << 'EOF'
---
from: accounting@vendor.com
subject: Invoice #INV-2026-001 - $2,500
priority: high
source: email
---

Invoice payment due for Q1 services totaling $2,500.
Payment methods accepted: Wire transfer, ACH, credit card.

Please process by end of month.
EOF
```

### Step 2: Run Ralph Loop with Gold Tier Enhancements
```bash
# Option A: Process all files with full multi-step support
python3 tools/ralph_loop_runner.py --process-needs-action --max-iterations 20

# Option B: Custom prompt
python3 tools/ralph_loop_runner.py "Process multi-step task in Needs_Action" --max-iterations 20
```

### Step 3: Monitor Execution
The loop will display:
```
🎯 RALPH WIGGUM LOOP - GOLD TIER (Multi-Step Tasks)
================================================

🔄 ITERATION 1/20
----
📄 Processing: test_sales_lead.md
   🌟 Multi-step task detected: sales_workflow
   📋 Workflow: scan → draft → hitl → approve → publish

✓ Plan created: plan_20260329_120000_abc123_test_sales_lead.md
   Review plan in: Plans/plan_20260329_120000_abc123_test_sales_lead.md

🌐 GOLD TIER: Cross Domain Integration
OK: Summary created: /Logs/cross_domain_2026-03-29.md
OK: Routed 1 personal items to /Pending_Approval
OK: Routed 1 business items to /Approved

⏳ Iteration 1 complete - 1 task(s) remaining
   1 multi-step task(s) in progress
```

### Step 4: Verify Files Moved Through Workflow

```bash
# Check Plans folder for created plans
ls -la Plans/plan_*

# Check Pending Approval for drafts awaiting human review
ls -la Pending_Approval/

# Check logs for audit trail
tail -50 Logs/audit_2026-03-29.json

# Check cross domain summary
cat Logs/cross_domain_2026-03-29.md

# When complete, verify Done folder
ls -la Done/
```

### Step 5: Expected Output

**Loop Completion:**
```
🏁 RALPH WIGGUM LOOP - COMPLETION SUMMARY
===========================================
Iterations completed: 2/20
Tasks processed: 2
Multi-step tasks: 2
Task complete: True
State file: tools/state/loop_state_20260329_120000.json

✅ SUCCESS: All tasks completed!

<promise>TASK_COMPLETE</promise>
```

**Audit Trail Entry:**
```json
{
  "timestamp": "2026-03-29T01:24:15.123456",
  "action_type": "loop_end",
  "actor": "ralph_loop_runner",
  "target": "system",
  "status": "completed",
  "details": {
    "iterations": 2,
    "tasks_processed": 2,
    "multi_step_tasks": 2,
    "complete": true
  }
}
```

---

## File Movement Tracking

### Sales Lead Workflow (BUSINESS Domain)
```
/Needs_Action/sales_lead_demo.md
    ↓ (Loop: Create Plan)
/Plans/plan_20260329_*.md
    ↓ (Cross Domain Integrator: Business domain detected)
/Plans/linkedin_post_*.md (created by Auto LinkedIn Poster)
    ↓ (Move to HITL)
/Pending_Approval/linkedin_post_*.md
    ↓ (Human approves)
/Approved/linkedin_post_*.md
    ↓ (Publish + Log to audit)
/Done/processed_sales_lead_*.md
```

### Payment Request Workflow (PERSONAL Domain)
```
/Needs_Action/invoice_demo.md
    ↓ (Loop: Create Plan)
/Plans/plan_20260329_*.md
    ↓ (Cross Domain Integrator: Personal domain detected)
/Pending_Approval/plan_20260329_*.md
    ↓ (Human approves payment)
/Approved/plan_20260329_*.md
    ↓ (Process + Log to audit)
/Done/processed_invoice_*.md
```

---

## Audit Log Tracking

### Loop Start
```json
{
  "timestamp": "2026-03-29T01:23:00.000000",
  "action_type": "loop_start",
  "actor": "ralph_loop_runner",
  "target": "system",
  "status": "started",
  "details": {
    "max_iterations": 20,
    "prompt": "Process multi-step task in Needs_Action"
  }
}
```

### Task Processing
```json
{
  "timestamp": "2026-03-29T01:23:15.000000",
  "action_type": "task_processing",
  "actor": "ralph_loop_runner",
  "target": "Needs_Action/sales_lead_demo.md",
  "status": "in_progress",
  "details": {
    "workflow_type": "sales_workflow",
    "plan_file": "plan_20260329_120000_abc123.md",
    "iteration": 1
  }
}
```

### Cross Domain Integration
```json
{
  "timestamp": "2026-03-29T01:23:20.000000",
  "action_type": "cross_domain_integration",
  "actor": "ralph_loop_runner",
  "target": "system",
  "status": "completed",
  "details": {
    "items_processed": 2,
    "personal_routed": 1,
    "business_routed": 1
  }
}
```

### Loop Completion
```json
{
  "timestamp": "2026-03-29T01:24:15.000000",
  "action_type": "loop_end",
  "actor": "ralph_loop_runner",
  "target": "system",
  "status": "completed",
  "details": {
    "iterations": 2,
    "tasks_processed": 2,
    "multi_step_tasks": 2,
    "complete": true
  }
}
```

---

## Troubleshooting

### Issue: Tasks not moving to Done
**Solution:** Check `/Logs/audit_*.json` for errors. Ensure HITL approval workflow is followed:
1. Plan created in `/Plans/`
2. Human moves to `/Pending_Approval/` or approves
3. Task executor moves to `/Approved/`
4. Loop moves to `/Done/` on next iteration

### Issue: Loop hits max iterations
**Solution:** Check `/Plans/` for plans awaiting approval. Manually approve tasks or increase max-iterations:
```bash
python3 tools/ralph_loop_runner.py --process-needs-action --max-iterations 30
```

### Issue: Cross Domain Integrator not running
**Solution:** Ensure `/Needs_Action/` files have proper YAML frontmatter with keywords:
- Sales: "sales", "client", "project"
- Payment: "invoice", "payment", "financial"
- Communication: "email", "message", "whatsapp"

### Issue: Audit logs not created
**Solution:** Verify AuditLogger is importing correctly:
```bash
python -c "from skills.audit_logger import AuditLogger; a = AuditLogger(); print('✓ OK')"
```

---

## Integration with Gold Tier Skills

The Ralph Loop automatically orchestrates:

| Skill | When | Purpose |
|-------|------|---------|
| Task Analyzer | Iteration start | Analyze task type and create plan |
| Cross Domain Integrator | Each iteration | Classify task domain (PERSONAL/BUSINESS) |
| Auto LinkedIn Poster | Business domain | Draft posts from sales leads |
| Social Summary Generator | Business domain | Draft social media responses |
| HITL Approval Handler | After draft | Process human approvals |
| Audit Logger | Every step | Track full workflow in audit trail |
| Weekly Audit Briefer | Daily briefing | Summarizes loop activity |

---

## Performance Metrics

Expected execution times:

| Task Type | Time | Steps |
|-----------|------|-------|
| Sales lead | 5-10 sec | 5 (scan → draft → HITL → approve → publish) |
| Payment | 3-5 sec | 6 (classify → extract → draft → HITL → approve → execute) |
| Communication | 4-7 sec | 5 (extract → classify → draft → HITL → send) |
| Loop iteration | 10-20 sec | 3 (scan → process → integrate) |
| Full workflow | 20-60 sec | 20 max iterations |

---

## Next Steps

1. **Test with sample files** (see Testing section above)
2. **Monitor audit logs** to verify integration
3. **Deploy to PM2** for continuous processing:
   ```bash
   pm2 start tools/ralph_loop_runner.py --name ralph-loop --interpreter python3 --cron "*/30 * * * *"
   ```
4. **Create wrapper script** `./ralph:loop` for easy invocation
5. **Update CI/CD** to run loop on new messages in /Needs_Action

---

## Summary

✅ **Ralph Wiggum Loop - Gold Tier:**
- Extended to 20 iterations (complex multi-step workflows)
- Auto-detects workflow types
- Integrates Cross Domain Integrator for domain classification
- Full audit logging with AuditLogger
- Handles BUSINESS (auto-process) and PERSONAL (HITL) domains
- Complete file movement tracking
- Production-ready for autonomous multi-step task completion
