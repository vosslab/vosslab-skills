# Reference survey

This is the committed coverage map for the three local-only design books in
`references/local-only/`: `About_Face.txt`, `Practical_UI.txt`, and
`Refactoring_UI.txt`. These are general UX and visual-design texts, not
framework-specific sources, so this survey lenses them for framework-agnostic
UX review: visual hierarchy, interaction quality, state coverage, and
accessibility. The books are flat text with no reliable headings, so locate a
passage by grepping the named file for a listed term.

## How to use this survey

- Pick the topic, open the strongest book listed, and grep that file for a term.
- Reference a book by its bare path plus a grep term, for example
  `references/local-only/About_Face.txt`, grep `posture`. Do not link a book.
- When the books are absent (a clean clone gitignores `references/local-only/`)
  or a topic is marked thin, route to [design_books.md](design_books.md) for the
  broader design literature, or reason from first-principles UX heuristics instead.
- The books cover design quality and interaction reasoning. For framework-specific
  implementation details, consult framework documentation directly.

## Shared book facts

These columns are the canonical shared-book facts. The first two columns match
the `pyside6-engineer` survey exactly; only the lens-routed chapter column differs
because a Qt lens and a UX-review lens surface different chapters of the same
general UX book. Every grep term below was verified to hit its book.

| Book filename | Coverage strength | Grep terms (from validated pool) | Chapter/section (lens-routed) |
| --- | --- | --- | --- |
| `About_Face.txt` | strong | `posture`, `dialog`, `modal`, `modeless`, `navigation`, `excise`, `affordance`, `feedback`, `mental model`, `wizard`, `menu`, `toolbar` | Task flow and interaction design, dialog behavior and feedback patterns, navigation structure and window posture, multi-step wizard flows |
| `Practical_UI.txt` | strong | `visual hierarchy`, `spacing`, `contrast`, `typography`, `form`, `label`, `layout`, `accessibility`, `disabled` | Visual hierarchy and layout fundamentals, form design and label clarity, accessibility and disabled state handling |
| `Refactoring_UI.txt` | partial | `spacing`, `color`, `contrast`, `typography`, `shadow`, `depth`, `hierarchy`, `size`, `weight` | Visual polish pass: spacing rhythm, color and contrast, emphasis through size and weight |

`Refactoring_UI.txt` is rated partial because it is a short, tactics-focused
visual-design book; it is strong on spacing, color, and typography but thin on
interaction flow, dialogs, navigation, and state coverage. Lean on `About_Face.txt`
for those.

## Topic-to-reference map

### Visual hierarchy and emphasis

Coverage: strong.

- `references/local-only/Practical_UI.txt`. grep `visual hierarchy`, `contrast`, `typography`, `spacing`.
- `references/local-only/Refactoring_UI.txt`. grep `hierarchy`, `size`, `weight`, `color`.
- `references/local-only/About_Face.txt`. grep `feedback`, `affordance`.
- Lens: establish a clear reading order through spacing, grouping, size, and weight
  before reaching for color or decoration.

### Interaction quality and feedback

Coverage: strong (`About_Face.txt` is the primary source).

- `references/local-only/About_Face.txt`. grep `feedback`, `affordance`, `mental model`, `excise`.
- `references/local-only/Practical_UI.txt`. grep `label`, `disabled`, `accessibility`.
- Lens: give immediate feedback for user actions, prevent errors before showing
  them, and remove excise steps that stand between the user and their goal.

### State coverage (empty, loading, error)

Coverage: partial.

- `references/local-only/About_Face.txt`. grep `feedback`, `dialog`, `modal`.
- `references/local-only/Practical_UI.txt`. grep `disabled`, `form`, `accessibility`.
- `references/local-only/Refactoring_UI.txt`. grep `color`, `contrast`.
- Lens: empty, loading, and busy states are thin in the books; design them to look
  intentional rather than broken. Route to first-principles reasoning and
  framework documentation when the books are insufficient.

### Navigation and flow

Coverage: strong (`About_Face.txt`).

- `references/local-only/About_Face.txt`. grep `navigation`, `posture`, `menu`, `toolbar`, `excise`, `wizard`.
- `references/local-only/Practical_UI.txt`. grep `layout`, `label`.
- Lens: set the window or page posture (sovereign, transient, or daemon), expose
  commands through menus or toolbars, route multi-step flows with wizard patterns,
  and remove navigation excise.

### Accessibility and inclusive design

Coverage: strong (`Practical_UI.txt` is the primary source).

- `references/local-only/Practical_UI.txt`. grep `accessibility`, `contrast`, `label`, `disabled`.
- `references/local-only/About_Face.txt`. grep `affordance`, `feedback`.
- Lens: check keyboard flow, sensible tab order, sufficient color contrast,
  explicit labels, and accessible names for interactive controls.

### Form design and input states

Coverage: strong.

- `references/local-only/Practical_UI.txt`. grep `form`, `label`, `spacing`, `disabled`, `accessibility`.
- `references/local-only/About_Face.txt`. grep `affordance`, `feedback`.
- Lens: keep forms short, labels explicit, and primary actions visually dominant;
  design explicit disabled, validation, and error states so users recover easily.

### Visual polish and theming

Coverage: partial (`Refactoring_UI.txt` is concise tactics).

- `references/local-only/Refactoring_UI.txt`. grep `spacing`, `color`, `contrast`, `shadow`, `depth`.
- `references/local-only/Practical_UI.txt`. grep `spacing`, `contrast`, `typography`.
- Lens: apply visual polish as a finishing layer over good layout and interaction
  structure, not as a substitute for either.

## Weak-coverage decision

Empty states, loading and busy states, and framework-specific accessibility APIs
are thin or absent in these general design books. For these topics, treat the books
as secondary and route to [design_books.md](design_books.md) for the broader design
literature, to framework documentation, and to first-principles UX reasoning.
