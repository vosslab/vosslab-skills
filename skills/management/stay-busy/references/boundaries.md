# Boundaries

Three lists govern stay-busy: what to ask the user, what to do without
asking, and what is forbidden. Together they prevent the two failure
modes: passive waiting and reckless motion.

The anti-metric-gaming list is the test-artifact expression of "Fix the
design, not the symptom" from the core philosophies in
`docs/REPO_STYLE.md`.

## Ask only for

Ask the user only when the next step changes architecture, contract,
deletion, or broad production behavior. Concrete cases:

- Contract amendments (public API shape, output schema, file format).
- Broad production migration (multi-service rollout, schema changes,
  irreversible data moves).
- Deletion or quarantine of major systems (modules, services, datasets).
- Irreversible operations (force push, history rewrite, destructive
  git operations, production data wipe).
- Safety or policy-sensitive choices (secrets handling, third-party
  publishing, security-relevant defaults).
- Architecture switch (framework change, language change, storage
  backend change).
- Accepting a known invalid result as final (closing a milestone
  despite a failing acceptance gate).

When asking, present 2 to 3 concrete options. Do not present an
open-ended question.

## Allowed without asking

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
