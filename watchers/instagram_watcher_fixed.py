#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram DM Watcher - FIXED HEADLESS VERSION
Simplified version that runs in headless mode without persistent context
"""

import os
import sys
import time
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

Path("watchers/logs").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("watchers/logs/instagram_watcher_fixed.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import error recovery
from watchers.error_recovery import WatcherErrorRecovery


class InstagramWatcherFixed:
    """Instagram DM Watcher - Headless Only"""
    KEYWORDS = ['sales', 'client', 'project', 'urgent', 'invoice', 'payment', 'deal', 'opportunity', 'partnership', 'lead', 'inquiry']
    CHECK_INTERVAL = 60
    NEEDS_ACTION_DIR = Path("Needs_Action")

    def __init__(self):
        self.processed_messages = set()
        self.consecutive_failures = 0
        self.recovery = WatcherErrorRecovery("instagram_watcher_fixed", ".")

    def ensure_dirs(self):
        """Ensure required directories exist"""
        self.NEEDS_ACTION_DIR.mkdir(parents=True, exist_ok=True)
        logger.info("[OK] Directories ready")

    def monitor_instagram(self):
        """Monitor Instagram DMs - main loop"""
        logger.info("[START] Instagram Watcher (Headless Fixed) starting...")
        self.ensure_dirs()

        failure_count = 0
        max_failures = 3

        while True:
            try:
                logger.info("[CHECK] Scanning Instagram DMs...")
                found_messages = self._check_instagram_dms()

                if found_messages:
                    logger.info(f"[FOUND] {found_messages} new messages captured")
                else:
                    logger.info("[NO_NEW] No new business messages")

                failure_count = 0
                time.sleep(self.CHECK_INTERVAL)

            except Exception as e:
                failure_count += 1
                logger.error(f"[ERROR] Check failed ({failure_count}/{max_failures}): {e}")
                # Log error to /Logs/
                self.recovery.log_error(e, context=f"check_failure_{failure_count}", retry_count=failure_count)

                if failure_count >= max_failures:
                    logger.error("[FATAL] Too many consecutive failures, restarting...")
                    failure_count = 0
                    time.sleep(5)
                else:
                    delay = self.recovery.get_delay(failure_count - 1)
                    logger.warning(f"[BACKOFF] Retry {failure_count}/{max_failures} in {delay:.1f}s...")
                    time.sleep(delay)

    def _check_instagram_dms(self) -> int:
        """Check Instagram DMs for new messages (headless)"""
        playwright = None
        browser = None
        messages_found = 0

        try:
            playwright = sync_playwright().start()

            logger.debug("[BROWSER] Launching Chromium in headless mode...")
            browser = playwright.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                ]
            )

            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()

            logger.debug("[NAV] Navigating to Instagram DMs...")
            try:
                page.goto("https://www.instagram.com/direct/", timeout=20000)
            except PlaywrightTimeoutError:
                logger.warning("[TIMEOUT] Navigation timeout, attempting alternate URL...")
                try:
                    page.goto("https://www.instagram.com/direct")
                except:
                    pass

            time.sleep(3)

            try:
                # Look for direct message elements
                messages = page.query_selector_all('[data-testid*="thread"]')
                logger.debug(f"[DOM] Found {len(messages)} DM thread elements")

                for msg_element in messages:
                    try:
                        msg_text = msg_element.inner_text()

                        if any(kw.lower() in msg_text.lower() for kw in self.KEYWORDS):
                            msg_hash = hashlib.md5(msg_text.encode()).hexdigest()[:8]

                            if msg_hash not in self.processed_messages:
                                self.processed_messages.add(msg_hash)
                                self._save_message(msg_text, datetime.now().isoformat(), msg_hash)
                                messages_found += 1
                                logger.info(f"[CAPTURED] Message: {msg_text[:50]}...")

                    except Exception as e:
                        logger.debug(f"[SKIP] Could not extract message: {e}")

            except Exception as e:
                logger.warning(f"[EXTRACT] Could not extract messages: {e}")

            context.close()

        except Exception as e:
            logger.error(f"[BROWSER_ERROR] {e}", exc_info=False)

        finally:
            if browser:
                try:
                    browser.close()
                except:
                    pass
            if playwright:
                try:
                    playwright.stop()
                except:
                    pass

        return messages_found

    def _save_message(self, content: str, timestamp: str, msg_id: str):
        """Save captured message"""
        try:
            filename = self.NEEDS_ACTION_DIR / f"instagram_{timestamp.replace(':', '').replace('-', '')[:14]}_{msg_id}_message.md"

            message_content = f"""---
source: instagram
timestamp: {timestamp}
keywords: {[kw for kw in self.KEYWORDS if kw.lower() in content.lower()]}
priority: medium
message_id: {msg_id}
---

{content}
"""
            filename.write_text(message_content, encoding='utf-8')
            logger.info(f"[SAVED] {filename.name}")

        except Exception as e:
            logger.error(f"[SAVE_ERROR] Failed to save message: {e}")


def main():
    """Main entry point"""
    try:
        watcher = InstagramWatcherFixed()
        watcher.monitor_instagram()
    except KeyboardInterrupt:
        logger.info("[STOP] Watcher stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"[FATAL] Unhandled error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
