# Capacity And Sizing

Numeric planning targets for manager throughput. Keep these numbers here so updates do not drift across guides.

## Team Capacity Assumption
- Assume up to 8 coders per manager during a milestone window.
- Plans should keep most coders unblocked most of the time.

## Workstream Targets Per Milestone
- Prefer 4 to 8 workstreams per milestone that can run in parallel.
- Target 0.75 to 1 workstream per coder where practical.
- Each workstream has a named owner and explicit interfaces.

## Work Package Targets Per Workstream
- Per-workstream target: 6 to 16 work packages.
- Work packages are sized for one coder and should result in at least one patch.

## Ready-At-Start Minimums
- At milestone start, have at least 16 ready work packages (not blocked) so 8 coders can pull work immediately and still have slack.
- Ready means:
  - No external decisions pending.
  - Dependencies listed as none.
  - Verification commands already specified.

## Patch Cadence And Sizing Rules
- Work is tracked and reported as patches, not effort.
- Target 1 to 2 reviewable patches per coder per week.
- If review becomes the bottleneck, split patches before adding more coders.
- If a patch touches more than two components, split it.
