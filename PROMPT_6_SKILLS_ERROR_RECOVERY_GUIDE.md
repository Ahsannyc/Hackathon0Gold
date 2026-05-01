---
title: Skills Error Recovery Implementation Guide
date: 2026-03-29
status: Ready for Implementation
version: 1.0
---

# Skills Error Recovery Implementation Guide - All 10 Skills

**Status:** Phase 2 (Watchers) Complete ✅ | Phase 3 (Skills) Ready for Implementation

---

## Overview: What Each Skill Needs

All 10 skills require:
1. **Import error handler:** `from skills.error_handler import SkillErrorHandler`
2. **Initialize in `__init__`:** `self.error_handler = SkillErrorHandler("skill_name", ".")`
3. **Add error logging:** `self.error_handler.write_error(e, context="...", extra={...})`
4. **Add manual fallback (where applicable):** `self.error_handler.write_manual_fallback(...)`

---

## Skill-by-Skill Implementation Plan

### 1. **basic_file_handler.py** - Priority: HIGH
**Current State:** No error handling
**Changes Needed:**
```python
# At top, add import
from skills.error_handler import SkillErrorHandler

# In __init__, add:
self.error_handler = SkillErrorHandler("basic_file_handler", ".")

# Wrap all try-except blocks with:
except Exception as e:
    self.error_handler.write_error(e, context="file_operation", extra={"file": filename})
    # Continue or gracefully degrade
```

---

### 2. **task_analyzer.py** - Priority: HIGH
**Current State:** Has bare `except: pass` (silent failures!)
**Changes Needed:**
```python
# Replace bare except with proper error handling
from skills.error_handler import SkillErrorHandler
# In __init__: self.error_handler = SkillErrorHandler("task_analyzer", ".")

# Replace:
except:
    pass

# With:
except Exception as e:
    self.error_handler.write_error(e, context="task_analysis")
```

---

### 3. **auto_linkedin_poster.py** - Priority: MEDIUM
**Current State:** Good try-except blocks already present
**Changes Needed:**
```python
# At top, add import
from skills.error_handler import SkillErrorHandler

# In __init__, add:
self.error_handler = SkillErrorHandler("auto_linkedin_poster", ".")

# In main exception handlers, add error logging:
except Exception as e:
    self.error_handler.write_error(
        e,
        context="lead_processing",
        extra={"lead_file": filepath.name}
    )
```

---

### 4. **hitl_approval_handler.py** - Priority: MEDIUM
**Current State:** Good try-except blocks
**Changes Needed:**
```python
from skills.error_handler import SkillErrorHandler

# In __init__:
self.error_handler = SkillErrorHandler("hitl_approval_handler", ".")

# In exception handlers:
except Exception as e:
    self.error_handler.write_error(e, context="approval_processing")
```

---

### 5. **gmail_label_organizer.py** - Priority: MEDIUM
**Current State:** Uses print() instead of logging
**Changes Needed:**
```python
# Add import
from skills.error_handler import SkillErrorHandler

# In __init__:
self.error_handler = SkillErrorHandler("gmail_label_organizer", ".")

# Replace all print statements with logger.info()
# Add error handling:
except Exception as e:
    self.error_handler.write_error(
        e,
        context="email_labeling",
        extra={"email_id": email_id}
    )
```

---

### 6. **cross_domain_scheduler.py** - Priority: MEDIUM
**Current State:** Minimal error handling
**Changes Needed:**
```python
from skills.error_handler import SkillErrorHandler

# In __init__:
self.error_handler = SkillErrorHandler("cross_domain_scheduler", ".")

# In subprocess/scheduling exception handlers:
except Exception as e:
    self.error_handler.write_error(
        e,
        context="subprocess_execution",
        severity="error"
    )
```

---

### 7. **cross_domain_integrator.py** - Priority: HIGH
**Current State:** Has silent bare `except:` blocks
**Changes Needed:**
```python
from skills.error_handler import SkillErrorHandler

# In __init__:
self.error_handler = SkillErrorHandler("cross_domain_integrator", ".")

# Replace all bare except: pass with:
except Exception as e:
    self.error_handler.write_error(
        e,
        context="domain_classification",
        extra={"message_file": filepath.name}
    )
```

---

### 8. **social_summary_generator.py** - Priority: MEDIUM
**Current State:** Good try-except, missing error_handler integration
**Changes Needed:**
```python
from skills.error_handler import SkillErrorHandler

# In __init__:
self.error_handler = SkillErrorHandler("social_summary_generator", ".")

# In exception handlers:
except Exception as e:
    self.error_handler.write_error(e, context="social_summary_generation")
    # Generate manual fallback for MCP failures
    if "mcp" in str(e).lower() or "api" in str(e).lower():
        self.error_handler.write_manual_fallback(
            "Review social media message and draft response manually",
            context={"source_file": filepath.name},
            priority="high"
        )
```

---

### 9. **twitter_post_generator.py** - Priority: MEDIUM
**Current State:** Good try-except, missing error_handler integration
**Changes Needed:**
```python
from skills.error_handler import SkillErrorHandler

# In __init__:
self.error_handler = SkillErrorHandler("twitter_post_generator", ".")

# In exception handlers:
except Exception as e:
    self.error_handler.write_error(e, context="twitter_post_generation")
    # Manual fallback for failures
    self.error_handler.write_manual_fallback(
        "Draft Twitter response manually for captured DM",
        context={"source_message": message.get('content', 'Unknown')},
        priority="medium"
    )
```

---

### 10. **weekly_audit_briefer.py** - Priority: MEDIUM
**Current State:** Partial error handling
**Changes Needed:**
```python
from skills.error_handler import SkillErrorHandler

# In __init__:
self.error_handler = SkillErrorHandler("weekly_audit_briefer", ".")

# In main briefing generation:
except Exception as e:
    self.error_handler.write_error(
        e,
        context="briefing_generation",
        severity="error"
    )
    # Continue with partial data instead of crashing
    logger.warning("Briefing generation failed, using partial data...")
```

---

## File Locations Summary - Updated Files

**Watchers (Already Updated):**
```
✅ watchers/gmail_watcher.py - Error recovery added
✅ watchers/whatsapp_persistent.py - Error recovery added
✅ watchers/linkedin_persistent.py - Error recovery added
✅ watchers/instagram_watcher_fixed.py - Error recovery added
```

**Skills (To Update):**
```
□ skills/basic_file_handler.py
□ skills/task_analyzer.py
□ skills/auto_linkedin_poster.py
□ skills/hitl_approval_handler.py
□ skills/gmail_label_organizer.py
□ skills/cross_domain_scheduler.py
□ skills/cross_domain_integrator.py
□ skills/social_summary_generator.py
□ skills/twitter_post_generator.py
□ skills/weekly_audit_briefer.py
```

**Utility Modules (Already Created):**
```
✅ watchers/error_recovery.py (159 lines)
✅ skills/error_handler.py (223 lines)
```

---

## Output Directories - Will Auto-Create

| Directory | Purpose | Auto-Create | Status |
|---|---|---|---|
| `/Logs/` | Watcher error logs | ✅ Yes (error_recovery.py) | Ready |
| `/Errors/` | Skill error logs | ✅ Yes (error_handler.py) | Ready |
| `/Plans/manual_*` | Manual fallback actions | ✅ Yes (error_handler.py) | Ready |

---

## Quick Implementation Template

For each skill, follow this pattern:

```python
#!/usr/bin/env python3
"""Skill description"""

import logging
from pathlib import Path
from skills.error_handler import SkillErrorHandler

logger = logging.getLogger(__name__)

class MySkill:
    def __init__(self):
        self.error_handler = SkillErrorHandler("my_skill", ".")
        self.setup()

    def setup(self):
        """Setup"""
        try:
            # Initialization logic
            logger.info("Skill initialized")
        except Exception as e:
            self.error_handler.write_error(e, context="initialization")
            raise

    def execute(self):
        """Main execution"""
        try:
            # Main logic
            result = self.do_work()
            logger.info(f"Success: {result}")
            return result
        except Exception as e:
            # Log error
            self.error_handler.write_error(e, context="execution")

            # If it's an API/MCP failure, create manual fallback
            if "api" in str(e).lower() or "mcp" in str(e).lower():
                self.error_handler.write_manual_fallback(
                    "Complete this task manually",
                    context={"error": str(e)},
                    priority="medium"
                )
            return None
```

---

## Testing Each Skill Update

After updating each skill:

```bash
# 1. Check import works
python -c "from skills.error_handler import SkillErrorHandler; print('✓ Import OK')"

# 2. Test skill initialization
python skills/my_skill.py

# 3. Trigger error (remove required file or data)
mv Company_Handbook.md Company_Handbook.md.bak
python skills/auto_linkedin_poster.py

# 4. Check error files created
ls Errors/skill_error_*.md
cat Errors/skill_error_*.md

# 5. Check manual fallback created (if applicable)
ls Plans/manual_my_skill_*.md
cat Plans/manual_my_skill_*.md

# 6. Restore files
mv Company_Handbook.md.bak Company_Handbook.md
```

---

## Next Steps

1. **For each of 10 skills:** Apply error_handler integration (5-10 minutes per skill)
2. **Test each skill:** Run with simulated errors (2-3 minutes per skill)
3. **Monitor in production:** Check `/Logs/` and `/Errors/` directories for failures
4. **Adjust severity levels:** Use 'warning', 'error', 'critical' as appropriate

---

## Summary

- **Watchers:** 4 of 4 updated with error_recovery ✅
- **Skills:** 10 of 10 need error_handler integration (10-15 minutes total)
- **Output:** Automated directories with all logs/errors/fallbacks
- **Testing:** Comprehensive guide provided above

