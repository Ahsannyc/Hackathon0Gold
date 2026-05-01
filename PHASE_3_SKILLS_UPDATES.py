#!/usr/bin/env python3
"""
PHASE 3 SKILLS UPDATES - Error Handler Integration
Instructions for updating all 10 skills with error recovery

Each skill needs:
1. Import: from skills.error_handler import SkillErrorHandler
2. Instantiate in __init__ or at function start: self.error_handler = SkillErrorHandler("skill_name", project_root)
3. Wrap core logic in try/except
4. On exception: call error_handler.write_error(e, context=...)
5. On MCP/API fail: call error_handler.write_manual_fallback(description, context=...)
"""

SKILLS_UPDATE_PLAN = {
    1: {
        "file": "basic_file_handler.py",
        "issue": "Zero error handling - will crash on file not found",
        "priority": "HIGH",
        "changes": [
            "Add: from skills.error_handler import SkillErrorHandler",
            "Add to __init__: self.error_handler = SkillErrorHandler('basic_file_handler', '.')",
            "Wrap read_handbook_rules() in try/except",
            "Wrap list_md_files() in try/except",
            "Wrap summarize_file() in try/except",
            "Wrap move_to_done() in try/except",
            "On exception: error_handler.write_error(e, context='operation_name')"
        ]
    },
    2: {
        "file": "task_analyzer.py",
        "issue": "bare 'except: pass' silently swallows errors",
        "priority": "HIGH",
        "changes": [
            "Add: from skills.error_handler import SkillErrorHandler",
            "Add to __init__: self.error_handler = SkillErrorHandler('task_analyzer', '.')",
            "Replace bare 'except: pass' with proper exception logging",
            "In execute(): wrap file operations in try/except",
            "Call error_handler.write_error() on failures"
        ]
    },
    3: {
        "file": "auto_linkedin_poster.py",
        "issue": "Already has good try/except, needs error file + manual fallback",
        "priority": "MEDIUM",
        "changes": [
            "Add: from skills.error_handler import SkillErrorHandler",
            "Already instantiated via logger, add error_handler too",
            "In process_leads(): add error_handler.write_error() calls",
            "On lead processing fail: error_handler.write_manual_fallback('Draft LinkedIn post manually', {'file': lead_file})",
            "On MCP call fail: write_manual_fallback()"
        ]
    },
    4: {
        "file": "hitl_approval_handler.py",
        "issue": "Already has good try/except, just needs error file logging",
        "priority": "MEDIUM",
        "changes": [
            "Add: from skills.error_handler import SkillErrorHandler",
            "In __init__: add self.error_handler = SkillErrorHandler('hitl_approval_handler', '.')",
            "In catch blocks: add error_handler.write_error(e, context=...)",
            "Log all execution attempts to error file for audit trail"
        ]
    },
    5: {
        "file": "gmail_label_organizer.py",
        "issue": "Uses print() only, no logging or error tracking",
        "priority": "MEDIUM",
        "changes": [
            "Add: from skills.error_handler import SkillErrorHandler",
            "In __init__: add self.error_handler = SkillErrorHandler('gmail_label_organizer', '.')",
            "In organize_by_sender(): add try/except",
            "On error: error_handler.write_error(e, context='gmail_operation')",
            "On auth fail: write_manual_fallback('Re-authenticate to Gmail')"
        ]
    },
    6: {
        "file": "cross_domain_scheduler.py",
        "issue": "Basic handling, subprocess errors not logged to /Errors/",
        "priority": "LOW",
        "changes": [
            "Add: from skills.error_handler import SkillErrorHandler",
            "Add to module level: error_handler = SkillErrorHandler('cross_domain_scheduler', '.')",
            "In run_integrator() exception handler: error_handler.write_error(e, context='subprocess')",
            "On timeout: error_handler.write_manual_fallback('Run cross_domain_integrator manually')"
        ]
    },
    7: {
        "file": "cross_domain_integrator.py",
        "issue": "Silent bare 'except:' on YAML parse - errors disappear",
        "priority": "HIGH",
        "changes": [
            "Add: from skills.error_handler import SkillErrorHandler",
            "Add to __init__: self.error_handler = SkillErrorHandler('cross_domain_integrator', '.')",
            "Replace bare 'except:' with proper exception catching and logging",
            "In execute(): add error_handler.write_error() on parse/io failures",
            "On routing fail: write_manual_fallback('Manually route message')"
        ]
    },
    8: {
        "file": "social_summary_generator.py",
        "issue": "Already has good try/except, needs error file + manual fallback",
        "priority": "MEDIUM",
        "changes": [
            "Add: from skills.error_handler import SkillErrorHandler",
            "In __init__: add self.error_handler = SkillErrorHandler('social_summary_generator', '.')",
            "In process_messages(): add error_handler.write_error() calls",
            "On draft generation fail: write_manual_fallback('Draft response manually', {'platform': 'facebook/instagram', 'message': content})",
            "On MCP fail: write_manual_fallback()"
        ]
    },
    9: {
        "file": "twitter_post_generator.py",
        "issue": "Already has good try/except, needs error file + manual fallback",
        "priority": "MEDIUM",
        "changes": [
            "Add: from skills.error_handler import SkillErrorHandler",
            "In __init__: add self.error_handler = SkillErrorHandler('twitter_post_generator', '.')",
            "In process_messages(): add error_handler.write_error() calls",
            "On draft fail: write_manual_fallback('Draft Twitter reply manually', {'dm_content': content})",
            "On MCP fail: write_manual_fallback()"
        ]
    },
    10: {
        "file": "weekly_audit_briefer.py",
        "issue": "Re-raises exceptions, stops on first error - needs graceful continue",
        "priority": "MEDIUM",
        "changes": [
            "Add: from skills.error_handler import SkillErrorHandler",
            "In __init__: add self.error_handler = SkillErrorHandler('weekly_audit_briefer', '.')",
            "In generate_briefing(): wrap each item extraction in try/except",
            "On extraction fail: error_handler.write_error(e, context='item_extraction')",
            "On MCP fail: write_manual_fallback('Review metrics manually')",
            "Generate partial briefing even if some sections fail"
        ]
    }
}

print("=" * 100)
print("PHASE 3 SKILLS UPDATES - All 10 Skills Error Recovery Integration")
print("=" * 100)
print()

# Print by priority
for priority in ["HIGH", "MEDIUM", "LOW"]:
    print(f"\n{'#' * 100}")
    print(f"PRIORITY: {priority}")
    print(f"{'#' * 100}\n")

    for num, details in sorted(SKILLS_UPDATE_PLAN.items()):
        if details['priority'] == priority:
            print(f"{num:2d}. {details['file']:<40s} | Issue: {details['issue']}")
            for change in details['changes']:
                print(f"    → {change}")
            print()

print("\n" + "=" * 100)
print("STANDARD ERROR HANDLER PATTERN")
print("=" * 100)

PATTERN = '''
# At top of file:
from skills.error_handler import SkillErrorHandler

# In __init__:
self.error_handler = SkillErrorHandler("skill_name", project_root)

# In core logic (try/except):
try:
    # Do work
    result = api_call()
except Exception as e:
    # Log error to /Errors/
    self.error_handler.write_error(
        e,
        context="api_call_failed",
        extra={"data": str(data)},
        severity="error"
    )

    # If it's an external API/MCP failure, create manual fallback
    if isinstance(e, (ConnectionError, TimeoutError)):
        self.error_handler.write_manual_fallback(
            "Complete this action manually in /Needs_Action/",
            context={"source_file": filename, "action": "process_message"}
        )

    # Continue processing instead of crashing
    continue
'''

print(PATTERN)

print("\n" + "=" * 100)
print("COMPLETION CHECKLIST")
print("=" * 100)

checklist = """
Update Priority (HIGH - do first):
  [ ] basic_file_handler.py - Add full error handling
  [ ] task_analyzer.py - Fix bare except: pass
  [ ] cross_domain_integrator.py - Fix silent bare except

Update Priority (MEDIUM - next):
  [ ] auto_linkedin_poster.py - Add error file + manual fallback
  [ ] hitl_approval_handler.py - Add error file logging
  [ ] gmail_label_organizer.py - Add logging + error tracking
  [ ] social_summary_generator.py - Add error file + manual fallback
  [ ] twitter_post_generator.py - Add error file + manual fallback
  [ ] weekly_audit_briefer.py - Add error tracking + graceful continue

Update Priority (LOW - last):
  [ ] cross_domain_scheduler.py - Log subprocess errors to /Errors/

Verification:
  [ ] All skills import SkillErrorHandler
  [ ] All skills instantiate error_handler in __init__
  [ ] All core logic wrapped in try/except
  [ ] All exceptions logged to error_handler.write_error()
  [ ] All MCP/API failures create manual fallback
  [ ] No bare 'except: pass' remaining
  [ ] /Errors/ and /Plans/ directories created on first error

Test all skills:
  python skills/basic_file_handler.py           # Check error logging
  python skills/task_analyzer.py                # Check error logging
  python skills/auto_linkedin_poster.py         # Check manual fallback
  python skills/weekly_audit_briefer.py         # Check partial output on error

Check error files:
  ls Errors/ Plans/
  cat Errors/skill_error_*.md
  cat Plans/manual_*_*.md
"""

print(checklist)

print("\n" + "=" * 100)
print("SUMMARY: 10 SKILLS → 100% ERROR RECOVERY COVERAGE")
print("=" * 100)
print("""
After completion:
- All 6 watchers: Exponential backoff + error logging ✓
- All 10 skills: Error tracking + manual fallback ✓
- /Logs/: All watcher errors recorded ✓
- /Errors/: All skill errors recorded ✓
- /Plans/: Manual fallback actions generated ✓

System resilience: 24/7 operation with graceful degradation
Observability: Complete error trail for debugging
Recovery: Automatic backoff + manual intervention capability
""")
