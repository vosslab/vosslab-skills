---
name: ui-ux-engineer
description: Review, improve, and engineer UI/UX quality in any framework. Covers visual hierarchy, interaction quality, accessibility, validation, error states, empty states, and design heuristics. Use when reviewing or improving the user experience of an interface, regardless of the underlying technology.
---

# UI/UX Engineer

## Overview

Use this skill to review and improve the user experience of any interface.
This skill is framework-agnostic and focuses on design quality, interaction logic, and usability.
It applies equally to desktop, web, and mobile surfaces.

## Workflow

1. Detect project shape.
- New or greenfield UI: establish the user goal and primary flow first, choose a
  window posture or page layout, and defer visual polish until the interaction
  structure is sound.
- Improving an existing interface: read the existing surface first, identify the
  main friction points across hierarchy, interaction quality, and state coverage,
  then scope changes by user impact.

2. Identify the surface and its primary user goal.
- Determine what the user is trying to accomplish and what states must be handled: loading, empty, valid, invalid, busy, success, and failure.
- Identify the main workflow path and any secondary paths.

3. Review visual hierarchy and layout.
- Make visual hierarchy obvious with spacing, grouping, alignment, and restrained emphasis.
- Keep forms short, labels explicit, and primary actions visually dominant.
- Check that the screen communicates its purpose in three seconds.
- Check that the main action is obvious and visually dominant.
- Read [`references/ui_ux_review.md`](references/ui_ux_review.md) for the full review checklist covering hierarchy, interaction quality, validation, state coverage, and accessibility.

4. Review interaction quality.
- Give immediate feedback for user actions.
- Prevent errors before showing errors.
- Keep destructive actions explicit and reversible when practical.
- Support keyboard flow, sensible tab order, and accessible names or tooltips where needed.
- Check whether busy work has been removed from the user's path.

5. Review edge states.
- Check whether edge states (empty, error, loading, offline) look intentional rather than broken.
- Verify that validation messages are clear and actionable.
- Verify that error recovery paths exist.

6. Reference design heuristics when needed.
- Read [`references/design_books.md`](references/design_books.md) when you need durable design heuristics, typography guidance, grid and layout thinking, or design-system perspective.
- Reach for these books when they match the problem:
  - "Refactoring UI" for visual hierarchy, spacing, typography, color, and component polish.
  - "Practical UI" for logic-driven accessibility, interaction, and usability rules.
  - "About Face" for flow, task structure, dialog behavior, and interaction model decisions.

## Implementation defaults

- Load the local-only books first when present; see the coverage map in [`references/reference_survey.md`](references/reference_survey.md) and the broader design literature in [`references/design_books.md`](references/design_books.md).

## Quality bar

- Favor clarity over decoration.
- Avoid cramped layouts, unlabeled icons, ambiguous submit buttons, and dialogs that ask questions without context.
- UI decisions should be defensible in terms of user goals, not personal taste.

## Output expectations

When using this skill, aim to produce:
- Specific, actionable feedback tied to user goals and usability principles.
- A short explanation of key UX decisions when the change is non-obvious.
- Recommendations grounded in the reference materials rather than subjective opinion.
