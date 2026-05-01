#!/usr/bin/env python3
"""
Ralph Wiggum Loop - Gold Tier Multi-Step Task Runner
Extends from Silver Tier (10 iterations) to Gold Tier (20 iterations)
Supports multi-step workflow detection and cross-domain integration
"""

import os
import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, '.')


class RalphLoopRunner:
    """Gold Tier Ralph Loop with multi-step workflow support"""

    def __init__(self, project_root=".", max_iterations=20):
        self.project_root = Path(project_root)
        self.max_iterations = max_iterations
        self.needs_action_dir = self.project_root / "Needs_Action"
        self.plans_dir = self.project_root / "Plans"
        self.pending_approval_dir = self.project_root / "Pending_Approval"
        self.approved_dir = self.project_root / "Approved"
        self.done_dir = self.project_root / "Done"
        self.logs_dir = self.project_root / "Logs"

        # Create directories if they don't exist
        for d in [self.plans_dir, self.pending_approval_dir, self.approved_dir,
                  self.done_dir, self.logs_dir]:
            d.mkdir(exist_ok=True)

        # Import audit logger
        try:
            from skills.audit_logger import AuditLogger
            self.audit = AuditLogger(str(self.project_root))
        except ImportError:
            print("⚠️  AuditLogger not available")
            self.audit = None

        # Import cross domain integrator
        try:
            from skills.cross_domain_integrator import CrossDomainIntegrator
            self.integrator = CrossDomainIntegrator()
        except ImportError:
            print("⚠️  CrossDomainIntegrator not available")
            self.integrator = None

    def detect_multi_step_task(self, content):
        """
        Detect multi-step workflow type from task content

        Returns:
            {
                "workflow_type": "sales_workflow|financial_workflow|communication_workflow",
                "domain": "BUSINESS|PERSONAL",
                "steps": 5,
                "workflow": ["scan", "draft", "hitl", "approve", "publish"]
            }
        """
        content_lower = content.lower()

        # Sales workflow
        sales_keywords = ["sales", "client", "project", "opportunity", "partnership", "lead"]
        if any(kw in content_lower for kw in sales_keywords):
            return {
                "workflow_type": "sales_workflow",
                "domain": "BUSINESS",
                "steps": 5,
                "workflow": ["scan", "draft", "hitl", "approve", "publish"]
            }

        # Financial workflow
        financial_keywords = ["invoice", "payment", "amount", "due", "financial", "bill"]
        if any(kw in content_lower for kw in financial_keywords):
            return {
                "workflow_type": "financial_workflow",
                "domain": "PERSONAL",
                "steps": 6,
                "workflow": ["classify", "extract", "draft", "hitl", "approve", "execute"]
            }

        # Communication workflow
        communication_keywords = ["email", "message", "whatsapp", "facebook", "response"]
        if any(kw in content_lower for kw in communication_keywords):
            return {
                "workflow_type": "communication_workflow",
                "domain": "BUSINESS",
                "steps": 5,
                "workflow": ["extract", "classify", "draft", "hitl", "send"]
            }

        # Default
        return {
            "workflow_type": "generic_workflow",
            "domain": "BUSINESS",
            "steps": 3,
            "workflow": ["analyze", "plan", "execute"]
        }

    def scan_and_create_plans(self):
        """ITERATION 1: Scan Needs_Action and create plans"""
        print("\n🔄 ITERATION 1: SCAN & CLASSIFY")
        print("=" * 60)

        if not self.needs_action_dir.exists():
            print("  ℹ️  No Needs_Action directory found")
            return 0

        task_files = list(self.needs_action_dir.glob("*.md"))
        if not task_files:
            print("  ℹ️  No tasks in Needs_Action")
            return 0

        print(f"  📄 Found {len(task_files)} task(s)")

        for task_file in task_files:
            try:
                content = task_file.read_text()
                workflow = self.detect_multi_step_task(content)

                print(f"  📄 Processing: {task_file.name}")
                print(f"     🌟 Detected: {workflow['workflow_type']}")
                print(f"     📋 Domain: {workflow['domain']}")
                print(f"     📊 Steps: {workflow['steps']}")

                # Create plan
                plan_name = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{task_file.stem}.md"
                plan_path = self.plans_dir / plan_name
                plan_content = f"""---
type: plan
source: {task_file.name}
workflow_type: {workflow['workflow_type']}
domain: {workflow['domain']}
steps: {workflow['steps']}
created: {datetime.now().isoformat()}
---

# Plan for {task_file.stem}

## Workflow
{' → '.join(workflow['workflow'])}

## Details
Domain: {workflow['domain']}
Type: {workflow['workflow_type']}
Steps: {workflow['steps']}

## Original Task
{content}
"""
                plan_path.write_text(plan_content)
                print(f"  ✓ Plan created: {plan_name}")

                # Log to audit
                if self.audit:
                    self.audit.log_action(
                        "task_processing",
                        "ralph_loop_runner",
                        str(task_file),
                        "in_progress",
                        {
                            "workflow_type": workflow['workflow_type'],
                            "domain": workflow['domain'],
                            "plan_file": plan_name
                        }
                    )

            except Exception as e:
                print(f"  ❌ Error processing {task_file.name}: {e}")
                if self.audit:
                    self.audit.log_action(
                        "error",
                        "ralph_loop_runner",
                        str(task_file),
                        "failed",
                        {"error": str(e)}
                    )

        return len(task_files)

    def run_cross_domain_integration(self):
        """ITERATION 2: Cross Domain Integration"""
        print("\n🔄 ITERATION 2: CROSS DOMAIN INTEGRATION")
        print("=" * 60)

        if self.integrator:
            print("  🌐 Running Cross Domain Integrator")
            try:
                self.integrator.execute()
                print("  ✓ Cross Domain Integration complete")

                if self.audit:
                    self.audit.log_action(
                        "cross_domain_integration",
                        "ralph_loop_runner",
                        "system",
                        "completed",
                        {"integration": "complete"}
                    )
            except Exception as e:
                print(f"  ⚠️  Cross Domain Integration error: {e}")
        else:
            print("  ℹ️  Cross Domain Integrator not available")

    def process_approved_tasks(self):
        """ITERATION 3+: Process approved tasks"""
        print("\n🔄 ITERATION 3+: EXECUTE & COMPLETE")
        print("=" * 60)

        if not self.approved_dir.exists():
            print("  ℹ️  No Approved directory found")
            return 0

        approved_files = list(self.approved_dir.glob("*"))
        if not approved_files:
            print("  ℹ️  No approved tasks")
            return 0

        print(f"  📋 Found {len(approved_files)} approved task(s)")

        for task_file in approved_files:
            try:
                print(f"  ✓ Completing: {task_file.name}")

                # Move to Done
                done_file = self.done_dir / f"processed_{task_file.name}"
                task_file.rename(done_file)

                if self.audit:
                    self.audit.log_action(
                        "task_completion",
                        "ralph_loop_runner",
                        str(task_file),
                        "completed",
                        {"completed_at": datetime.now().isoformat()}
                    )

            except Exception as e:
                print(f"  ❌ Error completing {task_file.name}: {e}")

        return len(approved_files)

    def run_loop(self, max_iterations=None):
        """Run the complete Ralph Loop"""
        if max_iterations is None:
            max_iterations = self.max_iterations

        print("\n" + "=" * 60)
        print("🎯 RALPH WIGGUM LOOP - GOLD TIER (Multi-Step Tasks)")
        print("=" * 60)

        if self.audit:
            self.audit.log_action(
                "loop_start",
                "ralph_loop_runner",
                "system",
                "started",
                {"max_iterations": max_iterations}
            )

        for iteration in range(1, max_iterations + 1):
            print(f"\n📍 Iteration {iteration}/{max_iterations}")

            if iteration == 1:
                tasks = self.scan_and_create_plans()
            elif iteration == 2:
                self.run_cross_domain_integration()
                tasks = 1  # Continue to next iterations
            else:
                tasks = self.process_approved_tasks()

            if tasks == 0 and iteration > 2:
                print(f"\n✅ All tasks completed!")
                break

        print("\n" + "=" * 60)
        print("🏁 RALPH WIGGUM LOOP - COMPLETION")
        print("=" * 60)
        print(f"Iterations: {iteration}/{max_iterations}")
        print("Status: ✅ Complete")

        if self.audit:
            self.audit.log_action(
                "loop_end",
                "ralph_loop_runner",
                "system",
                "completed",
                {
                    "iterations": iteration,
                    "max_iterations": max_iterations,
                    "complete": True
                }
            )

        print("\n<promise>TASK_COMPLETE</promise>\n")

    @staticmethod
    def create_loop_state_file(state_file, max_iterations, prompt):
        """Create loop state file for tracking"""
        state = {
            "timestamp": datetime.now().isoformat(),
            "max_iterations": max_iterations,
            "prompt": prompt,
            "status": "running"
        }

        Path(state_file).write_text(json.dumps(state, indent=2))
        print(f"📝 State file: {state_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Ralph Wiggum Loop - Gold Tier Multi-Step Task Runner"
    )
    parser.add_argument("prompt", nargs="?", default="Process multi-step task in Needs_Action",
                       help="Task prompt for Claude")
    parser.add_argument("--max-iterations", type=int, default=20,
                       help="Maximum iterations (default: 20 for Gold Tier)")
    parser.add_argument("--process-needs-action", action="store_true",
                       help="Process all tasks in Needs_Action")

    args = parser.parse_args()

    runner = RalphLoopRunner(max_iterations=args.max_iterations)
    runner.run_loop(args.max_iterations)


if __name__ == "__main__":
    main()
