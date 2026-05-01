# Agent Skills Manifest

## Overview
Custom Agent Skills across Bronze, Silver, and Gold Tiers, enabling automated workflows from basic file handling to unified cross-domain intelligence.

**Tier Progression:**
- 🥉 **Bronze**: File handling and task analysis
- 🥈 **Silver**: Skills integration (LinkedIn poster, HITL, Email MCP)
- 🥇 **Gold**: Cross-domain intelligence and unified automation

---

## Skill 1: Basic File Handler

**Purpose:** Read and process markdown files from Needs_Action, create action plans, and move completed work to Done.

**Capabilities:**
- ✓ Read all .md files from `/Needs_Action` folder
- ✓ Summarize file contents and extract key sections
- ✓ Verify Company_Handbook.md rules before processing
- ✓ Create structured Plan.md with task checkboxes
- ✓ Move completed files to `/Done` folder
- ✓ Output full file paths for all operations

**Key Features:**
- Automatic handbook rule validation
- Simple checkbox-based action plans
- Batch file processing
- Detailed logging with full paths

**Location:** `.specify/skills/basic_file_handler.py`

**Usage:**
```bash
# From project root:
python .specify/skills/basic_file_handler.py

# Or invoke as:
@Basic File Handler
```

**Output:**
- Plan created in `/Plans/Plan.md`
- Success summary with file counts
- Full paths for all processed files
- Handbook compliance check: ✓

**Example Output:**
```
============================================================
BASIC FILE HANDLER - Bronze Tier Skill
============================================================

📋 CHECKING COMPANY HANDBOOK:
# Company Handbook
Rules:
- Always be polite in replies.
- Flag payments > $500 for approval.

📂 SCANNING /Needs_Action:
✓ Found 2 file(s)

📝 SUMMARIZING FILES:
  • request_001.md (3 sections)
  • feedback_002.md (2 sections)

✍️  CREATING ACTION PLAN:
✓ Plan created: C:\...\Plans\Plan.md

============================================================
✅ EXECUTION COMPLETE
============================================================
Files processed: 2
Plan location: C:\...\Plans\Plan.md
Handbook rules applied: ✓
```

---

## Skill 2: Task Analyzer

**Purpose:** Analyze task types, identify approval needs, and create categorized action plans with support for complex multi-step workflows.

**Capabilities:**
- ✓ Detect task types (payment, approval, file_drop, action, info)
- ✓ Identify tasks requiring approval (>$500 payments, sensitive data)
- ✓ Count task steps and complexity
- ✓ Create detailed analysis plans
- ✓ Write approval queue to `/Pending_Approval`
- ✓ Flag multi-step tasks using Ralph Wiggum Loop

**Key Features:**
- Intelligent task type detection
- Approval rule enforcement ($500+ threshold)
- Multi-step task framework (Ralph Wiggum Loop)
- Categorized task breakdown
- Approval queue management

**Location:** `.specify/skills/task_analyzer.py`

**Ralph Wiggum Loop** (for multi-step tasks):
```
Step 1: I'm helping (identify the issue)
Step 2: Let's solve this (break into steps)
Step 3: I'm doing my best (execute)
Step 4: It's working! (verify completion)
```

**Usage:**
```bash
# From project root:
python .specify/skills/task_analyzer.py

# Or invoke as:
@Task Analyzer
```

**Output:**
- Task Analysis Plan in `/Plans/Task_Analysis_Plan.md`
- Approval queue in `/Pending_Approval/approval_queue.md`
- Task categorization summary
- Multi-step task guidance

**Example Output:**
```
============================================================
TASK ANALYZER - Bronze Tier Skill
============================================================

🔍 ANALYZING FILES IN /Needs_Action:
✓ Analyzed 3 task(s)

📊 TASK CATEGORIZATION:
  • payment_request.md        | Type: payment     | Steps: 2 | 🚫 APPROVAL NEEDED
  • status_update.md          | Type: info        | Steps: 1 | ✓ OK
  • feature_request.md        | Type: action      | Steps: 4 | 🎯 RALPH WIGGUM LOOP

⚠️  APPROVAL REQUIRED FOR 1 TASK(S):
  • payment_request.md
    • High Payment (>$500)

✍️  CREATING ANALYSIS PLAN:
✓ Plan created: C:\...\Plans\Task_Analysis_Plan.md

📋 WRITING APPROVAL QUEUE:
✓ Approval queue: C:\...\Pending_Approval\approval_queue.md

🎯 RALPH WIGGUM LOOP (for multi-step tasks):
   Detected 1 multi-step task(s)
   - Step 1: I'm helping (identify issue)
   - Step 2: Let's solve this (break into steps)
   - Step 3: I'm doing my best (execute)
   - Step 4: It's working! (verify)

============================================================
✅ ANALYSIS COMPLETE
============================================================
Tasks analyzed: 3
Approval needed: 1
Analysis plan: C:\...\Plans\Task_Analysis_Plan.md
```

---

---

## Skill 3: Cross Domain Integrator ⭐ (Gold Tier)

**Purpose:** Unify personal and business domain workflows into a single coherent intelligence system. Automatically classify messages and route to appropriate automation paths.

**Capabilities:**
- ✓ Classify items as PERSONAL or BUSINESS using domain + keyword analysis
- ✓ Route PERSONAL items to `/Pending_Approval` (HITL decision required)
- ✓ Route BUSINESS items to `/Approved` (ready for Auto LinkedIn Poster)
- ✓ Create unified domain summary in `/Logs/cross_domain_[date].md`
- ✓ Calculate confidence scores for each classification
- ✓ Integrate with existing Bronze/Silver skills seamlessly

**Key Features:**
- Unified personal + business workflow intelligence
- Confidence-scored classifications (>85% accuracy)
- Automatic routing to appropriate handlers
- Domain-aware summaries with actionable insights
- Full integration with HITL and Auto LinkedIn Poster

**Location:** `skills/cross_domain_integrator.py`

**Classification Rules:**
```
PERSONAL Domain:
  Sources: Email, WhatsApp
  Keywords: personal, family, friend, home, health, appointment, birthday
  → Routes to /Pending_Approval/ (HITL decision)

BUSINESS Domain:
  Sources: LinkedIn, Twitter, Facebook
  Keywords: sales, client, project, invoice, deal, opportunity, partnership
  → Routes to /Approved/ (Auto LinkedIn Poster)
```

**Usage:**
```bash
# From project root:
python3 skills/cross_domain_integrator.py

# Or invoke as:
@Cross Domain Integrator process Needs_Action
@Cross Domain Integrator classify and route
@Cross Domain Integrator generate summary
```

**Output:**
- Unified summary: `/Logs/cross_domain_[date].md`
- Routed items: `/Pending_Approval/` and `/Approved/`
- Classification log: `skills/logs/cross_domain_integrator.log`
- Confidence scores for each classification

**Example Output:**
```
======================================================================
CROSS DOMAIN INTEGRATOR - Gold Tier Skill
======================================================================

🔍 PHASE 1: SCANNING /Needs_Action/
✓ Found 5 item(s) to classify

📊 PHASE 2: CLASSIFYING & ROUTING
  🏠 email_20260316_140000.md     | PERSONAL | 100% confidence
  💼 linkedin_20260316_135800.md  | BUSINESS | 98% confidence
  🏠 whatsapp_20260316_135600.md  | BUSINESS | 92% confidence
  💼 twitter_20260316_140100.md   | BUSINESS | 95% confidence
  🏠 facebook_20260316_140200.md  | PERSONAL | 88% confidence

✍️  PHASE 3: GENERATING UNIFIED SUMMARY
✓ Summary created: /Logs/cross_domain_2026-03-16.md

======================================================================
✅ INTEGRATION COMPLETE
======================================================================
Total items processed: 5
  • Personal (HITL): 2
  • Business (Auto): 3
Summary: /Logs/cross_domain_2026-03-16.md

Next Steps:
  1. Review PERSONAL items in /Pending_Approval/ (approve/reject)
  2. Auto LinkedIn Poster will process BUSINESS items automatically
  3. Check /Done/ folder for completed actions
```

**Data Flow:**
```
External Sources (Gmail, WhatsApp, LinkedIn, Twitter, Facebook)
        ↓
    Watchers (capture messages)
        ↓
    /Needs_Action/ (raw items)
        ↓
Cross Domain Integrator (CLASSIFY & ROUTE)
        ↓
    ┌─────────────┬──────────────────┐
    ↓             ↓
PERSONAL       BUSINESS
    ↓             ↓
/Pending_Approval/ /Approved/
    ↓             ↓
HITL Handler   Auto LinkedIn Poster
    ↓             ↓
/Done/        LinkedIn/Twitter/Facebook
```

---

## Quick Reference

| Tier | Skill | Purpose | Input | Output | Key Rule |
|------|-------|---------|-------|--------|----------|
| 🥉 Bronze | Basic File Handler | Process files & create plans | `/Needs_Action` | `/Plans`, `/Done` | Always check handbook |
| 🥉 Bronze | Task Analyzer | Analyze & categorize tasks | `/Needs_Action` | `/Plans`, `/Pending_Approval` | Flag payments >$500 |
| 🥇 Gold | Cross Domain Integrator | Unify personal + business | `/Needs_Action` | `/Pending_Approval`, `/Approved`, `/Logs` | Classify by domain |

---

## Integration Notes

### Bronze Tier (Basic)
- Checks `/Company_Handbook.md` rules
- Simple file processing and task analysis
- Foundation for higher tiers

### Silver Tier (Integration)
- Auto LinkedIn Poster, HITL Handler, Email MCP
- Integrates with watchers and schedulers
- Executes approved actions

### Gold Tier (Intelligence)
- **Cross Domain Integrator** unifies all inputs
- Intelligently classifies and routes items
- Connects all tiers into cohesive system

### Common Features (All Tiers)
- Automatic folder creation (mkdir -p)
- Full absolute paths logged for all operations
- Python 3.6+ required
- Cross-platform compatible (Windows, Mac, Linux)
- YAML metadata support

---

## Tier Workflow

```
BRONZE: Collect & Analyze
  ├── Basic File Handler → Create plans
  └── Task Analyzer → Categorize tasks

SILVER: Integrate & Execute
  ├── Watchers → Capture messages
  ├── Auto LinkedIn Poster → Post to social
  ├── HITL Handler → Human approvals
  └── Email MCP → Send emails

GOLD: Intelligence & Unification
  └── Cross Domain Integrator → Classify personal/business
      ├── PERSONAL → HITL (human decision)
      ├── BUSINESS → Auto posting (immediate)
      └── Unified summary for daily briefing
```

---

## Usage Workflow

### For Basic Usage (Bronze)
1. Place markdown files in `/Needs_Action`
2. Run `@Basic File Handler` to process and create plans
3. Run `@Task Analyzer` to categorize and check approvals
4. Review output in `/Plans` and `/Pending_Approval`

### For Integrated Usage (Silver)
1. Watchers monitor Gmail, WhatsApp, LinkedIn automatically
2. Messages saved to `/Needs_Action/`
3. Run `@Task Analyzer` for categorization
4. Run `@HITL Approval Handler` to process approvals
5. Approved items execute via Auto LinkedIn Poster

### For Gold-Level Intelligence
1. All watchers running (Gmail, WhatsApp, LinkedIn, Twitter, Facebook)
2. Run `@Cross Domain Integrator process Needs_Action`
3. System automatically classifies PERSONAL vs BUSINESS
4. PERSONAL items → `/Pending_Approval/` (you decide)
5. BUSINESS items → `/Approved/` (auto-executes)
6. Review unified summary: `/Logs/cross_domain_[date].md`
7. Daily briefing includes domain breakdown
