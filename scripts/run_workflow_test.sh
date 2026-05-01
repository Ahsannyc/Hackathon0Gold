#!/bin/bash

################################################################################
# AI Social Media Manager - Full Workflow Test Script
#
# This script automates the complete workflow test:
# 1. Start Master Orchestrator
# 2. Create draft posts
# 3. Approve and move to orchestrator
# 4. Monitor processing and completion
# 5. Verify success and generate report
#
# Usage:
#   ./scripts/run_workflow_test.sh [--platform PLATFORM] [--count N] [--batch]
#
# Examples:
#   ./scripts/run_workflow_test.sh                    # Interactive mode
#   ./scripts/run_workflow_test.sh --platform facebook --count 1
#   ./scripts/run_workflow_test.sh --batch            # All 6 platforms
#
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ORCHESTRATOR_SCRIPT="$SCRIPT_DIR/master_orchestrator.py"
TRIGGER_SCRIPT="$SCRIPT_DIR/trigger_posts.py"
EXECUTOR_SCRIPT="$SCRIPT_DIR/social_media_executor_v2.py"

PENDING_DIR="$PROJECT_ROOT/Pending_Approval"
APPROVED_DIR="$PROJECT_ROOT/Approved"
DONE_DIR="$PROJECT_ROOT/Done"
LOGS_DIR="$PROJECT_ROOT/Logs"

# Test configuration
PLATFORMS=("facebook" "linkedin" "twitter" "instagram" "whatsapp" "gmail")
TEST_COUNT=1
BATCH_MODE=false
SELECTED_PLATFORM=""

################################################################################
# Helper Functions
################################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

check_dependencies() {
    log_info "Checking dependencies..."

    # Check Python version
    if ! command -v python &> /dev/null; then
        log_error "Python not found"
        return 1
    fi

    # Check required modules
    python -c "import yaml" 2>/dev/null || { log_error "PyYAML not installed"; return 1; }
    python -c "import watchdog" 2>/dev/null || { log_error "watchdog not installed"; return 1; }
    python -c "import playwright" 2>/dev/null || { log_error "Playwright not installed"; return 1; }

    log_success "All dependencies installed"
    return 0
}

check_directories() {
    log_info "Checking directory structure..."

    for dir in "$PENDING_DIR" "$APPROVED_DIR" "$DONE_DIR" "$LOGS_DIR"; do
        if [ ! -d "$dir" ]; then
            log_warning "Creating directory: $dir"
            mkdir -p "$dir"
        fi
    done

    log_success "Directory structure verified"
}

check_scripts() {
    log_info "Checking script files..."

    if [ ! -f "$ORCHESTRATOR_SCRIPT" ]; then
        log_error "Orchestrator script not found: $ORCHESTRATOR_SCRIPT"
        return 1
    fi

    if [ ! -f "$TRIGGER_SCRIPT" ]; then
        log_error "Trigger script not found: $TRIGGER_SCRIPT"
        return 1
    fi

    if [ ! -f "$EXECUTOR_SCRIPT" ]; then
        log_error "Executor script not found: $EXECUTOR_SCRIPT"
        return 1
    fi

    log_success "All scripts found"
    return 0
}

show_menu() {
    echo ""
    echo -e "${BLUE}=== AI Social Media Manager - Workflow Test ===${NC}"
    echo ""
    echo "Select test mode:"
    echo "  1) Single Platform Test"
    echo "  2) Multi-Platform Batch Test (all 6)"
    echo "  3) Custom Test (specify platform and count)"
    echo "  4) Error Recovery Test"
    echo "  5) View Logs and Status"
    echo "  6) Clean Up Test Files"
    echo "  7) Exit"
    echo ""
    read -p "Enter choice (1-7): " choice

    case $choice in
        1) test_single_platform ;;
        2) test_batch_all ;;
        3) test_custom ;;
        4) test_error_recovery ;;
        5) view_logs ;;
        6) cleanup_test_files ;;
        7) log_info "Exiting"; exit 0 ;;
        *) log_error "Invalid choice"; show_menu ;;
    esac
}

start_orchestrator() {
    log_info "Starting Master Orchestrator..."
    echo ""
    echo "Opening new terminal for orchestrator (you may need to close it manually when done)"
    echo "If not working, start manually in separate terminal:"
    echo "  python $ORCHESTRATOR_SCRIPT"
    echo ""

    # Try to detect OS and open appropriate terminal
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux: try gnome-terminal, xterm, or konsole
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- python "$ORCHESTRATOR_SCRIPT" &
        elif command -v xterm &> /dev/null; then
            xterm -e python "$ORCHESTRATOR_SCRIPT" &
        else
            # Fallback: run in background
            python "$ORCHESTRATOR_SCRIPT" > "$LOGS_DIR/orchestrator_$(date +%Y-%m-%d).log" 2>&1 &
            ORCH_PID=$!
            log_info "Orchestrator started (PID: $ORCH_PID)"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open -a Terminal "$(which python)" "$ORCHESTRATOR_SCRIPT" &
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Windows
        start cmd.exe /k "python \"$ORCHESTRATOR_SCRIPT\""
    else
        # Fallback
        python "$ORCHESTRATOR_SCRIPT" > "$LOGS_DIR/orchestrator_$(date +%Y-%m-%d).log" 2>&1 &
        log_info "Orchestrator started in background"
    fi

    sleep 3
    log_success "Orchestrator started"
}

create_draft_post() {
    local platform=$1
    local content=$2
    local title=${3:-"Test Post"}

    log_info "Creating draft post for platform: $platform"

    python "$TRIGGER_SCRIPT" \
        -p "$platform" \
        -c "$content" \
        -t "$title" \
        --preview > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        log_success "Draft created for $platform"
        return 0
    else
        log_error "Failed to create draft for $platform"
        return 1
    fi
}

approve_posts() {
    local count=$(ls "$PENDING_DIR"/POST_*.md 2>/dev/null | wc -l)

    if [ $count -eq 0 ]; then
        log_warning "No posts to approve in $PENDING_DIR"
        return 1
    fi

    log_info "Approving $count post(s)..."
    mv "$PENDING_DIR"/POST_*.md "$APPROVED_DIR/" 2>/dev/null || true

    log_success "Approved $count post(s)"
    return 0
}

monitor_processing() {
    local max_wait=${1:-300}  # Default 5 minutes
    local start_time=$(date +%s)
    local initial_approved=$(ls "$APPROVED_DIR"/POST_*.md 2>/dev/null | wc -l)

    log_info "Monitoring processing (timeout: ${max_wait}s)..."

    while true; do
        local current_time=$(date +%s)
        local elapsed=$((current_time - start_time))

        if [ $elapsed -gt $max_wait ]; then
            log_warning "Monitoring timeout after ${max_wait}s"
            break
        fi

        local approved_now=$(ls "$APPROVED_DIR"/POST_*.md 2>/dev/null | wc -l)
        local done_now=$(ls "$DONE_DIR"/processed_POST_*.md 2>/dev/null | wc -l)

        echo -ne "\r[${elapsed}s] Approved: $approved_now | Done: $done_now"

        if [ $approved_now -eq 0 ] && [ $done_now -gt 0 ]; then
            echo ""
            log_success "All posts processed!"
            return 0
        fi

        sleep 2
    done

    echo ""
    log_warning "Monitoring completed with remaining posts"
    return 1
}

verify_results() {
    log_info "Verifying test results..."
    echo ""

    local pending=$(ls "$PENDING_DIR"/POST_*.md 2>/dev/null | wc -l)
    local approved=$(ls "$APPROVED_DIR"/POST_*.md 2>/dev/null | wc -l)
    local done=$(ls "$DONE_DIR"/processed_POST_*.md 2>/dev/null | wc -l)

    echo "Status Summary:"
    echo "  Pending Approval: $pending"
    echo "  Approved (Processing): $approved"
    echo "  Done (Completed): $done"
    echo ""

    # Check for errors
    local errors=$(grep -c "✗\|Error\|FAILED" "$LOGS_DIR"/orchestrator_*.log 2>/dev/null || echo "0")

    if [ "$errors" -gt 0 ]; then
        log_warning "Found $errors error(s) in logs"
    else
        log_success "No errors found"
    fi

    # Overall result
    if [ $done -gt 0 ] && [ $approved -eq 0 ]; then
        log_success "✓ Test PASSED - All posts processed successfully"
        return 0
    elif [ $done -gt 0 ]; then
        log_warning "Test PARTIAL - Some posts processed, some still pending"
        return 1
    else
        log_error "Test FAILED - No posts processed"
        return 1
    fi
}

test_single_platform() {
    echo ""
    log_info "=== Single Platform Test ==="
    echo ""
    echo "Available platforms: ${PLATFORMS[@]}"
    read -p "Enter platform (default: facebook): " platform
    platform=${platform:-facebook}

    # Validate platform
    if [[ ! " ${PLATFORMS[@]} " =~ " ${platform} " ]]; then
        log_error "Invalid platform: $platform"
        return 1
    fi

    start_orchestrator

    sleep 5
    read -p "Press Enter to create draft post..."

    create_draft_post "$platform" "🚀 Test from automation system!" "Test Post"

    read -p "Press Enter to approve post..."
    approve_posts

    echo ""
    monitor_processing 120  # 2 minute timeout

    echo ""
    verify_results
}

test_batch_all() {
    log_info "=== Batch Test (All 6 Platforms) ==="
    echo ""

    start_orchestrator

    sleep 5
    log_info "Creating draft posts for all 6 platforms..."

    for i in "${!PLATFORMS[@]}"; do
        platform="${PLATFORMS[$i]}"
        create_draft_post "$platform" "Batch test for $platform (#$((i+1))/6)" "Test Post - $platform"
        sleep 1
    done

    echo ""
    read -p "Press Enter to approve all posts..."
    approve_posts

    echo ""
    log_info "Monitoring batch processing (approx 5-10 minutes)..."
    monitor_processing 600  # 10 minute timeout

    echo ""
    verify_results
}

test_custom() {
    echo ""
    log_info "=== Custom Test ==="
    echo ""
    echo "Available platforms: ${PLATFORMS[@]}"
    read -p "Enter platform: " platform
    read -p "Enter number of posts to create: " count

    platform=${platform:-facebook}
    count=${count:-1}

    # Validate
    if [[ ! " ${PLATFORMS[@]} " =~ " ${platform} " ]]; then
        log_error "Invalid platform"
        return 1
    fi

    if ! [[ "$count" =~ ^[0-9]+$ ]] || [ $count -le 0 ]; then
        log_error "Invalid count"
        return 1
    fi

    start_orchestrator

    sleep 5
    log_info "Creating $count draft post(s) for $platform..."

    for ((i=1; i<=count; i++)); do
        create_draft_post "$platform" "Custom test post #$i" "Test Post #$i"
        sleep 1
    done

    echo ""
    read -p "Press Enter to approve all posts..."
    approve_posts

    echo ""
    timeout_seconds=$((count * 40))  # ~40 seconds per post
    log_info "Monitoring processing (approx ${timeout_seconds}s)..."
    monitor_processing "$timeout_seconds"

    echo ""
    verify_results
}

test_error_recovery() {
    log_info "=== Error Recovery Test ==="
    echo ""
    log_warning "This test creates a post and simulates a failure scenario"
    echo ""

    start_orchestrator

    sleep 5
    create_draft_post "facebook" "Error recovery test" "Error Test"
    approve_posts

    sleep 5
    log_warning "Now manually close the browser window to simulate failure..."
    sleep 10

    log_info "Checking if orchestrator retries..."
    sleep 300  # 5 minute retry cooldown

    log_info "Checking status..."
    local approved=$(ls "$APPROVED_DIR"/POST_*.md 2>/dev/null | wc -l)

    if [ $approved -gt 0 ]; then
        log_warning "Post is in retry cooldown - waiting for automatic retry"
        monitor_processing 300
    fi

    verify_results
}

view_logs() {
    echo ""
    log_info "=== Latest Log Entries ==="
    echo ""

    if [ -f "$LOGS_DIR"/orchestrator_*.log ]; then
        log_info "Orchestrator logs:"
        tail -20 "$LOGS_DIR"/orchestrator_*.log | grep -E "Processing|Executing|SUCCESS|FAILED" || echo "  (no entries)"
        echo ""
    fi

    if [ -f "$LOGS_DIR"/trigger_posts_*.log ]; then
        log_info "Trigger posts logs:"
        tail -10 "$LOGS_DIR"/trigger_posts_*.log | grep "Post created" || echo "  (no entries)"
        echo ""
    fi

    log_info "File status:"
    echo "  Pending: $(ls "$PENDING_DIR"/POST_*.md 2>/dev/null | wc -l)"
    echo "  Approved: $(ls "$APPROVED_DIR"/POST_*.md 2>/dev/null | wc -l)"
    echo "  Done: $(ls "$DONE_DIR"/processed_POST_*.md 2>/dev/null | wc -l)"
    echo ""
}

cleanup_test_files() {
    echo ""
    log_warning "This will DELETE all test files!"
    read -p "Are you sure? (yes/no): " confirm

    if [ "$confirm" != "yes" ]; then
        log_info "Cleanup cancelled"
        return 0
    fi

    rm -f "$PENDING_DIR"/POST_test_*.md 2>/dev/null || true
    rm -f "$APPROVED_DIR"/POST_test_*.md 2>/dev/null || true
    rm -f "$DONE_DIR"/processed_POST_test_*.md 2>/dev/null || true

    log_success "Test files cleaned up"
}

################################################################################
# Main Execution
################################################################################

main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║   AI Social Media Manager - Workflow Test Script              ║"
    echo "║   Testing: Trigger Posts → Orchestrator → Executor            ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    # Pre-test checks
    check_dependencies || exit 1
    check_directories
    check_scripts || exit 1

    # Parse command-line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --platform)
                SELECTED_PLATFORM="$2"
                shift 2
                ;;
            --count)
                TEST_COUNT="$2"
                shift 2
                ;;
            --batch)
                BATCH_MODE=true
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    # Run based on arguments or show menu
    if [ -n "$SELECTED_PLATFORM" ]; then
        start_orchestrator
        sleep 5
        for ((i=1; i<=TEST_COUNT; i++)); do
            create_draft_post "$SELECTED_PLATFORM" "Test post #$i" "Test Post #$i"
            sleep 1
        done
        approve_posts
        monitor_processing $((TEST_COUNT * 40))
        verify_results
    elif [ "$BATCH_MODE" = true ]; then
        test_batch_all
    else
        show_menu
    fi
}

# Run main function
main "$@"
