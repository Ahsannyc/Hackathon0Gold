"""
Watcher Error Recovery Utility

Provides exponential backoff, error logging, and retry management for all watchers.
All watchers should instantiate WatcherErrorRecovery in __init__ and use its methods
for consistent error handling and recovery across all 6 active watchers.

Usage:
    from watchers.error_recovery import WatcherErrorRecovery

    class MyWatcher:
        def __init__(self):
            self.recovery = WatcherErrorRecovery("my_watcher", "/path/to/project")

        def run(self):
            retry_count = 0
            while True:
                try:
                    # Do work
                except Exception as e:
                    retry_count += 1
                    self.recovery.log_error(e, context=f"cycle_{cycle_count}_retry_{retry_count}")

                    if self.recovery.should_retry(retry_count):
                        delay = self.recovery.get_delay(retry_count)
                        logger.warning(f"Retry {retry_count}/3 in {delay}s")
                        time.sleep(delay)
                        continue
                    else:
                        logger.error("Max retries reached, resetting connection...")
                        retry_count = 0
                        self.reset_connection()  # reset logic
                else:
                    # Success - reset retry counter
                    retry_count = 0
"""

import logging
import traceback
import time
from pathlib import Path
from datetime import datetime, date
from typing import Optional

logger = logging.getLogger(__name__)


class WatcherErrorRecovery:
    """Provides exponential backoff and error logging for watchers."""

    def __init__(self, watcher_name: str, project_root: str):
        """
        Initialize error recovery for a specific watcher.

        Args:
            watcher_name: Name of the watcher (e.g., 'gmail', 'facebook_js')
            project_root: Path to project root directory
        """
        self.watcher_name = watcher_name
        self.project_root = Path(project_root)
        self.logs_dir = self.project_root / "Logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Backoff constants
        self.BACKOFF_BASE = 1  # Start at 1 second
        self.BACKOFF_MAX = 60  # Cap at 60 seconds
        self.MAX_RETRIES = 3   # Max 3 retries before reset

    def get_delay(self, retry_count: int) -> float:
        """
        Calculate exponential backoff delay.

        Formula: delay = min(BACKOFF_BASE * (2 ** retry_count), BACKOFF_MAX)
        Sequence: 1s, 2s, 4s, 8s... capped at 60s

        Args:
            retry_count: Which retry attempt (0-indexed or 1-indexed)

        Returns:
            Delay in seconds
        """
        delay = self.BACKOFF_BASE * (2 ** retry_count)
        return min(delay, self.BACKOFF_MAX)

    def should_retry(self, retry_count: int, max_retries: Optional[int] = None) -> bool:
        """
        Check if we should retry based on retry count.

        Args:
            retry_count: Current retry count
            max_retries: Max retries (default 3). Override per-call if needed.

        Returns:
            True if retry_count < max_retries, False otherwise
        """
        max_r = max_retries if max_retries is not None else self.MAX_RETRIES
        return retry_count < max_r

    def log_error(self, error: Exception, context: str = "", retry_count: int = 0) -> None:
        """
        Log an error to /Logs/error_{watcher}_{date}.log

        Creates append-only log file with timestamped entries. Each error includes:
        - Timestamp
        - Watcher name
        - Retry count and max retries
        - Context (e.g., cycle number, operation)
        - Error type and message
        - Full traceback

        Args:
            error: The exception that was caught
            context: Context string (e.g., 'cycle_42', 'get_messages')
            retry_count: Current retry attempt number (optional, for logging)
        """
        log_file = self.logs_dir / f"error_{self.watcher_name}_{date.today()}.log"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        error_type = type(error).__name__
        error_msg = str(error)
        tb_str = traceback.format_exc()

        # Build error log entry
        entry = (
            f"\n{'='*70}\n"
            f"[{timestamp}] [{self.watcher_name}] "
            f"[RETRY={retry_count}/{self.MAX_RETRIES}] [CONTEXT={context}]\n"
            f"{'='*70}\n"
            f"Error Type: {error_type}\n"
            f"Error Message: {error_msg}\n"
            f"\nTraceback:\n{tb_str}\n"
        )

        # Append to log file
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(entry)
        except Exception as write_error:
            # If we can't write the error log, at least log it to console
            logger.error(f"Failed to write error log: {write_error}")
            logger.error(f"Original error: {error_type}: {error_msg}")

    def reset_backoff(self) -> None:
        """Reset backoff state. Currently a no-op but included for completeness."""
        pass

    def format_retry_message(self, retry_count: int) -> str:
        """
        Format a user-friendly retry message.

        Args:
            retry_count: Current retry attempt

        Returns:
            Formatted string like "Retry 2/3 in 2s"
        """
        delay = self.get_delay(retry_count)
        return f"Retry {retry_count}/{self.MAX_RETRIES} in {delay:.1f}s"
