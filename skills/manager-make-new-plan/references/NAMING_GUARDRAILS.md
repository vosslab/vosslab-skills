# Naming Guardrails

Rules for keeping planning vocabulary out of durable repository identifiers.

## Core Rule
- Use planning terms (milestone, workstream, work package) only in planning docs, never in filenames, module names, test names, CLI flags, or public APIs.
- Reason: planning labels change over time; code identifiers must remain stable.

## Durable Naming In Code
- Use Stage / Pass / Step for durable pipeline or algorithm steps.
- Use Component / Module / Subsystem / Contract for durable boundaries and behavior surfaces.
- Prefer behavior-based test names (for example, `test_export_contract.py`) over schedule-based names.

## Legacy Handling
- If a repository already has `phase3_*`-style filenames, treat "phase" there as legacy meaning "stage".
- Do not introduce new planning-phase terminology into code.
- Migrate legacy names opportunistically when safe, but do not block delivery solely for renames.
