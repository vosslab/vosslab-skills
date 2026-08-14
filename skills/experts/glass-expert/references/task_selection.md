# Task selection

Classify a Liquid Glass request before opening a focused guide. Glass work
mixes design judgment, rendering mechanics, and evidence discipline; the first
job is to name which kind of task this is and what the backdrop situation is.

## Task dimensions

Answer these questions to frame the task:

- Task type: placement (what should be glass at all), implementation (build a
  custom glass surface), verification (prove the effect is live), debugging
  (glass renders flat, gray, or invisible), or contrast (text legibility over
  glass).
- Surface role: control, navigation, or transient overlay (glass candidates)
  versus dense content such as text, tables, editors, and figures (stays
  stable). System chrome (toolbars, menus) is rented from the OS and stays on
  standard APIs.
- Backdrop control: app-controlled backdrop (a known gradient or view) versus
  user-controlled content (photos, documents, arbitrary windows). User-controlled
  backdrops force the layered contrast strategy.
- Evidence status: does the claim "glass works" carry live on-screen captures,
  or only code and offscreen renders? Unverified glass is unproven glass.
- Platform path: SwiftUI (the implementation layer) versus a legacy AppKit
  bridge (an escape hatch used only when SwiftUI cannot express the behavior).

## Route by task type

- Placement or "should this be glass": [design_placement.md](design_placement.md).
- Implementation of a custom surface: [layers_and_sampling.md](layers_and_sampling.md)
  for the sampling path, then [component_seeds.md](component_seeds.md) for the
  seed views, then [api_quick_reference.md](api_quick_reference.md) for exact
  API shapes.
- Verification or acceptance of finished work:
  [testing_and_oracles.md](testing_and_oracles.md), with capture mechanics in
  [capture_paths.md](capture_paths.md).
- Debugging flat, gray, or invisible glass: start at the symptom router
  [topic_index.md](topic_index.md).
- Contrast or legibility over glass: [color_and_contrast.md](color_and_contrast.md).

## Red flags that reclassify the task

- "The screenshot looks fine" with no gradient or photo behind the glass:
  this is a verification task, not a done task; nothing over a plain backdrop
  proves glass.
- A capture produced by `cacheDisplay`, `bitmapImageRepForCachingDisplay`, or
  `ImageRenderer`: capture-path validation comes first; see
  [capture_paths.md](capture_paths.md).
- Hardcoded label colors over glass: a contrast task hiding inside an
  implementation task; see [color_and_contrast.md](color_and_contrast.md).
- Custom glass proposed for a toolbar, menu, or full-window background: a
  placement decision that routes to [design_placement.md](design_placement.md)
  before any implementation.
