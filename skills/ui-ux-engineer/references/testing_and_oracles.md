# Testing and oracles

Use this reference when building the fixture corpus and audit checks for any UX task on a
target interface project.

## Degenerate fixture corpus

Include at least these cases in the fixture corpus for every interactive surface:

- Empty state: the surface when no data is present yet; must look intentional, not broken.
- Loading state: the surface while data is in flight; progress must be visible and the surface
  must remain responsive.
- Error state: a network failure or server error; context must be preserved, a recovery action
  must be offered.
- Success state: confirmation that the action completed; must not block the next user step.
- Keyboard reachability: every primary action reachable by Tab, Enter, and arrow keys without
  a pointer device.
- High-contrast mode: verify layout and icons remain usable when OS high-contrast mode is
  enabled.
- Touch targets: every interactive element meets a 44x44 px minimum touch-target size.
- Screen-reader output: every interactive control announces a non-empty name, its role, and
  its current state when focused.
- Responsive layout: the primary flow must be functional and legible at four viewport widths:
  320 px (narrow mobile), 480 px (wide mobile), 768 px (tablet), and 1920 px (desktop).

## Oracles

Validate a UX decision against a trusted oracle before declaring it correct.

- Nielsen 10 heuristics: score each heuristic on a 0-4 scale (0 = critical violation,
  4 = no issue). The ten heuristics are: visibility of system status; match between system
  and real world; user control and freedom; consistency and standards; error prevention;
  recognition over recall; flexibility and efficiency; aesthetic and minimalist design;
  help users recognize and recover from errors; help and documentation.
- WCAG 2.1 AA audit with axe-core: run axe-core (or an equivalent automated tool) and resolve
  all critical and serious violations. Manual checks cover keyboard operability, focus order,
  accessible names, and color-only meaning.
- Task-completion test: trace the primary user goal from entry to success, counting steps,
  decision points, and error-recovery steps. Compare against the design contract minimum.
- Contrast checker: measure foreground/background contrast ratios with a dedicated tool
  (e.g., WebAIM Contrast Checker). Normal text must meet 4.5:1; large text 3:1; focus
  indicators and non-text UI components 3:1.

## Invariants

Test these invariants in addition to state-by-state checks:

- One dominant primary action: each screen in the primary flow has exactly one visually
  dominant call-to-action.
- Grouped controls: related controls are visually grouped with spacing before borders or
  decorative containers.
- Actionable error messages: every error names the problem and states the next recovery
  step; no generic "something went wrong" messages.
- Keyboard tab order matches reading order: pressing Tab moves focus in the same direction
  a user reads the content, left-to-right then top-to-bottom.
- Labeled icons: every icon-only button has an accessible name (aria-label, aria-labelledby,
  or an equivalent platform attribute); no icon is the sole indicator of meaning without a
  text alternative.

## Inspectable artifacts

Generate at least one of these artifacts when a UX review or design task produces output:

- Heuristic checklist: a table with one row per Nielsen heuristic, scored 0-4, with a specific
  finding and fix for each violation.
- A11y report: axe-core output or a manual audit log with violation type, affected element,
  WCAG criterion, and proposed fix.
- Interaction-flow diagram: a flowchart or annotated wireframe showing the primary flow and
  each branch state (error, empty, success) with recovery paths.
- Responsive screenshot grid: one screenshot or annotated layout per breakpoint
  (320 / 480 / 768 / 1920 px) showing the primary surface at each width.

## How to prove the target improved

Record before-and-after measurements as the acceptance gate:

1. Baseline: before any changes, score each Nielsen heuristic (0-4) and count WCAG AA
   violations by severity (critical, serious, moderate, minor).
2. After changes: re-score each heuristic and re-run the WCAG audit.
3. Delta: report the change in heuristic scores and the reduction in violation counts.
4. Accept when: all heuristic scores are 3 or above (no critical or major issues), and all
   critical and serious WCAG violations are resolved.

## Project locations

Place fixtures and artifacts in these standard locations:
- `docs/ux/` for UX audits, state matrices, heuristic checklists, and annotated screenshots.
- `tests/fixtures/ux/` for structured fixture data (user flow scripts, state definitions).
- `debug/ux/` for temporary artifacts generated during a UX investigation.
