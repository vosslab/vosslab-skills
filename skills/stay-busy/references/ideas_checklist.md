# Workstream ideas and checklist

Read this guide after selecting a tier and before emitting the TaskList. It
helps choose useful workstreams, attach blocked fallbacks, and reject motion
that produces no trustworthy evidence.

## Selection checklist

- [ ] The finish-before-expanding gate is clean.
- [ ] Every workstream relates to the active project or milestone.
- [ ] The selected count fits the tier in
  [scaling_and_cleanup.md](scaling_and_cleanup.md).
- [ ] Every task has one owner, one outcome, and one verification step.
- [ ] Every task names a canonical status label and inspectable artifact.
- [ ] Every task includes a blocked fallback.
- [ ] `SIDE QUEST` labels appear only on optional evidence-producing work.
- [ ] Ask-only decisions route through [boundaries.md](boundaries.md).
- [ ] The final output uses
  [workstream_templates.md](workstream_templates.md).

## Idea catalog

Choose ideas that fit current evidence and project risk:

- Audit correctness, style, contracts, coverage gaps, dead code, or data
  quality without editing production code.
- Compare alternative implementations or methodologies on the same inputs
  and metrics.
- Build missing tests, hard-negative fixtures, stress matrices, cluttered
  scenes, or long-run reliability checks.
- Capture screenshots, output galleries, benchmark traces, or profiling
  summaries.
- Investigate one known failure, regression, intermittent test, or suspicious
  metric with a bounded diagnostic artifact.
- Refresh documentation examples, release readiness evidence, release notes,
  or a long-form synthesis report.
- Prototype a next-iteration feature or uncertain approach as an explicitly
  labeled side quest.

Use the precise per-type prompt from
[workstream_templates.md](workstream_templates.md), not this idea list, when
dispatching.

## Blocked-fallback starters

- Generator unavailable: hand-author a small representative fixture set.
- Browser automation unavailable: capture static evidence and document the
  blocked interactive check.
- Production seam unavailable: continue with read-only audit, tests, or a
  reproducible diagnostic.
- External data unavailable: validate the pipeline against committed samples
  and record the missing-data boundary.
- Performance environment unstable: record variance and compare relative
  results rather than claiming an absolute benchmark.

## Reject before dispatch

- Fake progress, unsupported success claims, or artifacts that cannot be
  inspected.
- High-risk changes, broad migrations, or deletions without required approval.
- Test weakening, hidden failures, metric gaming, or uncertainty presented as
  certainty.
- Tiny task spam, endless planning documents, or housekeeping unrelated to the
  active milestone.
- Work that overrides explicit user instructions or substitutes motion for
  useful evidence.
