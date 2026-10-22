---
name: game-design-expert
description: Use when designing or improving a game's controls, mechanics, surprise, progression, character identity, or art direction, especially when a working game feels repetitive, generic, or unrewarding.
---

# Game design expert

Turn an intended player experience into a playable, distinctive game. Use the
six successful games in the references as evidence for decisions, with books
providing supporting principles. Adapt their strengths to the current game.

## Governing design principles

- **Fun first, teaching when relevant.** Make the main action satisfying and
  let relevant understanding emerge through play.
- **Expect the unexpected = fun.** Keep players curious about what happens
  next through fresh situations, helpful chaos, discoveries, and payoffs.
- **Create a world worth exploring, characters worth recognizing, and
  consequences worth seeing.** Connect expressive art to the experience.
- **Finish independently.** If the human goes to sleep, the manager and
  subagents still have a complete path through every milestone.

## Workflow and reference routing

1. Select the design problem with
   [references/task_selection.md](references/task_selection.md). Use the
   user's request and project evidence to resolve routine choices.
2. Detect a new versus existing project before edits. Follow
   [references/project_workflow.md](references/project_workflow.md) to establish
   the shared brief or inspect the current experience and preserve its strengths.
3. Read the relevant cases in
   [references/case_studies.md](references/case_studies.md). Turn each borrowed
   lesson into a decision for this game's audience, genre, and controls.
4. Shape actions, choices, surprise, progression, and recovery using
   [references/design_principles.md](references/design_principles.md).
   Prototype the greatest uncertainty, then complete the requested scope.
5. For characters, environments, or visual consequences, use
   [references/art_direction.md](references/art_direction.md). Carry artistic
   intent into gameplay and asset assignments, then inspect the integrated view.
6. Implement or coordinate the requested improvements. Follow
   [references/testing_and_oracles.md](references/testing_and_oracles.md) for
   proportional evidence, independent assessment, correction, and completion.

Use [references/topic_index.md](references/topic_index.md) for focused lookup.
For deeper book evidence, consult
[references/reference_survey.md](references/reference_survey.md) and
[references/local_books.md](references/local_books.md). The committed guidance
works when the optional books and example repositories are absent.

## Boundaries and specialist handoffs

- Use `html-game-parallel-builder` when a modular TypeScript game needs parallel
  implementation. It owns dispatch, contracts, integration, serving, and delivery;
  this skill supplies the shared creative brief and experience assessment.
- Use `typescript-engineer` for type design and `svg-creator-expert` for editable
  SVG production. Use available image tools for other requested asset formats.
  Choose specialists for the actual task rather than assembling a default team.
- Consult the target's `docs/FUN_VIBES_DESIGN_STYLE.md` and
  `docs/PLAYFUL_TRAINING_GAME_STYLE.md` when available. Their canonical sources
  live in `starter-repo-template/templates/typescript/docs/`; keep guide copies
  out of skills. The focused references here remain sufficient without them.
- Keep routine code maintenance in the normal engineering workflow. Activate
  this skill when a decision about the player experience needs design judgment.

## Completion and evidence

For implementation requests, finish the integrated improvement and its checks;
for design-only requests, deliver actionable decisions and an executable path
to acceptance. State what changed, why, evidence inspected, and remaining limits.
Use behavior tests for correctness and proportionate agent assessment for
experience quality. Keep claims about human enjoyment or learning tied to actual
human evidence. Optional feedback never becomes a milestone dependency.
