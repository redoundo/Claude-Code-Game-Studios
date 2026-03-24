#!/bin/bash

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_LOG_DIR="production/session-logs"
STATE_FILE="production/session-state/active.md"

mkdir -p "$SESSION_LOG_DIR" 2>/dev/null

RECENT_COMMITS=$(git log --oneline --since="8 hours ago" 2>/dev/null)
MODIFIED_FILES=$(git diff --name-only 2>/dev/null)

ARCHIVED_STATE=0
if [ -f "$STATE_FILE" ]; then
    {
        echo "## Session End: $TIMESTAMP"
        echo "### Archived Session State"
        cat "$STATE_FILE"
        echo "---"
        echo ""
    } >> "$SESSION_LOG_DIR/session-log.md" 2>/dev/null
    rm "$STATE_FILE" 2>/dev/null
    ARCHIVED_STATE=1
fi

if [ -n "$RECENT_COMMITS" ] || [ -n "$MODIFIED_FILES" ]; then
    {
        echo "## Session Summary: $TIMESTAMP"
        if [ -n "$RECENT_COMMITS" ]; then
            echo "### Commits"
            echo "$RECENT_COMMITS"
        fi
        if [ -n "$MODIFIED_FILES" ]; then
            echo "### Uncommitted Changes"
            echo "$MODIFIED_FILES"
        fi
        echo "---"
        echo ""
    } >> "$SESSION_LOG_DIR/session-log.md" 2>/dev/null
fi

echo "Session log updated: $SESSION_LOG_DIR/session-log.md"
if [ "$ARCHIVED_STATE" -eq 1 ]; then
    echo "Archived and removed: $STATE_FILE"
else
    echo "No active session state file was present."
fi

if [ -n "$MODIFIED_FILES" ]; then
    echo "Uncommitted files still present:"
    echo "$MODIFIED_FILES"
fi
