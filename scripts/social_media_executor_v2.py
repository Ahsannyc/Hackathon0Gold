#!/usr/bin/env python3
"""
Social Media Executor v2.0 - Multi-Platform Autonomous Poster
================================================================================
Uses Playwright with persistent contexts for 6 social platforms:
- LinkedIn (Start a post → fill content → click Post)
- Facebook (Next → fill content → Post/Share)
- Twitter/X (compose tweet → post)
- Instagram (create post → share)
- WhatsApp (select contact → send message)
- Gmail (compose → send)

Requirements:
- Persistent browser sessions in /session/ folder
- Manual login once (no tokens needed)
- Retry 3 times on failure
- Take error screenshots to /Logs/error_[date].png
- Move successful posts to /Done/
- YAML + Markdown file format from /Approved/

Usage:
    python scripts/social_media_executor_v2.py /Approved/facebook_draft_20260329_abc123.md
    python scripts/social_media_executor_v2.py --all-pending
"""

import asyncio
import os
import sys
import json
import yaml
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple, Optional
import shutil
from dataclasses import dataclass

from playwright.async_api import async_playwright, Page, BrowserContext, expect

# Setup logging
os.makedirs("Logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"Logs/social_executor_{datetime.now().strftime('%Y-%m-%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class PostContent:
    """Parsed post content from markdown file"""
    platform: str
    content: str
    title: str
    from_user: str
    priority: str
    filename: str
    filepath: Path


class SocialMediaExecutor:
    """Main executor for multi-platform social media posting"""

    def __init__(self):
        self.session_dir = Path("session")
        self.approved_dir = Path("Approved")
        self.done_dir = Path("Done")
        self.logs_dir = Path("Logs")
        self.max_retries = 3

        # Ensure directories exist
        for directory in [self.session_dir, self.approved_dir, self.done_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        logger.info("Social Media Executor v2.0 initialized")

    def parse_post_file(self, filepath: Path) -> Optional[PostContent]:
        """Parse YAML frontmatter + content from markdown file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract YAML frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        metadata = yaml.safe_load(parts[1]) or {}
                        body = parts[2].strip()

                        # Detect platform from filename or metadata
                        platform = metadata.get('platform', self.detect_platform(filepath.name))

                        return PostContent(
                            platform=platform,
                            content=body,
                            title=metadata.get('subject', metadata.get('title', 'Post')),
                            from_user=metadata.get('from', 'system'),
                            priority=metadata.get('priority', 'medium'),
                            filename=filepath.name,
                            filepath=filepath
                        )
                    except yaml.YAMLError as e:
                        logger.error(f"YAML parse error in {filepath.name}: {e}")
                        return None

            logger.warning(f"No YAML frontmatter in {filepath.name}")
            return None
        except Exception as e:
            logger.error(f"Error parsing {filepath.name}: {e}")
            return None

    def detect_platform(self, filename: str) -> str:
        """Detect platform from filename"""
        filename_lower = filename.lower()
        for platform in ['linkedin', 'facebook', 'twitter', 'instagram', 'whatsapp', 'gmail']:
            if platform in filename_lower:
                return platform
        return 'unknown'

    async def post_to_linkedin(self, page: Page, content: PostContent) -> bool:
        """Post to LinkedIn - Using correct selectors"""
        try:
            logger.info(f"🔴 Posting to LinkedIn: {content.title}")

            # Navigate to LinkedIn
            if "linkedin.com" not in page.url:
                await page.goto("https://www.linkedin.com/feed/")
                await page.wait_for_load_state("networkidle")

            await page.wait_for_timeout(1000)

            # Click "Start a post" button - try multiple selectors
            logger.info("Opening composer...")
            start_selectors = [
                'button:has-text("Start a post")',
                ".share-mbw-trigger",
                '[aria-label="Start a post"]',
                "text=Start a post"
            ]

            start_clicked = False
            for selector in start_selectors:
                try:
                    logger.info(f"[LINKEDIN] Trying selector: {selector}")
                    btn = page.locator(selector)
                    await btn.click(timeout=2000)
                    logger.info(f"[LINKEDIN] Clicked {selector}")
                    start_clicked = True
                    break
                except:
                    continue

            if not start_clicked:
                logger.error("Could not click 'Start a post' button")
                return False

            await page.wait_for_timeout(2500)

            # Find editor using correct selector
            logger.info("Finding editor...")
            editor_selectors = [
                'div[role="textbox"]',
                "div[contenteditable='true']"
            ]

            editor = None
            for selector in editor_selectors:
                try:
                    editor = page.locator(selector).first
                    await editor.click()
                    logger.info(f"[LINKEDIN] Found editor via: {selector}")
                    break
                except:
                    continue

            if not editor:
                logger.error("Could not find editor")
                return False

            await page.wait_for_timeout(400)

            # Type content
            await page.keyboard.type(content.content, delay=15)
            await page.wait_for_timeout(1500)

            # Click POST button using CORRECT class selector
            logger.info("Clicking Post button...")
            post_button = page.locator(".share-actions__primary-action")

            try:
                await post_button.click(timeout=5000)
                logger.info("[LINKEDIN] Clicked Post button via: .share-actions__primary-action")
            except Exception as e:
                logger.warning(f"Primary selector failed: {e}, trying backup...")
                # Backup: try text selector
                post_button = page.locator("button:has-text('Post')")
                await post_button.click(timeout=5000)
                logger.info("[LINKEDIN] Clicked Post button via: text selector")

            # Wait for submission
            await page.wait_for_timeout(5000)

            logger.info("✅ [SUCCESS] Task completed and moved to Done.")
            return True

        except Exception as e:
            logger.error(f"❌ LinkedIn posting failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    async def post_to_facebook(self, page: Page, content: PostContent) -> bool:
        """Post to Facebook - multi-selector approach"""
        try:
            logger.info(f"📘 Posting to Facebook: {content.title}")

            # Navigate to Facebook if needed
            if "facebook.com" not in page.url:
                await page.goto("https://www.facebook.com/")
                await page.wait_for_load_state("networkidle")

            await page.wait_for_timeout(1500)

            # Click "Create post" - try multiple selectors
            create_selectors = [
                "text=What's on your mind",
                '[aria-label="What\'s on your mind?"]',
                '[data-testid="status-post"]'
            ]

            created = False
            for selector in create_selectors:
                try:
                    logger.info(f"[FACEBOOK] Trying selector: {selector}")
                    create_post = page.locator(selector).first
                    await create_post.click(timeout=3000)
                    logger.info(f"[FACEBOOK] Clicked {selector}")
                    created = True
                    break
                except:
                    continue

            if not created:
                logger.error("Could not open Facebook post composer")
                return False

            await page.wait_for_timeout(2000)

            # Fill content
            editor = page.locator("div[contenteditable='true']").first
            await editor.click()
            await page.keyboard.type(content.content, delay=12)
            await page.wait_for_timeout(1000)

            # Click Post button - try multiple selectors
            post_selectors = [
                "button:has-text('Post')",
                '[data-testid="xod-form-submit-button"]',
                '.share-action-button'
            ]

            posted = False
            for selector in post_selectors:
                try:
                    logger.info(f"[FACEBOOK] Trying post selector: {selector}")
                    post_button = page.locator(selector).first
                    await post_button.click(timeout=5000)
                    logger.info(f"[FACEBOOK] Clicked Post via: {selector}")
                    posted = True
                    break
                except:
                    continue

            if not posted:
                logger.error("Could not click Facebook Post button")
                return False

            # Wait for post to complete
            await page.wait_for_timeout(4000)
            logger.info("✅ Facebook post successful")
            return True

        except Exception as e:
            logger.error(f"❌ Facebook posting failed: {e}")
            return False

    async def post_to_twitter(self, page: Page, content: PostContent) -> bool:
        """Post to Twitter/X - multi-selector approach"""
        try:
            logger.info(f"🐦 Posting to Twitter: {content.title}")

            # Navigate to Twitter if needed
            if "twitter.com" not in page.url and "x.com" not in page.url:
                await page.goto("https://twitter.com/home")
                await page.wait_for_load_state("networkidle")

            await page.wait_for_timeout(1500)

            # Click Compose button - try multiple selectors
            compose_selectors = [
                "[aria-label='Compose']",
                "a[href='/compose/tweet']",
                'button:has-text("Compose")',
                'button[aria-label="Compose"]'
            ]

            composed = False
            for selector in compose_selectors:
                try:
                    logger.info(f"[TWITTER] Trying selector: {selector}")
                    compose_btn = page.locator(selector).first
                    await compose_btn.click(timeout=3000)
                    logger.info(f"[TWITTER] Clicked {selector}")
                    composed = True
                    break
                except:
                    continue

            if not composed:
                logger.error("Could not open Twitter compose")
                return False

            await page.wait_for_timeout(2000)

            # Fill tweet content
            editor = page.locator("div[contenteditable='true']").first
            await editor.click()
            await page.keyboard.type(content.content, delay=10)
            await page.wait_for_timeout(1000)

            # Click Post button - try multiple selectors
            post_selectors = [
                "[data-testid='Tweet_Button']",
                "button:has-text('Post')",
                '[role="button"]:has-text("Post")'
            ]

            posted = False
            for selector in post_selectors:
                try:
                    logger.info(f"[TWITTER] Trying post selector: {selector}")
                    post_button = page.locator(selector).first
                    await post_button.click(timeout=5000)
                    logger.info(f"[TWITTER] Clicked Post via: {selector}")
                    posted = True
                    break
                except:
                    continue

            if not posted:
                logger.error("Could not click Twitter Post button")
                return False

            # Wait for tweet to post
            await page.wait_for_timeout(3000)
            logger.info("✅ Twitter post successful")
            return True

        except Exception as e:
            logger.error(f"❌ Twitter posting failed: {e}")
            return False

    async def post_to_instagram(self, page: Page, content: PostContent) -> bool:
        """Post to Instagram - multi-selector approach"""
        try:
            logger.info(f"📷 Posting to Instagram: {content.title}")

            # Navigate to Instagram if needed
            if "instagram.com" not in page.url:
                await page.goto("https://www.instagram.com/")
                await page.wait_for_load_state("networkidle")

            await page.wait_for_timeout(1500)

            # Click Create button - try multiple selectors
            create_selectors = [
                "[aria-label='Create']",
                'a[href="#"]',
                '[data-testid="new_post_button"]',
                'button[aria-label="Create"]'
            ]

            created = False
            for selector in create_selectors:
                try:
                    logger.info(f"[INSTAGRAM] Trying selector: {selector}")
                    create_btn = page.locator(selector).first
                    await create_btn.click(timeout=3000)
                    logger.info(f"[INSTAGRAM] Clicked {selector}")
                    created = True
                    break
                except:
                    continue

            if not created:
                logger.error("Could not open Instagram create")
                return False

            await page.wait_for_timeout(1500)

            # Select "Post" option
            post_option = page.locator("text=Post").first
            await post_option.click()
            await page.wait_for_timeout(1500)

            # Fill caption using textarea
            caption_selectors = [
                "textarea[aria-label='Write a caption...']",
                "textarea[placeholder='Write a caption...']",
                "div[contenteditable='true']"
            ]

            caption_filled = False
            for selector in caption_selectors:
                try:
                    caption = page.locator(selector).first
                    await caption.click()
                    await page.keyboard.type(content.content, delay=10)
                    logger.info(f"[INSTAGRAM] Filled caption via: {selector}")
                    caption_filled = True
                    break
                except:
                    continue

            if not caption_filled:
                logger.error("Could not fill Instagram caption")
                return False

            await page.wait_for_timeout(1000)

            # Click Share button - try multiple selectors
            share_selectors = [
                "button:has-text('Share')",
                '[data-testid="share_button"]',
                '.share-button'
            ]

            shared = False
            for selector in share_selectors:
                try:
                    logger.info(f"[INSTAGRAM] Trying share selector: {selector}")
                    share_btn = page.locator(selector).first
                    await share_btn.click(timeout=5000)
                    logger.info(f"[INSTAGRAM] Clicked Share via: {selector}")
                    shared = True
                    break
                except:
                    continue

            if not shared:
                logger.error("Could not click Instagram Share button")
                return False

            # Wait for post to complete
            await page.wait_for_timeout(3000)
            logger.info("✅ Instagram post successful")
            return True

        except Exception as e:
            logger.error(f"❌ Instagram posting failed: {e}")
            return False

    async def post_to_whatsapp(self, page: Page, content: PostContent) -> bool:
        """Send message via WhatsApp - multi-selector approach"""
        try:
            logger.info(f"💬 Sending WhatsApp message: {content.title}")

            # Navigate to WhatsApp Web if needed
            if "whatsapp.com" not in page.url:
                await page.goto("https://web.whatsapp.com/")
                await page.wait_for_load_state("networkidle")

            await page.wait_for_timeout(2000)

            # Find message input - try multiple selectors
            msg_selectors = [
                "div[contenteditable='true'][data-tab='10']",
                "[data-testid='input']",
                'div[role="textbox"]',
                "div[contenteditable='true']"
            ]

            msg_input = None
            for selector in msg_selectors:
                try:
                    logger.info(f"[WHATSAPP] Trying selector: {selector}")
                    msg_input = page.locator(selector).first
                    await msg_input.click()
                    logger.info(f"[WHATSAPP] Found input via: {selector}")
                    break
                except:
                    continue

            if not msg_input:
                logger.error("Could not find WhatsApp message input")
                return False

            await page.keyboard.type(content.content, delay=10)
            await page.wait_for_timeout(1000)

            # Click send button - try multiple selectors
            send_selectors = [
                "button[aria-label='Send']",
                "[data-testid='send']",
                'button[aria-label="Send message"]'
            ]

            sent = False
            for selector in send_selectors:
                try:
                    logger.info(f"[WHATSAPP] Trying send selector: {selector}")
                    send_btn = page.locator(selector).first
                    await send_btn.click(timeout=5000)
                    logger.info(f"[WHATSAPP] Clicked Send via: {selector}")
                    sent = True
                    break
                except:
                    continue

            if not sent:
                logger.error("Could not click WhatsApp Send button")
                return False

            # Wait for message to send
            await page.wait_for_timeout(2000)
            logger.info("✅ WhatsApp message sent successfully")
            return True

        except Exception as e:
            logger.error(f"❌ WhatsApp send failed: {e}")
            return False

    async def post_to_gmail(self, page: Page, content: PostContent) -> bool:
        """Send email via Gmail - multi-selector approach"""
        try:
            logger.info(f"📧 Sending Gmail: {content.title}")

            # Navigate to Gmail if needed
            if "mail.google.com" not in page.url:
                await page.goto("https://mail.google.com/")
                await page.wait_for_load_state("networkidle")

            await page.wait_for_timeout(2000)

            # Click compose button - try multiple selectors
            compose_selectors = [
                "button:has-text('Compose')",
                "[aria-label='Compose']",
                '[data-tooltip="Compose"]'
            ]

            composed = False
            for selector in compose_selectors:
                try:
                    logger.info(f"[GMAIL] Trying selector: {selector}")
                    compose_btn = page.locator(selector).first
                    await compose_btn.click(timeout=3000)
                    logger.info(f"[GMAIL] Clicked {selector}")
                    composed = True
                    break
                except:
                    continue

            if not composed:
                logger.error("Could not open Gmail compose")
                return False

            await page.wait_for_timeout(1500)

            # Fill recipient
            to_selectors = [
                "input[aria-label='To']",
                "input[placeholder='To']",
                "[role='combobox']"
            ]

            to_filled = False
            for selector in to_selectors:
                try:
                    to_field = page.locator(selector).first
                    await to_field.click()
                    await page.keyboard.type(content.from_user, delay=10)
                    logger.info(f"[GMAIL] Filled To via: {selector}")
                    to_filled = True
                    break
                except:
                    continue

            if not to_filled:
                logger.error("Could not fill Gmail To field")
                return False

            await page.wait_for_timeout(500)

            # Fill subject
            subject_field = page.locator("input[placeholder='Subject']")
            await subject_field.fill(content.title)
            await page.wait_for_timeout(500)

            # Fill body
            body_selectors = [
                "div[aria-label='Message body']",
                "div[role='textbox']",
                "div[contenteditable='true']"
            ]

            body_filled = False
            for selector in body_selectors:
                try:
                    body_field = page.locator(selector).first
                    await body_field.click()
                    await page.keyboard.type(content.content, delay=10)
                    logger.info(f"[GMAIL] Filled body via: {selector}")
                    body_filled = True
                    break
                except:
                    continue

            if not body_filled:
                logger.error("Could not fill Gmail body")
                return False

            await page.wait_for_timeout(1000)

            # Click send button - try multiple selectors
            send_selectors = [
                "button[aria-label='Send ']",
                "[data-tooltip='Send']",
                'button:has-text("Send")'
            ]

            sent = False
            for selector in send_selectors:
                try:
                    logger.info(f"[GMAIL] Trying send selector: {selector}")
                    send_btn = page.locator(selector).first
                    await send_btn.click(timeout=5000)
                    logger.info(f"[GMAIL] Clicked Send via: {selector}")
                    sent = True
                    break
                except:
                    continue

            if not sent:
                logger.error("Could not click Gmail Send button")
                return False

            # Wait for send to complete
            await page.wait_for_timeout(2000)
            logger.info("✅ Gmail sent successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Gmail send failed: {e}")
            return False

    async def take_error_screenshot(self, page: Page, content: PostContent, attempt: int) -> None:
        """Take screenshot on error"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"error_{content.platform}_{timestamp}_attempt{attempt}.png"
            filepath = self.logs_dir / filename

            await page.screenshot(path=str(filepath))
            logger.info(f"📸 Error screenshot saved: {filepath}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")

    async def post_with_retry(self, context: BrowserContext, content: PostContent) -> bool:
        """Attempt to post with retry logic"""
        page = await context.new_page()

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"\n🔄 Attempt {attempt}/{self.max_retries} - {content.platform}")

                # Route to appropriate platform
                if content.platform == 'linkedin':
                    success = await self.post_to_linkedin(page, content)
                elif content.platform == 'facebook':
                    success = await self.post_to_facebook(page, content)
                elif content.platform == 'twitter':
                    success = await self.post_to_twitter(page, content)
                elif content.platform == 'instagram':
                    success = await self.post_to_instagram(page, content)
                elif content.platform == 'whatsapp':
                    success = await self.post_to_whatsapp(page, content)
                elif content.platform == 'gmail':
                    success = await self.post_to_gmail(page, content)
                else:
                    logger.warning(f"Unknown platform: {content.platform}")
                    success = False

                if success:
                    await page.close()
                    return True
                else:
                    # Take screenshot on failure
                    await self.take_error_screenshot(page, content, attempt)

                    if attempt < self.max_retries:
                        wait_time = 2 ** attempt  # Exponential backoff
                        logger.info(f"⏳ Waiting {wait_time}s before retry...")
                        await asyncio.sleep(wait_time)

            except Exception as e:
                logger.error(f"Exception on attempt {attempt}: {e}")
                await self.take_error_screenshot(page, content, attempt)

                if attempt < self.max_retries:
                    wait_time = 2 ** attempt
                    logger.info(f"⏳ Waiting {wait_time}s before retry...")
                    await asyncio.sleep(wait_time)

        await page.close()
        return False

    def move_to_done(self, content: PostContent) -> bool:
        """Move successful post to /Done/"""
        try:
            destination = self.done_dir / f"processed_{content.filename}"
            shutil.move(str(content.filepath), str(destination))
            logger.info(f"✅ Moved to Done: {destination.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to move file to Done: {e}")
            return False

    async def process_file(self, filepath: Path) -> bool:
        """Process single file from /Approved"""
        logger.info(f"\n{'='*70}")
        logger.info(f"Processing: {filepath.name}")
        logger.info(f"{'='*70}")

        # Parse file
        content = self.parse_post_file(filepath)
        if not content:
            logger.error(f"Failed to parse {filepath.name}")
            return False

        logger.info(f"Platform: {content.platform}")
        logger.info(f"Title: {content.title}")
        logger.info(f"Content length: {len(content.content)} chars")

        # Post to platform with persistent context
        async with async_playwright() as p:
            # Use persistent context with /session folder
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(self.session_dir / content.platform),
                headless=False,  # Set to True for headless mode
                args=["--no-sandbox"]
            )

            # Attempt to post with retry
            success = await self.post_with_retry(context, content)

            await context.close()

        if success:
            self.move_to_done(content)
            logger.info(f"✅ Successfully posted and moved to Done")
            return True
        else:
            logger.error(f"❌ Failed after {self.max_retries} attempts")
            return False

    async def process_all_pending(self) -> None:
        """Process all files in /Approved"""
        files = list(self.approved_dir.glob("*.md"))

        if not files:
            logger.info("No files in /Approved folder")
            return

        logger.info(f"Found {len(files)} file(s) to process")

        results = {"success": 0, "failed": 0}

        for filepath in files:
            success = await self.process_file(filepath)
            if success:
                results["success"] += 1
            else:
                results["failed"] += 1

        logger.info(f"\n{'='*70}")
        logger.info("SUMMARY")
        logger.info(f"{'='*70}")
        logger.info(f"✅ Successful: {results['success']}")
        logger.info(f"❌ Failed: {results['failed']}")
        logger.info(f"Total: {results['success'] + results['failed']}")


async def main():
    """Main entry point"""
    executor = SocialMediaExecutor()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--all-pending":
            # Process all files in /Approved
            await executor.process_all_pending()
        else:
            # Process specific file
            filepath = Path(sys.argv[1])
            if filepath.exists():
                await executor.process_file(filepath)
            else:
                logger.error(f"File not found: {filepath}")
    else:
        print(__doc__)
        print("\nUsage:")
        print("  python scripts/social_media_executor_v2.py /Approved/facebook_draft_20260329_abc123.md")
        print("  python scripts/social_media_executor_v2.py --all-pending")


if __name__ == "__main__":
    asyncio.run(main())
