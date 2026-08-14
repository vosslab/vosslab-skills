# Topic index

This is the routing front door. Start here, match the user problem to a row, then open
the named guide. Derived from the committed reference files in `references/`. For Qt API
entry points, official tutorials, and installation, always open
`references/official_qt_for_python_docs.md` first.

## Problem routing table

| User problem / trigger | Qt task | Primary reference | Secondary reference |
| --- | --- | --- | --- |
| Multi-pane editor or synchronized views | State sync across widgets | `references/pyside6_patterns.md` | `references/signals_slots.md` |
| Signals not firing or wrong widget updated | Signal-slot wiring | `references/signals_slots.md` | `references/pyside6_patterns.md` |
| Large table with real-time or frequent updates | Model-view architecture | `references/model_view.md` | `references/signals_slots.md` |
| Table rows flicker or scroll position resets | Model reset vs row insert | `references/model_view.md` | - |
| Tree with expand/collapse and lazy loading | `QTreeView` + model | `references/model_view.md` | `references/pyside6_patterns.md` |
| Background I/O, network, or compute | Threading with `QThread` | `references/pyside6_patterns.md` | `references/signals_slots.md` |
| UI freezes during long operation | Event-loop blocking | `references/pyside6_patterns.md` | `references/signals_slots.md` |
| Form validation, error states, disabled inputs | Form patterns | `references/pyside6_patterns.md` | `references/official_qt_for_python_docs.md` |
| Navigation between screens or steps | `QStackedWidget` / `QWizard` | `references/pyside6_patterns.md` | `references/signals_slots.md` |
| Dialog lifecycle: accept, reject, re-open | `QDialog` patterns | `references/pyside6_patterns.md` | `references/official_qt_for_python_docs.md` |
| `.ui` file or Qt Designer involved | Designer workflow | `references/designer_ui_workflow.md` | `references/official_qt_for_python_docs.md` |
| Packaging, deployment, or distributable app | Packaging | `references/deployment_and_packaging.md` | `references/official_qt_for_python_docs.md` |
| Qt API module, class, or install question | Official Qt for Python docs | `references/official_qt_for_python_docs.md` | - |
| Visual polish, spacing, color, or QSS theming | Design books via survey | `references/reference_survey.md` | `references/pyside6_patterns.md` |
| Window posture, modal vs modeless dialog | UX design | `references/reference_survey.md` | `references/pyside6_patterns.md` |
| New app: which window shell to choose | Task classification | `references/task_selection.md` | `references/pyside6_patterns.md` |
| Existing app: where to start improving | Project workflow | `references/project_workflow.md` | `references/task_selection.md` |

## Per-area detail

### State sync and multi-pane editors

Keep shared state in a model or controller object. Expose updates as signals; connect all
view widgets that display that data. Avoid letting sibling widgets call each other's methods
directly. See `references/pyside6_patterns.md` (grep `state`, `controller`) and
`references/signals_slots.md` (grep `disconnect`, `blockSignals`).

### Large table real-time updates

Use a `QAbstractItemModel` subclass with `dataChanged` emission rather than resetting the
whole model on every update. Batch row inserts with `beginInsertRows` / `endInsertRows`.
See `references/model_view.md` (grep `dataChanged`, `beginInsertRows`).

### Background I/O threading

Create a worker `QObject`, move it to a `QThread`, connect `started` to the worker slot,
emit a result signal back to the UI thread. Do not subclass `QThread`. See
`references/pyside6_patterns.md` (grep `QThread`, `worker`, `moveToThread`).

### Form validation

Keep validation logic in a controller or validator function, not spread across widget
event handlers. Drive the valid/invalid/disabled states from that single source. See
`references/pyside6_patterns.md` (grep `valid`, `QLineEdit`, `setEnabled`).

### Official Qt API

For module lookup, installation, tutorial entry points, `pyside6-uic`, `pyside6-rcc`,
and Qt examples, open `references/official_qt_for_python_docs.md` first. The books in
`references/local-only/` are UX design sources, not Qt API references; see the survey
in `references/reference_survey.md` for when to use each book.

## Alias and trigger vocabulary

- State sync: cross-view update, shared model, connected widgets, observer pattern.
- Model-view: `QTableView`, `QTreeView`, `QListView`, `QAbstractItemModel`, custom model.
- Threading: `QThread`, `moveToThread`, worker, async, background, freeze, blocking.
- Signals/slots: `.connect()`, `.disconnect()`, `emit`, custom signal, `pyqtSignal`.
- Form validation: `QLineEdit`, `QComboBox`, `QSpinBox`, valid state, error state, disabled.
- Navigation: `QStackedWidget`, `QWizard`, `QTabWidget`, page routing, multi-step flow.
- Packaging: `pyside6-deploy`, `Nuitka`, PyInstaller, distributable, freeze.
