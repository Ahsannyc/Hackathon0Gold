#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facebook Messenger Watcher - Persistent Browser Session (FACEBOOK ONLY)
Keeps the browser open between checks to maintain authentication
One-time setup: manual login, then continuous monitoring
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
        logging.FileHandler("watchers/logs/facebook_watcher_only.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FacebookWatcherOnly:
    """
    Facebook Messenger Only Watcher
    Monitors ONLY Facebook Messenger for business keywords
    """
    KEYWORDS = ['sales', 'client', 'project', 'urgent', 'invoice', 'payment', 'deal', 'opportunity', 'partnership', 'lead', 'inquiry']
    CHECK_INTERVAL = 60  # seconds between message checks
    SESSION_REFRESH_INTERVAL = 5400  # 90 minutes
    NEEDS_ACTION_DIR = Path("Needs_Action")
    SESSION_PATH = Path("session/facebook")
    AUTH_MARKER_FILE = Path("session/facebook_authenticated.txt")

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.processed_messages = set()
        self.is_authenticated = False
        self.last_auth_check = time.time()
        self.consecutive_failures = 0
        self.max_consecutive_failures = 5
        self.launch_retry_count = 0
        self.max_launch_retries = 3

    def ensure_session_dir(self):
        """Ensure session directory exists"""
        try:
            self.SESSION_PATH.mkdir(parents=True, exist_ok=True)
            self.NEEDS_ACTION_DIR.mkdir(parents=True, exist_ok=True)
            logger.info(f"[OK] Session directory: {self.SESSION_PATH.absolute()}")
            # Clean up any lock files that might prevent browser launch
            lock_files = list(self.SESSION_PATH.glob("**/lock"))
            for lock in lock_files:
                try:
                    lock.unlink()
                    logger.info(f"[CLEANUP] Removed stale lock file: {lock}")
                except:
                    pass
        except Exception as e:
            logger.error(f"[ERROR] Failed to create session directory: {e}")

    def is_already_authenticated(self) -> bool:
        """Check if we've authenticated before"""
        return self.AUTH_MARKER_FILE.exists()

    def mark_authenticated(self):
        """Mark that we've successfully authenticated"""
        self.AUTH_MARKER_FILE.write_text(datetime.now().isoformat())
        logger.info("[OK] Authentication marked - session will be reused")

    def launch_browser_persistent(self):
        """Launch browser with persistent session that stays open"""
        try:
            self.playwright = sync_playwright().start()

            logger.info("[SETUP] Launching Chromium with persistent session...")
            self.browser = self.playwright.chromium.launch_persistent_context(
                str(self.SESSION_PATH.absolute()),
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-gpu',
                    '--disable-web-resources',
                    '--disable-component-update',
                ]
            )

            self.page = self.browser.new_page()
            logger.info("[OK] Browser launched, navigating to Facebook Messenger...")

            try:
                self.page.goto("https://www.facebook.com/messages/t/", wait_until="networkidle", timeout=30000)
            except Exception as nav_err:
                logger.warning(f"[WARN] Navigation timeout or error: {nav_err}, proceeding anyway...")
                try:
                    self.page.goto("https://www.facebook.com/messages/t/")
                except:
                    pass

            logger.info("[LOAD] Page loaded, waiting for messenger area...")

            # Try to detect if authenticated
            time.sleep(2)
            auth_status = self._check_authentication()

            if auth_status:
                logger.info("[OK] AUTHENTICATED - Facebook Messenger detected!")
                self.is_authenticated = True
                self.mark_authenticated()
                time.sleep(2)
            else:
                if self.is_already_authenticated():
                    logger.warning("[WARN] Auth marker exists but messenger not visible")
                    logger.info("[INFO] Session might need refresh, waiting 30 seconds...")
                    time.sleep(30)
                    self.is_authenticated = True
                else:
                    logger.warning("[WARN] First run detected - messenger not visible")
                    logger.info("[INFO] Waiting 120 seconds for manual login...")
                    logger.info("[INFO] >>> LOG IN TO FACEBOOK NOW IN THE BROWSER WINDOW <<<")
                    time.sleep(120)
                    auth_status = self._check_authentication()
                    if auth_status:
                        logger.info("[OK] Authentication successful!")
                        self.is_authenticated = True
                        self.mark_authenticated()
                        time.sleep(2)
                    else:
                        logger.warning("[WARN] Messenger still not visible - will proceed anyway")
                        self.is_authenticated = True

        except Exception as e:
            logger.error(f"[ERROR] Browser launch failed: {e}", exc_info=True)
            logger.info("[INFO] Attempting cleanup...")
            if self.browser:
                try:
                    self.browser.close()
                except:
                    pass
            if self.playwright:
                try:
                    self.playwright.stop()
                except:
                    pass

            logger.error("""
[TROUBLESHOOTING]
1. Try deleting session folder: rm -r session/facebook/*
2. Check if other Chrome processes are running: tasklist | grep chrome
3. Kill existing processes: taskkill /IM chrome.exe /F
4. Restart and try again
            """)
            raise

    def _check_authentication(self) -> bool:
        """Check if we're authenticated (messenger visible)"""
        try:
            is_messenger_visible = self.page.is_visible('[data-testid="message_list"]', timeout=3000)
            if is_messenger_visible:
                return True
        except:
            pass

        try:
            is_conv_visible = self.page.is_visible('div[role="main"]', timeout=2000)
            if is_conv_visible:
                return True
        except:
            pass

        try:
            page_text = self.page.inner_text("body").lower()
            if "sign in" in page_text and "email" in page_text:
                return False
            if len(page_text) > 500:
                return True
        except:
            pass

        return False

    def refresh_session(self) -> bool:
        """Periodic session refresh - verify authentication is still valid"""
        logger.info("[SESSION] Performing periodic authentication check...")
        try:
            if self._check_authentication():
                logger.info("[SESSION] ✓ Authentication still valid - session healthy")
                self.consecutive_failures = 0
                return True
            else:
                logger.warning("[SESSION] ✗ Authentication failed - session may be expired")
                self.consecutive_failures += 1

                if self.consecutive_failures >= self.max_consecutive_failures:
                    logger.error(f"[SESSION] {self.consecutive_failures} consecutive failures - initiating browser restart")
                    return False
                else:
                    logger.info(f"[SESSION] Failure count: {self.consecutive_failures}/{self.max_consecutive_failures}")
                    try:
                        logger.info("[SESSION] Attempting page refresh...")
                        self.page.reload(wait_until="networkidle")
                        time.sleep(3)
                        if self._check_authentication():
                            logger.info("[SESSION] ✓ Refresh successful")
                            self.consecutive_failures = 0
                            return True
                    except Exception as e:
                        logger.warning(f"[SESSION] Refresh failed: {e}")
                    return False
        except Exception as e:
            logger.error(f"[SESSION] Refresh check error: {e}")
            self.consecutive_failures += 1
            return self.consecutive_failures < self.max_consecutive_failures

    def get_messages(self) -> List[Dict]:
        """Extract messages from Facebook Messenger"""
        messages = []
        try:
            logger.debug("[FB] Extracting Facebook Messenger messages...")

            if not self._check_authentication():
                logger.warning("[WARN] Messenger area not visible - page may have logged out")
                return messages

            js_code = """
            () => {
                const items = [];
                try {
                    const conversations = document.querySelectorAll('[role="button"][data-testid^="conversation_item"]');

                    for (let conv of conversations) {
                        try {
                            const text = conv.innerText || conv.textContent;
                            if (!text || text.length < 3) continue;

                            const lines = text.split('\\n').map(l => l.trim()).filter(l => l);
                            if (lines.length < 1) continue;

                            const sender = lines[0];
                            const preview = lines.slice(1).join(' ').substring(0, 200);

                            if (sender && sender.length > 2 && sender.length < 150) {
                                const key = sender + '|' + preview.substring(0, 30);
                                const exists = items.some(i =>
                                    i.sender === sender &&
                                    i.preview.substring(0, 30) === preview.substring(0, 30)
                                );

                                if (!exists) {
                                    items.push({
                                        sender: sender,
                                        preview: preview || text.substring(0, 200),
                                        full_text: text.substring(0, 500),
                                        platform: 'facebook'
                                    });
                                }
                            }
                        } catch (e) {
                            // Skip items that error
                        }
                    }

                    return {
                        success: true,
                        items: items,
                        total_found: items.length,
                        page_title: document.title
                    };
                } catch (err) {
                    return {
                        success: false,
                        error: err.message,
                        items: []
                    };
                }
            }
            """

            result = self.page.evaluate(js_code)

            if not result.get('success'):
                logger.error(f"[FB] Error: {result.get('error')}")
                return messages

            items = result.get('items', [])
            logger.info(f"[FB] Found {len(items)} messages from Facebook Messenger")

            for idx, item in enumerate(items):
                try:
                    sender = item.get('sender', 'Unknown')
                    preview = item.get('preview', '')
                    full_text = item.get('full_text', '')

                    if not preview:
                        if full_text:
                            preview = full_text
                        else:
                            logger.debug(f"[FB ITEM {idx}] Skipping - no content")
                            continue

                    logger.debug(f"[FB ITEM {idx}] From: {sender} | Preview: {preview[:80]}")

                    keywords_found = [kw for kw in self.KEYWORDS if kw.lower() in preview.lower() or kw.lower() in full_text.lower()]

                    if keywords_found:
                        msg_hash = hashlib.md5((sender + preview).encode()).hexdigest()[:8]

                        if msg_hash not in self.processed_messages:
                            messages.append({
                                'from': sender,
                                'message': preview if preview else full_text[:200],
                                'received': datetime.now().isoformat(),
                                'priority': 'high' if 'urgent' in preview.lower() else 'medium',
                                'keywords_found': keywords_found,
                                'type': 'facebook',
                                'status': 'pending',
                                'hash': msg_hash,
                                'platform': 'facebook'
                            })
                            self.processed_messages.add(msg_hash)
                            logger.info(f"[OK] Captured Facebook message from {sender}: {keywords_found} - {preview[:50]}")
                        else:
                            logger.debug(f"[FB ITEM {idx}] Already processed")
                    else:
                        logger.debug(f"[FB ITEM {idx}] No keywords found")

                except Exception as e:
                    logger.debug(f"[FB ITEM {idx}] Error: {e}")

            return messages

        except Exception as e:
            logger.error(f"[ERROR] Failed to extract Facebook messages: {e}", exc_info=True)
            return messages

    def save_to_markdown(self, message: Dict) -> Path:
        """Save message as markdown file with YAML metadata"""
        try:
            self.NEEDS_ACTION_DIR.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            msg_hash = message.get('hash', hashlib.md5(str(time.time()).encode()).hexdigest()[:6])
            safe_sender = "".join(c for c in message['from'] if c.isalnum() or c in ' -_')[:20]
            platform = message.get('type', 'facebook')
            filename = f"{platform}_{timestamp}_{msg_hash}_{safe_sender}.md"
            filepath = self.NEEDS_ACTION_DIR / filename

            source = message.get('platform', platform)
            keywords_str = ", ".join(message.get('keywords_found', []))

            content = f"""---
type: {message.get('type', 'facebook')}
from: {message.get('from', 'Unknown')}
subject: Facebook message from {message.get('from', 'Unknown')}
received: {message.get('received', datetime.now().isoformat())}
priority: {message.get('priority', 'medium')}
status: {message.get('status', 'pending')}
source: {source}
keywords_found: [{keywords_str}]
created_at: {datetime.now().isoformat()}
---

# Facebook Message from {message.get('from', 'Unknown')}

**From:** {message.get('from', 'Unknown')}

**Received:** {message.get('received', 'Unknown')}

**Priority:** {message.get('priority', 'medium').upper()}

**Keywords:** {keywords_str}

---

## Message

{message.get('message', '(No content)')}

---

## Action Required

- [ ] Review message on Facebook
- [ ] Assess opportunity
- [ ] Draft response if interested
- [ ] Archive when done
"""

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"[OK] Saved: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"[ERROR] Error saving markdown: {e}")
            return None

    def run(self):
        """Main watcher loop - keeps browser open between checks"""
        logger.info(f"Starting FACEBOOK ONLY Watcher - Check interval: {self.CHECK_INTERVAL}s")

        try:
            self.ensure_session_dir()

            # Retry loop for browser launch
            while self.launch_retry_count < self.max_launch_retries:
                try:
                    self.launch_browser_persistent()
                    break
                except Exception as e:
                    self.launch_retry_count += 1
                    if self.launch_retry_count < self.max_launch_retries:
                        wait_time = 10 * self.launch_retry_count
                        logger.warning(f"[RETRY {self.launch_retry_count}/{self.max_launch_retries}] Browser launch failed, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"[ERROR] Browser launch failed after {self.max_launch_retries} retries")
                        raise

            if not self.is_authenticated:
                logger.error("[ERROR] Could not authenticate - giving up")
                return

            logger.info("[OK] Starting monitoring loop...")

            cycle_count = 0
            while True:
                cycle_count += 1
                try:
                    current_time = time.time()

                    if current_time - self.last_auth_check >= self.SESSION_REFRESH_INTERVAL:
                        logger.info(f"\n[CYCLE {cycle_count}] Session health check...")
                        if not self.refresh_session():
                            logger.error("[ERROR] Session refresh failed - restarting browser")
                            self.browser.close()
                            self.playwright.stop()
                            self.launch_browser_persistent()
                        self.last_auth_check = current_time

                    logger.info(f"[CYCLE {cycle_count}] Checking Facebook Messenger...")
                    messages = self.get_messages()

                    if messages:
                        logger.info(f"[CYCLE {cycle_count}] Total messages to save: {len(messages)}")
                        for msg in messages:
                            self.save_to_markdown(msg)
                    else:
                        logger.debug(f"[CYCLE {cycle_count}] No new messages with keywords")

                    logger.info(f"[CYCLE {cycle_count}] Waiting {self.CHECK_INTERVAL}s until next check...")
                    time.sleep(self.CHECK_INTERVAL)

                except KeyboardInterrupt:
                    logger.info("[INFO] Keyboard interrupt received - shutting down gracefully...")
                    break
                except Exception as e:
                    logger.error(f"[ERROR] Error in monitoring loop: {e}", exc_info=True)
                    time.sleep(self.CHECK_INTERVAL)

        except Exception as e:
            logger.error(f"[FATAL] Fatal error: {e}", exc_info=True)
        finally:
            logger.info("[CLEANUP] Closing browser...")
            if self.browser:
                try:
                    self.browser.close()
                except:
                    pass
            if self.playwright:
                try:
                    self.playwright.stop()
                except:
                    pass
            logger.info("[CLEANUP] Watcher stopped")


if __name__ == "__main__":
    watcher = FacebookWatcherOnly()
    watcher.run()
