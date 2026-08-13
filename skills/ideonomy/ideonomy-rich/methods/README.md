# Method catalog

Browse-only index. The agent doesn't read this — it reads the picks from `bin/pick`. This file exists for humans to scan what's available.

## Operators (`operators/`)

The eight ideonomic operations, all traceable to Grace Kind's essays.

- **negation** — find core/definitional properties, identify each one's opposite, enumerate the opposite-set
- **substitution** — hold all properties constant except one; swap that property's value
- **combination** — cross two organons; each pair is a candidate composite idea
- **organon-construction** — capture the idea as a structured artifact; the structure surfaces gaps
- **dimension-identification** — name the axes along which versions of this idea can vary
- **tree-finding** — find parents, children, siblings, and levels of generality (the dendritic structure)
- **abstraction-lift** — strip domain-specific surface features; expose the structural shape underneath
- **cross-domain-reinstantiation** — re-instantiate the abstracted form in a different domain

## Organons (`organons/`)

The structured artifacts Grace names in her intro, tree (which she identifies as a fundamental ideonomic pattern), plus 10 distinct structural shapes added later.

**Grace-named:**
- **list** — ordered or unordered enumeration
- **chart** — 2D grid where rows and columns are dimensions, cells contain instances
- **graph** — nodes and edges
- **atlas** — bound collection of maps over the same territory at different scales/themes
- **scale** — ordered axis with marked positions
- **dictionary** — term-and-definition pairs
- **tree** — branching hierarchy

**Added (each structurally distinct from the above):**
- **matrix** — 2D grid where cells contain *relations* / *evaluations*, not instances (Pugh, decision, confusion)
- **cycle** — closed scale where endpoints connect (calendar, OODA, life cycle)
- **spectrum** — continuous axis with no canonical marked points
- **timeline** — anisotropic axis (past fixed, future open); direction is load-bearing
- **lattice** — partial-order; some pairs comparable, others not (subset, type hierarchies)
- **map** — 2D spatial layout where *position itself* carries information (subway, mind, concept)
- **notation** — the syntax IS the organon (music, chemistry, dance, regex)
- **procedure** — ordered sequence where order is load-bearing (recipe, algorithm, ritual)
- **state-machine** — nodes are states; edges are conditional transitions
- **periodic-grid** — saturated chart where empty cells are *predictions*, not gaps

## Dimension-prompts (`dimension-prompts/`)

Question templates that surface an idea's dimensions. Grace describes the method ("identify the axes along which versions of this could vary"); this catalog gives 25 ready-to-pick prompts grouped loosely by family.

**Temporal** — longevity, rate, cyclicity, age, direction
**Scale & magnitude** — size, cardinality, scope
**Structure** — homogeneity, hierarchicalness, modularity, connectivity, symmetry
**Agency & causation** — animacy, autonomy, intentionality
**Origin** — naturalness, source, discovery-vs-invention
**Function** — purpose, side-effect, reversibility
**Embodiment & knowability** — materiality, visibility, predictability
**Complexity & polarity** — complexity, decomposability, polarity, distribution

## A note on recipes

There is deliberately no `recipes/` directory — no saved-combinations layer. Combinations are what the picker produces by drawing operators × organons × dimension-prompts; freezing past combinations into named recipes pulls the picker toward defaults and works against the random-selection mechanism that makes the skill useful in the first place. Some historical recipe sketches survive under `examples/historical-recipes/` for browsing only; they are not part of the active catalog.
