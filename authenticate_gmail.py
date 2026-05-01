#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Gmail OAuth Authentication Script
Run this once to generate the token, then PM2 can use it continuously
"""

import sys
import io
from pathlib import Path

# Fix UTF-8 encoding on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials as OAuth2Credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
CREDS_PATH = Path("credentials.json")
TOKEN_PATH = Path("watchers/.gmail_token.json")

print("\n" + "="*60)
print("GMAIL OAUTH AUTHENTICATION")
print("="*60 + "\n")

# Check if credentials.json exists
if not CREDS_PATH.exists():
    print("ERROR: credentials.json not found!")
    print(f"Expected at: {CREDS_PATH.absolute()}\n")
    print("Get credentials.json from Google Cloud Console:")
    print("1. Go to: https://console.cloud.google.com")
    print("2. Create OAuth 2.0 credentials (Desktop application)")
    print("3. Download and save as credentials.json\n")
    sys.exit(1)

print(f"Found credentials.json")
print(f"Token will be saved to: {TOKEN_PATH.absolute()}\n")

try:
    print("Opening browser for authentication...")
    print("(If browser doesn't open, manually visit the URL shown)\n")

    # Run OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDS_PATH), SCOPES)
    creds = flow.run_local_server(port=0, open_browser=True)

    # Save token
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_PATH, 'w') as token:
        token.write(creds.to_json())

    print("\n" + "="*60)
    print("SUCCESS! Token saved and ready to use.")
    print("="*60)
    print(f"\nToken location: {TOKEN_PATH.absolute()}")
    print("\nYou can now run:")
    print("  pm2 start watchers/gmail_watcher.py --name gmail_watcher --interpreter python")
    print("\nOr simply:")
    print("  pm2 restart gmail_watcher\n")

except Exception as e:
    print(f"\nERROR during authentication: {e}\n")
    sys.exit(1)
