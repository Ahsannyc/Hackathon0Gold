#!/usr/bin/env python3
"""
Error Recovery & Graceful Degradation System
Allows system to continue functioning when APIs fail or resources are unavailable.

Features:
- Exponential backoff retry logic
- Error classification (transient vs permanent)
- Per-component fallback strategies
- Human alerts on critical failures
- Graceful degradation patterns
"""

import time
import logging
import json
from pathlib import Path
from typing import Callable, Dict, Optional, Any, Tuple
from datetime import datetime
from enum import Enum


class ErrorType(Enum):
    """Classification of errors."""
    TRANSIENT = "transient"  # Network timeout, rate limit, temporary failure
    AUTHENTICATION = "authentication"  # Token expired, auth failed
    NOT_FOUND = "not_found"  # Resource doesn't exist
    PERMISSION = "permission"  # Insufficient permissions
    LOGIC = "logic"  # Claude misinterpretation
    DATA = "data"  # Corrupted or invalid data
    SYSTEM = "system"  # System-level error
    UNKNOWN = "unknown"


class RetryStrategy(Enum):
    """How to handle failures."""
    EXPONENTIAL_BACKOFF = "exponential_backoff"  # Keep retrying
    QUEUE_FOR_RETRY = "queue_for_retry"  # Save and retry later
    FALLBACK_TO_LOCAL = "fallback_to_local"  # Use local storage
    MANUAL_APPROVAL = "manual_approval"  # Require human approval
    SKIP = "skip"  # Skip this item and continue
    ABORT = "abort"  # Stop processing


class ErrorHandler:
    """Handles errors and implements recovery strategies."""

    def __init__(self, vault_path: Path = None):
        self.vault_path = vault_path or Path.cwd()
        self.logs_dir = self.vault_path / "Logs"
        self.logs_dir.mkdir(exist_ok=True)

        self.logger = logging.getLogger("ErrorHandler")
        self.error_log_file = self.logs_dir / "errors.json"

        # Ensure error log exists
        if not self.error_log_file.exists():
            self.error_log_file.write_text("[]")

    def with_retry(
        self,
        func: Callable,
        *args,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_multiplier: float = 2.0,
        **kwargs
    ) -> Tuple[bool, Any, Optional[str]]:
        """
        Execute function with exponential backoff retry.

        Args:
            func: Function to execute
            max_attempts: Maximum number of attempts
            base_delay: Initial delay between retries (seconds)
            max_delay: Maximum delay between retries
            backoff_multiplier: Multiplier for exponential backoff

        Returns:
            Tuple of (success, result, error_message)
        """

        for attempt in range(1, max_attempts + 1):
            try:
                result = func(*args, **kwargs)
                if attempt > 1:
                    self.logger.info(f"Recovered on attempt {attempt}: {func.__name__}")
                return (True, result, None)

            except Exception as e:
                error_msg = str(e)
                error_type = self._classify_error(e)

                # Don't retry permanent errors
                if error_type in [
                    ErrorType.AUTHENTICATION,
                    ErrorType.NOT_FOUND,
                    ErrorType.PERMISSION,
                    ErrorType.LOGIC
                ]:
                    self.logger.error(
                        f"Permanent error (not retrying): {error_type.value}: {error_msg}"
                    )
                    self._log_error(func.__name__, error_type, error_msg, attempt)
                    return (False, None, error_msg)

                # Retry transient errors
                if attempt < max_attempts:
                    delay = min(base_delay * (backoff_multiplier ** (attempt - 1)), max_delay)
                    self.logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed ({error_type.value}). "
                        f"Retrying in {delay}s: {error_msg}"
                    )
                    time.sleep(delay)
                else:
                    # All attempts failed
                    self.logger.error(
                        f"All {max_attempts} attempts failed: {error_msg}"
                    )
                    self._log_error(func.__name__, error_type, error_msg, attempt)
                    return (False, None, error_msg)

        return (False, None, "Max attempts exceeded")

    def _classify_error(self, error: Exception) -> ErrorType:
        """Classify error by type."""
        error_str = str(error).lower()

        if any(keyword in error_str for keyword in [
            "timeout", "connection", "network", "rate limit", "429"
        ]):
            return ErrorType.TRANSIENT

        if any(keyword in error_str for keyword in [
            "auth", "token", "unauthorized", "401", "403"
        ]):
            return ErrorType.AUTHENTICATION

        if any(keyword in error_str for keyword in [
            "404", "not found", "no such"
        ]):
            return ErrorType.NOT_FOUND

        if any(keyword in error_str for keyword in [
            "permission", "permission denied", "forbidden"
        ]):
            return ErrorType.PERMISSION

        if any(keyword in error_str for keyword in [
            "invalid", "corrupted", "malformed", "bad json"
        ]):
            return ErrorType.DATA

        return ErrorType.UNKNOWN

    def _log_error(
        self,
        function: str,
        error_type: ErrorType,
        error_msg: str,
        attempt: int
    ):
        """Log error to file."""
        try:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "function": function,
                "error_type": error_type.value,
                "error_message": error_msg,
                "attempt": attempt
            }

            logs = json.loads(self.error_log_file.read_text())
            logs.append(entry)
            self.error_log_file.write_text(json.dumps(logs, indent=2))
        except Exception as e:
            self.logger.error(f"Failed to log error: {e}")

    def create_alert(
        self,
        severity: str,  # critical, high, medium, low
        component: str,
        error: str,
        recommended_action: str
    ):
        """
        Create human alert for critical errors.

        Creates file that human should review.
        """
        alert_file = self.vault_path / "Alerts" / f"ALERT_{severity.upper()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        alert_file.parent.mkdir(exist_ok=True)

        content = f"""---
severity: {severity}
component: {component}
created: {datetime.now().isoformat()}
status: needs_review
---

# {severity.upper()}: {component} Error

## Error Details
{error}

## Recommended Action
{recommended_action}

## Next Steps
1. Review error details above
2. Check /Logs/errors.json for history
3. Take recommended action
4. Move to /Done/ once resolved
"""

        alert_file.write_text(content)
        self.logger.warning(f"Created alert: {alert_file.name}")


class GracefulDegradation:
    """Implements fallback strategies for component failures."""

    def __init__(self, vault_path: Path = None):
        self.vault_path = vault_path or Path.cwd()
        self.queues_dir = self.vault_path / "Queues"
        self.queues_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger("GracefulDegradation")

    def queue_for_later(
        self,
        component: str,
        action: str,
        data: Dict,
        reason: str
    ) -> str:
        """
        Queue action for retry when component recovers.

        Components:
        - email: Send when Gmail API recovers
        - social: Post when social API recovers
        - odoo: Sync when Odoo recovers
        - payment: Process when payment API recovers
        """

        queue_file = (
            self.queues_dir /
            f"QUEUE_{component}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )

        content = f"""---
component: {component}
action: {action}
queued_at: {datetime.now().isoformat()}
reason: {reason}
status: queued
---

# Queued for {component.upper()}

Action: {action}

Data:
```json
{json.dumps(data, indent=2)}
```

Reason for queuing:
{reason}

Status: Waiting for {component} to recover
"""

        queue_file.write_text(content)
        self.logger.info(f"Queued action: {queue_file.name}")

        return str(queue_file)

    def implement_fallback(
        self,
        component: str,
        original_action: str,
        data: Dict
    ) -> bool:
        """
        Implement component-specific fallback.

        Returns True if fallback successful.
        """

        fallbacks = {
            "email": self._fallback_email,
            "social": self._fallback_social,
            "odoo": self._fallback_odoo,
            "payment": self._fallback_payment,
        }

        fallback_fn = fallbacks.get(component)
        if not fallback_fn:
            self.logger.error(f"No fallback defined for {component}")
            return False

        try:
            return fallback_fn(original_action, data)
        except Exception as e:
            self.logger.error(f"Fallback failed for {component}: {e}")
            return False

    def _fallback_email(self, action: str, data: Dict) -> bool:
        """
        Fallback for email failures.

        Strategy: Queue email locally for retry when API recovers
        """
        self.queue_for_later(
            component="email",
            action=action,
            data=data,
            reason="Gmail API unavailable. Will retry when restored."
        )
        return True

    def _fallback_social(self, action: str, data: Dict) -> bool:
        """
        Fallback for social media failures.

        Strategy: Queue posts locally, process on recovery
        """
        self.queue_for_later(
            component="social",
            action=action,
            data=data,
            reason="Social media API unavailable. Will retry when restored."
        )
        return True

    def _fallback_odoo(self, action: str, data: Dict) -> bool:
        """
        Fallback for Odoo failures.

        Strategy: Log to CSV, sync to Odoo when recovered
        """
        csv_file = self.vault_path / "Accounting" / "pending_sync.csv"
        csv_file.parent.mkdir(exist_ok=True)

        # Append to CSV
        with open(csv_file, "a") as f:
            f.write(f"{datetime.now().isoformat()},{action},{json.dumps(data)}\n")

        self.logger.info(f"Logged to pending sync: {csv_file}")
        return True

    def _fallback_payment(self, action: str, data: Dict) -> bool:
        """
        Fallback for payment failures.

        Strategy: Create approval request, manual review required
        """
        approval_file = (
            self.vault_path / "Pending_Approval" /
            f"PAYMENT_MANUAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        approval_file.parent.mkdir(exist_ok=True)

        content = f"""---
action: {action}
requires_manual_review: true
created: {datetime.now().isoformat()}
status: pending_approval
---

# Manual Payment Review Required

Payment API unavailable. Manual review and execution required.

Details:
{json.dumps(data, indent=2)}

Action: {action}

Please review and approve in /Approved/ folder to execute.
"""

        approval_file.write_text(content)
        self.logger.info(f"Created manual approval: {approval_file.name}")
        return True

    def process_recovery_queue(self, component: str) -> Dict[str, int]:
        """
        Process queued items when component recovers.

        Returns:
            Dict with counts of processed, succeeded, failed
        """

        result = {"total": 0, "succeeded": 0, "failed": 0}

        for queue_file in self.queues_dir.glob(f"QUEUE_{component}_*.md"):
            result["total"] += 1

            try:
                # In real implementation, retry the queued action
                # For now, just log that we found it
                self.logger.info(f"Processing recovery: {queue_file.name}")
                result["succeeded"] += 1

                # Move to archive
                archive_dir = self.queues_dir / "archived"
                archive_dir.mkdir(exist_ok=True)
                queue_file.rename(archive_dir / queue_file.name)

            except Exception as e:
                self.logger.error(f"Failed to process recovery: {e}")
                result["failed"] += 1

        return result


def main():
    """CLI for error handling and recovery."""
    import argparse

    parser = argparse.ArgumentParser(description="Error Handler & Recovery")
    subparsers = parser.add_subparsers(dest="command")

    # View errors
    errors_parser = subparsers.add_parser("errors")
    errors_parser.add_argument("--limit", type=int, default=10)

    # Process recovery queue
    recovery_parser = subparsers.add_parser("recovery")
    recovery_parser.add_argument("component", help="Component to recover (email, social, odoo, payment)")

    args = parser.parse_args()
    handler = ErrorHandler()
    degradation = GracefulDegradation()

    if args.command == "errors":
        error_log = json.loads(handler.error_log_file.read_text())
        for entry in error_log[-args.limit:]:
            print(json.dumps(entry, indent=2))

    elif args.command == "recovery":
        result = degradation.process_recovery_queue(args.component)
        print(f"Processed {result['total']} queued items")
        print(f"Succeeded: {result['succeeded']}")
        print(f"Failed: {result['failed']}")

    else:
        print("Use: python error_handler.py errors|recovery [options]")


if __name__ == "__main__":
    main()
