"""
Audit Logger - Centralized action tracking for Gold Tier skills
Records all skill actions to JSON audit trail with 90-day retention
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

class AuditLogger:
    """Centralized audit logging for all Gold Tier skills"""

    def __init__(self, project_root: str = "."):
        """Initialize audit logger and setup cleanup"""
        self.project_root = project_root
        self.logs_dir = Path(project_root) / "Logs"
        self.logs_dir.mkdir(exist_ok=True)

        # Run cleanup on init (lightweight - just checks dates)
        self.cleanup_old_logs(retain_days=90)

    def log_action(self, action_type: str, actor: str, target: str,
                   status: str, details: dict = None) -> None:
        """
        Log an action to the audit trail

        Args:
            action_type: "skill_start", "skill_end", "mcp_call", "error", "file_created"
            actor: skill name or system component
            target: file path, API endpoint, or "system"
            status: "started", "completed", "failed", "skipped"
            details: optional dict with additional context
        """
        timestamp = datetime.now().isoformat()

        entry = {
            "timestamp": timestamp,
            "action_type": action_type,
            "actor": actor,
            "target": target,
            "status": status,
            "details": details or {}
        }

        # Get today's log file
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.logs_dir / f"audit_{today}.json"

        # Read existing entries or create new list
        entries = []
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    entries = json.load(f)
            except (json.JSONDecodeError, IOError):
                entries = []

        # Append new entry
        entries.append(entry)

        # Write back (UTF-8 for cross-platform)
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"⚠️ Warning: Could not write audit log: {e}")

    def cleanup_old_logs(self, retain_days: int = 90) -> int:
        """
        Delete audit logs older than retain_days

        Args:
            retain_days: Number of days to retain (default 90)

        Returns:
            Number of files deleted
        """
        if not self.logs_dir.exists():
            return 0

        deleted = 0
        cutoff_date = datetime.now() - timedelta(days=retain_days)

        for log_file in self.logs_dir.glob("audit_*.json"):
            try:
                # Parse date from filename: audit_YYYY-MM-DD.json
                date_str = log_file.stem.replace("audit_", "")
                file_date = datetime.strptime(date_str, "%Y-%m-%d")

                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted += 1
            except (ValueError, OSError):
                # Skip files we can't parse or delete
                pass

        return deleted

    def get_weekly_summary(self, week_start):
        """
        Get aggregated summary of logs for a week

        Args:
            week_start: datetime object for Monday of the week

        Returns:
            dict with aggregated statistics
        """
        summary = {
            "total_actions": 0,
            "actions_by_type": {},
            "actions_by_actor": {},
            "success_rate": 0.0,
            "errors": []
        }

        all_entries = []

        # Read 7 days of logs
        for i in range(7):
            log_date = week_start + timedelta(days=i)
            date_str = log_date.strftime("%Y-%m-%d")
            log_file = self.logs_dir / f"audit_{date_str}.json"

            if log_file.exists():
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        entries = json.load(f)
                        all_entries.extend(entries)
                except (json.JSONDecodeError, IOError):
                    pass

        # Aggregate statistics
        summary["total_actions"] = len(all_entries)

        completed = 0
        for entry in all_entries:
            # By type
            action_type = entry.get("action_type", "unknown")
            summary["actions_by_type"][action_type] = \
                summary["actions_by_type"].get(action_type, 0) + 1

            # By actor
            actor = entry.get("actor", "unknown")
            summary["actions_by_actor"][actor] = \
                summary["actions_by_actor"].get(actor, 0) + 1

            # Track completions
            if entry.get("status") == "completed":
                completed += 1

            # Track errors
            if entry.get("status") == "failed":
                summary["errors"].append({
                    "timestamp": entry.get("timestamp"),
                    "actor": actor,
                    "error": entry.get("details", {}).get("error", "unknown")
                })

        # Calculate success rate
        if summary["total_actions"] > 0:
            summary["success_rate"] = completed / summary["total_actions"]

        return summary

    def get_latest_errors(self, limit: int = 10):
        """Get most recent errors from logs"""
        errors = []

        # Check last 7 days
        for i in range(7):
            log_date = datetime.now() - timedelta(days=i)
            date_str = log_date.strftime("%Y-%m-%d")
            log_file = self.logs_dir / f"audit_{date_str}.json"

            if log_file.exists():
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        entries = json.load(f)
                        for entry in entries:
                            if entry.get("status") == "failed":
                                errors.append({
                                    "timestamp": entry.get("timestamp"),
                                    "actor": entry.get("actor"),
                                    "error": entry.get("details", {}).get("error")
                                })
                except (json.JSONDecodeError, IOError):
                    pass

        return errors[:limit]


# Quick test
if __name__ == "__main__":
    logger = AuditLogger()
    logger.log_action("skill_start", "test_skill", "system", "started")
    logger.log_action("skill_end", "test_skill", "system", "completed",
                     {"duration_ms": 142})
    print("✓ Audit logger working")
