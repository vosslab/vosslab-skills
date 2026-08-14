# Component seeds

Two seed views under `assets/` encode the correct patterns as code, so a coder
consumes one component instead of remembering six rules. Copy the files into
the target project (they are seeds; the target owns its copy) and adjust
padding, radius, and defaults to fit.

## GlassSurface

`assets/GlassSurface.swift` -- a drop-in glass surface with the layered
contrast fixes built in:

- Reads `accessibilityReduceTransparency` and `colorSchemeContrast`; renders
  an opaque fill instead of glass when either demands it.
- Optional `scrimOpacity` for text over uncontrolled backdrops (0.4 black
  scrim gives roughly a 4.6:1 floor under white text).
- Applies `.glassEffect(.regular, in: .rect(cornerRadius:))` on the normal
  path, keeping the sampling path clear.

Usage in the target:

```swift
GlassSurface(cornerRadius: 16, scrimOpacity: 0.4) {
	Label("Inspect", systemImage: "sidebar.trailing")
		.foregroundStyle(.primary)
}
```

Wrap glass groups that should merge or morph in a `GlassEffectContainer` at
the call site; the seed deliberately owns one surface, not the grouping (see
[layers_and_sampling.md](layers_and_sampling.md)).

## GlassEvidenceView

`assets/GlassEvidenceView.swift` -- the verification harness. Renders one
glass surface and one flat `.regularMaterial` control side by side over a
multi-color gradient, so a single on-screen capture carries its own
differential control: if the two pills look the same, glass is not rendering.

Wire it into a debug window or preview in the target app, then run the
evidence protocol in [testing_and_oracles.md](testing_and_oracles.md) against
it. It is also the known-good baseline when debugging a broken surface: if the
harness shows live glass and the app surface does not, the defect is in the
app's sampling path, not the environment.

## Seed policy

Both files are annotated `@available(macOS 26.0, *)` and compile only against
the macOS 26+ SDK. They are starting points: keep the accessibility branches
when editing, and keep any opaque fill out of the path between the glass and
the content behind it.
