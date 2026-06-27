# Reference survey

This is the committed coverage map for the three local-only design books in
`references/local-only/`: `About_Face.txt`, `Practical_UI.txt`, and
`Refactoring_UI.txt`. These are general UX and visual-design texts, not Qt API
sources, so this survey lenses them for a Qt engineer applying UX design quality
to PySide6 work (hierarchy, dialogs, navigation, form density). Qt API evidence
lives in a separate guide, see the Qt implementation evidence note below. The
books are flat text with no reliable headings, so locate a passage by grepping
the named file for a listed term.

## How to use this survey

- Pick the topic, open the strongest book listed, and grep that file for a term.
- Reference a book by its bare path plus a grep term, for example
  `references/local-only/About_Face.txt`, grep `posture`. Do not link a book.
- When the books are absent (a clean clone gitignores `references/local-only/`)
  or a topic is marked thin, route to the official Qt docs in
  [`official_qt_for_python_docs.md`](official_qt_for_python_docs.md),
  to the `ui-ux-engineer` skill, or to first-principles UX reasoning instead.
- The books inform design quality, not Qt mechanics. For widget APIs, signals,
  layouts, and tools, use the Qt implementation evidence note below.

## Shared book facts

These columns are the canonical shared-book facts. The `ui-ux-engineer` survey
reuses the first two columns and draws its grep terms from this validated pool;
only its lens-routed column differs. Every grep term below was verified to hit
its book.

| Book filename | Coverage strength | Grep terms (from validated pool) | Chapter/section (lens-routed) |
| --- | --- | --- | --- |
| `About_Face.txt` | strong | `posture`, `dialog`, `modal`, `modeless`, `navigation`, `excise`, `affordance`, `feedback`, `mental model`, `wizard`, `menu`, `toolbar` | Qt dialog mode (modal vs modeless), window posture for a `QMainWindow` shell, menu and toolbar command surfaces, cutting navigation excise |
| `Practical_UI.txt` | strong | `visual hierarchy`, `spacing`, `contrast`, `typography`, `form`, `label`, `layout`, `accessibility`, `disabled` | Form layout and density, label clarity, control hierarchy, disabled and validation states for `QWidget` forms |
| `Refactoring_UI.txt` | partial | `spacing`, `color`, `contrast`, `typography`, `shadow`, `depth`, `hierarchy`, `size`, `weight` | Visual polish of stylesheets (QSS): spacing rhythm, color and contrast, elevation and depth, emphasis through size and weight |

`Refactoring_UI.txt` is rated partial because it is a short, tactics-focused
visual-design book; it is strong on spacing, color, and typography but thin on
interaction flow, dialogs, and navigation. Lean on `About_Face.txt` for those.

## Topic-to-reference map

### Visual hierarchy and emphasis

Coverage: strong.

- `references/local-only/Practical_UI.txt`. grep `visual hierarchy`, `contrast`, `typography`.
- `references/local-only/Refactoring_UI.txt`. grep `hierarchy`, `size`, `weight`, `color`.
- `references/local-only/About_Face.txt`. grep `hierarchy`.
- Lens: decide which widget reads as primary, then express that in font weight,
  size, and spacing within layouts and QSS rather than absolute positioning.

### Dialogs and modal flow

Coverage: strong (`About_Face.txt` is the primary source).

- `references/local-only/About_Face.txt`. grep `dialog`, `modal`, `modeless`, `error`, `feedback`.
- Lens: choose `QDialog` modal versus modeless deliberately; reserve modal for
  short focused confirmations, and design error and feedback messaging in place.

### Navigation and window shells

Coverage: strong (`About_Face.txt`).

- `references/local-only/About_Face.txt`. grep `navigation`, `posture`, `menu`, `toolbar`, `excise`.
- Lens: set the `QMainWindow` posture (sovereign, transient, or daemon), expose
  commands through menus and toolbars, route multi-step flows with
  `QStackedWidget`, and remove excise navigation between the user and the goal.

### Form density and input states

Coverage: strong (`Practical_UI.txt` plus `About_Face.txt`).

- `references/local-only/Practical_UI.txt`. grep `form`, `label`, `spacing`, `disabled`, `accessibility`.
- `references/local-only/About_Face.txt`. grep `form`, `input`, `validation`, `affordance`.
- `references/local-only/Refactoring_UI.txt`. grep `spacing`, `border`.
- Lens: tune `QFormLayout` density and label alignment, make input affordances
  obvious, and design explicit disabled, validation, and error states.

### Visual polish and theming

Coverage: partial (`Refactoring_UI.txt` is concise tactics).

- `references/local-only/Refactoring_UI.txt`. grep `spacing`, `color`, `contrast`, `shadow`, `depth`.
- `references/local-only/Practical_UI.txt`. grep `spacing`, `contrast`, `border`.
- Lens: apply QSS stylesheet polish as a finishing layer over good widget choice
  and layout structure, not as a substitute for either.

## Qt implementation evidence

The three books inform design quality only. For Qt APIs, widget choice, signals
and slots, layouts, model/view, and the `pyside6-*` tools, the committed source
of truth is
[`official_qt_for_python_docs.md`](official_qt_for_python_docs.md).
Pair a design decision from the books with the Qt mechanics from that guide.

## Weak-coverage decision

Empty states, loading and busy states, and any Qt-specific API behavior are thin
or absent in these general design books. For these, treat the books as secondary
and route to
[`official_qt_for_python_docs.md`](official_qt_for_python_docs.md),
to the `ui-ux-engineer` skill for framework-agnostic state coverage, and to
first-principles UX reasoning. The grep term `empty state` hits only
`Refactoring_UI.txt` (a few matches), so do not rely on the books for empty and
loading state design.
