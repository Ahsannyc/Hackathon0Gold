#!/usr/bin/env python3
"""Quick test to check if all 6 platforms are logged in"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def check_platform(platform_name, url, check_selector):
    """Check if a platform loads with authenticated session"""
    try:
        session_path = Path(f"session/{platform_name}")
        
        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                str(session_path),
                headless=True,
                timeout=10000
            )
            page = await context.new_page()
            
            print(f"\n[{platform_name.upper()}]", end=" ")
            
            # Try to navigate with timeout
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=10000)
                
                # Check if logged in
                try:
                    await page.wait_for_selector(check_selector, timeout=3000)
                    print("✅ LOGGED IN")
                    result = "LOGGED_IN"
                except:
                    print("❌ NOT LOGGED IN (selector not found)")
                    result = "NOT_LOGGED_IN"
                    
            except Exception as e:
                print(f"❌ TIMEOUT/ERROR - {str(e)[:50]}")
                result = "ERROR"
            
            await context.close()
            return platform_name, result
            
    except Exception as e:
        print(f"\n[{platform_name.upper()}] ❌ ERROR - {e}")
        return platform_name, "ERROR"

async def main():
    print("=" * 60)
    print("Platform Login Status Check")
    print("=" * 60)
    
    platforms = [
        ("linkedin", "https://linkedin.com", "[data-test-id='global-nav']"),
        ("facebook", "https://facebook.com", "a[aria-label='Home']"),
        ("twitter", "https://twitter.com/home", "[data-testid='primaryColumn']"),
        ("instagram", "https://instagram.com", "[data-testid='side-nav']"),
        ("whatsapp", "https://web.whatsapp.com", "button[title='Start chat']"),
        ("gmail", "https://mail.google.com", "[data-tooltip='Compose']"),
    ]
    
    results = {}
    for platform, url, selector in platforms:
        name, status = await check_platform(platform, url, selector)
        results[name] = status
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("=" * 60)
    for platform, status in results.items():
        emoji = "✅" if status == "LOGGED_IN" else "❌"
        print(f"{emoji} {platform.upper():12} - {status}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
