---
name: glass-expert
description: 'Design, implement, verify, and debug Apple Liquid Glass in SwiftUI on macOS 26+ and iOS 26. Use for `.glassEffect`, morphing, backdrop sampling, flat or invisible glass, on-screen capture proof, surface placement, and accessible contrast.'
---

# Liquid Glass Expert

## Overview

Use this skill to get Liquid Glass demonstrably correct in SwiftUI apps on
macOS 26+ (and iOS 26). Glass is a backdrop-sampling material: it blurs,
refracts, and tints whatever renders behind it, adapts its own opacity to the
backdrop, and guarantees no minimum text contrast. Most failures are silent --
the code compiles and a capture looks plausible while the effect is absent or
illegible. This skill turns "add glass" into layered implementation plus
visual evidence: a correct sampling path, colors that stay legible, and
captures that prove the effect is live.

SwiftUI is the implementation layer; treat AppKit as a legacy escape hatch
reached only when SwiftUI cannot yet express the behavior.

## When to use

- Implement custom glass (`.glassEffect`, `GlassEffectContainer`, morphing).
- Debug glass that renders flat, gray, invisible, or unexpectedly opaque.
- Prove with captures that glass is live before accepting work as done.
- Decide which surfaces should be glass and which stay stable content.
- Guarantee text contrast over glass across arbitrary backdrops.
- Review or harden an existing app's glass adoption.

## When not to use

- Web glassmorphism (CSS `backdrop-filter`); this skill is SwiftUI-specific.
- App-icon glass (Icon Composer layered icons); a different pipeline.
- General SwiftUI layout or state questions with no glass involvement.

## Workflow

1. Frame the project shape. When invoked on a target app, decide greenfield
   versus improve-existing and follow the matching workflow in
   [`references/project_workflow.md`](references/project_workflow.md). Skip
   this step for a one-off question with no target repo.
2. Classify the task (placement, implementation, verification, debugging, or
   contrast) using
   [`references/task_selection.md`](references/task_selection.md).
3. For an observed problem ("glass looks flat", "text unreadable"), start at
   the symptom router
   [`references/topic_index.md`](references/topic_index.md).
4. Open the one matching reference from the routing table below.
5. Implement with the seed views in `assets/` (see
   [`references/component_seeds.md`](references/component_seeds.md)) when the
   surface carries text or needs accessibility fallbacks.
6. Prove the result with the evidence protocol in
   [`references/testing_and_oracles.md`](references/testing_and_oracles.md),
   using the capture and comparison tools in `scripts/`. Ship only on visual
   evidence, never on compiling code.

## Routing table

| Look for | Reference |
| --- | --- |
| What should be glass, control vs content layer, hierarchy, system components first | [`references/design_placement.md`](references/design_placement.md) |
| Toolbar design, action grouping, `ToolbarSpacer`, symbols vs text, prominence, tint restraint, scroll edge style | [`references/toolbar_best_practices.md`](references/toolbar_best_practices.md) |
| z-order, sampling path, glass on glass, opaque background blocking, `GlassEffectContainer`, morphing, default capsule shape | [`references/layers_and_sampling.md`](references/layers_and_sampling.md) |
| tint, vibrancy, semantic colors, adaptive opacity, contrast over glass, scrims, Reduce Transparency, Increase Contrast, WCAG ratios | [`references/color_and_contrast.md`](references/color_and_contrast.md) |
| screenshots, `screencapture`, `cacheDisplay`, `ImageRenderer`, offscreen render, appearance labeling, window ids | [`references/capture_paths.md`](references/capture_paths.md) |
| evidence protocol, differential proof, expected appearance per backdrop, SHIP/REWORK criteria, dispatch brief | [`references/testing_and_oracles.md`](references/testing_and_oracles.md) |
| `GlassSurface` wrapper, `GlassEvidenceView` harness, seed code to copy | [`references/component_seeds.md`](references/component_seeds.md) |
| API names, availability, `#available`, Info.plist compatibility key, `buttonStyle(.glass)` | [`references/api_quick_reference.md`](references/api_quick_reference.md) |
| Refreshing or auditing this skill itself: new OS release, WWDC cycle, HIG update, stale facts | [`references/skill_maintenance.md`](references/skill_maintenance.md) |

## Bundled tools

- `scripts/list_window_ids.swift`: print on-screen window ids for an app so
  `screencapture -l` can grab the live composited window.
- `scripts/capture_glass_evidence.sh`: capture a window by id and label the
  file with the appearance mode and Reduce Transparency state at capture time.
- `scripts/compare_captures.py`: pixel-compare two captures and print a
  DIFFERENT / IDENTICAL verdict for the differential proof.
- `assets/GlassSurface.swift`: drop-in glass surface with accessibility
  fallbacks and an optional contrast scrim.
- `assets/GlassEvidenceView.swift`: harness rendering glass next to a flat
  material control over a gradient, so one capture proves the effect.

## Quality bar

- Every glass surface ships with visual evidence per the evidence protocol.
- Text over glass measures at least 4.5:1 (3:1 at 18pt and larger) on every
  tested backdrop.
- Reduce Transparency and Increase Contrast paths render opaque fallbacks.
- The sampling path stays clear: real content behind glass, no glass on
  glass, no opaque background between glass and content.

## Output expectations

A delegated invocation returns the code as a paste-ready block, the reference
file it is grounded in, the capture set proving the effect (or the exact
captures still required), and any contrast risk with a one-line scope
assessment.
