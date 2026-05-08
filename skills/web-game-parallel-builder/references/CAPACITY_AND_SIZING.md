# Capacity And Sizing

Numeric execution targets for batched parallel web-game delivery.

## Team Capacity Assumption
- Assume one orchestrator plus up to 6 coding agents during a milestone window.
- Plans should keep most coding agents unblocked most of the time.

## Workstream Targets Per Milestone
- Prefer 3 to 6 workstreams per milestone that can run in parallel.
- Each workstream has a named owner and explicit interfaces.

## Work Package Targets Per Workstream
- Per-workstream target: 2 to 6 work packages.
- Work packages should be completable by one coder and result in at least one patch.

## Ready-At-Start Minimums
- At milestone start, have at least 8 ready work packages (not blocked) so agents can pull work immediately.
- Ready means:
  - No external decisions pending.
  - Dependencies listed as none.
  - Verification commands already specified.

## Patch Cadence And Sizing Rules
- Track progress as patches, not effort.
- Target 1 to 2 reviewable patches per coding agent per week.
- If review becomes the bottleneck, split patches before adding more parallel work.
- If a patch touches more than two components, split it.
