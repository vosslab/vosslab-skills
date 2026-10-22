# Assess the integrated experience

Match evidence to the claim and the uncertainty. Keep technical correctness,
observed behavior, agent design judgment, and measured human experience separate.
Complete authorized work without a human playtest or aesthetic approval dependency.

## Proportional checks and assessment

| Change | Evidence and assessment | Failure action |
| --- | --- | --- |
| Straightforward documentation | Existing metadata, link, and consistency checks; manager inspection | Correct the specific defect |
| Local gameplay behavior | Focused behavior test or probe and actual-control reproduction | Repair the responsible behavior and rerun |
| Substantial gameplay or campaign revision | Representative opening, progression, failure/retry, and completion runs; independent assessment | Revise the supported weak experience and verify affected scenarios |
| Substantial artwork or transformation | Shipping-render captures at gameplay scale, including state pairs or progression; independent visual assessment | Correct the asset or integration that breaks the intended reading |
| Integrated parallel build | Required engineering gates, actual-control playthrough, and fresh independent review of the shared brief | Repair supported findings and recheck the integrated result |

Use existing validators for ordinary skill documentation changes. Add independent
assessment where uncertainty, substantive creative work, or cross-module integration
warrants it. Keep minor repairs inside the focused verification loop.

## Evidence that answers questions

- **Control:** exercise turns, release, collision, and retry in representative
  encounters. Compare intended input with response; use the target device and
  frame behavior where the claim depends on them.
- **Novelty and pacing:** inspect the sequence of player actions and decisions.
  Name what changes, where discovery gives way to practice, and where repetition
  no longer adds interest. Distinguish a new experience from higher difficulty.
- **Identity and readability:** inspect actual-size silhouettes, expressions,
  hazards, and scene composition. Compare beginning/middle/end states together.
- **Progress and fairness:** exercise promised goals, meaningful consequences,
  loss, recovery, and completion. Check the route from failure back to useful play.
- **Coherence:** follow a complete interaction across input, simulation, artwork,
  audio, camera, and reward. Compare it with the shared brief and baseline.

Use real browser controls for route evidence. Deterministic state probes help
inspect rare states but do not establish that players can reach them normally.
Use meaningful stable behavior tests where justified; temporary probes suffice
for tunable settings and exploratory evidence. Keep arbitrary fun scores out of
acceptance. Human enjoyment and learning gains require actual human evidence.

## Independent review and correction

For a substantive review, give a fresh agent the request, shared brief, relevant
baseline, artifact, reproducible scenario, and evidence without an expected verdict.
Ask for concrete findings about control, surprise, readability, pacing, identity,
fairness, or payoff. Reviewers should distinguish observations from hypotheses.

The manager resolves supported findings through bounded correction and verification.
Use an additional independent inspector only for a material unresolved disagreement;
decide from the brief and reproducible evidence. A vague preference alone does not
justify another redesign cycle. Report real unavailable evidence and its limits.

## Audit the unattended path

During planning, trace deliverable, prerequisites, checks, assessment, correction,
and completion with no further human messages. Replace manual input, asset handoff,
preview startup, screenshot capture, style selection, or final approval assumptions
with actions available to the manager and subagents. Missing human availability is
not a blocker. Optional feedback can revise a decision or start follow-up work.
Keep execution within authorized scope and preserve the target's required checks.
