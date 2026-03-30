#!/usr/bin/env python3
"""
Social Summary Generator - Silver Tier Agent Skill
Processes Facebook/Instagram messages and generates draft responses
Implements HITL (Human In The Loop) approval workflow

SKILL USAGE:
============

Command Line:
  python3 skills/social_summary_generator.py [--process] [--dry-run]

Agent Invocation:
  @Social Summary Generator process messages
  @Social Summary Generator scan

PM2 Schedule:
  pm2 start skills/social_summary_generator.py --name social_summary_generator --interpreter python3 --cron "0 * * * *"

WORKFLOW:
=========
1. Scan /Needs_Action for files with keywords: sales, client, project
2. Extract YAML metadata and message content
3. Reference Company_Handbook.md for tone/language guidelines
4. Draft response based on message type (Facebook/Instagram)
5. Save draft to /Plans/facebook_draft_[date]_[hash].md with YAML metadata
6. HITL: Move to /Pending_Approval for human review and approval
7. Once approved, ready for publishing

TESTING:
========
1. Create test file in /Needs_Action with keywords (facebook_*.md or instagram_*.md)
2. Run: python3 skills/social_summary_generator.py --dry-run
3. Check /Plans for draft files
4. Review YAML metadata and content
5. Move approved posts to /Approved folder
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
        logging.FileHandler("skills/logs/social_summary_generator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SocialSummaryGenerator:
    KEYWORDS = ['sales', 'client', 'project']
    NEEDS_ACTION_DIR = Path("Needs_Action")
    PLANS_DIR = Path("Plans")
    PENDING_APPROVAL_DIR = Path("Pending_Approval")
    APPROVED_DIR = Path("Approved")
    HANDBOOK_PATH = Path("Company_Handbook.md")

    # Response templates for different scenarios
    FACEBOOK_TEMPLATES = [
        "Thanks for reaching out! I'd love to discuss {service}. Let's connect!",
        "Great to hear from you! I can definitely help with {service}. Let's chat more.",
        "Appreciate the message! {service} is exactly what we specialize in. DM me!",
    ]

    INSTAGRAM_TEMPLATES = [
        "Thanks for the DM! Interested in {service}? Let's connect! 🙌",
        "Love this! {service} is our specialty. Let's chat more in DMs! 💼",
        "Great timing! I'd love to help with {service}. Slide into my DMs! 📨",
    ]

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.handbook_guidelines = self.load_handbook()
        self.processed_files = set()
        self.ensure_directories()
        self.audit = AuditLogger()
        self.error_handler = SkillErrorHandler("social_summary_generator", ".")

    def ensure_directories(self):
        """Ensure all required directories exist"""
        for directory in [self.NEEDS_ACTION_DIR, self.PLANS_DIR, self.PENDING_APPROVAL_DIR, self.APPROVED_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
        logger.info("✓ Directories verified")

    def load_handbook(self) -> str:
        """Load Company Handbook guidelines"""
        try:
            if self.HANDBOOK_PATH.exists():
                with open(self.HANDBOOK_PATH, 'r', encoding='utf-8') as f:
                    content = f.read()
                logger.info("✓ Loaded Company_Handbook.md")
                return content
            else:
                logger.warning("⚠ Company_Handbook.md not found")
                return "Default: Be polite, professional, and engaging in social messages."
        except Exception as e:
            logger.error(f"✗ Error loading handbook: {e}")
            return "Default: Be polite, professional, and engaging in social messages."

    def parse_markdown_yaml(self, filepath: Path) -> Tuple[Dict, str]:
        """Parse markdown file with YAML frontmatter"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract YAML frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1]
                    body = parts[2].strip()

                    try:
                        metadata = yaml.safe_load(yaml_content) or {}
                        return metadata, body
                    except yaml.YAMLError as e:
                        logger.warning(f"⚠ YAML parse error in {filepath.name}: {e}")
                        return {}, content
            return {}, content
        except Exception as e:
            logger.error(f"✗ Error parsing {filepath.name}: {e}")
            return {}, ""

    def extract_message_info(self, metadata: Dict, body: str) -> Optional[Dict]:
        """Extract message information from parsed markdown"""
        try:
            # Check if content matches keywords
            combined_text = f"{metadata.get('subject', '')} {body}".lower()
            has_keyword = any(kw in combined_text for kw in self.KEYWORDS)

            if not has_keyword:
                return None

            message_info = {
                'from': metadata.get('from', 'Unknown Contact'),
                'subject': metadata.get('subject', '(No Subject)'),
                'priority': metadata.get('priority', 'medium'),
                'type': metadata.get('type', 'social'),
                'platform': metadata.get('type', 'social'),
                'content': body,
                'source': metadata.get('source', 'unknown'),
                'received': metadata.get('received', datetime.now().isoformat()),
            }

            return message_info
        except Exception as e:
            logger.error(f"✗ Error extracting message info: {e}")
            return None

    def scan_needs_action(self) -> List[Tuple[Path, Dict, str]]:
        """Scan /Needs_Action for social media messages (facebook/instagram)"""
        messages = []
        try:
            if not self.NEEDS_ACTION_DIR.exists():
                logger.warning(f"⚠ {self.NEEDS_ACTION_DIR} does not exist")
                return messages

            # Find only facebook and instagram files
            markdown_files = sorted(self.NEEDS_ACTION_DIR.glob("facebook_*.md")) + \
                           sorted(self.NEEDS_ACTION_DIR.glob("instagram_*.md"))

            if not markdown_files:
                logger.info("ℹ No Facebook/Instagram files found in /Needs_Action")
                return messages

            for filepath in markdown_files:
                try:
                    metadata, body = self.parse_markdown_yaml(filepath)
                    message_info = self.extract_message_info(metadata, body)

                    if message_info:
                        messages.append((filepath, message_info, body))
                except Exception as e:
                    logger.warning(f"⚠ Error processing {filepath.name}: {e}")

            if messages:
                logger.info(f"✓ Found {len(messages)} social media messages with keywords")

            return messages
        except Exception as e:
            logger.error(f"✗ Error scanning /Needs_Action: {e}")
            return []

    def draft_response(self, message: Dict) -> str:
        """Draft response from message information"""
        try:
            # Extract service and benefit from message content
            content_lower = message['content'].lower()

            # Simple extraction based on keywords
            service = "our services"
            platform = message['platform']

            # Try to extract from content
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

            # Select template based on platform
            if platform == 'facebook':
                template = self.FACEBOOK_TEMPLATES[0]
            elif platform == 'instagram':
                template = self.INSTAGRAM_TEMPLATES[0]
            else:
                template = self.FACEBOOK_TEMPLATES[0]

            response = template.format(service=service)

            # Ensure polite tone (from handbook)
            response = self.ensure_polite_tone(response)

            return response
        except Exception as e:
            logger.error(f"✗ Error drafting response: {e}")
            return "Thanks for reaching out! Let's connect and discuss this opportunity."

    def ensure_polite_tone(self, text: str) -> str:
        """Ensure text follows Company Handbook guidelines"""
        # Handbook says: Always be polite in replies
        polite_replacements = {
            'need': 'would appreciate',
            'must': 'should',
            'can\'t': 'unable to',
            'don\'t': 'do not',
        }

        for word, replacement in polite_replacements.items():
            text = re.sub(rf'\b{word}\b', replacement, text, flags=re.IGNORECASE)

        return text

    def save_draft(self, message: Dict, response: str, source_file: Path) -> Optional[Path]:
        """Save draft response to /Plans with YAML metadata"""
        try:
            self.PLANS_DIR.mkdir(exist_ok=True)

            # Create filename
            timestamp = datetime.now().strftime("%Y%m%d")
            response_hash = hashlib.md5(response.encode()).hexdigest()[:6]
            safe_from = "".join(c for c in message['from'] if c.isalnum() or c in ' -_')[:20]
            platform = message['platform']
            filename = f"{platform}_draft_{timestamp}_{response_hash}_{safe_from}.md"
            filepath = self.PLANS_DIR / filename

            # Create markdown with YAML frontmatter
            keywords = message.get('keywords_found', [])
            keywords_str = ", ".join(keywords) if keywords else ""

            content = f"""---
type: {platform}_response
from: {message['from']}
subject: {platform.title()} Response Draft
source_message: {source_file.name}
priority: {message['priority']}
status: draft
requires_approval: true
created_at: {datetime.now().isoformat()}
keywords: {keywords_str}
---

# {platform.title()} Draft Response

**To:** {message['from']}

**Source:** {source_file.name}

**Priority:** {message['priority'].upper()}

**Status:** Awaiting Approval

---

## Message Summary

**Received:** {message.get('received', 'Unknown')}

**Keywords:** {keywords_str if keywords_str else 'None specified'}

**Category:** BUSINESS - {('Sales Lead' if 'sales' in keywords_str else 'Client Communication')}

---

## Drafted Response

{response}

---

## Original Message Context

**Subject:** {message['subject']}

**From:** {message['from']}

---

## Message Content

{message['content'][:500]}

---

## Action Required

This response draft is ready for review and approval.

- [ ] Review message context
- [ ] Review drafted response
- [ ] Verify tone (per Company_Handbook.md)
- [ ] Edit response if needed
- [ ] Approve draft
- [ ] Move to /Approved
- [ ] Send response

**Next Step:** Move this file to /Pending_Approval for HITL review.
"""

            if not self.dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"✓ Draft saved: {filepath}")
            else:
                logger.info(f"[DRY-RUN] Would save: {filepath}")

            return filepath
        except Exception as e:
            logger.error(f"✗ Error saving draft: {e}")
            return None

    def move_to_pending_approval(self, draft_file: Path, source_file: Path) -> bool:
        """Move draft to /Pending_Approval for HITL review"""
        try:
            self.PENDING_APPROVAL_DIR.mkdir(exist_ok=True)

            target_file = self.PENDING_APPROVAL_DIR / draft_file.name

            if not self.dry_run:
                # Copy draft to pending approval
                with open(draft_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Update status in metadata
                with open(target_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Update status field
                content = content.replace('status: draft', 'status: pending_approval')

                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                logger.info(f"✓ Moved to approval: {target_file.name}")
            else:
                logger.info(f"[DRY-RUN] Would move to: {target_file}")

            return True
        except Exception as e:
            logger.error(f"✗ Error moving to approval: {e}")
            return False

    def process_messages(self) -> Dict:
        """Process all identified social media messages"""
        logger.info("=" * 60)
        logger.info("SOCIAL SUMMARY GENERATOR - Processing Messages")
        logger.info("=" * 60)

        # Log skill start
        self.audit.log_action(
            action_type="skill_start",
            actor="social_summary_generator",
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

        try:
            messages = self.scan_needs_action()
            results['scanned'] = len(list(self.NEEDS_ACTION_DIR.glob("facebook_*.md"))) + \
                                len(list(self.NEEDS_ACTION_DIR.glob("instagram_*.md"))) if self.NEEDS_ACTION_DIR.exists() else 0
            results['messages_found'] = len(messages)

            for source_file, message_info, body in messages:
                try:
                    # Draft response
                    response = self.draft_response(message_info)
                    logger.info(f"✓ Drafted response for: {message_info['from']}")

                    # Save draft
                    draft_file = self.save_draft(message_info, response, source_file)
                    if draft_file:
                        results['drafts_created'] += 1

                        # Move to pending approval (HITL)
                        if self.move_to_pending_approval(draft_file, source_file):
                            results['pending_approval'] += 1
                            logger.info(f"✓ Response moved to /Pending_Approval for approval")
                except Exception as e:
                    logger.error(f"✗ Error processing message: {e}")
                    self.error_handler.write_error(e, context="message_processing", extra={"source": str(message_info.get('from', 'unknown'))})
                    results['errors'] += 1

        except Exception as e:
            logger.error(f"✗ Error in process_messages: {e}")
            self.error_handler.write_error(e, context="process_messages_workflow", extra={"messages_found": results['messages_found']})
            results['errors'] += 1

        # Log skill end
        self.audit.log_action(
            action_type="skill_end",
            actor="social_summary_generator",
            target="Plans/facebook_draft_*.md" if results['drafts_created'] > 0 else "system",
            status="completed" if results['errors'] == 0 else "failed",
            details={
                "messages_found": results['messages_found'],
                "drafts_created": results['drafts_created'],
                "pending_approval": results['pending_approval'],
                "errors": results['errors']
            }
        )

        # Print summary
        self.print_summary(results)
        return results

    def print_summary(self, results: Dict):
        """Print processing summary"""
        logger.info("=" * 60)
        logger.info("SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Files scanned:         {results['scanned']}")
        logger.info(f"Messages found:        {results['messages_found']}")
        logger.info(f"Drafts created:        {results['drafts_created']}")
        logger.info(f"Pending approval:      {results['pending_approval']}")
        logger.info(f"Errors:                {results['errors']}")
        logger.info("=" * 60)

        if results['pending_approval'] > 0:
            logger.info(f"\n📋 HITL REQUIRED: {results['pending_approval']} response(s) awaiting approval")
            logger.info(f"📂 Location: {self.PENDING_APPROVAL_DIR.absolute()}")

def main():
    parser = argparse.ArgumentParser(
        description="Social Summary Generator - Agent Skill for Silver Tier"
    )
    parser.add_argument('--process', action='store_true', help='Process messages and draft responses')
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode (no files created)')
    args = parser.parse_args()

    # If no args, default to process
    if not args.process and not args.dry_run:
        args.process = True

    dry_run = args.dry_run
    if dry_run:
        logger.info("[DRY-RUN MODE] No files will be created")

    generator = SocialSummaryGenerator(dry_run=dry_run)
    results = generator.process_messages()

    return 0 if results['errors'] == 0 else 1

if __name__ == "__main__":
    exit(main())
