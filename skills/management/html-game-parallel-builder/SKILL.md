---
name: html-game-parallel-builder
description: Use when the user requests a parallel multi-agent build or major workstream for a modular TypeScript browser game, including integrated serving, smoke testing, export, or Pages delivery.
---

# Web Game Parallel Build

Use for a time-pressured, modular TypeScript browser-game build where multiple
agents must author interacting modules and the live local preview is the
immediate target. It is not for a simple edit, server application, heavyweight
multi-page build, or work where one agent can finish promptly. Parallelism cuts
wall time only when contracts and integration gates remain intact.

## Required routing

Before dispatch, invoke `delegate-manager-to-subagents` for ownership and
evidence discipline, `parallel-plan` for lane sizing and ownership splits, and
`typescript-engineer` for all type design. Read the TypeScript skill's game
type, modular-type, strict-mode, and opaque-type references before defining
cross-module contracts. This skill owns browser-game orchestration, not
TypeScript design rules.

Read [references/BATCH_DISPATCH.md](references/BATCH_DISPATCH.md) before file
assignment. It owns the A0-E layout, batch-specific prompt requirements,
exclusive file ownership, and the type-design pause-and-route procedure. Use
[templates/agent_prompt_template.md](templates/agent_prompt_template.md) for
every coding assignment.

## Build and release identity

Default to a GitHub Pages-ready build in `dist/`. Use a portable single-file
export in `dist-single/` only when explicitly requested. Keep the three paths
separate: `run_web_server.sh` serves the live preview,
`build_github_pages.sh` produces the Pages build, and
`export_single_file.sh` produces the optional portable artifact. Read
[references/BUILD_ARTIFACTS.md](references/BUILD_ARTIFACTS.md) for ownership,
starter-template parity, copied artifacts, and output constraints. Read
[references/GITHUB_PAGES_DEPLOY.md](references/GITHUB_PAGES_DEPLOY.md) only
when configuring or diagnosing deployment.

## Control loop

1. Capture UI preferences, define a minimal core loop, and write real shared
   contracts in `src/types/` before any coding agent starts.
2. Configure the supported scaffold and establish a clean
   `npx tsc --noEmit -p tsconfig.json` gate.
3. Run Batch 1 sequentially, then Batches 2-4 in the ownership order from
   [references/BATCH_DISPATCH.md](references/BATCH_DISPATCH.md).
4. After every batch, run the type-check and Playwright smoke described in
   [references/SMOKE_AND_GOTCHAS.md](references/SMOKE_AND_GOTCHAS.md). A
   failing check stops progression: repair the responsible module or contract,
   then rebuild and re-test.
5. After the final batch, run the full playthrough and use the small-scope fix
   loop in [references/STEP_DETAILS.md](references/STEP_DETAILS.md) until
   clean.

## Load-bearing safeguards

- Never dispatch coding agents before contracts exist.
- Never declare a batch green without the exact successful `tsc --noEmit`
  evidence and its required smoke result.
- Never skip a between-batch smoke or proceed past its failure.
- Never locally redeclare a cross-module shape; route it to the contract owner
  and `typescript-engineer`.
- Keep coding ownership exclusive. The manager writes no game code except the
  documented Batch 1 foundation boundary.
- Do not blend build identities, weaken type safety with casts, or replace
  browser evidence with a claim that the game is green.

Read [references/QUALITY_GUARDRAILS.md](references/QUALITY_GUARDRAILS.md) for
the complete red flags and rationale; read
[references/SMOKE_AND_GOTCHAS.md](references/SMOKE_AND_GOTCHAS.md) when web
platform behavior fails. Use [references/STEP_DETAILS.md](references/STEP_DETAILS.md)
for conditional setup, scope, and repair detail. Definitions, naming, capacity,
and visual style route respectively through
[references/DEFINITIONS.md](references/DEFINITIONS.md),
[references/NAMING_GUARDRAILS.md](references/NAMING_GUARDRAILS.md),
[references/CAPACITY_AND_SIZING.md](references/CAPACITY_AND_SIZING.md), and the
applicable design-style references.
