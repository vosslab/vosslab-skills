# Organon: procedure

An ordered sequence where order is load-bearing. Distinct from a list because the items can't be reordered without changing what the procedure *is*. Recipes, algorithms, rituals, protocols, choreographies, multi-track scores.

## To procedure-ify an idea

1. **State the goal-state** the procedure produces.
2. **Enumerate the steps** in order. Number them. Each step has a precondition (what must be true before it runs) and a postcondition (what's true after).
3. **Mark the dependencies.** Which steps must come before which? Sometimes the procedure has a strict order; sometimes only partial order, with parallel branches.
4. **Identify failure modes per step.** Where can each step fail, and what's the recovery?

## What procedures surface

- **Implicit prerequisites** — steps depend on conditions you'd never have stated explicitly until forced to write them down.
- **Recoverability per step** — some steps are reversible if they fail; some aren't. The asymmetry tells you where the risk lives.
- **Hidden parallelism** — when you map dependencies, you often discover steps that *could* run in parallel but conventionally don't. Each is a potential variant of the procedure.
- **Step-level substitution** — substituting one step for another (different ingredient, different algorithm, different ritual phrase) produces variants of the whole procedure.

## Pairing

Procedures pair with **tree-finding** (each step can be decomposed into sub-procedures) and with **substitution** (per-step variants are exactly the substitution operator applied at procedure-step granularity). They're the right organon when sequence matters and the idea is fundamentally about *how to do something* rather than *what something is*.
