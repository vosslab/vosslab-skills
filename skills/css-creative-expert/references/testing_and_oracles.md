# CSS testing and oracles

Use rendered output as the primary oracle; a stylesheet can parse while the page
still clips content, loses hierarchy, or fails in an untested scheme.

## Choose evidence

- Capture screenshots for each affected page state at narrow, typical, and wide
  viewports, plus light and dark schemes when themes exist.
- Run a focused Playwright path using the target repository's
  `docs/PLAYWRIGHT_TEST_STYLE.md` when the target serves HTML. Exercise visible
  actions and assert a user-visible state; use markup inspection as supporting
  diagnostics.
- Add computed-style assertions for critical values such as display mode,
  overflow, token resolution, visibility, and reduced-motion overrides.
- Check long strings, empty content, zoom, keyboard focus, and image loading
  where the changed component depends on them.

## Accessibility and compatibility

- Design meaningful foreground, surface, and state color roles here; hand a
  numerical contrast measurement and repair workflow to
  `color-accessibility-expert`.
- Test `prefers-reduced-motion` when adding motion and inspect fallback behavior
  before relying on a new selector, layout primitive, or color function.
- Treat browser support matrices and CSS specifications as the authority for
  version-sensitive features; use book conversions and parser results as
  supporting context.

## Report

State the URLs or components, viewports, schemes, actions, screenshots,
computed-style checks, and any delegated contrast result. Keep temporary
implementation probes out of permanent test suites unless they satisfy the
target repository's durable-test policy.
