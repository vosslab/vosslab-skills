# Testing and oracles

Use this reference when building tests, fixture scenarios, and proof-of-improvement evidence for
any PySide6 application. The goal is to prove that a target app improved: a before-and-after
screenshot grid plus state-transition test results are the minimum acceptable evidence.

## Degenerate fixture scenarios

Include at least these scenarios in the test corpus for any non-trivial surface:

- Empty state: no data rows, no file loaded, no search results; confirm the empty-state widget
  or message is shown and no crash occurs.
- Loading state: data fetch in progress; confirm a spinner or progress indicator is shown and the
  UI remains responsive (event loop not blocked).
- Error / failure state: network error, file not found, or invalid input; confirm the error is
  shown in the UI and the app can recover or retry without a restart.
- Success state: action completed; confirm a confirmation message, status bar update, or visual
  change is present.
- Resize: drag the window from its minimum size to a large size and back; confirm no layout
  overflow, clipping, or widget disappearance.
- Close with unsaved changes: trigger the close event while the document is dirty; confirm a
  save prompt appears and cancel keeps the window open.
- High-DPI screen: run with `QT_SCALE_FACTOR=2`; confirm icons, fonts, and layout remain correct.
- Rapid input: type or click faster than the UI would normally process; confirm no queue
  build-up, freeze, or duplicate actions.
- Thread completion after window close: confirm the `QThread` worker stops cleanly and does not
  emit signals after the parent widget is deleted.

## Oracles

Validate UI behavior against a trusted oracle before declaring it correct.

- `pytest-qt` with `qtbot`: simulate clicks, key presses, and widget interactions in a
  headless test; assert on widget text, enabled state, and visibility.
- `QTest`: send synthetic mouse and keyboard events at the C++ level; useful for timing-sensitive
  interactions.
- Screenshot regression: capture the window in each required state with
  `QWidget.grab()` or `screencapture`; compare to a known-good baseline image.
- Widget-tree dump: use `QApplication.allWidgets()` or a recursive walk to dump class names,
  object names, and visibility; compare before and after a state transition.
- Manual state walkthrough: drive each required state by hand (or with `qtbot`) and record the
  result in a checklist; the checklist is the oracle for states that are hard to automate.

## Property and state invariants

Test these invariants in addition to exact-output comparisons:

- All primary actions are reachable by keyboard navigation (Tab, Enter, and shortcut keys) and
  not just by mouse click.
- No `QThread` is left running after the main window closes.
- A model change (insert, remove, update) updates all views that display that model.
- A signal emitted on a worker thread reaches the UI slot on the UI thread (not the worker
  thread); verify with `QThread.currentThread()` in the slot during testing.
- The same data item cannot appear with two different values in two different views
  simultaneously (cross-view consistency).
- Closing a dialog with the X button has the same effect as clicking Cancel (rejected outcome,
  no side effects).

## Inspectable artifacts

Generate at least one inspectable artifact when a surface changes:

- Screenshot grid: one screenshot per required state (loading, empty, valid, invalid, busy,
  success, failure) captured with `QWidget.grab()` or `screencapture`. This is the primary
  visual proof of correctness.
- State-transition test results: a `pytest-qt` run log showing which transitions pass and which
  fail; attach the log as the acceptance artifact for the task.
- Widget-tree dump: a text file listing class names, object names, enabled state, and visibility
  for the top-level window after each major state change.
- Before-and-after screenshot pair: for any existing-repo improvement, capture the same state
  before and after the change; the pair is the minimum proof of visual improvement.

## How to prove the target improved

Use this checklist when the task is "improve my PySide6 app" or similar:

1. Capture screenshots of the current state before any changes (loading, empty, error, success at
   minimum); these are the before evidence.
2. Write characterization tests for the state transitions you will touch; run them before
   changing any code to confirm which pass and which fail.
3. Make the changes described in `references/project_workflow.md` (existing-repo path), one
   cross-widget dependency at a time.
4. After each change, run the characterization tests; confirm previously failing transitions now
   pass and no previously passing transitions regressed.
5. Capture the after screenshots in the same states as step 1.
6. Deliver the before-and-after screenshot grid and the test run log as the proof artifact.

## Project locations

Place test fixtures and artifacts in standard locations:

- `tests/` for `pytest-qt` tests and widget-interaction tests.
- `tests/fixtures/qt/` for reusable fixture data (sample files, model payloads, error
  responses).
- `docs/screenshots/` for before-and-after screenshot grids included in documentation.
- Temporary debug artifacts (widget-tree dumps, state logs) go in the scratchpad or `/tmp/`;
  do not commit them.
