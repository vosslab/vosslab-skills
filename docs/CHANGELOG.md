## 2026-02-21

- Renamed terminology and metadata in `skills/orchestrate-next-milestone/SKILL.md` from legacy phase language to milestone/workstream/work package/patch language aligned with `skills/manager-make-new-plan`.
- Updated `skills/orchestrate-next-milestone/agents/openai.yaml` interface labels and default prompt to use the renamed `$orchestrate-next-milestone` skill and milestone-first wording.
- Expanded and standardized `skills/manager-make-new-plan/SKILL.md` with milestone-first planning language, explicit terminology-collision rules, dependency-by-ID requirements, and links to canonical references.
- Expanded `skills/manager-make-new-plan/references/plan_quality_standard.md` to enforce manager-grade structure, workstream/work-package planning requirements, dependency clarity, patch-oriented reporting, and anti-pattern checks.
- Added `skills/manager-make-new-plan/references/DEFINITIONS.md` as the canonical terminology source and kept it number-free.
- Added `skills/manager-make-new-plan/references/CAPACITY_AND_SIZING.md` as the single source of numeric capacity/sizing targets and patch throughput rules.
- Added `skills/manager-make-new-plan/references/NAMING_GUARDRAILS.md` to isolate naming anti-footgun rules, durable naming guidance, and legacy `phase3_*` handling.
- Refactored guide cross-references so mutable numeric targets live in one file, terminology meanings live in one file, and naming constraints live in one file to reduce drift across docs.
- Updated `skills/parallel-web-game-build/SKILL.md` to adopt milestone/workstream terminology, add a dedicated terminology-collision section, enforce stage-based durable naming, and replace `*_phase.js` template references with `*_stage.js`.
- Added `skills/parallel-web-game-build/references/DEFINITIONS.md` for canonical planning and durable-engineering terms.
- Added `skills/parallel-web-game-build/references/NAMING_GUARDRAILS.md` for anti-footgun naming policy and legacy `phaseN_*` handling.
- Added `skills/parallel-web-game-build/references/CAPACITY_AND_SIZING.md` for centralized parallel execution targets and patch sizing/cadence guidance.
- Reframed `skills/parallel-web-game-build/SKILL.md` as a specialized implementation profile of `manager-make-new-plan` and added preassigned default workstreams to enable faster manager execution with explicit ownership continuity.
- Refreshed `README.md` documentation links to match the current small docset and keep quick start concise and verifiable.
