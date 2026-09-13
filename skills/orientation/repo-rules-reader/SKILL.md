---
name: repo-rules-reader
description: Orient to repository rules for an explicit orientation request, a workflow that requires a rules receipt, or substantial repository work when no valid same-session receipt exists.
---

# Read repo rules

## Purpose

Establish one authoritative rules receipt for the current repository work session.

## Workflow

1. Read these required paths:
   - `AGENTS.md`
   - `docs/*_STYLE.md`
   - the latest dated entry in `docs/CHANGELOG.md`
2. Retain and apply the rules throughout subsequent work. Treat the receipt as valid for the same
   session while the task scope and relevant guidance remain unchanged.
3. Give a concise read receipt:
   - Name the files read.
   - From `AGENTS.md`, include `source source_me.sh && python3` when specified.
   - When pytest work or its policy materially affects the request, state what
     `docs/PYTEST_STYLE.md` considers a fragile pytest.
   - When it materially affects the request's scope or a decision, state the relevant most
     recent change from `docs/CHANGELOG.md`.
4. Answer any exact questions or requested format from the file content.
5. Continue the task with the rules applied, or be ready for a task to be provided. Reuse the
   receipt without rereading when another workflow requests orientation in the same unchanged
   scope; reread when the scope changes or relevant guidance may have changed.

Claude Code also reads `docs/CLAUDE_HOOK_USAGE_GUIDE.md`.
