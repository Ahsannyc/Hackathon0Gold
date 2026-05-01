#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facebook Messenger Watcher - ROBUST VERSION
Uses persistent context with better stealth and error handling
"""

import os
import sys
import time
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

Path("watchers/logs").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("watchers/logs/facebook_watcher_robust.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FacebookWatcherRobust:
    """Facebook Watcher - Robust Persistent Context"""
    KEYWORDS = ['sales', 'client', 'project', 'urgent', 'invoice', 'payment', 'deal', 'opportunity', 'partnership', 'lead', 'inquiry']
    CHECK_INTERVAL = 60
    NEEDS_ACTION_DIR = Path("Needs_Action")
    SESSION_PATH = Path("session/facebook_robust")

    def __init__(self):
        self.processed_messages = set()
        self.playwright = None
        self.browser = None
        self.page = None

    def ensure_dirs(self):
        """Ensure directories exist"""
        self.NEEDS_ACTION_DIR.mkdir(parents=True, exist_ok=True)
        self.SESSION_PATH.mkdir(parents=True, exist_ok=True)
        logger.info("[OK] Directories ready")

    def launch_browser(self):
        """Launch persistent browser context with stealth"""
        logger.info("[BROWSER] Launching with persistent context (stealth mode)...")

        try:
            self.playwright = sync_playwright().start()

            self.browser = self.playwright.chromium.launch_persistent_context(
                str(self.SESSION_PATH.absolute()),
                headless=False,  # Show window for interactive use
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-extensions',
                    '--disable-sync',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                ],
                ignore_https_errors=True,
                locale='en-US',
                timezone_id='America/New_York',
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )

            self.page = self.browser.new_page()
            logger.info("[OK] Browser context created")
            return True

        except Exception as e:
            logger.error(f"[ERROR] Failed to launch browser: {e}")
            self.cleanup()
            return False

    def monitor_facebook(self):
        """Main monitoring loop"""
        logger.info("[START] Facebook Watcher (Robust) starting...")
        self.ensure_dirs()

        failure_count = 0
        max_failures = 3

        while True:
            try:
                # Launch browser if not running
                if not self.page or not self.browser:
                    if not self.launch_browser():
                        time.sleep(10)
                        continue

                logger.info("[CHECK] Scanning Facebook Messenger...")
                found = self._check_facebook()

                if found:
                    logger.info(f"[FOUND] {found} new messages")
                else:
                    logger.info("[NO_NEW] No new messages")

                failure_count = 0
                time.sleep(self.CHECK_INTERVAL)

            except Exception as e:
                failure_count += 1
                logger.error(f"[ERROR] Check failed ({failure_count}/{max_failures}): {e}")
                self.cleanup()

                if failure_count >= max_failures:
                    logger.error("[RESTART] Too many failures, restarting...")
                    failure_count = 0
                    time.sleep(5)

    def _check_facebook(self) -> int:
        """Check for new messages"""
        try:
            logger.debug("[NAV] Navigating to messenger...")

            try:
                # Try with longer timeout and relaxed wait condition
                self.page.goto(
                    "https://www.facebook.com/messages/t/",
                    timeout=30000,
                    wait_until="domcontentloaded"  # Less strict than load
                )
            except Exception as nav_err:
                logger.warning(f"[WARN] Navigation warning: {nav_err}, trying alternate...")
                try:
                    self.page.goto("https://www.facebook.com/messages/", timeout=30000)
                except:
                    logger.error("[ERROR] Could not navigate to Facebook")
                    return 0

            time.sleep(2)

            # Try to get page content
            try:
                page_text = self.page.inner_text("body")
                logger.debug(f"[PAGE] Got {len(page_text)} chars of text")

                if "sign in" in page_text.lower() or "log in" in page_text.lower():
                    logger.warning("[AUTH] Page shows login required - session expired?")
                    return 0

            except Exception as e:
                logger.debug(f"[INFO] Could not read page text: {e}")

            # Try multiple message selectors
            messages_found = 0
            selectors = [
                '[data-testid*="message"]',
                '[role="main"] [data-testid*="message"]',
                '.x5jyip7',
                'div[class*="message"]',
            ]

            for selector in selectors:
                try:
                    elements = self.page.query_selector_all(selector)
                    logger.debug(f"[DOM] Selector '{selector}': {len(elements)} elements")

                    for elem in elements:
                        try:
                            text = elem.inner_text()
                            if text and any(kw.lower() in text.lower() for kw in self.KEYWORDS):
                                msg_hash = hashlib.md5(text.encode()).hexdigest()[:8]
                                if msg_hash not in self.processed_messages:
                                    self.processed_messages.add(msg_hash)
                                    self._save_message(text)
                                    messages_found += 1
                                    logger.info(f"[CAPTURED] {text[:40]}...")
                        except:
                            pass

                except Exception as e:
                    logger.debug(f"[SKIP] Selector error: {e}")

            return messages_found

        except Exception as e:
            logger.error(f"[ERROR] Check failed: {e}")
            return 0

    def _save_message(self, content: str):
        """Save captured message"""
        try:
            ts = datetime.now().isoformat().replace(':', '').replace('-', '')[:14]
            msg_id = hashlib.md5(content.encode()).hexdigest()[:8]
            filename = self.NEEDS_ACTION_DIR / f"facebook_{ts}_{msg_id}_message.md"

            message_content = f"""---
source: facebook
timestamp: {datetime.now().isoformat()}
keywords: {[kw for kw in self.KEYWORDS if kw.lower() in content.lower()]}
priority: medium
---

{content}
"""
            filename.write_text(message_content, encoding='utf-8')
            logger.info(f"[SAVED] {filename.name}")

        except Exception as e:
            logger.error(f"[SAVE_ERROR] {e}")

    def cleanup(self):
        """Clean shutdown"""
        try:
            if self.page:
                self.page.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except:
            pass
        self.page = None
        self.browser = None
        self.playwright = None


def main():
    """Main entry point"""
    try:
        watcher = FacebookWatcherRobust()
        watcher.monitor_facebook()
    except KeyboardInterrupt:
        logger.info("[STOP] Stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"[FATAL] {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
