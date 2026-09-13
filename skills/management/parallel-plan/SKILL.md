---
name: parallel-plan
description: "In-flight nudge to split current work into independent tracks for parallel subagent dispatch; does not create new plans (use blueprint-plan-drafter for that)."
---

# Parallel plan

## Purpose

Turn current in-flight work into the smallest set of independent workstreams that lowers elapsed
time to a correct, integrated result. Use the milestone, workstream, work package, and patch terms
from `blueprint-plan-drafter` without creating a new full plan.

## Select an execution mode

- Use real parallel execution when independent streams can run concurrently with isolated file or
  state ownership.
- Use orchestration-only when the environment cannot provide concurrency; still write complete
  stream briefs and dependency order.
- Keep work serial when dispatch, coordination, and integration would cost more than the split saves.
- Resolve shared types, schemas, fixtures, interfaces, and migration order before dispatch.

## Discover available roles

Inspect the live agent catalog exposed by the current environment and the target repository's
owned agent metadata, if present. Read the matching role instructions before assignment. Use the
most specialized available role whose permissions and responsibility fit the stream; use generic
owner labels when no catalog exists. Treat the live catalog as authority rather than copying role
names into this skill.

## Define workstreams

For each stream, state:

- one objective and one owner;
- the exact files, directories, or mutable state it owns;
- dependencies and required inputs;
- an assignment-sized set of work packages;
- one focused verification step;
- an orchestrator-selected, collision-safe report path when file-backed reports are needed.

Merge or serialize streams that would edit the same files or mutable state. Use the smallest number
of streams that materially improves wall time.

## Dispatch and integration

1. Complete shared prerequisites in the manager context.
2. Launch every ready stream concurrently through the environment's supported dispatch mechanism.
3. Require compact handoffs; keep large logs and detailed findings in the assigned report files.
4. Confirm every expected report exists and every stream-specific check passes.
5. Integrate in dependency order and run the shared verification gate once.
6. Repair failed streams or integration before declaring the milestone complete.

Use [`references/parallel_plan_templates.md`](references/parallel_plan_templates.md) for stream
briefs, compact handoffs, report structure, synthesis, checkpoints, and fake-parallelism checks.

## Independence rules

- Parallel streams have no in-flight dependency on one another's output.
- Each mutable resource has exactly one owner.
- Dependency-establishing work finishes before dependent streams launch.
- Research and review streams receive only the evidence needed for independent judgment.
- Status messages report progress; follow-up editing work receives a fresh bounded assignment under
  the active environment's delegation rules.

## Output contract

Produce:

1. The milestone objective.
2. Workstreams with owners, scope boundaries, dependencies, and verification.
3. Work packages within each workstream.
4. An ordered patch and integration plan.
5. Checkpoints with pass/fail criteria and correction paths.

Each stream handoff reports status, report path when assigned, three to six summary bullets,
validation status, and blocking issues. Each detailed report records assumptions, decisions,
concrete next steps, changed files, and validation performed.

## Completion

Finish when all shared prerequisites are resolved, ownership is non-overlapping, every stream has a
bounded brief and verification, all required reports and checks pass, and the integrated result has
one ordered completion gate.
