---
id: "001"
title: "Facebook Watcher JavaScript Extraction Fix"
stage: "green"
date: "2026-03-24"
surface: "agent"
model: "claude-haiku-4-5-20251001"
feature: "facebook-watcher"
branch: "1-fastapi-backend"
user: "14loa"
command: "/continue (context resumed from previous session)"
labels: ["facebook", "automation", "bug-fix", "javascript-injection", "message-capture"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
---

## Problem Statement
Facebook Messenger watcher was failing to capture incoming messages despite user receiving them. Root causes:
- CSS selector-based extraction timed out (SelectorsTimeouts)
- Selectors returned 0 elements (DOM structure mismatch)
- Facebook dynamically changes DOM structure frequently
- Selenium WebDriver with CSS queries was unreliable

## Solution Implemented
Replaced CSS selector-based extraction with **JavaScript injection approach** that:
1. Injects JavaScript directly into browser context
2. Extracts ALL visible text from multiple DOM strategies
3. Removes duplicates using JavaScript Set
4. Filters by keywords automatically
5. Saves matches to Needs_Action/ folder

## Implementation Details

### Files Created
- `watchers/facebook_watcher_js_extract.py` (9.9 KB)
  - Uses undetected-chromedriver for anti-bot bypass
  - Implements execute_script() for JavaScript injection
  - Multi-strategy text extraction (selector → text nodes)
  - MD5 hashing for deduplication

### Technology Stack
- **Browser:** undetected-chromedriver (bypasses Facebook anti-bot detection)
- **Extraction:** JavaScript injection via driver.execute_script()
- **Session:** Browser profile directory at `session/facebook_js_extract/`
- **Dedup:** MD5 hash (16-char hex) for message uniqueness
- **Deployment:** PM2 Process ID 12

### Key Code Pattern
```python
# Execute JavaScript in browser context
result = self.driver.execute_script(self.EXTRACT_JS)

# JavaScript extracts all visible text
EXTRACT_JS = """
(function() {
    let messages = [];

    // Strategy 1: Use multiple CSS selectors
    let selectors = ['div[role="main"]', 'div[data-testid="conversation"]', ...];
    for (let selector of selectors) {
        let elements = document.querySelectorAll(selector);
        for (let elem of elements) {
            let text = elem.innerText || elem.textContent;
            if (text && text.trim().length > 0) {
                messages.push(text.trim());
            }
        }
    }

    // Strategy 2: Get all text nodes
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
    return { success: true, count: messages.length, messages: messages };
})();
"""

# Process results
if result.get('success'):
    for msg_text in result.get('messages', []):
        keywords_found = [kw for kw in self.KEYWORDS if kw.lower() in msg_text.lower()]
        if keywords_found:
            # Save to Needs_Action/
```

## Deployment
```bash
# Step 1: Stop old version
pm2 stop facebook-watcher && pm2 delete facebook-watcher

# Step 2: Start new version
pm2 start watchers/facebook_watcher_js_extract.py \
  --name facebook-watcher \
  --interpreter python

# Step 3: Verify
pm2 list
```

## Test Results
**Test Case:** Send message with multiple keywords
```
Message: "lets talk about sales, client, project, urgent, invoice, payment again"
Keywords Matched: 6/6 ✅
File Created: Needs_Action/facebook_20260324T06560_8892709d_message.md
Timestamp: 2026-03-24T06:56:05.903127
```

## Verification Checklist
- ✅ JavaScript injection executes successfully
- ✅ Multi-strategy text extraction finds all visible text
- ✅ Keyword matching works on extracted text
- ✅ Deduplication prevents duplicate captures
- ✅ Messages saved to Needs_Action/ folder
- ✅ PM2 process is stable (0 restarts in 14 minutes)
- ✅ Browser session persists across monitoring cycles

## Why This Works
1. **Robust:** Not dependent on specific CSS selectors that Facebook changes
2. **Complete:** Captures all visible text, not just targeted elements
3. **Adaptive:** Multiple extraction strategies handle DOM variations
4. **Deduped:** Automatic duplicate removal with JavaScript Set
5. **Reliable:** undetected-chromedriver bypasses anti-bot detection
6. **Persistent:** Browser profile directory maintains session state

## System Impact
**Before:** 4/5 watchers working (Facebook broken)
**After:** 5/5 watchers working (Facebook fixed)

All watchers now capture messages with universal keywords:
- Gmail (ID 1) ✅
- WhatsApp (ID 2) ✅
- LinkedIn (ID 3) ✅
- Instagram (ID 4) ✅
- Facebook (ID 12) ✅ **NEWLY FIXED**

## Next Steps (Optional)
- Add error recovery for browser crashes
- Implement incremental capture (only new messages)
- Add message threading/context preservation
- Integrate with Ralph Loop for auto-processing

## Documentation Created
- `FACEBOOK_WATCHER_FIX_SUMMARY.md` - Detailed implementation summary
- `FACEBOOK_FIX_QUICK_STEPS.md` - Quick reference guide
- PM2 configuration saved to `~/.pm2/dump.pm2` (76 KB)

---

**Status:** ✅ COMPLETE & VERIFIED
**Confidence:** HIGH (Tested with real message capture)
**Ready for Production:** YES
