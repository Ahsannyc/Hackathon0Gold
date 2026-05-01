#!/usr/bin/env python3
"""
Comprehensive Audit Logger
Logs every action for compliance, debugging, and audit trails.

Features:
- JSON format with standardized schema
- Rolling 90-day retention
- Error tracking and stack traces
- Approval chain logging
- Searchable by action type, actor, timestamp
- Integration with all MCP calls and Claude operations
"""

import json
import logging
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any
from enum import Enum
import traceback


class ActionType(Enum):
    """Standardized action types for audit logging."""
    # Task execution
    TASK_START = "task_start"
    TASK_ITERATION = "task_iteration"
    TASK_COMPLETE = "task_complete"
    TASK_FAIL = "task_fail"

    # MCP operations
    MCP_CALL = "mcp_call"
    MCP_SUCCESS = "mcp_success"
    MCP_ERROR = "mcp_error"

    # Approvals
    APPROVAL_REQUEST = "approval_request"
    APPROVAL_GRANTED = "approval_granted"
    APPROVAL_REJECTED = "approval_rejected"

    # File operations
    FILE_CREATED = "file_created"
    FILE_MODIFIED = "file_modified"
    FILE_MOVED = "file_moved"
    FILE_DELETED = "file_deleted"

    # User actions
    USER_ACTION = "user_action"

    # System events
    SYSTEM_START = "system_start"
    SYSTEM_SHUTDOWN = "system_shutdown"
    SYSTEM_ERROR = "system_error"


class AuditLogger:
    """Main audit logging system."""

    def __init__(self, vault_path: Optional[Path] = None, retention_days: int = 90):
        self.vault_path = vault_path or Path.cwd()
        self.logs_dir = self.vault_path / "Logs"
        self.retention_days = retention_days
        self.logs_dir.mkdir(exist_ok=True)

        # Current audit file
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.audit_file = self.logs_dir / f"audit_{self.current_date}.json"

        # Initialize today's log file
        self._ensure_audit_file()

        # Setup Python logging too
        self._setup_python_logging()

    def _ensure_audit_file(self):
        """Ensure today's audit file exists."""
        if not self.audit_file.exists():
            self.audit_file.write_text("[]")

    def _setup_python_logging(self):
        """Setup Python logging to file."""
        log_file = self.logs_dir / "audit_system.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger("AuditLogger")

    def log_action(
        self,
        action_type: ActionType,
        description: str,
        actor: str = "system",
        target: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        approval_required: bool = False,
        approval_status: Optional[str] = None,
        error: Optional[str] = None,
        error_trace: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Log a single action.

        Args:
            action_type: Type of action from ActionType enum
            description: Human-readable description
            actor: Who performed the action (e.g., "claude_code", "user", "system")
            target: What was targeted (e.g., email address, file path)
            details: Additional structured data
            approval_required: Whether this action requires approval
            approval_status: Status if approval-related (pending, approved, rejected)
            error: Error message if action failed
            error_trace: Full stack trace if error

        Returns:
            The logged entry for reference
        """

        # Rotate file if date changed
        today = datetime.now().strftime("%Y-%m-%d")
        if today != self.current_date:
            self.current_date = today
            self.audit_file = self.logs_dir / f"audit_{today}.json"
            self._ensure_audit_file()

        # Create entry
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type.value,
            "description": description,
            "actor": actor,
            "target": target,
            "details": details or {},
            "approval_required": approval_required,
            "approval_status": approval_status,
            "status": "error" if error else "success",
            "error": error,
            "error_trace": error_trace
        }

        # Append to today's audit log
        try:
            entries = json.loads(self.audit_file.read_text())
            entries.append(entry)
            self.audit_file.write_text(json.dumps(entries, indent=2))

            # Log to Python logger too
            self.logger.info(
                f"{action_type.value}: {description} "
                f"(actor={actor}, status={'error' if error else 'success'})"
            )
        except Exception as e:
            self.logger.error(f"Failed to write audit log: {e}")

        return entry

    def log_task_start(self, task_id: str, prompt: str) -> Dict:
        """Log task execution start."""
        return self.log_action(
            ActionType.TASK_START,
            f"Task execution started: {task_id}",
            actor="ralph_wiggum",
            target=task_id,
            details={"task_id": task_id, "prompt": prompt[:100]}
        )

    def log_task_iteration(
        self,
        task_id: str,
        iteration: int,
        progress: str
    ) -> Dict:
        """Log task iteration."""
        return self.log_action(
            ActionType.TASK_ITERATION,
            f"Task iteration {iteration}: {progress}",
            actor="claude_code",
            target=task_id,
            details={"task_id": task_id, "iteration": iteration}
        )

    def log_task_complete(
        self,
        task_id: str,
        iterations: int,
        completion_type: str
    ) -> Dict:
        """Log successful task completion."""
        return self.log_action(
            ActionType.TASK_COMPLETE,
            f"Task completed: {task_id}",
            actor="system",
            target=task_id,
            details={
                "task_id": task_id,
                "iterations": iterations,
                "completion_type": completion_type
            }
        )

    def log_task_failure(
        self,
        task_id: str,
        iterations: int,
        error: str
    ) -> Dict:
        """Log task failure."""
        return self.log_action(
            ActionType.TASK_FAIL,
            f"Task failed: {task_id}",
            actor="system",
            target=task_id,
            error=error,
            details={"task_id": task_id, "iterations": iterations}
        )

    def log_mcp_call(
        self,
        mcp_server: str,
        tool_name: str,
        parameters: Dict,
        actor: str = "claude_code"
    ) -> Dict:
        """Log MCP tool invocation."""
        return self.log_action(
            ActionType.MCP_CALL,
            f"MCP call: {mcp_server}.{tool_name}",
            actor=actor,
            target=f"{mcp_server}.{tool_name}",
            details={
                "mcp_server": mcp_server,
                "tool_name": tool_name,
                "parameters": parameters
            }
        )

    def log_mcp_success(
        self,
        mcp_server: str,
        tool_name: str,
        result: Any
    ) -> Dict:
        """Log successful MCP call."""
        return self.log_action(
            ActionType.MCP_SUCCESS,
            f"MCP success: {mcp_server}.{tool_name}",
            actor="system",
            target=f"{mcp_server}.{tool_name}",
            details={
                "mcp_server": mcp_server,
                "tool_name": tool_name,
                "result": str(result)[:100]
            }
        )

    def log_mcp_error(
        self,
        mcp_server: str,
        tool_name: str,
        error: str,
        error_trace: Optional[str] = None
    ) -> Dict:
        """Log failed MCP call."""
        return self.log_action(
            ActionType.MCP_ERROR,
            f"MCP error: {mcp_server}.{tool_name}",
            actor="system",
            target=f"{mcp_server}.{tool_name}",
            error=error,
            error_trace=error_trace,
            details={
                "mcp_server": mcp_server,
                "tool_name": tool_name
            }
        )

    def log_approval_request(
        self,
        approval_id: str,
        action: str,
        details: Dict,
        created_by: str = "claude_code"
    ) -> Dict:
        """Log approval request creation."""
        return self.log_action(
            ActionType.APPROVAL_REQUEST,
            f"Approval requested: {action}",
            actor=created_by,
            target=approval_id,
            approval_required=True,
            approval_status="pending",
            details={"approval_id": approval_id, "action": action, **details}
        )

    def log_approval_granted(
        self,
        approval_id: str,
        action: str,
        approved_by: str
    ) -> Dict:
        """Log approval granted."""
        return self.log_action(
            ActionType.APPROVAL_GRANTED,
            f"Approval granted: {action}",
            actor=approved_by,
            target=approval_id,
            approval_status="approved",
            details={"approval_id": approval_id, "action": action}
        )

    def log_approval_rejected(
        self,
        approval_id: str,
        action: str,
        rejected_by: str
    ) -> Dict:
        """Log approval rejected."""
        return self.log_action(
            ActionType.APPROVAL_REJECTED,
            f"Approval rejected: {action}",
            actor=rejected_by,
            target=approval_id,
            approval_status="rejected",
            details={"approval_id": approval_id, "action": action}
        )

    def log_file_operation(
        self,
        operation: str,  # created, modified, moved, deleted
        file_path: str,
        actor: str = "claude_code"
    ) -> Dict:
        """Log file operation."""
        action_map = {
            "created": ActionType.FILE_CREATED,
            "modified": ActionType.FILE_MODIFIED,
            "moved": ActionType.FILE_MOVED,
            "deleted": ActionType.FILE_DELETED
        }

        action = action_map.get(operation, ActionType.FILE_CREATED)

        return self.log_action(
            action,
            f"File {operation}: {file_path}",
            actor=actor,
            target=file_path,
            details={"operation": operation, "file_path": file_path}
        )

    def cleanup_old_logs(self) -> int:
        """
        Remove audit logs older than retention period.

        Returns:
            Number of files deleted
        """
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        deleted_count = 0

        try:
            for log_file in self.logs_dir.glob("audit_*.json"):
                # Extract date from filename
                date_str = log_file.stem.replace("audit_", "")
                try:
                    file_date = datetime.strptime(date_str, "%Y-%m-%d")
                    if file_date < cutoff_date:
                        log_file.unlink()
                        deleted_count += 1
                        self.logger.info(f"Deleted old audit log: {log_file.name}")
                except ValueError:
                    pass  # Skip files that don't match date pattern
        except Exception as e:
            self.logger.error(f"Error cleaning up old logs: {e}")

        return deleted_count

    def get_logs_by_date(self, date: str) -> List[Dict]:
        """
        Retrieve all logs for a specific date.

        Args:
            date: Date string in format "YYYY-MM-DD"

        Returns:
            List of log entries for that date
        """
        log_file = self.logs_dir / f"audit_{date}.json"

        if log_file.exists():
            try:
                return json.loads(log_file.read_text())
            except Exception as e:
                self.logger.error(f"Error reading logs for {date}: {e}")
                return []

        return []

    def get_logs_by_actor(self, actor: str, date: Optional[str] = None) -> List[Dict]:
        """Filter logs by actor."""
        if date:
            logs = self.get_logs_by_date(date)
        else:
            # Get all logs from all files
            logs = []
            for log_file in self.logs_dir.glob("audit_*.json"):
                try:
                    logs.extend(json.loads(log_file.read_text()))
                except:
                    pass

        return [log for log in logs if log.get("actor") == actor]

    def get_logs_by_action_type(self, action_type: str) -> List[Dict]:
        """Filter logs by action type."""
        logs = []
        for log_file in self.logs_dir.glob("audit_*.json"):
            try:
                entries = json.loads(log_file.read_text())
                logs.extend([e for e in entries if e.get("action_type") == action_type])
            except:
                pass

        return logs

    def get_approval_chain(self, approval_id: str) -> List[Dict]:
        """Get all log entries related to an approval."""
        logs = []
        for log_file in self.logs_dir.glob("audit_*.json"):
            try:
                entries = json.loads(log_file.read_text())
                logs.extend([e for e in entries if e.get("target") == approval_id])
            except:
                pass

        return sorted(logs, key=lambda x: x.get("timestamp", ""))


def main():
    """CLI interface for audit logger."""
    import argparse

    parser = argparse.ArgumentParser(description="Audit Logger CLI")
    subparsers = parser.add_subparsers(dest="command")

    # View commands
    view_parser = subparsers.add_parser("view")
    view_parser.add_argument("--date", help="View logs for specific date (YYYY-MM-DD)")
    view_parser.add_argument("--actor", help="Filter by actor")
    view_parser.add_argument("--type", help="Filter by action type")

    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup")
    cleanup_parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    logger = AuditLogger()

    if args.command == "view":
        if args.date:
            logs = logger.get_logs_by_date(args.date)
        elif args.actor:
            logs = logger.get_logs_by_actor(args.actor)
        elif args.type:
            logs = logger.get_logs_by_action_type(args.type)
        else:
            logs = logger.get_logs_by_date(datetime.now().strftime("%Y-%m-%d"))

        print(json.dumps(logs, indent=2))

    elif args.command == "cleanup":
        deleted = logger.cleanup_old_logs()
        print(f"Deleted {deleted} old audit logs")

    else:
        print("Use: python audit_logger.py view|cleanup [options]")


if __name__ == "__main__":
    main()
