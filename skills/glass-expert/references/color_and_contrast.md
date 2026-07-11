# Color and contrast

Glass has no fixed color and guarantees no minimum text contrast. Color
choices decide whether the effect is visible and whether text stays legible
over backdrops the user controls.

## The material adapts by itself

- Glass switches between light and dark treatment based on the luminance of
  the content behind it. A hardcoded foreground color that reads well over one
  backdrop fails over another; use semantic styles
  (`.foregroundStyle(.primary)`, `.secondary`) so vibrancy adapts with the
  material.
- Glass self-adjusts its own opacity: more opaque over busy content such as
  text (to keep foreground elements readable), more transparent over plain
  backgrounds. Identical code looks different across backdrops by design.
- macOS 27 adds a system-wide transparency slider (ultra clear to fully
  tinted) and diffuses complex content behind glass more aggressively, with
  darkened edges and brighter specular highlights. Translucency is a
  user-controlled range; never tune contrast to one observed look.
- `.tint(...)` modulates the sampled backdrop rather than painting a flat
  color; a tinted glass control shifts hue over busy content. Verify tint over
  light and dark backdrops before shipping it.
- Pure white or pure black backdrops hide most of the effect; judge glass over
  mid-tone, multi-color content.

## Contrast is guaranteed by layers, not observed

White text over glass can pass WCAG AAA over a dark backdrop and drop below
2:1 over a bright photo. Apply these in order:

1. Read `@Environment(\.accessibilityReduceTransparency)`. When true, replace
   glass with an opaque fill. Highest-value fix: it honors every user who
   already told the system they need it. (A legacy AppKit bridge checks
   `NSWorkspace.shared.accessibilityDisplayShouldReduceTransparency`.)
2. Read `@Environment(\.colorSchemeContrast)`. When `.increased`, switch
   labels to full-alpha semantic colors and drop custom tints over glass.
3. Add a text protection scrim when the backdrop is uncontrolled and the
   surface carries text: black at 40 percent opacity under white text
   guarantees roughly 4.6:1 over any backdrop.
4. Use vibrancy for secondary labels only; primary labels need full-opacity
   semantic color.
5. Judge contrast over three backdrops: near-white, a bright photo, and a
   mid-tone gradient. Two of the three are the common failure cases.
6. Measure captured screenshots. Use the color-accessibility-expert skill's
   `image_contrast.py --points` mode to eyedrop text against the glass region
   behind it. Below 4.5:1 for normal text, or 3:1 for 18pt and larger, is a
   bug, not a design decision.

The seed view in [component_seeds.md](component_seeds.md) implements steps 1-3
as a single wrapper. The capture workflow for the measurements lives in
[capture_paths.md](capture_paths.md).
