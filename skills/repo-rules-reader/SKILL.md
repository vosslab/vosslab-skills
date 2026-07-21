---
name: repo-rules-reader
description: Load required repo rules before coding, reviewing, or delegating. Reads `AGENTS.md`, `docs/*_STYLE.md`, Claude hook guidance, and the latest changelog entry; use for rule orientation or targeted questions.
---

# Read repo rules

## Purpose

Load the repository's current instructions into working context for subsequent work.

## Workflow

1. Read these required paths:
   - `AGENTS.md`
   - `docs/*_STYLE.md`
   - `docs/CLAUDE_HOOK_USAGE_GUIDE.md`
   - the latest dated entry in `docs/CHANGELOG.md`
2. Retain and apply the rules throughout subsequent work.
3. Give a concise read receipt:
   - Name the files read.
   - From `AGENTS.md`, include `source source_me.sh && python3` when specified.
   - From `docs/PYTEST_STYLE.md`, state what is considered a fragile pytest.
   - From `docs/CLAUDE_HOOK_USAGE_GUIDE.md`, state how Claude should search or grep files.
   - From `docs/CHANGELOG.md`, state the most recent change.
4. Answer any exact questions or requested format from the file content.
5. Continue the task with the rules applied, or be ready for a task to be provided.
