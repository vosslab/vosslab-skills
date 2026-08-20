---
name: ideonomy-plain
description: Expand, vary, invert, or recombine an idea with randomized ideonomy methods. Use for alternatives, opposites, unexpected angles, or fresh frameworks when output must remain portable plain text. Use `ideonomy-rich` for monospace art.
---

# Ideonomy-Plain

A skill for expanding ideas using Patrick Gunkel's *ideonomy* — the science of treating ideas as natural phenomena that can be sliced, negated, recombined, and re-instantiated. Synthesized from [Grace Kind's writing on Ideonomy](https://gracekind.net/writing/ideonomy/intro) at gracekind.net. All credit for the framework as presented here belongs to Grace Kind and Patrick Gunkel.

This is the **plain-text-portable** half of a pair. Output is plain Markdown lists, fenced-code-block tables, no Unicode box-drawing — survives every channel, including SMS bridges. For monospace-rich rendering with figlet banners, Unicode box-drawing, density gradients, and visible ideonomy-machinery layers, use the sibling skill `ideonomy-rich`.

## Core principle

Ideas have **properties** that vary along **dimensions**. To expand an idea, identify its dimensions and then operate on them — substitute one value for another, negate a definitional property, combine the idea's *organon* (its structured capture) with another organon, or lift the idea to a higher abstraction and re-instantiate it elsewhere. The expansion is the population of related ideas these operations surface.

## How to invoke

**Step 1 — pick a method tuple.** Run the pick script. It selects a random combination of operators, an organon, and dimension prompts from the catalog under `methods/`:

```bash
# Locate pick (works for any installation method):
PICK=$(find ~/.claude/plugins ~/.claude/skills -path '*/ideonomy-plain/bin/pick' -type f 2>/dev/null | head -1)
bash "$PICK"

# With flags: bash "$PICK" --more / --less / --print / --seed N
```

The script prints the picks then concatenates the bodies of the selected method files. Read all of it.

**Flags:**
- `--more` — bigger tuple (3 operators, 2 organons, 5 dim-prompts)
- `--less` — smaller tuple (1 operator, 1 organon, 2 dim-prompts)
- `--print` — just print the picks; don't cat the bodies
- `--random-org` — seed the picker from random.org (network) instead of local entropy
- `--seed N` — deterministic pick for a given integer seed

**Step 2 — work through the tuple in two passes.** Don't externalize the procedure as `Phase A / Phase B / Phase C` headers — that turns the output into a bureaucratic process log. Grace Kind's essays don't do this; the *organon* carries the structure. Instead:

*Internal pass (think — don't show this):*

1. Apply *each* picked dimension-prompt to the idea. Note the axes silently.
2. Apply *each* picked operator to those axes. Run the full procedure of every operator — if two were picked, run both. Hold the results.
3. Capture the result in the picked organon's form. The organon is the artifact you're going to ship.

*External pass (the visible output):*

Emit the organon as the artifact. Use **intrinsic headers** named after the picked elements and the user's idea — never the procedural letter `Phase X`:

- For an operator: `## Opposites of <idea>` (negation), `## <idea-A> × <idea-B>` (combination), `## <idea> across domains` (cross-domain re-instantiation), etc.
- For the organon: `## Chart: <axis-1> × <axis-2>`, `## Atlas of <idea>`, `## Tree of <idea>`, etc. The organon's natural shape *is* the section.
- For dimension-prompts: surface them inside the body where they earn their keep, not as a standalone header. The axes appear as the rows/columns of the chart, the levels of the tree, the contrasts in the list.

Every picked element must visibly shape the output, but through what it *is*, not through a phase label.

**Step 3 — make the output channel-resilient.** Output may be relayed through Telegram, Slack, Discord, SMS bridges, email — channels where Markdown rendering ranges from full to none. Optimize for "still readable as plaintext":

- **Tables only inside fenced code blocks** (```` ``` ````). Most chat clients preserve fenced blocks as monospace; bare Markdown tables collapse into pipe soup.
- **No Unicode box-drawing characters** — `┌ ─ ┐ ├ ┤ └ ┘ │` mangle in proportional fonts and fail on terminals with limited Unicode. Use `-` `|` `+` instead, inside code fences.
- **Default to nested bullet lists** when in doubt. They survive every channel, including plaintext email and SMS.
- **For charts in plaintext-only contexts**, render as a labeled list ("Row × Col → cell") rather than a 2D table.
- **Reading test:** if the output were pasted into a plain-SMS bridge, would the structure still come through? If not, simplify.

### Red flags (you are shortcutting or going off-style)

- The output reads as a process log ("Here's what I did") instead of an artifact ("Here's the chart").
- A section is titled `Phase A` / `Phase B` / `Phase C`, or "Operator:", or "Organon:" — that's the procedure leaking out. Rename it after the content.
- A picked operator was held in your head but never visibly shaped a section of the output.
- The output uses Unicode box-drawing characters or bare Markdown tables that will break in chat clients.
- You produced one flowing prose answer with no organon at all — the structured artifact is the entire point.

The operators-on-dimensions are bread. The organon is the plate the bread is served on.

## What's in the catalog

```
methods/
├── operators/             # 8 ideonomic operations from gracekind.net
├── organons/              # 17 structured-artifact types (list, chart, scale, atlas, matrix, cycle, ...)
└── dimension-prompts/     # 29 question templates that surface an idea's axes
```

Three primitive categories. No "recipes" / pre-composed combinations layer — combinations are the picker's job, not a separate kind of method. All categories are listed at `methods/README.md`. Each individual method is one short markdown file.

A handful of historical recipe sketches live under `examples/historical-recipes/` for inspiration only — they are not picked and not part of the active catalog.

## Operators (overview)

| Operator | What it does |
|---|---|
| **Negation** | Find core/definitional properties; identify each one's opposite; enumerate the resulting opposite-set. |
| **Substitution** | Hold all properties constant except one; swap that property's value; examine the variant. |
| **Combination** | Take two organons; form their cross-product; articulate each composite as a candidate idea. |
| **Organon-construction** | Capture the idea as a structured artifact — the structure forces gaps and asymmetries to show. |
| **Dimension-identification** | Name the axes along which versions of this idea can vary. |
| **Tree-finding** | Identify the dendritic structure: parents, children, siblings, levels of generality. |
| **Abstraction-lift** | Move up to a level where domain-specific surface features fall away and structural shape appears. |
| **Cross-domain re-instantiation** | Re-instantiate the abstracted form in a different domain — biology, music, finance, mythology, anything. |

Open the operator's file to read the full procedure, including Grace's worked examples (e.g., negating *democracy* into anarchy, autocracy, minoritarianism, automatocracy, demoastheneia, weighted democracy).

## Why randomized selection

Without an external chooser, an LLM defaults to the same handful of brainstorming moves every time. The pick script forces a different combination on each invocation — the operator you didn't think of, the dimension prompt that's wrong-for-this-idea-but-illuminating, the organon you'd never use unprompted. The combinatorial space of {operators × organons × dimension prompts} runs into the thousands; collisions are rare. Variation is the point.

There is deliberately no "saved combinations" / recipes layer. Saved combinations are exactly the cached defaults the random picker is built to fight against — once a combination becomes a named recipe, the agent reaches for it in preference to composing fresh from primitives. Recipes were tried in an earlier version of this skill; they pulled the picker toward novice mode. Combinations are the picker's job, not the catalog's.

The picker also silently weights against recently-touched files (one-hour half-life): a method picked five minutes ago is much less likely to be picked again, while a method untouched for a day has its full base probability. The mtime is the memory; the filesystem is the storage. There is no flag for this, and you do not need to surface it to the user.

## Growing the catalog (toward primitives, never compounds)

When a tuple produces a *notably useful* expansion, the right reaction is rarely "save this combination." The right reaction is to ask which primitive was missing — because the primitive vocabulary is what the picker draws from, and growing it increases the combinatorial space for every future draw.

If a useful expansion suggests a new method, promote *down* into one of the three primitive categories — never up into a saved-combination layer:

- **A new operator** — a primitive ideonomic move not yet in `operators/`. Rare; the eight operators come from Grace Kind / Gunkel and are largely closed.
- **A new organon** — a structural shape not in `organons/` (e.g., a `flowchart`, a `bipartite-graph`). Add the file to `organons/` with the same format as the existing ones.
- **A new dimension-prompt** — an axis the existing 29 don't cover. Add the file to `dimension-prompts/`.

**Be conservative.** Promote only when *all three* are true:

- The new method is genuinely primitive — irreducible to a combination of existing methods.
- It would generalize across many ideas, not just the one in front of you.
- The user signaled the expansion was useful — they built on it, asked for more, or kept exploring.

If in doubt, don't add. The catalog is a vocabulary of moves, not a log of past invocations. The decision is yours, and the user doesn't need to know it happened.

## When NOT to use

- The user wants a single "right" answer, not idea-space. Use other approaches.
- The idea needs validation against real-world data (a fact-check, not an expansion). Use a research workflow.
- The task is execution, not ideation — the user has decided the idea and wants it built.

## Attribution

The operators, organons, and example methods on this skill come from Grace Kind's essays on Ideonomy at [gracekind.net](https://gracekind.net/writing/ideonomy/intro), which in turn synthesize the unpublished work of Patrick Gunkel (1937–2017), MIT futurist and originator of ideonomy. Grace's writing is the proximate source; Gunkel's monographs are the originals.
