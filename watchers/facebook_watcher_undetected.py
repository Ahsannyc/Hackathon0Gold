#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facebook Messenger Watcher - UNDETECTED CHROMEDRIVER
Uses undetected-chromedriver to bypass Facebook's anti-bot detection
Much more reliable than Playwright for heavily protected sites
"""

import os
import sys
import time
import logging
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import List

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Try to import undetected-chromedriver
try:
    from undetected_chromedriver import Chrome as UndetectedChrome
    HAS_UNDETECTED = True
except ImportError:
    HAS_UNDETECTED = False
    print("ERROR: undetected-chromedriver not installed!")
    print("Installing: pip install undetected-chromedriver")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

Path("watchers/logs").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("watchers/logs/facebook_watcher_undetected.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FacebookWatcherUndetected:
    """Facebook Messenger Watcher - Undetected Chromedriver (Anti-Bot Bypass)"""

    KEYWORDS = ['sales', 'client', 'project', 'urgent', 'invoice', 'payment', 'deal', 'opportunity', 'partnership', 'lead', 'inquiry']
    CHECK_INTERVAL = 60
    NEEDS_ACTION_DIR = Path("Needs_Action")
    PROFILE_DIR = Path("session/facebook_undetected")

    def __init__(self):
        self.processed_messages = set()
        self.driver = None
        self.consecutive_failures = 0

    def ensure_dirs(self):
        """Ensure required directories exist"""
        self.NEEDS_ACTION_DIR.mkdir(parents=True, exist_ok=True)
        self.PROFILE_DIR.mkdir(parents=True, exist_ok=True)
        logger.info("[OK] Directories ready")

    def launch_browser(self):
        """Launch undetected Chrome browser"""
        logger.info("[BROWSER] Launching undetected Chrome...")

        try:
            # Use undetected-chromedriver
            options = webdriver.ChromeOptions()
            options.add_argument(f"--user-data-dir={self.PROFILE_DIR.absolute()}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--start-maximized")
            # Don't hide - show window for login
            # options.add_argument("--headless")

            # Create undetected Chrome instance
            self.driver = UndetectedChrome(options=options, use_subprocess=False)
            logger.info("[OK] Undetected Chrome launched")
            return True

        except Exception as e:
            logger.error(f"[ERROR] Failed to launch browser: {e}")
            return False

    def login_and_monitor(self):
        """Navigate to Messenger and monitor for messages"""
        try:
            logger.info("[NAV] Navigating to Facebook Messenger...")
            self.driver.get("https://www.facebook.com/messages/t/")

            # Wait for page to load
            time.sleep(5)

            # Check if login page is shown
            page_source = self.driver.page_source.lower()
            if "login" in page_source or "sign in" in page_source:
                logger.warning("[AUTH] Login page detected - please log in manually")
                logger.info("[WAIT] Waiting for login (120 seconds)...")

                # Wait for successful login (URL change)
                try:
                    WebDriverWait(self.driver, 120).until(
                        lambda driver: "messages" in driver.current_url and "login" not in driver.current_url
                    )
                    logger.info("[OK] Login successful!")
                    time.sleep(5)
                except TimeoutException:
                    logger.warning("[WARN] Login timeout - continuing anyway")

            logger.info("[READY] Starting message monitoring...")

            # Main monitoring loop
            cycle = 0
            while True:
                cycle += 1
                logger.info(f"[CYCLE {cycle}] Checking for new messages...")

                try:
                    # Refresh Messenger
                    self.driver.get("https://www.facebook.com/messages/t/")
                    time.sleep(3)

                    # Extract messages
                    found = self._extract_messages()
                    logger.info(f"[RESULT] Found {found} new messages with keywords")

                    self.consecutive_failures = 0

                except Exception as e:
                    logger.error(f"[ERROR] Check failed: {e}")
                    self.consecutive_failures += 1

                    if self.consecutive_failures >= 3:
                        logger.error("[RESTART] Too many failures, restarting...")
                        self.cleanup()
                        if self.launch_browser():
                            self.login_and_monitor()
                        return

                logger.info(f"[WAIT] Sleeping {self.CHECK_INTERVAL}s until next check...")
                time.sleep(self.CHECK_INTERVAL)

        except KeyboardInterrupt:
            logger.info("[STOP] Stopped by user")
        except Exception as e:
            logger.error(f"[ERROR] Fatal error: {e}", exc_info=True)
        finally:
            self.cleanup()

    def _extract_messages(self) -> int:
        """Extract Messenger messages with keywords"""
        messages_found = 0

        try:
            # Multiple selector strategies
            selectors = [
                # Messenger message containers
                'div[data-testid*="message"]',
                'div[role="article"]',
                'div[class*="message"]',
                'span[class*="text"]',
                # Conversation containers
                'div[role="main"]',
                'div[data-testid*="thread"]',
            ]

            found_elements = set()

            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    logger.debug(f"[DOM] Selector '{selector}': {len(elements)} elements")

                    for elem in elements:
                        try:
                            text = elem.text
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
        """Main entry point"""
        if not HAS_UNDETECTED:
            logger.error("[FATAL] undetected-chromedriver not installed")
            logger.error("Install with: pip install undetected-chromedriver")
            return

        self.ensure_dirs()

        if not self.launch_browser():
            logger.error("[FATAL] Could not launch browser")
            return

        self.login_and_monitor()


def main():
    """Main entry point"""
    try:
        watcher = FacebookWatcherUndetected()
        watcher.run()
    except KeyboardInterrupt:
        logger.info("[STOP] Stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"[FATAL] {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
