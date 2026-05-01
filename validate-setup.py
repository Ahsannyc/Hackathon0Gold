#!/usr/bin/env python3
"""
Hackathon0Gold - System Validation Script
Validates that all 5 watchers and dependencies are properly set up
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

class Validator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.successes = []
        self.project_root = Path(__file__).parent

    def log_success(self, msg):
        print(f"[OK] {msg}")
        self.successes.append(msg)

    def log_error(self, msg):
        print(f"[ERROR] {msg}")
        self.errors.append(msg)

    def log_warning(self, msg):
        print(f"[WARNING] {msg}")
        self.warnings.append(msg)

    def log_info(self, msg):
        print(f"[INFO] {msg}")

    def log_header(self, msg):
        print(f"\n===== {msg} =====\n")

    # Validation methods
    def check_python(self):
        """Check Python version"""
        self.log_header("Python Environment")
        version = sys.version_info
        if version.major >= 3 and version.minor >= 11:
            self.log_success(f"Python {version.major}.{version.minor}.{version.micro} (3.11+ required)")
        else:
            self.log_error(f"Python {version.major}.{version.minor} - Need 3.11 or higher")

    def check_pip_packages(self):
        """Check critical Python packages"""
        self.log_header("Python Packages")
        packages = {
            'playwright': 'Browser automation',
            'selenium': 'WebDriver protocol',
            'undetected_chromedriver': 'Facebook anti-bot bypass',
            'google_auth_oauthlib': 'Gmail OAuth',
            'requests': 'HTTP library',
        }

        for package, description in packages.items():
            try:
                __import__(package.replace('_', '-'))
                self.log_success(f"{package}: {description}")
            except ImportError:
                self.log_error(f"{package}: {description} - NOT INSTALLED")

    def check_nodejs(self):
        """Check Node.js and npm"""
        self.log_header("Node.js & PM2")
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            node_version = result.stdout.strip()
            self.log_success(f"Node.js {node_version}")
        except FileNotFoundError:
            self.log_error("Node.js not found - Install from https://nodejs.org/")

        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            npm_version = result.stdout.strip()
            self.log_success(f"npm {npm_version}")
        except FileNotFoundError:
            self.log_error("npm not found")

        try:
            result = subprocess.run(['pm2', '--version'], capture_output=True, text=True)
            pm2_version = result.stdout.strip()
            self.log_success(f"PM2 {pm2_version}")
        except FileNotFoundError:
            self.log_error("PM2 not installed - Run: npm install -g pm2")

    def check_watchers(self):
        """Check all 5 watcher files exist"""
        self.log_header("Watcher Files (5 Required)")
        required_watchers = {
            'watchers/gmail_watcher.py': 'Gmail monitoring',
            'watchers/whatsapp_persistent.py': 'WhatsApp monitoring',
            'watchers/linkedin_persistent.py': 'LinkedIn monitoring',
            'watchers/instagram_watcher_fixed.py': 'Instagram monitoring',
            'watchers/facebook_watcher_js_extract.py': 'Facebook monitoring (NEW)',
        }

        for watcher_path, description in required_watchers.items():
            full_path = self.project_root / watcher_path
            if full_path.exists():
                size = full_path.stat().st_size / 1024  # KB
                self.log_success(f"{watcher_path} ({size:.1f} KB) - {description}")
            else:
                self.log_error(f"{watcher_path} - NOT FOUND")

    def check_folders(self):
        """Check required folder structure"""
        self.log_header("Folder Structure")
        required_folders = {
            'Needs_Action': 'Auto-captured messages',
            'Pending_Approval': 'Tasks awaiting approval',
            'Approved': 'Approved tasks',
            'Done': 'Completed tasks',
            'session': 'Browser sessions & tokens',
            'watchers/logs': 'Watcher logs',
            'skills': 'AI skills',
            'tools': 'System tools',
            'history': 'Documentation',
        }

        for folder, description in required_folders.items():
            folder_path = self.project_root / folder
            if folder_path.exists() and folder_path.is_dir():
                item_count = len(list(folder_path.iterdir())) if folder_path.exists() else 0
                self.log_success(f"{folder}/ - {description} ({item_count} items)")
            else:
                self.log_warning(f"{folder}/ - {description} (will be created)")

    def check_config_files(self):
        """Check configuration files"""
        self.log_header("Configuration Files")
        required_configs = {
            'ecosystem.config.js': 'PM2 configuration',
            'requirements.txt': 'Python dependencies',
            'STARTUP_GUIDE.md': 'Startup guide',
            'SYSTEM_REQUIREMENTS.md': 'System requirements',
            'PROJECT_STRUCTURE.md': 'Project structure',
            'FACEBOOK_WATCHER_FIX_SUMMARY.md': 'Facebook fix documentation',
        }

        for config_file, description in required_configs.items():
            config_path = self.project_root / config_file
            if config_path.exists():
                size = config_path.stat().st_size / 1024  # KB
                self.log_success(f"{config_file} ({size:.1f} KB) - {description}")
            else:
                self.log_error(f"{config_file} - NOT FOUND")

    def check_pm2_status(self):
        """Check current PM2 status"""
        self.log_header("PM2 Status")
        try:
            result = subprocess.run(['pm2', 'list'], capture_output=True, text=True)
            if 'facebook-watcher' in result.stdout:
                self.log_success("PM2 has running processes (including facebook-watcher)")
                self.log_info("Current processes:")
                for line in result.stdout.split('\n'):
                    if any(x in line for x in ['gmail', 'whatsapp', 'linkedin', 'instagram', 'facebook']):
                        print(f"  {line}")
            else:
                self.log_warning("No watchers currently running in PM2")
                self.log_info("Start with: pm2 start ecosystem.config.js")
        except Exception as e:
            self.log_error(f"Could not check PM2 status: {e}")

    def check_messages(self):
        """Check captured messages"""
        self.log_header("Captured Messages")
        needs_action = self.project_root / 'Needs_Action'
        if needs_action.exists():
            message_files = list(needs_action.glob('*.md'))
            if message_files:
                self.log_success(f"Found {len(message_files)} captured messages")
                # Show latest 3
                latest = sorted(message_files, key=lambda x: x.stat().st_mtime, reverse=True)[:3]
                for msg_file in latest:
                    mtime = datetime.fromtimestamp(msg_file.stat().st_mtime)
                    self.log_info(f"  {msg_file.name} ({mtime.strftime('%Y-%m-%d %H:%M')})")
            else:
                self.log_warning("No messages captured yet")
        else:
            self.log_error("Needs_Action folder not found")

    def generate_report(self):
        """Generate validation report"""
        self.log_header("Validation Summary")

        total = len(self.successes) + len(self.errors) + len(self.warnings)
        passed = len(self.successes)

        print(f"[PASS] Passed: {passed}")
        print(f"[FAIL] Errors: {len(self.errors)}")
        print(f"[WARN] Warnings: {len(self.warnings)}")
        print(f"\nTotal Checks: {total}\n")

        if self.errors:
            print(f"ERRORS (Must Fix):")
            for error in self.errors:
                print(f"  X {error}")
            print()

        if self.warnings:
            print(f"WARNINGS (Should Check):")
            for warning in self.warnings:
                print(f"  ! {warning}")
            print()

        # Recommendation
        if len(self.errors) == 0:
            print("[SUCCESS] System is ready to use!")
            print("\nNext steps:")
            print("  1. Start watchers: pm2 start ecosystem.config.js")
            print("  2. Check status: pm2 list")
            print("  3. Monitor messages: python monitor-messages.py")
            return True
        else:
            print("[FAILED] Please fix errors before starting")
            print("\nConsult:")
            print("  - SYSTEM_REQUIREMENTS.md (for setup help)")
            print("  - STARTUP_GUIDE.md (for troubleshooting)")
            return False

    def run_all_checks(self):
        """Run all validation checks"""
        print(f"\n===== Hackathon0Gold - System Validation ({datetime.now().strftime('%Y-%m-%d %H:%M')}) =====\n")

        self.check_python()
        self.check_pip_packages()
        self.check_nodejs()
        self.check_watchers()
        self.check_folders()
        self.check_config_files()
        self.check_pm2_status()
        self.check_messages()

        return self.generate_report()

def main():
    validator = Validator()
    success = validator.run_all_checks()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
