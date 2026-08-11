# CSS project workflow

## Existing stylesheet

1. Locate the rendered route, stylesheet entry point, component ownership, asset
   pipeline, and existing visual or browser checks.
2. Inventory the cascade surface: layer order, custom properties, global rules,
   selectors with escalating specificity, `!important`, media/container queries,
   color-scheme rules, and motion preferences.
3. Capture baseline screenshots at the affected viewport sizes and schemes.
4. Write a visual contract, change the owning rule or token, and keep the diff
   narrow enough to attribute the rendered result.
5. Recheck long, empty, and translated content plus keyboard focus and reduced
   motion where relevant.

## Greenfield page

1. Define semantic regions and content hierarchy before visual effects.
2. Set a small token vocabulary for type, space, color roles, borders, and
   elevation; implement baseline mobile layout with grid or flexbox.
3. Add fluid sizing and responsive constraints, then a deliberate dark scheme
   and purposeful motion only where the content benefits.
4. Capture rendered evidence at narrow, typical, and wide viewports before
   extending the component set.

## Change boundaries

- Keep component-local rules local and document intentional global tokens.
- Confirm current browser support before deploying newer CSS features.
- Use [testing_and_oracles.md](testing_and_oracles.md) before calling a visual
  change complete.
