# Local books

Use this reference to pick the right local-only design book for a PySide6 task.
The three converted books live in `references/local-only/` and stay out of git.
Load them by bare path text at runtime and grep the named file for a keyword.
The detailed coverage map lives in [reference_survey.md](reference_survey.md).

These three books are general UX and visual-design texts, not Qt API sources.
They inform interface and interaction quality; for Qt widgets, signals, layouts,
and tools, use [official_qt_for_python_docs.md](official_qt_for_python_docs.md).

## Reading order (strongest first for Qt UX work)

1. `references/local-only/About_Face.txt`
   Best for interaction design and behavior: window posture, modal versus
   modeless dialogs, navigation, command surfaces, and reducing wasted work.
   Start here for how a desktop app should behave.
   grep `posture`, `dialog`, `modal`, `modeless`, `navigation`, `excise`,
   `affordance`, `feedback`, `wizard`, `menu`, `toolbar`.
2. `references/local-only/Practical_UI.txt`
   Best for layout, visual hierarchy, form density, labels, and accessibility
   in dense business UIs.
   grep `visual hierarchy`, `form`, `label`, `spacing`, `disabled`,
   `accessibility`, `contrast`, `typography`.
3. `references/local-only/Refactoring_UI.txt`
   Best as a short, tactics-focused visual-polish reference: spacing rhythm,
   color and contrast, and elevation. Concise but thin on interaction flow.
   grep `spacing`, `color`, `contrast`, `shadow`, `depth`, `hierarchy`,
   `size`, `weight`.

## Qt-UX lens per book

- `references/local-only/About_Face.txt` through a Qt lens: set the `QMainWindow`
  posture (sovereign, transient, or daemon); choose `QDialog` modal vs modeless
  deliberately; expose commands through menus and toolbars; route multi-step flows
  with `QStackedWidget` to remove excise navigation between the user and the goal.
- `references/local-only/Practical_UI.txt` through a Qt lens: tune `QFormLayout`
  density and label alignment; make input affordances obvious with placeholder text
  and label pairing; design explicit disabled, validation, and error states as
  widget-state changes, not hidden widgets.
- `references/local-only/Refactoring_UI.txt` through a Qt lens: apply QSS stylesheet
  polish as a finishing layer over good widget choice and layout structure; do not
  use QSS to substitute for either.

## Practical mapping

- For app behavior and window structure, read `About_Face.txt` first.
- For form layout, hierarchy, and accessible labels, read `Practical_UI.txt`.
- For final visual polish of a stylesheet, read `Refactoring_UI.txt`.
- For Qt mechanics behind any of these decisions, read
  [official_qt_for_python_docs.md](official_qt_for_python_docs.md).
- Where the survey marks coverage thin (empty states, loading and busy states,
  Qt-specific behavior), lean on [official_qt_for_python_docs.md](official_qt_for_python_docs.md)
  and the `ui-ux-engineer` skill instead.
- See [reference_survey.md](reference_survey.md) for the full topic-to-book map and
  the complete validated grep term pool.

## Absent on a clean clone

The books are gitignored, so a fresh checkout has none of them. When a book is
absent, route the design question to
[official_qt_for_python_docs.md](official_qt_for_python_docs.md), the
`ui-ux-engineer` skill, or first-principles UX reasoning. No committed file
depends on a book being present.
