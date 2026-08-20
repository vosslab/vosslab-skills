# Rendering: dictionary

A dictionary is a set of term-and-definition pairs. In ideonomy, dictionaries are good for: enumerating named alternatives (e.g., redesign options), defining a vocabulary the artifact will use, or capturing a typology where each entry is structurally complete and roughly parallel.

## Form

Each entry is its own heavy-bordered panel: term as the title bar, definition body, then attribute bullets. The double-line `╔═╗` frame says "this is a complete unit." Multiple entries stack vertically with whitespace between them.

## Worked example — *vigil v2 redesign options*

```
╔═══════════════════════════════════════════════════════════════════════════════════════════╗
║   A.  vigil-trail            ─  add a footer, change nothing else                         ║
╠═══════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                           ║
║   Negate "process is invisible"; substitute → "process leaves a trail."                   ║
║                                                                                           ║
║   Every vigil-touched response ends with a small structured footer:                       ║
║                                                                                           ║
║      ╭─────────────────────────────────────────────────────────────────────╮              ║
║      │  [vigil · L1 · branching]                                           │              ║
║      │   reframe:    confirmed                                             │              ║
║      │   confidence: 0.72  ·  mandates: ✓ verify ✓ investigate ✗ extend    │              ║
║      ╰─────────────────────────────────────────────────────────────────────╯              ║
║                                                                                           ║
║   ▸ effort:           LOW                                                                 ║
║   ▸ falsifiable:      ●●●○○                                                               ║
║   ▸ shortcut-resist:  ●●○○○                                                               ║
║   ▸ best for:         daily use, low ceremony, baseline observability                     ║
║                                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════════════════╗
║   B.  vigil-twin             ─  decompose into draft + auditor (subagent)                 ║
╠═══════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                           ║
║   ...                                                                                     ║
║                                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════════════════════╝
```

## Anatomy of a dictionary entry

```
╔════════════════════════════════════════════════════════════════════════════════╗
║   <KEY>          ─  <one-line tagline>                            ← title bar  ║
╠════════════════════════════════════════════════════════════════════════════════╣
║                                                                                ║
║   <generative move that produced this entry — the operator's "X → Y">         ║
║                                                                                ║
║   <body, 2-6 lines: what it is, how it works>                                  ║
║                                                                                ║
║      <small embedded diagram, frame, formula — optional>                       ║
║                                                                                ║
║   ▸ <attribute>:  <value, rating, or 5-dot scale ●●●○○>                       ║
║   ▸ <attribute>:  <value>                                                      ║
║   ▸ <attribute>:  <value>                                                      ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

## Conventions

- **Title bar** (top): `<KEY>  ─  <tagline>` — key in caps if it's a label (A, B, C); plain if it's a name (`vigil-trail`)
- **Generative-move line** (first body line): say which operator produced this entry and what move it made, when relevant. Example: `Substitute "self-grading" → "twin-grading."` This makes the dictionary itself an instance of operator-name-and-move visibility.
- **Body**: 2-6 lines explaining what the entry is. Keep it tight; the panel is not a paragraph dumping ground.
- **Embedded diagram**: optional. If the entry's idea has a small visual form (a flow, a frame, a formula), embed it inside the entry's panel using `╭─╮` rounded frames so it doesn't compete with the entry's outer `╔═╗`.
- **Attribute bullets** (`▸`): 3-5 attributes per entry, each one line. Use 5-dot scales `●●●○○` for ratings; short labels for categorical values.
- **Whitespace**: blank line between entries when stacked vertically; the gap signals "next unit."

## Drama

Dictionaries' drama is in the *diagonal* — when one entry's attributes are notably stronger than the others on the most-important attribute, mark it with `★` in the title bar (`╔═══ ★ B. vigil-twin  ─  ...`). The reader's eye lands on the starred entry first.

If two entries trade off cleanly along an axis (one strong on cost, one strong on payoff), state that explicitly in the artifact text after the dictionary, with a tiny placement diagram showing where each lives.

## Anti-patterns

- Inconsistent attribute sets across entries → if A has `effort/falsifiable/best-for` and B has `cost/risk/notes`, the dictionary isn't really parallel; pick one schema and apply to all
- Entry bodies of wildly different lengths (one entry is 2 lines, another is 20) → dictionary lost; either compress the long ones or split into a different organon
- Mixed frame styles (some `╔═╗`, some `┌─┐`) → pick one weight and apply to all entries
- More than 6-7 entries → dictionary becomes a list; consider switching organon to `list` with markers
- No `★` on any entry, no synthesis after → dictionary is just a catalog, not an artifact pointing somewhere
