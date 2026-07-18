# Operating modes and authority

Read this guide after the finish-before-expanding gate passes. It defines
how away mode changes workstream defaults and which decisions the manager
makes without interrupting the user.

## Away mode

When the user is sleeping, leaving, or running an unattended session,
widen workstream scope and prefer finished evidence over pending questions.
Away mode never bypasses unfinished verification, documentation, or handoff
work from the active plan.

- Bump the normal tier once: small to medium, medium to large, and large to
  stress. Explicit long-running requests remain stress tier.
- Prefer multi-methodology suites, writeups, A/B testing, labeled side
  quests, and codebase audits over small recovery tasks.
- Resolve reversible choices with a documented assumption. Ask only when a
  choice crosses a boundary in [boundaries.md](boundaries.md).
- Treat a 25-100 page report as valid when enough evidence exists. TypeScript
  repositories may render HTML to PDF with Playwright evidence; Python
  repositories use Markdown under repo style.
- Finish every workstream to an inspectable artifact before handoff.

Use [scaling_and_cleanup.md](scaling_and_cleanup.md) to choose the bumped
tier and [workstream_templates.md](workstream_templates.md) to dispatch the
selected workstream types.

## Manager decision authority

The manager decides every choice that does not cross an ask-only boundary.
Record the reasoning in the workstream artifact and continue.

- Investigate surprising results with more evidence: variance runs, input
  sweeps, or comparisons against the incumbent.
- When two safe options remain, choose the one that best matches project
  priorities and record both the choice and runner-up.
- Treat uncertain findings as prompts for more testing, not prompts for the
  user, unless further work would change architecture, contract, deletion,
  or broad production behavior.
- Require the canonical status label and artifact path on every handoff so
  the user can audit unattended decisions later.

## Default-to-safe-work rules

- Execute decisions already present in the plan or prompt.
- Take safe defaults and document material assumptions.
- When one workstream blocks, dispatch another safe workstream.
- Fix failed checks and rerun them.
- Continue the current milestone past non-blocking issues; record them in
  the artifact.
- Ask the user only at the boundaries listed in
  [boundaries.md](boundaries.md), with two or three concrete options.

## Situation routing

| Situation | Action |
| --- | --- |
| A task finishes | Dispatch the next unblocked plan task |
| A check fails | Fix the failure and rerun the check |
| A background agent runs | Prepare review, next brief, file list, or test plan |
| A non-blocking issue appears | Document it and continue the milestone |
| A real boundary appears | Stop and ask with two or three concrete options |
