# Software design and verification

Read for software plans so coding-specific policy stays out of non-coding planning context.

## Robustness and adaptability

Robust software continues to function despite imperfect inputs, data, state, or behavior. Handle
imperfections according to their context and impact, using graceful recovery to preserve useful
operation where appropriate while protecting correctness.

Favor clear boundaries, stable domain concepts, and replaceable components over speculative
edge-case machinery. Cover concrete requirements and likely failure modes; leave room to address
unexpected cases later. Apply the entrypoint's KISS and configuration criteria to each mechanism.

## Choose verification

Consult applicable repository guidance, including `docs/REPO_STYLE.md`, `docs/PYTEST_STYLE.md` and
its permanent-test checklist, `tests/TESTS_README.md`, and `devel/DEVEL_README.md` when present.
Match checks to the actual outcome, using exact commands when they materially affect execution.

Separate one-time implementation evidence from permanent tests. Every permanent test constrains
future design and must protect intentionally stable, important behavior with plausible regression
risk. Prefer contracts over implementation details. When the retention case is weak, use a one-time
check. When in doubt, remove the test.

Keep temporary checks in repository-relative `tests/_temp/`, outside permanent test ownership and
Git tracking. Follow the repository's temporary-check execution conventions. At closeout, promote
only checks whose behavior deserves permanent protection and remove the rest.

If a test requires an unrelated implementation hack, question the test first. Permit intended
behavior changes while preserving genuine contracts. Each blocking gate needs a grounded reason
and a concrete decision, correction, or recovery action when it fails, as defined in the entrypoint.
