---
name: repo-rules-reader
description: Read specified repo rule files (AGENTS.md, docs/REPO_STYLE.md, docs/PYTHON_STYLE.md,
  docs/PYTEST_STYLE.md, docs/CLAUDE_HOOK_USAGE_GUIDE.md, docs/CHANGELOG.md) and answer
  targeted repo-rule questions, with missing-file handling and explicit-path checks. For
  docs/CHANGELOG.md, report only the latest dated entry. Use when a prompt asks for repo
  instruction answers about code execution, pytest style, Claude hook usage, or recent changes.
mode: reviewer
execution: direct
---

# Read Repo Rules

## Overview
Answer key repo-rule questions with enough context to be useful, while preserving missing-file stop
conditions.

## Workflow
1. Verify each requested file path exists using explicit paths only, such as `ls <paths>` or
   `test -f`. If any requested file is missing, output `MISSING: <path>` and stop.
2. Read only the requested repo rule files. For the default repo-rule output, read:
   AGENTS.md, docs/REPO_STYLE.md, docs/PYTHON_STYLE.md, docs/PYTEST_STYLE.md,
   docs/CLAUDE_HOOK_USAGE_GUIDE.md, and docs/CHANGELOG.md.
3. Read normal rule files with bounded commands such as `sed -n "1,200p"`.
4. For docs/CHANGELOG.md, identify the latest dated entry and read only that entry section, from
   its heading to the line before the next dated heading or the end of file.
5. Answer the prompt's exact questions when provided. When the prompt asks for the default
   repo-rule output, answer these six questions:
   - AGENTS.md: how should agents run repo-local Python code? Include
     `source source_me.sh && python3` when the file says so.
   - docs/REPO_STYLE.md: what repo-wide workflow or file organization rule matters for the
     current task?
   - docs/PYTHON_STYLE.md: what Python implementation rule matters for the current task?
   - docs/PYTEST_STYLE.md: what is considered a fragile pytest?
   - docs/CLAUDE_HOOK_USAGE_GUIDE.md: how should Claude search or grep files?
   - docs/CHANGELOG.md: what is the most recent change?
6. Ground each answer in the file content. Keep answers concise unless more context is needed to
   avoid ambiguity.
7. Use the prompt's requested order and prefixes when provided, such as `AGENTS: ...`,
   `REPO_STYLE: ...`, `PYTHON_STYLE: ...`, `PYTEST_STYLE: ...`,
   `CLAUDE_HOOK_USAGE_GUIDE: ...`, and `CHANGELOG: ...`.
8. When the prompt requests exact lines, exact prefixes, or no extra text, follow that format
   exactly and do not add commentary.
9. Use explicit requested paths for listings; avoid recursive listings such as `ls -R`.
