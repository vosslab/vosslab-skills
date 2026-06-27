# Project workflow

Use this reference when the skill is invoked on a target PySide6 application, not while
building the pyside6-engineer skill itself. The two workflows below cover the two starting
states: building a new Qt app from nothing, and improving or debugging an existing one.

## Detect the project state

Inspect the target repo before writing any Qt code:

- Search for PySide6 source: `QMainWindow`, `QDialog`, `QWidget` subclasses, `.ui` files,
  `.connect()` signal wiring, `QThread` usage, and model classes.
- Search for Qt tests or screenshots: any `pytest-qt` tests, `QTest` calls, or GUI screenshots
  in the repo.
- Search for architecture docs that describe a window structure, threading model, or state
  ownership.

If any of these exist, follow the existing-repo path. If none exist, follow the greenfield path.

## Qt contract

Both paths write and maintain a Qt contract. Use the target repo's existing docs location when
present; otherwise create `docs/QT_CONTRACT.md`. The contract records:

- Window structure: which class is the top-level window and why (`QMainWindow` vs `QDialog` vs
  bare `QWidget`).
- Composition tree: the logical widget hierarchy, one level of nesting per line.
- State ownership: which object owns each piece of mutable state (model class, controller, or
  window), and how views read it.
- Threading model: which work runs off the UI thread, the worker class name, and the signals that
  carry results back to the UI thread.
- Required states per surface: loading, empty, valid, invalid, busy, success, failure.

## Greenfield path

1. Evidence: choose the window shell and sketch the composition tree before coding.
   - Answer the task-classification questions in `references/task_selection.md`.
   - Decide `QMainWindow`, `QDialog`, `QWidget`, or `QWizard` and state the reason.
   - Draw the composition tree: top-level window, major layout regions, and key child widgets.
   - Identify where each required state (loading, empty, valid, invalid, busy, success, failure)
     will appear in the tree.

2. Design contract: write the Qt contract before opening any editor.
   - Record the window structure, composition tree, state ownership, and threading model.
   - This is the single source of truth; all implementation decisions reference it.
   - Consult `references/topic_index.md` to match each feature area to its reference guide.

3. Implementation choices: pick the concrete Qt classes.
   - Qt Widgets vs Qt Quick: default to Qt Widgets for dense business UI, forms, and inspectors;
     use Qt Quick only when the request explicitly names QML or requires fluid animation.
   - Model/view separation: use `QAbstractItemModel` whenever a table or tree will have more than
     a few hundred rows, or the same data appears in more than one view.
   - Signal design: define signal boundaries up front; avoid connecting widgets to each other
     directly when a model or controller can own the state.
   - Threading: if any operation can block for more than a few milliseconds, name the worker
     class and thread boundary in the contract before implementing.

4. Validation: verify each surface before calling the task done.
   - Run state-transition checks: manually or with `pytest-qt`, drive the UI through loading,
     empty, valid, invalid, busy, success, and failure states and confirm each renders correctly.
   - Capture a screenshot grid: one screenshot per required state for each major surface.
   - Confirm keyboard navigation reaches every primary action.
   - Confirm no `QThread` is left running after the window closes.

## Existing-repo path

1. Inspect first: read the target before writing a line.
   - List `.ui` files and which classes load them.
   - List `QMainWindow`, `QDialog`, and `QWidget` subclasses.
   - Find all `.connect()` wiring and map signal sources to slots.
   - Find any existing GUI tests or screenshots.

2. Identify the current design: build a picture of the existing state.
   - List the widget classes and their parent-child relationships.
   - Identify state bottlenecks: places where one widget reaches into another's internals, or
     where state is duplicated across two or more objects.
   - Note the threading model as-is: are there `QThread` workers, and do they clean up correctly?
   - Write or update the Qt contract to reflect what is actually there, not what it should be.

3. Repo-specific changes: make targeted changes one dependency at a time.
   - Refactor one cross-widget dependency at a time; do not reorganize the whole tree in one pass.
   - For each change, state the before and after in terms of the Qt contract (ownership,
     signal boundary, or threading model).
   - Tie each change to a specific issue, failing test, or state that renders incorrectly.

4. Prove improvement: demonstrate the change had the intended effect.
   - Write or update characterization tests that cover the changed state transitions.
   - Capture a screenshot before-and-after grid for any changed visual surface.
   - Run the full test suite; confirm no regressions.
   - Confirm the Qt contract is up to date with the new structure.

## Qt review checklist

Before closing any Qt task, verify:

- The Qt contract is written and current.
- Every required state (loading, empty, valid, invalid, busy, success, failure) is handled for
  each surface.
- No long-running work blocks the UI thread.
- `QThread` workers are properly connected and clean up when the window closes.
- Signal ownership is explicit: each signal has one clear emitter and its receivers are connected
  in one place.
- At least one inspectable artifact exists: a screenshot grid, a widget-tree dump, or a
  state-transition test result.
