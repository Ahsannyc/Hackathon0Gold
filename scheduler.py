#!/usr/bin/env python3
"""
Scheduler - Gold Tier Task Scheduler
Runs weekly (Monday 8 AM), daily, and scheduled tasks
Integrates with skills like Weekly Audit Briefer
"""

import sys
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Callable, Dict, List

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [SCHEDULER] - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


class TaskScheduler:
    """Task scheduler with weekly, daily, and hourly support"""

    # Days: 0=Monday, 1=Tuesday, ..., 6=Sunday
    MONDAY = 0
    AUDIT_HOUR = 8  # 8 AM

    def __init__(self):
        self.last_audit = None
        self.last_daily = None
        self.scheduled_tasks = []

    def register_task(self, name: str, schedule: str, callable_func: Callable):
        """Register a scheduled task
        schedule: 'weekly', 'daily', 'hourly', or '<day>-<hour>' (e.g., 'monday-8')
        """
        self.scheduled_tasks.append({
            'name': name,
            'schedule': schedule,
            'func': callable_func,
            'last_run': None,
        })
        logger.info(f"[REGISTER] {name} - Schedule: {schedule}")

    def is_time_to_run_weekly_audit(self) -> bool:
        """SCHEDULER ITEM 2: Weekly Trigger Logic - Check if it's Monday 8 AM (within 1 hour window)"""
        now = datetime.now()
        is_monday = now.weekday() == self.MONDAY
        is_audit_hour = self.AUDIT_HOUR <= now.hour < self.AUDIT_HOUR + 1

        # Check if we've already run this week
        if self.last_audit:
            same_week = (now.date() - self.last_audit.date()).days < 7

            if same_week and is_monday:
                logger.debug("[ITEM 2] Already ran this week, skipping duplicate")
                return False

        result = is_monday and is_audit_hour
        if result:
            logger.info("[ITEM 2] Weekly trigger detected: Monday 8 AM window activated")
        return result

    def is_time_to_run_daily(self) -> bool:
        """Check if it's been 24 hours since last daily task"""
        now = datetime.now()

        if self.last_daily is None:
            return True

        hours_elapsed = (now - self.last_daily).total_seconds() / 3600
        return hours_elapsed >= 24

    def run_weekly_audit(self) -> bool:
        """Run weekly audit briefer"""
        try:
            logger.info("="*60)
            logger.info("[TASK] Running Weekly Audit Briefer")
            logger.info("="*60)

            # Import and run the briefer
            from skills.weekly_audit_briefer import WeeklyAuditBriefer

            briefer = WeeklyAuditBriefer()
            briefing_file = briefer.run()

            logger.info(f"[SUCCESS] Briefing: {briefing_file}")
            self.last_audit = datetime.now()
            return True

        except Exception as e:
            logger.error(f"[ERROR] Weekly audit failed: {e}", exc_info=True)
            return False

    def run_custom_task(self, task: Dict) -> bool:
        """Run a custom registered task"""
        try:
            logger.info(f"[TASK] Running {task['name']}")
            result = task['func']()
            task['last_run'] = datetime.now()
            logger.info(f"[SUCCESS] {task['name']}")
            return True
        except Exception as e:
            logger.error(f"[ERROR] {task['name']}: {e}")
            return False

    def check_and_run_tasks(self):
        """SCHEDULER ITEM 1: Daily Scheduler Checks - Run task dispatcher logic"""
        # Check weekly audit
        if self.is_time_to_run_weekly_audit():
            logger.info("[ITEM 1] Triggering weekly audit from scheduler checks...")
            self.run_weekly_audit()

        # Check custom registered tasks
        for task in self.scheduled_tasks:
            schedule = task['schedule'].lower()

            if schedule == 'weekly' and self.is_time_to_run_weekly_audit():
                logger.info(f"[ITEM 1] Triggering weekly task: {task['name']}")
                self.run_custom_task(task)
            elif schedule == 'daily' and self.is_time_to_run_daily():
                logger.info(f"[ITEM 1] Triggering daily task: {task['name']}")
                self.run_custom_task(task)

    def start(self, check_interval: int = 60):
        """Start scheduler loop
        check_interval: seconds between checks (default 60s = 1 minute)
        """
        logger.info("="*60)
        logger.info("TASK SCHEDULER - 2-Item Integration Started")
        logger.info("="*60)
        logger.info("[ITEM 1] Daily Scheduler Checks - Runs every cycle")
        logger.info("[ITEM 2] Weekly Trigger Logic - Monday 8:00 AM window")
        logger.info("="*60)
        logger.info(f"Check interval: {check_interval} seconds")
        logger.info("Weekly Audit Briefer: Monday 8:00 AM")
        logger.info("Press Ctrl+C to stop")
        logger.info("")

        try:
            cycle = 0
            while True:
                cycle += 1
                now = datetime.now()

                # Run task checks
                self.check_and_run_tasks()

                # Log periodic status
                if cycle % 60 == 0:  # Every 60 checks (1 hour)
                    logger.info(f"[STATUS] Scheduler running - {now.strftime('%Y-%m-%d %H:%M:%S')}")

                time.sleep(check_interval)

        except KeyboardInterrupt:
            logger.info("\n" + "="*60)
            logger.info("[STOP] Scheduler stopped by user")
            logger.info("="*60)
            sys.exit(0)
        except Exception as e:
            logger.error(f"[FATAL] Scheduler error: {e}", exc_info=True)
            sys.exit(1)


def main():
    """Main entry point"""
    scheduler = TaskScheduler()

    # Register weekly audit (runs Monday 8 AM)
    # (Already built-in, but can register custom weekly tasks here)

    logger.info("Starting Task Scheduler...")
    logger.info("Weekly Audit Briefer: Monday 8:00 AM")
    logger.info("")

    # Start scheduler loop
    scheduler.start(check_interval=60)


if __name__ == "__main__":
    main()
