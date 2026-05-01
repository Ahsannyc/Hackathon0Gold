#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail Label Organizer Skill
Creates labels and automatically moves emails from specific senders into organized folders

Usage:
  python skills/gmail_label_organizer.py --create-label "Hennessy, Sean" --from "Sean.Hennessy@amerisbank.com"
"""

import sys
import io
import argparse
from pathlib import Path
from typing import Optional

# Fix UTF-8 encoding on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials as OAuth2Credentials
from googleapiclient import discovery

from skills.audit_logger import AuditLogger
from skills.error_handler import SkillErrorHandler

class GmailLabelOrganizer:
    """Manage Gmail labels and organize emails"""

    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']  # Need modify for labels
    TOKEN_PATH = Path("watchers/.gmail_token.json")
    CREDS_PATH = Path("credentials.json")

    def __init__(self):
        self.service = None
        self.audit = AuditLogger()
        self.error_handler = SkillErrorHandler("gmail_label_organizer", ".")
        self.authenticate()

    def authenticate(self):
        """Authenticate with Gmail API for label management"""
        try:
            creds = None

            # Load existing token
            if self.TOKEN_PATH.exists():
                creds = OAuth2Credentials.from_authorized_user_file(
                    str(self.TOKEN_PATH), self.SCOPES)

            # If token doesn't have modify scope, we need to re-authenticate
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    print("Refreshing token for label management...")
                    creds.refresh(Request())
                else:
                    print("ERROR: Could not authenticate with Gmail API")
                    raise Exception("Authentication failed")

            self.service = discovery.build('gmail', 'v1', credentials=creds)
            print("[OK] Gmail authenticated for label management")

        except Exception as e:
            print(f"[ERROR] Authentication failed: {e}")
            raise

    def create_label(self, label_name: str) -> Optional[str]:
        """
        Create a Gmail label if it doesn't already exist
        Returns: label ID if created/exists, None if error
        """
        try:
            # Check if label already exists
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])

            for label in labels:
                if label['name'] == label_name:
                    print(f"[INFO] Label '{label_name}' already exists (ID: {label['id']})")
                    return label['id']

            # Create new label
            label_object = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }

            created_label = self.service.users().labels().create(
                userId='me',
                body=label_object
            ).execute()

            print(f"[OK] Created label: '{label_name}' (ID: {created_label['id']})")
            return created_label['id']

        except Exception as e:
            print(f"[ERROR] Failed to create label: {e}")
            return None

    def find_emails_from_sender(self, sender_email: str) -> list:
        """
        Find all emails from a specific sender
        Returns: list of message IDs
        """
        try:
            query = f'from:{sender_email}'
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=100  # Gmail API limit per request
            ).execute()

            messages = results.get('messages', [])
            print(f"[INFO] Found {len(messages)} emails from {sender_email}")
            return messages

        except Exception as e:
            print(f"[ERROR] Failed to find emails: {e}")
            return []

    def move_emails_to_label(self, message_ids: list, label_id: str, sender_email: str) -> int:
        """
        Move emails to a label (add label AND remove from inbox)
        Returns: number of emails successfully labeled
        """
        if not message_ids:
            print("[INFO] No emails to move")
            return 0

        success_count = 0
        total = len(message_ids)

        print(f"\n[PROCESSING] Moving {total} emails to label (removing from inbox)...")

        for i, msg in enumerate(message_ids, 1):
            try:
                msg_id = msg['id']
                # Add new label AND remove INBOX label (true move)
                self.service.users().messages().modify(
                    userId='me',
                    id=msg_id,
                    body={
                        'addLabelIds': [label_id],
                        'removeLabelIds': ['INBOX']  # Remove from inbox
                    }
                ).execute()
                success_count += 1

                # Progress indicator
                if i % 10 == 0 or i == total:
                    print(f"  [{i}/{total}] emails moved...")

            except Exception as e:
                print(f"  [WARN] Failed to move message {msg_id}: {e}")

        print(f"\n[OK] Successfully moved {success_count}/{total} emails (removed from inbox)")
        return success_count

    def organize_by_sender(self, label_name: str, sender_email: str) -> dict:
        """
        Complete workflow: Create label and move emails from sender
        Returns: summary dict
        """
        try:
            # Log skill start
            self.audit.log_action(
                action_type="skill_start",
                actor="gmail_label_organizer",
                target="system",
                status="started",
                details={"label_name": label_name, "sender_email": sender_email}
            )

            print("\n" + "="*60)
            print(f"GMAIL LABEL ORGANIZER")
            print("="*60)
            print(f"Label: {label_name}")
            print(f"Sender: {sender_email}")
            print("="*60 + "\n")

            # Step 1: Create label
            label_id = self.create_label(label_name)
            if not label_id:
                print("[ERROR] Failed to create label, aborting")
                # Log skill end failure
                self.audit.log_action(
                    action_type="skill_end",
                    actor="gmail_label_organizer",
                    target="system",
                    status="failed",
                    details={"error": "Label creation failed"}
                )
                return {"success": False, "error": "Label creation failed"}

            # Step 2: Find emails
            print(f"\n[SEARCHING] Looking for emails from {sender_email}...")
            messages = self.find_emails_from_sender(sender_email)

            if not messages:
                print(f"[INFO] No emails found from {sender_email}")
                # Log skill end - no emails found
                self.audit.log_action(
                    action_type="skill_end",
                    actor="gmail_label_organizer",
                    target="system",
                    status="completed",
                    details={
                        "label_created": True,
                        "label_name": label_name,
                        "emails_moved": 0,
                        "total_emails": 0
                    }
                )
                return {
                    "success": True,
                    "label_created": True,
                    "label_id": label_id,
                    "emails_moved": 0,
                    "message": f"Label '{label_name}' created, but no existing emails found"
                }

            # Step 3: Move emails
            moved_count = self.move_emails_to_label(messages, label_id, sender_email)

            print("\n" + "="*60)
            print("SUMMARY")
            print("="*60)
            print(f"Label Created: '{label_name}' (ID: {label_id})")
            print(f"Emails Moved: {moved_count}/{len(messages)}")
            print(f"Status: SUCCESS")
            print("="*60 + "\n")

            # Log skill end success
            self.audit.log_action(
                action_type="skill_end",
                actor="gmail_label_organizer",
                target="system",
                status="completed",
                details={
                    "label_created": True,
                    "label_name": label_name,
                    "emails_moved": moved_count,
                    "total_emails": len(messages)
                }
            )

            return {
                "success": True,
                "label_created": True,
                "label_name": label_name,
                "label_id": label_id,
                "total_emails_found": len(messages),
                "emails_moved": moved_count
            }
        except Exception as e:
            print(f"[ERROR] Organization failed: {e}")
            self.error_handler.write_error(e, context="email_organization_workflow", extra={"label_name": label_name, "sender_email": sender_email})
            self.audit.log_action(
                action_type="skill_end",
                actor="gmail_label_organizer",
                target="system",
                status="failed",
                details={"error": str(e)}
            )
            return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description='Organize Gmail emails by creating labels and moving messages'
    )
    parser.add_argument('--create-label', required=True, help='Label name to create')
    parser.add_argument('--from', dest='sender', required=True, help='Sender email address')

    args = parser.parse_args()

    try:
        organizer = GmailLabelOrganizer()
        result = organizer.organize_by_sender(args.create_label, args.sender)

        if result['success']:
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        print(f"\n[FATAL] {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
