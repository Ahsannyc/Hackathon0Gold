#!/usr/bin/env python3
"""
Ralph Wiggum Loop Executor
Enables Claude to work autonomously on multi-step tasks until completion.

Pattern:
1. Orchestrator creates task state file in /Plans/TASK_<id>.md
2. Claude processes task, creates/updates files, makes progress
3. Claude signals completion via: <promise>TASK_COMPLETE</promise>
4. Or: Executor detects task file moved to /Done/
5. If incomplete after max iterations, human review required
6. Logs all state transitions for audit trail
"""

import os
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import subprocess
import sys

# Configuration
VAULT_PATH = Path(__file__).parent.parent
PLANS_FOLDER = VAULT_PATH / "Plans"
DONE_FOLDER = VAULT_PATH / "Done"
LOGS_FOLDER = VAULT_PATH / "Logs"
STATE_FOLDER = VAULT_PATH / ".ralph-state"

# Ensure folders exist
STATE_FOLDER.mkdir(exist_ok=True)
LOGS_FOLDER.mkdir(exist_ok=True)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOGS_FOLDER / "ralph_wiggum.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("RalphWiggum")


class TaskState:
    """Tracks task progress across iterations."""

    def __init__(self, task_id: str):
        self.task_id = task_id
        self.state_file = STATE_FOLDER / f"{task_id}.json"
        self.data = self._load()

    def _load(self) -> Dict:
        """Load or initialize state."""
        if self.state_file.exists():
            with open(self.state_file) as f:
                return json.load(f)
        return {
            "task_id": self.task_id,
            "created_at": datetime.now().isoformat(),
            "iterations": 0,
            "status": "pending",  # pending, running, completed, failed
            "completion_type": None,  # "promise" or "file_move"
            "last_claude_output": None,
            "iterations_log": []
        }

    def save(self):
        """Persist state to disk."""
        with open(self.state_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def log_iteration(self, iteration: int, output: str, task_file_moved: bool):
        """Record iteration details."""
        self.data["iterations"] = iteration
        self.data["last_claude_output"] = output[:500]  # First 500 chars
        self.data["iterations_log"].append({
            "iteration": iteration,
            "timestamp": datetime.now().isoformat(),
            "task_file_moved": task_file_moved,
            "status": "completed" if task_file_moved else "in_progress"
        })
        self.save()

    def mark_complete(self, completion_type: str):
        """Mark task as complete."""
        self.data["status"] = "completed"
        self.data["completion_type"] = completion_type
        self.data["completed_at"] = datetime.now().isoformat()
        self.save()

    def mark_failed(self, reason: str):
        """Mark task as failed."""
        self.data["status"] = "failed"
        self.data["failure_reason"] = reason
        self.data["failed_at"] = datetime.now().isoformat()
        self.save()


class RalphWiggumLoop:
    """Main executor for autonomous task loops."""

    def __init__(self, max_iterations: int = 10, iteration_timeout: int = 300):
        self.max_iterations = max_iterations
        self.iteration_timeout = iteration_timeout

    def find_task_file(self, task_id: str) -> Optional[Path]:
        """Find task file in Plans or Done folder."""
        # Check Plans folder
        for pattern in [f"TASK_{task_id}.md", f"{task_id}.md"]:
            for folder in [PLANS_FOLDER, DONE_FOLDER]:
                matches = list(folder.glob(pattern))
                if matches:
                    return matches[0]
        return None

    def task_completed_file_move(self, task_id: str) -> bool:
        """Check if task file has moved to /Done."""
        for pattern in ["*", "TASK_*", task_id + "*"]:
            done_files = list(DONE_FOLDER.glob(pattern))
            for f in done_files:
                if task_id in f.name:
                    return True
        return False

    def task_completed_promise(self, output: str) -> bool:
        """Check if output contains completion promise."""
        return "<promise>TASK_COMPLETE</promise>" in output or "TASK_COMPLETE" in output

    def run_task(self, task_id: str, prompt: str, use_promise: bool = False) -> Dict:
        """
        Execute a task with Ralph Wiggum loop.

        Args:
            task_id: Unique task identifier
            prompt: Claude prompt to execute
            use_promise: If True, wait for <promise>TASK_COMPLETE</promise>
                        If False, detect completion by file move to /Done

        Returns:
            Execution result with status and summary
        """
        logger.info(f"Starting Ralph Wiggum loop for task: {task_id}")
        state = TaskState(task_id)
        result = {
            "task_id": task_id,
            "status": "pending",
            "iterations": 0,
            "completion_type": None,
            "error": None,
            "summary": None
        }

        try:
            for iteration in range(1, self.max_iterations + 1):
                logger.info(f"Iteration {iteration}/{self.max_iterations}")

                # Create task file if doesn't exist
                task_file = self.find_task_file(task_id)
                if not task_file:
                    task_file = PLANS_FOLDER / f"TASK_{task_id}.md"
                    logger.info(f"Creating task file: {task_file}")

                # Run Claude on this iteration
                logger.info(f"Executing Claude prompt (iteration {iteration})")
                claude_result = self._run_claude(prompt, task_file, iteration)

                if claude_result["error"]:
                    logger.error(f"Claude execution failed: {claude_result['error']}")
                    state.mark_failed(f"Claude error: {claude_result['error']}")
                    result["error"] = claude_result["error"]
                    result["status"] = "failed"
                    return result

                output = claude_result.get("output", "")

                # Check completion
                file_moved = self.task_completed_file_move(task_id)
                promise_found = use_promise and self.task_completed_promise(output)

                state.log_iteration(iteration, output, file_moved or promise_found)

                if file_moved:
                    logger.info(f"✓ Task completed: File moved to /Done")
                    state.mark_complete("file_move")
                    result["status"] = "completed"
                    result["completion_type"] = "file_move"
                    result["iterations"] = iteration
                    self._audit_log_completion(task_id, iteration, "file_move")
                    return result

                if promise_found:
                    logger.info(f"✓ Task completed: Promise detected")
                    state.mark_complete("promise")
                    result["status"] = "completed"
                    result["completion_type"] = "promise"
                    result["iterations"] = iteration
                    self._audit_log_completion(task_id, iteration, "promise")
                    return result

                logger.info(f"Task incomplete. Continuing loop...")
                # Small delay between iterations to avoid API rate limits
                time.sleep(2)

            # Max iterations reached without completion
            logger.warning(f"Max iterations ({self.max_iterations}) reached without completion")
            state.mark_failed(f"Max iterations ({self.max_iterations}) reached")
            result["status"] = "incomplete"
            result["error"] = f"Task not completed after {self.max_iterations} iterations"
            result["iterations"] = self.max_iterations
            self._audit_log_completion(task_id, self.max_iterations, "timeout")

        except Exception as e:
            logger.exception(f"Ralph Wiggum loop error: {e}")
            state.mark_failed(str(e))
            result["status"] = "failed"
            result["error"] = str(e)

        return result

    def _run_claude(self, prompt: str, task_file: Path, iteration: int) -> Dict:
        """
        Execute Claude on the task.

        Returns dict with 'error' and 'output' keys.
        """
        try:
            # This would be called via Claude Code CLI
            # For now, return a template showing how to integrate

            # In practice, you would:
            # 1. Write state file for Claude to read
            # 2. Call: claude <prompt> --cwd <vault_path>
            # 3. Capture output
            # 4. Parse for completion signals

            logger.info(f"Prompt for Claude iteration {iteration}:")
            logger.info(f"  {prompt}")
            logger.info(f"  Task file: {task_file}")

            # Placeholder - would be replaced with actual Claude CLI call
            return {
                "error": None,
                "output": "Mock Claude output - implement actual CLI integration"
            }
        except Exception as e:
            return {
                "error": str(e),
                "output": None
            }

    def _audit_log_completion(self, task_id: str, iterations: int, completion_type: str):
        """Log task completion to audit trail."""
        audit_log = LOGS_FOLDER / "audit_tasks.json"

        entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "iterations": iterations,
            "completion_type": completion_type,
            "max_iterations": self.max_iterations
        }

        try:
            entries = []
            if audit_log.exists():
                with open(audit_log) as f:
                    entries = json.load(f)
            entries.append(entry)
            with open(audit_log, 'w') as f:
                json.dump(entries, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to log completion: {e}")


def main():
    """CLI interface for Ralph Wiggum executor."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Ralph Wiggum Loop Executor - Autonomous task completion"
    )
    parser.add_argument("task_id", help="Unique task identifier")
    parser.add_argument("prompt", help="Claude prompt to execute")
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=10,
        help="Maximum iterations before giving up (default: 10)"
    )
    parser.add_argument(
        "--use-promise",
        action="store_true",
        help="Wait for <promise>TASK_COMPLETE</promise> instead of file move"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Timeout per iteration in seconds (default: 300)"
    )

    args = parser.parse_args()

    executor = RalphWiggumLoop(
        max_iterations=args.max_iterations,
        iteration_timeout=args.timeout
    )

    result = executor.run_task(
        task_id=args.task_id,
        prompt=args.prompt,
        use_promise=args.use_promise
    )

    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "completed" else 1)


if __name__ == "__main__":
    main()
