# Testing and oracles

Glass fails silently: the code compiles and a capture can look plausible while
the effect is absent or illegible. Ship only on visual evidence that shows the
backdrop-sampling behavior itself. Capture mechanics live in
[capture_paths.md](capture_paths.md).

## Evidence protocol

1. Put strong multi-color content behind the glass surface -- a gradient, a
   photo, or syntax-highlighted text reaching under the glass edges. The
   harness in [component_seeds.md](component_seeds.md) provides one.
2. Capture the live window on screen. The glass region must show blurred,
   refracted color from the content behind it, not a uniform fill.
3. Differential proof: capture once normally, once with Reduce Transparency
   enabled. The reduced capture must be visibly more opaque; run
   `scripts/compare_captures.py` on the pair. A DIFFERENT verdict proves the
   effect responds to system state; IDENTICAL means flat fill.
4. Side-by-side control: the same layout with `.regularMaterial` in place of
   glass must look different from the glass capture (the seed harness renders
   both in one frame).
5. Scroll or move the content behind the glass and capture again; the glass
   region must change with the backdrop.
6. Repeat in light and dark mode; label every capture with the effective
   appearance, Reduce Transparency state, and OS version at capture time.

## Oracles

- Pixel differential: `scripts/compare_captures.py` prints mean channel
  difference, changed-pixel fraction, and a DIFFERENT / IDENTICAL verdict.
  Crop to the glass region with `--region x,y,w,h` when the rest of the frame
  is static.
- Contrast measurement: the color-accessibility-expert skill's
  `image_contrast.py --points` samples text against the glass region behind
  it. Thresholds: 4.5:1 normal text, 3:1 at 18pt and larger.
- Expected-appearance matrix: judge each capture against its backdrop.

| Backdrop behind glass | Correct appearance |
| --- | --- |
| Plain white | Nearly invisible; faint edge highlight. Expected, not a bug. |
| Plain black | Barely visible; subtle rim light. Expected, not a bug. |
| Mid-tone gradient | Blurred, refracted color inside the shape. Best judging backdrop. |
| Busy photo or text | Visibly tinted, more opaque; backdrop shapes muted but present. |
| Reduce Transparency on | Flat opaque fill. Expected; this is the differential proof. |

A capture proves glass only on the two contrast-bearing rows; over plain
white or black, correct and broken look the same.

## Paste-able dispatch brief

Copy into a subagent brief when dispatching glass work, filling in the surface:

```text
Build <surface> with .glassEffect targeting macOS 26+.
Return these captures with the result:
1. On-screen capture (screencapture -o -l <window-id>) of the live window,
   with multi-color content reaching under the glass edges.
2. The same view with Reduce Transparency enabled; it must be visibly more
   opaque than capture 1.
3. The same layout with .regularMaterial in place of glass; it must look
   different from capture 1.
4. Light and dark captures, each labeled with the effective appearance,
   Reduce Transparency state, and OS version at capture time.
SHIP when the glass region visibly blurs and refracts the backdrop and all
text over glass measures at least 4.5:1 (3:1 for text 18pt and larger).
REWORK when the glass region reads as a flat panel, or when any pair of
captures above is pixel-identical.
```
