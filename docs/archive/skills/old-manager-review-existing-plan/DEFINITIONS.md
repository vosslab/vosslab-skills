# Definitions

Canonical terminology for manager planning docs in this skill.

## Planning Terms
- Milestone: timeboxed planning unit with deliverables and gates. Use in docs only.
- Workstream: parallel lane inside a milestone. Ownable by one coder or a small pair.
- Work package: coder-sized chunk with acceptance criteria and verification commands.
- Patch: a reviewable code change set (PR-sized), used in summaries and changelog entries.

## Durable Engineering Terms
- Stage / Step / Pass: durable pipeline step or algorithm pass (allowed in code identifiers).
- Component / Module / Subsystem: durable code boundary (allowed in filenames, packages, tests).
- Preferred durable labels in code: component, module, stage, pass, feature, contract.
- Naming policy and legacy handling live in `references/NAMING_GUARDRAILS.md`.
