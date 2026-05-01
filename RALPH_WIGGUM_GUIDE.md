# Ralph Wiggum Loop: Complete Implementation Guide
**Version:** 1.0  
**Status:** Ready for Testing  
**Last Updated:** 2026-04-30

---

## 🎯 What is Ralph Wiggum Loop?

The **Ralph Wiggum Loop** is a pattern that enables Claude to work **autonomously on multi-step tasks** without requiring human input between each step.

### The Problem It Solves

**Without Ralph Wiggum:**
```
1. Human: "Process invoices"
2. Claude: "I need approval files to exist first" → Exit
3. Human must run Claude again
4. Claude: "Invoices created, need email approval" → Exit
5. Human must run Claude AGAIN
6. Claude: "Task complete" ✓

Result: Human must invoke Claude 3+ times for 1 task
```

**With Ralph Wiggum:**
```
1. Human: "Process all invoices (Ralph loop)"
2. Claude: Read task, make progress
3. Auto loop: Check completion → Not done → Continue
4. Claude: Continue from where it left off
5. Auto loop: Check completion → Done! ✓

Result: Single invocation, Claude completes entire workflow
```

---

## 🚀 Quick Start (5 minutes)

### Step 1: Verify Installation

```bash
# Check Ralph executor exists
ls -la tools/ralph_wiggum_executor.py

# Verify skill exists
ls -la skills/ralph_wiggum_skill.md
```

### Step 2: Create Test Task

Create `/Plans/TEST_basic_workflow.md`:

```markdown
---
task_id: test_basic_001
status: in_progress
created: 2026-04-30T10:00:00Z
---

# Test Task: Process 3 Files

## Objective
Move 3 test files from /Needs_Action to /Done to verify Ralph loop works.

## Steps
1. List files in /Needs_Action
2. Read each file
3. Update this task file with progress
4. Create processed version
5. When all 3 done → Move this task to /Done

## Progress
- [ ] File 1
- [ ] File 2  
- [ ] File 3

## Status
Starting...
```

### Step 3: Create Test Data Files

```bash
# Create test files in /Needs_Action
echo "Test file 1" > Needs_Action/test_file_1.md
echo "Test file 2" > Needs_Action/test_file_2.md
echo "Test file 3" > Needs_Action/test_file_3.md
```

### Step 4: Run Ralph Loop

```bash
# Start the loop
python tools/ralph_wiggum_executor.py \
  "test_basic_001" \
  "Process the 3 test files: read each one, update progress, move task to /Done when done" \
  --max-iterations 5
```

### Step 5: Verify Results

```bash
# Check if task moved to Done
ls -la Done/ | grep TEST_basic

# Check state
cat .ralph-state/test_basic_001.json | jq .

# Check logs
tail -20 Logs/ralph_wiggum.log
```

---

## 📊 Architecture Details

### State Machine

```
         ┌─────────┐
         │ Pending │
         └────┬────┘
              │
              ▼
        ┌──────────┐
    ┌──►│ Running  │
    │   │Iter 1..N │
    │   └────┬─────┘
    │        │
    │   ┌────▼─────────┐
    │   │ Completion   │
    │   │ Check?       │
    │   └────┬────┬────┘
    │        │    │
    │    Yes │    │ No
    │        │    │
    │        │    └──────┬─► Sleep 2s ──┐
    │        │           │               │
    │        ▼           └───────────────┘
    │   ┌──────────┐
    └───┤ Complete │
        └──────────┘

Completion can be triggered by:
  - File moved to /Done/ (primary method)
  - <promise>TASK_COMPLETE</promise> in output (secondary)
  - Max iterations reached (timeout)
```

### Iteration Flow

```
Each Iteration:

1. CREATE/READ
   └─ Task file exists in /Plans/

2. EXECUTE
   └─ Claude processes task
   └─ Claude updates /Plans/ file
   └─ Claude creates/modifies files

3. CHECK COMPLETION
   └─ Is task file in /Done/? YES → Complete
   └─ Is promise in output? YES → Complete
   └─ Iteration < max? YES → Loop back

4. LOOP/EXIT
   └─ If incomplete: Sleep 2s, continue
   └─ If complete: Return success
   └─ If max iterations: Return timeout
```

### File Locations

```
Hackathon0Gold/
├── Plans/
│   └── TASK_<id>.md          ← Task definition (Claude reads/updates)
├── Done/
│   └── TASK_<id>.md          ← Completion signal (file moved here)
├── Logs/
│   └── ralph_wiggum.log      ← Execution trace
│   └── audit_tasks.json      ← Completion audit
└── .ralph-state/
    └── <id>.json             ← State tracking between iterations
```

---

## 🧪 Test Scenarios

### Test 1: Basic Task Completion

**File:** `Plans/TASK_test_basic_001.md`

```markdown
---
task_id: test_basic_001
---

# Test: Move Task to Done

When this task is ready, move it to /Done/TASK_test_basic_001.md
```

**Command:**
```bash
python tools/ralph_wiggum_executor.py \
  "test_basic_001" \
  "Read /Plans/TASK_test_basic_001.md, process it, then move it to /Done/"
```

**Expected Result:**
```
Status: completed
Iterations: 1
Completion Type: file_move
```

---

### Test 2: Multi-Step Processing

**File:** `Plans/TASK_test_multistep_001.md`

```markdown
---
task_id: test_multistep_001
progress: 0
---

# Test: 5-Step Task

1. [ ] Check prerequisites
2. [ ] Create output file
3. [ ] Update this progress
4. [ ] Verify output
5. [ ] Move to /Done

Current step: 1
```

**Command:**
```bash
python tools/ralph_wiggum_executor.py \
  "test_multistep_001" \
  "Complete all 5 steps in order. Update progress after each step. Move task to /Done when all complete."
```

**Expected Result:**
```
Status: completed
Iterations: 5-7 (one per step, plus verification)
Completion Type: file_move
```

---

### Test 3: Error Handling

**File:** `Plans/TASK_test_errors_001.md`

```markdown
---
task_id: test_errors_001
---

# Test: Handle Missing Files

Read files:
- [ ] /Needs_Action/exists.md (will succeed)
- [ ] /Needs_Action/missing.md (will fail)
- [ ] Handle error gracefully
- [ ] Move to /Done regardless

This tests error recovery.
```

**Command:**
```bash
python tools/ralph_wiggum_executor.py \
  "test_errors_001" \
  "Try to read both files. Handle missing file error gracefully. Log what happened. Move to /Done."
```

**Expected Result:**
```
Status: completed
Iterations: 2-3 (one for reading, one for error handling)
Error logged but handled gracefully
```

---

### Test 4: Iteration Limit

**File:** `Plans/TASK_test_timeout_001.md`

```markdown
---
task_id: test_timeout_001
---

# Test: Max Iterations

This task will never complete.
(Used to test max_iterations limit)
```

**Command:**
```bash
python tools/ralph_wiggum_executor.py \
  "test_timeout_001" \
  "Try to complete this task forever" \
  --max-iterations 3
```

**Expected Result:**
```
Status: incomplete
Iterations: 3
Error: Max iterations (3) reached
```

---

## 🔧 Integration Points

### With Schedulers

Add to your cron/Task Scheduler for recurring autonomous tasks:

```bash
# Run morning invoice processing loop
0 6 * * * python tools/ralph_wiggum_executor.py invoice_daily_001 "Process daily invoices"

# Run weekly social media posting loop
0 8 * * 1 python tools/ralph_wiggum_executor.py social_weekly_001 "Post weekly content"

# Run nightly cleanup loop
0 22 * * * python tools/ralph_wiggum_executor.py cleanup_daily_001 "Archive old files"
```

### With MCP Servers

Ralph Wiggum tasks can use all MCP servers:

```markdown
# Task: Send Invoices via Email

Process /Needs_Action/invoices:
1. Read invoice details
2. Create in Odoo via Odoo MCP
3. Get customer email
4. Send via Email MCP
5. Move to /Done when all sent
```

### With Watchers

Watchers create files → Ralph loop processes them:

```
Gmail Watcher (every 120s)
  └─ Creates: /Needs_Action/EMAIL_*.md

Ralph Loop (scheduled 6AM, 12PM, 6PM)
  └─ Processes all /Needs_Action files
  └─ Moves to /Done when done
  └─ Watchers continue monitoring
```

---

## 📈 Monitoring & Debugging

### View Execution Log

```bash
# Real-time tail
tail -f Logs/ralph_wiggum.log

# Last 50 lines
tail -50 Logs/ralph_wiggum.log

# Search for specific task
grep "test_basic_001" Logs/ralph_wiggum.log
```

### Check Task State

```bash
# View JSON state
cat .ralph-state/test_basic_001.json | jq .

# Pretty print
cat .ralph-state/test_basic_001.json | python -m json.tool

# Check iterations
cat .ralph-state/test_basic_001.json | jq '.iterations_log | length'
```

### View Audit Trail

```bash
# All task completions
cat Logs/audit_tasks.json | jq .

# Last 5 completions
cat Logs/audit_tasks.json | jq '.[-5:]'

# Completions by date
cat Logs/audit_tasks.json | jq 'group_by(.timestamp | split("T")[0])'
```

---

## ⚠️ Troubleshooting

### Issue: "Task not completing"

**Diagnosis:**
1. Check task file exists in /Plans/
2. Check logs for errors
3. Verify completion signal (file move or promise)

**Solution:**
```bash
# Check if task file exists
ls -la Plans/TASK_*

# Check logs for errors
grep ERROR Logs/ralph_wiggum.log

# Manually check /Done for the task
ls -la Done/ | grep TASK_
```

### Issue: "Hits max_iterations immediately"

**Diagnosis:**
- Task defined poorly
- Completion condition never met
- File movement not happening

**Solution:**
```bash
# Check task file state
cat Plans/TASK_*.md

# Check if file should be in /Done
ls -la Done/

# Debug: Run with lower max_iterations
python tools/ralph_wiggum_executor.py <id> "<prompt>" --max-iterations 2
```

### Issue: "Claude not updating task file"

**Diagnosis:**
- Claude prompt doesn't mention task file
- File permissions issue
- Claude not writing to vault

**Solution:**
```bash
# Verify task file writable
touch Plans/TASK_test.md && echo "test" >> Plans/TASK_test.md

# Check Claude prompt mentions file updates
# Prompt should say: "Update /Plans/TASK_*.md with progress"

# Verify vault permissions
ls -la Plans/
```

---

## 🎓 Advanced Patterns

### Pattern 1: Workflow with Approval

```markdown
# Task: Invoice Creation with Approval

1. Read /Needs_Action invoices
2. Create in Odoo (draft status)
3. Create /Pending_Approval/INVOICE_*.md
4. Wait for human approval
5. On approval, post invoice
6. Move task to /Done

Completion: File in /Done
```

### Pattern 2: Data Transformation Pipeline

```markdown
# Task: Transform CSV to Records

1. Read input CSV from /Data/input.csv
2. Parse each row
3. Validate data
4. Transform to Markdown
5. Create output files in /Accounting/
6. Generate summary report
7. Move task to /Done

Completion: File in /Done with summary
```

### Pattern 3: Scheduled Recurring Task

```markdown
# Task: Daily Report Generation

1. Check if report exists for today
2. If not, collect data
3. Generate report to /Logs/
4. Move task to /Done

Completion: Today's report generated

Scheduled: Daily at 7 AM
```

---

## ✅ Verification Checklist

Before going live with Ralph Wiggum, verify:

- [ ] Task files created in `/Plans/` successfully
- [ ] Ralph executor handles errors gracefully
- [ ] State files created in `/.ralph-state/`
- [ ] Logs written to `/Logs/ralph_wiggum.log`
- [ ] Audit trail in `/Logs/audit_tasks.json`
- [ ] File movement completes tasks reliably
- [ ] Max iterations limits respected
- [ ] State persists between iterations
- [ ] Integration with MCP servers works
- [ ] Integration with schedulers works
- [ ] Monitoring and debugging tools available

---

## 📚 Related Documentation

- `skills/ralph_wiggum_skill.md` - Agent Skill definition
- `tools/ralph_wiggum_executor.py` - Source code
- `GOLD_TIER_IMPLEMENTATION_PLAN.md` - How Ralph Wiggum fits into Gold Tier
- `Dashboard.md` - Monitor execution via Dashboard updates

---

## 🚀 Next Steps

1. **Run Test 1 (Basic):** Verify executor works
2. **Run Test 2 (Multi-step):** Test iteration loop
3. **Run Test 3 (Errors):** Test error handling
4. **Review Logs:** Understand execution flow
5. **Create Real Task:** First invoice processing loop
6. **Schedule Recurring:** Add to cron/Task Scheduler
7. **Monitor & Iterate:** Adjust based on real usage

---

**Status:** ✅ Ready to test  
**Confidence Level:** High  
**Next Phase:** Phase 1.2 (Audit Logging)
