# Project Structure & Architecture
**Hackathon0Gold - Complete System Design**

---

## 🏗️ Complete Folder Structure

```
Hackathon0Gold/
│
├── 📄 Configuration Files
│   ├── ecosystem.config.js         ⭐ PM2 master configuration (5 watchers)
│   ├── requirements.txt             ⭐ Python dependencies
│   ├── .env                         OAuth tokens and API keys (gitignored)
│   └── .gitignore                   Git ignore rules
│
├── 📂 watchers/                     ⭐ CORE SYSTEM - Message monitoring
│   ├── gmail_watcher.py            ✅ Email capture (Gmail API)
│   ├── whatsapp_persistent.py      ✅ WhatsApp capture (Playwright)
│   ├── linkedin_persistent.py      ✅ LinkedIn capture (Playwright)
│   ├── instagram_watcher_fixed.py  ✅ Instagram capture (Playwright)
│   ├── facebook_watcher_js_extract.py ✅ Facebook Messenger (Undetected Chrome + JavaScript)
│   │
│   ├── [Legacy/Experimental files - can be deleted]
│   ├── facebook_watcher_undetected.py
│   ├── facebook_watcher_visible.py
│   ├── facebook_watcher_robust.py
│   ├── facebook_watcher_fixed.py
│   ├── facebook_watcher_only.py
│   ├── facebook_instagram_watcher.py
│   ├── instagram_watcher_only.py
│   ├── whatsapp_watcher.py
│   ├── whatsapp_watcher_js.py
│   ├── whatsapp_watcher_simplified.py
│   ├── linkedin_watcher.py
│   ├── filesystem_watcher.py
│   ├── filesystem_watcher_simple.py
│   │
│   ├── logs/                        PM2 managed logs
│   │   ├── facebook_watcher_js.log
│   │   ├── whatsapp_watcher.log
│   │   └── ...
│   └── __pycache__/                Python cache (auto-generated)
│
├── 📂 session/                      ⭐ Persistent authentication & state
│   ├── gmail_session/              Gmail OAuth token storage
│   ├── facebook_js_extract/        Facebook browser profile (user-data-dir)
│   ├── whatsapp_session/           WhatsApp browser context
│   ├── linkedin_session/           LinkedIn browser context
│   ├── instagram_session/          Instagram browser context
│   └── facebook_cookies.json       Saved cookies (if applicable)
│
├── 📂 Needs_Action/                 ⭐ AUTO-CAPTURED MESSAGES
│   ├── facebook_20260324T06560_8892709d_message.md
│   ├── gmail_20260324T093015_a4f2c1e0_message.md
│   ├── whatsapp_20260324T102030_b5g3d2f1_message.md
│   ├── linkedin_20260324T110145_c6h4e3g2_message.md
│   ├── instagram_20260324T120300_d7i5f4h3_message.md
│   └── [Messages auto-deleted after processing or moved to Done/]
│
├── 📂 Pending_Approval/             Tasks awaiting human approval
│   ├── task_001_action_plan.md
│   └── [Tasks moved here by Ralph Loop for HITL review]
│
├── 📂 Approved/                     Approved for execution
│   ├── task_002_email_response.md
│   └── [Approved tasks ready for action]
│
├── 📂 Done/                         Completed tasks
│   ├── task_003_completed.md
│   └── [Finished work moved here]
│
├── 📂 Rejected/                     Rejected tasks
│   └── [Human rejected tasks]
│
├── 📂 skills/                       AI agent skills & utilities
│   ├── auto_linkedin_poster.py     Draft LinkedIn posts from leads
│   ├── hitl_approval_handler.py    Human-in-the-loop approval workflow
│   ├── gmail_label_organizer.py    Organize Gmail by sender
│   ├── social_summary_generator.py Generate response drafts
│   ├── task_analyzer.py            Analyze tasks from messages
│   ├── logs/                        Skill execution logs
│   └── __pycache__/
│
├── 📂 tools/                        Core system tools
│   ├── ralph_loop_runner.py        Iterative reasoning engine
│   ├── email_processor.py          Process Gmail messages
│   ├── logs/
│   └── __pycache__/
│
├── 📂 mcp_servers/                  External integrations
│   └── email-mcp/                  Node.js MCP server for Gmail
│       ├── package.json
│       ├── server.js
│       └── ...
│
├── 📂 history/                      Documentation & project history
│   │
│   ├── adr/                         Architecture Decision Records
│   │   ├── 001-javascript-extraction-for-facebook.md
│   │   └── [Major architectural decisions documented here]
│   │
│   ├── prompts/                     Prompt History Records (PHRs)
│   │   ├── facebook-watcher/
│   │   │   └── 001-facebook-js-extraction-fix.green.prompt.md
│   │   ├── gmail/
│   │   ├── general/
│   │   └── [All AI interactions logged here for traceability]
│   │
│   └── [Session logs, project notes, etc.]
│
├── 📂 Logs/                         Archived logs
│   ├── SESSION_2026-02-25_GMAIL_ORGANIZATION.md
│   ├── SYSTEM_STATUS_2026-02-25.md
│   └── [Historical logs and session records]
│
├── 📂 Plans/                        Planning documents
│   └── [Feature plans, architecture sketches]
│
├── 📂 Inbox/                        Unprocessed items
│   └── [New items before categorization]
│
├── 📂 .specify/                     Spec-Driven Development templates
│   ├── memory/
│   ├── templates/
│   └── scripts/
│
├── 📄 Documentation (in root)
│   ├── README.md                   Project overview
│   ├── STARTUP_GUIDE.md            ⭐ How to start the system
│   ├── SYSTEM_REQUIREMENTS.md      ⭐ Dependencies & setup
│   ├── PROJECT_STRUCTURE.md        This file
│   ├── FACEBOOK_WATCHER_FIX_SUMMARY.md    ⭐ Facebook implementation
│   ├── FACEBOOK_FIX_QUICK_STEPS.md        ⭐ Quick reference
│   ├── CLAUDE.md                   Project rules & guidelines
│   └── [Other documentation]
│
├── 📝 Git Configuration
│   ├── .git/                        Git repository (version control)
│   ├── .gitignore                   Files to ignore in Git
│   └── [Branches: main, 1-fastapi-backend, etc.]
│
└── 📊 System Files
    ├── __pycache__/
    └── *.pyc
```

---

## 🎯 The 5 Active Watchers

### 1. **Gmail Watcher** 📧
- **File:** `watchers/gmail_watcher.py`
- **Technology:** Google Gmail API (OAuth 2.0)
- **Interval:** 60 seconds
- **Session:** `session/gmail_session/` (OAuth token)
- **Output:** Emails matching keywords → `Needs_Action/`
- **Keywords:** ['urgent', 'invoice', 'payment', 'sales', 'client', 'project', ...]
- **Status:** ✅ STABLE (205+ restarts due to token refresh)

### 2. **WhatsApp Watcher** 💬
- **File:** `watchers/whatsapp_persistent.py`
- **Technology:** Playwright + WhatsApp Web
- **Interval:** 90 seconds
- **Session:** `session/whatsapp_session/` (Browser context)
- **Output:** Messages matching keywords → `Needs_Action/`
- **Keywords:** ['urgent', 'invoice', 'payment', 'sales', ...]
- **Status:** ✅ STABLE (5+ restarts)
- **Note:** Requires phone for QR code scan on first login

### 3. **LinkedIn Watcher** 💼
- **File:** `watchers/linkedin_persistent.py`
- **Technology:** Playwright + LinkedIn Web
- **Interval:** 90 seconds
- **Session:** `session/linkedin_session/` (Browser context)
- **Output:** Posts/messages matching keywords → `Needs_Action/`
- **Keywords:** ['sales', 'client', 'project', 'opportunity', 'partnership', ...]
- **Status:** ✅ STABLE (3+ restarts)
- **Note:** Monitors feed and messaging

### 4. **Instagram Watcher** 📸
- **File:** `watchers/instagram_watcher_fixed.py`
- **Technology:** Playwright + Instagram Web
- **Interval:** 90 seconds
- **Session:** `session/instagram_session/` (Browser context)
- **Output:** DMs matching keywords → `Needs_Action/`
- **Keywords:** ['urgent', 'invoice', 'payment', 'sales', ...]
- **Status:** ✅ STABLE (3+ restarts)
- **Note:** May prompt for code verification on login

### 5. **Facebook Watcher** 🔵 (NEWLY FIXED)
- **File:** `watchers/facebook_watcher_js_extract.py`
- **Technology:** Undetected Chromedriver + JavaScript injection
- **Interval:** 60 seconds
- **Session:** `session/facebook_js_extract/` (Browser profile)
- **Output:** Messenger messages matching keywords → `Needs_Action/`
- **Keywords:** ['sales', 'client', 'project', 'urgent', 'invoice', 'payment', ...]
- **Status:** ✅ STABLE (0 restarts) - NEWLY FIXED
- **Special:** Uses JavaScript extraction instead of CSS selectors
- **Implementation:** See `FACEBOOK_WATCHER_FIX_SUMMARY.md`

---

## 📬 Message Flow

```
┌─────────────────────────────────────────────────────┐
│             External Platforms                      │
│  Gmail / WhatsApp / LinkedIn / Instagram / Facebook │
└──────────────────────┬──────────────────────────────┘
                       │
                       │ (User receives messages)
                       │
┌──────────────────────▼──────────────────────────────┐
│             5 Autonomous Watchers                    │
│  - Gmail API client (every 60s)                     │
│  - Playwright browsers (every 90s)                  │
│  - Undetected Chrome (every 60s)                    │
└──────────────────────┬──────────────────────────────┘
                       │
        (Keyword matching: sales, urgent, payment, ...)
                       │
┌──────────────────────▼──────────────────────────────┐
│         Needs_Action/ Folder                        │
│    (Auto-saved messages with keywords)              │
│                                                     │
│  facebook_20260324T06560_8892709d_message.md       │
│  gmail_20260324T093015_a4f2c1e0_message.md         │
│  whatsapp_20260324T102030_b5g3d2f1_message.md      │
│  linkedin_20260324T110145_c6h4e3g2_message.md      │
│  instagram_20260324T120300_d7i5f4h3_message.md     │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│         Ralph Loop (Iterative Reasoning)            │
│    (AI agent processes messages max 10 iterations)  │
└──────────────────────┬──────────────────────────────┘
                       │
        (Requires human approval for actions)
                       │
┌──────────────────────▼──────────────────────────────┐
│     Pending_Approval/ Folder                        │
│  (Tasks awaiting human review & approval)           │
└──────────────────────┬──────────────────────────────┘
                       │
        (User approves or rejects in Pending_Approval/)
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
   ┌─────────┐               ┌──────────────┐
   │ Approved│               │  Rejected    │
   └────┬────┘               └──────────────┘
        │
        │ (Execute approved action)
        │
        ▼
   ┌──────────────┐
   │    Done/     │
   │(Completed)   │
   └──────────────┘
```

---

## 🔄 System Components

### Message Capture Layer (Watchers)
- **Purpose:** Monitor 5 platforms 24/7
- **Input:** Live platform messages
- **Output:** Filtered messages with keywords
- **Technology:** API + Browsers
- **Deployment:** PM2 (auto-restart on crash)

### Processing Layer (Ralph Loop)
- **Purpose:** Analyze captured messages
- **Input:** Messages from Needs_Action/
- **Output:** Proposed actions
- **Technology:** Claude AI (iterative reasoning)
- **Constraints:** Max 10 iterations per message

### Approval Layer (HITL - Human-In-The-Loop)
- **Purpose:** Human review & decision
- **Input:** Proposed actions
- **Output:** Approval or rejection
- **Workflow:** Move files between Pending_Approval/ and Approved/

### Execution Layer (Skills)
- **Purpose:** Perform approved actions
- **Input:** Approved tasks
- **Output:** Completed work
- **Examples:** Email replies, LinkedIn posts, etc.

### Archival Layer (History)
- **Purpose:** Document all work
- **Input:** All decisions & actions
- **Output:** Historical records (ADR, PHR)
- **Technology:** Markdown files

---

## 📊 Data Storage

| Data | Location | Format | Purpose |
|------|----------|--------|---------|
| Captured Messages | `Needs_Action/` | Markdown | Ready for processing |
| OAuth Tokens | `session/gmail_session/` | JSON | Gmail authentication |
| Browser State | `session/*/` | Chrome profile | Session persistence |
| Approval Tasks | `Pending_Approval/` | Markdown | Human review |
| Approved Tasks | `Approved/` | Markdown | Ready to execute |
| Completed Tasks | `Done/` | Markdown | Historical record |
| Logs | `~/.pm2/logs/` + `watchers/logs/` | Text | Debug & monitoring |
| ADRs | `history/adr/` | Markdown | Architecture decisions |
| PHRs | `history/prompts/` | Markdown | AI interaction records |

---

## 🚀 Deployment Model

### Current (PM2-Based)
```
┌────────────────────────────────────────┐
│   Your Computer (Windows 11)           │
│  ┌──────────────────────────────────┐ │
│  │  Terminal 1: PM2 Manager         │ │
│  │  - Runs all 5 watchers           │ │
│  │  - Auto-restarts on crash        │ │
│  │  - Monitors memory/CPU           │ │
│  └──────────────────────────────────┘ │
│  ┌──────────────────────────────────┐ │
│  │  Terminal 2: Monitor Messages    │ │
│  │  - Watches Needs_Action/ folder  │ │
│  │  - Real-time notifications       │ │
│  └──────────────────────────────────┘ │
└────────────────────────────────────────┘
```

### Planned (FastAPI Backend - Branch: 1-fastapi-backend)
```
┌──────────────────────────────────────────┐
│   Your Computer (Windows 11)             │
│  ┌────────────────────────────────────┐ │
│  │  FastAPI Server (Port 8000)        │ │
│  │  - RESTful API over message system │ │
│  │  - Web dashboard                   │ │
│  │  - Remote monitoring               │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │  PM2 Manager (Backend)             │ │
│  │  - 5 watchers (unchanged)          │ │
│  │  - Ralph Loop processor             │ │
│  │  - Skill executor                  │ │
│  └────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

---

## 🔐 Security Model

- **Secrets:** API keys stored in `.env` (gitignored)
- **Sessions:** Browser profiles in `session/` (local storage only)
- **OAuth:** Google handles auth flow securely
- **Logs:** Sensitive info should be masked (TODO)
- **Access:** Single-user (local machine only)
- **Backup:** Regularly backup `session/` and `Needs_Action/` folders

---

## 📈 Scalability

### Current (Single Machine)
- **Capacity:** ~10,000+ messages/day
- **Latency:** 60-90 seconds per check
- **Memory:** ~1.5 GB for all watchers
- **Bottleneck:** Selenium/Playwright browser startup time

### Future (Distributed)
- Multiple workers per platform
- Cloud deployment (AWS, GCP, Azure)
- Message queue (RabbitMQ, Kafka)
- Scalable processing (Celery)

---

**Complete system architecture documented and ready for deployment!** ✨
