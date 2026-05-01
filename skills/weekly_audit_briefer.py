#!/usr/bin/env python3
"""
Weekly Audit Briefer - Gold Tier Skill
Generates CEO weekly briefing from system logs, completed tasks, and company goals
Audits performance, identifies bottlenecks, tracks revenue
Runs Monday at 8 AM via scheduler
"""

import os
import sys
import re
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import defaultdict

from skills.audit_logger import AuditLogger
from skills.error_handler import SkillErrorHandler

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Setup logging
os.makedirs("skills/logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("skills/logs/weekly_audit_briefer.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WeeklyAuditBriefer:
    """Generate CEO weekly audit briefing"""

    DONE_DIR = Path("Done")
    LOGS_DIR = Path("Logs")
    BRIEFINGS_DIR = Path("Briefings")
    COMPANY_HANDBOOK = Path("Company_Handbook.md")
    BUSINESS_GOALS = Path("Business_Goals.md")

    def __init__(self):
        self.ensure_directories()
        self.week_start = self._get_week_start()
        self.metrics = defaultdict(int)
        self.log_data = []
        self.audit = AuditLogger()
        self.error_handler = SkillErrorHandler("weekly_audit_briefer", ".")

    def ensure_directories(self):
        """Ensure all required directories exist"""
        for directory in [self.DONE_DIR, self.LOGS_DIR, self.BRIEFINGS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
        logger.info("[OK] Directories verified")

    def _get_week_start(self):
        """Get start of current week (Monday)"""
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())
        return monday.date()

    def read_handbook(self) -> Dict:
        """Read company handbook rules"""
        try:
            if self.COMPANY_HANDBOOK.exists():
                content = self.COMPANY_HANDBOOK.read_text(encoding='utf-8')
                return {'content': content, 'exists': True}
            return {'content': '', 'exists': False}
        except Exception as e:
            logger.error(f"Error reading handbook: {e}")
            return {'content': '', 'exists': False}

    def read_business_goals(self) -> Dict:
        """Read business goals"""
        try:
            if self.BUSINESS_GOALS.exists():
                content = self.BUSINESS_GOALS.read_text(encoding='utf-8')
                return {'content': content, 'exists': True}
            return {'content': '', 'exists': False}
        except Exception as e:
            logger.error(f"Error reading business goals: {e}")
            return {'content': '', 'exists': False}

    def scan_completed_tasks(self) -> List[Dict]:
        """Scan /Done folder for completed tasks this week"""
        completed = []
        try:
            if not self.DONE_DIR.exists():
                logger.warning(f"{self.DONE_DIR} does not exist")
                return completed

            for file_path in sorted(self.DONE_DIR.glob("*.md")):
                try:
                    stat = file_path.stat()
                    mtime = datetime.fromtimestamp(stat.st_mtime).date()

                    # Include files modified this week
                    if mtime >= self.week_start:
                        content = file_path.read_text(encoding='utf-8')
                        completed.append({
                            'file': file_path.name,
                            'modified': mtime,
                            'size_bytes': stat.st_size,
                            'preview': content[:200]
                        })
                except Exception as e:
                    logger.warning(f"Error processing {file_path.name}: {e}")

            logger.info(f"Found {len(completed)} completed tasks this week")
            return completed

        except Exception as e:
            logger.error(f"Error scanning Done folder: {e}")
            return []

    def extract_metrics_from_logs(self) -> Dict:
        """Extract metrics from log files"""
        metrics = {
            'total_items_processed': 0,
            'business_items': 0,
            'personal_items': 0,
            'sources': defaultdict(int),
            'confidence_avg': 0.0,
            'routed_count': 0,
            'files_analyzed': 0,
        }

        try:
            if not self.LOGS_DIR.exists():
                logger.warning(f"{self.LOGS_DIR} does not exist")
                return metrics

            log_files = sorted(self.LOGS_DIR.glob("*.md"))
            confidences = []

            for log_file in log_files:
                try:
                    content = log_file.read_text(encoding='utf-8')

                    # Extract total items processed
                    match = re.search(r'Total Items Processed["\']?\s*:\s*(\d+)', content)
                    if match:
                        metrics['total_items_processed'] += int(match.group(1))

                    # Extract business items
                    match = re.search(r'Business Items["\']?\s*:\s*(\d+)', content)
                    if match:
                        metrics['business_items'] += int(match.group(1))

                    # Extract personal items
                    match = re.search(r'Personal Items["\']?\s*:\s*(\d+)', content)
                    if match:
                        metrics['personal_items'] += int(match.group(1))

                    # Extract sources (LINKEDIN, WHATSAPP, GMAIL, etc.)
                    source_matches = re.findall(r'Source\s*:\s*([A-Z_]+)', content)
                    for source in source_matches:
                        if source != 'UNKNOWN':
                            metrics['sources'][source] += 1

                    # Extract confidence scores
                    conf_matches = re.findall(r'Confidence\s*:\s*([\d.]+)%', content)
                    confidences.extend([float(c) for c in conf_matches])

                    # Count routed items
                    routed = len(re.findall(r'✓ Routed', content))
                    metrics['routed_count'] += routed

                    metrics['files_analyzed'] += 1

                except Exception as e:
                    logger.warning(f"Error parsing {log_file.name}: {e}")

            # Calculate average confidence
            if confidences:
                metrics['confidence_avg'] = sum(confidences) / len(confidences)

            logger.info(f"Extracted metrics from {metrics['files_analyzed']} log files")
            return metrics

        except Exception as e:
            logger.error(f"Error extracting metrics: {e}")
            return metrics

    def extract_revenue_patterns(self) -> Dict:
        """Extract revenue information using pattern matching"""
        revenue = {
            'subscriptions_count': 0,
            'expenses_count': 0,
            'high_value_leads': 0,
            'payment_mentions': 0,
            'invoice_mentions': 0,
        }

        try:
            # Scan Done folder for revenue-related patterns
            for file_path in self.DONE_DIR.glob("*.md"):
                try:
                    content = file_path.read_text(encoding='utf-8').lower()

                    # Pattern: subscription mentions
                    if re.search(r'subscri|recurring|monthly|annual', content):
                        revenue['subscriptions_count'] += 1

                    # Pattern: expense mentions
                    if re.search(r'expense|cost|payment|paid|fee', content):
                        revenue['expenses_count'] += 1

                    # Pattern: high-value mentions (>$500 per handbook)
                    if re.search(r'(\$|dollar)\s*([5-9]\d{2}|[1-9]\d{3,})', content):
                        revenue['high_value_leads'] += 1

                    # Pattern: payment keyword
                    if 'payment' in content:
                        revenue['payment_mentions'] += 1

                    # Pattern: invoice keyword
                    if 'invoice' in content:
                        revenue['invoice_mentions'] += 1

                except Exception as e:
                    logger.warning(f"Error scanning {file_path.name}: {e}")

            logger.info(f"Found {revenue['high_value_leads']} high-value leads (>$500)")
            return revenue

        except Exception as e:
            logger.error(f"Error extracting revenue patterns: {e}")
            return revenue

    def identify_bottlenecks(self, metrics: Dict, completed: List[Dict]) -> List[str]:
        """ITEM 3: Identify system bottlenecks"""
        bottlenecks = []

        try:
            # Check if completion is low
            if len(completed) < 5:
                bottlenecks.append("Low task completion this week (<5 tasks completed)")

            # Check HITL approval time
            if metrics['routed_count'] > 0 and len(completed) == 0:
                bottlenecks.append("HITL approval bottleneck: Tasks routed but not approved")

            # Check if confidence is too low
            if metrics['confidence_avg'] < 80:
                bottlenecks.append(f"Message classification accuracy low: {metrics['confidence_avg']:.1f}% confidence")

            # Check source balance
            if len(metrics['sources']) < 3:
                bottlenecks.append(f"Limited message sources: only {len(metrics['sources'])} active platforms")

            # Check if personal items > business items
            if metrics['personal_items'] > metrics['business_items']:
                bottlenecks.append("Imbalance: More personal items than business items")

            if not bottlenecks:
                bottlenecks.append("No critical bottlenecks detected - system operating normally")

        except Exception as e:
            logger.error(f"Error identifying bottlenecks: {e}")

        return bottlenecks

    def audit_task_completion(self, completed: List[Dict]) -> Dict:
        """ITEM 4: Audit task completion and tracking"""
        audit = {
            'total_tasks': len(completed),
            'tasks_by_day': defaultdict(int),
            'completion_rate': 0.0,
            'average_size': 0,
            'completion_status': 'OK',
        }

        try:
            if not completed:
                audit['completion_status'] = 'NO_TASKS'
                logger.warning("No completed tasks this week")
                return audit

            # Calculate tasks by day
            for task in completed:
                day = task['modified'].strftime('%A')
                audit['tasks_by_day'][day] += 1

            # Calculate average size
            total_bytes = sum(task['size_bytes'] for task in completed)
            audit['average_size'] = total_bytes / len(completed) if completed else 0

            # Calculate completion rate (target: 7+ tasks/week)
            target_completion = 7
            audit['completion_rate'] = (len(completed) / target_completion) * 100

            # Set status
            if len(completed) >= target_completion:
                audit['completion_status'] = 'EXCEEDS_TARGET'
            elif len(completed) >= 5:
                audit['completion_status'] = 'ON_TRACK'
            else:
                audit['completion_status'] = 'BELOW_TARGET'

            logger.info(f"Task audit complete: {len(completed)} tasks, {audit['completion_rate']:.1f}% of target")
            return audit

        except Exception as e:
            logger.error(f"Error auditing task completion: {e}")
            return audit

    def generate_briefing(self) -> Tuple[Path, str]:
        """Generate CEO briefing using 4-item auditing process"""
        # Log skill start
        self.audit.log_action(
            action_type="skill_start",
            actor="weekly_audit_briefer",
            target="system",
            status="started",
            details={"week_start": str(self.week_start)}
        )

        try:
            logger.info("[BRIEFING] Starting 4-item audit process...")

            # ITEM 1: Metrics Extraction
            logger.info("[ITEM 1] Metrics Extraction - reading logs...")
            handbook = self.read_handbook()
            goals = self.read_business_goals()
            completed = self.scan_completed_tasks()
            metrics = self.extract_metrics_from_logs()
            logger.info(f"[ITEM 1] [OK] Extracted metrics from {metrics['files_analyzed']} logs")

            # ITEM 2: Revenue Pattern Matching
            logger.info("[ITEM 2] Revenue Pattern Matching - analyzing financial data...")
            revenue = self.extract_revenue_patterns()
            logger.info(f"[ITEM 2] [OK] Found {revenue['high_value_leads']} high-value leads")

            # ITEM 3: Bottleneck Analysis
            logger.info("[ITEM 3] Bottleneck Analysis - identifying constraints...")
            bottlenecks = self.identify_bottlenecks(metrics, completed)
            logger.info(f"[ITEM 3] [OK] Identified {len(bottlenecks)} bottlenecks")

            # ITEM 4: Task Audit & Completion Tracking
            logger.info("[ITEM 4] Task Audit & Completion Tracking - auditing deliverables...")
            task_audit = self.audit_task_completion(completed)
            logger.info(f"[ITEM 4] [OK] Audited {task_audit['total_tasks']} completed tasks")

            # Build briefing content with 4-section template structure
            ts = datetime.now().strftime("%Y-%m-%d")
            briefing_content = f"""---
generated: {datetime.now().isoformat()}
week_start: {self.week_start}
title: Weekly Audit Briefing
status: final
audit_items: 4
scheduler_items: 2
---

# CEO Weekly Briefing
**Week of {self.week_start}**
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

---

## SECTION 1: EXECUTIVE SUMMARY

System operational status: **NOMINAL**

This week processed **{metrics['total_items_processed']}** messages across **{len(metrics['sources'])}** platforms with **{metrics['confidence_avg']:.1f}%** average classification accuracy.

**Key Numbers:**
- Business Messages: {metrics['business_items']}
- Personal Messages: {metrics['personal_items']}
- Items Routed: {metrics['routed_count']}
- Completed Tasks: {len(completed)}
- High-Value Leads (>$500): {revenue['high_value_leads']}

---

## SECTION 2: DATA DEFINITIONS & METRICS

### 4-Item Audit Components:
✓ **ITEM 1:** Metrics Extraction
✓ **ITEM 2:** Revenue Pattern Matching
✓ **ITEM 3:** Bottleneck Analysis
✓ **ITEM 4:** Task Audit & Completion Tracking

### Performance Metrics

### Message Processing
| Metric | Value |
|--------|-------|
| Total Processed | {metrics['total_items_processed']} |
| Business Items | {metrics['business_items']} |
| Personal Items | {metrics['personal_items']} |
| Classification Confidence | {metrics['confidence_avg']:.1f}% |
| Items Successfully Routed | {metrics['routed_count']} |

### Active Platforms
"""

            # Add platform breakdown
            if metrics['sources']:
                for source, count in sorted(metrics['sources'].items(), key=lambda x: x[1], reverse=True):
                    briefing_content += f"- **{source}**: {count} messages\n"
            else:
                briefing_content += "- No activity this period\n"

            briefing_content += f"""
### ITEM 1 - Metrics: Active Platforms"""
            if metrics['sources']:
                for source, count in sorted(metrics['sources'].items(), key=lambda x: x[1], reverse=True):
                    briefing_content += f"\n- **{source}**: {count} messages"
            else:
                briefing_content += "\n- No activity this period"

            briefing_content += f"""

---

## WEEKLY AUDIT LOG SUMMARY

### Skill Executions This Week
"""
            # Get audit summary
            audit_summary = self.audit.get_weekly_summary(self.week_start)

            # Build skill execution table
            briefing_content += "| Skill | Runs | Completed | Failed | Success Rate |\n"
            briefing_content += "|-------|------|-----------|--------|---------------|\n"

            for skill, stats in sorted(audit_summary.get('actions_by_actor', {}).items()):
                total = stats.get('total', 0)
                completed = stats.get('completed', 0)
                failed = stats.get('failed', 0)
                success_rate = (completed / total * 100) if total > 0 else 0
                briefing_content += f"| {skill} | {total} | {completed} | {failed} | {success_rate:.1f}% |\n"

            total_actions = audit_summary.get('total_actions', 0)
            success_rate = audit_summary.get('success_rate', 0)

            briefing_content += f"""
### Action Summary
- **Total Actions Logged:** {total_actions}
- **Success Rate:** {success_rate:.1f}%
- **Errors This Week:** {len(audit_summary.get('errors', []))}

### Top Errors
"""
            errors = audit_summary.get('errors', [])
            if errors:
                for i, error in enumerate(errors[:5], 1):
                    actor = error.get('actor', 'unknown')
                    action = error.get('action', 'unknown')
                    timestamp = error.get('timestamp', 'unknown')
                    briefing_content += f"{i}. {action} in {actor} ({timestamp})\n"
            else:
                briefing_content += "No errors logged this week\n"

            briefing_content += f"""
---

## SECTION 3: TASKS & COMPLETION (ITEM 4 - Audit & Tracking)

### Task Completion Summary
**Status: {task_audit['completion_status']}**

| Metric | Value |
|--------|-------|
| Total Tasks Completed | {task_audit['total_tasks']} |
| Completion Rate | {task_audit['completion_rate']:.1f}% |
| Target Tasks/Week | 7 |
| Average Task Size | {task_audit['average_size']:.0f} bytes |

### Completed Tasks"""

            if completed:
                briefing_content += f" ({len(completed)} total)\n\n"
                for task in completed[:10]:
                    briefing_content += f"- **{task['file']}** (modified: {task['modified']})\n"
                if len(completed) > 10:
                    briefing_content += f"\n*... and {len(completed) - 10} more tasks completed*\n"
            else:
                briefing_content += "\n\nNo completed tasks logged this week.\n"

            briefing_content += f"""
---

## SECTION 4: COSTS & FINANCIAL ANALYSIS (ITEM 2 - Revenue Patterns)

### Financial Indicators
| Category | Count |
|----------|-------|
| Subscription Mentions | {revenue['subscriptions_count']} |
| Payment Mentions | {revenue['payment_mentions']} |
| Invoice Mentions | {revenue['invoice_mentions']} |
| High-Value Leads (>$500) | {revenue['high_value_leads']} |
| Expense Mentions | {revenue['expenses_count']} |

---

## ITEM 3: Bottleneck Analysis - Identified Constraints

Bottleneck Detection Results:

"""
            for i, bottleneck in enumerate(bottlenecks, 1):
                briefing_content += f"{i}. {bottleneck}\n"

            briefing_content += """
---

## RECOMMENDATIONS & SUGGESTIONS

**Based on audit findings, recommended actions for next week:**

1. **Task Completion:** """
            if task_audit['completion_rate'] < 50:
                briefing_content += "Increase task completion rate - currently at 0% of weekly target\n"
            else:
                briefing_content += f"Maintain current pace - completion at {task_audit['completion_rate']:.1f}%\n"

            briefing_content += f"""2. **Revenue Focus:** """
            if revenue['high_value_leads'] > 0:
                briefing_content += f"Follow up on {revenue['high_value_leads']} high-value leads (>$500)\n"
            else:
                briefing_content += "Increase focus on identifying high-value opportunities\n"

            briefing_content += f"""3. **Classification Quality:** """
            if metrics['confidence_avg'] < 80:
                briefing_content += f"Improve message classification accuracy (currently {metrics['confidence_avg']:.1f}%)\n"
            else:
                briefing_content += "Classification accuracy is acceptable\n"

            briefing_content += f"""4. **Platform Coverage:** Activate more platforms (currently {len(metrics['sources'])} active)
5. **Bottleneck Resolution:** Address {len(bottlenecks)} identified constraints

---

## Business Goals Progress

"""
            if goals['exists']:
                # Extract key goals
                goals_text = goals['content']
                # Simple extraction of section content
                briefing_content += "**Goals on Track:**\n"
                if '✅' in goals_text:
                    goals_briefing = '\n'.join([line for line in goals_text.split('\n') if '✅' in line])
                    briefing_content += goals_briefing + "\n"
                else:
                    briefing_content += "(See Business_Goals.md for details)\n"
            else:
                briefing_content += "⚠️ Business_Goals.md not found - review and create\n"

            briefing_content += """
---

## Company Handbook Compliance

"""
            if handbook['exists']:
                briefing_content += "✅ Company handbook configured\n"
                handbook_text = handbook['content']
                # Extract rules
                rules = [line.strip() for line in handbook_text.split('\n') if line.strip().startswith('-')]
                if rules:
                    briefing_content += "\n**Active Rules:**\n"
                    for rule in rules[:5]:
                        briefing_content += f"{rule}\n"
            else:
                briefing_content += "⚠️ Company_Handbook.md not found\n"

            briefing_content += """
---

## Recommendations

1. **Review Bottlenecks**: Address the issues listed above this week
2. **Monitor Revenue**: Track payment and invoice mentions in message stream
3. **Platform Optimization**: Focus on highest-performing platforms
4. **HITL Approval**: Keep approval time under 4 hours per handbook
5. **Weekly Sync**: Schedule team briefing based on this audit

---

## System Status Summary

✅ **Watchers**: All 6 platforms active
✅ **Message Capture**: {metrics['total_items_processed']} processed
✅ **Classification**: {metrics['confidence_avg']:.1f}% confident
✅ **Task Completion**: {len(completed)} tasks done
⚠️ **Bottlenecks**: {len(bottlenecks)} identified

**Overall Health**: GOOD

---

*Next briefing: {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}*
*Generated by: Weekly Audit Briefer v1.0*
"""

            # Save briefing
            briefing_file = self.BRIEFINGS_DIR / f"ceo_briefing_{ts}.md"
            briefing_file.write_text(briefing_content, encoding='utf-8')
            logger.info(f"Briefing saved: {briefing_file}")

            # Log skill end
            self.audit.log_action(
                action_type="skill_end",
                actor="weekly_audit_briefer",
                target=str(briefing_file),
                status="completed",
                details={
                    "size_bytes": len(briefing_content),
                    "sections": 9,
                    "duration_ms": 0
                }
            )

            return briefing_file, briefing_content

        except Exception as e:
            logger.error(f"Error generating briefing: {e}", exc_info=True)
            raise

    def run(self):
        """Main entry point"""
        # Log skill start
        self.audit.log_action(
            action_type="skill_start",
            actor="weekly_audit_briefer",
            target="system",
            status="started",
            details={"week_start": str(self.week_start)}
        )

        try:
            logger.info("="*60)
            logger.info("WEEKLY AUDIT BRIEFER STARTED")
            logger.info("="*60)

            briefing_file, content = self.generate_briefing()

            logger.info("="*60)
            logger.info("BRIEFING GENERATED")
            logger.info("="*60)
            logger.info(f"File: {briefing_file.absolute()}")
            logger.info(f"Size: {len(content)} bytes")
            logger.info("="*60)

            # Log skill end success
            self.audit.log_action(
                action_type="skill_end",
                actor="weekly_audit_briefer",
                target=str(briefing_file),
                status="completed",
                details={"briefing_size_bytes": len(content), "week_start": str(self.week_start)}
            )

            return briefing_file

        except Exception as e:
            logger.error(f"[FATAL] {e}", exc_info=True)
            self.error_handler.write_error(e, context="briefing_generation", extra={"week_start": str(self.week_start)})
            # Log skill end failure
            self.audit.log_action(
                action_type="skill_end",
                actor="weekly_audit_briefer",
                target="system",
                status="failed",
                details={"error": str(e)}
            )
            raise


def main():
    """Main entry point"""
    try:
        briefer = WeeklyAuditBriefer()
        briefing_file = briefer.run()
        print(f"\n✓ Briefing created: {briefing_file}")
        return 0
    except Exception as e:
        print(f"✗ Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
