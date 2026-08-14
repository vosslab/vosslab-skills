# Capture paths

Glass evidence is only as good as the capture path. Offscreen render paths can
omit the live backdrop compositing, producing flat gray "evidence" from a
perfectly working app.

## Why offscreen captures lie

`cacheDisplay(in:to:)`, `bitmapImageRepForCachingDisplay(in:)`, and SwiftUI
`ImageRenderer` render the view tree in isolation. The glass region can come
out flat gray even when the on-screen app is correct. Validate any offscreen
path before trusting it: render one known-glass view and one flat control
through it, and if the two look the same, switch to on-screen capture.

## On-screen capture workflow

1. Find the window id of the running app:

   ```bash
   swift scripts/list_window_ids.swift MyApp
   ```

   Prints `windowID  owner  title  WxH` for each on-screen window matching
   the app-name substring.

2. Capture the composited on-screen window, labeled with the appearance mode
   and Reduce Transparency state at capture time:

   ```bash
   bash scripts/capture_glass_evidence.sh <window-id> evidence/toolbar
   ```

   Writes `evidence/toolbar_<light|dark>_<normal|reduced>.png` using
   `screencapture -o -l <window-id>` (`-o` omits the window shadow so pixel
   comparisons align). The script prints the output filename.

3. Record the OS version with the capture set (`sw_vers -productVersion`).
   Glass chrome renders differently on macOS 26 and 27 by design, so an
   unlabeled capture cannot be judged later.

## Capture states to collect

- Light and dark mode. Force per-app appearance for the run rather than
  flipping the whole system when possible; query the effective appearance at
  capture time rather than trusting the launch setting.
- Reduce Transparency off and on (System Settings > Accessibility > Display).
  Toggle it manually; the labeled filenames from the capture script keep the
  states distinct.
- A scrolled variant when content moves under the glass: the glass region
  must change when the backdrop changes.

## Comparing captures

Use `scripts/compare_captures.py -a one.png -b two.png` for the differential
verdicts; the decision rules live in
[testing_and_oracles.md](testing_and_oracles.md).
