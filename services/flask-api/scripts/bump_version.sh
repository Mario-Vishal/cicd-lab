#!/usr/bin/env bash
set -e

# Usage: ./scripts/bump_version.sh [major|minor|patch]
# Default: patch

LEVEL="${1:-patch}"

if [ ! -f VERSION ]; then
  echo "VERSION file not found" >&2
  exit 1
fi

CURRENT="$(cat VERSION)"

IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

case "$LEVEL" in
  major)
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    ;;
  minor)
    MINOR=$((MINOR + 1))
    PATCH=0
    ;;
  patch)
    PATCH=$((PATCH + 1))
    ;;
  *)
    echo "Invalid level: $LEVEL (use major|minor|patch)" >&2
    exit 2
    ;;
esac

NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
echo "$NEW_VERSION" > VERSION
echo "Version bumped: $CURRENT -> $NEW_VERSION"

