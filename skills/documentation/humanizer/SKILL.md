---
name: humanizer
description: "Humanize text: strip AI-isms and add real voice."
version: 2.5.2
author: Siqi Chen (@blader, https://github.com/blader/humanizer), ported by Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, editing, humanize, anti-ai-slop, voice, prose, text]
    category: documentation
    homepage: https://github.com/blader/humanizer
---

# Humanizer

Use when asked to make writing sound natural, match the author's voice, or review a draft for
AI-like prose. Apply the same editing checks to your own user-facing writing.

## Editing pass

1. Read the original and any voice sample. Identify the reader, the purpose, and the main point.
2. Fix clarity first. Name the actor and action when known, resolve vague references, and put the
   result or request where readers can find it. Flag missing facts rather than guessing.
3. Match the author's tone and the genre. Keep useful passives, hedges, and punctuation. Treat
   surface patterns as editing clues, not as evidence of authorship or a detector target.
4. Compare the rewrite with the original. Check who did what, attribution, negation, quantities,
   scope, conditions, and uncertainty. Keep claims, quotes, and personal details grounded in the
   source. Read the result aloud to check the rhythm.
5. For a requested rewrite, show the draft, a brief clarity and fidelity audit, and the final
   version. For edits on disk, show a diff or the changed passage.

## Dr. Voss's everyday email

- Use `5pm`, `9am`, and `5:30pm` in subject lines and body text. Keep that format when editing his
  drafts: lowercase, no spaces or periods, and no zero minutes on whole hours.
- Use `today at 5pm` when the day is clear. Add a date such as `Nov 18` when readers need it. Keep
  exact dates, times, and time zones where precision matters, and follow any specified style guide.

## References

- Read [references/ai-writing-checklist.md](references/ai-writing-checklist.md) for substantive
  rewrites, voice matching, or a requested AI-writing review. Use the relevant checks for short
  edits. After multiple passes, compare final claims and certainty with the author's original.
- Read [references/writing-patterns.md](references/writing-patterns.md) when matching a voice sample
  or diagnosing a recurring writing pattern. It includes examples and upstream attribution.
- Read [references/zonderlabs-clarity.md](references/zonderlabs-clarity.md) for tricky clarity edits,
  review cases, or source evaluation when updating the skill. Ordinary rewrites need no research.
- Read [references/rewrite-example.md](references/rewrite-example.md) when demonstrating a draft,
  audit, and final rewrite.

## Maintenance

Edit the canonical copy in `vosslab-skills/skills/documentation/humanizer/`. Hermes loads that
copy through its documentation skill link. Keep conditional details in the linked references.
