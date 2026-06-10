# Execution Resources

Agent catalog, skill lifecycle, and assignment guidelines for mapping work packages to owners.

## Agent Catalog

Planning-oriented summary of available agent types. The Owner field in work package templates must reference one of these agents.

| Agent | Model | Capability | Cannot do | Best for |
| --- | --- | --- | --- | --- |
| coder | sonnet | Production code, small doc updates | Architectural redesign, self-review | Default code work packages |
| expert_coder | opus | Hard, ambiguous, or design-sensitive code | Architectural redesign, self-review | Complex code work packages, `BLOCKED` escalations |
| tester | haiku | Tests, coverage, validation | Production code | Test work packages |
| planner | -- | Plans and docs | Code or tests | Doc-only work packages |
| architect | -- | Cross-cutting design approval | Implementation | Architecture decisions, design gates |
| reviewer | sonnet | Read-only code/plan review | Code modification | Patch review, plan auditing |
| orchestrator | sonnet | Parallel task coordination | -- | Multi-stream milestone coordination |
| parallelizer | -- | Team creation, messaging | -- | Dispatching parallel teams |
| integrator | sonnet | Merge, rebase, conflict resolution | New production code | Merge work packages |
| maintainer | haiku | Cleanup, lint, index regen | Features, arch decisions | Housekeeping work packages |
| monitor | haiku | Observe progress, detect stalls | Code modification | Operational oversight |
| scheduler | haiku | Trigger workflows, retry tasks | Diagnosis, code | Recurring workflow triggers |
| image_evaluator | opus | Image and screenshot evaluation writeups | Production code | Visual acceptance, design QA work packages |
| playwright_operator | sonnet | Browser automation and screenshots via Playwright | Production code | Web capture and UI walkthrough work packages |

## Skill Lifecycle

Each stage of the plan lifecycle is handled by a different skill.

| Stage | Skill | Purpose |
| --- | --- | --- |
| Plan creation | blueprint-plan-drafter | Build plan from scratch |
| Plan execution (parallel) | parallel-plan | Lightweight parallelization for active work |
| Subagent dispatch | delegate-manager-to-subagents | Fresh-subagent dispatch of independent work packages |
| Pre-merge audit | audit-code-reviewer | Parallel multi-reviewer audit before merge or release |
| Multi-agent coordination | gas-town-workflow | Role-mapped task routing with convoy patterns |

## Assignment Guidelines

Rules for mapping work packages to agent owners:

- Assign code work packages to `coder` (sonnet) by default.
- Assign hard, ambiguous, or design-sensitive code work packages to `expert_coder` (opus); keep routine work packages on `coder`.
- Assign test work packages to `tester`.
- Assign doc-only work packages to `planner`.
- Architecture decisions and design gates require `architect` approval.
- Every patch must be audited by `reviewer` before closure.
- Merge and integration work packages go to `integrator`.
- Cleanup, lint, and index regeneration go to `maintainer`.
- Do not assign implementation work to `monitor` or `scheduler`; they are read-only or trigger-only.
- Use `orchestrator` to coordinate multi-stream milestones with parallel workstreams.
- Use `parallelizer` when dispatching independent teams that need messaging.
- When a work package spans code and tests, split it into separate packages for `coder` and `tester`.
- Assign image and screenshot evaluation to `image_evaluator`; reserve its opus tier for substantive writeups, not trivial image reads.
- Assign browser capture and UI walkthroughs to `playwright_operator`.
- The two pair for visual-acceptance loops: `playwright_operator` captures, `image_evaluator` judges. The operator follows local repo patterns first (for example a `devel/setup_playwright.sh` helper or `tests/playwright/` conventions when the repo provides them).
