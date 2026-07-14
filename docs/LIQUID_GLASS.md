# Liquid Glass Guidance for macOS 26+ SwiftUI Apps

Liquid Glass should be treated as the default macOS 26 visual language, not as an optional decorative layer. The best way to get strong Liquid Glass adoption is to use standard SwiftUI components first, then add custom glass only where the interface needs a deliberate control, navigation, or transient surface. SwiftUI is the implementation layer for all new UI in this repo family; treat AppKit as deprecated, reached only through narrow legacy bridges (see section 9).

This doc exists to help a manager get Liquid Glass right: sections 1-10 guide design decisions
before work is dispatched, sections 11-13 verify and debug the result, and section 14 is the
short version.

## Table of contents

Design the interface (read before dispatching UI work):

- [1. Use system components first](#1-use-system-components-first)
- [2. Use Liquid Glass for controls and navigation](#2-use-liquid-glass-for-controls-and-navigation)
- [3. Keep content readable](#3-keep-content-readable)
- [4. Separate content, control, and navigation layers](#4-separate-content-control-and-navigation-layers)
- [5. Use custom Liquid Glass deliberately](#5-use-custom-liquid-glass-deliberately)
- [6. Preserve native macOS behavior](#6-preserve-native-macos-behavior)
- [7. Design toolbars and menus for glass](#7-design-toolbars-and-menus-for-glass) -- macOS 27
  uniform frosted toolbar, system-owned chrome, user transparency slider
- [8. Check accessibility early](#8-check-accessibility-early)
- [9. Treat AppKit bridges as legacy escape hatches](#9-treat-appkit-bridges-as-legacy-escape-hatches)
- [10. Review custom UI against a simple test](#10-review-custom-ui-against-a-simple-test)

Verify and debug the result (read before accepting screenshots as evidence):

- [11. Verify the glass with visual evidence](#11-verify-the-glass-with-visual-evidence) --
  capture-path hazards, evidence protocol, flat-glass checklist, expected-appearance matrix,
  paste-able dispatch brief
- [12. Subtle gotchas: layers and colors](#12-subtle-gotchas-layers-and-colors) -- z-order,
  glass on glass, sampling path, shape defaults, adaptive opacity
- [13. Guarantee contrast over glass](#13-guarantee-contrast-over-glass) -- accessibility
  flags, scrims, vibrancy, multi-backdrop contrast audits

Summary:

- [14. Compact rule set](#14-compact-rule-set)

## 1. Use system components first

Apple's Liquid Glass guidance says standard framework components such as controls and navigation elements adopt the new appearance and behavior automatically.[^liquid-glass] Apple's adoption guidance also says apps using standard framework components pick up the latest look and feel when built with the latest SDKs and run on the latest platforms.[^adopting-liquid-glass] Build all new UI with standard SwiftUI components so this adoption is automatic.

Prefer standard system UI for:

- Windows and scenes
- Toolbars
- Sidebars
- Split views
- Sheets
- Popovers
- Menus
- Search fields
- Buttons
- Toggles
- Pickers
- Sliders
- Segmented controls
- Inspectors
- Alerts

Good rule:

> Maximize Liquid Glass adoption by maximizing standard system UI.

## 2. Use Liquid Glass for controls and navigation

Apple describes Liquid Glass as a dynamic material that combines the optical qualities of glass with a sense of fluidity. It reflects and refracts its surroundings and helps bring focus to underlying content.[^liquid-glass][^meet-liquid-glass]

Use Liquid Glass most aggressively on:

- Toolbars
- Navigation controls
- Floating controls
- Inspectors
- Search and filter controls
- Popovers
- Sheets
- Menus
- Selection controls
- Mode controls
- Transient overlays

Use quieter, more stable surfaces for:

- Dense text
- Long-form documents
- Code editors
- Tables
- Scientific figures
- Charts
- Reading panes
- Data-heavy views
- Primary content canvases

Good rule:

> Controls can be glassy. Content should stay legible.

## 3. Keep content readable

Liquid Glass should clarify hierarchy without making the app harder to use. It should not turn the content layer into decoration.

Use Liquid Glass to express:

- Navigation
- Control grouping
- Mode changes
- Transient actions
- Selection state
- Tool availability
- Interface depth

Avoid using Liquid Glass as:

- A general background texture
- A replacement for layout hierarchy
- A styling pass over every surface
- A way to hide weak information architecture
- A treatment for dense reading or editing areas

Good rule:

> Build the hierarchy first. Let Liquid Glass express the hierarchy.

## 4. Separate content, control, and navigation layers

A good macOS 26 layout usually separates visual responsibility:

```text
window and scene structure
  sidebar / navigation / document tabs where appropriate

control layer
  toolbar, search, filters, view mode, inspectors, transient actions

content layer
  text, tables, editors, diagrams, media, scientific data, documents
```

Liquid Glass belongs mostly in the control layer and selected navigation surfaces. The content layer should remain calm, readable, and predictable.

## 5. Use custom Liquid Glass deliberately

Apple documents SwiftUI APIs for applying Liquid Glass to custom interface elements and animations. Standard components already use Liquid Glass, while custom components can adopt glass effects to move, combine, and morph with unique transitions.[^custom-liquid-glass]

Custom Liquid Glass is appropriate for:

- Custom tool palettes
- Floating control groups
- Transient overlays
- Small navigation affordances
- Mode selectors
- Inspector controls
- Selection controls
- Custom controls that need to feel system-native

Custom Liquid Glass is usually not appropriate for:

- Full-window backgrounds
- Large text regions
- Dense tables
- Code or prose editors
- Scientific data displays
- Decorative cards with no interaction role

Good rule:

> Custom glass should explain interaction. It should not merely announce style.

## 6. Preserve native macOS behavior

Liquid Glass should support native Mac behavior, not replace it.

A modern macOS app should still respect:

- Menu bar commands
- Keyboard shortcuts
- Focus rings
- Toolbar conventions
- Multi-window workflows
- Document behavior
- File drag and drop
- Undo and redo
- Resizable windows
- Accessibility settings
- Light mode and dark mode
- High contrast
- Reduced transparency
- Reduced motion

Apple's macOS design guidance emphasizes the Mac as a powerful, spacious, flexible platform where people often use several apps at once.[^designing-for-macos]

Good rule:

> Liquid Glass should make the app feel more native, not more custom.

## 7. Design toolbars and menus for glass

Liquid Glass chrome evolves year over year, and Apple retunes it at the OS
level: macOS 26 (Tahoe) shipped floating, separated toolbar controls, and
macOS 27 (Golden Gate) replaces them with a uniform frosted toolbar across the
top of the app for better legibility and control visibility, standardizes
window corner radius, returns sidebars from floating panels to edge-to-edge
layouts, adds a system-wide transparency slider (ultra clear to fully tinted),
and diffuses complex content behind glass more aggressively with darkened
edges and brighter specular highlights.[^golden-gate-glass]

The design consequence: system chrome belongs to the system.

- Build toolbars with the standard SwiftUI `.toolbar { ToolbarItem(...) }`
  API and let the system draw the toolbar material. Apps on standard
  components inherit each year's retuning (floating in 26, uniform frosted in
  27) with no code change.
- Toolbar quality is best-practices work, not API work; adoption is
  automatic and the craft is in grouping, symbols, and restraint:
  - Grouping is meaning. Items sharing a glass group read as related
    actions; split semantic clusters with a fixed `ToolbarSpacer` and push
    groups apart with a flexible one. Navigation controls together, view
    modes together, confirmatory actions ("Done", "Save") apart. Fewer,
    well-grouped items beat many flat ones; overflow belongs in menus.
  - Symbols first, consistently. Use SF Symbol items built as `Label`s (the
    text serves accessibility and customization even when hidden); keep icon
    versus text consistent within the bar, with text reserved for
    confirmatory placements.
  - Placement drives prominence. Rely on `ToolbarItemPlacement`
    (`.confirmationAction` gets the prominent glass treatment
    automatically); tint at most one action per bar, via
    `.buttonStyle(.glassProminent)` so the tint covers the whole button; use
    badges with the same restraint; otherwise trust the defaults.
  - Tune where content meets the bar with `.scrollEdgeEffectStyle(_:for:)`:
    `.hard` for a discrete edge over tables, editors, and dense data,
    `.soft` for immersive content, `.automatic` otherwise.
  - Apple's worked example is the "Landmarks: Refining the system provided
    Liquid Glass effect in toolbars" sample in the SwiftUI documentation.
- Keep custom `.glassEffect` surfaces out of the toolbar band and the menu
  bar; hand-rolled glass chrome freezes one year's look and drifts from the
  platform on every OS release.
- Build menus with the standard `Menu` and `commands` APIs; the system owns
  menu material and legibility treatment.
- Treat translucency as a user-controlled range, not a fixed design value:
  the macOS 27 Appearance slider lets users tune glass from ultra clear to
  fully tinted. This is one more reason contrast must be guaranteed by your
  layers (section 13), never tuned to one observed look.
- Evidence captures of toolbar or menu chrome should record the OS version
  alongside the appearance mode; the same standard code renders differently
  on 26 and 27 by design.

Good rule:

> Own your glass surfaces; rent the system's chrome. Toolbars and menus are rented.

## 8. Check accessibility early

Liquid Glass depends on translucency, depth, reflection, refraction, and motion. These can reduce usability if applied too broadly.

Check the interface in:

- Light mode
- Dark mode
- High contrast
- Increased contrast
- Reduced transparency
- Reduced motion
- VoiceOver
- Keyboard-only navigation
- Different window sizes
- Busy content backgrounds

If a glass surface harms readability, reduce the effect or move the effect to the control layer.

Good rule:

> Accessibility is part of the Liquid Glass design, not a cleanup pass.

## 9. Treat AppKit bridges as legacy escape hatches

SwiftUI is the implementation layer for all new UI, including every glass surface. Treat AppKit as deprecated: reach for an AppKit bridge only when SwiftUI cannot yet express the behavior (advanced text editing internals, low-level window behavior, responder-chain work), keep the bridge narrow, and plan to remove it when SwiftUI catches up.

When a bridge exists, SwiftUI still owns the Liquid Glass styling. Do not split visual responsibility across both layers.

Good pattern:

```text
SwiftUI feature
  owns state and app structure

SwiftUI glass/control wrapper
  owns visual system integration

AppKit adapter (legacy escape hatch)
  owns only the behavior SwiftUI cannot yet express
```

## 10. Review custom UI against a simple test

Before adding custom Liquid Glass, ask:

1. Is this surface a control, navigation element, or transient interface layer?
2. Does glass clarify hierarchy or interaction?
3. Does the content remain readable behind it?
4. Does the effect behave well in light and dark mode?
5. Does the interface still work with reduced transparency and reduced motion?
6. Would a standard system component solve this better?

If the answer to the last question is yes, use the standard component.

## 11. Verify the glass with visual evidence

Liquid Glass fails silently. The code compiles, the app runs, and a missing precondition (old
SDK, opaque backing, reduced transparency, empty backdrop) degrades the effect to a flat fill
that looks plausible in a screenshot. Never claim glass works without visual evidence that shows
the backdrop-sampling behavior itself.

### Why screenshots can lie

Glass is a backdrop-sampling effect: it blurs, refracts, and tints whatever renders behind
it.[^meet-liquid-glass] Two capture hazards follow:

- Offscreen and cached render paths (`cacheDisplay(in:to:)`,
  `bitmapImageRepForCachingDisplay(in:)`, SwiftUI `ImageRenderer`) can render the view tree in
  isolation, without live backdrop compositing. Glass regions come out flat gray even when the
  on-screen app is correct. Validate the capture path before trusting any capture: render one
  known-glass view and one flat control through it, and if they look the same, switch to a real
  on-screen capture (`screencapture -l <window-id>`) of the live window.
- A backdrop with no contrast produces no visible effect. Over an empty white document, glass
  has nothing to sample; the capture is indistinguishable from a flat fill even when glass is
  live.

### Evidence protocol

1. Put strong multi-color content behind the glass surface -- a gradient, a photo, or
   syntax-highlighted text that reaches under the glass edges.
2. Capture the live window on screen. The glass region must show blurred, refracted color from
   the content behind it, not a uniform fill.
3. Differential proof: capture once normally, once with Reduce Transparency enabled. The
   reduced capture must be visibly more opaque. A difference between the two proves the effect
   responds to system state; identical captures mean flat fill.
4. Side-by-side control: render the same layout with `.regularMaterial` or an opaque fill in
   place of glass. If the glass capture is indistinguishable from the control, glass is not
   rendering.
5. Scroll or move the content behind the glass and capture again; the glass region must change
   with the content.
6. Repeat in light and dark mode, and label each capture with the actual appearance mode it ran
   in (query the effective appearance at capture time rather than trusting the launch setting).

### Checklist when glass looks flat

1. Built with the macOS 26 SDK, and the `#available(macOS 26.0, *)` branch actually taken?
2. Info.plist compatibility opt-out (`UIDesignRequiresCompatibility`) absent or false?
3. System Settings > Accessibility > Display > Reduce Transparency off on the test machine?
4. Anything with visual contrast actually behind the glass?
5. Any opaque `.background(...)` between the glass and the content behind it?
6. Capture path compositing the live backdrop, not an offscreen cache?

### What correct glass looks like

Judge a capture against the backdrop it was taken over. Glass adapts to the backdrop by
design, so the same correct code produces every row below.

| Backdrop behind glass | Correct appearance |
| --- | --- |
| Plain white | Nearly invisible; faint edge highlight only. Expected, not a bug. |
| Plain black | Barely visible; subtle rim light. Expected, not a bug. |
| Mid-tone gradient | Blurred, refracted color inside the shape; edges bend the backdrop. Best judging backdrop. |
| Busy photo or text | Visibly tinted and more opaque; backdrop shapes muted but present (the material raises its own opacity for legibility). |
| Reduce Transparency on | Flat opaque fill, no sampling. Expected under that setting; use it as the differential proof. |

A capture can only prove glass on the two middle rows. Over plain white or black, a correct
implementation and a broken one look the same.

### Paste-able evidence brief for dispatch

Copy this into the subagent brief when dispatching glass work, filling in the surface:

```text
Build <surface> with .glassEffect targeting macOS 26.
Return these captures with the result:
1. On-screen capture (screencapture -l <window-id>) of the live window, with
   multi-color content reaching under the glass edges.
2. The same view with Reduce Transparency enabled; it must be visibly more
   opaque than capture 1.
3. The same layout with .regularMaterial in place of glass; it must look
   different from capture 1.
4. Light and dark captures, each labeled with the effective appearance
   queried at capture time and the OS version (glass chrome renders
   differently on macOS 26 and 27 by design).
SHIP when the glass region visibly blurs and refracts the backdrop and all
text over glass measures at least 4.5:1 (3:1 for text 18pt and larger).
REWORK when the glass region reads as a flat panel, or when any pair of
captures above is pixel-identical.
```

Good rule:

> A screenshot proves glass only when the glass region visibly samples what is behind it.

## 12. Subtle gotchas: layers and colors

Glass samples the content layer behind it, so layer order and color choices decide whether the
effect is visible at all.[^applying-liquid-glass]

The sampling path, bottom to top -- keep it clear of opaque layers:

```text
vibrant label             .foregroundStyle(.primary) -- adapts with the material
glass surface             .glassEffect(...) -- samples everything below it
(keep this gap clear)     an opaque .background(...) here blocks sampling
content layer             gradient, photo, document, editor -- what glass refracts
```

Layer gotchas:

- Glass must sit above content in z-order (overlay or `ZStack`) with real content underneath.
  Glass with nothing behind it refracts nothing and reads as an empty gray panel.
- Keep glass off glass. Glass samples the content layer; a glass surface stacked over another
  glass surface muddies both and defeats the depth cue the material exists to provide.
- An opaque background anywhere between the glass and the content blocks sampling. Modifier
  order matters: an opaque `.background(...)` wrapped around a glass element removes the
  translucency it was meant to show.
- Group nearby custom glass shapes in one `GlassEffectContainer` so they sample consistently
  and can merge; use `glassEffectID(_:in:)` with `@Namespace` for morph transitions.
- `.glassEffect()` defaults to a capsule shape; pass `in: .rect(cornerRadius:)` or another
  shape for anything that is not a pill.

Color gotchas:

- Glass has no fixed color. It switches between light and dark treatment based on the luminance
  of the content behind it, so a hardcoded foreground color that reads well over one backdrop
  fails over another. Use semantic styles (`.foregroundStyle(.primary)`, `.secondary`) so
  vibrancy adapts with the material.
- `.tint(...)` on glass modulates the sampled backdrop rather than painting a flat color; a
  tinted glass control shifts hue over busy content. Verify tint over both light and dark
  backdrops before shipping it.
- Pure white or pure black test backdrops hide most of the effect. Judge glass over mid-tone,
  multi-color content.
- Glass self-adjusts its own opacity with the backdrop: it turns more opaque over busy content
  such as text (to keep foreground elements readable) and more transparent over plain
  backgrounds. Identical glass code looks different across backdrops by design; compare
  captures against the same backdrop, and treat cross-backdrop variation as expected behavior,
  not a rendering bug.
- Add `.interactive()` to custom glass controls the user clicks or touches so the material
  responds the way system controls do.

Minimal harness for evidence captures:

```swift
// Verification harness: the glass region must show blurred,
// refracted gradient color, not a uniform fill.
struct GlassEvidenceView: View {
	var body: some View {
		ZStack {
			LinearGradient(
				colors: [.orange, .purple, .teal],
				startPoint: .topLeading,
				endPoint: .bottomTrailing
			)
			.ignoresSafeArea()
			Text("Liquid Glass")
				.padding(24)
				.glassEffect(.regular, in: .rect(cornerRadius: 16))
		}
	}
}
```

## 13. Guarantee contrast over glass

Glass is a real-time compositing layer: it samples the pixels behind it, blurs them, adjusts
saturation, and overlays the control. Text contrast over glass therefore shifts with whatever
the user puts behind it. The material guarantees no minimum contrast. White text over glass can
pass WCAG AAA over a dark backdrop and drop below 2:1 over a bright photo. A layout that looks
fine over the default test backdrop can fail badly over real user content.

Layered fixes that hold regardless of backdrop:

1. Read `@Environment(\.accessibilityReduceTransparency)`. When true, replace glass surfaces
   with opaque fills. This is the single highest-value fix: it honors every user who already
   told the system they need it. (A legacy AppKit bridge can check
   `NSWorkspace.shared.accessibilityDisplayShouldReduceTransparency`.)
2. Read `@Environment(\.colorSchemeContrast)`. When `.increased`, switch labels to full-alpha
   semantic colors and drop custom tints over glass.
3. Add a text protection scrim when the contrast flags are off and the backdrop is
   uncontrolled: a black fill at 40 percent opacity under white text guarantees roughly 4.6:1
   over any backdrop.
4. Use vibrancy for secondary labels only. Vibrancy adapts luminance against the blurred
   region; primary labels need full-opacity semantic color, not vibrancy.
5. Judge contrast over multiple backdrops, not one: a near-white backdrop, a bright photo, and
   a mid-tone gradient. Two of the three are the common failure cases.
6. Audit captured screenshots with a contrast checker (for example TPGi Colour Contrast
   Analyser): eyedrop the text and the glass region behind it. Below 4.5:1 for normal text, or
   3:1 for large text, is a bug, not a design decision.

Good rule:

> The backdrop is user-controlled, so contrast over glass must be guaranteed by your layers,
> not observed on one lucky screenshot.

## 14. Compact rule set

Use this as the short version:

- Use standard SwiftUI components first; treat AppKit as deprecated.
- Let toolbars, sidebars, sheets, popovers, menus, and controls inherit Liquid Glass.
- Add custom glass only to controls, navigation, and transient overlays.
- Keep dense content stable and readable.
- Preserve native macOS behavior.
- Test accessibility modes early.
- Keep AppKit bridges narrow legacy escape hatches; SwiftUI owns glass styling.
- Treat glass as hierarchy, not decoration.
- Verify glass with on-screen captures over colorful content; offscreen render paths and empty
  backdrops both hide the effect.
- Keep the sampling path clear: no glass on glass, no opaque backgrounds between glass and
  content.
- Guarantee text contrast with reduce-transparency and increased-contrast checks plus scrims;
  never trust contrast measured over one backdrop.
- Build toolbars and menus with standard APIs; the system retunes that chrome every OS release
  (floating in macOS 26, uniform frosted in 27).

## References

[^liquid-glass]: Apple Developer Documentation, "Liquid Glass." https://developer.apple.com/documentation/technologyoverviews/liquid-glass
[^adopting-liquid-glass]: Apple Developer Documentation, "Adopting Liquid Glass." https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass
[^meet-liquid-glass]: Apple Developer, WWDC25, "Meet Liquid Glass." https://developer.apple.com/videos/play/wwdc2025/219/
[^custom-liquid-glass]: Apple Developer, WWDC25, "Explore custom Liquid Glass with SwiftUI." https://developer.apple.com/videos/play/wwdc2025/284/
[^applying-liquid-glass]: Apple Developer Documentation, "Applying Liquid Glass to custom views." https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views
[^designing-for-macos]: Apple Developer Documentation, "Designing for macOS." https://developer.apple.com/design/human-interface-guidelines/designing-for-macos
[^golden-gate-glass]: MacRumors, "All the Liquid Glass Changes in macOS Golden Gate." https://www.macrumors.com/2026/06/09/macos-golden-gate-liquid-glass/
