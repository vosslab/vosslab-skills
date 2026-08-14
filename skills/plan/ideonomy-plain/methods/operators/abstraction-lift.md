# Abstraction-lift

Move up to a higher level of abstraction where domain-specific surface features fall away and the underlying structural shape becomes visible.

Per Grace, summarizing Gunkel's premise: *"over-specialization obscures cross-disciplinary patterns; higher-level abstraction reveals hidden connections between fields."* Lifting is the operation that exposes those connections.

## Procedure

1. **State the most concrete framing first.** Write the idea down in the most specific, domain-bound, surface-feature-heavy way you can. (You're going to peel layers off it.)
2. **Strip the proper nouns and domain vocabulary.** Replace specific entities with generic placeholders. Replace domain-specific verbs with their structural equivalents (negotiate → exchange → transfer).
3. **State what's underneath.** What's the structural shape? Often it's a *process*, *relation*, *topology*, *flow*, *transformation*, *equilibrium*, or *bifurcation*. Name the shape.
4. **Sanity-check.** The abstracted form should be recognizable in *other* domains. If you can't name another domain where this shape appears, you haven't lifted high enough.

## Why it works

Specific things look unique. Their specificity is mostly surface. When you remove the surface, the underlying shape is one of a small library of recurring patterns — feedback loop, gradient ascent, marketplace, immune response, allocation problem, signal-and-noise, propagation through a network. Once you've named the shape, every other instance of it becomes a comparator and a source of moves.

## Pairing

Abstraction-lift is the setup for **cross-domain re-instantiation** — you lift in order to drop the lifted form into a different domain. The pair is the engine behind most analogical reasoning. (See the `cross-domain-lift` recipe.)

## Worked example

Original: "Our company's authentication service has a single point of failure — if that server goes down, nobody can log in."

Strip:
- "Our company's authentication service" → *a gatekeeper*
- "single point of failure" → *single instance with no redundancy*
- "nobody can log in" → *the system it gates becomes inaccessible*

Lifted: *A unique gatekeeper guards access to a system; if the gatekeeper fails, the system is unreachable.*

Recognizable in other domains:
- Biology: a single chokepoint enzyme in a metabolic pathway
- City planning: a single bridge connecting two districts
- Mythology: the single ferryman across the Styx
- Software: any single-master architecture

Each of those domains has worked out its own answers (redundant copies, parallel pathways, ferry-fleet, multi-master replication). Each answer is a candidate solution to lift back down to the original problem.
