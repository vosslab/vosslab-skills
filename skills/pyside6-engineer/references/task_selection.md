# Task selection

Use this reference to classify a PySide6 request before consulting the topic index or
implementation guides. Answering these questions before writing any code prevents the
most common mismatch: choosing the wrong window container or threading model early
and refactoring later.

## Task dimensions

Answer these questions to frame the task:

- Window container: `QMainWindow` (menus, toolbars, docks, status bar), `QDialog` (short focused
  task, confirmation, or cancellation), `QWidget` (embedded panel or standalone surface),
  `QWizard` (multi-step sequential flow), or `QStackedWidget` controller (multi-step flow that
  tabs would over-complicate).
- Toolkit layer: Qt Widgets (classic desktop productivity, forms, tables, dense business UI) or
  Qt Quick / QML (animated, fluid, or media-centric surfaces where QML is the stated target).
- State coordination: single-window (one `QMainWindow` owns all state), multi-document interface
  (`QMdiArea` or tabbed sub-windows), or cross-view (multiple independent views that must stay
  synchronized through a shared model or signals).
- User goal: the single action the user wants to complete. Name it explicitly before picking
  widgets.
- Required states: which of these must the UI handle? loading (data not yet ready), empty (no
  records or results), valid (form passes validation), invalid (form has errors), busy (background
  work in progress), success (action completed), failure (action failed with recoverable error).

## Common task types

- Form and settings panel: `QDialog` or docked `QWidget` with `QFormLayout`, validation states,
  and accept/cancel flow.
- Inspector or property editor: docked `QWidget` with a model-driven property table; cross-view
  state sync through signals.
- Data table or tree browser: `QMainWindow` or embedded `QWidget` with `QTableView` /
  `QTreeView` plus a `QAbstractItemModel` subclass.
- Wizard or guided flow: `QWizard` for linear confirmed steps; `QStackedWidget` for non-linear
  multi-step routing with a controller.
- Progress and background task: any container with a `QProgressBar` or status bar update driven
  by a `QThread` worker; busy and success/failure states are required.
- Dashboard or overview: `QMainWindow` with a central `QSplitter` or `QStackedWidget` layout;
  loading and empty states are required.
- Document editor: `QMainWindow` with a central editor widget and file-menu actions; dirty-state
  tracking and close-with-unsaved handling are required.
- Alert and confirmation: `QMessageBox` (no layout code needed) or a small `QDialog` with a
  custom message; do not use a full `QMainWindow` for a one-question interaction.

## Clarifying questions to answer before coding

- Which window container fits the task? If unclear, default to `QMainWindow` for multi-region
  apps and `QDialog` for focused single-purpose tasks.
- Is this a new surface (greenfield) or a change to an existing widget class (existing-repo)?
- Which states must be handled, and which widget or controller owns each state transition?
- Does any work run off the UI thread? If yes, name the thread boundary and the signal that
  carries the result back to the UI.
- Is model/view separation required? If the table or tree will exceed a few hundred rows, or if
  the same data appears in more than one view, yes.
- Does the request mention `.ui` files, Qt Designer, or `pyside6-uic`? Route to
  `references/designer_ui_workflow.md` before writing layout code.
- Does the request mention packaging, deployment, or distribution? Route to
  `references/deployment_and_packaging.md` first.
