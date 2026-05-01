#!/usr/bin/env python3
"""
Twitter Post Generator - Gold Tier Skill
Processes Twitter DM messages and generates draft responses
Implements HITL (Human In The Loop) approval workflow
"""

import os
import re
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import hashlib
import yaml
import argparse

from skills.audit_logger import AuditLogger
from skills.error_handler import SkillErrorHandler

# Setup logging
os.makedirs("skills/logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("skills/logs/twitter_post_generator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TwitterPostGenerator:
    KEYWORDS = ['sales', 'client', 'project']
    NEEDS_ACTION_DIR = Path("Needs_Action")
    PLANS_DIR = Path("Plans")
    PENDING_APPROVAL_DIR = Path("Pending_Approval")
    APPROVED_DIR = Path("Approved")

    # Response templates for Twitter
    TWITTER_TEMPLATES = [
        "Thanks for reaching out! I'd love to discuss {service}. Let's DM! 🙌",
        "Great to hear! {service} is exactly what we specialize in. Let's connect!",
        "Appreciate the message! I can definitely help with {service}. DM me! 💼",
    ]

    DM_TEMPLATES = [
        "Thanks for the message! Interested in {service}? Let's chat more.",
        "Love this! {service} is our specialty. Let's discuss this opportunity.",
        "Great timing! I'd love to help with {service}. Let's keep this conversation going.",
    ]

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.processed_files = set()
        self.ensure_directories()
        self.audit = AuditLogger()
        self.error_handler = SkillErrorHandler("twitter_post_generator", ".")

    def ensure_directories(self):
        """Ensure all required directories exist"""
        for directory in [self.NEEDS_ACTION_DIR, self.PLANS_DIR, self.PENDING_APPROVAL_DIR, self.APPROVED_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
        logger.info("Directories verified")

    def parse_markdown_yaml(self, filepath: Path) -> Tuple[Dict, str]:
        """Parse markdown file with YAML frontmatter"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1]
                    body = parts[2].strip()

                    try:
                        metadata = yaml.safe_load(yaml_content) or {}
                        return metadata, body
                    except yaml.YAMLError as e:
                        logger.warning(f"YAML parse error in {filepath.name}: {e}")
                        return {}, content
            return {}, content
        except Exception as e:
            logger.error(f"Error parsing {filepath.name}: {e}")
            return {}, ""

    def extract_message_info(self, metadata: Dict, body: str) -> Optional[Dict]:
        """Extract message information"""
        try:
            combined_text = f"{metadata.get('subject', '')} {body}".lower()
            has_keyword = any(kw in combined_text for kw in self.KEYWORDS)

            if not has_keyword:
                return None

            message_info = {
                'from': metadata.get('from', 'Unknown User'),
                'source': metadata.get('source', 'twitter'),
                'platform': metadata.get('platform', 'twitter'),
                'content': body,
                'priority': metadata.get('priority', 'medium'),
                'received': metadata.get('received', datetime.now().isoformat()),
            }

            return message_info
        except Exception as e:
            logger.error(f"Error extracting message info: {e}")
            return None

    def scan_needs_action(self) -> List[Tuple[Path, Dict, str]]:
        """Scan /Needs_Action for Twitter DM messages"""
        messages = []
        try:
            if not self.NEEDS_ACTION_DIR.exists():
                logger.warning(f"{self.NEEDS_ACTION_DIR} does not exist")
                return messages

            # Find only Twitter files
            markdown_files = sorted(self.NEEDS_ACTION_DIR.glob("twitter_*.md"))

            if not markdown_files:
                logger.info("No Twitter files found in /Needs_Action")
                return messages

            for filepath in markdown_files:
                try:
                    metadata, body = self.parse_markdown_yaml(filepath)
                    message_info = self.extract_message_info(metadata, body)

                    if message_info:
                        messages.append((filepath, message_info, body))
                except Exception as e:
                    logger.warning(f"Error processing {filepath.name}: {e}")

            if messages:
                logger.info(f"Found {len(messages)} Twitter messages with keywords")

            return messages
        except Exception as e:
            logger.error(f"Error scanning /Needs_Action: {e}")
            return []

    def draft_response(self, message: Dict) -> str:
        """Draft response from message"""
        try:
            content_lower = message['content'].lower()

            service = "our services"

            if 'invoice' in content_lower:
                service = "invoice management solutions"
            elif 'payment' in content_lower:
                service = "payment solutions"
            elif 'sales' in content_lower:
                service = "sales enablement"
            elif 'client' in content_lower:
                service = "client relationship management"
            elif 'project' in content_lower:
                service = "project management expertise"

            # Use DM template
            template = self.DM_TEMPLATES[0]
            response = template.format(service=service)

            return response
        except Exception as e:
            logger.error(f"Error drafting response: {e}")
            return "Thanks for reaching out! Let's discuss this opportunity."

    def save_draft(self, message: Dict, response: str, source_file: Path) -> Optional[Path]:
        """Save draft to /Plans"""
        try:
            ts = datetime.now().strftime("%Y%m%d")
            msg_id = hashlib.md5(response.encode()).hexdigest()[:8]
            filename = self.PLANS_DIR / f"twitter_draft_{ts}_{msg_id}.md"

            keywords_str = "sales, client, project"

            draft_content = f"""---
source: twitter
from: {message.get('from', 'Unknown')}
timestamp: {datetime.now().isoformat()}
source_message: {source_file.name}
priority: {message.get('priority', 'medium')}
status: draft
requires_approval: true
keywords: {keywords_str}
---

## Original Message

{message['content']}

## Generated Response

{response}

## Action Required

This response draft is ready for review and approval.

- [ ] Review message context
- [ ] Review drafted response
- [ ] Approve response
- [ ] Send response

**Next Step:** Move this file to /Pending_Approval for HITL review.
"""

            if not self.dry_run:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(draft_content)
                logger.info(f"Draft saved: {filename}")

            return filename
        except Exception as e:
            logger.error(f"Error saving draft: {e}")
            return None

    def move_to_pending_approval(self, draft_file: Path, source_file: Path) -> bool:
        """Move draft to /Pending_Approval for HITL review"""
        try:
            self.PENDING_APPROVAL_DIR.mkdir(exist_ok=True)

            target_file = self.PENDING_APPROVAL_DIR / draft_file.name

            if not self.dry_run:
                with open(draft_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                content = content.replace('status: draft', 'status: pending_approval')

                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                logger.info(f"Moved to approval: {target_file.name}")
            else:
                logger.info(f"[DRY-RUN] Would move to: {target_file}")

            return True
        except Exception as e:
            logger.error(f"Error moving to approval: {e}")
            return False

    def process_messages(self) -> Dict:
        """Process all Twitter messages"""
        # Log skill start
        self.audit.log_action(
            action_type="skill_start",
            actor="twitter_post_generator",
            target="system",
            status="started",
            details={"dry_run": self.dry_run}
        )

        results = {
            'scanned': 0,
            'messages_found': 0,
            'drafts_created': 0,
            'pending_approval': 0,
            'errors': 0,
        }

        messages = self.scan_needs_action()
        results['scanned'] = len(messages)

        for source_file, message_info, body in messages:
            try:
                results['messages_found'] += 1

                response = self.draft_response(message_info)

                draft_file = self.save_draft(message_info, response, source_file)

                if draft_file:
                    results['drafts_created'] += 1

                    if self.move_to_pending_approval(draft_file, source_file):
                        results['pending_approval'] += 1
                        logger.info("Response moved to /Pending_Approval for approval")
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                self.error_handler.write_error(e, context="message_processing", extra={"source": str(message_info.get('from', 'unknown'))})
                results['errors'] += 1

        # Log skill end
        self.audit.log_action(
            action_type="skill_end",
            actor="twitter_post_generator",
            target="Plans/twitter_*.md" if results['drafts_created'] > 0 else "system",
            status="completed" if results['errors'] == 0 else "failed",
            details={
                "messages_found": results['messages_found'],
                "drafts_created": results['drafts_created'],
                "pending_approval": results['pending_approval'],
                "errors": results['errors']
            }
        )

        self.print_summary(results)
        return results

    def print_summary(self, results: Dict):
        """Print processing summary"""
        logger.info("=" * 60)
        logger.info("TWITTER POST GENERATOR - SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Messages found:        {results['messages_found']}")
        logger.info(f"Drafts created:        {results['drafts_created']}")
        logger.info(f"Pending approval:      {results['pending_approval']}")
        logger.info(f"Errors:                {results['errors']}")
        logger.info("=" * 60)

        if results['pending_approval'] > 0:
            logger.info(f"\nHTIL REQUIRED: {results['pending_approval']} response(s) awaiting approval")
            logger.info(f"Location: {self.PENDING_APPROVAL_DIR.absolute()}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Twitter Post Generator')
    parser.add_argument('--process', action='store_true', help='Process messages')
    parser.add_argument('--dry-run', action='store_true', help='Dry run (no files modified)')

    args = parser.parse_args()
    dry_run = args.dry_run

    generator = TwitterPostGenerator(dry_run=dry_run)
    results = generator.process_messages()

    return 0 if results['errors'] == 0 else 1


if __name__ == "__main__":
    exit(main())
