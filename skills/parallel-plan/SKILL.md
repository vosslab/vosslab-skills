---
name: parallel-plan
description: Plan and execute large tasks with independent concurrent workstreams and explicit dependency gates. Use when a request has multiple separable tracks, needs parallel subagents/sessions, or is too large for a single linear pass. Skip this skill for tightly coupled single-file edits.
---

# Parallel Plan

## Overview

Decompose large tasks into safe parallel workstreams, dispatch each stream with clear contracts, and synthesize one ordered execution plan before coding. Keep concurrency real, not simulated. Keep orchestrator memory usage bounded by requiring file-backed stream reports and compact stream handoffs.

## Choose Execution Species

- Decide between `orchestration-only` and `real parallel execution`.
- Use `orchestration-only` when environment limits prevent true concurrency. Still split into independent streams and write complete stream briefs.
- Use `real parallel execution` when streams can run at the same time in isolated sessions/worktrees or a single batched multi-task dispatch.

## Tooling and State

- Keep execution tooling non-prescriptive.
- Treat `tmux` as an optional helper, not a requirement.
- Accept any equivalent mechanism that provides true concurrent execution and isolation.
- Default to lightweight text artifacts for task state (stream briefs, stream reports, unified plan).
- Make the orchestrator choose report paths per run; do not hardcode a global fixed path.
- Use collision-safe naming for report paths (for example: run id + stream id + timestamp/random suffix).
- Prefer repo-local temp directories or other orchestrator-selected temp locations when practical.
- Add a task database (`sqlite`/Berkeley DB) only when cross-session resume or external query requirements are explicit.

## Workflow

1. Resolve shared prerequisites first.
- Identify shared contracts (types, interfaces, schemas, migration order).
- Execute shared prerequisites in the orchestrator main context.
- Complete shared prerequisites before parallel dispatch.

2. Define independent workstreams.
- Assign each stream a clear goal, scope boundary, and owned files/directories.
- Merge or re-scope any streams that would modify the same files.

3. Dispatch correctly.
- For real parallel execution, launch streams concurrently in one batch dispatch or separate isolated sessions.
- Do not send stream tasks sequentially if true parallelism is required.

4. Enforce file-backed standardized stream outputs.
- Assign each stream an orchestrator-selected unique report path in the stream brief.
- Require each stream to write its full report only to the provided path.
- Require each stream to return only a compact handoff message with status, report path, validation status, and a short bullet summary.
- Require deep research streams to put full findings in report files and return only the compact handoff in chat.
- Reject stream responses that paste full reports or large logs inline.

5. Synthesize one ordered plan.
- Synthesize only after all stream validations pass; if any validation fails, stop and fix before synthesis.
- Read stream report files from orchestrator-assigned paths and merge them into one execution sequence with checkpoints.
- Add integration risks, dependency notes, and fallback handling.

6. Gate before implementation.
- Confirm no unresolved cross-stream dependencies remain.
- Confirm each checkpoint has explicit verification commands.
- Confirm all expected stream report files exist and are readable before synthesis.

## Independence Rules

- Parallelize only streams that do not depend on each other in-flight outputs.
- Do not parallelize streams that edit the same files or the same mutable state.
- If independence is uncertain, serialize that portion.
- Prefer finishing dependency-establishing work first, then parallelizing the rest.

## Orchestrator Memory Rules

- Do not request full stream reports inline in orchestrator chat.
- Use file-path handoff first; read files on demand during synthesis.
- Default final handoffs to short bullet lists (`3-6` bullets).
- Cap stream handoff size (for example, `<=1 KB` plus report path).
- Keep verbose command output and diagnostics inside report files, not in handoff messages.

## Required Output Contract

Require this structure from each stream handoff message:
1. Status
2. Report file path
3. Summary (`3-6` bullets)
4. Validation status (`pass`/`fail`)
5. Blocking issues (optional)

Require this structure inside each stream report file:
1. Assumptions
2. Decisions
3. Concrete next steps
4. Changed files
5. Validation performed

Then synthesize:
1. Ordered unified plan
2. Checkpoints with pass/fail criteria
3. Integration risks and mitigations

## Templates

Use the reusable templates in `references/parallel_plan_templates.md` for:
- stream brief format
- compact stream handoff format
- stream report file format
- synthesis and checkpoint checklist
- anti-pattern checks for fake parallelism and memory overload
