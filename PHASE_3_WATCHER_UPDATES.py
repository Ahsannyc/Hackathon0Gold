#!/usr/bin/env python3
"""
PHASE 3 WATCHER UPDATES - Error Recovery Integration
Instructions for updating the remaining 4 watchers

Each watcher needs these changes:
1. Add import: from watchers.error_recovery import WatcherErrorRecovery
2. Add to __init__: self.recovery = WatcherErrorRecovery("watcher_name", project_root)
3. Replace cycle exception handler with exponential backoff + error logging
4. Add error logging calls for significant failures

Template for each watcher's run() or main loop:
"""

TEMPLATE = '''
# BEFORE (Old cycle exception handler):
except Exception as e:
    logger.error(f"[ERROR] Cycle failed: {e}")
    self.consecutive_failures += 1

# AFTER (With error recovery):
except Exception as e:
    retry_count += 1
    logger.error(f"[ERROR] Cycle {cycle} failed (retry {retry_count}/3): {e}")
    self.recovery.log_error(e, context=f"cycle_{cycle}", retry_count=retry_count)

    if self.recovery.should_retry(retry_count):
        delay = self.recovery.get_delay(retry_count)
        logger.warning(f"Retry {retry_count}/3 in {delay}s")
        time.sleep(delay)
        continue
    else:
        logger.error("Max retries reached, resetting...")
        retry_count = 0
        self.consecutive_failures = 0
        # Reset connection/state here
else:
    retry_count = 0  # Reset on success
'''

WATCHERS_TO_UPDATE = {
    "gmail_watcher.py": {
        "class": "GmailWatcher",
        "already_has_backoff": True,
        "note": "Already has 1.5x exponential backoff, just add recovery.log_error() calls",
        "changes": [
            "1. Add import: from watchers.error_recovery import WatcherErrorRecovery",
            "2. Add to __init__: self.recovery = WatcherErrorRecovery('gmail', project_root)",
            "3. In get_unread_emails() exception handler: call self.recovery.log_error(e, ...)",
            "4. In run() cycle exception handler: call self.recovery.log_error(e, ...)"
        ]
    },
    "whatsapp_persistent.py": {
        "class": "WhatsAppPersistentWatcher",
        "already_has_backoff": False,
        "note": "Add exponential backoff to cycle exception handler",
        "changes": [
            "1. Add import: from watchers.error_recovery import WatcherErrorRecovery",
            "2. Add to __init__: self.recovery = WatcherErrorRecovery('whatsapp_persistent', project_root)",
            "3. Add retry_count = 0 before main loop",
            "4. Replace cycle exception handler with template above",
            "5. Add else: retry_count = 0 after except block"
        ]
    },
    "linkedin_persistent.py": {
        "class": "LinkedInPersistentWatcher",
        "already_has_backoff": False,
        "note": "Same as WhatsApp - add exponential backoff pattern",
        "changes": [
            "1. Add import: from watchers.error_recovery import WatcherErrorRecovery",
            "2. Add to __init__: self.recovery = WatcherErrorRecovery('linkedin_persistent', project_root)",
            "3. Add retry_count = 0 before main loop",
            "4. Replace cycle exception handler with template above",
            "5. Add else: retry_count = 0 after except block"
        ]
    },
    "instagram_watcher_only.py": {
        "class": "InstagramWatcherOnly",
        "already_has_backoff": False,
        "note": "Add backoff to both launch retry and cycle exception handler",
        "changes": [
            "1. Add import: from watchers.error_recovery import WatcherErrorRecovery",
            "2. Add to __init__: self.recovery = WatcherErrorRecovery('instagram_watcher_only', project_root)",
            "3. In launch_browser() retry loop: use recovery.get_delay() instead of fixed 10s * retry_count",
            "4. In main cycle: add exponential backoff with template above"
        ]
    }
}

print("=" * 80)
print("PHASE 3 WATCHER UPDATES - Instructions")
print("=" * 80)
print()

for watcher_file, details in WATCHERS_TO_UPDATE.items():
    print(f"\n{'#'*80}")
    print(f"FILE: {watcher_file}")
    print(f"{'#'*80}")
    print(f"Class: {details['class']}")
    print(f"Already has backoff: {details['already_has_backoff']}")
    print(f"Note: {details['note']}")
    print("\nChanges needed:")
    for i, change in enumerate(details['changes'], 1):
        print(f"  {i}. {change}")

print("\n" + "=" * 80)
print("STANDARD PATTERN TO APPLY TO ALL")
print("=" * 80)
print(TEMPLATE)

print("\n" + "=" * 80)
print("COMPLETION CHECKLIST")
print("=" * 80)
print("""
After updating all 4 watchers, verify:

[ ] gmail_watcher.py imports WatcherErrorRecovery
[ ] whatsapp_persistent.py has exponential backoff + error logging
[ ] linkedin_persistent.py has exponential backoff + error logging
[ ] instagram_watcher_only.py has exponential backoff + error logging

Test all watchers:
  pm2 logs gmail-watcher | grep error
  pm2 logs whatsapp-watcher | grep RETRY
  pm2 logs linkedin-watcher | grep RETRY
  pm2 logs instagram-watcher | grep RETRY

Check error logs created:
  ls Logs/error_*
  cat Logs/error_*.log
""")
