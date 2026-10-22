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

Before contracts or dispatch, invoke `game-design-expert` to establish the
shared design brief: intended experience, core actions and decisions, surprise
and progression, visual identity and visible consequence, cross-module
dependencies, and evidence. Keep that concise brief in the project's existing
planning documentation. It is the creative source for contracts, assignments,
and integrated review.

Also invoke `delegate-manager-to-subagents` for ownership and evidence
discipline, `parallel-plan` for lane sizing and ownership splits, and
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
export in `output_single_file/` only when explicitly requested. Keep the three paths
separate: `run_web_server.sh` serves the live preview,
`build_github_pages.sh` produces the Pages build, and
`export_single_file.sh` produces the optional portable artifact. Read
[references/BUILD_ARTIFACTS.md](references/BUILD_ARTIFACTS.md) for ownership,
starter-template parity, copied artifacts, and output constraints. Read
[references/GITHUB_PAGES_DEPLOY.md](references/GITHUB_PAGES_DEPLOY.md) only
when configuring or diagnosing deployment.

## Control loop

1. Establish the shared design brief without waiting for human input, define a
   first playable slice, and write real shared contracts in `src/types/` before
   any coding agent starts. The slice orders work; it does not reduce the
   requested game to a smaller final outcome.
2. Configure the supported scaffold and establish a clean
   `npx tsc --noEmit -p tsconfig.json` gate.
3. Run Batch 1 sequentially, then Batches 2-4 in the ownership order from
   [references/BATCH_DISPATCH.md](references/BATCH_DISPATCH.md).
4. After every batch, run the type-check and Playwright smoke described in
   [references/SMOKE_AND_GOTCHAS.md](references/SMOKE_AND_GOTCHAS.md). A
   failing check stops progression: repair the responsible module or contract,
   then rebuild and re-test.
5. After the final batch, run the full playthrough and use the proportional
   integrated-review and fix loop in
   [references/STEP_DETAILS.md](references/STEP_DETAILS.md) until clean.

## Load-bearing safeguards

- Never dispatch coding agents before contracts exist.
- Never define contracts or assignments before the shared design brief exists.
- Never declare a batch green without the exact successful `tsc --noEmit`
  evidence and its required smoke result.
- Never skip a between-batch smoke or proceed past its failure.
- Never locally redeclare a cross-module shape; route it to the contract owner
  and `typescript-engineer`.
- Keep coding ownership exclusive. The manager writes no game code except the
  documented Batch 1 foundation boundary.
- Keep every milestone, prerequisite, assessment, correction, and final
  acceptance executable by the manager and subagents without waiting for a
  human. Scale independent assessment to the change's importance and
  uncertainty; do not add routine artwork bake-offs or extra reviewers for
  small, settled fixes.
- Do not blend build identities, weaken type safety with casts, or replace
  browser evidence with a claim that the game is green.

Read [references/QUALITY_GUARDRAILS.md](references/QUALITY_GUARDRAILS.md) for
the complete red flags and rationale; read
[references/SMOKE_AND_GOTCHAS.md](references/SMOKE_AND_GOTCHAS.md) when web
platform behavior fails. Use [references/STEP_DETAILS.md](references/STEP_DETAILS.md)
for conditional setup, scope, and repair detail. Definitions, naming, and capacity
route respectively through
[references/DEFINITIONS.md](references/DEFINITIONS.md),
[references/NAMING_GUARDRAILS.md](references/NAMING_GUARDRAILS.md),
[references/CAPACITY_AND_SIZING.md](references/CAPACITY_AND_SIZING.md).

Read the target repository's `docs/FUN_VIBES_DESIGN_STYLE.md` and
`docs/PLAYFUL_TRAINING_GAME_STYLE.md` when present. Their canonical sources
live in `starter-repo-template/templates/typescript/docs/`; this skill bundles
neither guide. When absent, use `game-design-expert` and the shared brief.
