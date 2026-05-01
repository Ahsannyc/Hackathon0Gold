"""
Skill Error Handler Utility

Provides error logging and manual fallback plan generation for all skills.
All skills should instantiate SkillErrorHandler in __init__ and use its methods
for consistent error handling across all 10 skills.

Two key capabilities:
1. write_error() - Log errors to /Errors/skill_error_{date}.md
2. write_manual_fallback() - Generate manual action checklist in /Plans/ when auto-processing fails

Usage:
    from skills.error_handler import SkillErrorHandler

    class MySkill:
        def __init__(self):
            self.error_handler = SkillErrorHandler("my_skill", "/path/to/project")

        def process(self):
            try:
                # Do work
            except Exception as e:
                self.error_handler.write_error(e, context="processing", extra={"file": "test.md"})

        def process_with_fallback(self):
            try:
                # Call MCP or external API
            except Exception as e:
                self.error_handler.write_error(e, context="mcp_call")
                self.error_handler.write_manual_fallback(
                    "Process the message manually",
                    context={"source_file": "message.md", "action": "draft_response"}
                )
"""

import logging
import traceback
from pathlib import Path
from datetime import datetime, date
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class SkillErrorHandler:
    """Provides error logging and manual fallback plan generation for skills."""

    def __init__(self, skill_name: str, project_root: str):
        """
        Initialize error handler for a specific skill.

        Args:
            skill_name: Name of the skill (e.g., 'auto_linkedin_poster')
            project_root: Path to project root directory
        """
        self.skill_name = skill_name
        self.project_root = Path(project_root)
        self.errors_dir = self.project_root / "Errors"
        self.plans_dir = self.project_root / "Plans"

        # Create directories if they don't exist
        self.errors_dir.mkdir(parents=True, exist_ok=True)
        self.plans_dir.mkdir(parents=True, exist_ok=True)

    def write_error(
        self,
        error: Exception,
        context: str = "",
        extra: Optional[Dict[str, Any]] = None,
        severity: str = "warning"
    ) -> None:
        """
        Write error to /Errors/skill_error_{date}.md

        Appends to a daily error log file with YAML frontmatter (one per day).
        Each error entry includes timestamp, skill name, error type, context, and traceback.

        Args:
            error: The exception that was caught
            context: Context string (e.g., 'processing_lead', 'mcp_call')
            extra: Optional dict with additional context (file names, data, etc.)
            severity: 'critical', 'error', 'warning' (default: 'warning')
        """
        error_file = self.errors_dir / f"skill_error_{date.today()}.md"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_type = type(error).__name__
        error_msg = str(error)
        tb_str = traceback.format_exc()

        # Build error entry
        entry = (
            f"## {self.skill_name.upper()} - {timestamp}\n"
            f"**Severity:** {severity}  \n"
            f"**Error Type:** {error_type}  \n"
            f"**Context:** {context}  \n"
        )

        if extra:
            entry += f"**Extra Context:**\n"
            for key, value in extra.items():
                entry += f"- {key}: {value}\n"

        entry += (
            f"\n**Error Message:**\n```\n{error_msg}\n```\n\n"
            f"**Traceback:**\n```\n{tb_str}```\n\n"
            f"---\n\n"
        )

        # Check if file exists to add header only once
        file_exists = error_file.exists()

        try:
            with open(error_file, 'a', encoding='utf-8') as f:
                # Write header only on first entry
                if not file_exists:
                    f.write(
                        f"---\n"
                        f"date: {date.today()}\n"
                        f"type: skill_error_log\n"
                        f"---\n\n"
                        f"# Skill Error Log - {date.today()}\n\n"
                    )
                f.write(entry)
        except Exception as write_error:
            logger.error(f"Failed to write error log: {write_error}")
            logger.error(f"Original error: {error_type}: {error_msg}")

    def write_manual_fallback(
        self,
        action_description: str,
        context: Optional[Dict[str, Any]] = None,
        priority: str = "medium"
    ) -> None:
        """
        Write manual fallback action to /Plans/manual_{skill}_{timestamp}.md

        Generated when automatic processing fails (e.g., MCP call, API error).
        Creates a checklist of manual steps for human operator to complete the task.

        Args:
            action_description: Description of what needs to be done (e.g., 'Draft response to Twitter DM')
            context: Optional dict with details (source_file, message_content, etc.)
            priority: 'low', 'medium', 'high' (default: 'medium')
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        manual_file = self.plans_dir / f"manual_{self.skill_name}_{timestamp}.md"

        # Build manual action plan
        content = (
            f"---\n"
            f"date: {date.today()}\n"
            f"time: {datetime.now().strftime('%H:%M:%S')}\n"
            f"skill: {self.skill_name}\n"
            f"type: manual_fallback\n"
            f"priority: {priority}\n"
            f"---\n\n"
            f"# Manual Fallback Action Required\n\n"
            f"**Skill:** {self.skill_name}  \n"
            f"**Priority:** {priority}  \n"
            f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"## What Needs to be Done\n\n{action_description}\n\n"
        )

        # Add context if provided
        if context:
            content += "## Context Details\n\n"
            for key, value in context.items():
                content += f"**{key.replace('_', ' ').title()}:** {value}\n\n"

        # Add checklist template
        content += (
            "## Action Checklist\n\n"
            "- [ ] Review the details above\n"
            "- [ ] Complete the required action manually\n"
            "- [ ] Move completed item to /Done/ folder\n"
            "- [ ] Delete this file once action is complete\n"
        )

        try:
            with open(manual_file, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Manual fallback created: {manual_file.name}")
        except Exception as write_error:
            logger.error(f"Failed to write manual fallback: {write_error}")

    def check_directories_exist(self) -> bool:
        """
        Check if /Errors/ and /Plans/ directories exist and are writable.

        Returns:
            True if both directories exist and are writable
        """
        if not self.errors_dir.exists():
            return False
        if not self.plans_dir.exists():
            return False
        return True

    def get_latest_errors(self, limit: int = 10) -> list:
        """
        Get most recent error entries from today's error log.

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of error entries (as strings)
        """
        error_file = self.errors_dir / f"skill_error_{date.today()}.md"
        if not error_file.exists():
            return []

        try:
            with open(error_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Split by error headers and return last N entries
                entries = content.split("## ")[1:]  # Skip header
                return entries[-limit:]
        except Exception as e:
            logger.error(f"Failed to read error log: {e}")
            return []
