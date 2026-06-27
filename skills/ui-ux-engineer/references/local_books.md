# Local books

Use this reference to pick the right local-only book for a UX task. The three
converted books live in `references/local-only/` and stay out of git. Load them
by bare path text at runtime and grep the named file for a keyword. The detailed
coverage map lives in [reference_survey.md](reference_survey.md).

## Reading order (strongest first for UX work)

1. `references/local-only/About_Face.txt`
   Best for interaction design fundamentals: task flow, goal-directed behavior,
   dialog behavior, posture, navigation, affordances, feedback, and excise.
   Start here for questions about how an interface should behave.
   grep `posture`, `dialog`, `navigation`, `excise`, `affordance`, `feedback`.

2. `references/local-only/Practical_UI.txt`
   Best for applied visual logic: visual hierarchy, spacing, typography, form
   design, label clarity, accessibility, and disabled state handling.
   Start here for questions about how a surface should look and read.
   grep `visual hierarchy`, `spacing`, `form`, `label`, `accessibility`, `disabled`.

3. `references/local-only/Refactoring_UI.txt`
   Best as a concise visual tactics reference: spacing rhythm, color, contrast,
   shadow, depth, and emphasis through size and weight. Rated partial because it
   is short and focused on visual polish; it is thin on interaction and flow.
   Use as a finishing-layer reference after hierarchy and interaction are sound.
   grep `spacing`, `color`, `contrast`, `shadow`, `hierarchy`.

## Practical mapping

- For interaction questions (dialogs, flow, affordances, feedback): start with `About_Face.txt`.
- For visual-logic questions (hierarchy, spacing, forms, accessibility): start with `Practical_UI.txt`.
- For visual polish (color, contrast, spacing rhythm, depth): start with `Refactoring_UI.txt`.
- Where the survey marks coverage thin (empty/loading states, framework-specific APIs),
  route to [design_books.md](design_books.md) and first-principles UX reasoning instead.
