# Organon: lattice

A partial-order structure: some pairs of items are comparable (one is "above" the other), and some are not. Distinct from a tree because items can have multiple parents; distinct from a graph because edges have a directional ordering meaning.

## To lattice-ify an idea

1. **Pick an ordering relation.** Subset, generality, dependency, precedence, refinement, abstraction, type-conformance.
2. **Place items.** Each item sits at some level. Some items have multiple parents (multiple things that are "more general"). Some pairs are incomparable — neither above nor below the other.
3. **Identify the top and bottom.** The top is the most general / most abstract / most encompassing element; the bottom is the most specific / null / contradiction.
4. **Find the meets and joins.** For two items, their *meet* is the most specific common ancestor; their *join* is the most general common descendant. These structural points are often the load-bearing concepts.

## What lattices surface

- **Multiple inheritance** — when an item has two non-comparable parents, the item participates in two conceptual lineages at once. That's information about the idea's mixed nature.
- **Incomparability** — pairs that have no ordering relationship. In a tree everything is implicitly ordered through the root; lattices honest about the items that genuinely aren't.
- **Diamond patterns** — two items with two common children, where the children are not directly comparable. The diamond names a structural ambiguity.

## Pairing

Lattices pair with **tree-finding** (a lattice that turns out to be a tree is a special case) and with **dimension-identification** (each axis of generality is a dimension). They're the right organon when the idea's structure has multiple inheritance, partial-orders, or genuine incomparability — situations a tree would distort.
