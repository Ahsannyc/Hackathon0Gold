#!/bin/bash
#
# Ralph Wiggum Loop Convenience Wrapper
# Makes it easy to run autonomous tasks
#
# Usage:
#   ./tools/run_ralph_loop.sh task_id "Your task description"
#   ./tools/run_ralph_loop.sh task_id "Your task" --max-iterations 15
#   ./tools/run_ralph_loop.sh task_id "Your task" --use-promise
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VAULT_DIR="$(dirname "$SCRIPT_DIR")"

# Defaults
MAX_ITERATIONS=10
USE_PROMISE=false
TIMEOUT=300

# Parse arguments
if [ $# -lt 2 ]; then
    echo -e "${RED}Usage: $0 <task_id> <prompt> [--max-iterations N] [--use-promise] [--timeout SECONDS]${NC}"
    echo ""
    echo "Examples:"
    echo "  $0 invoices_daily 'Process all invoices'"
    echo "  $0 social_weekly 'Post weekly content' --max-iterations 20"
    echo "  $0 emails_test 'Send confirmation' --use-promise"
    exit 1
fi

TASK_ID=$1
PROMPT=$2
shift 2

# Parse optional arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --max-iterations)
            MAX_ITERATIONS="$2"
            shift 2
            ;;
        --use-promise)
            USE_PROMISE=true
            shift
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          Ralph Wiggum Loop Executor                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Task ID:${NC}          $TASK_ID"
echo -e "${YELLOW}Prompt:${NC}          $PROMPT"
echo -e "${YELLOW}Max Iterations:${NC}   $MAX_ITERATIONS"
echo -e "${YELLOW}Use Promise:${NC}      $USE_PROMISE"
echo -e "${YELLOW}Timeout/Iter:${NC}     ${TIMEOUT}s"
echo ""

# Verify executor exists
if [ ! -f "$SCRIPT_DIR/ralph_wiggum_executor.py" ]; then
    echo -e "${RED}Error: ralph_wiggum_executor.py not found${NC}"
    exit 1
fi

# Verify vault structure
for folder in Plans Done Logs .ralph-state; do
    if [ ! -d "$VAULT_DIR/$folder" ]; then
        echo -e "${YELLOW}Creating missing folder: $folder${NC}"
        mkdir -p "$VAULT_DIR/$folder"
    fi
done

# Build Python command
PYTHON_CMD="python3 $SCRIPT_DIR/ralph_wiggum_executor.py \"$TASK_ID\" \"$PROMPT\" --max-iterations $MAX_ITERATIONS --timeout $TIMEOUT"

if [ "$USE_PROMISE" = true ]; then
    PYTHON_CMD="$PYTHON_CMD --use-promise"
fi

# Execute
echo -e "${GREEN}Starting Ralph Wiggum loop...${NC}"
echo ""

# Change to vault directory for relative paths
cd "$VAULT_DIR"

# Run the executor and capture output
if eval "$PYTHON_CMD"; then
    RESULT=$?
    echo ""
    echo -e "${GREEN}✓ Task completed successfully${NC}"

    # Show results
    if [ -f ".ralph-state/$TASK_ID.json" ]; then
        echo ""
        echo -e "${BLUE}Task State:${NC}"
        cat ".ralph-state/$TASK_ID.json" | python3 -m json.tool
    fi

    exit 0
else
    RESULT=$?
    echo ""
    echo -e "${RED}✗ Task execution failed or incomplete${NC}"

    # Show state for debugging
    if [ -f ".ralph-state/$TASK_ID.json" ]; then
        echo ""
        echo -e "${YELLOW}Task State (for debugging):${NC}"
        cat ".ralph-state/$TASK_ID.json" | python3 -m json.tool
    fi

    echo ""
    echo -e "${YELLOW}Debugging tips:${NC}"
    echo "  1. Check logs: tail -50 Logs/ralph_wiggum.log"
    echo "  2. Check task file: cat Plans/TASK_$TASK_ID.md"
    echo "  3. Check state: cat .ralph-state/$TASK_ID.json | python3 -m json.tool"

    exit $RESULT
fi
