#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail OAuth Authentication with MODIFY scope
Run this to upgrade token for label management (create, move, organize)
"""

import sys
import io
from pathlib import Path

# Fix UTF-8 encoding on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']  # Full modify access
CREDS_PATH = Path("credentials.json")
TOKEN_PATH = Path("watchers/.gmail_token.json")

print("\n" + "="*60)
print("GMAIL OAUTH - UPGRADE TO MODIFY SCOPE")
print("="*60 + "\n")

print("This will upgrade your token to allow:")
print("  - Creating labels/folders")
print("  - Moving emails between folders")
print("  - Organizing inbox\n")

if not CREDS_PATH.exists():
    print("ERROR: credentials.json not found!")
    sys.exit(1)

try:
    print("Opening browser for authentication...")
    print("(You may see permission request for 'Manage your Gmail')\n")

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDS_PATH), SCOPES)
    creds = flow.run_local_server(port=0, open_browser=True)

    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_PATH, 'w') as token:
        token.write(creds.to_json())

    print("\n" + "="*60)
    print("SUCCESS! Token upgraded with MODIFY permissions.")
    print("="*60)
    print(f"\nToken location: {TOKEN_PATH.absolute()}")
    print("\nYou can now:")
    print("  - Create labels in Gmail")
    print("  - Move emails to folders")
    print("  - Organize your inbox\n")

except Exception as e:
    print(f"\nERROR: {e}\n")
    sys.exit(1)
