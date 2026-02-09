#!/bin/bash
# 🚨 AUTO-GENERATED - DO NOT EDIT 🚨 Source: features/claudekit/templates/parallel-research.sh
# Parallel research using Agent Executor (supports Gemini/OpenCode/Copilot) or CSV fallback
# Usage: ./parallel-research.sh "feature description"
# Debug mode: DEBUG=1 ./parallel-research.sh "feature description"
# Inspect mode: INSPECT=1 ./parallel-research.sh "feature description"
# Force CSV: USE_CSV=1 ./parallel-research.sh "feature description"

FEATURE="$1"
TMP_DIR="/tmp/claudekit-research"
LOG_FILE="${LOG_FILE:-/tmp/claudekit-research.log}"
DEBUG="${DEBUG:-0}"
INSPECT="${INSPECT:-0}"
USE_CSV="${USE_CSV:-0}"

# Enable debug tracing if requested
if [ "$DEBUG" = "1" ]; then
    set -x
fi

# Logging function with timestamps
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp
    timestamp=$(date +"%Y-%m-%d %H:%M:%S.%3N")
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# Create temp directory
mkdir -p "$TMP_DIR"

# Cleanup function (keep logs in inspect mode)
cleanup() {
    if [ "$INSPECT" = "1" ]; then
        log "INFO" "Inspect mode: Keeping temp files in $TMP_DIR"
        log "INFO" "Logs saved to: $LOG_FILE"
    else
        rm -rf "$TMP_DIR"
    fi
}
trap cleanup EXIT

log "INFO" "Starting parallel research for: $FEATURE"
echo "🔍 Running parallel research for: $FEATURE"

# Locate scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_EXECUTOR="$SCRIPT_DIR/../../workflows/scripts/agent_executor.py"
SEARCH_SCRIPT="$SCRIPT_DIR/../../ui-ux-pro-max/scripts/search.py"
QUERY_SCRIPT="$SCRIPT_DIR/../../instructions/scripts/query-rules.py"

# UI-Aware Design Intelligence (Powered by UI/UX Pro Max)
UI_KEYWORDS="ui|ux|landing|dashboard|component|style|color|layout|responsive|interface|mobile"
if echo "$FEATURE" | grep -Ei "$UI_KEYWORDS" > /dev/null; then
    log "INFO" "UI-related keywords detected, spawning query 4: Design Intelligence"
    if [ -f "$SEARCH_SCRIPT" ]; then
        python3 "$SEARCH_SCRIPT" "$FEATURE" --domain product --domain style > "$TMP_DIR/ui-ux-intelligence.md" 2>&1 &
        PID4=$!
        log "INFO" "Query 4 (UI/UX) started with PID: $PID4"
    else
        log "WARN" "UI/UX search script not found at $SEARCH_SCRIPT"
    fi
fi

# Strategy Selection
USE_AGENT_EXECUTOR=0

if [ "$USE_CSV" = "0" ] && [ -f "$AGENT_EXECUTOR" ]; then
    log "INFO" "Agent Executor found at $AGENT_EXECUTOR"
    USE_AGENT_EXECUTOR=1
else
    log "INFO" "Agent Executor not found or disabled, checking legacy CLI or CSV"
fi

if [ "$USE_AGENT_EXECUTOR" = "1" ]; then
    log "INFO" "Delegating research to Agent Executor (Multi-Agent)"
    echo "✅ Using Agent Executor (Gemini/OpenCode/Copilot)"
    
    # Run Agent Executor for 3 aspects in parallel (managed by python script internally or here?)
    # agent_executor.py aggregates tools for ONE query.
    # But parallel-research.sh wants 3 distinct queries: Best Practices, Patterns, Security.
    # So we call agent_executor.py 3 times in parallel!
    
    log "INFO" "Spawning Executor 1: Best practices"
    python3 "$AGENT_EXECUTOR" "Best practices for: $FEATURE" < /dev/null > "$TMP_DIR/best-practices.md" 2>&1
    EXIT_CODE_1=$?
    log "INFO" "Executor 1 completed with exit code: $EXIT_CODE_1"

    log "INFO" "Spawning Executor 2: Common patterns"
    python3 "$AGENT_EXECUTOR" "Common patterns for: $FEATURE" < /dev/null > "$TMP_DIR/patterns.md" 2>&1
    EXIT_CODE_2=$?
    log "INFO" "Executor 2 completed with exit code: $EXIT_CODE_2"

    log "INFO" "Spawning Executor 3: Security considerations"
    python3 "$AGENT_EXECUTOR" "Security considerations for: $FEATURE" < /dev/null > "$TMP_DIR/security.md" 2>&1
    EXIT_CODE_3=$?
    log "INFO" "Executor 3 completed with exit code: $EXIT_CODE_3"

    # Wait logic (Legacy parallel code removed for stability)
    START_TIME=$(date +%s)


    if [ -n "$PID4" ]; then
        wait "$PID4"
        EXIT_CODE_4=$?
        log "INFO" "Query 4 (UI/UX) completed with exit code: $EXIT_CODE_4"
    fi
    
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    log "INFO" "All agents completed in ${DURATION}s"

else
    # Fallback to CSV Database (Legacy/Offline)
    log "INFO" "Using CSV database for research (Fallback)"
    echo "✅ Using CSV database (instant, offline, comprehensive)"
    echo ""
    
    if [ -f "$QUERY_SCRIPT" ]; then
        python3 "$QUERY_SCRIPT" --format markdown
        RET_CODE=$?
        if [ $RET_CODE -ne 0 ]; then
            log "ERROR" "CSV database query failed with code $RET_CODE"
            echo "❌ Error: CSV database query failed"
            exit $RET_CODE
        fi
        log "INFO" "CSV database research complete"
        
        # Include UI Intelligence if available
        if [ -n "$PID4" ]; then
            wait "$PID4"
            if [ -f "$TMP_DIR/ui-ux-intelligence.md" ]; then
                echo ""
                echo "## UI/UX Design Intelligence (Pro Max)"
                cat "$TMP_DIR/ui-ux-intelligence.md"
            fi
        fi
        
        echo ""
        echo "✅ Research complete (CSV database)"
        exit 0
    else
        log "ERROR" "CSV database query script not found: $QUERY_SCRIPT"
        echo "❌ Error: CSV database not available"
        exit 1
    fi
fi

# Aggregate results
echo ""
echo "📚 Research Results:"
echo "===================="
echo ""

if [ "$INSPECT" = "1" ]; then
    log "INFO" "Inspect mode: Displaying file sizes and line counts"
    echo "📊 Inspection Details:"
    echo "---"
    for file in "$TMP_DIR"/*.md; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            size=$(wc -c < "$file")
            lines=$(wc -l < "$file")
            log "INFO" "$filename: $lines lines, $size bytes"
            echo "  - $filename: $lines lines, $size bytes"
        fi
    done
    echo ""
fi

log "INFO" "Aggregating results..."

echo "## Best Practices"
cat "$TMP_DIR/best-practices.md" 2>/dev/null || echo "No results."
echo ""

echo "## Common Patterns"
cat "$TMP_DIR/patterns.md" 2>/dev/null || echo "No results."
echo ""

echo "## Security Considerations"
cat "$TMP_DIR/security.md" 2>/dev/null || echo "No results."
echo ""

if [ -f "$TMP_DIR/ui-ux-intelligence.md" ]; then
    echo "## UI/UX Design Intelligence (Pro Max)"
    cat "$TMP_DIR/ui-ux-intelligence.md"
    echo ""
fi

log "INFO" "Research complete"

# Check aggregated exit codes
# If Agent executor runs, it returns 0 even if tools fail (it reports errors in output).
# But we can check if file is empty or missing if needed.
# For now, simplistic exit code check.
if [ "$EXIT_CODE_1" != "0" ] || [ "$EXIT_CODE_2" != "0" ] || [ "$EXIT_CODE_3" != "0" ]; then
    log "WARN" "Some research agents failed"
    echo "⚠️  Warning: Some research agents failed to complete."
else
    echo "✅ Research complete"
fi

if [ "$INSPECT" = "1" ]; then
    echo ""
    echo "🔍 Inspection Summary:"
    echo "  - Duration: ${DURATION}s"
    echo "  - PIDs: $PID1, $PID2, $PID3"
    echo "  - Exit codes: $EXIT_CODE_1, $EXIT_CODE_2, $EXIT_CODE_3"
    echo "  - Logs: $LOG_FILE"
    echo "  - Temp files: $TMP_DIR"
fi

# Disable debug tracing
if [ "$DEBUG" = "1" ]; then
    set +x
fi
