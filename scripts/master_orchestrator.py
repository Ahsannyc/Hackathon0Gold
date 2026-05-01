#!/usr/bin/env python3
"""
Master Orchestrator - Autonomous Social Media Publishing System
================================================================================
Monitors /Approved folder for POST_*.md files and autonomously publishes them
using Social Media Executor v2.0.

Features:
- Watchdog-based folder monitoring (5-second check interval)
- Automatic file detection (POST_* naming convention)
- Async execution with Social Media Executor v2.0
- Retry logic: 3 attempts with 5-minute cooldown
- Comprehensive logging to /Logs/orchestrator_[date].log
- Status tracking (processing, success, failed, retry)
- Event notifications (start, complete, error)

Usage:
    python scripts/master_orchestrator.py

Requirements:
    pip install watchdog pyyaml

Workflow:
    /Approved/POST_*.md
        ↓ (Watchdog detects)
    Social Media Executor v2.0
        ↓ Success
    /Done/processed_*.md

    /Approved/POST_*.md (Failed)
        ↓ Retry 3x
    5-minute cooldown
        ↓
    Retry again
"""

import asyncio
import os
import sys
import json
import yaml
import logging
import time
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import signal

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent


# ============================================================================
# ENUMS & DATA CLASSES
# ============================================================================

class FileStatus(Enum):
    """Status of a file being processed"""
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    RETRY = "retry"
    COOLDOWN = "cooldown"


@dataclass
class FileRecord:
    """Track status of a file"""
    filename: str
    filepath: str
    platform: str
    status: FileStatus
    attempts: int = 0
    last_attempt: Optional[str] = None
    next_retry: Optional[str] = None
    error_message: str = ""
    created_at: str = ""

    def to_dict(self):
        return {
            'filename': self.filename,
            'filepath': self.filepath,
            'platform': self.platform,
            'status': self.status.value,
            'attempts': self.attempts,
            'last_attempt': self.last_attempt,
            'next_retry': self.next_retry,
            'error_message': self.error_message,
            'created_at': self.created_at
        }


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging():
    """Configure logging for orchestrator"""
    os.makedirs("Logs", exist_ok=True)

    log_file = f"Logs/orchestrator_{datetime.now().strftime('%Y-%m-%d')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)


logger = setup_logging()


# ============================================================================
# MASTER ORCHESTRATOR CLASS
# ============================================================================

class MasterOrchestrator:
    """Orchestrates autonomous social media publishing"""

    def __init__(self):
        self.approved_dir = Path("Approved")
        self.done_dir = Path("Done")
        self.logs_dir = Path("Logs")
        self.status_file = self.logs_dir / f"status_{datetime.now().strftime('%Y-%m-%d')}.json"

        # Configuration
        self.max_retries = 3
        self.retry_cooldown = 300  # 5 minutes in seconds
        self.check_interval = 5  # seconds

        # State tracking
        self.file_records: Dict[str, FileRecord] = {}
        self.is_running = False

        # Ensure directories exist
        for directory in [self.approved_dir, self.done_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        logger.info("=" * 70)
        logger.info("Master Orchestrator v1.0 initialized")
        logger.info(f"Approved folder: {self.approved_dir.absolute()}")
        logger.info(f"Done folder: {self.done_dir.absolute()}")
        logger.info(f"Logs folder: {self.logs_dir.absolute()}")
        logger.info(f"Check interval: {self.check_interval} seconds")
        logger.info(f"Max retries: {self.max_retries}")
        logger.info(f"Retry cooldown: {self.retry_cooldown} seconds")
        logger.info("=" * 70)

    def detect_platform(self, filename: str) -> str:
        """Detect platform from filename or file content"""
        filename_lower = filename.lower()
        for platform in ['linkedin', 'facebook', 'twitter', 'instagram', 'whatsapp', 'gmail']:
            if platform in filename_lower:
                return platform
        return "unknown"

    def parse_post_file(self, filepath: Path) -> Optional[str]:
        """Extract platform from post file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 2:
                    try:
                        metadata = yaml.safe_load(parts[1]) or {}
                        platform = metadata.get('platform', self.detect_platform(filepath.name))
                        return platform
                    except yaml.YAMLError:
                        return self.detect_platform(filepath.name)

            return self.detect_platform(filepath.name)
        except Exception as e:
            logger.error(f"Error parsing {filepath.name}: {e}")
            return None

    def log_event(self, event_type: str, filename: str, details: Dict = None) -> None:
        """Log event to status file"""
        try:
            event = {
                'timestamp': datetime.now().isoformat(),
                'event': event_type,
                'filename': filename,
                'details': details or {}
            }

            # Append to status file
            events = []
            if self.status_file.exists():
                try:
                    with open(self.status_file, 'r') as f:
                        events = json.load(f)
                except:
                    events = []

            events.append(event)

            with open(self.status_file, 'w') as f:
                json.dump(events, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to log event: {e}")

    async def execute_social_media_executor(self, filepath: Path) -> bool:
        """Execute social_media_executor_v2.py for a file"""
        try:
            logger.info(f"🚀 Executing: {filepath.name}")

            # Run the social media executor
            result = subprocess.run(
                [sys.executable, "scripts/social_media_executor_v2.py", str(filepath)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                logger.info(f"✅ Executor succeeded: {filepath.name}")
                return True
            else:
                logger.error(f"❌ Executor failed: {filepath.name}")
                logger.error(f"   Error output: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error(f"❌ Executor timeout: {filepath.name}")
            return False
        except Exception as e:
            logger.error(f"❌ Exception executing {filepath.name}: {e}")
            return False

    async def process_file(self, filepath: Path) -> bool:
        """Process a single file with retry logic"""
        filename = filepath.name
        platform = self.parse_post_file(filepath)

        # Create or get file record
        if filename not in self.file_records:
            self.file_records[filename] = FileRecord(
                filename=filename,
                filepath=str(filepath),
                platform=platform or "unknown",
                status=FileStatus.PENDING,
                created_at=datetime.now().isoformat()
            )

        record = self.file_records[filename]

        # Check cooldown
        if record.status == FileStatus.COOLDOWN:
            if record.next_retry:
                next_retry_time = datetime.fromisoformat(record.next_retry)
                if datetime.now() < next_retry_time:
                    logger.info(f"⏳ Cooldown active for {filename}, retry at {record.next_retry}")
                    return False
                else:
                    # Cooldown expired, reset status
                    record.status = FileStatus.RETRY
                    logger.info(f"✅ Cooldown expired for {filename}, attempting retry")

        # Execute
        record.status = FileStatus.PROCESSING
        record.last_attempt = datetime.now().isoformat()
        record.attempts += 1

        logger.info(f"\n{'='*70}")
        logger.info(f"📋 Processing: {filename}")
        logger.info(f"   Platform: {record.platform}")
        logger.info(f"   Attempt: {record.attempts}/{self.max_retries + 1}")
        logger.info(f"{'='*70}")

        success = await self.execute_social_media_executor(filepath)

        if success:
            # Move to Done
            record.status = FileStatus.SUCCESS
            destination = self.done_dir / f"processed_{filename}"

            try:
                shutil.move(str(filepath), str(destination))
                logger.info(f"✅ SUCCESS: Moved to Done: {destination.name}")
                self.log_event("success", filename, {
                    'attempts': record.attempts,
                    'platform': record.platform
                })
                return True
            except Exception as e:
                logger.error(f"❌ Failed to move file: {e}")
                record.status = FileStatus.FAILED
                return False

        else:
            # Handle failure
            record.attempts += 1

            if record.attempts <= self.max_retries:
                # Schedule retry with cooldown
                record.status = FileStatus.COOLDOWN
                cooldown_until = datetime.now() + timedelta(seconds=self.retry_cooldown)
                record.next_retry = cooldown_until.isoformat()

                logger.warning(f"⚠️  Failed attempt {record.attempts - 1}/{self.max_retries}")
                logger.warning(f"⏳ Cooldown until: {cooldown_until.strftime('%Y-%m-%d %H:%M:%S')}")
                self.log_event("retry_scheduled", filename, {
                    'attempt': record.attempts - 1,
                    'next_retry': record.next_retry
                })
                return False
            else:
                # Max retries exceeded
                record.status = FileStatus.FAILED
                record.error_message = "Max retries exceeded"

                logger.error(f"❌ FAILED: Max retries exceeded ({self.max_retries} attempts)")
                logger.error(f"   File remains in /Approved: {filepath.name}")
                logger.error(f"   Manual review required")

                self.log_event("failed", filename, {
                    'attempts': record.attempts - 1,
                    'platform': record.platform,
                    'reason': 'max_retries_exceeded'
                })
                return False

    async def check_approved_folder(self) -> None:
        """Check /Approved folder for POST_* files"""
        if not self.approved_dir.exists():
            return

        # Find all POST_*.md files
        post_files = sorted(self.approved_dir.glob("POST_*.md"))

        for filepath in post_files:
            filename = filepath.name

            # Skip if already processed successfully
            if filename in self.file_records:
                record = self.file_records[filename]
                if record.status == FileStatus.SUCCESS:
                    continue

            # Process file
            await self.process_file(filepath)

    async def monitor_loop(self) -> None:
        """Main monitoring loop"""
        logger.info("🔍 Starting orchestrator monitoring loop...")
        logger.info(f"   Checking every {self.check_interval} seconds")

        self.is_running = True

        try:
            while self.is_running:
                try:
                    await self.check_approved_folder()
                    await asyncio.sleep(self.check_interval)
                except Exception as e:
                    logger.error(f"Error in monitoring loop: {e}")
                    await asyncio.sleep(self.check_interval)

        except KeyboardInterrupt:
            logger.info("\n📴 Orchestrator stopped by user")
            self.is_running = False
        except Exception as e:
            logger.error(f"Fatal error in monitoring loop: {e}")
            self.is_running = False

    def print_status(self) -> None:
        """Print current status"""
        if not self.file_records:
            logger.info("📭 No files tracked yet")
            return

        logger.info("\n" + "="*70)
        logger.info("📊 ORCHESTRATOR STATUS")
        logger.info("="*70)

        for filename, record in self.file_records.items():
            status_icon = {
                FileStatus.PENDING: "⏳",
                FileStatus.PROCESSING: "🔄",
                FileStatus.SUCCESS: "✅",
                FileStatus.FAILED: "❌",
                FileStatus.RETRY: "🔁",
                FileStatus.COOLDOWN: "❄️"
            }.get(record.status, "❓")

            logger.info(f"{status_icon} {filename:<40} | {record.status.value:<12} | "
                       f"Attempts: {record.attempts}")

            if record.next_retry:
                logger.info(f"   └─ Next retry: {record.next_retry}")

        logger.info("="*70)

    async def run(self) -> None:
        """Run the orchestrator"""
        logger.info("\n🚀 Master Orchestrator starting...")

        # Print startup info
        logger.info(f"Monitoring: {self.approved_dir.absolute()}")
        logger.info(f"File pattern: POST_*.md")
        logger.info(f"Check interval: {self.check_interval}s")
        logger.info(f"Max retries: {self.max_retries}")
        logger.info(f"Cooldown: {self.retry_cooldown}s (5 minutes)")

        # Run monitoring loop
        await self.monitor_loop()

        # Print final status
        self.print_status()


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

async def main():
    """Main entry point"""
    try:
        orchestrator = MasterOrchestrator()
        await orchestrator.run()
    except KeyboardInterrupt:
        logger.info("\n📴 Master Orchestrator stopped")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════╗
║        MASTER ORCHESTRATOR v1.0 - STARTUP                      ║
║   Autonomous Social Media Publishing Orchestrator              ║
╚════════════════════════════════════════════════════════════════╝

This orchestrator monitors /Approved/ for POST_*.md files and
autonomously publishes them using Social Media Executor v2.0.

Features:
  ✓ Real-time folder monitoring (5-second checks)
  ✓ Automatic file detection (POST_* pattern)
  ✓ Async execution with retry logic
  ✓ 3 retries with 5-minute cooldown between attempts
  ✓ Comprehensive logging
  ✓ Status tracking & event logging

Usage:
  python scripts/master_orchestrator.py

Requirements:
  pip install watchdog

Press Ctrl+C to stop

═══════════════════════════════════════════════════════════════════
""")

    asyncio.run(main())
