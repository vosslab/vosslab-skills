# Toolbar best practices

The glass toolbar is best-practices territory, not API work: adoption is
automatic, and quality comes from grouping, symbols, and restraint. The system
draws and retunes the toolbar surface (floating groups on macOS 26, one
uniform frosted bar on macOS 27); your job is to make the contents read
clearly. Apple's worked sample is "Landmarks: Refining the system provided
Liquid Glass effect in toolbars" in the SwiftUI documentation.

## Grouping is meaning

Toolbar grouping is a semantic signal, not a layout detail: items that share a
glass group read as related actions; a spacer between groups tells the user
"different role".

- Group by function and frequency: navigation controls together, view-mode
  controls together, primary confirmatory actions ("Done", "Save") apart.
- Split semantic clusters with `ToolbarSpacer` (fixed); use a flexible spacer
  to push groups apart across the bar.
- Custom items group separately from the system back button automatically;
  keep it that way rather than fighting the grouping.
- Fewer, well-grouped items beat many flat ones. A toolbar is for frequent
  actions; everything else belongs in menus.

## Symbols first, consistently

- Prefer symbol-based items (SF Symbols); the glass toolbar is designed
  around monochrome symbols and reads cleanest with them.
- Keep icon versus text consistent within the bar: mixing text-labeled and
  symbol-only buttons side by side reduces clarity. Text is right for
  confirmatory actions; let placement handle that (below).
- Provide both image and text label on each button (`Label`), so
  accessibility, customization UI, and text-mode toolbars stay correct even
  when only the symbol shows.

## Placement drives prominence

- Rely on `ToolbarItemPlacement` for styling: `.confirmationAction` gets the
  prominent glass treatment automatically; `.destructiveAction`,
  `.cancellationAction`, and friends carry their own semantics.
- Tint sparingly -- at most one primary action per bar. When tinting, use
  `.buttonStyle(.glassProminent)` so the tint covers the whole button surface
  uniformly instead of coloring the symbol alone.
- Badges on toolbar items follow the same restraint rule: only for status the
  user must see.
- Trust the defaults. Manual styling overrides are how a toolbar freezes one
  year's look and drifts from the platform (see
  [design_placement.md](design_placement.md): rent the system's chrome).

## Where content meets the bar

- Content scrolls under the glass toolbar by design; the system keeps the bar
  legible (macOS 27 frosts it harder for exactly this reason).
- Tune the boundary with `.scrollEdgeEffectStyle(_:for:)`: `.hard` for a
  discrete edge over tables, editors, and dense data; `.soft` for immersive
  content; `.automatic` otherwise.
- Give the bar something real to sit over in evidence captures: a toolbar
  screenshotted over empty white proves nothing (see
  [testing_and_oracles.md](testing_and_oracles.md)); capture with
  syntax-highlighted or colorful content scrolled under the bar, labeled with
  the OS version, since 26 and 27 render the same code differently.

## Review questions

1. Does each glass group contain only related actions?
2. Could any toolbar item move to a menu without hurting frequent workflows?
3. Is at most one action tinted or prominent?
4. Are all items symbols with labels, with text reserved for confirmatory
   placements?
5. Does the scroll edge style match the content underneath (hard for dense
   data, soft for immersive)?
