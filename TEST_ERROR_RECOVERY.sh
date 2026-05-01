#!/bin/bash
# Prompt 6 Error Recovery - Quick Test Script
# Run this to verify all error recovery systems are working

echo "=================================="
echo "PROMPT 6: ERROR RECOVERY TEST SUITE"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test 1: Verify error_recovery.py loads
echo -e "${YELLOW}[TEST 1]${NC} Verify error_recovery module..."
python3 -c "from watchers.error_recovery import WatcherErrorRecovery; print('✓ error_recovery.py loads OK')" 2>/dev/null || echo "✗ FAILED"
echo ""

# Test 2: Verify error_handler.py loads
echo -e "${YELLOW}[TEST 2]${NC} Verify error_handler module..."
python3 -c "from skills.error_handler import SkillErrorHandler; print('✓ error_handler.py loads OK')" 2>/dev/null || echo "✗ FAILED"
echo ""

# Test 3: Check if Logs directory exists
echo -e "${YELLOW}[TEST 3]${NC} Check Logs directory..."
if [ -d "Logs" ]; then
    echo "✓ Logs/ directory exists"
    ls -la Logs/ | head -10
else
    echo "○ Logs/ directory will be created at runtime"
fi
echo ""

# Test 4: Check if Errors directory can be created
echo -e "${YELLOW}[TEST 4]${NC} Test Errors directory auto-creation..."
python3 -c "
from pathlib import Path
errors_dir = Path('Errors')
errors_dir.mkdir(parents=True, exist_ok=True)
if errors_dir.exists():
    print('✓ Errors/ directory created/exists')
else:
    print('✗ Failed to create Errors/')
" 2>/dev/null || echo "✗ FAILED"
echo ""

# Test 5: List updated watcher files
echo -e "${YELLOW}[TEST 5]${NC} Verify updated watcher files..."
watchers=(
    "watchers/gmail_watcher.py"
    "watchers/whatsapp_persistent.py"
    "watchers/linkedin_persistent.py"
    "watchers/instagram_watcher_fixed.py"
    "watchers/facebook_watcher_js_extract.py"
    "watchers/twitter_watcher.py"
)

for watcher in "${watchers[@]}"; do
    if grep -q "WatcherErrorRecovery" "$watcher" 2>/dev/null; then
        echo "✓ $(basename $watcher) has error recovery"
    else
        echo "✗ $(basename $watcher) missing error recovery"
    fi
done
echo ""

# Test 6: Simulate a simple error logging
echo -e "${YELLOW}[TEST 6]${NC} Test error logging functionality..."
python3 -c "
from watchers.error_recovery import WatcherErrorRecovery
from datetime import datetime

# Create test error recovery
recovery = WatcherErrorRecovery('test_watcher', '.')

# Log a test error
try:
    raise ValueError('Test error message')
except Exception as e:
    recovery.log_error(e, context='test_context', retry_count=1)
    print('✓ Error logged successfully')

# Check if log file was created
import os
from pathlib import Path
log_files = list(Path('Logs').glob('error_test_watcher_*.log'))
if log_files:
    print(f'✓ Log file created: {log_files[0].name}')
    print('  Content preview:')
    with open(log_files[0], 'r') as f:
        lines = f.readlines()[:10]
        for line in lines:
            print(f'    {line.rstrip()}')
else:
    print('✗ No log file created')
" 2>/dev/null || echo "✗ FAILED"
echo ""

# Test 7: Test exponential backoff calculation
echo -e "${YELLOW}[TEST 7]${NC} Test exponential backoff delays..."
python3 -c "
from watchers.error_recovery import WatcherErrorRecovery
recovery = WatcherErrorRecovery('test', '.')
print('Backoff sequence for retries:')
for i in range(1, 6):
    delay = recovery.get_delay(i)
    print(f'  Retry {i}: {delay:.1f}s')
" 2>/dev/null
echo ""

# Test 8: Test manual fallback creation
echo -e "${YELLOW}[TEST 8]${NC} Test manual fallback plan creation..."
python3 -c "
from skills.error_handler import SkillErrorHandler

handler = SkillErrorHandler('test_skill', '.')
handler.write_manual_fallback(
    'Test manual action required',
    context={'test': 'data'},
    priority='medium'
)
print('✓ Manual fallback created')

from pathlib import Path
plan_files = list(Path('Plans').glob('manual_test_skill_*.md'))
if plan_files:
    print(f'✓ Plan file: {plan_files[0].name}')
    print('  Content preview:')
    with open(plan_files[0], 'r') as f:
        lines = f.readlines()[:15]
        for line in lines:
            print(f'    {line.rstrip()}')
" 2>/dev/null || echo "✗ FAILED"
echo ""

# Summary
echo "=================================="
echo -e "${GREEN}TEST SUITE COMPLETE${NC}"
echo "=================================="
echo ""
echo "Key Directories:"
echo "  • Logs/                - Watcher error logs (auto-created)"
echo "  • Errors/              - Skill error logs (auto-created)"
echo "  • Plans/manual_*.md    - Manual fallback actions"
echo ""
echo "Next Steps:"
echo "  1. Run all 6 watchers with: pm2 start ecosystem.config.js"
echo "  2. Trigger errors and verify logging works"
echo "  3. Update remaining 10 skills with error_handler"
echo "  4. See PROMPT_6_IMPLEMENTATION_SUMMARY.md for full test guide"
echo ""
