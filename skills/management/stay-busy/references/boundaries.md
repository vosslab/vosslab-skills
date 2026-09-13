# Boundaries

Three lists govern stay-busy: resolvable choices, protected no-mutation
boundaries, and safe autonomous actions. Together they prevent the two
failure modes: passive waiting and reckless motion.

The anti-metric-gaming list is the test-artifact expression of "Fix the
design, not the symptom" from the core philosophies in
`docs/REPO_STYLE.md`.

## Resolve plan-governed choices autonomously

Architecture, contract, deletion, and authority ambiguity are not
automatic reasons to stop. First use the approved plan, captured inputs
and invariants, current repository authorities, and bounded repository
evidence to identify the option that best preserves the requested
outcome. When that evidence establishes one clearly best reversible
option, implement it and record the evidence and assumption.

Use a fresh independent review before making that resolution. If the
first two inspections disagree, request a third independent inspection
and resolve only when the combined evidence identifies a clearly best
reversible option. Do not substitute a weaker or narrower outcome merely
to avoid an ambiguity.

This applies, for example, to a compatible public-API or file-format
detail, a bounded architecture choice already constrained by the plan,
or removal of an obsolete local artifact whose replacement and recovery
path are established by current authority. Continue unrelated safe work
while this evidence is gathered.

## Protected no-mutation boundaries

Do not make a mutation when the next step is risky, irreversible,
externally mutating, or expands authority beyond the approved plan. This
includes:

- Broad production migration (multi-service rollout, schema changes,
  irreversible data moves).
- Deletion or quarantine of major systems (modules, services, datasets)
  without a plan-established replacement and recovery path.
- Irreversible operations (force push, history rewrite, destructive
  repository operations, production data wipe).
- Safety or policy-sensitive choices (secrets handling, third-party
  publishing, security-relevant defaults).
- An architecture switch not bounded by the plan (framework, language,
  or storage-backend change).
- Contract amendments that expand public commitments beyond established
  authority.
- Accepting a known invalid result as final (closing a milestone despite
  a failing acceptance gate).

For a boundary case, record the exact action, missing authority or
evidence, affected scope, and why it cannot be safely reversed. Leave
that action unmodified and continue every independent safe workstream.
The record is a blocker for that action, not a reason to require a human
response before completing unrelated work.

## Safe autonomous actions

These actions are reversible, evidence-producing, or scoped within the
current milestone. Do them; do not interrupt the user to confirm.

- Rerunning tests, lints, or any pytest gate.
- Reverting a recent overstep (single-commit revert; bounded file
  restore).
- Writing documentation: changelog entries, plan updates, report files,
  inline comments per `docs/PYTHON_STYLE.md`.
- Capturing screenshots, including Playwright runs against existing
  pages.
- Running diagnostics: profilers, memory probes, log clustering.
- Bounded CSS or styling changes scoped to a single component or page.
- Launching read-only audits (audit workstream from
  [workstream_templates.md](workstream_templates.md)).
- Producing reports that synthesize existing evidence.
- Generating stress tests, cluttered scenes, edge inputs.
- Adding skipped tests with `pytest.skip("reason")` to mark gaps
  without claiming false passes.
- Updating `docs/CHANGELOG.md` under today's date heading.

## Metric-gaming forbidden

The output must remain trustworthy. The skill forbids these because they
turn evidence into a lie:

- Changing the diagnostic so it passes. Fix the artifact, not the test.
- Deleting DOM, files, or state before a precheck so the precheck
  succeeds against an empty target.
- Hiding failures by catching errors silently or rerouting output to
  `/dev/null`.
- Using untracked files as proof. Evidence paths must be tracked or
  explicitly listed as transient outputs under `output/`.
- Claiming success from a written summary when no inspectable artifact
  was produced. "I looked into it" handoffs are rejected.
- Broad rewrites that obscure the cause of a failure. Keep the
  failure-causing change isolated and reviewable.
- Weakening tests to make them pass: removing assertions, loosening
  tolerances, replacing exact matches with substring matches just to
  avoid red. Either fix the artifact or mark the test as a known gap.
- Renaming a failing workstream as `DONE_WITH_CONCERNS` to dodge
  `BLOCKED`. Status labels carry contract weight; misuse forfeits trust.
