# Topic index

This is the routing front door. Start here, match the user problem to a row,
then open the named guide or local book. Book paths are bare text; grep the named
file for the listed keyword to find the passage. Derived from [reference_survey.md](reference_survey.md).

## Problem routing table

| User problem / trigger | UX task | Primary guide | Section |
| --- | --- | --- | --- |
| Onboarding or first-run: screen is empty and user does not know where to start | Empty state design | [ui_ux_review.md](ui_ux_review.md) | State coverage |
| Dense data-entry form with inline validation, error messages, and required fields | Form validation and error design | [ui_ux_review.md](ui_ux_review.md) | Validation and errors |
| Error or failure states: network down, permission denied, resource not found | Error and failure state design | [ui_ux_review.md](ui_ux_review.md) | State coverage |
| Responsive or multi-viewport layout: content breaks at narrow widths or feels unbalanced | Grid, spacing, and responsive layout | [design_books.md](design_books.md) | Grid Systems in Graphic Design; Refactoring UI |
| Accessibility review: keyboard reachability, screen-reader labels, color contrast | WCAG 2.1 AA audit and keyboard flow | [ui_ux_review.md](ui_ux_review.md) | Accessibility and keyboard support |
| List or table with search, filter, and sort: interactions feel inconsistent or slow | Interaction quality on structured data | [ui_ux_review.md](ui_ux_review.md) | Interaction quality |

## Per-topic detail

### Visual hierarchy and emphasis

Establish a clear reading order before adding decoration. Use spacing and grouping
as primary tools, size and weight as secondary emphasis, and color only to reinforce
hierarchy already established in layout. Read [ui_ux_review.md](ui_ux_review.md) for
the full hierarchy checklist.
Books: `references/local-only/Practical_UI.txt` (grep `visual hierarchy`, `spacing`),
`references/local-only/Refactoring_UI.txt` (grep `hierarchy`, `weight`, `size`).

### Interaction quality and affordances

Every interactive control must communicate its purpose without a label in the best
case, and with a clear label in every case. Give immediate feedback for user actions.
Remove any step that exists only to serve the system, not the user (excise). Reserve
modals for short, focused confirmations.
Book: `references/local-only/About_Face.txt` (grep `affordance`, `feedback`, `excise`).

### State coverage

Design all reachable states explicitly: empty (no data yet), loading (data in flight),
error (something went wrong with a recovery path), success, disabled, and offline.
States that are not designed look broken by default.
Books: `references/local-only/About_Face.txt` (grep `feedback`, `dialog`),
`references/local-only/Practical_UI.txt` (grep `disabled`, `accessibility`).

### Navigation and flow

Set the window or page posture to match the task (sovereign for sustained work,
transient for quick confirmations, daemon for background work). Expose commands
consistently through menus or toolbars. Route multi-step work through a wizard or
stepped layout. Measure excise: count every navigation step that does not advance
the user goal, then remove it.
Book: `references/local-only/About_Face.txt` (grep `navigation`, `posture`, `excise`, `wizard`).

### Accessibility

Check in this order: color contrast (WCAG AA minimum), explicit accessible names for
every interactive control, logical tab order, keyboard operability without a mouse,
and no focus traps. Verify disabled controls communicate why they are disabled.
Book: `references/local-only/Practical_UI.txt` (grep `accessibility`, `contrast`, `label`, `disabled`).

### Form design

Keep forms as short as possible. Every field needs an explicit label (not just a
placeholder). Show inline validation errors with a recovery path. Design the submit
button as the visually dominant action. Make clear why a submit is disabled when it
is. After submission, confirm success explicitly.
Books: `references/local-only/Practical_UI.txt` (grep `form`, `label`, `disabled`),
`references/local-only/About_Face.txt` (grep `affordance`, `feedback`).

## Alias and trigger vocabulary

- Visual clutter: too busy, cramped, hard to scan, no hierarchy, everything looks the same.
- Affordance: button not obvious, icon unclear, no hover state, ambiguous control.
- Excise: unnecessary click, extra screen, redundant confirmation, forced navigation.
- State: empty state, loading spinner, error message, success toast, offline banner.
- Accessibility: screen reader, keyboard navigation, WCAG, contrast ratio, tab order, ARIA label.
- Form: input, label, placeholder, validation, error message, required, disabled submit.

## Book source map (which book for this problem)

- Interaction design, dialogs, flow, navigation: `references/local-only/About_Face.txt`
  (grep `posture`, `dialog`, `navigation`, `excise`, `affordance`).
- Visual hierarchy, spacing, forms, accessibility: `references/local-only/Practical_UI.txt`
  (grep `visual hierarchy`, `spacing`, `form`, `label`, `accessibility`).
- Visual polish tactics, color, typography refinement: `references/local-only/Refactoring_UI.txt`
  (grep `spacing`, `color`, `contrast`, `shadow`).
- Where coverage is thin (empty/loading states, framework APIs, advanced accessibility),
  route to [design_books.md](design_books.md) and first-principles UX reasoning.
