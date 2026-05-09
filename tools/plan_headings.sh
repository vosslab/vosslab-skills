#!/usr/bin/env bash

for plan in ~/.claude/plans/*.md; do
  if grep -qi 'Design philosophy' "$plan"; then
    echo "======"
    echo "$plan"
    echo "======"
    grep -E '^#' "$plan"
    echo
  fi
done
