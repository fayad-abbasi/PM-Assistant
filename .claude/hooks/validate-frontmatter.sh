#!/usr/bin/env bash
# chmod +x .claude/hooks/validate-frontmatter.sh
#
# Validates YAML frontmatter on data/ Markdown files.
# Receives file path as $1. Exits 0 on success, 1 on failure.
set -euo pipefail

FILE="$1"
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TAGS_FILE="$PROJECT_ROOT/data/meta/tags.json"

# --- Gate: only validate files under data/ ---
case "$FILE" in
  "$PROJECT_ROOT"/data/*) ;;
  data/*) FILE="$PROJECT_ROOT/$FILE" ;;
  *) exit 0 ;;
esac

# Resolve to absolute path if relative
[[ "$FILE" = /* ]] || FILE="$PROJECT_ROOT/$FILE"

RELPATH="${FILE#"$PROJECT_ROOT"/}"

# Skip .gitkeep files
[[ "$(basename "$FILE")" == ".gitkeep" ]] && exit 0

# Skip JSON files (they have their own structure)
[[ "$FILE" == *.json ]] && exit 0

# Skip files in data/meta/
case "$RELPATH" in
  data/meta/*) exit 0 ;;
esac

# --- Check file exists ---
if [[ ! -f "$FILE" ]]; then
  exit 0
fi

# --- Extract frontmatter ---
# Frontmatter is between the first two lines that are exactly "---"
FRONTMATTER=$(awk '
  /^---$/ { count++; next }
  count == 1 { print }
  count >= 2 { exit }
' "$FILE")

if [[ -z "$FRONTMATTER" ]]; then
  echo "ERROR [$RELPATH]: No YAML frontmatter found (expected --- delimiters)." >&2
  exit 1
fi

# --- Helper: get a field value from frontmatter ---
get_field() {
  local field="$1"
  echo "$FRONTMATTER" | grep "^${field}:" | head -1 | sed "s/^${field}:[[:space:]]*//"
}

# --- Check required fields: id, title, created_at ---
for req_field in id title created_at; do
  val=$(get_field "$req_field")
  if [[ -z "$val" ]]; then
    echo "ERROR [$RELPATH]: Missing required frontmatter field '$req_field'." >&2
    exit 1
  fi
done

# --- Determine artifact type from path ---
get_artifact_type() {
  case "$RELPATH" in
    data/interviews/*)           echo "interviews" ;;
    data/insights/*)             echo "insights" ;;
    data/prds/*)                 echo "prds" ;;
    data/gtm/drafts/*)           echo "gtm-drafts" ;;
    data/uat/test-cases/*)       echo "uat-test-cases" ;;
    data/strategy/okrs/*)        echo "okrs" ;;
    data/strategy/roadmap/*)     echo "roadmap" ;;
    data/retros/*)               echo "retros" ;;
    data/stakeholder/decisions/*) echo "decisions" ;;
    data/stakeholder/reports/*)  echo "reports" ;;
    data/stakeholder/meetings/*) echo "meetings" ;;
    data/outcomes/records/*)     echo "outcomes" ;;
    data/ux/journeys/*)          echo "journeys" ;;
    *)                           echo "unknown" ;;
  esac
}

ARTIFACT_TYPE=$(get_artifact_type)

# --- Validate status enum if present ---
STATUS=$(get_field "status")
if [[ -n "$STATUS" ]]; then
  VALID=""
  case "$ARTIFACT_TYPE" in
    interviews)
      VALID="raw analyzed"
      ;;
    insights)
      VALID="active superseded archived"
      ;;
    prds)
      VALID="draft review approved deprecated"
      ;;
    gtm-drafts)
      VALID="draft approved"
      ;;
    uat-test-cases)
      # Markdown test cases shouldn't exist (they're JSON), but skip validation
      VALID=""
      ;;
    # These types have no status enum to validate
    retros|decisions|reports|meetings|outcomes|journeys|okrs|roadmap|unknown)
      VALID=""
      ;;
  esac

  if [[ -n "$VALID" ]]; then
    FOUND=0
    for v in $VALID; do
      if [[ "$STATUS" == "$v" ]]; then
        FOUND=1
        break
      fi
    done
    if [[ $FOUND -eq 0 ]]; then
      echo "ERROR [$RELPATH]: Invalid status '$STATUS' for $ARTIFACT_TYPE. Valid values: $VALID" >&2
      exit 1
    fi
  fi
fi

# --- Validate tags against tags.json ---
# Extract tags array lines from frontmatter (handles YAML list format)
# Tags can appear as:
#   tags: [tag1, tag2]
#   tags:
#     - tag1
#     - tag2

TAGS_BLOCK=""

# Check for inline array format: tags: [tag1, tag2]
INLINE_TAGS=$(echo "$FRONTMATTER" | grep "^tags:" | head -1 | sed 's/^tags:[[:space:]]*//')
if echo "$INLINE_TAGS" | grep -q '^\['; then
  # Inline array: strip brackets, split by comma
  TAGS_BLOCK=$(echo "$INLINE_TAGS" | sed 's/^\[//; s/\]$//; s/,/\n/g' | sed 's/^[[:space:]]*//; s/[[:space:]]*$//' | sed 's/^"//; s/"$//' | sed "s/^'//; s/'$//")
else
  # Multi-line array: collect "  - tag" lines after "tags:"
  TAGS_BLOCK=$(echo "$FRONTMATTER" | awk '
    /^tags:/ { intags=1; next }
    intags && /^[[:space:]]*-/ {
      sub(/^[[:space:]]*-[[:space:]]*/, "")
      # Strip quotes
      gsub(/^["'"'"']|["'"'"']$/, "")
      print
      next
    }
    intags && /^[a-zA-Z]/ { exit }
  ')
fi

if [[ -n "$TAGS_BLOCK" && -f "$TAGS_FILE" ]]; then
  # Build a flat list of all valid tags from tags.json
  ALL_VALID_TAGS=$(grep '"[a-z]' "$TAGS_FILE" | sed 's/.*"\([^"]*\)".*/\1/')

  while IFS= read -r tag; do
    # Skip empty lines
    [[ -z "$tag" ]] && continue
    # Strip any remaining whitespace
    tag=$(echo "$tag" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
    [[ -z "$tag" ]] && continue

    # Check if tag exists in valid tags
    if ! echo "$ALL_VALID_TAGS" | grep -qx "$tag"; then
      echo "ERROR [$RELPATH]: Tag '$tag' not found in data/meta/tags.json. Add it there first." >&2
      exit 1
    fi
  done <<< "$TAGS_BLOCK"
fi

# All checks passed
exit 0
