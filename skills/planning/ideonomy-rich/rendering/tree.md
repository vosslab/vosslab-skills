# Rendering: tree

A tree is a branching hierarchy — parents above, siblings across, children below. Walk all four directions; the asymmetries surface ideas.

## Form

Use `╭── ├── │   ╰──` connectors for a soft, hand-drawn feel. Save `┌── ├── │   └──` for stricter, classification-style trees.

## Worked example — *meditation: walking the tree*

```
                              ╔═══════════════════════════════╗
                              ║   coordination of attention   ║   ← root
                              ╚═══════════════╦═══════════════╝
                                              │
                ┌─────────────────────────────┼─────────────────────────────┐
                │                             │                             │
        ╭───────┴───────╮             ╭───────┴───────╮             ╭───────┴───────╮
        │  market       │             │  jury         │             │  meditation   │   ← siblings
        │  (price)      │             │  (deliberation)│            │  (the idea)   │
        ╰───────────────╯             ╰───────────────╯             ╰───────┬───────╯
                                                                            │
                                            ┌───────────┬──────────────┬────┴────────┬──────────────┐
                                            │           │              │             │              │
                                          standup    1:1            retreat        ritual         brainstorm   ← children
                                            ▒           ▒              █             ▒              ▒
```

Density `█` / `▒` shows canonical-vs-marginal at the leaf level — *retreat* is the most-saturated child, the rest are partial.

## Conventions

- Root in `╔═╗` double-line — the most important node visually
- Mid-level nodes in `╭─╮` rounded — soft, intermediate
- Leaves are bare text or `▒`/`█` density blocks
- Vertical drop with `│`, horizontal gather with `┴`, branch with `├` or `┤`
- Siblings always horizontally aligned at the same row
- Walk the levels: root above, siblings across, children below

## Drama

The point of a tree is usually one of:

1. **Empty branch** — a child slot that should exist but doesn't. Mark with `◇` and isolate visually.
2. **Cross-level sibling** — at one level up, the peers reframe the idea (meditation → markets, juries, festivals). Often the most surprising expansion. Render this *one level up* with a banner `═══ AT ONE LEVEL UP ═══` so the reader sees the reframe.
3. **Mixed-level mistake** — two siblings at very different levels of generality. Mark with `▲` and a note: the taxonomy is sloppy here.

## Anti-patterns

- All branches the same depth → suspiciously uniform; real trees are jagged
- Root too general (e.g. "things") → walked too far up; pick a more useful root
- Children mixing sub-types and parts → pick one relation type per tree, stick with it
