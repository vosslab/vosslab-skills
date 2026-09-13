---
name: readme-docs
description: "Create or refresh a distinctive, evidence-backed `README.md` landing page for newcomers. Use when a README is missing, thin, generic, stale, or hard to navigate. Covers purpose, audience, first success, proof, examples, and documentation routes."
---

# README landing page

## Purpose

Make `README.md` a useful front door: establish identity, audience, value, proof, first success, and
deeper documentation routes in the order a newcomer needs them. This skill owns README content;
specialized documentation skills own their files under `docs/`.

## Route supporting resources

- Start from [`assets/README_TEMPLATE.md`](assets/README_TEMPLATE.md) for a missing, thin, or
  structurally failed README.
- Read [`references/readme_best_practices.md`](references/readme_best_practices.md) when project type
  or section choice is unclear.
- Read [`references/landing_page_ideas.md`](references/landing_page_ideas.md) when the page needs a
  stronger signature promise or proof treatment.
- Apply [`references/review_checklist.md`](references/review_checklist.md) for broad refreshes and
  final landing-page audits.
- Apply [`references/scoring_rubric.md`](references/scoring_rubric.md) for explicit scoring,
  before/after comparison, or a broad refresh.

Resolve every template placeholder before delivery.

## Landing-page contract

- Use one H1 for the project name, followed by a plain-prose opening paragraph of at most 250
  characters. State purpose, audience or use case, main benefit, and a distinguishing detail when
  space allows. Put links, badges, code, URLs, and setup after that paragraph.
- Establish purpose and the strongest available proof before `Quick start`.
- Give a verified install/run path that reaches a meaningful result, plus one representative example
  and expected behavior when useful.
- Summarize three to six concrete capabilities or outcomes and curate three to eight primary
  documentation routes before grouping a larger docset.
- Include supported status, limitations, prerequisites, platforms, help, license, citation, or
  contributor routes only when repository evidence makes them useful.
- Preserve current explanations, examples, visuals, warnings, and credits that remain accurate.

## Workflow

1. Read operative repository rules, the current README, core docs, manifests, executable front
   doors, examples, tests, screenshots, release/deployment evidence, and license files.
2. Derive the project name, audience, primary value, project type, first-success path, strongest
   proof, and adoption constraints from current evidence.
3. For a broad refresh, score the current page and identify the two highest-value improvements.
4. Design the newcomer journey: identity and value, proof, first success, representative use,
   deeper routes, then secondary adoption context.
5. Write a project-specific opening and choose a live demo, screenshot, output sample, compact
   transformation, architecture visual, or worked scenario that proves the signature promise.
6. Verify every command that is safe and practical. Match paths, claims, live links, deployment
   URLs, status, and license wording to repository evidence.
7. Apply the routed review checklist, repository Markdown/ASCII checks, and
   `tests/test_readme_first_paragraph.py` when present. Re-score broad refreshes.

## Managed visuals

When the project has a visual interface/output or the user requests screenshots, include this exact
empty block for `screenshot-docs`:

```markdown
<!-- screenshots:begin (managed by screenshot-docs) -->
<!-- screenshots:end -->
```

This skill owns surrounding prose and the sentinel lines. `screenshot-docs` owns capture,
`docs/screenshots/`, alt text, embed syntax, and the content between sentinels.

For a browser app, place a confirmed live link near the opening. Use a configured URL; derive a
Pages URL only when deployment evidence confirms it.

## Content boundary

Keep the value proposition, primary onboarding path, representative example, and navigation context
in README. Route exhaustive APIs, configuration, architecture, troubleshooting, and maintainer
process to their owning docs. Turn substantive missing docs and remaining landing-page opportunities
into bounded follow-ups with an owner, target, evidence, success criteria, and verification.

## Completion

Return the updated README, commands and links checked, unresolved claim status, and routed doc gaps.
For broad refreshes, include before/after scoring and the strongest gain. Finish only when the quick
start reaches a real result, the page carries project-specific proof when applicable, all placeholders
are resolved, and current valuable content remains discoverable.
