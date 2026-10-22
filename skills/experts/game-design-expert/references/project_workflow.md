# Improve the target game

Detect new versus existing project before editing gameplay or artwork. Use the
target's rules, available tools, and authorized resources. Choose a small amount
of evidence that resolves the actual design uncertainty.

## New game or expansion

1. Establish the shared brief below. Make the first goal and controls learnable
   through a playable opening with a distinctive interaction.
2. Prototype the uncertain action in its environment: moving through a current,
   using a partner's ability, carving a firing lane, or preparing a physical shot.
3. Review the prototype against the intended experience. Correct input, space,
   readability, or consequence before multiplying content that depends on them.
4. Expand through discoveries, practice, unexpected combinations, and memorable
   payoffs. A minimal first slice is execution order; finish the full requested scope.

## Existing game improvement

1. Inspect current documentation, real controls, representative gameplay, and
   established assets. Capture a baseline of the opening, later play, retry, and
   payoff appropriate to the request. Record initial observations before reading
   puzzle solutions when evaluating discoverability.
2. Name strengths to preserve and the weakest experiences with evidence: repeated
   solved tasks, delayed turns, indistinct hazards, hollow rewards, or generic art.
   Separate reasoning difficulty from timing, precision, and hazard pressure.
3. Choose a connected improvement with a clear hypothesis. For example, give a
   repetitive region a new use for an existing enemy attack, a readable visual
   cue, a safe introduction, and a later payoff using that interaction.
4. Implement, compare with the baseline, and inspect the surrounding experience.
   Retain good rooms and successful identity while correcting demonstrated weaknesses.

## Shared brief and assignments

Keep one concise brief in existing project planning documentation. Where no
planning document exists, use a short `docs/GAME_DESIGN.md`. Maintain decisions
and acceptance scenarios there instead of multiplying contracts.

Include only what the work needs:

- Promise, audience, main actions, meaningful decisions, controls, and opening hook.
- Progression: what players discover, practice, recombine, and gain; signature
  moments and quiet passages; failure and recovery behavior.
- Art direction: world materials, character identity and motion, readable hazards,
  important visual transformations, and accepted artwork to preserve.
- Relevant learning relationships and boundaries of scientific abstraction.
- Evidence scenarios, completion criteria, agent assessment, and correction path.

For parallel builds, give `html-game-parallel-builder` this brief before it defines
contracts. Each assignment receives its owned artifact, contribution to the
promise, relevant gameplay and art decisions, shared dependencies, and checks.
For example: a new ride-producing attack needs compatible enemy timing, player
attachment behavior, visual anticipation, and a level that makes the ride useful.
The manager resolves these dependencies before dispatch and reviews them together.

## Independent path to completion

Trace each milestone from prerequisites to final verification. Assets, preview
startup, test inputs, captures, artistic choices, and review must have an
agent-executable path. Resolve routine choices from user direction, project
evidence, and recorded defaults. Optional human responses are refinement input.

Use [testing_and_oracles.md](testing_and_oracles.md) to scale assessment to the
change. A failed check returns to focused correction and verification. Complete
authorized work through the final integrated result; state real unresolved tool
or environment failures accurately rather than treating missing evidence as a pass.
