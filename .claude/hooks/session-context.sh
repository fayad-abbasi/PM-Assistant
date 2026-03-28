#!/usr/bin/env bash
# Session-start context injection hook
# Surfaces key context so Claude never starts cold:
# - Active OKR status
# - PRD priorities
# - Stale/blocked items
# - Recent decisions
# - Accumulated learnings/mistakes

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DATA="$ROOT/data"

echo "=== PM ASSISTANT SESSION CONTEXT ==="
echo ""

# Learnings (always inject — this is the compound knowledge)
LEARNINGS="$DATA/meta/learnings.md"
if [ -f "$LEARNINGS" ] && [ -s "$LEARNINGS" ]; then
    echo "--- LEARNINGS & CORRECTIONS ---"
    cat "$LEARNINGS"
    echo ""
fi

# Active OKRs summary
OKR_DIR="$DATA/strategy/okrs"
if [ -d "$OKR_DIR" ]; then
    OKR_FILES=$(find "$OKR_DIR" -name "*.json" ! -name ".gitkeep" 2>/dev/null || true)
    if [ -n "$OKR_FILES" ]; then
        OKR_COUNT=$(echo "$OKR_FILES" | wc -l | tr -d ' ')
        echo "--- ACTIVE OKRs ($OKR_COUNT) ---"
        echo "$OKR_FILES" | while IFS= read -r f; do
            if [ -f "$f" ]; then
                # Extract top-level JSON fields (2-space indent = top level)
                objective=$(grep '^  "objective"' "$f" 2>/dev/null | head -1 | sed 's/.*"objective"[[:space:]]*:[[:space:]]*"//;s/".*//' || echo "?")
                status=$(grep '^  "status"' "$f" 2>/dev/null | head -1 | sed 's/.*"status"[[:space:]]*:[[:space:]]*"//;s/".*//' || echo "?")
                okr_id=$(grep '^  "id"' "$f" 2>/dev/null | head -1 | sed 's/.*"id"[[:space:]]*:[[:space:]]*"//;s/".*//' || echo "?")
                if [ "$status" = "active" ]; then
                    echo "  $okr_id: $objective [$status]"
                fi
            fi
        done
        echo ""
    fi
fi

# PRD status summary
PRD_DIR="$DATA/prds"
if [ -d "$PRD_DIR" ]; then
    PRD_FILES=$(find "$PRD_DIR" -name "*.md" ! -name ".gitkeep" 2>/dev/null || true)
    if [ -n "$PRD_FILES" ]; then
        PRD_COUNT=$(echo "$PRD_FILES" | wc -l | tr -d ' ')
        echo "--- PRDs ($PRD_COUNT) ---"
        echo "$PRD_FILES" | while IFS= read -r f; do
            if [ -f "$f" ]; then
                # Extract frontmatter fields with awk
                awk '/^---$/{n++; next} n==1 && /^(id|title|status|priority):/{print "  " $0}' "$f" 2>/dev/null || true
                echo ""
            fi
        done
    fi
fi

# Recent decisions (last 5)
DECISIONS_DIR="$DATA/stakeholder/decisions"
if [ -d "$DECISIONS_DIR" ]; then
    DECISION_FILES=$(find "$DECISIONS_DIR" -name "*.md" ! -name ".gitkeep" 2>/dev/null | sort -r | head -5 || true)
    if [ -n "$DECISION_FILES" ]; then
        echo "--- RECENT DECISIONS ---"
        echo "$DECISION_FILES" | while IFS= read -r f; do
            if [ -f "$f" ]; then
                awk '/^---$/{n++; next} n==1 && /^(id|title|decision):/{print "  " $0}' "$f" 2>/dev/null || true
                echo ""
            fi
        done
    fi
fi

# Open action items from meetings (flag overdue by deadline)
MEETINGS_DIR="$DATA/stakeholder/meetings"
if [ -d "$MEETINGS_DIR" ]; then
    MEETING_FILES=$(find "$MEETINGS_DIR" -name "*.md" ! -name ".gitkeep" 2>/dev/null || true)
    if [ -n "$MEETING_FILES" ]; then
        echo "--- OPEN ACTION ITEMS ---"
        echo "$MEETING_FILES" | while IFS= read -r f; do
            if [ -f "$f" ]; then
                # Extract action items from YAML frontmatter using awk
                # Look for assignee/task/deadline patterns in the frontmatter
                awk '
                BEGIN { in_fm=0; in_actions=0 }
                /^---$/ { in_fm++; next }
                in_fm == 1 {
                    if (/^action_items:/) { in_actions=1; next }
                    if (in_actions && /^[a-z]/) { in_actions=0 }
                    if (in_actions && /assignee:/) {
                        gsub(/.*assignee: *"?/, ""); gsub(/".*/, "")
                        assignee=$0
                    }
                    if (in_actions && /task:/) {
                        gsub(/.*task: *"?/, ""); gsub(/".*/, "")
                        task=$0
                    }
                    if (in_actions && /deadline:/) {
                        gsub(/.*deadline: *"?/, ""); gsub(/".*/, "")
                        deadline=$0
                        if (assignee != "" && task != "") {
                            print "  - " assignee ": " task " (due: " deadline ")"
                        }
                        assignee=""; task=""; deadline=""
                    }
                }
                in_fm >= 2 { exit }
                ' "$f" 2>/dev/null || true
            fi
        done
        echo ""
    fi
fi

# Upcoming people context (from person pages)
PEOPLE_DIR="$DATA/stakeholder/people"
if [ -d "$PEOPLE_DIR" ]; then
    PEOPLE_COUNT=$(find "$PEOPLE_DIR" -name "*.md" ! -name ".gitkeep" 2>/dev/null | wc -l | tr -d ' ' || echo "0")
    if [ "$PEOPLE_COUNT" -gt 0 ]; then
        echo "--- STAKEHOLDER PROFILES ($PEOPLE_COUNT tracked) ---"
        find "$PEOPLE_DIR" -name "*.md" ! -name ".gitkeep" 2>/dev/null | while IFS= read -r f; do
            if [ -f "$f" ]; then
                name=$(awk '/^---$/{n++; next} n==1 && /^name:/{gsub(/.*name: *"?/,""); gsub(/"$/,""); print}' "$f" 2>/dev/null || true)
                role=$(awk '/^---$/{n++; next} n==1 && /^role:/{gsub(/.*role: *"?/,""); gsub(/"$/,""); print}' "$f" 2>/dev/null || true)
                if [ -n "$name" ]; then
                    echo "  - $name ($role)"
                fi
            fi
        done
        echo ""
    fi
fi

echo "=== END SESSION CONTEXT ==="
