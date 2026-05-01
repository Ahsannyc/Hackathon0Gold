#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facebook Messenger Watcher - FIXED HEADLESS VERSION
Simplified version that runs in headless mode without persistent context
This avoids browser crashes on Windows systems
"""

import os
import sys
import time
import logging
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# UTF-8 encoding support for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Create logs directory
Path("watchers/logs").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("watchers/logs/facebook_watcher_fixed.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FacebookWatcherFixed:
    """
    Simplified Facebook Watcher - Headless Only
    Avoids persistent context issues by using standard headless browser
    """
    KEYWORDS = ['sales', 'client', 'project', 'urgent', 'invoice', 'payment', 'deal', 'opportunity', 'partnership', 'lead', 'inquiry']
    CHECK_INTERVAL = 60  # Check every 60 seconds
    NEEDS_ACTION_DIR = Path("Needs_Action")

    def __init__(self):
        self.processed_messages = set()
        self.consecutive_failures = 0

    def ensure_dirs(self):
        """Ensure required directories exist"""
        self.NEEDS_ACTION_DIR.mkdir(parents=True, exist_ok=True)
        logger.info("[OK] Directories ready")

    def monitor_facebook(self):
        """Monitor Facebook for messages - main loop"""
        logger.info("[START] Facebook Watcher (Headless Fixed) starting...")
        self.ensure_dirs()

        failure_count = 0
        max_failures = 3

        while True:
            try:
                logger.info("[CHECK] Scanning Facebook Messenger...")
                found_messages = self._check_facebook_messages()

                if found_messages:
                    logger.info(f"[FOUND] {found_messages} new messages captured")
                else:
                    logger.info("[NO_NEW] No new business messages")

                failure_count = 0
                time.sleep(self.CHECK_INTERVAL)

            except Exception as e:
                failure_count += 1
                logger.error(f"[ERROR] Check failed ({failure_count}/{max_failures}): {e}")

                if failure_count >= max_failures:
                    logger.error("[FATAL] Too many consecutive failures, restarting...")
                    failure_count = 0
                    time.sleep(5)
                else:
                    time.sleep(self.CHECK_INTERVAL)

    def _check_facebook_messages(self) -> int:
        """Check Facebook for new messages (headless)"""
        playwright = None
        browser = None
        messages_found = 0

        try:
            playwright = sync_playwright().start()

            # Launch in headless mode - much more reliable
            logger.debug("[BROWSER] Launching Chromium in headless mode...")
            browser = playwright.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                ]
            )

            context = browser.new_context(
                # Use minimal context setup
                ignore_https_errors=True,
            )
            page = context.new_page()

            logger.debug("[NAV] Navigating to Facebook Messenger...")
            try:
                page.goto("https://www.facebook.com/messages/t/", timeout=20000)
            except PlaywrightTimeoutError:
                logger.warning("[TIMEOUT] Navigation timeout, attempting anyway...")
                try:
                    page.goto("https://www.facebook.com/messages/")
                except:
                    pass

            time.sleep(3)

            # Try to extract messages from the page
            try:
                # Look for message elements
                messages = page.query_selector_all('[data-testid*="message"]')
                logger.debug(f"[DOM] Found {len(messages)} message elements")

                for msg_element in messages:
                    try:
                        msg_text = msg_element.inner_text()
                        msg_time = datetime.now().isoformat()

                        # Check for keywords
                        if any(kw.lower() in msg_text.lower() for kw in self.KEYWORDS):
                            msg_hash = hashlib.md5(msg_text.encode()).hexdigest()[:8]

                            if msg_hash not in self.processed_messages:
                                self.processed_messages.add(msg_hash)
                                self._save_message(msg_text, msg_time, msg_hash)
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
        """Save captured message to Needs_Action folder"""
        try:
            filename = self.NEEDS_ACTION_DIR / f"facebook_{timestamp.replace(':', '').replace('-', '')[:14]}_{msg_id}_message.md"

            message_content = f"""---
source: facebook
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
        watcher = FacebookWatcherFixed()
        watcher.monitor_facebook()
    except KeyboardInterrupt:
        logger.info("[STOP] Watcher stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"[FATAL] Unhandled error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
