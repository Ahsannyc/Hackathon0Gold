#!/usr/bin/env python3
"""
Real-time Message Monitor
Watches Needs_Action folder and displays captured messages as they arrive
"""

import os
import sys
import time
import hashlib
from pathlib import Path
from datetime import datetime

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

NEEDS_ACTION_DIR = Path("Needs_Action")
MONITOR_INTERVAL = 5  # Check every 5 seconds

# Track files we've already seen
seen_files = set()

def read_message(file_path):
    """Read and parse message file"""
    try:
        content = file_path.read_text(encoding='utf-8')
        return content
    except Exception as e:
        return f"[ERROR reading file: {e}]"

def display_message(file_path, content):
    """Display captured message"""
    print("\n" + "="*80)
    print(f"📬 NEW MESSAGE CAPTURED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 File: {file_path.name}")
    print("="*80)
    print(content[:500])  # Show first 500 chars
    if len(content) > 500:
        print(f"\n... (Message truncated, {len(content)} total characters)")
    print("="*80 + "\n")

def monitor_messages():
    """Main monitoring loop"""
    print("\n" + "="*80)
    print("🔍 MESSAGE MONITOR STARTED")
    print("="*80)
    print(f"Monitoring: {NEEDS_ACTION_DIR.absolute()}")
    print(f"Check interval: {MONITOR_INTERVAL} seconds")
    print("Press Ctrl+C to stop\n")

    NEEDS_ACTION_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize with existing files
    for file_path in sorted(NEEDS_ACTION_DIR.glob("*.md")):
        if file_path.name not in ['FILE_PAKISTAN.md', 'FILE_PAKISTAN.md.md']:
            seen_files.add(file_path.name)

    try:
        while True:
            # Check for new files
            current_files = set(f.name for f in NEEDS_ACTION_DIR.glob("*.md"))
            new_files = current_files - seen_files

            if new_files:
                for filename in sorted(new_files):
                    file_path = NEEDS_ACTION_DIR / filename
                    if file_path.exists():
                        content = read_message(file_path)
                        display_message(file_path, content)
                        seen_files.add(filename)

            time.sleep(MONITOR_INTERVAL)

    except KeyboardInterrupt:
        print("\n" + "="*80)
        print("🛑 MONITOR STOPPED")
        print("="*80 + "\n")
        sys.exit(0)

if __name__ == "__main__":
    monitor_messages()
