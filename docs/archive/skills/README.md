# Archived skills

Skills that were once published under `skills/` but were retired. Preserved
for historical context. Not indexed in [docs/SKILLS_INDEX.md](../../SKILLS_INDEX.md)
and not published in the plugin manifest.

## Retired 2026-05-20

| Skill | Reason | Replacement |
| --- | --- | --- |
| [old-manager-review-existing-plan](old-manager-review-existing-plan/) | Severe internal inconsistency: divergent duplicate of `plan_quality_standard.md` (milestone vs phase vocabulary), broken cross-links to a missing `references/CAPACITY_AND_SIZING.md`, and `DEFINITIONS.md`/`NAMING_GUARDRAILS.md` at skill root but referenced as `references/X.md`. Already excluded from plugin manifest. | [audit-code-reviewer](../../../skills/audit-code-reviewer/SKILL.md) for pre-merge multi-reviewer audit + [blueprint-plan-drafter](../../../skills/blueprint-plan-drafter/SKILL.md) for forward-looking planning standard. |
| [old-orchestrate-next-milestone](old-orchestrate-next-milestone/) | Skill body explicitly cross-referenced `delegate-manager-to-subagents` as its modern home; standalone-doer mode rarely applied. Already excluded from plugin manifest. | [delegate-manager-to-subagents](../../../skills/delegate-manager-to-subagents/SKILL.md) for manager-driven dispatch + [parallel-plan](../../../skills/parallel-plan/SKILL.md) for lane splitting. |

## Still active

[skills/old-python-code-review/SKILL.md](../../../skills/old-python-code-review/SKILL.md)
is kept frozen under `skills/` (not archived here). `audit-code-reviewer` is
a heavyweight parallel multi-reviewer coordinator and is not a 1:1
replacement for the lightweight single-pass case, so the skill remains
available even though it is excluded from the published plugin manifest.
