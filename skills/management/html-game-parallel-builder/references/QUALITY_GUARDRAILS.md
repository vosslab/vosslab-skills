# Quality guardrails

Detail companion to [`../SKILL.md`](../SKILL.md). The control plane
keeps a short critical-guardrails list inline (the load-bearing rules
the skill fails without); this file carries the bottleneck rationale,
the rationalization table, the full red-flags list, and the
common-mistakes prose.

## Bottlenecks and mitigation

The skill bends wall clock without lowering the quality bar. The
sequential steps below are the minimum needed to keep the code good
under parallel authoring in a live/podcast context; minimize but do
not skip.

| Bottleneck | Time | Why sequential | Mitigation |
| --- | --- | --- | --- |
| UI preference interview | ~2 min | Must happen before any code. | Prepare a short checklist; ask before opening the repo. |
| Type contracts | ~5-10 min | Every agent needs the contracts before writing code. | Reuse the feature-area split from `game-type-patterns.md`; do not invent a new layout per game. Promote a shape to `src/types/` only on the third cross-module use, per `modular-type-design.md`. |
| Batch 1 foundation | ~2 min | Constants, characters, and game state define the data model all other modules depend on. | Keep Batch 1 to 3 files max; data model and state machine only, no UI, no game logic. |
| Smoke tests between batches | ~2 min each, 4 total | Each batch must pass before the next starts. | Tight smokes: build, load, console check, click one element. Save full playthroughs for the final batch. Reuse the recipe in `../templates/playwright_smoke_test.md`. |

The hidden bottleneck is skipping these steps. Without contracts,
debugging mismatches cost 60+ minutes. Without batching, all bugs
surface at the end in a 14-module pile. The sequential gates are
faster than the alternative.

Where time is NOT a bottleneck: subagent authoring within a batch is
fully parallel. Six subagents writing 14 files in 4 batches takes
~15 min of agent wall-clock time. Sequential overhead (contracts +
smoke tests) adds ~15 min. Total: ~30 min. Compare to all-at-once:
8 min authoring + 60 min debugging = 68 min.

## Independent component testing

Modules should be testable in isolation, without waiting for
integration. Each subagent's prompt includes instructions to write
their module so it degrades gracefully when other modules are absent:

- A display function should render something when called with
  hardcoded test data, even if the generator module does not exist
  yet.
- A data generator should be callable from the browser console with
  test inputs, even if no UI exists to trigger it.

This catches internal bugs (wrong property names, missing returns)
before integration, when the fix scope is one file instead of
fourteen.

## Complex module detection and splitting

A batch finishes as fast as its slowest agent. If one module is
significantly more complex than its batch-mates, it becomes the
bottleneck.

| Signal | Likely complex |
| --- | --- |
| Multiple content types (help topics, tooltips, explanations, summaries) | Yes -- split by content type. |
| More than 2 distinct UI screens or flows | Yes -- split by screen. |
| Both data generation AND display logic | Yes -- split generator from renderer. |
| Over ~400 lines expected | Yes -- find a split point. |

Two options when a module is complex:

1. Split it into smaller files assigned to separate agents in the
   same batch.
2. Reduce scope for the first pass.

Prefer option 2 (reduce scope) over option 1 (split files) when
possible. Splitting adds coordination overhead. Reducing scope
removes work entirely.

## Rationalization table

| Excuse | Reality |
| --- | --- |
| "Contracts take too long" | 10 min contracts vs 60 min debugging mismatches. Not negotiable. |
| "We can fix integration later" | Integration bugs compound. 2 mismatched modules = 1 fix. 14 mismatched modules = 20 fixes. |
| "Let's add all features now" | Get 2 working before adding 3 more. Scope creep killed every podcast build that tried it. |
| "Smoke tests slow us down" | 2 min smoke catches bugs worth 30 min of debugging. |
| "Agents can figure out the interface" | They cannot. Every generator/display pair mismatched without contracts. Every single one. |
| "I'll ask about UI preferences after" | UI rewrite cost 30 min. Asking first costs 2 min. |
| "requestAnimationFrame is optional" | Canvas will be blank. This is not optional. |
| "All agents can run at once" | Foundation agents must finish first. Batching is the whole point. |
| "One agent can handle this big module" | A batch finishes as fast as its slowest agent. Split or scope-reduce. |
| "We'll test it all together at the end" | Test each module in isolation first. |
| "TypeScript slows agents down" | `tsc --noEmit` between batches catches contract drift in seconds; the JS version found the same drift only at Playwright time. |
| "We can `as any` the tricky spot" | Forbidden outside brand constructors and save-file type guards. Route the problem to `typescript-engineer`. |
| "Parallel means we can lower the quality bar to hit the deadline" | No. The skill exists to hit the deadline AT the quality bar. Cutting contracts, smoke tests, or `tsc --noEmit` does not buy time; it moves the same time into integration debugging at the end. |

## Red flags - STOP

- Dispatching coding agents before contracts are written.
- Skipping a smoke test between batches.
- Skipping `tsc --noEmit` before a Playwright smoke.
- Adding features beyond the minimum viable scope in batch 3-4.
- Agent prompts that don't include the contracts list.
- Two agents assigned to the same file.
- No Playwright browser testing planned.
- Skipping UI preference gathering.
- One agent assigned a module with 4+ content types or 400+ expected
  lines without splitting or scope-reducing.
- Contracts written in JSDoc comments instead of `src/types/*.ts`.
- An agent prompt that does not name the type files it must import
  from.
- A batch declared green without `tsc --noEmit` passing.
- Any `as` cast outside a brand constructor or save-file type guard.
- `build_github_pages.sh` modified to produce single-file output.
- `export_single_file.sh` modified to write into `dist/`.

## Common mistakes

**Locally redeclaring a contract shape.** If a generator and a display
both need the same return type, export the type from
`src/types/<feature>.ts` and have both modules import it via
`import type`. Do not let each side define its own version; that is
the JSDoc-era trap in TypeScript clothing.

**Canvas in `innerHTML`.** Always use `requestAnimationFrame` after
`innerHTML` that creates a canvas. Always set canvas `width` and
`height` as element attributes. This is the #1 rendering bug in
browser games.

**Mixing build identities.** `build_github_pages.sh` is the GitHub
Pages release path; `export_single_file.sh` is the portable artifact
path. Each has a distinct output location (`dist/` vs `dist-single/`)
for a reason. Do not blend them.
