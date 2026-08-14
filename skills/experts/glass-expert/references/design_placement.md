# Design placement

Decide which surfaces get glass before implementing any. Liquid Glass is the
default visual language on macOS 26+, expressed mostly through standard
components; custom glass is a deliberate exception for controls, navigation,
and transient surfaces.

## System components first

Standard SwiftUI components (toolbars, sidebars, sheets, popovers, menus,
search fields, buttons, pickers, segmented controls, inspectors, alerts) adopt
Liquid Glass automatically when built with the current SDK. Maximize glass
adoption by maximizing standard system UI. Custom glass is for surfaces the
system does not provide.

## Glass belongs to controls and navigation

Use glass on toolbars, navigation controls, floating control groups,
inspectors, search and filter controls, popovers, sheets, menus, selection and
mode controls, and transient overlays. Keep quieter, stable surfaces for dense
text, long documents, code editors, tables, charts, reading panes, and primary
content canvases. Controls can be glassy; content stays legible.

Layer separation:

```text
control layer      toolbar, search, filters, view mode, transient actions
content layer      text, tables, editors, media, documents (stays calm)
```

Glass lives in the control layer. Custom glass is usually wrong for
full-window backgrounds, large text regions, dense tables, editors, and
decorative cards with no interaction role.

## Toolbars and menus are rented chrome

Apple retunes system chrome every OS release: macOS 26 (Tahoe) shipped
floating, separated toolbar controls; macOS 27 (Golden Gate) replaces them
with a uniform frosted toolbar across the top of the app for legibility, plus
standardized window corner radius, edge-to-edge sidebars, and a system-wide
transparency slider (ultra clear to fully tinted).

- Build toolbars with standard `.toolbar { ToolbarItem(...) }` and menus with
  standard `Menu` / `commands` APIs; each year's retuning then applies with no
  code change. Toolbar quality is best-practices work, not API work: see
  [toolbar_best_practices.md](toolbar_best_practices.md) for grouping
  semantics, symbols-first items, placement-driven prominence, and scroll
  edge tuning.
- Keep custom `.glassEffect` out of the toolbar band and menu bar; hand-rolled
  glass chrome freezes one year's look and drifts from the platform yearly.
- Treat translucency as a user-controlled range (the macOS 27 slider), never
  a fixed design value; contrast must come from layers, not from one look.

Own your glass surfaces; rent the system's chrome.

## Review questions before adding custom glass

1. Is this surface a control, navigation element, or transient layer?
2. Does glass clarify hierarchy or interaction here?
3. Does the content behind it remain readable?
4. Does it behave in light mode, dark mode, and reduced transparency?
5. Would a standard system component solve this better? If yes, use it.

When placement is settled, implement via
[layers_and_sampling.md](layers_and_sampling.md) and the seeds in
[component_seeds.md](component_seeds.md).
