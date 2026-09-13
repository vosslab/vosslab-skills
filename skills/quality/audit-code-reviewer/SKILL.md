---
name: audit-code-reviewer
description: Coordinate independent multi-reviewer audits before a merge or release; not for an ordinary single-pass review.
---

# Audit code review

Coordinate a release- or merge-level audit through independent reviewers. Use
this only when multiple focused review passes are needed; use a normal review
for a bounded single-pass request.

## Coordinator contract

- Gather the user request, applicable plan or ticket, changed-source boundary,
  relevant repository rules, and focused verification evidence.
- Launch the six named review passes in parallel once that minimal context is
  ready. Give each reviewer raw shared context and a distinct scope without an
  expected conclusion.
- Every pass uses a fresh independent reviewer. Do not reuse a reviewer for
  another pass or send follow-on editing work to a completed reviewer.
- Wait for results, merge concrete findings by severity, remove duplicates, and
  retain meaningful disagreement and missing-evidence risk.
- If independent reviewers are unavailable, report that the independent audit
  could not be performed and stop after reporting the gathered context and
  reason.

Inspect the supplied change boundary or current source evidence; preserve content
outside the intended review/fix boundary. Do not assume a repository-history,
staging, or diff mechanism is available.

## Review passes

Dispatch exactly these focused passes: Plan, Test, Style, Docs, Legacy, and
Comment. Read [Reviewer briefs](references/reviewer_briefs.md) for their
individual scope and the common prompt template. That reference owns the
detailed style and test checks so the audit stays aligned with the repository's
authoritative rules rather than copied checklists.

## Test and gate posture

Tests are liabilities as well as assets, and the audit asks for fewer of them.
Accept a reviewer's new-test finding when it cites the permanent-test checklist
in `docs/PYTEST_STYLE.md`; route every other test suggestion to `tests/_temp/`
as a one-time check. Report plan gates that lack a grounding need, such as
arbitrary thresholds or byte or pixel equivalence, as findings with the
recovery the plan should adopt instead.

## Integration and fixes

Prepare only the finding-severity order, changed-file list, test evidence, and
documentation evidence while reviewers run. Then produce findings first, with
issue, evidence, impact, and smallest useful fix; follow with assumptions,
residual risks, and a concise test/documentation summary.

After reporting findings, apply only obvious low-risk fixes within the authorized
change boundary, such as typos, stale documentation, dead imports, missing
comments, or removal of fragile tests identified by the Test pass. Report
any proposed permanent test as a finding for the human to approve. Leave
contested, architecture-level, or cross-file design changes as findings unless
the task separately authorizes their implementation.

## Completion

State whether all six independent passes completed. If they did, identify no-
finding passes and residual risks such as unavailable evidence or unreviewed
areas. If they did not, name every missing pass and why. Preserve the fresh-
reviewer safeguard even when one pass fails.
