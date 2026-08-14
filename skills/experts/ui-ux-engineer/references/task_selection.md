# Task selection

Use this reference to classify a UI/UX request before consulting the topic index
or review guides.

## Surface type

Identify the primary surface type to scope the review:

- Form: data entry with labels, inputs, and a submit action (sign-up, checkout, settings edit).
- Dashboard: overview with aggregated metrics, charts, and status summaries.
- Modal or dialog: overlay that interrupts the current flow for a focused decision or confirmation.
- Wizard: sequential steps with progress, branching, and a completion state.
- List or table: structured rows with optional search, filter, and sort controls.
- Detail or profile view: single-entity expanded view (record, product, article, user profile).
- Settings or preferences: grouped controls to configure persistent behavior.
- Checkout or conversion flow: high-stakes transactional path with validation and confirmation.

## Primary user goal

Answer this before reviewing:

- What is the user trying to accomplish on this surface?
- What does success look like from the user's perspective?
- What information or action does the user arrive expecting to find?

Every element in the review should be judged against this goal. Elements that do not serve
the primary goal are candidates for removal, deprioritization, or restructuring.

## Edge states to design explicitly

Every surface must handle these states with an intentional layout:

- Empty: no data exists yet; guide the user toward the first action.
- Loading: data is being fetched; indicate progress and whether the surface is still responsive.
- Error: a request failed or an action could not complete; preserve context and offer recovery.
- Success: action completed; confirm the outcome without blocking next steps.
- Offline: network is unavailable; show what is still usable.
- Permission-denied: user lacks access; explain why and what they can do instead.

## Accessibility scope

Determine which dimensions apply before the review begins:

- Keyboard navigation: all primary actions reachable without a pointer; tab order matches
  reading and task order.
- Screen reader: semantic labels on all interactive controls; no icon-only buttons without
  accessible names; live regions announce state changes.
- Contrast: text meets WCAG 2.1 AA (4.5:1 for normal text, 3:1 for large text); icons and
  focus indicators meet 3:1.
- Touch targets: interactive elements meet a 44x44 px minimum touch-target size.
- Cognitive load: instructions are short and close to the action; error messages name the
  problem and the fix; one primary action per screen.

## Task dimensions summary

Before routing to the topic index, answer these:

- Surface type: which of the eight surface types above best matches?
- Primary goal: what is the user trying to accomplish?
- Edge states required: which of the six edge states must be explicitly designed?
- Accessibility scope: which dimensions apply (keyboard, screen reader, contrast, touch, cognitive)?
- Failure mode: what breaks when UX quality is low (lost data, failed task, confused user,
  inaccessible flow)?
