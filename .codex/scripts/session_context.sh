#!/bin/bash

set +e

echo "=== Game Studios Codex Context ==="

BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ -n "$BRANCH" ]; then
    echo "Branch: $BRANCH"
    echo ""
    echo "Recent commits:"
    git log --oneline -5 2>/dev/null | while read -r line; do
        echo "  $line"
    done
fi

LATEST_SPRINT=$(ls -t production/sprints/sprint-*.md 2>/dev/null | head -1)
if [ -n "$LATEST_SPRINT" ]; then
    echo ""
    echo "Active sprint: $(basename "$LATEST_SPRINT" .md)"
fi

LATEST_MILESTONE=$(ls -t production/milestones/*.md 2>/dev/null | head -1)
if [ -n "$LATEST_MILESTONE" ]; then
    echo "Active milestone: $(basename "$LATEST_MILESTONE" .md)"
fi

BUG_COUNT=0
for dir in tests/playtest production; do
    if [ -d "$dir" ]; then
        count=$(find "$dir" -name "BUG-*.md" 2>/dev/null | wc -l)
        BUG_COUNT=$((BUG_COUNT + count))
    fi
done
if [ "$BUG_COUNT" -gt 0 ]; then
    echo "Open bugs: $BUG_COUNT"
fi

if [ -d "src" ]; then
    TODO_COUNT=$(grep -r "TODO" src/ 2>/dev/null | wc -l)
    FIXME_COUNT=$(grep -r "FIXME" src/ 2>/dev/null | wc -l)
    if [ "$TODO_COUNT" -gt 0 ] || [ "$FIXME_COUNT" -gt 0 ]; then
        echo ""
        echo "Code health: ${TODO_COUNT} TODOs, ${FIXME_COUNT} FIXMEs in src/"
    fi
fi

STATE_FILE="production/session-state/active.md"
if [ -f "$STATE_FILE" ]; then
    echo ""
    echo "=== ACTIVE SESSION STATE ==="
    echo "Resume from: $STATE_FILE"
    head -20 "$STATE_FILE" 2>/dev/null
    TOTAL_LINES=$(wc -l < "$STATE_FILE" 2>/dev/null)
    if [ "$TOTAL_LINES" -gt 20 ]; then
        echo "  ... ($TOTAL_LINES total lines)"
    fi
fi

echo ""
echo "=== Documentation Gaps ==="

FRESH_PROJECT=true
if [ -f ".claude/docs/technical-preferences.md" ]; then
    ENGINE_LINE=$(grep -E "^\- \*\*Engine\*\*:" .claude/docs/technical-preferences.md 2>/dev/null)
    if [ -n "$ENGINE_LINE" ] && ! echo "$ENGINE_LINE" | grep -q "TO BE CONFIGURED" 2>/dev/null; then
        FRESH_PROJECT=false
    fi
fi

if [ -f "design/gdd/game-concept.md" ]; then
    FRESH_PROJECT=false
fi

if [ -d "src" ]; then
    SRC_CHECK=$(find src -type f \( -name "*.gd" -o -name "*.cs" -o -name "*.cpp" -o -name "*.c" -o -name "*.h" -o -name "*.hpp" -o -name "*.rs" -o -name "*.py" -o -name "*.js" -o -name "*.ts" \) 2>/dev/null | head -1)
    if [ -n "$SRC_CHECK" ]; then
        FRESH_PROJECT=false
    fi
fi

if [ "$FRESH_PROJECT" = true ]; then
    echo "Fresh project detected. Suggested next step: \$start"
    echo "For a full analysis, run: \$project-stage-detect"
    echo "==================================="
    exit 0
fi

if [ -d "src" ]; then
    SRC_FILES=$(find src -type f \( -name "*.gd" -o -name "*.cs" -o -name "*.cpp" -o -name "*.c" -o -name "*.h" -o -name "*.hpp" -o -name "*.rs" -o -name "*.py" -o -name "*.js" -o -name "*.ts" \) 2>/dev/null | wc -l)
else
    SRC_FILES=0
fi

if [ -d "design/gdd" ]; then
    DESIGN_FILES=$(find design/gdd -type f -name "*.md" 2>/dev/null | wc -l)
else
    DESIGN_FILES=0
fi

SRC_FILES=$(echo "$SRC_FILES" | tr -d ' ')
DESIGN_FILES=$(echo "$DESIGN_FILES" | tr -d ' ')

if [ "$SRC_FILES" -gt 50 ] && [ "$DESIGN_FILES" -lt 5 ]; then
    echo "Gap: substantial codebase ($SRC_FILES files) but sparse design docs ($DESIGN_FILES files)"
    echo "Suggested next step: \$reverse-document design src/[system]"
fi

if [ -d "prototypes" ]; then
    PROTOTYPE_DIRS=$(find prototypes -mindepth 1 -maxdepth 1 -type d 2>/dev/null)
    if [ -n "$PROTOTYPE_DIRS" ]; then
        while IFS= read -r proto_dir; do
            if [ ! -f "${proto_dir}/README.md" ] && [ ! -f "${proto_dir}/CONCEPT.md" ]; then
                echo "Gap: undocumented prototype at ${proto_dir}/"
                echo "Suggested next step: \$reverse-document concept ${proto_dir}"
            fi
        done <<< "$PROTOTYPE_DIRS"
    fi
fi

if [ -d "src/core" ] || [ -d "src/engine" ]; then
    if [ ! -d "docs/architecture" ]; then
        echo "Gap: core systems exist but docs/architecture/ is missing"
        echo "Suggested next step: \$architecture-decision"
    fi
fi

if [ "$SRC_FILES" -gt 100 ] && [ ! -d "production/sprints" ] && [ ! -d "production/milestones" ]; then
    echo "Gap: large codebase ($SRC_FILES files) but no production planning found"
    echo "Suggested next step: \$sprint-plan"
fi

echo ""
echo "For a full analysis, run: \$project-stage-detect"
echo "==================================="
