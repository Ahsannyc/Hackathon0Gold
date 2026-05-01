---
ID: 001
TITLE: Facebook/Instagram Watcher + Social Summary Generator Implementation
STAGE: gold
DATE_ISO: 2026-03-19
SURFACE: agent
MODEL: claude-haiku-4.5
FEATURE: facebook-instagram-monitoring
BRANCH: 1-fastapi-backend
USER: claude-code
COMMAND: Implement plan
LABELS: ["gold-tier", "watchers", "skills", "social-media", "facebook", "instagram", "hitl"]
LINKS:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
FILES_YAML:
  - watchers/facebook_instagram_watcher.py
  - skills/social_summary_generator.py
  - FACEBOOK_INSTAGRAM_SETUP_GUIDE.md
TESTS_YAML:
  - Manual: Send test message with keyword "sales" to Facebook Messenger
  - Manual: Send test DM with keyword "client" to Instagram
  - Manual: Verify Needs_Action captures both messages
  - Manual: Run skill and verify Plans/Pending_Approval populated
  - Manual: PM2 start and monitor continuous operation
---

# Implementation: Facebook/Instagram Watcher + Social Summary Generator

## Summary

Implemented Gold Tier Facebook/Instagram monitoring system with persistent browser session and HITL-based response generation. Follows existing pattern from LinkedIn watcher and auto-poster skill with Meta-specific adaptations.

## What Was Built

### 1. Facebook/Instagram Persistent Watcher
**File:** `watchers/facebook_instagram_watcher.py` (~400 lines)

**Key Features:**
- Persistent Playwright context for FB + IG simultaneous monitoring
- Separate message extraction for Facebook Messenger and Instagram DMs
- Keyword filtering (sales, client, project)
- MD5 deduplication of captured messages
- 60-second polling interval, 90-minute session refresh
- Auto-restart on 5+ consecutive auth failures
- Comprehensive logging to `watchers/logs/facebook_instagram_watcher.log`

**Session Management:**
- `session/facebook/` - shared Meta login (FB + IG single auth)
- `session/facebook_authenticated.txt` - timestamp marker
- Persistent cookies/localStorage across restarts

**Message Capture:**
- Facebook: Monitors `https://www.facebook.com/messages/t/`
- Instagram: Navigates to `https://www.instagram.com/direct/inbox/`
- Both use JavaScript extraction via `page.evaluate()`
- Detects: sender name, message preview (200 chars), full text (500 chars)

**Markdown Output Format:**
```
Needs_Action/facebook_YYYYMMDD_HHMMSS_<md5-8chars>_<safe_sender>.md
Needs_Action/instagram_YYYYMMDD_HHMMSS_<md5-8chars>_<safe_sender>.md
```

### 2. Social Summary Generator Skill
**File:** `skills/social_summary_generator.py` (~450 lines)

**Key Features:**
- Scans `/Needs_Action` for `facebook_*.md` and `instagram_*.md` files
- Extracts YAML metadata and message content
- Generates contextual response drafts using platform-specific templates
- References `Company_Handbook.md` for tone guidelines
- Saves drafts to `/Plans` with YAML frontmatter
- Moves drafts to `/Pending_Approval` for HITL review
- Polite tone enforcement (replaces negative words)

**Response Templates:**
- Facebook: "Thanks for reaching out! I'd love to discuss {service}..."
- Instagram: "Thanks for the DM! Interested in {service}? Let's connect! 🙌"

**Metadata Tracking:**
```
type: facebook_response | instagram_response
from: <sender_name>
status: draft → pending_approval → ready_for_sending
priority: high | medium
keywords: [sales, client]
created_at: <ISO timestamp>
```

### 3. Setup Guide & Documentation
**File:** `FACEBOOK_INSTAGRAM_SETUP_GUIDE.md` (~400 lines)

**Contents:**
- Prerequisites and installation steps
- Manual and PM2 startup procedures
- Three test scenarios (FB Messenger, IG DMs, Skill)
- Complete workflow diagram (message capture → approval → completion)
- Configuration options (keywords, intervals, refresh timing)
- Logging and monitoring commands
- Comprehensive troubleshooting section
- PM2 management commands
- Verification checklist
- Integration with existing system (Ralph Loop, HITL, Daily Briefing)

## Implementation Details

### Architecture Decisions

1. **Shared Meta Session:**
   - Single `session/facebook/` directory for both FB + IG
   - Meta account login works for both platforms
   - Reduces authentication complexity

2. **Persistent Browser Context:**
   - Mimics LinkedIn watcher pattern exactly
   - Keeps browser open between checks to avoid login loops
   - Session validation every 90 minutes with auto-restart

3. **Keyword-Based Filtering:**
   - Same `KEYWORDS = ['sales', 'client', 'project']` as LinkedIn
   - Allows consistent routing across all watchers
   - Extensible by editing one line in each file

4. **YAML Frontmatter:**
   - Matches existing pattern from LinkedIn messages
   - Enables skill-to-skill chaining (watcher → generator → HITL handler)
   - Preserves metadata through entire workflow

5. **HITL Approval Loop:**
   - Drafts created in `/Plans` (staging)
   - Moved to `/Pending_Approval` (requires human review)
   - User moves to `/Approved` to authorize sending
   - Integrates with existing `hitl_approval_handler.py`

### Code Quality

- **Error Handling:** Try-catch wraps all network/file operations
- **Logging:** Structured logs with [OK], [ERROR], [WARN] prefixes
- **Windows Support:** UTF-8 encoding support with TextIOWrapper
- **Deduplication:** MD5 hash of sender + message content
- **Session Recovery:** 5-strike consecutive failure limit before restart
- **Memory Management:** PM2 restarts on 500MB+ memory usage

## Testing Strategy

### Scenario 1: Facebook Messenger
```
1. Start watcher
2. Send "Hi, I have a **sales** project for you"
3. Verify Needs_Action/facebook_*.md created
4. Check YAML metadata: type: facebook, keywords: [sales, project]
5. Verify message content captured correctly
```

### Scenario 2: Instagram DMs
```
1. Watcher already running
2. Send "Hey, interested in a **client** opportunity"
3. Verify Needs_Action/instagram_*.md created
4. Check watcher navigated to /direct/inbox/
```

### Scenario 3: Skill Processing
```
1. Ensure messages in Needs_Action
2. Run: python3 skills/social_summary_generator.py --dry-run
3. Verify console shows "Found X social media messages with keywords"
4. Run: python3 skills/social_summary_generator.py --process
5. Verify Plans/facebook_draft_*.md created
6. Verify Pending_Approval/facebook_draft_*.md created
7. Check drafted response includes keywords and is platform-appropriate
```

### Scenario 4: PM2 Integration
```
1. pm2 start watchers/facebook_instagram_watcher.py --name facebook-instagram-watcher --interpreter python3
2. pm2 logs facebook-instagram-watcher
3. Send test message with keyword
4. Verify capture in logs and filesystem
5. pm2 restart facebook-instagram-watcher (verify auto-recovery)
```

## Verification Checklist

- [x] Watcher file exists: `watchers/facebook_instagram_watcher.py`
- [x] Skill file exists: `skills/social_summary_generator.py`
- [x] Setup guide exists: `FACEBOOK_INSTAGRAM_SETUP_GUIDE.md`
- [x] Session path configured: `session/facebook/`
- [x] Keywords consistent: `['sales', 'client', 'project']`
- [x] YAML frontmatter matches existing pattern
- [x] Markdown output filenames follow convention
- [x] Logging infrastructure in place
- [x] PM2 commands documented
- [x] Troubleshooting section comprehensive
- [x] Integration with HITL handler documented
- [x] Code follows existing patterns (LinkedIn, WhatsApp watchers)

## Next Steps

1. **Start watcher:** `pm2 start watchers/facebook_instagram_watcher.py --name facebook-instagram-watcher --interpreter python3`
2. **Send test message** with keyword (sales/client/project)
3. **Verify capture:** `ls Needs_Action/facebook_*.md`
4. **Run skill:** `python3 skills/social_summary_generator.py --process`
5. **Review draft:** `cat Pending_Approval/facebook_draft_*.md`
6. **Schedule skill with cron:** `pm2 start skills/social_summary_generator.py --name social_summary_generator --interpreter python3 --cron "0 * * * *"`

## Integration Points

- **Ralph Loop Runner:** Can process Approved drafts for message sending
- **HITL Handler:** Existing approval workflow compatible
- **Daily Briefing:** Can summarize Facebook/Instagram messages in daily report
- **LinkedIn Watcher:** Parallel operation with same directory structure
- **Email Watcher:** All route through `Needs_Action/` → skill processing → `Pending_Approval/`

---

**Implementation Time:** ~30 minutes
**Files Created:** 3
**Lines of Code:** 850+
**Status:** Ready for Testing
