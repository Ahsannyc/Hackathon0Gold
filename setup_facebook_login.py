#!/usr/bin/env python3
"""
Facebook Setup - One-time Login for Initial Authentication
Run this ONCE to login, then the automated watcher will use the saved session
"""

import sys
import time
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

SESSION_PATH = Path("session/facebook")
AUTH_MARKER = Path("session/facebook_authenticated.txt")


def setup_facebook_login():
    """Interactive login for Facebook"""
    logger.info("=" * 60)
    logger.info("FACEBOOK MESSENGER - INITIAL LOGIN SETUP")
    logger.info("=" * 60)
    logger.info("A browser window will open. Please log in to Facebook.")
    logger.info("After login, DO NOT close the browser window.")
    logger.info("Press Ctrl+C in this terminal when ready to exit.")
    logger.info("=" * 60)

    SESSION_PATH.mkdir(parents=True, exist_ok=True)

    playwright = sync_playwright().start()

    try:
        logger.info("🔄 Launching Chromium browser...")
        browser = playwright.chromium.launch(
            headless=False,  # Show the window for login!
            args=['--disable-blink-features=AutomationControlled']
        )

        context = browser.new_context()
        page = context.new_page()

        logger.info("📱 Navigating to Facebook Messenger...")
        page.goto("https://www.facebook.com/messages/t/")

        logger.info("✅ Browser is open - LOG IN NOW")
        logger.info("After you log in successfully:")
        logger.info("  1. You'll see your messages/inbox")
        logger.info("  2. The watcher will save your session")
        logger.info("  3. Close this browser window")
        logger.info("\n⏳ Waiting for you to login... (Press Ctrl+C to exit)")

        # Keep browser open until user closes it
        time.sleep(300)  # 5 minute timeout as fallback

        context.close()

    except KeyboardInterrupt:
        logger.info("\n✅ Setup complete! Session saved.")
        AUTH_MARKER.write_text("authenticated")

    except Exception as e:
        logger.error(f"Error: {e}")

    finally:
        try:
            browser.close()
        except:
            pass
        playwright.stop()

        if AUTH_MARKER.exists():
            logger.info("✅ Facebook authentication saved!")
            logger.info("You can now run: pm2 restart facebook-watcher")
        else:
            logger.warning("⚠️  Session not saved. Make sure you logged in completely.")


if __name__ == "__main__":
    setup_facebook_login()
