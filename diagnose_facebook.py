#!/usr/bin/env python3
"""
Diagnostic script to see what Facebook page looks like in headless mode
"""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 80)
print("FACEBOOK HEADLESS DIAGNOSTIC")
print("=" * 80)

playwright = sync_playwright().start()

try:
    print("\n🔄 Launching browser...")
    browser = playwright.chromium.launch(
        headless=True,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-dev-shm-usage',
        ]
    )

    context = browser.new_context()
    page = context.new_page()

    print("📱 Navigating to facebook.com/messages/t/...")
    page.goto("https://www.facebook.com/messages/t/", timeout=20000)

    time.sleep(3)

    # Get page content
    print("\n📄 PAGE CONTENT ANALYSIS:")
    print("-" * 80)

    # Check title
    title = page.title()
    print(f"Page Title: {title}")

    # Check URL
    print(f"Current URL: {page.url}")

    # Get page text
    body_text = page.inner_text("body")
    print(f"\nPage Text Length: {len(body_text)} chars")

    if "sign in" in body_text.lower() or "log in" in body_text.lower():
        print("⚠️  WARNING: Page shows LOGIN REQUIRED")
        print("First 200 chars:", body_text[:200])
    elif "inbox" in body_text.lower() or "message" in body_text.lower():
        print("✅ Page shows messages/inbox content")
        print("First 200 chars:", body_text[:200])
    else:
        print("❓ Unknown page content")
        print("First 200 chars:", body_text[:200])

    # Check for message elements with different selectors
    print("\n🔍 CHECKING MESSAGE SELECTORS:")
    print("-" * 80)

    selectors = [
        '[data-testid*="message"]',
        '[data-testid="message_list"]',
        '[role="main"]',
        '.xuwq0c6',  # Facebook message container
        '[data-testid*="thread"]',
        '.x5jyip7',  # Common message div
    ]

    for selector in selectors:
        try:
            elements = page.query_selector_all(selector)
            print(f"✓ Selector '{selector}': Found {len(elements)} elements")
            if elements:
                first_text = elements[0].inner_text()[:50]
                print(f"  First element text: {first_text}...")
        except Exception as e:
            print(f"✗ Selector '{selector}': Error - {e}")

    # Check for any text mentioning conversations/messages
    print("\n🔎 KEYWORD SEARCH IN PAGE:")
    print("-" * 80)
    keywords = ["conversation", "message", "inbox", "thread", "chat"]
    for kw in keywords:
        count = body_text.lower().count(kw)
        if count > 0:
            print(f"✓ Found '{kw}': {count} times")

    context.close()

except Exception as e:
    print(f"❌ ERROR: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()

finally:
    try:
        browser.close()
    except:
        pass
    playwright.stop()

print("\n" + "=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)
