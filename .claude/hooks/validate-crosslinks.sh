#!/usr/bin/env bash
# chmod +x .claude/hooks/validate-crosslinks.sh
#
# Validates cross-references in data/ files.
# Receives file path as $1. Exits 0 on success, 1 on broken link.
set -uo pipefail

FILE="$1"
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

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

# Skip files in data/meta/
case "$RELPATH" in
  data/meta/*) exit 0 ;;
esac

# --- Check file exists ---
if [[ ! -f "$FILE" ]]; then
  exit 0
fi

ERRORS=0

# --- Helper: check if an ID exists in any file in a directory ---
# Usage: check_id_in_dir <id> <directory> <file_extension>
check_id_in_dir() {
  local target_id="$1"
  local search_dir="$PROJECT_ROOT/$2"
  local ext="$3"

  if [[ ! -d "$search_dir" ]]; then
    return 1
  fi

  # Search for the id field in all files in the directory
  for f in "$search_dir"/*."$ext"; do
    [[ -f "$f" ]] || continue
    if grep -q "\"id\":[[:space:]]*\"$target_id\"" "$f" 2>/dev/null || \
       grep -q "^id:[[:space:]]*$target_id" "$f" 2>/dev/null || \
       grep -q "\"id\":[[:space:]]*\"$target_id\"" "$f" 2>/dev/null; then
      return 0
    fi
  done
  return 1
}

# --- Helper: extract IDs from a YAML list field in frontmatter ---
# Handles both inline [id1, id2] and multi-line - id formats
extract_ids_from_field() {
  local field_name="$1"
  local content="$2"

  # Check for inline format: field: [id1, id2]
  local inline
  inline=$(echo "$content" | grep "^${field_name}:" | head -1 | sed "s/^${field_name}:[[:space:]]*//" || true)

  if echo "$inline" | grep -q '^\['; then
    # Inline array
    echo "$inline" | sed 's/^\[//; s/\]$//; s/,/\n/g' | \
      sed 's/^[[:space:]]*//; s/[[:space:]]*$//' | \
      sed 's/^"//; s/"$//' | sed "s/^'//; s/'$//"
  else
    # Multi-line format
    echo "$content" | awk -v field="^${field_name}:" '
      $0 ~ field { infield=1; next }
      infield && /^[[:space:]]*-/ {
        sub(/^[[:space:]]*-[[:space:]]*/, "")
        gsub(/^["'"'"']|["'"'"']$/, "")
        print
        next
      }
      infield && /^[a-zA-Z]/ { exit }
    '
  fi
}

# --- Helper: extract a single-value ID field ---
extract_single_id() {
  local field_name="$1"
  local content="$2"
  echo "$content" | grep "^${field_name}:" | head -1 | sed "s/^${field_name}:[[:space:]]*//" | \
    sed 's/^"//; s/"$//' | sed "s/^'//; s/'$//"
}

# --- Extract content for parsing ---
if [[ "$FILE" == *.json ]]; then
  CONTENT=$(cat "$FILE")
  IS_JSON=1
else
  # Extract YAML frontmatter
  CONTENT=$(awk '
    /^---$/ { count++; next }
    count == 1 { print }
    count >= 2 { exit }
  ' "$FILE")
  IS_JSON=0
fi

if [[ -z "$CONTENT" ]]; then
  exit 0
fi

# --- Define link field -> target directory mappings ---
# Format: field_name|target_directory|file_extension

LINK_DEFS=(
  "linked_interviews|data/interviews|md"
  "linked_insights|data/insights|md"
  "linked_prds|data/prds|md"
  "linked_outcomes|data/outcomes/records|json"
  "okr_ids|data/strategy/okrs|json"
  "roadmap_ids|data/strategy/roadmap|json"
)

SINGLE_LINK_DEFS=(
  "prd_id|data/prds|md"
)

# --- Process array link fields ---
for def in "${LINK_DEFS[@]}"; do
  IFS='|' read -r field_name target_dir target_ext <<< "$def"

  IDS=""
  if [[ "$IS_JSON" -eq 1 ]]; then
    # For JSON: extract array values for the field
    # Handles "field": ["id1", "id2"] format
    IDS=$(grep -o "\"${field_name}\"[[:space:]]*:[[:space:]]*\[.*\]" "$FILE" 2>/dev/null | \
      sed "s/\"${field_name}\"[[:space:]]*:[[:space:]]*\[//; s/\]//" | \
      sed 's/,/\n/g' | sed 's/^[[:space:]]*"//; s/"[[:space:]]*$//' | \
      grep -v '^$' || true)
  else
    IDS=$(extract_ids_from_field "$field_name" "$CONTENT")
  fi

  # Check each ID
  while IFS= read -r id; do
    [[ -z "$id" ]] && continue
    id=$(echo "$id" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
    [[ -z "$id" ]] && continue

    if ! check_id_in_dir "$id" "$target_dir" "$target_ext"; then
      echo "ERROR [$RELPATH]: Broken link in '$field_name': ID '$id' not found in $target_dir/" >&2
      ERRORS=$((ERRORS + 1))
    fi
  done <<< "$IDS"
done

# --- Process single-value link fields ---
for def in "${SINGLE_LINK_DEFS[@]}"; do
  IFS='|' read -r field_name target_dir target_ext <<< "$def"

  ID=""
  if [[ "$IS_JSON" -eq 1 ]]; then
    ID=$(grep -o "\"${field_name}\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" "$FILE" 2>/dev/null | \
      sed "s/\"${field_name}\"[[:space:]]*:[[:space:]]*\"//" | sed 's/"$//' || true)
  else
    ID=$(extract_single_id "$field_name" "$CONTENT")
  fi

  ID=$(echo "$ID" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
  [[ -z "$ID" ]] && continue

  if ! check_id_in_dir "$ID" "$target_dir" "$target_ext"; then
    echo "ERROR [$RELPATH]: Broken link in '$field_name': ID '$ID' not found in $target_dir/" >&2
    ERRORS=$((ERRORS + 1))
  fi
done

# --- Exit ---
if [[ $ERRORS -gt 0 ]]; then
  exit 1
fi

exit 0
