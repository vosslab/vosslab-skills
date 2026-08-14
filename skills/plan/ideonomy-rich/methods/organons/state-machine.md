# Organon: state-machine

Nodes are *states*; edges are *transitions* labeled with the conditions or events that fire them. Distinct from a graph because there is a "current state" and edges are conditional — only some are available at any moment.

## To state-machine-ify an idea

1. **Enumerate the states** the idea can occupy. *Logged-in / logged-out*; *single / married / divorced*; *unread / read / archived*; *learning / mastery / forgetting*. Each state is a self-consistent configuration.
2. **Identify transitions.** What event or condition takes the system from state A to state B? Label each edge with that trigger.
3. **Mark unreachable transitions.** Pairs of states with no direct transition between them — the idea can only get from A to C by going through B. The forced path is itself information.
4. **Identify start and accept states.** Where does the system begin? Where does it stop, succeed, or terminate? Some states are absorbing (you don't leave once you arrive); naming them is part of the analysis.

## What state-machines surface

- **Forbidden transitions** — pairs of states the idea can't move between directly. The forbidden pairs reveal structural constraints that the noun-form of the idea hides.
- **Cycles vs absorbing states** — does the idea have a stable equilibrium, or does it cycle indefinitely? The answer is often non-obvious until you draw the machine.
- **Trigger asymmetries** — when the trigger to enter a state is hard to fire and the trigger to leave is easy (or vice versa), the state is fragile or sticky. These are properties of the idea that words rarely capture.

## Pairing

State-machines pair with **negation** (negating a state's defining condition gives its anti-state, which often turns out to already be in the machine) and with **cycle** (a state machine with a closed orbit *is* a cycle). They're the right organon when the idea has discrete configurations and conditional movement between them — workflows, lifecycles, computational systems, protocols.
