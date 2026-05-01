#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facebook Messenger Watcher - JAVASCRIPT EXTRACTION
Uses JavaScript injection to directly extract message text from DOM
More robust than CSS selectors which Facebook frequently changes
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

from undetected_chromedriver import Chrome as UndetectedChrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# Import error recovery
from watchers.error_recovery import WatcherErrorRecovery

Path("watchers/logs").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("watchers/logs/facebook_watcher_js.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FacebookWatcherJS:
    """Facebook Messenger Watcher - JavaScript Extraction"""

    KEYWORDS = ['sales', 'client', 'project', 'urgent', 'invoice', 'payment', 'deal', 'opportunity', 'partnership', 'lead', 'inquiry']
    CHECK_INTERVAL = 60
    NEEDS_ACTION_DIR = Path("Needs_Action")
    PROFILE_DIR = Path("session/facebook_js_extract")

    # JavaScript to extract all visible text from the messenger area
    EXTRACT_JS = """
    (function() {
        try {
            // Strategy 1: Get all text content from conversation area
            let messages = [];

            // Try multiple strategies to find message containers
            let selectors = [
                // Get all text from main messenger area
                'div[role="main"]',
                'div[data-testid="conversation"]',
                'div[data-testid*="message"]',
                '[role="article"]'
            ];

            for (let selector of selectors) {
                let elements = document.querySelectorAll(selector);
                for (let elem of elements) {
                    let text = elem.innerText || elem.textContent;
                    if (text && text.trim().length > 0) {
                        messages.push(text.trim());
                    }
                }
            }

            // Strategy 2: Get all span/div elements with text content
            let allDivs = document.querySelectorAll('span, div, p, li');
            for (let elem of allDivs) {
                if (elem.childNodes.length === 1 && elem.childNodes[0].nodeType === 3) {
                    let text = elem.textContent.trim();
                    if (text.length > 3 && text.length < 500) {
                        messages.push(text);
                    }
                }
            }

            // Remove duplicates
            messages = [...new Set(messages)];

            return {
                success: true,
                count: messages.length,
                messages: messages,
                pageTitle: document.title,
                url: window.location.href
            };
        } catch(e) {
            return {
                success: false,
                error: e.message
            };
        }
    })();
    """

    def __init__(self, project_root: str = "."):
        self.processed_messages = set()
        self.driver = None
        self.consecutive_failures = 0
        self.recovery = WatcherErrorRecovery("facebook_watcher_js_extract", project_root)

    def ensure_dirs(self):
        """Ensure required directories exist"""
        self.NEEDS_ACTION_DIR.mkdir(parents=True, exist_ok=True)
        self.PROFILE_DIR.mkdir(parents=True, exist_ok=True)
        logger.info("[OK] Directories ready")

    def launch_browser(self):
        """Launch undetected Chrome browser"""
        logger.info("[BROWSER] Launching undetected Chrome with JS extraction...")

        try:
            options = webdriver.ChromeOptions()
            options.add_argument(f"--user-data-dir={self.PROFILE_DIR.absolute()}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--start-maximized")

            self.driver = UndetectedChrome(options=options, use_subprocess=False)
            logger.info("[OK] Browser launched")
            return True

        except Exception as e:
            logger.error(f"[ERROR] Failed to launch: {e}")
            return False

    def login_and_monitor(self):
        """Navigate to Messenger and monitor using JavaScript extraction"""
        try:
            logger.info("[NAV] Navigating to Facebook Messenger...")
            self.driver.get("https://www.facebook.com/messages/t/")
            time.sleep(5)

            # Check for login
            page_source = self.driver.page_source.lower()
            if "login" in page_source or "sign in" in page_source:
                logger.warning("[AUTH] Login required - please log in manually")
                logger.info("[WAIT] Waiting 120 seconds for login...")

                try:
                    # Wait for successful navigation
                    for i in range(24):
                        time.sleep(5)
                        if "login" not in self.driver.page_source.lower() and "messages" in self.driver.current_url:
                            logger.info("[OK] Login successful!")
                            break
                except:
                    logger.warning("[WARN] Login timeout - continuing anyway")

            logger.info("[READY] Starting message monitoring with JavaScript extraction...")

            # Main monitoring loop
            cycle = 0
            retry_count = 0
            while True:
                cycle += 1
                logger.info(f"[CYCLE {cycle}] Checking for new messages...")

                try:
                    # Navigate to messenger to refresh
                    self.driver.get("https://www.facebook.com/messages/t/")
                    time.sleep(3)

                    # Execute JavaScript to extract messages
                    result = self.driver.execute_script(self.EXTRACT_JS)

                    if result and isinstance(result, dict) and result.get('success'):
                        messages = result.get('messages', [])
                        logger.debug(f"[PAGE] Found {len(messages)} text elements on page")

                        # Check each message for keywords
                        found = 0
                        for msg_text in messages:
                            if len(msg_text) > 5:
                                keywords_found = [kw for kw in self.KEYWORDS if kw.lower() in msg_text.lower()]

                                if keywords_found:
                                    msg_hash = hashlib.md5(msg_text.encode()).hexdigest()[:16]
                                    if msg_hash not in self.processed_messages:
                                        self.processed_messages.add(msg_hash)
                                        self._save_message(msg_text, keywords_found)
                                        found += 1
                                        logger.info(f"[CAPTURED] {keywords_found}: {msg_text[:60]}...")

                        logger.info(f"[RESULT] Found {found} new messages with keywords")
                        self.consecutive_failures = 0
                        retry_count = 0  # Reset on success
                    else:
                        error_msg = result.get('error') if result else "JavaScript returned None"
                        logger.error(f"[ERROR] JS extraction failed: {error_msg}")
                        self.consecutive_failures += 1
                        retry_count += 1

                except Exception as e:
                    logger.error(f"[ERROR] Cycle failed: {e}")
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

    def _save_message(self, content: str, keywords: List[str]):
        """Save captured message"""
        try:
            ts = datetime.now().isoformat().replace(':', '').replace('-', '')[:14]
            msg_id = hashlib.md5(content.encode()).hexdigest()[:8]
            filename = self.NEEDS_ACTION_DIR / f"facebook_{ts}_{msg_id}_message.md"

            message_content = f"""---
source: facebook
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
            if self.driver:
                self.driver.quit()
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
        watcher = FacebookWatcherJS()
        watcher.run()
    except KeyboardInterrupt:
        logger.info("[STOP] Stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"[FATAL] {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
