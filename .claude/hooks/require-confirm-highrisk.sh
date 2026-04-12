#!/bin/bash
# PreToolUse hook: Intercepts risky Bash patterns and forces deny unless explicitly allowed
# Exits with code 2 to deny risky operations

# Read hook context from stdin (JSON)
HOOK_DATA=$(cat)

# Extract tool name and command
TOOL_NAME=$(echo "$HOOK_DATA" | grep -o '"tool"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 || echo "")
COMMAND=$(echo "$HOOK_DATA" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 || echo "")

# Only check bash/terminal commands
if [ "$TOOL_NAME" != "run_terminal_cmd" ] && [ "$TOOL_NAME" != "bash" ]; then
    exit 0
fi

# Risky patterns that should be blocked
RISKY_PATTERNS=(
    "rm -rf"
    "rm -r"
    "rm -f"
    "> /dev/"
    "> /proc/"
    "> /sys/"
    "dd if="
    "mkfs"
    "fdisk"
    "format"
    "chmod 777"
    "chmod +x /"
    "sudo rm"
    "sudo mv"
    "sudo cp"
    "sudo chmod"
    "sudo chown"
)

# Check if command contains risky patterns
for pattern in "${RISKY_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qi "$pattern"; then
        # Check if explicitly allowed (via environment variable)
        if [ "${CLAUDE_ALLOW_HIGHRISK:-false}" != "true" ]; then
            echo "BLOCKED: Risky command pattern detected: $pattern" >&2
            echo "Command: $COMMAND" >&2
            echo "Set CLAUDE_ALLOW_HIGHRISK=true to allow (not recommended)" >&2
            exit 2  # Exit code 2 = deny
        fi
    fi
done

# Allow the operation
exit 0
