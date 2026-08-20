# Rendering: chart

A chart is a 2D grid: rows = values of one dimension, columns = values of another. Cells hold instances, names, or `◇` for empty/coinage.

## Form

Double-line outer frame for the chart proper. Single-line internal divisions. The first column (row labels) divided from data with `║`; data columns separated with `│`.

## Worked example — *meditation: cardinality × autonomy*

```
╔══════════════════╦═══════════════╤═══════════════╤════════════════╤═══════════════╗
║                  ║ self-driven   │ instructor    │ community      │ partly-auto   ║
╠══════════════════╬═══════════════╪═══════════════╪════════════════╪═══════════════╣
║ solo             ║ ● conventional│   guided      │      ◇         │ habit-tracker ║
║ few (2-10)       ║   partner sit │   small group │  retreat co-m. │ shared-app sit║
║ many (50+)       ║      ◇        │   mass-led    │  flash-mob     │ platform sync ║
║ co-distributed   ║      ★        │      ◇        │  global synced │ algo-cued bell║
╚══════════════════╩═══════════════╧═══════════════╧════════════════╧═══════════════╝

                                                            ★ self-driven, co-distributed:
                                                            ╭───────────────────────────╮
                                                            │  no recognized name yet   │
                                                            │  (coinage opportunity)    │
                                                            ╰───────────────────────────╯
```

## Conventions

- `●` = canonical instance for that cell
- `◇` = empty / no recognized concept (a typed prediction the chart is making)
- `★` = the cell that surprised, the pivot of the artifact
- Column widths uniform unless one axis genuinely demands more
- Cell text > column width: coin a single-word label, don't wrap

## Drama

Charts are made to be read. The empty `◇` cells aren't gaps — they're the point. After the chart, call out the most interesting `◇` or `★` in a small rounded box `╭─╮` with an arrow back to its grid position. This is where the reader lands.

## Anti-patterns

- All cells full → the dimensions aren't independent, or the territory is densely populated and the chart isn't surfacing anything new. Try different dimensions.
- Diagonal pattern (full on diagonal, empty off-diagonal) → dimensions are correlated. Pick one.
- One row full, others empty → that "row dimension" only varies in one value among real instances. Drop it as a dimension.
