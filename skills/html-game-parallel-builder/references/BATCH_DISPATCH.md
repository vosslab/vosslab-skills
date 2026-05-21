# Batched agent dispatch

Detail companion to [`../SKILL.md`](../SKILL.md). The control plane
names the four batches and their critical guardrails; this file carries
the per-batch tables, the per-agent prompt requirements, and the
wall-clock comparison.

Manager dispatch is governed by `delegate-manager-to-subagents`. Lane
count and scope splits across batches are decided once in
`parallel-plan` before Batch 1; revisit if any batch becomes lopsided.
The per-batch tables below define each agent's owned files and the
type contracts each agent must import; the manager applies the
delegation contract on top.

After Workstream A0 (Types and contracts) finishes, dispatch the four
batches below.

The contracts named in this file (per-agent gate, batch gate, agent
return fields, type-delegation pause-and-wait) exist because this
skill ships a game inside a live podcast window. They are not
bureaucratic overhead; they are how the deadline gets hit. A 30-second
`tsc --noEmit` line in each subagent report catches contract drift
that would otherwise surface 20 minutes later in a Playwright failure
across multiple modules. A 1-minute pause-and-invoke for a typed stub
prevents three agents from importing three different versions of the
same shape. Cutting any of these to "save time" moves the same time
into integration debt and blows the window.

## Two distinct gates

The skill runs the type check at two different layers; do not conflate
them:

- **Per-agent gate (subagent's responsibility before reporting DONE):**
  `npx tsc --noEmit -p tsconfig.json`. The subagent must run this
  on its own changes and quote the exact success line in its report
  (`exit 0`, no diagnostic output). This is the agent's own evidence.
- **Per-batch gate (manager's responsibility after all agents in the
  batch report DONE):** `./check_codebase.sh` (the canonical
  starter-template gate: typecheck + eslint + prettier --check + node
  --test + playwright + production build). The manager runs this once
  per batch as the integration check. Failure here triggers a
  fix-agent dispatch, not just a re-run.

The agent's `tsc` run inside its own scope is not the integration
gate, and the batch's `check_codebase.sh` run is not the agent's
self-report substitute. Keep both.

## What each agent must return

Every coding subagent's report (manager dispatches one of these per
batch slot) must contain:

- Files changed: absolute path list, each labelled with the batch-slot
  requirement it satisfies.
- Exact command run: literally `npx tsc --noEmit -p tsconfig.json`.
- Exact success line: `exit 0` with no diagnostic output. Quote it.
- Cross-module type imports used: list the `import type` lines from
  `src/types/*.ts` the agent relied on. Confirms the agent did not
  redeclare a contract shape locally.
- Any failure, warning, or skipped check: each with a one-line scope
  assessment (in scope or out of scope) and the evidence (diff line
  or exact command output).

`DONE` without the exact command line and its exact success line is
treated as a false-green claim; the manager re-dispatches with a
context bump.

## Type-design delegation contract

When a coding subagent needs a cross-module type that does not yet
exist in `src/types/`, or hits a type-system question (generic
constraint, conditional shape, save-file boundary, brand constructor):

1. Pause its own implementation work.
2. Invoke `typescript-engineer` with one narrow question (one shared
   type, one brand, one boundary shape; not a full audit).
3. Wait for `typescript-engineer`'s return: a typed stub the agent
   can paste, plus the exact `tsc --noEmit` line and its success
   output.
4. Resume implementation only after the stub is in place.

Do NOT define cross-module shapes locally to keep moving. Time
"saved" by skipping delegation lands as integration debt at the
batch boundary, where the cost is multiplied by every other agent
that already imported the wrong shape. The `typescript-engineer`
return contract is documented in that skill's `## Delegated
execution` section.

## Batch 1: Foundation (sequential, ~2 min)

Write in the orchestrator or a single agent:

- `src/constants.ts` -- game config, level/room data
- `src/characters.ts` -- entity definitions
- `src/game_state.ts` -- state machine, stage transitions

These define the data model everything else depends on. They MUST
import their cross-module shapes from `src/types/`.

Batch integration gate (manager runs after Batch 1 DONE):
`./check_codebase.sh` passes; build with `./build_github_pages.sh`;
open in browser; verify no JS errors.

## Batch 2: Infrastructure (parallel, ~4 min)

| Agent | Files | Imports types from |
| --- | --- | --- |
| Styling | `src/style.css`, `src/head.html`, `src/body.html`, `src/tail.html`, `src/index.html` | (HTML/CSS only) |
| Timer + utilities | `src/timer.ts`, `src/save_load.ts` | `src/types/save.ts` |
| UI rendering | `src/ui_rendering.ts` | `src/types/events.ts` |

Each agent prompt MUST include:

- The full type-contract file list (`src/types/*.ts`).
- The constants/state foundation (or key excerpts).
- Their owned files (no other files).
- Explicit constraint: "Do NOT modify files outside your assignment."

Batch integration gate (manager runs after all Batch 2 agents DONE):
`./check_codebase.sh` passes; Playwright smoke per
[`../templates/playwright_smoke_test.md`](../templates/playwright_smoke_test.md).

## Batch 3: Core game stages (parallel, ~5 min)

| Agent | Files | Imports types from |
| --- | --- | --- |
| Scene stage | `src/scene_stage.ts` | `src/types/events.ts`, feature-local types |
| Data generation | `src/data_generation.ts` | feature-local return types |

Batch integration gate (manager runs after all Batch 3 agents DONE):
`./check_codebase.sh` passes; Playwright smoke verifies the core
loop end-to-end.

## Batch 4: Advanced features (parallel, ~5 min)

| Agent | Files | Imports types from |
| --- | --- | --- |
| Lab + gel | `src/lab_stage.ts`, `src/gel_rendering.ts` | feature-local types, `src/types/events.ts` |
| Case board + scoring + educational | `src/case_board.ts`, `src/scoring.ts`, `src/educational.ts` | `src/types/save.ts`, feature-local types |

Batch integration gate (manager runs after all Batch 4 agents DONE):
`./check_codebase.sh` passes; full playthrough via Playwright.

## Total wall-clock: ~20 min with 4 integration checkpoints

Compare: all-at-once parallel (8 min authoring + 60 min debugging =
68 min). The sequential gates exist to keep the code good under
parallel authoring; parallelism is how those same gates still fit
inside a live window.
