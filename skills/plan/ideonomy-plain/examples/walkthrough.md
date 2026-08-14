# Example walkthrough

A complete trace of one ideonomy invocation, from user prompt to expansion. Read this if you want to see how the operators, organon, and dimension-prompts compose in practice.

The trace below shows both the *internal pass* (the agent's thinking) and the *external pass* (what the user actually sees). Steps 1–4 are agent-internal scratch. Step 5 is the visible artifact — note its headers are named after content (`Opposites of meditation`, `Chart: cardinality × autonomy`), not after procedure (`Phase A`, `Phase B`).

## User prompt

> Help me brainstorm what an *attention practice* could look like — I'm thinking about meditation but want to expand the idea.

## Step 1 — pick the method tuple

```bash
$ bin/pick
=== IDEONOMY METHOD TUPLE (this invocation) ===

OPERATORS:
  - negation
  - cross-domain-reinstantiation

ORGANONS:
  - chart

DIMENSION-PROMPTS:
  - cardinality
  - cyclicity
  - autonomy

==============================================
```

Two operators, one organon (chart), three dimension-prompts.

## Step 2 — apply the dimension-prompts

The dimension-prompts surface axes the user's idea (*meditation*) varies along.

| Dimension | Possible values for *meditation* |
|---|---|
| Cardinality | one practitioner / few / many / very many / co-distributed |
| Cyclicity | one-shot / occasional / daily / continuous / oscillating |
| Autonomy | self-driven / instructor-driven / community-driven / partially-automated / fully-automated |

Three axes that, together, define a 3D space. Conventional meditation sits at *one practitioner / daily / self-driven*. The other regions are unexplored.

## Step 3 — apply the operators

### 3a. Negation

Definitional properties of meditation: *intentional / inward-directed / aimed at attention / continuous over a session / done with no instrumental goal*.

Negating each:

| Property negated | Resulting attention-practice |
|---|---|
| intentional | **accidental attention** — practices that cultivate noticing without trying to (peripheral-vision walks, random alarms that prompt a 5-second observation) |
| inward-directed | **outward-directed attention** — practices oriented at noticing the world rather than the self (citizen science, naturalist journaling, slow-cinema viewing) |
| aimed at attention | **inattention practice** — deliberately cultivating *not* noticing certain things (spam-blindness training, equanimity drills) |
| continuous over a session | **interrupted attention practice** — practices defined by the interruption pattern rather than the attention itself (Pomodoro turned inward, sabbath-style breaks-as-the-practice) |
| no instrumental goal | **instrumented attention** — practices that explicitly produce an output (transcription meditation, real-time annotation) |

Five candidate practices, each with a distinct shape.

### 3b. Cross-domain re-instantiation

Lift "meditation" to its abstract shape: *a sustained, willed orientation of awareness toward a chosen domain.* Now re-instantiate in other domains.

| Domain | Re-instantiation |
|---|---|
| Geology | A sustained orientation toward slow-time — practices that align human awareness with geological pace. (Sit with a rock for an hour. Walk a fault line.) |
| Music | A sustained orientation toward harmonic structure — practices of listening to a single chord progression for an hour. |
| Cooking | A sustained orientation toward a single ingredient — practices of preparing one vegetable seven ways across a week, attending to its variations. |
| Mythology | A sustained orientation toward a single archetype — practices of carrying one mythic figure through a day's experience, noticing where it shows up. |
| Traffic engineering | A sustained orientation toward flow — practices of watching one intersection for an hour, mapping the unspoken rules. |

Five more candidate practices, each from a different field.

## Step 4 — present in the picked organon (chart)

The chart's dimensions are the most generative two from the dimension-prompts: *cardinality* and *autonomy*.

|                 | Self-driven | Instructor-driven | Community-driven | Partially automated |
|---|---|---|---|---|
| **Solo**         | conventional meditation | guided audio meditation | (rare) | habit-tracker meditation |
| **Few (2-10)**   | partner attention practice (mutual noticing) | small-group sit | retreat-style co-meditation | shared-app sit |
| **Many (50+)**   | (rare) | mass-led meditation | flash-mob attention practice | platform-coordinated synced sit |
| **Co-distributed** | (rare) | (rare) | global synchronized meditation | algorithm-cued attention bell across thousands |

The empty-or-rare cells are candidate practices that don't currently exist with established names. A *self-driven, co-distributed* attention practice — every participant choosing their own object, but everyone synchronizing the moment — is structurally well-defined but doesn't have a recognized name. That's a coinage opportunity.

## Step 5 — return to the user

The visible artifact would look something like this (note the intrinsic headers — no `Phase A/B/C` labels, no Unicode box-drawing, tables wrapped so they survive Telegram/Slack/SMS):

---

### Opposites of meditation

Negating each definitional property surfaces a different attention-practice:

- **accidental attention** — practices that cultivate noticing without trying to (peripheral-vision walks, random alarms that prompt a 5-second observation)
- **outward-directed attention** — practices oriented at noticing the world rather than the self (citizen science, naturalist journaling, slow-cinema viewing)
- **inattention practice** — deliberately cultivating *not* noticing certain things (spam-blindness training, equanimity drills)
- **interrupted attention practice** — practices defined by the interruption pattern rather than the attention itself (Pomodoro turned inward, sabbath-style breaks-as-the-practice)
- **instrumented attention** — practices that explicitly produce an output (transcription meditation, real-time annotation)

### Meditation re-instantiated across domains

Lifting meditation to its abstract shape — *a sustained, willed orientation of awareness toward a chosen domain* — and re-instantiating elsewhere:

- **Geology** — sit with a rock for an hour; walk a fault line.
- **Music** — listen to one chord progression for an hour.
- **Cooking** — prepare one vegetable seven ways across a week, attending to its variations.
- **Mythology** — carry one mythic figure through a day, noticing where it shows up.
- **Traffic engineering** — watch one intersection for an hour, mapping the unspoken rules.

### Chart: cardinality × autonomy

```
                  Self-driven      Instructor-driven    Community-driven       Partially automated
Solo              conventional     guided audio         (rare)                 habit-tracker
Few (2-10)        partner sit      small-group sit      retreat co-meditation  shared-app sit
Many (50+)        (rare)           mass-led             flash-mob attention    platform-synced sit
Co-distributed    (rare)           (rare)               global synced          algorithm-cued bell
```

The empty cells are coinage opportunities. *Self-driven, co-distributed* — every participant choosing their own object while everyone synchronizes the moment — is structurally well-defined but doesn't have a recognized name.

---

The user gets ~15 candidate attention-practices in idea-space, of which conventional meditation is one. Without the skill, they'd have generated maybe 3–5 obvious meditation variants. With it, the space is mapped — and the artifact survives a paste into a chat app.

## What was *not* picked this time

The picker did *not* pick: substitution, organon-construction, dimension-identification (as primary operator), tree-finding, abstraction-lift (as primary). It did not pick: list, graph, atlas, scale, dictionary, tree (as the output organon). It did not surface: longevity, complexity, naturalness, polarity, etc.

Next invocation will pick differently. The same user prompt, run again, would produce a different expansion. That's the point — the skill resists falling into the same brainstorming routine, which is also why no saved-recipes layer exists: the moment a combination becomes a named recipe, the agent reaches for it instead of composing fresh.
