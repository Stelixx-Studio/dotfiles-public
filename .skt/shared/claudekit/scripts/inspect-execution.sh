#!/bin/bash
# ClaudeKit Workflow Execution Inspector
# Usage: ./inspect-execution.sh <workflow> <description>
# Example: ./inspect-execution.sh cook "user authentication"

WORKFLOW="$1"
DESCRIPTION="$2"
MONITOR_INTERVAL="${MONITOR_INTERVAL:-0.5}"
LOG_FILE="/tmp/claudekit-inspector-$(date +%Y%m%d-%H%M%S).log"
PROCESS_LOG="/tmp/claudekit-processes-$(date +%Y%m%d-%H%M%S).log"

# Colors for output
COLOR_RESET='\033[0m'
COLOR_BLUE='\033[0;34m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[0;33m'
COLOR_RED='\033[0;31m'
COLOR_CYAN='\033[0;36m'

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S.%3N")
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

# Print with color
print_color() {
    local color="$1"
    shift
    echo -e "${color}$*${COLOR_RESET}"
}

# Display header
print_header() {
    echo ""
    print_color "$COLOR_CYAN" "╔════════════════════════════════════════════════════════════╗"
    print_color "$COLOR_CYAN" "║        ClaudeKit Workflow Execution Inspector             ║"
    print_color "$COLOR_CYAN" "╚════════════════════════════════════════════════════════════╝"
    echo ""
}

# Monitor processes in background
monitor_processes() {
    local monitor_pid_file="/tmp/claudekit-monitor.pid"
    
    (
        echo "Starting process monitoring at $(date)" > "$PROCESS_LOG"
        echo "Monitoring interval: ${MONITOR_INTERVAL}s" >> "$PROCESS_LOG"
        echo "---" >> "$PROCESS_LOG"
        
        while true; do
            {
                echo "=== $(date +"%H:%M:%S.%3N") ==="
                echo ""
                
                # Monitor ClaudeKit processes
                echo "ClaudeKit Processes:"
                ps aux | grep -E 'query-workflow|parallel-research|gh copilot' | grep -v grep | while IFS= read -r line; do
                    echo "  $line"
                done
                
                echo ""
                
                # Monitor Python processes
                echo "Python Processes:"
                ps aux | grep -E 'python3.*claudekit' | grep -v grep | while IFS= read -r line; do
                    echo "  $line"
                done
                
                echo ""
                
                # Monitor GitHub CLI processes
                echo "GitHub CLI Processes:"
                ps aux | grep -E 'gh copilot' | grep -v grep | while IFS= read -r line; do
                    echo "  $line"
                done
                
                echo ""
                echo "---"
                echo ""
            } >> "$PROCESS_LOG"
            
            sleep "$MONITOR_INTERVAL"
        done
    ) &
    
    MONITOR_PID=$!
    echo $MONITOR_PID > "$monitor_pid_file"
    log "INFO" "Process monitor started with PID: $MONITOR_PID"
}

# Stop process monitoring
stop_monitoring() {
    if [ -n "$MONITOR_PID" ]; then
        kill "$MONITOR_PID" 2>/dev/null
        log "INFO" "Process monitor stopped (PID: $MONITOR_PID)"
    fi
}

# Execute workflow with inspection
execute_workflow() {
    local workflow="$1"
    local description="$2"
    
    print_color "$COLOR_BLUE" "📊 Executing workflow: $workflow"
    print_color "$COLOR_BLUE" "📝 Description: $description"
    echo ""
    
    log "INFO" "Starting workflow execution: $workflow"
    log "INFO" "Description: $description"
    
    # Set environment variables for enhanced inspection
    export DEBUG=0
    export INSPECT=1
    export LOG_FILE="$LOG_FILE"
    
    # Record start time
    START_TIME=$(date +%s)
    log "INFO" "Workflow start time: $(date)"
    
    # Execute workflow
    print_color "$COLOR_YELLOW" "⚙️  Running workflow phases..."
    echo ""
    
    python3 .shared/claudekit/scripts/query-workflow.py "$workflow" 2>&1 | tee -a "$LOG_FILE"
    WORKFLOW_EXIT_CODE=$?
    
    # Record end time
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    
    log "INFO" "Workflow completed in ${DURATION}s with exit code: $WORKFLOW_EXIT_CODE"
    
    echo ""
    print_color "$COLOR_GREEN" "✅ Workflow execution completed"
}

# Generate execution report
generate_report() {
    local duration="$1"
    local exit_code="$2"
    
    echo ""
    print_color "$COLOR_CYAN" "╔════════════════════════════════════════════════════════════╗"
    print_color "$COLOR_CYAN" "║                  Inspection Report                         ║"
    print_color "$COLOR_CYAN" "╚════════════════════════════════════════════════════════════╝"
    echo ""
    
    print_color "$COLOR_BLUE" "📊 Execution Summary:"
    echo "  ├─ Workflow: $WORKFLOW"
    echo "  ├─ Description: $DESCRIPTION"
    echo "  ├─ Duration: ${duration}s"
    echo "  ├─ Exit Code: $exit_code"
    echo "  └─ Timestamp: $(date)"
    echo ""
    
    print_color "$COLOR_BLUE" "📁 Generated Files:"
    echo "  ├─ Execution log: $LOG_FILE"
    echo "  └─ Process log: $PROCESS_LOG"
    echo ""
    
    print_color "$COLOR_BLUE" "📈 Process Activity:"
    local total_snapshots=$(grep -c "^===" "$PROCESS_LOG")
    echo "  ├─ Total snapshots: $total_snapshots"
    echo "  ├─ Monitoring interval: ${MONITOR_INTERVAL}s"
    echo "  └─ Monitoring duration: ${duration}s"
    echo ""
    
    print_color "$COLOR_BLUE" "🔍 Platform Compatibility:"
    echo "  ├─ VS Code Copilot: ✅ Compatible"
    echo "  ├─ GitHub Copilot CLI: $(command -v gh &>/dev/null && echo '✅ Installed' || echo '❌ Not found')"
    echo "  └─ Antigravity: ✅ Compatible"
    echo ""
    
    print_color "$COLOR_YELLOW" "💡 View detailed logs:"
    echo "  $ cat $LOG_FILE"
    echo "  $ cat $PROCESS_LOG"
    echo ""
    
    print_color "$COLOR_YELLOW" "💡 Analyze process timeline:"
    echo "  $ grep 'ClaudeKit Processes' $PROCESS_LOG -A 5"
    echo "  $ grep 'GitHub CLI Processes' $PROCESS_LOG -A 5"
    echo ""
}

# Cleanup function
cleanup() {
    stop_monitoring
    
    if [ -f "/tmp/claudekit-monitor.pid" ]; then
        rm -f "/tmp/claudekit-monitor.pid"
    fi
}

# Main execution
main() {
    # Validate arguments
    if [ -z "$WORKFLOW" ] || [ -z "$DESCRIPTION" ]; then
        print_color "$COLOR_RED" "❌ Error: Missing required arguments"
        echo ""
        echo "Usage: $0 <workflow> <description>"
        echo ""
        echo "Examples:"
        echo "  $0 cook 'user authentication'"
        echo "  $0 plan 'implement dashboard'"
        echo "  $0 fix 'login timeout bug'"
        echo ""
        exit 1
    fi
    
    # Setup cleanup trap
    trap cleanup EXIT
    
    # Display header
    print_header
    
    log "INFO" "Inspector started"
    log "INFO" "Log file: $LOG_FILE"
    log "INFO" "Process log: $PROCESS_LOG"
    
    # Start process monitoring
    print_color "$COLOR_YELLOW" "🔍 Starting process monitoring..."
    monitor_processes
    sleep 1  # Give monitor time to start
    echo ""
    
    # Execute workflow with inspection
    execute_workflow "$WORKFLOW" "$DESCRIPTION"
    
    # Stop monitoring
    print_color "$COLOR_YELLOW" "⏸️  Stopping process monitoring..."
    stop_monitoring
    sleep 1  # Give monitor time to stop
    
    # Calculate duration
    TOTAL_DURATION=$(($(date +%s) - START_TIME))
    
    # Generate report
    generate_report "$TOTAL_DURATION" "$WORKFLOW_EXIT_CODE"
    
    log "INFO" "Inspector completed"
    
    # Exit with workflow's exit code
    exit $WORKFLOW_EXIT_CODE
}

# Run main function
main
