#!/usr/bin/env python3
"""
AI Social Media Manager - Full Workflow Test Script

Tests the complete workflow:
1. Start Master Orchestrator
2. Create draft posts with Trigger Posts
3. Approve and move to Orchestrator
4. Monitor processing and completion
5. Verify success and generate report

Usage:
    python run_workflow_test.py                    # Interactive menu
    python run_workflow_test.py --platform facebook --count 1
    python run_workflow_test.py --batch             # Test all 6 platforms

"""

import os
import sys
import argparse
import subprocess
import time
import json
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

# ANSI color codes
class Color:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    RESET = '\033[0m'

def log_info(msg: str):
    print(f"{Color.BLUE}[INFO]{Color.RESET} {msg}")

def log_success(msg: str):
    print(f"{Color.GREEN}[✓]{Color.RESET} {msg}")

def log_error(msg: str):
    print(f"{Color.RED}[✗]{Color.RESET} {msg}")

def log_warning(msg: str):
    print(f"{Color.YELLOW}[!]{Color.RESET} {msg}")

class WorkflowTest:
    """Main test class for workflow validation"""

    PLATFORMS = ["facebook", "linkedin", "twitter", "instagram", "whatsapp", "gmail"]

    def __init__(self):
        """Initialize paths and configuration"""
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent

        self.orchestrator_script = self.script_dir / "master_orchestrator.py"
        self.trigger_script = self.script_dir / "trigger_posts.py"
        self.executor_script = self.script_dir / "social_media_executor_v2.py"

        self.pending_dir = self.project_root / "Pending_Approval"
        self.approved_dir = self.project_root / "Approved"
        self.done_dir = self.project_root / "Done"
        self.logs_dir = self.project_root / "Logs"

        self.orchestrator_process = None

    def check_dependencies(self) -> bool:
        """Verify all required Python packages are installed"""
        log_info("Checking dependencies...")

        required_modules = ["yaml", "watchdog", "playwright"]
        missing = []

        for module in required_modules:
            try:
                __import__(module)
                log_success(f"✓ {module} installed")
            except ImportError:
                missing.append(module)
                log_error(f"✗ {module} not found")

        if missing:
            log_error(f"Missing modules: {', '.join(missing)}")
            log_info("Install with: pip install " + " ".join(missing))
            return False

        return True

    def check_directories(self) -> bool:
        """Create or verify directory structure"""
        log_info("Checking directory structure...")

        for dir_path in [self.pending_dir, self.approved_dir, self.done_dir, self.logs_dir]:
            if not dir_path.exists():
                log_warning(f"Creating directory: {dir_path}")
                dir_path.mkdir(parents=True, exist_ok=True)

        log_success("Directory structure verified")
        return True

    def check_scripts(self) -> bool:
        """Verify all required scripts exist"""
        log_info("Checking script files...")

        for script in [self.orchestrator_script, self.trigger_script, self.executor_script]:
            if not script.exists():
                log_error(f"Script not found: {script}")
                return False
            log_success(f"✓ {script.name}")

        return True

    def start_orchestrator(self) -> bool:
        """Start Master Orchestrator in background"""
        log_info("Starting Master Orchestrator...")

        try:
            # Start orchestrator in background
            if sys.platform == "win32":
                # Windows: start in new window
                self.orchestrator_process = subprocess.Popen(
                    [sys.executable, str(self.orchestrator_script)],
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            else:
                # Linux/Mac: run in background
                self.orchestrator_process = subprocess.Popen(
                    [sys.executable, str(self.orchestrator_script)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            time.sleep(3)
            log_success("Orchestrator started")
            return True
        except Exception as e:
            log_error(f"Failed to start orchestrator: {e}")
            return False

    def create_draft_post(self, platform: str, content: str, title: str = "Test Post") -> bool:
        """Create a draft post using Trigger Posts script"""
        log_info(f"Creating draft post for {platform}...")

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(self.trigger_script),
                    "-p", platform,
                    "-c", content,
                    "-t", title,
                    "--preview"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                log_success(f"Draft created for {platform}")
                return True
            else:
                log_error(f"Failed to create draft: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            log_error(f"Timeout creating draft for {platform}")
            return False
        except Exception as e:
            log_error(f"Error creating draft: {e}")
            return False

    def count_files(self, directory: Path) -> int:
        """Count POST_*.md files in directory"""
        try:
            return len(list(directory.glob("POST_*.md")))
        except:
            return 0

    def approve_posts(self) -> int:
        """Move posts from Pending_Approval to Approved"""
        pending_count = self.count_files(self.pending_dir)

        if pending_count == 0:
            log_warning("No posts to approve")
            return 0

        log_info(f"Approving {pending_count} post(s)...")

        try:
            for file in self.pending_dir.glob("POST_*.md"):
                file.rename(self.approved_dir / file.name)
            log_success(f"Approved {pending_count} post(s)")
            return pending_count
        except Exception as e:
            log_error(f"Error approving posts: {e}")
            return 0

    def monitor_processing(self, timeout: int = 300) -> bool:
        """Monitor processing until all posts complete or timeout"""
        log_info(f"Monitoring processing (timeout: {timeout}s)...")

        start_time = time.time()
        previous_approved = self.count_files(self.approved_dir)

        while True:
            elapsed = int(time.time() - start_time)

            if elapsed > timeout:
                log_warning(f"Monitoring timeout after {timeout}s")
                return False

            approved_now = self.count_files(self.approved_dir)
            done_now = self.count_files(self.done_dir)

            # Show progress
            sys.stdout.write(f"\r[{elapsed}s] Approved: {approved_now} | Done: {done_now}")
            sys.stdout.flush()

            # Check if all processed
            if approved_now == 0 and done_now > 0:
                print()
                log_success("All posts processed!")
                return True

            time.sleep(2)

        return False

    def verify_results(self) -> Tuple[bool, dict]:
        """Verify test results and generate report"""
        log_info("Verifying test results...")
        print()

        pending = self.count_files(self.pending_dir)
        approved = self.count_files(self.approved_dir)
        done = self.count_files(self.done_dir)

        report = {
            "timestamp": datetime.now().isoformat(),
            "pending": pending,
            "approved": approved,
            "done": done,
            "status": "unknown",
            "errors": 0
        }

        print(f"Status Summary:")
        print(f"  Pending Approval: {pending}")
        print(f"  Approved (Processing): {approved}")
        print(f"  Done (Completed): {done}")
        print()

        # Check for errors in logs
        try:
            log_file = list(self.logs_dir.glob("orchestrator_*.log"))
            if log_file:
                with open(log_file[-1], 'r') as f:
                    content = f.read()
                    error_count = content.count("✗") + content.count("FAILED")
                    report["errors"] = error_count
                    if error_count > 0:
                        log_warning(f"Found {error_count} error(s) in logs")
                    else:
                        log_success("No errors found")
        except:
            pass

        # Determine overall result
        if done > 0 and approved == 0:
            report["status"] = "PASSED"
            log_success("✓ Test PASSED - All posts processed successfully")
            return True, report
        elif done > 0:
            report["status"] = "PARTIAL"
            log_warning("Test PARTIAL - Some posts processed, some still pending")
            return False, report
        else:
            report["status"] = "FAILED"
            log_error("Test FAILED - No posts processed")
            return False, report

    def cleanup_test_files(self) -> None:
        """Clean up test files"""
        log_info("Cleaning up test files...")

        for dir_path in [self.pending_dir, self.approved_dir, self.done_dir]:
            try:
                for file in dir_path.glob("POST_test_*.md"):
                    file.unlink()
            except:
                pass

        log_success("Test files cleaned up")

    def view_logs(self) -> None:
        """Display latest log entries"""
        print()
        log_info("=== Latest Log Entries ===")
        print()

        # Orchestrator logs
        try:
            log_files = list(self.logs_dir.glob("orchestrator_*.log"))
            if log_files:
                with open(log_files[-1], 'r') as f:
                    lines = f.readlines()
                    relevant = [l for l in lines if any(x in l for x in ["Processing", "Executing", "SUCCESS", "FAILED"])]
                    if relevant:
                        log_info("Orchestrator logs:")
                        for line in relevant[-10:]:
                            print(f"  {line.strip()}")
        except:
            pass

        print()

        # File status
        log_info("File status:")
        print(f"  Pending: {self.count_files(self.pending_dir)}")
        print(f"  Approved: {self.count_files(self.approved_dir)}")
        print(f"  Done: {self.count_files(self.done_dir)}")
        print()

    def test_single_platform(self, platform: str = None) -> None:
        """Test single platform workflow"""
        if platform is None:
            print()
            print(f"Available platforms: {', '.join(self.PLATFORMS)}")
            platform = input("Enter platform (default: facebook): ").strip() or "facebook"

        if platform not in self.PLATFORMS:
            log_error(f"Invalid platform: {platform}")
            return

        log_info(f"=== Single Platform Test ({platform}) ===")
        print()

        if not self.start_orchestrator():
            return

        time.sleep(5)
        if not self.create_draft_post(platform, "🚀 Test from automation system!", "Test Post"):
            return

        input("\nPress Enter to approve post...")
        self.approve_posts()

        print()
        self.monitor_processing(120)

        print()
        success, report = self.verify_results()

    def test_batch_all(self) -> None:
        """Test all 6 platforms"""
        log_info("=== Batch Test (All 6 Platforms) ===")
        print()

        if not self.start_orchestrator():
            return

        time.sleep(5)
        log_info("Creating draft posts for all 6 platforms...")

        for i, platform in enumerate(self.PLATFORMS, 1):
            self.create_draft_post(platform, f"Batch test for {platform} (#{i}/6)", f"Test Post - {platform}")
            time.sleep(1)

        print()
        input("Press Enter to approve all posts...")
        self.approve_posts()

        print()
        log_info("Monitoring batch processing (approx 5-10 minutes)...")
        self.monitor_processing(600)

        print()
        success, report = self.verify_results()

    def test_custom(self) -> None:
        """Custom test with user input"""
        print()
        log_info("=== Custom Test ===")
        print()

        print(f"Available platforms: {', '.join(self.PLATFORMS)}")
        platform = input("Enter platform: ").strip() or "facebook"

        try:
            count = int(input("Enter number of posts (default: 1): ") or "1")
        except ValueError:
            count = 1

        if platform not in self.PLATFORMS or count <= 0:
            log_error("Invalid input")
            return

        if not self.start_orchestrator():
            return

        time.sleep(5)
        log_info(f"Creating {count} draft post(s) for {platform}...")

        for i in range(1, count + 1):
            self.create_draft_post(platform, f"Custom test post #{i}", f"Test Post #{i}")
            time.sleep(1)

        print()
        input("Press Enter to approve all posts...")
        self.approve_posts()

        print()
        timeout = count * 40  # ~40 seconds per post
        log_info(f"Monitoring processing (approx {timeout}s)...")
        self.monitor_processing(timeout)

        print()
        success, report = self.verify_results()

    def show_menu(self) -> None:
        """Interactive menu"""
        while True:
            print()
            print(f"{Color.BLUE}=== AI Social Media Manager - Workflow Test ==={Color.RESET}")
            print()
            print("Select test mode:")
            print("  1) Single Platform Test")
            print("  2) Multi-Platform Batch Test (all 6)")
            print("  3) Custom Test")
            print("  4) View Logs and Status")
            print("  5) Clean Up Test Files")
            print("  6) Exit")
            print()

            choice = input("Enter choice (1-6): ").strip()

            if choice == "1":
                self.test_single_platform()
            elif choice == "2":
                self.test_batch_all()
            elif choice == "3":
                self.test_custom()
            elif choice == "4":
                self.view_logs()
            elif choice == "5":
                confirm = input("Delete all test files? (yes/no): ").strip().lower()
                if confirm == "yes":
                    self.cleanup_test_files()
            elif choice == "6":
                log_info("Exiting")
                break
            else:
                log_error("Invalid choice")

    def cleanup(self) -> None:
        """Clean up resources"""
        if self.orchestrator_process:
            try:
                self.orchestrator_process.terminate()
            except:
                pass

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AI Social Media Manager - Workflow Test Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_workflow_test.py                    # Interactive menu
  python run_workflow_test.py --platform facebook --count 1
  python run_workflow_test.py --batch             # Test all 6 platforms
        """
    )

    parser.add_argument(
        "--platform", "-p",
        help="Test specific platform (facebook, linkedin, twitter, instagram, whatsapp, gmail)"
    )
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=1,
        help="Number of posts to create (default: 1)"
    )
    parser.add_argument(
        "--batch", "-b",
        action="store_true",
        help="Test all 6 platforms"
    )

    args = parser.parse_args()

    print()
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║   AI Social Media Manager - Workflow Test Script              ║")
    print("║   Testing: Trigger Posts → Orchestrator → Executor            ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()

    # Create test instance
    test = WorkflowTest()

    # Pre-test checks
    if not test.check_dependencies():
        sys.exit(1)
    test.check_directories()
    if not test.check_scripts():
        sys.exit(1)

    # Run based on arguments or show interactive menu
    try:
        if args.batch:
            test.test_batch_all()
        elif args.platform:
            test.test_single_platform(args.platform)
        else:
            test.show_menu()
    except KeyboardInterrupt:
        print()
        log_warning("Test interrupted by user")
    finally:
        test.cleanup()

if __name__ == "__main__":
    main()
