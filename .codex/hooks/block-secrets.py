#!/usr/bin/env python3
"""
PreToolUse hook: Blocks edits/writes to sensitive files and directories.
Exits with code 2 to deny the operation (per Claude Code hook specification).
"""

import sys
import os
import json

# Sensitive paths that should never be edited
BLOCKED_PATTERNS = [
    '.env',
    '.env.local',
    '.env.*.local',
    '**/secrets/**',
    '**/*secret_key*',
    '**/*_secret*',
    '**/*client_secret*',
    '**/*_password*',
    '**/*passwd*',
    '**/*api_key*',
    '**/*api-key*',
    '**/*apikey*',
    '**/*private_key*',
    '**/*private-key*',
    '**/.aws/**',
    '**/.ssh/**',
    '**/credentials/**',
    '**/config/secrets.*',
]

def normalize_path(path):
    """Normalize path for comparison."""
    return os.path.normpath(path).replace('\\', '/')

def is_blocked(file_path):
    """Check if a file path matches any blocked pattern."""
    normalized = normalize_path(file_path)
    
    for pattern in BLOCKED_PATTERNS:
        # Simple pattern matching
        if pattern.startswith('**/'):
            # Match anywhere in path
            pattern_suffix = pattern[3:]
            if pattern_suffix in normalized or normalized.endswith('/' + pattern_suffix):
                return True
        elif pattern.startswith('**/*'):
            # Match files with pattern in name
            pattern_suffix = pattern[4:]
            if pattern_suffix in normalized:
                return True
        elif pattern.startswith('.'):
            # Exact match or ends with pattern
            if normalized == pattern or normalized.endswith('/' + pattern):
                return True
        else:
            # Contains pattern
            if pattern in normalized:
                return True
    
    return False

def main():
    """Main hook entry point."""
    # Read hook context from stdin (Claude Code provides this)
    try:
        hook_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        # If no input, allow (shouldn't happen in PreToolUse)
        sys.exit(0)
    
    # Extract tool name and target
    tool_name = hook_data.get('tool', '')
    target = hook_data.get('target', '') or hook_data.get('file_path', '') or hook_data.get('path', '')
    
    # Only block write/edit operations
    write_tools = ['write', 'edit', 'search_replace', 'delete_file']
    
    if tool_name in write_tools:
        if target and is_blocked(target):
            print(f"BLOCKED: Attempt to modify sensitive file: {target}", file=sys.stderr)
            print(f"Pattern matched: {target}", file=sys.stderr)
            sys.exit(2)  # Exit code 2 = deny
    
    # Allow the operation
    sys.exit(0)

if __name__ == '__main__':
    main()
