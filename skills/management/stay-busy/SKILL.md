---
name: stay-busy
description: "Keep an agent manager productive through safe, evidence-producing follow-on work. Use for `/stay-busy`, idle orchestrators, waiting subagents, or active delegated workflows. Generates bounded workstreams and fallbacks; not productivity advice."
---

# Stay busy

Use this only inside an active `delegate-manager-to-subagents` workflow when
the obvious execution queue is genuinely empty and a safe, project-relevant
workstream remains. It generates workstream-shaped tasks; the manager owns
dispatch and completion.

## Non-negotiable boundary

Finish the obvious before expanding. Inspect every active or paused plan task
first. If any task needs implementation, verification, documentation, or
handoff, queue and close that task before creating a new workstream. Do not use
this skill to avoid final verification, to inflate scope, or to turn a targeted
request into speculative production changes.

Every selected task must produce evidence or remove a blocker. It carries:

- one canonical status: `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or
  `BLOCKED`; and
- one inspectable artifact path, such as a report, screenshot, command log,
  JSON record, or before/after metric.

`SIDE QUEST` is an optional task annotation, never a status. It remains
project-related and distinct from production-ready work.

## Decide before dispatch

1. Confirm the active approved plan, current idle state, and the clean
   finish-before-expanding gate.
2. Read [references/operating_modes.md](references/operating_modes.md) for
   away-mode decisions, safe defaults, and situation routing.
3. Read [references/scaling_and_cleanup.md](references/scaling_and_cleanup.md)
   to select the tier, apply an away-mode bump, and close stale excess work.
4. Read [references/ideas_checklist.md](references/ideas_checklist.md) to
   choose evidence-producing work and reject busywork. Then load only the
   selected workstream's requirements through
   [references/workstream_templates.md](references/workstream_templates.md).
5. Attach an explicit blocked fallback and use
   [references/boundaries.md](references/boundaries.md) for every authority or
   ask-only decision.

Away mode means the manager documents reversible assumptions and continues,
then produces finished artifacts rather than questions for the absent user. A
real boundary remains a boundary; route it according to the references instead
of inventing authority.

## Emit a usable handoff

Create one task per chosen workstream, including its goal, owner boundary,
done-when evidence, canonical status requirement, artifact path, and blocked
fallback. Use the standard output template from
[references/workstream_templates.md](references/workstream_templates.md), with
the allowed-without-asking and ask-only lists from
[references/boundaries.md](references/boundaries.md). Return the task list to
`delegate-manager-to-subagents` for dispatch.

For lifecycle rationale, overnight examples, and sibling-skill composition,
read [references/big_picture.md](references/big_picture.md). The routed
references intentionally hold conditional detail so this entrypoint remains a
small control plane.
