---
name: css-creative-expert
description: Design, implement, debug, and review polished CSS. Use for gradients, backgrounds, custom properties, color functions, animation, dark mode, grid, flexbox, anchor positioning, cascade layers, selectors, container queries, and responsive design.
---

# CSS creative expert

## Overview

Turn an imprecise request to improve a page into a small, rendered, maintainable
CSS change. Own visual craft, layout, responsive behavior, theming, motion, and
accessible color design. Route measured contrast audits and palette repair to
`color-accessibility-expert`; route interaction, task flow, and usability
judgment to `ui-ux-engineer`.

## Workflow

1. Classify the request and choose a visible outcome.
- Sort it into visual craft, layout, theming, or motion; name the audience,
  page state, viewport range, color scheme, and observable improvement.
- Read [references/task_selection.md](references/task_selection.md), then use
  [references/topic_index.md](references/topic_index.md) for the focused route.

2. Detect the target project shape and map its cascade surface.
- Existing stylesheet: inventory entry points, layers, custom properties,
  specificity hot spots, component boundaries, responsive breakpoints, and
  existing visual tests before editing.
- Greenfield page: establish content hierarchy, semantic HTML, a token system,
  baseline layout, narrow-screen behavior, and one coherent visual direction.
- Read [references/project_workflow.md](references/project_workflow.md).

3. Establish the visual and structural contract.
- State the content hierarchy, layout primitive, width and overflow behavior,
  color-role intent, motion purpose, reduced-motion behavior, and target
  viewports. Keep design tokens and component rules legible in the cascade.
- Prefer a focused change that preserves the page's purpose over a generic
  restyle. Select the relevant source and verification move from
  [references/topic_index.md](references/topic_index.md).

4. Consult current evidence before version-sensitive CSS.
- Use [references/local_books.md](references/local_books.md) and the verified
  passages in [references/reference_survey.md](references/reference_survey.md)
  when the local corpus exists. Read the surrounding text together with each
  grep match.
- For thin coverage, newer syntax, browser support, or implementation details,
  confirm current behavior in MDN and the relevant CSS specification.

5. Implement one coherent CSS slice.
- Use grid or flexbox for page geometry, intrinsic sizing and logical properties
  where appropriate, and custom properties for repeated values and themes.
- Keep selectors scoped, specificity intentional, fallbacks explicit, and
  transitions purposeful. Respect `prefers-reduced-motion`; use motion to
  clarify content and essential controls.
- Keep color roles distinguishable and readable; send numerical contrast
  measurement and any resulting repair workflow to `color-accessibility-expert`.

6. Validate the rendered behavior and refine.
- Compare screenshots across required viewport sizes and light/dark schemes;
  run a focused Playwright pass when the target serves HTML.
- Inspect computed styles for the contract's critical rules and use the
  appropriate oracle in [references/testing_and_oracles.md](references/testing_and_oracles.md).

## Implementation defaults

- Start from semantic document structure and content hierarchy; let CSS express
  layout and presentation instead of compensating for missing structure.
- Use a small token vocabulary for color, spacing, type, radius, and elevation;
  define themes through custom properties and consolidate repeated overrides.
- Prefer fluid constraints (`minmax()`, `clamp()`, intrinsic sizing, container
  queries) before accumulating viewport-specific exceptions.
- Use cascade layers to make reset, base, component, utility, and override
  precedence visible when the target's scale warrants them.
- Make dark mode an intentional color-role design, then delegate measured
  contrast verification to `color-accessibility-expert`.
- Use animation to explain state change or spatial continuity, honor reduced
  motion, and validate performance on representative content.

## Quality bar

- Preserve content meaning, keyboard reachability, source order, and readable
  zoom behavior while improving the rendered result.
- Make responsive behavior work at intermediate and named device widths.
- Keep cascade priority explicit, content height fluid, and decorative effects
  subordinate to readability.
- Compare light and dark schemes, normal and reduced motion, empty and long
  content, and the layout's narrowest supported viewport.
- Use current primary documentation for browser support and new CSS features.

## Output expectations

When using this skill, produce:

- A concise visual contract, target files, cascade-surface inventory, and route.
- A file- and selector-specific CSS implementation or recommendation.
- Screenshot, computed-style, and browser-test evidence for the changed states.
- A handoff to `color-accessibility-expert` for measured contrast repair or to
  `ui-ux-engineer` for interaction and usability decisions when applicable.
- A clear next step if browser support, brand direction, or target viewports
  require user confirmation.
