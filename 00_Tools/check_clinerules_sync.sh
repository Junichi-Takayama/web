#!/bin/sh

set -eu

SOURCE="/Users/apple/Documents/projects/web/.clinerules"
TARGET="/Users/apple/Documents/projects/.clinerules"

if cmp -s "$SOURCE" "$TARGET"; then
  printf '%s\n' "OK: .clinerules files are synchronized."
  exit 0
fi

printf '%s\n' "ERROR: .clinerules files are not synchronized." >&2
printf '%s\n' "Source: $SOURCE" >&2
printf '%s\n' "Target: $TARGET" >&2
exit 1