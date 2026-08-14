# Organon: tree

A branching hierarchy. The idea, plus its parents, children, and siblings; recursively.

## To tree-ify an idea

1. **Identify a root.** A category general enough to contain the idea and its peers. (Sometimes the idea itself is the root, with the rest of the tree growing downward.)
2. **Recursively decompose.** For each node, list its children. Each child is either a sub-type, a part, or a sub-process — pick *one* relation type for the whole tree and stick with it (don't mix sub-typing and part-of in the same tree).
3. **Reach leaves.** Stop decomposing when nodes are atomic enough to be useful for the question at hand.
4. **Walk laterally.** At every level, list siblings — peers at the same level of generality.

## Why trees are a fundamental ideonomic organon

Per Grace, summarizing Gunkel, trees are "key to classification, decision-making, memory, information theory, government, computer programs." Trees show up everywhere because they're a structurally minimal way to express *containment with non-overlap*.

A well-formed tree:

- Has exactly one parent per non-root node.
- Children are mutually exclusive within their level.
- Children are collectively exhaustive of the parent (or, where they aren't, the gap is itself informative).

The discipline of well-formed-ness is the analytical work the tree does.

## What trees surface

- **Empty branches** — the parent has children A, B, D, but no C. Often C is a missing concept ready to be invented.
- **Mixed levels** — siblings at very different levels of generality reveals a sloppy taxonomy and points to a needed re-leveling.
- **Forced choices of relation type** — the act of picking *sub-type vs part-of vs sub-process* surfaces ambiguities in the original idea.

## Pairing

Trees are the output of the **tree-finding** operator. They're inputs to **substitution** when you substitute siblings for the original; they're inputs to **abstraction-lift** when you walk up to the root.
