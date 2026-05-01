#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter (X) Watcher - GOLD TIER
Monitors Twitter DMs, notifications, and mentions
Captures messages with business keywords
Uses Playwright for persistent browser automation
"""

import os
import sys
import time
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright

# Import error recovery
from watchers.error_recovery import WatcherErrorRecovery

Path("watchers/logs").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("watchers/logs/twitter_watcher.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TwitterWatcher:
    """Twitter (X) Watcher - Gold Tier"""

    KEYWORDS = ['sales', 'client', 'project', 'urgent', 'invoice', 'payment', 'deal', 'opportunity', 'partnership', 'lead', 'inquiry']
    CHECK_INTERVAL = 60
    NEEDS_ACTION_DIR = Path("Needs_Action")
    SESSION_PATH = Path("session/twitter")

    def __init__(self, project_root: str = "."):
        self.processed_messages = set()
        self.playwright = None
        self.browser = None
        self.page = None
        self.consecutive_failures = 0
        self.recovery = WatcherErrorRecovery("twitter_watcher", project_root)

    def ensure_dirs(self):
        """Ensure required directories exist"""
        self.NEEDS_ACTION_DIR.mkdir(parents=True, exist_ok=True)
        self.SESSION_PATH.mkdir(parents=True, exist_ok=True)
        logger.info("[OK] Directories ready")

    def launch_browser(self):
        """Launch Playwright browser with persistent context"""
        logger.info("[BROWSER] Launching Playwright Chromium...")

        try:
            self.playwright = sync_playwright().start()

            # Use persistent context for session persistence
            self.browser = self.playwright.chromium.launch(
                headless=False,  # Visible window for login
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-extensions',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                ]
            )

            # Create context with anti-detection
            context = self.browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )

            # Inject anti-detection script
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => false});
                window.chrome = {runtime: {}};
            """)

            self.page = context.new_page()
            logger.info("[OK] Browser launched")
            return True

        except Exception as e:
            logger.error(f"[ERROR] Failed to launch browser: {e}")
            return False

    def login_and_monitor(self):
        """Navigate to Twitter and monitor DMs"""
        try:
            logger.info("[NAV] Navigating to Twitter...")
            self.page.goto("https://twitter.com/messages", wait_until="domcontentloaded", timeout=30000)
            time.sleep(5)

            # Check for login
            page_text = self.page.inner_text("body").lower()
            if "login" in page_text or "sign in" in page_text:
                logger.warning("[AUTH] Login required - please log in manually")
                logger.info("[WAIT] Waiting 120 seconds for login...")

                try:
                    self.page.wait_for_url("**/messages**", timeout=120000)
                    logger.info("[OK] Login successful!")
                    time.sleep(3)
                except:
                    logger.warning("[WARN] Login timeout - but continuing anyway")

            logger.info("[READY] Starting DM monitoring...")

            # Main monitoring loop
            cycle = 0
            retry_count = 0
            while True:
                cycle += 1
                logger.info(f"[CYCLE {cycle}] Checking for new messages...")

                try:
                    # Refresh Twitter DMs
                    self.page.goto("https://twitter.com/messages", wait_until="domcontentloaded", timeout=20000)
                    time.sleep(2)

                    # Extract messages
                    found = self._extract_messages()

                    logger.info(f"[RESULT] Found {found} new messages with keywords")
                    self.consecutive_failures = 0
                    retry_count = 0  # Reset on success

                except Exception as e:
                    logger.error(f"[ERROR] Check cycle failed: {e}")
                    self.recovery.log_error(e, context=f"cycle_{cycle}", retry_count=retry_count)
                    self.consecutive_failures += 1
                    retry_count += 1

                if self.consecutive_failures >= 3:
                    logger.error(f"[RESTART] Too many failures ({retry_count}), initiating recovery...")
                    retry_count = 0
                    self.consecutive_failures = 0
                    return True  # Signal that a restart is needed

                logger.info(f"[WAIT] Sleeping {self.CHECK_INTERVAL}s until next check...")
                time.sleep(self.CHECK_INTERVAL)

        except KeyboardInterrupt:
            logger.info("[STOP] Stopped by user")
            return False
        except Exception as e:
            logger.error(f"[ERROR] Fatal error: {e}", exc_info=True)
            self.recovery.log_error(e, context="login_and_monitor", retry_count=retry_count)
            return True  # Signal restart needed
        finally:
            self.cleanup()

    def _extract_messages(self) -> int:
        """Extract Twitter DM messages with keywords"""
        messages_found = 0

        try:
            # Multiple selector strategies for Twitter DMs
            selectors = [
                '[data-testid*="message"]',
                '[role="article"]',
                'div[class*="message"]',
                'div[class*="dm"]',
            ]

            found_elements = set()

            for selector in selectors:
                try:
                    elements = self.page.query_selector_all(selector)
                    logger.debug(f"[DOM] Selector '{selector}': {len(elements)} elements")

                    for elem in elements:
                        try:
                            text = elem.inner_text()
                            if text and len(text) > 3:
                                # Avoid duplicates
                                elem_id = hashlib.md5(text.encode()).hexdigest()[:8]
                                if elem_id not in found_elements:
                                    found_elements.add(elem_id)

                                    # Check for keywords
                                    keywords_found = [kw for kw in self.KEYWORDS if kw.lower() in text.lower()]

                                    if keywords_found:
                                        msg_hash = hashlib.md5(text.encode()).hexdigest()[:16]
                                        if msg_hash not in self.processed_messages:
                                            self.processed_messages.add(msg_hash)
                                            self._save_message(text, keywords_found)
                                            messages_found += 1
                                            logger.info(f"[CAPTURED] {keywords_found}: {text[:60]}...")
                        except:
                            pass

                except Exception as e:
                    logger.debug(f"[SKIP] Selector error: {e}")

        except Exception as e:
            logger.error(f"[ERROR] Message extraction failed: {e}")

        return messages_found

    def _save_message(self, content: str, keywords: List[str]):
        """Save captured message"""
        try:
            ts = datetime.now().isoformat().replace(':', '').replace('-', '')[:14]
            msg_id = hashlib.md5(content.encode()).hexdigest()[:8]
            filename = self.NEEDS_ACTION_DIR / f"twitter_{ts}_{msg_id}_message.md"

            message_content = f"""---
source: twitter
timestamp: {datetime.now().isoformat()}
keywords_found: {keywords}
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
            logger.info("[OK] Browser closed")
        except:
            pass

    def run(self):
        """Main entry point - iterative restart loop (not recursive)"""
        self.ensure_dirs()
        restart_count = 0
        max_consecutive_restarts = 3

        while True:
            try:
                if not self.launch_browser():
                    logger.error("[FATAL] Could not launch browser")
                    time.sleep(60)
                    restart_count += 1
                    if restart_count >= max_consecutive_restarts:
                        logger.error("[FATAL] Max restart attempts reached")
                        break
                    continue

                restart_count = 0  # Reset restart counter on successful launch

                # Monitor until restart needed
                needs_restart = self.login_and_monitor()
                if not needs_restart:
                    # User interrupted or fatal error
                    break

                # Restart needed - reset and try again
                logger.info("[RESTART] Restarting after failure...")
                restart_count += 1
                time.sleep(10)  # Wait before restart

                if restart_count >= max_consecutive_restarts:
                    logger.warning(f"[PAUSE] {max_consecutive_restarts} restarts in a row, pausing 60s...")
                    restart_count = 0
                    time.sleep(60)

            except KeyboardInterrupt:
                logger.info("[STOP] Stopped by user")
                break
            except Exception as e:
                logger.error(f"[ERROR] Unexpected error in main loop: {e}", exc_info=True)
                self.recovery.log_error(e, context="main_run_loop", retry_count=restart_count)
                restart_count += 1
                time.sleep(30)

        self.cleanup()


def main():
    """Main entry point"""
    try:
        watcher = TwitterWatcher()
        watcher.run()
    except KeyboardInterrupt:
        logger.info("[STOP] Stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"[FATAL] {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
