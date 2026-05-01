# Ralph Wiggum Loop Skill
**Name:** ralph-wiggum  
**Type:** Agent Skill  
**Purpose:** Enable Claude to work autonomously on multi-step tasks until completion

---

## Description

The Ralph Wiggum Loop Skill allows Claude to execute autonomous, self-iterating tasks. When invoked, Claude will:

1. **Read** the task state
2. **Think** about what needs to be done next
3. **Act** by creating/updating files or making API calls
4. **Signal** completion via file movement or promise
5. **Loop back** until the task is complete

Without this skill, Claude must wait for human input between each step. With this skill, Claude can complete entire workflows autonomously.

---

## How It Works

### Basic Flow

```
┌─────────────────────────────────────────────────────┐
│ Orchestrator: Create task_id and prompt             │
└────────────────┬──────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│ Iteration 1: Claude reads task, makes progress      │
│ - Reads /Plans/TASK_<id>.md                         │
│ - Creates/updates files                             │
│ - Makes API calls via MCP                           │
│ - Saves intermediate results                        │
└────────────────┬──────────────────────────────────────┘
                 │
                 ▼
         ┌───────────────┐
         │ Task Complete?│
         └───┬───────┬───┘
             │       │
          Yes│       │No → Loop back to iteration 2
             │       └─────────────────────────────┐
             ▼                                     │
    ┌──────────────────┐                          │
    │ Return result    │◄─────────────────────────┘
    │ Status: success  │
    └──────────────────┘
```

### Completion Detection: Two Strategies

**Strategy 1: File Movement (Recommended)**
- Task file starts in `/Plans/`
- Claude moves it to `/Done/` when complete
- More natural: file movement is part of normal workflow
- More reliable: easy to verify

**Strategy 2: Promise-Based**
- Claude outputs: `<promise>TASK_COMPLETE</promise>`
- Executor detects in output
- Simpler to implement
- Less reliable (output parsing fragile)

---

## Usage

### Basic Command (File Movement Detection)

```bash
# Run autonomous task until /Done
python tools/ralph_wiggum_executor.py \
  "invoice_processing_001" \
  "Process all urgent invoices in /Needs_Action:
   1. Read each file
   2. Create invoice in Odoo
   3. Draft approval request
   4. Move to /Done when complete"
```

### Advanced Command (Promise-Based)

```bash
# Run autonomous task with promise detection
python tools/ralph_wiggum_executor.py \
  "lead_followup_002" \
  "Follow up with all leads in /Inbox:
   1. Read lead details
   2. Draft personalized email
   3. Send via MCP
   4. Update CRM
   5. Output: <promise>TASK_COMPLETE</promise>" \
  --use-promise \
  --max-iterations 15
```

---

## Task File Format

Claude reads and updates task state files in `/Plans/`:

```markdown
---
task_id: invoice_processing_001
status: in_progress
created: 2026-04-30T10:00:00Z
progress: "Processed 3/5 invoices"
next_step: "Process invoice #456"
completion_target: /Done/TASK_invoice_processing_001.md
---

## Task: Process Invoices

### Objective
Process all urgent invoices from /Needs_Action folder.

### Progress
- [x] Invoice #123 - Created in Odoo, draft approval
- [x] Invoice #234 - Created in Odoo, draft approval
- [x] Invoice #345 - Created in Odoo, draft approval
- [ ] Invoice #456 - Next
- [ ] Invoice #567 - Pending

### Current Step
Processing invoice #456: Create in Odoo, create approval request

### Errors
None yet.

### Next Actions
1. Read /Needs_Action/invoice_456.md
2. Create invoice in Odoo via MCP
3. Create /Pending_Approval/INVOICE_456.md
4. Check if any remain
5. If done: Move this file to /Done/
```

---

## Prompt Template

When invoking Ralph Wiggum, structure your prompt like this:

```markdown
# Task: [Brief Title]

## Objective
[1-2 sentence goal]

## Steps
1. [Step 1 - specific action]
2. [Step 2 - specific action]
3. [Step 3 - specific action]
...

## Files to Monitor
- Input: /Needs_Action/ (watch for new items)
- Working: /Plans/ (update task progress)
- Output: /Done/ (move when complete)

## Success Criteria
- All items processed
- No errors in audit log
- Files moved to appropriate folders

## Completion Signal
Move /Plans/TASK_<id>.md to /Done/ when all steps complete.
```

---

## Configuration

### Environment Variables

```bash
# .env
RALPH_MAX_ITERATIONS=10          # Default: 10
RALPH_ITERATION_TIMEOUT=300      # Default: 300 seconds
RALPH_VAULT_PATH=/path/to/vault  # Auto-detected if not set
```

### CLI Arguments

```bash
--max-iterations N     # Max iterations before timeout (default: 10)
--use-promise         # Wait for <promise>TASK_COMPLETE</promise>
--timeout SECONDS     # Timeout per iteration (default: 300)
```

---

## Examples

### Example 1: Process Emails to Invoices

**Task Definition:**
```markdown
---
task_id: email_to_invoice_20260430
---

# Convert Urgent Emails to Invoices

Process all emails in /Needs_Action marked "invoice":
1. Read email content
2. Extract customer and amount
3. Create draft invoice in Odoo
4. Create /Pending_Approval/INVOICE_<id>.md
5. Mark original email as processed
6. When all done, move this task to /Done/
```

**Invocation:**
```bash
python tools/ralph_wiggum_executor.py \
  "email_to_invoice_20260430" \
  "$(cat Plans/TASK_email_to_invoice_20260430.md)" \
  --max-iterations 20
```

**Expected Output:**
```json
{
  "task_id": "email_to_invoice_20260430",
  "status": "completed",
  "iterations": 7,
  "completion_type": "file_move",
  "summary": "Processed 5 emails, created 5 draft invoices"
}
```

---

### Example 2: Social Media Weekly Posts

**Task Definition:**
```markdown
---
task_id: weekly_social_posts_20260505
---

# Generate and Post Weekly Content

1. Read /Plans/content_calendar.md
2. Generate posts for Mon, Wed, Fri
3. Use omni_publisher to post across Facebook, Instagram, Twitter
4. Update social_summary.md with scheduling
5. Move task to /Done when complete
```

**Invocation:**
```bash
python tools/ralph_wiggum_executor.py \
  "weekly_social_posts_20260505" \
  "Post weekly content to social media per content calendar"
```

---

## State Tracking

Ralph Wiggum maintains state in `/.ralph-state/`:

```json
{
  "task_id": "invoice_processing_001",
  "created_at": "2026-04-30T10:00:00Z",
  "iterations": 7,
  "status": "completed",
  "completion_type": "file_move",
  "completed_at": "2026-04-30T10:15:30Z",
  "iterations_log": [
    {
      "iteration": 1,
      "timestamp": "2026-04-30T10:00:15Z",
      "task_file_moved": false,
      "status": "in_progress"
    },
    ...
    {
      "iteration": 7,
      "timestamp": "2026-04-30T10:15:25Z",
      "task_file_moved": true,
      "status": "completed"
    }
  ]
}
```

---

## Logging

All executions logged to `/Logs/ralph_wiggum.log`:

```
2026-04-30 10:00:00 [INFO] Starting Ralph Wiggum loop for task: invoice_processing_001
2026-04-30 10:00:00 [INFO] Iteration 1/10
2026-04-30 10:00:00 [INFO] Executing Claude prompt (iteration 1)
2026-04-30 10:00:15 [INFO] Task incomplete. Continuing loop...
2026-04-30 10:00:20 [INFO] Iteration 2/10
...
2026-04-30 10:15:25 [INFO] ✓ Task completed: File moved to /Done
2026-04-30 10:15:30 [INFO] Task completed in 7 iterations
```

---

## Audit Logging

All task completions logged to `/Logs/audit_tasks.json`:

```json
[
  {
    "timestamp": "2026-04-30T10:15:30Z",
    "task_id": "invoice_processing_001",
    "iterations": 7,
    "completion_type": "file_move",
    "max_iterations": 10
  }
]
```

---

## Best Practices

### ✅ Do's

- **Clear objectives:** Make goal explicit in task definition
- **Small steps:** Each iteration should make measurable progress
- **File markers:** Use file movements to signal state transitions
- **Logging:** Update /Plans/ task file with progress each iteration
- **Checkpoints:** Create intermediate files for verification
- **Timeouts:** Use reasonable max_iterations (10-20 typically)

### ❌ Don'ts

- **Open loops:** Don't create tasks with unclear completion criteria
- **Infinite work:** Don't ask Claude to work indefinitely
- **Silent failures:** Don't skip error handling
- **File races:** Don't have multiple agents writing same file
- **Huge iterations:** Avoid max_iterations > 50 (indicates flawed task design)

---

## Troubleshooting

### Task Doesn't Complete

**Symptom:** Hits max_iterations without completion

**Diagnosis:**
1. Check `/Plans/TASK_<id>.md` - is it being updated?
2. Check `/Logs/ralph_wiggum.log` - any errors?
3. Is task file moved to `/Done/`?
4. Check audit trail for failed MCP calls

**Fix:**
- Clarify task objective
- Break into smaller steps
- Increase max_iterations if task is complex

### Infinite Loop

**Symptom:** Repeats same action without progress

**Diagnosis:**
1. Check iteration log - is progress logged?
2. Is file movement happening?
3. Is Claude making different decisions each iteration?

**Fix:**
- Add explicit progress markers
- Reduce max_iterations to 5 for debugging
- Review prompt for clarity

---

## Integration with Other Skills

Ralph Wiggum works with all other skills:

```
Ralph Wiggum (orchestrator)
├── Email MCP (send email from approved)
├── Odoo MCP (create invoices)
├── Social Media MCP (post to platforms)
├── Browser MCP (fill forms)
└── Calendar MCP (schedule meetings)
```

For example, a single Ralph Wiggum task might:
1. Read /Needs_Action files
2. Create invoices in Odoo (Odoo MCP)
3. Draft approval emails (Email MCP)
4. Post social updates (Social MCP)
5. Schedule follow-up meetings (Calendar MCP)

---

## Next Steps

1. **Test with simple task:** Process 3 items from /Needs_Action to /Done
2. **Verify audit logging:** Check /Logs/ralph_wiggum.log
3. **Monitor iterations:** Ensure progress each iteration
4. **Integrate with schedulers:** Add to cron/Task Scheduler for recurring tasks
5. **Extend to complex workflows:** Multi-step business processes

---

**Status:** ✅ Ready to use  
**Version:** 1.0  
**Last Updated:** 2026-04-30
