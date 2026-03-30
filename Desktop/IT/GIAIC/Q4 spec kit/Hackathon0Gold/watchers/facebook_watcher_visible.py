#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facebook Messenger Watcher - VISIBLE BROWSER APPROACH
Uses a visible (non-headless) browser window that stays open.
User logs in once, then watcher monitors continuously.
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
        logging.FileHandler("watchers/logs/facebook_watcher_visible.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FacebookWatcherVisible:
    """Facebook Messenger Watcher - Visible Browser (No Persistent Context Crash)"""

    KEYWORDS = ['sales', 'client', 'project', 'urgent', 'invoice', 'payment', 'deal', 'opportunity', 'partnership', 'lead', 'inquiry']
    CHECK_INTERVAL = 60  # Check every 60 seconds
    NEEDS_ACTION_DIR = Path("Needs_Action")
    SESSION_COOKIES = Path("session/facebook_cookies.json")

    def __init__(self):
        self.processed_messages = set()
        self.playwright = None
        self.browser = None
        self.page = None
        self.consecutive_failures = 0

    def ensure_dirs(self):
        """Ensure required directories exist"""
        self.NEEDS_ACTION_DIR.mkdir(parents=True, exist_ok=True)
        self.SESSION_COOKIES.parent.mkdir(parents=True, exist_ok=True)
        logger.info("[OK] Directories ready")

    def load_cookies(self):
        """Load saved cookies if they exist"""
        if self.SESSION_COOKIES.exists():
            try:
                with open(self.SESSION_COOKIES, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"[WARN] Could not load cookies: {e}")
        return []

    def save_cookies(self):
        """Save browser cookies for next run"""
        try:
            if self.page:
                cookies = self.page.context.cookies()
                with open(self.SESSION_COOKIES, 'w') as f:
                    json.dump(cookies, f, indent=2)
                logger.info("[OK] Cookies saved")
        except Exception as e:
            logger.error(f"[ERROR] Could not save cookies: {e}")

    def launch_browser(self):
        """Launch VISIBLE browser (not headless, not persistent context)"""
        logger.info("[BROWSER] Launching visible Chromium browser...")

        try:
            self.playwright = sync_playwright().start()

            # Launch browser in NON-HEADLESS mode (visible window)
            self.browser = self.playwright.chromium.launch(
                headless=False,  # VISIBLE WINDOW - important!
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-extensions',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-gpu-rasterization',
                ]
            )

            # Create context with saved cookies
            cookies = self.load_cookies()
            context_options = {
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            }
            if cookies:
                context_options['cookies'] = cookies

            context = self.browser.new_context(**context_options)

            # Inject anti-detection script
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => false});
                window.chrome = {runtime: {}};
            """)

            self.page = context.new_page()
            logger.info("[OK] Browser launched (VISIBLE window)")
            return True

        except Exception as e:
            logger.error(f"[ERROR] Failed to launch browser: {e}")
            return False

    def check_and_login(self):
        """Navigate to Messenger and wait for login if needed"""
        try:
            logger.info("[NAV] Navigating to Facebook Messenger...")
            self.page.goto("https://www.facebook.com/messages/t/", wait_until="domcontentloaded", timeout=30000)

            # Check if we're logged in
            time.sleep(3)
            page_text = self.page.inner_text("body").lower()

            if "login" in page_text or "sign in" in page_text:
                logger.warning("[AUTH] Login page detected - please log in manually in the browser window")
                logger.info("[WAIT] Waiting for successful login (120 seconds)...")

                # Wait for navigation away from login page
                try:
                    self.page.wait_for_url("**/messages**", timeout=120000)
                    logger.info("[OK] Login successful!")
                    time.sleep(3)

                    # Save authenticated cookies
                    self.save_cookies()
                except:
                    logger.warning("[WARN] Login timeout - but continuing anyway")
            else:
                logger.info("[OK] Already logged in")

        except Exception as e:
            logger.error(f"[ERROR] Navigation failed: {e}")
            return False

        return True

    def extract_messages(self) -> int:
        """Extract Messenger messages with keywords"""
        messages_found = 0

        try:
            # Multiple selector attempts
            selectors = [
                '[data-testid*="message"]',
                '[role="main"] div[class*="message"]',
                '.x5jyip7',  # Facebook message div
                'div[class*="message"]',
                '[data-testid*="thread"]',
            ]

            for selector in selectors:
                try:
                    elements = self.page.query_selector_all(selector)
                    logger.debug(f"[DOM] Selector '{selector}': {len(elements)} elements found")

                    for elem in elements:
                        try:
                            text = elem.inner_text()
                            if text and len(text) > 5:
                                # Check for keywords
                                keywords_found = [kw for kw in self.KEYWORDS if kw.lower() in text.lower()]

                                if keywords_found:
                                    msg_hash = hashlib.md5(text.encode()).hexdigest()[:8]
                                    if msg_hash not in self.processed_messages:
                                        self.processed_messages.add(msg_hash)
                                        self._save_message(text, keywords_found)
                                        messages_found += 1
                                        logger.info(f"[CAPTURED] Keywords {keywords_found}: {text[:50]}...")
                        except:
                            pass

                except Exception as e:
                    logger.debug(f"[SKIP] Selector error: {e}")

            if messages_found == 0:
                logger.info("[NO_NEW] No new messages with keywords")

        except Exception as e:
            logger.error(f"[ERROR] Message extraction failed: {e}")

        return messages_found

    def _save_message(self, content: str, keywords: List[str]):
        """Save captured message to file"""
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

    def monitor_messenger(self):
        """Main monitoring loop"""
        logger.info("[START] Facebook Messenger Watcher (Visible Browser) starting...")
        self.ensure_dirs()

        # Launch browser
        if not self.launch_browser():
            logger.error("[FATAL] Could not launch browser")
            return

        # Check login
        if not self.check_and_login():
            logger.error("[FATAL] Could not login to Facebook")
            return

        logger.info("[READY] Monitoring Messenger for messages...")

        try:
            cycle = 0
            while True:
                cycle += 1
                logger.info(f"[CYCLE {cycle}] Checking for new messages...")

                try:
                    # Navigate to messenger to refresh
                    self.page.goto("https://www.facebook.com/messages/t/", wait_until="domcontentloaded", timeout=20000)
                    time.sleep(2)

                    # Extract messages
                    found = self.extract_messages()

                    self.consecutive_failures = 0

                except Exception as e:
                    logger.error(f"[ERROR] Check cycle failed: {e}")
                    self.consecutive_failures += 1

                    if self.consecutive_failures >= 3:
                        logger.error("[RESTART] Too many failures, restarting browser...")
                        self.cleanup()
                        if self.launch_browser():
                            self.check_and_login()
                        self.consecutive_failures = 0

                logger.info(f"[WAIT] Sleeping {self.CHECK_INTERVAL}s until next check...")
                time.sleep(self.CHECK_INTERVAL)

        except KeyboardInterrupt:
            logger.info("[STOP] Stopped by user")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean shutdown"""
        try:
            self.save_cookies()
            if self.page:
                self.page.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except:
            pass


def main():
    """Main entry point"""
    try:
        watcher = FacebookWatcherVisible()
        watcher.monitor_messenger()
    except KeyboardInterrupt:
        logger.info("[STOP] Stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"[FATAL] {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
