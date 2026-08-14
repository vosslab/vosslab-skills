# API quick reference

The SwiftUI Liquid Glass surface, introduced at WWDC25 (macOS 26 / iOS 26 SDK)
and carried forward in the OS 27 cycle. The OS 27 retuning (uniform toolbar,
transparency slider, stronger diffusion) applies through the system with the
same APIs; SwiftUI apps pick it up by rebuilding against the current SDK.

## Core APIs

| API | What it does |
| --- | --- |
| `.glassEffect(_:in:)` | Applies glass to a custom view. Defaults to `.regular` glass in a capsule; pass `in: .rect(cornerRadius:)` for other shapes. |
| `Glass.regular` | The standard material variant passed to `glassEffect`. |
| `.tint(_:)` on glass | Modulates the sampled backdrop toward a color; not a flat paint. |
| `.interactive()` | Makes a custom glass control respond to interaction like system controls. |
| `GlassEffectContainer(spacing:)` | Groups nearby glass shapes so they sample consistently, merge when close, and can morph. |
| `.glassEffectID(_:in:)` | Identity for morph transitions between glass shapes, with a `@Namespace`, inside one container. |
| `.buttonStyle(.glass)` / `.glassProminent` | Standard glass button styles. |

## Toolbar APIs

The macOS 27 uniform frosted toolbar applies automatically to standard
toolbars; these APIs organize and tune it. Apple's worked sample is
"Landmarks: Refining the system provided Liquid Glass effect in toolbars" in
the SwiftUI documentation.

| API | What it does |
| --- | --- |
| `.toolbar { ToolbarItem(...) }` | Standard toolbar; the system draws the glass surface and retunes it per OS release. |
| `ToolbarItemGroup` | Groups related actions into one glass grouping. |
| `ToolbarSpacer` (fixed or flexible) | Splits toolbar items into separate glass groups; flexible spacers expand between groups. Custom items group separately from the system back button when built with Xcode 26+. |
| `.scrollEdgeEffectStyle(_:for:)` | Tunes how scrolling content meets the bar per `Edge.Set`: `.automatic`, `.hard` (sharp dividing line), `.soft` (diffused blur). |
| `.visibilityPriority(_:)` | OS 27: priority for which toolbar actions stay visible when space is tight. |

## Accessibility environment

| API | Use |
| --- | --- |
| `@Environment(\.accessibilityReduceTransparency)` | True means replace glass with opaque fills. |
| `@Environment(\.colorSchemeContrast)` | `.increased` means full-alpha semantic labels, no custom tints over glass. |
| `NSWorkspace.shared.accessibilityDisplayShouldReduceTransparency` | Legacy AppKit-bridge equivalent of the first check. |

## Availability and opt-outs

- Requires building with the macOS 26+ / iOS 26+ SDK (Xcode 26 or later).
  Guard custom glass with `#available(macOS 26.0, *)` and confirm at runtime
  that the branch is actually taken.
- Info.plist `UIDesignRequiresCompatibility` set to true opts the app out of
  the new design entirely; glass never renders while it is present. Remove it
  once the app is ready.
- Reduce Transparency (System Settings > Accessibility > Display) replaces
  glass with opaque fills system-wide; on a test machine this masquerades as
  "glass is broken".
- UIKit's equivalent (`UIGlassEffect` in a `UIVisualEffectView`) requires
  explicit adoption; SwiftUI standard components adopt automatically. In this
  skill's scope, SwiftUI is the implementation layer.

## Out of scope pointers

- App-icon glass is authored in Icon Composer (multi-layer icons with
  annotation for refraction and content effects), not with `glassEffect`.
- Web glassmorphism (`backdrop-filter`) shares the aesthetic, none of the
  APIs or verification behavior described in
  [testing_and_oracles.md](testing_and_oracles.md).
