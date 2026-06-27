# Project workflow

Use this reference when the skill is invoked on a target interface project, not while
building ui-ux-engineer itself. Two workflows are provided: one for greenfield (new) UI
and one for an existing repo or running interface.

## Detect project state

Inspect the target before writing UX recommendations:
- Read the existing surface: screenshots, component structure, or a live running UI.
- Search for UX or design documentation: style guide, design tokens, component library, or spec.
- Search for existing user flows, wireframes, or task scenarios.
- Search for any accessibility notes or a11y audit results.

If any existing surface or design documentation is present, follow the existing-repo path.
If none exist, follow the greenfield path.

## Greenfield path

### 1. Evidence

Establish the user goal and primary flow before making any design decisions:
- Name the primary user goal in one sentence.
- Trace the happy path from entry to success in the fewest steps.
- Sketch a low-fidelity layout (wireframe, text outline, or ASCII diagram) to make the
  structure tangible without committing to visual details.

### 2. Design contract

Write a UX contract before implementation begins. Record:
- Primary goal: the one thing the user is trying to accomplish on this surface.
- Required edge states: empty, loading, error (with recovery path), success, offline,
  permission-denied.
- WCAG compliance level: AA (minimum) or AAA for the surface.
- Device and viewport assumptions: mobile-first, desktop-only, or responsive with named
  breakpoints (320 px, 768 px, 1920 px).

### 3. Implementation choices

Apply design decisions in this order:
- Visual hierarchy: establish reading order through spacing and grouping before typography
  weight or color.
- Interaction flows: map every user action to a system response; design each edge state before
  adding polish.
- Accessibility: check keyboard tab order, accessible names for all controls, and color contrast
  before the visual pass.

### 4. Validation

Score the finished surface before shipping:
- Heuristic-eval rubric: score each of the Nielsen 10 heuristics on a 0-4 scale; record the
  scores.
- WCAG AA check: run axe-core or an equivalent tool; resolve all critical and serious violations.
- Record before-and-after scores if the surface existed in any prior form.

## Existing-repo path

### 1. Inspect first

Gather evidence before proposing changes:
- Collect any existing wireframes, interaction specs, or visual mockups.
- Read any existing a11y audit notes or WCAG compliance reports.
- Run a quick heuristic scan across all primary screens.

### 2. Identify current design quality

Measure the current state objectively:
- Score each of the Nielsen 10 heuristics (0-4 scale) across the primary flow.
- Run a WCAG 2.1 AA audit (axe-core or equivalent); count critical and serious violations.
- Measure task-completion friction: count the steps, decision points, and error-recovery
  paths required to complete the primary user goal.

### 3. Repo-specific changes

Scope the fix list:
- List the top friction points ranked by user impact (not implementation ease).
- Prioritize: fix the highest-friction issues in the primary flow first; defer visual polish.
- For each fix, state the finding, the proposed change, and the expected user-impact reduction.

### 4. Prove improvement

After changes are applied, show the delta:
- Re-score each of the Nielsen 10 heuristics; compare to the baseline scores.
- Re-run the WCAG AA audit; confirm critical and serious violations are resolved.
- Record the before-and-after heuristic scores and violation counts as the acceptance gate.

## UX review checklist

Before closing any UX task, verify:
- The primary user goal is clear from the screen in three seconds.
- The main action is visually dominant and unambiguous.
- All reachable states are explicitly designed: loading, empty, error, success, disabled.
- Validation errors name the problem and state the recovery path.
- Keyboard flow, tab order, and accessible names are correct.
- No navigation excise stands between the user and their goal.
- Visual hierarchy uses spacing and grouping first, color and decoration last.
- Before/after heuristic scores and WCAG violation counts are recorded.
