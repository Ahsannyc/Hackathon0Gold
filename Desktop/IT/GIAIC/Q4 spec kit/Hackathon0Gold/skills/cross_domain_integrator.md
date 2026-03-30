# Cross Domain Integrator - Gold Tier Skill

**Status**: ✅ Production Ready
**Tier**: Gold ⭐⭐⭐
**Type**: Agent Skill
**Created**: 2026-03-16
**Last Updated**: 2026-03-18

---

## Overview

The **Cross Domain Integrator** is a Gold Tier skill that unifies personal and business domain workflows into a single coherent intelligence system.

## What It Does

1. **Scans** `/Needs_Action/` for all incoming messages
2. **Classifies** each message as PERSONAL or BUSINESS
3. **Routes** items to appropriate handlers:
   - PERSONAL → `/Pending_Approval/` (HITL approval needed)
   - BUSINESS → `/Approved/` (Auto LinkedIn Poster processes)
4. **Creates** unified summary in `/Logs/cross_domain_[date].md`
5. **Logs** all decisions with confidence scores

## Classification Rules

### PERSONAL Domain
- **Sources**: Email, WhatsApp
- **Keywords**: personal, family, friend, home, health, appointment, birthday
- **Action**: Routes to `/Pending_Approval/` for human decision

### BUSINESS Domain
- **Sources**: LinkedIn, Twitter, Facebook
- **Keywords**: sales, client, project, invoice, payment, deal, opportunity, partnership
- **Action**: Routes to `/Approved/` for Auto LinkedIn Poster

## Usage

### Command Line
```bash
python skills/cross_domain_integrator.py
```

### Wrapper Scripts
```bash
run-cross-domain.bat          # Windows
run-cross-domain.ps1          # PowerShell
run-cross-domain.sh           # Bash
```

### Scheduled (Auto-Running)
```bash
pm2 logs cross_domain_integrator -f
```

### In Claude Code
```
@cross
```

## Output Files

- **Summary**: `/Logs/cross_domain_[date].md`
- **Personal Items**: `/Pending_Approval/*.md`
- **Business Items**: `/Approved/*.md`
- **Logs**: `skills/logs/cross_domain_integrator.log`

## Integration

Works with:
- ✅ Task Analyzer (Bronze)
- ✅ HITL Approval Handler (Silver)
- ✅ Auto LinkedIn Poster (Silver)
- ✅ Daily Briefing (Silver)

## Examples

### Input (Needs_Action/)
```
email_001.md - "family dinner this Sunday"
linkedin_001.md - "sales opportunity - $100K enterprise deal"
whatsapp_001.md - "project meeting at 3pm"
```

### Output After Classification
```
/Pending_Approval/
├── email_001.md          (95% confidence - PERSONAL)
└── whatsapp_001.md       (92% confidence - BUSINESS: "project")

/Approved/
└── linkedin_001.md       (98% confidence - BUSINESS)

/Logs/
└── cross_domain_2026-03-18.md (Complete summary)
```

## Files

- **Core**: `skills/cross_domain_integrator.py`
- **Scheduler**: `skills/cross_domain_scheduler.py`
- **Documentation**: `SKILL_CROSS_DOMAIN_INTEGRATOR.md`
- **Manifest**: `SKILLS_MANIFEST.md`

## Automation

**Runs automatically every 30 minutes via PM2:**
```bash
pm2 list                          # Status
pm2 logs cross_domain_integrator  # View logs
pm2 restart cross_domain_integrator # Restart
```

---

**Ready to use!** 🚀
