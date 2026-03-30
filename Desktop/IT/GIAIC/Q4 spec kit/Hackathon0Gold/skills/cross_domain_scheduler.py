#!/usr/bin/env python3
"""
Cross Domain Integrator Scheduler
Runs the integrator every 30 minutes continuously
"""

import subprocess
import time
import logging
from datetime import datetime
from pathlib import Path

from skills.audit_logger import AuditLogger
from skills.error_handler import SkillErrorHandler

# Setup logging
log_file = Path("skills/logs/cross_domain_scheduler.log")
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize audit logger at module level
audit = AuditLogger()
error_handler = SkillErrorHandler("cross_domain_scheduler", ".")

INTERVAL_MINUTES = 30

def run_integrator():
    """Run the Cross Domain Integrator"""
    # Log skill start
    audit.log_action(
        action_type="skill_start",
        actor="cross_domain_scheduler",
        target="system",
        status="started",
        details={"interval_minutes": INTERVAL_MINUTES}
    )

    try:
        logger.info(f"[SCHEDULER] Running Cross Domain Integrator...")
        result = subprocess.run(
            ["python", "skills/cross_domain_integrator.py"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            logger.info(f"[SCHEDULER] SUCCESS - Integration completed")
            # Log skill end success
            audit.log_action(
                action_type="skill_end",
                actor="cross_domain_scheduler",
                target="system",
                status="completed",
                details={"subprocess_exit_code": result.returncode}
            )
        else:
            logger.warning(f"[SCHEDULER] Process exited with code {result.returncode}")
            if result.stderr:
                logger.warning(f"[SCHEDULER] Error: {result.stderr[:500]}")
            # Log skill end failure
            audit.log_action(
                action_type="skill_end",
                actor="cross_domain_scheduler",
                target="system",
                status="failed",
                details={"subprocess_exit_code": result.returncode, "error": result.stderr[:200]}
            )
    except subprocess.TimeoutExpired as e:
        logger.error(f"[SCHEDULER] TIMEOUT - Process exceeded 5 minutes")
        error_handler.write_error(e, context="subprocess_timeout", extra={"timeout_seconds": 300})
        audit.log_action(
            action_type="skill_end",
            actor="cross_domain_scheduler",
            target="system",
            status="failed",
            details={"error": "TimeoutExpired"}
        )
    except Exception as e:
        logger.error(f"[SCHEDULER] ERROR: {e}")
        error_handler.write_error(e, context="subprocess_execution", extra={"command": "cross_domain_integrator.py"})
        audit.log_action(
            action_type="skill_end",
            actor="cross_domain_scheduler",
            target="system",
            status="failed",
            details={"error": str(e)}
        )

def main():
    """Main scheduler loop"""
    logger.info("=" * 70)
    logger.info("CROSS DOMAIN INTEGRATOR SCHEDULER - STARTED")
    logger.info("=" * 70)
    logger.info(f"Interval: Every {INTERVAL_MINUTES} minutes")
    logger.info(f"Status: Monitoring /Needs_Action/ continuously...")
    logger.info("")

    # Run once immediately
    logger.info("[SCHEDULER] Running initial integration...")
    run_integrator()

    # Then run every INTERVAL_MINUTES
    try:
        while True:
            logger.info(f"[SCHEDULER] Next run in {INTERVAL_MINUTES} minutes (at {datetime.now().strftime('%H:%M')})")
            time.sleep(INTERVAL_MINUTES * 60)
            logger.info("")
            run_integrator()
    except KeyboardInterrupt:
        logger.info("[SCHEDULER] Stopped by user")
    except Exception as e:
        logger.error(f"[SCHEDULER] Fatal error: {e}")
        error_handler.write_error(e, context="scheduler_main_loop", extra={"interval_minutes": INTERVAL_MINUTES})

if __name__ == "__main__":
    main()
