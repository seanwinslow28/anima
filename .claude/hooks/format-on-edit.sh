#!/bin/bash
# PostToolUse hook: Auto-formats files after edit
# Non-blocking - runs formatter in background

# Read hook context from stdin (JSON)
HOOK_DATA=$(cat)

# Extract file path
FILE_PATH=$(echo "$HOOK_DATA" | grep -o '"target"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 || echo "$HOOK_DATA" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 || echo "")

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Determine formatter based on file extension
case "$FILE_PATH" in
    *.js|*.jsx|*.ts|*.tsx|*.json|*.css|*.scss|*.md)
        # Try prettier if available
        if command -v prettier >/dev/null 2>&1; then
            prettier --write "$FILE_PATH" >/dev/null 2>&1 &
        fi
        ;;
    *.py)
        # Try black if available
        if command -v black >/dev/null 2>&1; then
            black "$FILE_PATH" >/dev/null 2>&1 &
        fi
        ;;
    *)
        # Unknown file type, skip
        ;;
esac

# Always allow (non-blocking)
exit 0
