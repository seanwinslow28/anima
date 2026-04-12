#!/bin/bash
# PostToolUse hook: Logs tool usage for audit trail
# Non-blocking - always exits 0

LOG_FILE="${CLAUDE_LOG_DIR:-.claude}/tool-use.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Read hook context from stdin (JSON)
HOOK_DATA=$(cat)

# Extract tool name and target (best effort parsing)
TOOL_NAME=$(echo "$HOOK_DATA" | grep -o '"tool"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 || echo "unknown")
TARGET=$(echo "$HOOK_DATA" | grep -o '"target"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 || echo "$HOOK_DATA" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 || echo "N/A")

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Append to log file
echo "[$TIMESTAMP] tool=$TOOL_NAME target=$TARGET" >> "$LOG_FILE"

# Always allow (non-blocking)
exit 0
