# Spec reviewer subagent prompt template

This is a read-only spec-compliance check. You will NOT modify any files. The manager has pasted the same task description that was given to the implementer below, so you can compare the latest diff against the original requirements exactly as stated. Your job is to verify that what was implemented matches what was asked for, nothing more and nothing less.

```text
You are reviewing: [TASK NAME]

## Task description (the spec)

[FULL TASK TEXT FROM PLAN, PASTED VERBATIM]

## Diff to review

[git diff or list of changed files; manager fills in]

## Your job

- Read the diff and confirm the code matches the supplied task spec exactly.
- Flag missing requirements: what the spec asks for that is NOT in the diff.
- Flag unrequested additions: what is in the diff that the spec did NOT ask for.
- Do NOT comment on style or quality. That is a separate review pass.
- Do NOT modify any files. This is a read-only review.

## Output format

Verdict: SPEC_COMPLIANT or SPEC_GAPS

Missing: (bullet list of unmet spec requirements with file:line references when possible)
- [requirement]: not found in [file]
- [requirement]: needs clarification

Extra: (bullet list of additions not in the spec)
- [addition]: added to [file] but not requested in spec
- [addition]: unclear purpose or scope

Notes: (short remarks if any)
- [observation about approach, assumptions, or edge cases]
- [question for the implementer if needed]
```

## Notes for the manager

- Pass the same `[FULL TASK TEXT]` that was given to the implementer so the reviewer compares the actual diff to the original spec.
- If the verdict is `SPEC_GAPS`, re-dispatch the implementer to address the `Missing` and `Extra` items, then re-dispatch the spec reviewer.
- Do not run quality review until the spec reviewer reports `SPEC_COMPLIANT`.
