# Organon: graph

Nodes and edges. The idea, plus the entities related to it, plus the named relationships between them.

## To graph-ify an idea

1. **Place the idea as a central node.**
2. **Add neighbor nodes** for everything related to the idea — causes, effects, components, alternatives, near-synonyms, prerequisites, dependents.
3. **Label the edges.** Don't draw unlabeled lines. Each edge should have a verb or relationship name: *causes, requires, enables, contradicts, refines, instantiates, is-a-kind-of, depends-on*.
4. **Walk outward.** For each neighbor, repeat. The graph grows by accretion.
5. **Look for cycles, dead ends, and central hubs.** Central hubs (high-degree nodes) are concepts the original idea silently depends on. Cycles are mutual-dependence loops. Dead ends are where the graph stops being interesting.

## What graphs surface

- **Hidden hubs** — concepts that have many edges to your graph but were not the focus. These often turn out to be the *real* topic.
- **Disconnected components** — if your graph splits into pieces, the idea is two ideas under one name.
- **Edge labels you have to invent** — if you can't name the relationship between two nodes, the relationship is doing work you haven't articulated.

## Pairing

Graphs combine well with **tree-finding** (a graph minus its non-hierarchical edges is a tree; comparing the two reveals which structure better fits the territory) and with **cross-domain re-instantiation** (graphs travel well between domains because the structure is what re-instantiates, not the labels).
