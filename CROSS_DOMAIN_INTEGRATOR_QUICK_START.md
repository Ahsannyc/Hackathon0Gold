# Cross Domain Integrator - Gold Tier Skill Quick Start

**Status**: ✅ Ready to Use
**Tier**: Gold ⭐⭐⭐
**Created**: 2026-03-16

---

## What It Does (In 30 Seconds)

Your AI system receives messages from 5 sources:
- 📧 Gmail (personal + business emails)
- 💬 WhatsApp (personal messages)
- 💼 LinkedIn (business opportunities)
- 🐦 Twitter (business announcements)
- 📘 Facebook (mixed content)

**Problem**: All messages go to `/Needs_Action/` mixed together.

**Solution**: Cross Domain Integrator **automatically separates** personal from business:
- 🏠 **Personal** → Human reviews & decides
- 💼 **Business** → Automatically posts to LinkedIn/Twitter/Facebook

---

## Quick Start (2 Steps)

### Step 1: Make Sure You Have Messages
```bash
# Check what's in Needs_Action
ls Needs_Action/

# Should see files like:
# email_20260316_001.md
# whatsapp_message_*.md
# linkedin_message_*.md
```

### Step 2: Run the Integrator
```bash
# From project root
python3 skills/cross_domain_integrator.py

# Expected output:
# ✓ Found 5 items to classify
# ✓ Classified: 2 PERSONAL, 3 BUSINESS
# ✓ Summary: /Logs/cross_domain_2026-03-16.md
```

**That's it!** ✅

---

## What Happens Next

### Personal Items (You Decide)
```
Your Email: "Family dinner Sunday?"
Your WhatsApp: "How's the family?"

⬇️ Routed to: /Pending_Approval/

Your Decision:
  ✓ Approve → Execute action
  ✗ Reject → Discard

HITL Handler monitors and executes your decision
```

### Business Items (Auto Posting)
```
LinkedIn: "Sales opportunity - $50K deal"
Twitter: "Partnership proposal"

⬇️ Routed to: /Approved/

Automatic:
  Auto LinkedIn Poster picks up
  Drafts and posts to LinkedIn/Twitter
  Logs success in /Done/
```

---

## See Results

### View the Summary
```bash
# View unified domain summary
cat Logs/cross_domain_2026-03-16.md

# Shows:
# - What items were classified
# - Confidence scores (87%, 95%, 100%, etc.)
# - What action each one will take
# - Personal vs Business breakdown
```

### Check Routing
```bash
# Personal items awaiting your decision
ls Pending_Approval/

# Business items ready for auto-posting
ls Approved/
```

### Monitor the Log
```bash
# View detailed routing log
cat skills/logs/cross_domain_integrator.log

# Shows decision for each item with timestamp
# Example:
# 2026-03-16 14:30:05 - ✓ Routed email_001.md → PERSONAL (100% confidence)
# 2026-03-16 14:30:05 - ✓ Routed linkedin_001.md → BUSINESS (98% confidence)
```

---

## How It Classifies

### PERSONAL Domain
**From**: Email, WhatsApp
**Keywords**: family, friend, home, personal, health, appointment, birthday
**Action**: Needs human approval → `/Pending_Approval/`

**Example**:
```
WhatsApp: "Hey, family dinner this Sunday?"
    ↓
Identified as: PERSONAL (WhatsApp source + "family" keyword)
    ↓
Routed to: /Pending_Approval/ (you decide)
```

### BUSINESS Domain
**From**: LinkedIn, Twitter, Facebook
**Keywords**: sales, client, project, invoice, deal, opportunity, partnership
**Action**: Ready for automation → `/Approved/`

**Example**:
```
LinkedIn: "Enterprise deal - $50K sales opportunity"
    ↓
Identified as: BUSINESS (LinkedIn source + "sales" + "opportunity")
    ↓
Routed to: /Approved/ (auto-posts immediately)
```

---

## Confidence Scores

The skill shows how confident it is about each classification:

```
email_20260316_001.md       | PERSONAL | 100% confidence ← Very sure
whatsapp_20260316_001.md    | BUSINESS |  92% confidence ← Pretty sure
linkedin_20260316_001.md    | BUSINESS |  98% confidence ← Very sure
twitter_20260316_001.md     | BUSINESS |  95% confidence ← Very sure
```

- **90-100%**: Trust the classification
- **80-90%**: Might want to double-check
- **<80%**: Ambiguous, may need review

---

## Daily Workflow

### Morning (Automatic)
1. ✅ Overnight watchers captured messages
2. ✅ Daily briefing runs at 8AM
3. ✅ Includes personal + business summary

### Anytime
```bash
# Run integrator manually
python3 skills/cross_domain_integrator.py

# Or via agent
@Cross Domain Integrator process Needs_Action
```

### Your Actions
1. **Review `/Pending_Approval/`** - Personal items waiting for you
   - Approve → Action executes
   - Reject → Item discarded

2. **Check `/Done/`** - Completed actions from yesterday
   - Personal approvals executed
   - Business posts successful

3. **View `/Logs/cross_domain_[date].md`** - Daily domain summary
   - What was personal, what was business
   - Success rates and actions taken

---

## Integration with Other Skills

### Works With: Task Analyzer (Bronze)
```
Task Analyzer: "This is a PAYMENT task"
Cross Domain: "This is also BUSINESS domain"
Result: High-priority business payment → Auto-routes
```

### Works With: HITL Approval Handler (Silver)
```
Cross Domain: "This is PERSONAL"
    ↓
HITL Handler: Monitors /Pending_Approval/
    ↓
You approve/reject
    ↓
HITL Handler executes your decision
```

### Works With: Auto LinkedIn Poster (Silver)
```
Cross Domain: "This is BUSINESS"
    ↓
Auto LinkedIn Poster: Picks up from /Approved/
    ↓
Posts to LinkedIn/Twitter/Facebook
    ↓
Logs success in /Done/
```

### Works With: Daily Briefing (Silver)
```
Daily Briefing reads: /Logs/cross_domain_[date].md
    ↓
Shows unified summary of:
  - What was personal (your decisions)
  - What was business (auto-executed)
  - Total value of business opportunities
  - Success rate of postings
```

---

## Common Commands

```bash
# Run integrator once
python3 skills/cross_domain_integrator.py

# See logs
cat skills/logs/cross_domain_integrator.log

# View today's summary
cat Logs/cross_domain_2026-03-16.md  # Update date as needed

# Check what's pending approval
ls Pending_Approval/

# Check what's approved and ready
ls Approved/

# View a specific routed item
cat Pending_Approval/email_*.md
cat Approved/linkedin_*.md
```

---

## Troubleshooting

### No items processed
**Check**: Is `/Needs_Action/` empty?
```bash
ls Needs_Action/
# If empty, run watchers to capture messages
pm2 list  # Check if watchers running
```

### Low confidence scores
**Check**: Item contains ambiguous keywords
**Solution**: Skill will mark as either PERSONAL or BUSINESS based on source

### Item routed to wrong folder
**Check**: Review the classification logic
**Solution**: Can manually move between `/Pending_Approval/` and `/Approved/`

---

## Success Indicators

✅ Items appearing in `/Needs_Action/`
✅ Running integrator shows "Found N items"
✅ Items split between `/Pending_Approval/` (personal) and `/Approved/` (business)
✅ Summary created in `/Logs/cross_domain_[date].md`
✅ Personal items awaiting your approval decision
✅ Business items auto-posting via LinkedIn Poster

All checkmarks? **System is working perfectly!** 🎉

---

## Key Benefits

| Benefit | Meaning |
|---------|---------|
| **Unified Intelligence** | One system handles personal + business, no context switching |
| **Automatic Classification** | Skill decides which domain, not you |
| **Smart Routing** | Items go to right place without manual intervention |
| **Human Control** | Personal decisions stay human-controlled |
| **Transparency** | Confidence scores show how sure the skill is |
| **Integration Ready** | Works with all existing Bronze/Silver skills |
| **Gold-Level Autonomy** | System thinks strategically about classification |

---

## Next Level: Scheduled Runs

Want it to run automatically? Set up PM2:

```bash
# Run every 30 minutes
pm2 start skills/cross_domain_integrator.py \
  --name cross_domain_integrator \
  --interpreter python3

# Or with cron schedule (every 30 minutes)
pm2 start "python3 skills/cross_domain_integrator.py" \
  --name cross_domain \
  --cron "*/30 * * * *"

# View logs
pm2 logs cross_domain_integrator
```

---

## Questions?

See detailed documentation:
- **Full Skill Docs**: `SKILL_CROSS_DOMAIN_INTEGRATOR.md`
- **Manifest**: `SKILLS_MANIFEST.md` (Gold Tier section)
- **How to Run**: `HOW_TO_RUN_PROJECT.md` (Gold Tier)

---

**Status**: ✅ Ready to Deploy
**Tier**: Gold ⭐⭐⭐
**Last Updated**: 2026-03-16
