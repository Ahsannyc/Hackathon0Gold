#!/usr/bin/env python3
"""
Trigger Posts - Draft Post Generator
================================================================================
Generates Markdown posts with YAML frontmatter and saves them to
/Pending_Approval for manual review and orchestrator processing.

Features:
- Command-line interface with argparse
- YAML frontmatter generation
- Automatic timestamp in filename
- Platform detection and validation
- Default content templates
- Custom content support
- File deduplication
- Comprehensive logging

Usage:
    python scripts/trigger_posts.py --platform linkedin --content "Your post text"
    python scripts/trigger_posts.py -p facebook -c "Test post"
    python scripts/trigger_posts.py --platform twitter  # Uses default content

Supported Platforms:
    linkedin, facebook, twitter, instagram, whatsapp, gmail

Output:
    /Pending_Approval/POST_[timestamp]_[platform].md
"""

import argparse
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
import hashlib
import yaml


# ============================================================================
# CONSTANTS
# ============================================================================

SUPPORTED_PLATFORMS = {
    'linkedin': {
        'title': 'LinkedIn Professional Post',
        'default_content': 'Excited to share insights from our latest project! 🚀\n\n'
                          'Key takeaways:\n'
                          '• Innovation drives results\n'
                          '• Collaboration is key\n'
                          '• Continuous learning matters\n\n'
                          '#Leadership #Professional #Growth',
    },
    'facebook': {
        'title': 'Facebook Community Post',
        'default_content': 'Great news from the team! 🎉\n\n'
                          'We\'re excited to share an update with our community.\n\n'
                          'Stay tuned for more!\n#Community #Updates',
    },
    'twitter': {
        'title': 'Twitter Tweet',
        'default_content': 'Just launched something amazing! 🚀\n\n'
                          'Check it out and let us know what you think! '
                          '#Launch #Excited',
    },
    'instagram': {
        'title': 'Instagram Post',
        'default_content': 'Creating something beautiful ✨\n\n'
                          'Stay inspired and keep creating!\n\n'
                          '#Inspiration #Creative #Growth',
    },
    'whatsapp': {
        'title': 'WhatsApp Message',
        'default_content': 'Hey! 👋 Just wanted to reach out and share some updates. '
                          'How have you been?',
    },
    'gmail': {
        'title': 'Gmail Email',
        'default_content': 'Hi there,\n\n'
                          'I hope this email finds you well.\n\n'
                          'I wanted to reach out with some exciting news.\n\n'
                          'Looking forward to hearing from you!\n\n'
                          'Best regards',
    }
}


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging():
    """Configure logging"""
    os.makedirs("Logs", exist_ok=True)

    log_file = f"Logs/trigger_posts_{datetime.now().strftime('%Y-%m-%d')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)


logger = setup_logging()


# ============================================================================
# TRIGGER POSTS CLASS
# ============================================================================

class TriggerPosts:
    """Generate and save draft posts for approval"""

    def __init__(self):
        self.pending_approval_dir = Path("Pending_Approval")
        self.approved_dir = Path("Approved")
        self.logs_dir = Path("Logs")

        # Ensure directories exist
        for directory in [self.pending_approval_dir, self.approved_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        logger.info("Trigger Posts initialized")

    def validate_platform(self, platform: str) -> bool:
        """Validate platform is supported"""
        if platform.lower() not in SUPPORTED_PLATFORMS:
            logger.error(f"❌ Unsupported platform: {platform}")
            logger.error(f"   Supported: {', '.join(SUPPORTED_PLATFORMS.keys())}")
            return False
        return True

    def get_default_content(self, platform: str) -> str:
        """Get default content for platform"""
        platform = platform.lower()
        if platform in SUPPORTED_PLATFORMS:
            return SUPPORTED_PLATFORMS[platform]['default_content']
        return "Default post content"

    def get_platform_title(self, platform: str) -> str:
        """Get title for platform"""
        platform = platform.lower()
        if platform in SUPPORTED_PLATFORMS:
            return SUPPORTED_PLATFORMS[platform]['title']
        return f"{platform.title()} Post"

    def generate_filename(self, platform: str) -> str:
        """Generate unique filename with timestamp and hash"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        platform_short = platform.lower()[:3]
        # Random element for uniqueness
        unique_id = hashlib.md5(f"{timestamp}{platform}".encode()).hexdigest()[:6]
        return f"POST_{timestamp}_{platform_short}_{unique_id}.md"

    def generate_markdown(self, platform: str, content: str, title: Optional[str] = None) -> str:
        """Generate Markdown with YAML frontmatter"""
        platform = platform.lower()

        # Create YAML frontmatter
        frontmatter = {
            'platform': platform,
            'title': title or self.get_platform_title(platform),
            'from': 'trigger_posts',
            'type': f'{platform}_post',
            'priority': 'medium',
            'status': 'pending_approval',
            'created_at': datetime.now().isoformat(),
            'requires_approval': True
        }

        # Convert to YAML
        yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)

        # Build markdown
        markdown = f"""---
{yaml_str}---

# {frontmatter['title']}

{content}

---

## Status
- **Platform:** {platform.title()}
- **Status:** Pending Approval
- **Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Next Step:** Move to /Approved to trigger publishing via Master Orchestrator
"""

        return markdown

    def save_post(self, platform: str, content: str, title: Optional[str] = None) -> Optional[Path]:
        """Generate and save post to /Pending_Approval"""
        try:
            # Validate platform
            if not self.validate_platform(platform):
                return None

            # Generate filename
            filename = self.generate_filename(platform)
            filepath = self.pending_approval_dir / filename

            # Generate markdown
            markdown = self.generate_markdown(platform, content, title)

            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown)

            logger.info(f"✅ Post created: {filepath.name}")
            logger.info(f"   Platform: {platform.title()}")
            logger.info(f"   Content length: {len(content)} chars")
            logger.info(f"   Path: {filepath.absolute()}")

            return filepath

        except Exception as e:
            logger.error(f"❌ Failed to save post: {e}")
            return None

    def move_to_approved(self, filepath: Path) -> bool:
        """Move post from Pending_Approval to Approved (with POST_ prefix for orchestrator)"""
        try:
            # Create destination filename with POST_ prefix
            filename = filepath.name
            if not filename.startswith('POST_'):
                filename = f'POST_{filename}'

            destination = self.approved_dir / filename

            # Copy file
            with open(filepath, 'r', encoding='utf-8') as src:
                content = src.read()

            with open(destination, 'w', encoding='utf-8') as dst:
                dst.write(content)

            logger.info(f"✅ Moved to Approved: {destination.name}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to move to Approved: {e}")
            return False

    def print_post_preview(self, filepath: Path) -> None:
        """Print preview of created post"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            print("\n" + "="*70)
            print("📝 POST PREVIEW")
            print("="*70)
            print(content)
            print("="*70)
            print(f"✅ Saved to: {filepath.absolute()}")
            print("="*70 + "\n")

        except Exception as e:
            logger.error(f"Failed to print preview: {e}")


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Trigger Posts - Generate draft posts for approval',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/trigger_posts.py --platform linkedin --content "Excited to share!"
  python scripts/trigger_posts.py -p facebook -c "New product launch!"
  python scripts/trigger_posts.py --platform twitter  # Uses default content
  python scripts/trigger_posts.py -p instagram -c "Beautiful moment" --title "Instagram Post"
  python scripts/trigger_posts.py --platform linkedin --move  # Create and move to Approved
        """
    )

    parser.add_argument(
        '-p', '--platform',
        required=True,
        help='Target platform: linkedin, facebook, twitter, instagram, whatsapp, gmail'
    )

    parser.add_argument(
        '-c', '--content',
        default=None,
        help='Post content (uses default if not provided)'
    )

    parser.add_argument(
        '-t', '--title',
        default=None,
        help='Post title (optional, auto-generated if not provided)'
    )

    parser.add_argument(
        '-m', '--move',
        action='store_true',
        help='Move post to /Approved for orchestrator processing'
    )

    parser.add_argument(
        '--preview',
        action='store_true',
        default=True,
        help='Show post preview after creation (default: True)'
    )

    args = parser.parse_args()

    # Initialize
    trigger = TriggerPosts()

    # Get content (use default if not provided)
    content = args.content or trigger.get_default_content(args.platform)

    logger.info(f"\n{'='*70}")
    logger.info("TRIGGER POSTS - POST GENERATOR")
    logger.info(f"{'='*70}")
    logger.info(f"Platform: {args.platform}")
    logger.info(f"Content: {content[:50]}..." if len(content) > 50 else f"Content: {content}")
    logger.info(f"Title: {args.title or 'Auto-generated'}")
    logger.info(f"Move to Approved: {args.move}")

    # Save post
    filepath = trigger.save_post(args.platform, content, args.title)

    if not filepath:
        logger.error("Failed to create post")
        return 1

    # Show preview
    if args.preview:
        trigger.print_post_preview(filepath)

    # Move to Approved if requested
    if args.move:
        if trigger.move_to_approved(filepath):
            logger.info("✅ Post ready for orchestrator!")
            logger.info("   Master Orchestrator will detect and publish automatically")
        else:
            logger.error("Failed to move post to Approved")
            return 1

    logger.info(f"{'='*70}\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("\n📴 Trigger Posts stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
