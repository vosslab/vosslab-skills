# Definitions

Canonical terminology for parallel web game planning docs in this skill.

## Planning Terms
- Milestone: a timeboxed integration checkpoint that groups parallel workstreams.
- Workstream: a parallel lane owned by one coding agent (or a small pair) within a milestone.
- Work package: an assignment-sized chunk with acceptance criteria and verification commands.
- Patch: a reviewable change set used for progress tracking and integration summaries.

## Durable Engineering Terms
- Stage / Step / Pass: durable gameplay pipeline or algorithm steps allowed in code identifiers.
- Component / Module / Subsystem: durable code boundaries allowed in filenames and tests.
- Preferred durable labels in code: component, module, stage, pass, feature, contract.

- Naming policy and legacy handling live in `references/NAMING_GUARDRAILS.md`.

## TypeScript Engineering Terms
- Type contract: a `src/types/*.ts` file that exports `type` and `interface` declarations consumed by multiple runtime modules. Type-only; no runtime values.
- Brand constructor: the normal place where an `as <Brand>` cast is isolated. Unchecked casts outside brand constructors or documented boundary guards (for example save-file `is*` type guards) are red flags; the canonical rule lives in `skills/typescript-engineer/references/opaque-types.md`.
- Strict baseline: `strict` + `noUncheckedIndexedAccess` + `exactOptionalPropertyTypes`, sourced from `skills/typescript-engineer/references/strict-mode-flags.md`.
