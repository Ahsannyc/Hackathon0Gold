#!/usr/bin/env python3
"""
Facebook Login Setup - Version 2
Opens browser with better error handling and timeouts
"""

import sys
import time
import logging
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
logger = logging.getLogger(__name__)

SESSION_PATH = Path("session/facebook_robust")
AUTH_MARKER = Path("session/facebook_authenticated.txt")


def setup_facebook_login():
    """Interactive Facebook login with better error handling"""

    logger.info("=" * 80)
    logger.info("FACEBOOK MESSENGER - LOGIN SETUP (v2)")
    logger.info("=" * 80)
    logger.info("")
    logger.info("A browser window will open in a moment...")
    logger.info("")
    logger.info("INSTRUCTIONS:")
    logger.info("1. Wait for the browser to load")
    logger.info("2. If you see a login page, enter your Facebook credentials")
    logger.info("3. Click 'Log In'")
    logger.info("4. Wait for Messages/Inbox to load")
    logger.info("5. Come back to this terminal and press Ctrl+C")
    logger.info("")
    logger.info("=" * 80)

    SESSION_PATH.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright

        logger.info("🔄 Starting Playwright...")
        playwright = sync_playwright().start()

        logger.info("🔄 Launching browser...")
        browser = playwright.chromium.launch_persistent_context(
            str(SESSION_PATH.absolute()),
            headless=False,  # Show window
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-extensions',
                '--no-sandbox',
                '--disable-dev-shm-usage',
            ]
        )

        logger.info("✅ Browser opened!")

        page = browser.new_page()

        logger.info("📱 Loading Facebook...")
        try:
            page.goto(
                "https://www.facebook.com/login/",
                timeout=30000,
                wait_until="domcontentloaded"
            )
            logger.info("✅ Facebook login page loaded")
        except Exception as e:
            logger.warning(f"⚠️  Page load warning: {e}")
            logger.info("Trying to load facebook.com instead...")
            try:
                page.goto("https://www.facebook.com/", timeout=30000)
                logger.info("✅ Facebook home page loaded")
            except:
                logger.error("❌ Could not load Facebook")
                raise

        logger.info("")
        logger.info("=" * 80)
        logger.info("✅ BROWSER IS READY")
        logger.info("=" * 80)
        logger.info("")
        logger.info("👤 Please log in with your Facebook account")
        logger.info("📱 Go to Messages/Inbox")
        logger.info("⏰ Take your time, browser will stay open")
        logger.info("")
        logger.info("When ready, press Ctrl+C in this terminal")
        logger.info("")
        logger.info("=" * 80)

        # Keep browser open indefinitely until user presses Ctrl+C
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("")
        logger.info("✅ Saving session...")
        AUTH_MARKER.write_text(str(time.time()))
        logger.info("✅ Session saved!")
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Run: pm2 restart facebook-watcher")
        logger.info("2. Wait 60 seconds")
        logger.info("3. Check: ls Needs_Action/ | grep facebook")
        logger.info("")

    except Exception as e:
        logger.error(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        logger.info("Cleaning up...")
        try:
            browser.close()
        except:
            pass
        try:
            playwright.stop()
        except:
            pass
        logger.info("✅ Done")


if __name__ == "__main__":
    setup_facebook_login()
