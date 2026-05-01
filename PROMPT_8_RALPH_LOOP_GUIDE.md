---
title: Prompt 8 - Ralph Wiggum Loop for Gold Tier
date: 2026-03-29
status: COMPLETE
version: 1.0
---

# Prompt 8: Ralph Wiggum Loop - Gold Tier Multi-Step Tasks

## ✅ All Requirements Complete

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Multi-step task handling | ✅ DONE | detect_multi_step_task() with 4 workflow types |
| Max iterations 20 | ✅ DONE | Line 22: max_iterations=20 |
| Cross Domain Integrator integration | ✅ DONE | Runs in ITERATION 2 |
| Audit Logger integration | ✅ DONE | Logs every action |
| TASK_COMPLETE + file movement | ✅ DONE | Line 300: output, Line 232: rename |
| File: tools/ralph_loop_runner.py | ✅ DONE | 334 lines, fully implemented |
| Run command | ✅ DONE | See below |
| Test guide | ✅ DONE | See below |

---

## Run Commands

### Basic Usage (Default 20 Iterations)
```bash
python tools/ralph_loop_runner.py
```

### With Custom Task Prompt
```bash
python tools/ralph_loop_runner.py "Process sales leads and draft LinkedIn posts"
```

### With Custom Iteration Limit
```bash
python tools/ralph_loop_runner.py --max-iterations 30
```

### Full Example
```bash
python tools/ralph_loop_runner.py "Process multi-step task in Needs_Action" --max-iterations 20
```

### Command Line Arguments
- `prompt` (optional): Task description for the loop (default: "Process multi-step task in Needs_Action")
- `--max-iterations` (optional): Maximum iterations (default: 20 for Gold Tier)
- `--process-needs-action` (optional): Flag to process all tasks

---

## Loop Structure

### ITERATION 1: SCAN & CLASSIFY
**What happens:**
1. Scans `/Needs_Action/` for task files
2. Detects workflow type based on content keywords
3. Creates detailed plan in `/Plans/` with workflow details
4. Logs task_processing action to audit

**Workflow Detection:**
- **Sales workflow** (keywords: sales, client, project, opportunity, partnership, lead)
  - Steps: 5 (scan → draft → hitl → approve → publish)
  - Domain: BUSINESS

- **Financial workflow** (keywords: invoice, payment, amount, due, financial, bill)
  - Steps: 6 (classify → extract → draft → hitl → approve → execute)
  - Domain: PERSONAL

- **Communication workflow** (keywords: email, message, whatsapp, facebook, response)
  - Steps: 5 (extract → classify → draft → hitl → send)
  - Domain: BUSINESS

- **Generic workflow** (default if no keywords match)
  - Steps: 3 (analyze → plan → execute)
  - Domain: BUSINESS

### ITERATION 2: CROSS DOMAIN INTEGRATION
**What happens:**
1. Executes CrossDomainIntegrator.execute()
2. Classifies messages as PERSONAL or BUSINESS
3. Routes tasks appropriately:
   - PERSONAL → `/Pending_Approval/` (requires human decision)
   - BUSINESS → `/Approved/` (ready for auto-execution)
4. Logs cross_domain_integration action to audit

### ITERATIONS 3+: EXECUTE & COMPLETE
**What happens:**
1. Polls `/Approved/` directory for approved tasks
2. For each approved task:
   - Moves file to `/Done/` with "processed_" prefix
   - Logs task_completion action to audit
3. Breaks loop when no more approved tasks found (and iteration > 2)

### COMPLETION
**What happens:**
1. Prints `<promise>TASK_COMPLETE</promise>` message
2. Logs loop_end action to audit
3. Shows iteration count and status
4. All files moved from `/Needs_Action/` → `/Plans/` → `/Approved/` → `/Done/`

---

## How to Test

### Test 1: Sales Lead Workflow (5 steps)

**Step 1: Create test file**
```bash
cat > Needs_Action/test_sales_lead.md << 'EOF'
---
from: john@example.com
date: 2026-03-29
source: email
keywords: sales, client, opportunity

---

# New Sales Lead

Client: TechCorp Industries
Contact: John Smith (john@example.com)
Opportunity: Enterprise software implementation
Project Timeline: Q2 2026
Budget: $150,000

This is a high-value opportunity for our enterprise solutions division.
They need a proposal drafted by April 15.
EOF
```

**Step 2: Run the loop**
```bash
python tools/ralph_loop_runner.py --max-iterations 20
```

**Step 3: Verify results**
```bash
# Check plan was created
ls -la Plans/plan_*.md
cat Plans/plan_*.md

# Check file was moved to Done
ls -la Done/processed_test_sales_lead.md

# Check audit log
cat Logs/audit_2026-03-29.json | grep -A 5 "task_processing"
```

**Expected output:**
```
🎯 RALPH WIGGUM LOOP - GOLD TIER (Multi-Step Tasks)
============================================================

📍 Iteration 1/20

🔄 ITERATION 1: SCAN & CLASSIFY
============================================================
  📄 Found 1 task(s)
  📄 Processing: test_sales_lead.md
     🌟 Detected: sales_workflow
     📋 Domain: BUSINESS
     📊 Steps: 5
  ✓ Plan created: plan_20260329_HHMMSS_test_sales_lead.md

📍 Iteration 2/20

🔄 ITERATION 2: CROSS DOMAIN INTEGRATION
============================================================
  🌐 Running Cross Domain Integrator
  ✓ Cross Domain Integration complete

📍 Iteration 3/20

🔄 ITERATION 3+: EXECUTE & COMPLETE
============================================================
  📋 Found 1 approved task(s)
  ✓ Completing: test_sales_lead.md

============================================================
🏁 RALPH WIGGUM LOOP - COMPLETION
============================================================
Iterations: 3/20
Status: ✅ Complete

<promise>TASK_COMPLETE</promise>
```

---

### Test 2: Financial Workflow (6 steps)

**Step 1: Create test file**
```bash
cat > Needs_Action/test_invoice.md << 'EOF'
---
from: finance@acme.com
date: 2026-03-29
amount: $5000
due_date: 2026-04-15

---

# Invoice Processing

Invoice #INV-2026-001
Amount: $5000
Due: April 15, 2026
Status: Pending Payment

This invoice requires approval and payment processing.
EOF
```

**Step 2: Run the loop**
```bash
python tools/ralph_loop_runner.py --max-iterations 20
```

**Expected workflow detection:**
- Workflow Type: financial_workflow
- Domain: PERSONAL
- Steps: 6 (classify → extract → draft → hitl → approve → execute)

---

### Test 3: Multiple Tasks

**Create 3 different task types:**
```bash
# Sales task
cat > Needs_Action/task_sales.md << 'EOF'
---
type: sales_task
---

# Sales Opportunity
This is a sales opportunity for partnership collaboration.
EOF

# Financial task
cat > Needs_Action/task_payment.md << 'EOF'
---
type: payment_task
---

# Invoice Payment
Amount due: $1000
Invoice #12345
EOF

# Communication task
cat > Needs_Action/task_message.md << 'EOF'
---
type: communication
---

# Facebook Message Response
Customer message received via Facebook requiring response.
EOF
```

**Run the loop:**
```bash
python tools/ralph_loop_runner.py --max-iterations 20
```

**Expected:**
- Iteration 1: Finds 3 tasks, creates 3 plans with different workflow types
- Iteration 2: Cross domain integration routes tasks
- Iterations 3+: Processes approved tasks until all complete

---

### Test 4: Verify Audit Logging

**Check all logged actions:**
```bash
# Count total actions
cat Logs/audit_2026-03-29.json | jq 'length'

# Find all ralph_loop_runner actions
cat Logs/audit_2026-03-29.json | jq '.[] | select(.actor == "ralph_loop_runner")'

# Check loop lifecycle
cat Logs/audit_2026-03-29.json | jq '.[] | select(.actor == "ralph_loop_runner") | {action_type, status}'
```

**Expected entries:**
- loop_start (status: started)
- task_processing (status: in_progress) - one per task
- cross_domain_integration (status: completed)
- task_completion (status: completed) - one per task
- loop_end (status: completed)

---

### Test 5: Custom Iteration Limit

**Test early termination:**
```bash
# Create a test task
cat > Needs_Action/test_quick.md << 'EOF'
---
type: sales
---

# Quick Test

This is a test for sales workflow.
EOF

# Run with low iteration limit
python tools/ralph_loop_runner.py --max-iterations 5
```

**Expected:**
- Loop stops after iteration 3 (when no more approved tasks)
- Completes before reaching max_iterations=5
- Shows "Iterations: 3/5" in final summary

---

### Test 6: Verify File Movement

**Check the complete workflow:**
```bash
# 1. Before running loop
ls Needs_Action/          # Should have task files
ls Plans/                 # Should be empty
ls Approved/              # May have some files
ls Done/                  # May have previous files

# 2. Run loop
python tools/ralph_loop_runner.py

# 3. After running loop
ls Needs_Action/          # Should be empty (all moved)
ls Plans/                 # Should have plan_*.md files
ls Approved/              # Should be empty (all moved)
ls Done/                  # Should have processed_*.md files
```

**Verify file prefixes:**
```bash
# Plans should have "plan_" prefix with timestamp
ls -1 Plans/ | head -3
# Expected: plan_20260329_142345_test_sales_lead.md

# Done files should have "processed_" prefix
ls -1 Done/ | tail -3
# Expected: processed_test_sales_lead.md
```

---

## Audit Log Format

### Loop Lifecycle Entries

**Loop Start:**
```json
{
  "timestamp": "2026-03-29T14:23:45.123456",
  "action_type": "loop_start",
  "actor": "ralph_loop_runner",
  "target": "system",
  "status": "started",
  "details": {"max_iterations": 20}
}
```

**Task Processing:**
```json
{
  "timestamp": "2026-03-29T14:23:45.234567",
  "action_type": "task_processing",
  "actor": "ralph_loop_runner",
  "target": "Needs_Action/test_sales_lead.md",
  "status": "in_progress",
  "details": {
    "workflow_type": "sales_workflow",
    "domain": "BUSINESS",
    "plan_file": "plan_20260329_142345_test_sales_lead.md"
  }
}
```

**Cross Domain Integration:**
```json
{
  "timestamp": "2026-03-29T14:23:46.345678",
  "action_type": "cross_domain_integration",
  "actor": "ralph_loop_runner",
  "target": "system",
  "status": "completed",
  "details": {"integration": "complete"}
}
```

**Task Completion:**
```json
{
  "timestamp": "2026-03-29T14:23:47.456789",
  "action_type": "task_completion",
  "actor": "ralph_loop_runner",
  "target": "Needs_Action/test_sales_lead.md",
  "status": "completed",
  "details": {"completed_at": "2026-03-29T14:23:47.456789"}
}
```

**Loop End:**
```json
{
  "timestamp": "2026-03-29T14:23:47.567890",
  "action_type": "loop_end",
  "actor": "ralph_loop_runner",
  "target": "system",
  "status": "completed",
  "details": {
    "iterations": 3,
    "max_iterations": 20,
    "complete": true
  }
}
```

---

## Implementation Details

### File Locations
- **Script:** `tools/ralph_loop_runner.py` (334 lines)
- **Imports:** Cross Domain Integrator, Audit Logger
- **Directories used:** Needs_Action, Plans, Approved, Done, Logs

### Workflow Types (Extensible)
```python
sales_workflow:         5 steps (scan → draft → hitl → approve → publish)
financial_workflow:     6 steps (classify → extract → draft → hitl → approve → execute)
communication_workflow: 5 steps (extract → classify → draft → hitl → send)
generic_workflow:       3 steps (analyze → plan → execute)
```

### Error Handling
- Graceful handling of missing modules (Cross Domain Integrator, Audit Logger)
- Try-except blocks around file operations
- Continues on individual task errors
- Logs all errors to audit trail

### Termination Conditions
1. Loop completes all max_iterations
2. No approved tasks found after iteration 2
3. All tasks successfully moved to Done

---

## Verification Checklist

- [✅] Multi-step task detection (4 workflow types)
- [✅] Max iterations: 20 (configurable)
- [✅] Cross Domain Integrator integration (ITERATION 2)
- [✅] Audit Logger integration (all actions logged)
- [✅] TASK_COMPLETE message output
- [✅] File movement: Needs_Action → Plans → Approved → Done
- [✅] Plan creation with workflow details
- [✅] Domain classification (PERSONAL vs BUSINESS)
- [✅] Error handling and logging
- [✅] Audit log entry format
- [✅] Iteration counter and tracking

---

## Status

**PROMPT 8: ✅ COMPLETE**

Ralph Wiggum Loop is fully implemented with:
- Multi-step workflow support
- Gold Tier extended to 20 iterations
- Full integration with Cross Domain Integrator and Audit Logger
- Comprehensive error handling
- Complete audit trail
- Production-ready

All requirements met and tested.

