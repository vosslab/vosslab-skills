# Fun vibes design style

> This file is vendored. Local changes can and will be overwritten by propagation.

Design playful browser games around satisfying actions, surprising situations, and a world worth
spending time in. **Fun first, teaching when relevant.** Let learning emerge from play or offer it
at a natural pause. A teaching feature earns its place by improving the experience.

Use both game guides together for games serving younger and older players. This guide emphasizes
the inviting arcade experience; [PLAYFUL_TRAINING_GAME_STYLE.md](PLAYFUL_TRAINING_GAME_STYLE.md)
adds the older-learner and subject-practice lens. Start with audience and planning, then use the
contents to find gameplay, artwork, implementation, or acceptance guidance.

## Table of contents

- [Audience and planning](#audience-and-planning)
  - [Choose the intended experience](#choose-the-intended-experience)
  - [Plan for independent completion](#plan-for-independent-completion)
- [Gameplay and pacing](#gameplay-and-pacing)
  - [Make the action rewarding](#make-the-action-rewarding)
  - [Tune feel before effects](#tune-feel-before-effects)
  - [Expect the unexpected](#expect-the-unexpected)
  - [Make recovery part of play](#make-recovery-part-of-play)
  - [Add rewards with purpose](#add-rewards-with-purpose)
    - [Quiz arcade pattern](#quiz-arcade-pattern)
- [Artwork and presentation](#artwork-and-presentation)
  - [Give the world character](#give-the-world-character)
    - [Shape before surface detail](#shape-before-surface-detail)
    - [Give details a reason](#give-details-a-reason)
    - [Make accomplishment visibly matter](#make-accomplishment-visibly-matter)
    - [Leave room for invention](#leave-room-for-invention)
    - [Brief and inspect assets](#brief-and-inspect-assets)
  - [Keep spectacle readable](#keep-spectacle-readable)
- [Implementation and acceptance](#implementation-and-acceptance)
  - [Engineering that preserves play](#engineering-that-preserves-play)
  - [Iterate against the promise](#iterate-against-the-promise)
  - [Design review checklist](#design-review-checklist)
- [Examples and references](#examples-and-references)
  - [Learn from these games](#learn-from-these-games)
  - [Book sources and applications](#book-sources-and-applications)
  - [See also](#see-also)

## Audience and planning

### Choose the intended experience

Use this guide for arcade games, cooperative puzzles, adventures, and playful learning games.
Bright colors, expressive characters, and ridiculous spectacle can suit adults as well as children.
Choose the tone from the game's promise and audience, rather than an age-based palette rule.

The original younger-player emphasis remains useful within a game built for both audiences:

- Make the first goal visible, teach controls through action, and keep required reading concise.
- Give older or experienced players meaningful choices, combinations to master, and optional
  depth while keeping the entry experience welcoming.
- Consider age, reading confidence, subject knowledge, and gaming experience separately. A
  younger player may be an expert gamer; an adult may need a gentle introduction to the controls.
- Use the same satisfying core actions for both audiences. Let optional explanations, hints,
  routes, and challenges accommodate different needs within the shared game.

Write the promise in one sentence: "Two friends turn a villain's attack into a ride" or "Shape a
bowling shot and watch a huge rack tumble." Name the action, the interesting situation, and the
payoff. Start with one playable example of that promise before expanding the campaign.

[PLAYFUL_TRAINING_GAME_STYLE.md](PLAYFUL_TRAINING_GAME_STYLE.md) adds guidance for games with a
learning purpose. The shared gameplay, artwork, and iteration guidance lives here. Neither guide
requires a quiz engine, shop, daily goals, persistent saves, or a particular framework.

### Plan for independent completion

**If the human goes to sleep, the manager and subagents must still have a complete path to
finish the entire plan.** Plan milestones should not require human interaction. Replace visible
and hidden human dependencies with independent agent assessments and automated behavior tests.
Apply this to implementation, artwork, integration, review, correction, and final acceptance.

- Give each milestone an owned result, executable checks, independent assessment criteria, and
  a correction path. The manager resolves findings and verifies the integrated result before
  marking the milestone complete. Carry this through the final milestone.
- Resolve routine design choices from the user's direction, existing artwork, and observed
  behavior. Record the rationale and let independent assessment challenge it.
- Audit prerequisites as well as explicit gates: obtaining assets, starting previews, supplying
  test inputs, capturing evidence, selecting an art direction, and reviewing results must all
  have an agent-executable path using available tools and authorized resources.
- Replace "ask the user to playtest" with automated actual-control runs covering opening,
  progression, failure, recovery, and completion, plus independent review of the experience.
- Replace "wait for art approval" with independent inspection of rendered scenes at gameplay
  size against the established direction, including character identity and changed world states.
- Replace "human confirms it feels fun" with independent assessments of control, pacing,
  surprise, readability, and payoff, supported by behavior tests and captured play evidence.
- Replace "manual final smoke test" with a reproducible check of the integrated build. Exercise
  real controls and shipping render paths; use deterministic state probes for focused diagnosis.
- Treat optional human feedback as input for refinement, with a defined agent assessment when
  none arrives. Avoid milestones that silently wait for a reply or an unassigned manual action.

Agent assessments are design judgments; automated tests demonstrate behavior. Neither establishes
human enjoyment or learning gains. State those evidence limits while completing the authorized
deliverable. Keep work within the user's authorized scope and choose completion criteria that
agents can satisfy without inventing an approval requirement.

## Gameplay and pacing

### Make the action rewarding

- **Polish the main verb.** Moving, aiming, jumping, splitting, steering, or choosing should be
  satisfying before rewards and menus are added. Tune the activity players repeat most.
- **Give choices consequences.** A route, timing decision, partner assignment, or resource use
  should change what happens next. Make the tradeoff visible enough to reason about.
- **Build mastery through variation.** Introduce a pattern, let players use it, then change its
  context or combine it with another. New colors and larger counts alone do not create depth.
- **Keep controls stable.** A few expressive inputs can support many situations. Let the world
  supply new problems before asking players to learn another button.
- **Make progress tangible.** Open a route, grow a party, build a trail, restore a patient, or
  clear a physical space. Numbers can reinforce a change the player can already see.
- **Make another attempt inviting.** Show what happened and return promptly to a useful decision.
  Preserve earned progress where that fits the game. Fair failure can remain part of the fun.

### Tune feel before effects

Steve Swink's game-feel framework connects control, simulated space, and presentation. Work on
them together: a movement speed only makes sense beside the corridor, landing area, or target.

- Tune acceleration, braking, turn acceptance, jump timing, and collision response in an actual
  encounter. Buffered turns or forgiving input windows should help express the player's intent.
- Make visible contact agree with the collision model. Keep important surfaces and openings clear.
- Match animation, sound, particles, and camera motion to the event they emphasize. A large impact
  deserves a different response from a small pickup; silence and stillness also create contrast.
- Let the camera show the decision before it celebrates the result. Keep hazards, landing zones,
  and the player's position readable during zooms or shake.
- Preserve the actual outcome. A bowling cascade looks impressive because real pins fall;
  presentation should explain and amplify that event.
- Check input and frame pacing on the intended device. Extra effects that delay control weaken
  the very sensation they are meant to improve.

### Expect the unexpected

Keep players wondering what the game will throw at them next. Introduce fresh situations
regularly throughout play: a strange encounter, unexpected ally, new use for a familiar tool,
environmental transformation, secret route, or spectacular chain reaction. Surprise is part of
the appeal in its own right; it can create delight, curiosity, humor, or a welcome advantage.

Teach reliable rules, then arrange them into unexpected situations. An enemy attack can become
transport; a shelter can become a firing lane; a familiar current can carry the player somewhere
new. Surprise feels earned when players can understand it afterward.

- Show a distinctive interaction early. Teach through a safe, playable encounter with a clear goal.
- Give each region or chapter a signature moment with a different action or spatial problem.
- Keep discoveries coming within regions too. Look for stretches where players repeat a solved
  action without a new decision, sight, or payoff, and give those stretches a worthwhile turn.
- Vary what arrives: a complication, helpful chaos, a comic interruption, a change of scale,
  or a quiet discovery. New enemies and increasing difficulty are only some of the possibilities.
- Alternate discovery, practice, pressure, payoff, and breathing room. Interest need not rise by
  making every level harder or filling every second with motion.
- Pace surprises around the player's activity. Give each discovery time to register and be
  enjoyed; use the next twist before the situation grows stale. There is no universal timer.
- When introducing a tool or rule, ease other demands so players can notice what changed.
- Signal new dangers in time to respond, keep controls dependable, and make recovery quick.
  Authored encounters and combinations of existing rules can sustain surprise across a campaign.
- Separate reasoning difficulty from execution, timing, and hazard pressure. An easy-to-understand
  room may still demand tight jumps; a slow room may contain a difficult cooperative puzzle.
- In cooperative games, give both players meaningful contributions and opportunities to trade
  roles. Parallel walking is weaker than helping a partner do something they cannot do alone.
- Use optional secrets and side routes for curiosity. Extend required play with worthwhile
  encounters, rather than travel padding, mandatory grinding, or minimum-duration timers.
- Make victory depend on the actions the game promises. Keep incomplete goals legible and give
  players a clear route back to unfinished work.

### Make recovery part of play

- Distinguish a readable, fair setback from a broken control or unclear rule. Fix the cause of
  confusion; preserve challenges that players can understand and improve at.
- Place retries near the next interesting decision. Return to a calm, usable state with a visible
  route forward, including after a missed ride, dropped object, or separated partner.
- Keep completed milestones when repeating them adds no worthwhile challenge.
- Offer help that acts visibly in the world: a repairing companion, a return current, or a route
  cue. Show what assistance did so the player still understands the result.
- Let success land before showing results: the final pop, escape, fall, or transformation is the
  payoff. Keep the next action easy to reach afterward.
- Require a fresh press for a new screen's action so held movement or fire cannot skip the result.

### Add rewards with purpose

Mastery, discovery, cooperation, and spectacle can carry a game without a reward economy.

- If a shop serves the experience, prefer one spendable cosmetic currency and distinguish it from
  score or lifetime achievement. Domain resources such as ATP and NADH have different jobs and
  need not be collapsed into that currency.
- Let the first optional reward arrive while the player is still discovering the loop. Tune its
  timing through play rather than assuming every game needs the same unlock schedule.
- Make streaks and milestone celebrations recognize worthwhile play. Keep them from discouraging
  experimentation or turning a recoverable mistake into a reason to quit.
- Add daily goals only when repeat sessions suit the game. Give them varied, meaningful actions;
  missed days should not erase progress or create an obligation to play.
- Keep cosmetic preview and equipment swaps immediate. Confirm spending or destructive resets
  when the consequence cannot be easily undone.

#### Quiz arcade pattern

For a game whose main action really is answering questions:

- Use large, readable stems and choices, generous touch targets, and keyboard shortcuts.
- Keep slot colors stable. Mark feedback with a corner badge and outline without covering labels.
- Show the chosen answer, the correction, and a useful reason. Let the learner control reading
  time; a quick animation should not dismiss the explanation.
- Rotate brief praise where it adds personality. Celebrate milestones more strongly than each
  individual answer.
- Use short rounds or spaced retries when they improve practice. Keep distractors plausible and
  answers unambiguous; adapt a thin pool instead of padding it with irrelevant choices.

## Artwork and presentation

### Give the world character

Create a world worth exploring, characters worth recognizing, and consequences worth seeing.
Express the game's identity through its forms, materials, movement, and transformations.
Art direction is part of the appeal from the first playable scene. Expressive faces, interesting
shapes, rich environments, and satisfying animation can be pleasurable in themselves; each
detail does not need an instructional or mechanical purpose.

Aim for **fun, unique, organic artwork that feels lived in**. Organic means forms have growth,
weight, material, and history; it does not require every setting to become biological. A bowling
lane can feel used and cared for, just as a cell can feel crowded and alive.

Let the setting affect surfaces, motion, obstacles, and atmosphere. Inside a body, folds,
crowding, currents, and irregular growth can make the location tangible. Choose a coherent
direction for each game: organic cartoon biology, bowling spectacle, and recognizable human
caricatures call for different forms and materials.

When available, use the `vosslab-skills:svg-creator-expert` workflow for original, editable SVG
assets. Its useful sequence is recognition, construction, coherent line and value hierarchy,
semantic SVG groups, then inspection through the real game renderer.

#### Shape before surface detail

- Give each important character a recognizable silhouette, posture, and way of moving. Start
  from the subject: molecular shapes, a surgeon's tools, a heavy ball, or a folded membrane.
- Choose proportions and poses that express identity and relationships: a tall, narrow partner
  beside a broad, heavy partner creates a recognizable cast. Carry identity through action states.
- Build large masses and negative spaces first. For a bold cartoon direction, heavier outer
  contours, quieter inner lines, and a few clear values can explain form. Match the treatment
  to the chosen art direction.
- Share a visual language across the cast while preserving distinct shapes. Use color as another
  identity cue alongside silhouette, labels, and motion.

#### Give details a reason

- Shape tissue into folds, bulges, compressed seams, branching vessels, and overlapping layers.
  Vary curves deliberately; use clusters and quiet gaps rather than uniform decorative scatter.
- Put wear where use would cause it: polished contact edges, lane scuffs, repaired panels,
  mismatched fasteners, rubbed handles, or a character's well-used equipment.
- Add small stories: a crooked repair, a tucked-away belonging, an overgrown passage, or debris
  caught in a current. Choose details that fit this place and its inhabitants.
- Let humor come from form and behavior: an overly proud enzyme, a wobbling load, a stubborn
  organelle, or a villain carried away by their own attack.
- Let play change the art: eroded shelter, repaired DNA, healthier tissue, a growing companion
  trail, or a visibly bound receptor. World changes make progress personal.
- Reserve the clearest edges and strongest separation for actors, hazards, and usable surfaces.
  Keep background texture quieter. Make a decorated platform's landing edge unambiguous.

#### Make accomplishment visibly matter

Give success a subject players care about: a recovering patient, a restored place, a rescued
companion, or a spectacular physical result. Show the consequence in that subject's appearance
and behavior as well as in the score.

- Make beginning, intermediate, and completed states substantially different at gameplay size.
  In a recovery scene, let skin, expression, surrounding tissue, and the whole body participate
  when the story calls for them to recover.
- Give contrasting states coherent color ranges, shapes, and surface qualities. In Bad Cell Day,
  warm healthy tissue and sickly, mottled growth establish a useful relationship. Choose palettes
  for the particular world; this is an example, not a universal biological color code.
- Preserve identity, composition, and recognizable anatomy across states so players can connect
  the change to their actions. Let recovery follow organic boundaries when the subject is organic.
- Compare before, middle, and after views side by side in the actual game composition. Check
  whether the transformation reads without counters, then check it with the normal interface.
- Establish one representative transformation before extending the treatment to a whole set.
  Keep successful artwork as the starting point for refinement.

#### Leave room for invention

Keep briefs short: identity, personality, intended experience, gameplay role, display size, and
the technical constraints the delivery path actually needs. Attribute required traits to the
human direction or concrete evidence; keep proposed treatments visibly optional.

Develop one strong direction by default. When an unresolved visual choice merits comparison,
use a few inexpensive silhouettes or small rendered samples with distinct design ideas. Choose
the useful direction before producing finished assets. Keep exploration proportional to the
decision and its token and time cost; a full artwork bake-off is an optional experiment.

M.U.L.E. is a caution, not one of the successful-game examples: its recorded guidance describes
accumulated constraints making independent designs converge. The maintainer considers the project
unsuccessful, but reports that its artwork bake-off partly worked and was stopped because it used
too many tokens. Preserve both lessons: room for invention and economical exploration.

#### Brief and inspect assets

Describe the intended effect clearly while allowing the artist to find its form. For example:

> Create an editable SVG of a mischievous cargo-carrying vesicle that belongs in this crowded
> cell adventure. Make it feel alive, burdened by its cargo, and eager to move. Its identity and
> docking opening should read at gameplay size. Preserve that identity between idle and loaded
> states. Choose shapes and material details that express its personality within the game's art
> direction, and group the parts needed for animation.

Use subject references to understand structure and synthesize original geometry. Preserve a
stable `viewBox`, meaningful groups, and reusable parts where they help editing. Keep the SVG as
the authored source when delivery uses a raster or Canvas derivative.

Inspect the actual render on its real background at the smallest and largest intended sizes.
Check silhouette, action pose, clipping, contrast, and collision readability before adding more
detail. Valid XML and an attractive isolated preview do not establish that an asset works in play.

Ask whether the scene expresses this game's identity, characters remain distinctive at gameplay
scale, and consequences are worth watching. Compare state pairs for continuity and substantial
change. Check that the brief still leaves a meaningful creative choice.

These refinements draw on the supplied maintainer guidance for Bad Cell Day's patient recovery,
Plaque Attack's original medical-inspired scenes,
[M.U.L.E. art briefs](https://github.com/vosslab/mule-game/blob/main/docs/HUMAN_GUIDANCE.md), and
[Virtual Lab's asset identity and state pairs](https://github.com/vosslab/virtual-lab-protocol-simulation/blob/main/docs/HUMAN_GUIDANCE.md).
Carry over the underlying relationships; retain each game's chosen visual direction and pipeline.

### Keep spectacle readable

- Use saturated palettes, chunky shapes, expressive typography, and bold outlines when they fit
  the promise. Rich color and readable contrast can coexist.
- Make the playfield dominant. Put scores, explanations, and menus where they support the action.
  Fit the intended viewport; desktop-first games can use a wide stage without pretending to be
  portrait-first apps.
- Size important characters so expressions and interactions survive at gameplay scale.
- Vary feedback strength. Small successes need a quick response; milestones can earn confetti,
  camera emphasis, a character celebration, or a changed world.
- Keep text and hazards visible during effects. A celebration must not hide an active decision.
- Provide reduced-motion alternatives, visible focus, readable text, and cues beyond color or
  sound alone. Keep the outcome understandable with sound muted.
- Choose sound defaults for the setting. Shared-classroom play may start muted; a voluntary arcade
  may start audio after Start. Keep mute easy to find and honor the player's choice.

## Implementation and acceptance

### Engineering that preserves play

- Keep rules and outcomes authoritative in the game state. Drive related sound, animation, and
  rewards from those events so one action produces a coherent response.
- Use a shared event path when multiple systems consume the same event. Choose architecture for
  the actual game rather than introducing an achievement framework in advance.
- Version and migrate persistent progress when the game has saves. Session-only games can remain
  session-only. Make reset and replay behavior clear.
- Support the intended inputs consistently. Give menus keyboard access; make touch controls large
  and comfortably separated when touch play is supported. Pause safely on focus loss as needed.
- Verify the built artifact and fresh asset loading. Use content-versioned assets or appropriate
  cache headers. A different development port creates a new save origin; keep the origin stable
  when checking persistence.

### Iterate against the promise

Start with the smallest playable scene that can answer a design question. Decide what to observe:
whether the first goal is apparent, a turn is accepted, a partner contributes, a miss is understood,
or a new encounter changes strategy. Revise the part that fails before adding more content.

When optional player sessions are available, let the game explain itself before coaching. Record
what happened before interpreting intentions or reading the intended solution. Ask what they
tried, what they expected, and what they wanted to do next. Treat hesitation and repeated mistakes
as evidence to investigate, not automatic reasons to remove challenge.

Automated actual-control runs, deterministic probes, screenshots, and recordings can establish
reachability, state transitions, timing, and visual behavior. Label assisted or synthetic runs.
Save final named screenshots as WebP at quality 90 (`cwebp -q 90`), following `docs/REPO_STYLE.md`.
Inspect the encoded WebP and use its `.webp` filename in reports and documentation.
Separate those results from claims about enjoyment and learning. Player feedback can refine the
design when available; completing the plan must remain independent of that availability.

### Design review checklist

- [ ] The opening delivers the promised action and a reason to continue.
- [ ] Younger and older players have a welcoming entry and worthwhile depth within the same game.
- [ ] Controls feel dependable in the spaces where they are used.
- [ ] Choices change outcomes; later encounters develop familiar rules.
- [ ] Fresh situations arrive throughout play, with room to enjoy each discovery.
- [ ] Failure is understandable, and recovery returns to worthwhile play.
- [ ] Progress has a visible consequence, with a satisfying final payoff.
- [ ] Artwork has distinctive shapes, material character, and readable action states.
- [ ] Effects support the action; muted sound and reduced motion retain essential cues.
- [ ] Teaching is relevant and preserves the fun of the current interaction.
- [ ] Verification names its evidence and distinguishes working behavior from enjoyment.
- [ ] Every milestone, including final acceptance, can finish while the human is unavailable.

The load-bearing review rule:

> Keep expressive color, big shapes, playful motion, and spectacle when they serve the experience.
> A finding should identify a concrete problem in control, readability, accessibility, pacing,
> fairness, or the game's promise, with evidence and a focused correction.

## Examples and references

### Learn from these games

These six games were selected by the maintainer as stronger examples. The observations below
come from local READMEs, design guidance, selected implementation paths, and existing screenshots
reviewed on 2026-10-22. They suggest reusable design strengths; they are not measured retention,
learning outcomes, or a new human playtest. Repository links identify the source projects;
published builds may differ from the reviewed local checkouts.

- **[Bad Cell Day](https://github.com/vosslab/bad-cell-day)**: Isp holds a door while Pac reaches
  a rescue switch; later villain attacks become lifts or shoves. Different bodies, partner
  dependencies, and reusable hazards create situations worth discussing. Study
  [src/levels_tutorial.ts](https://github.com/vosslab/bad-cell-day/blob/main/src/levels_tutorial.ts)
  and the illustrated encounters in its README. Borrow reciprocal roles and playful interference.
- **[glycolysis-okimon](https://github.com/vosslab/glycolysis-okimon)**: cofactors enter reactions,
  products remain visible, and recruited enzymes answer shuffled substrate challenges. The party
  matters after collection. Study
  [src/gameplay.ts](https://github.com/vosslab/glycolysis-okimon/blob/main/src/gameplay.ts).
  Borrow resources with understandable uses and later situations that reuse earlier discoveries.
- **[Ms Taq Man](https://github.com/vosslab/ms-taq-man)**: steering after a primer builds a visible
  helix, while enzyme rivals and a helpful clamp change the chase. Study
  [src/game/player.ts](https://github.com/vosslab/ms-taq-man/blob/main/src/game/player.ts)
  and its README's controls and helper behavior. Borrow movement that transforms the world,
  legible assistance, and alternate achievable completion goals.
- **[Plaque Attack](https://github.com/vosslab/plaque-attack)**: firing splits a large hazard into
  smaller ones, and carving tissue trades shelter for a firing lane. Campaign clears restore a
  patient map. Study
  [src/weapons.ts](https://github.com/vosslab/plaque-attack/blob/main/src/weapons.ts).
  Borrow a simple verb with tactical consequences and a visible story payoff.
- **[Super Bowling](https://github.com/vosslab/super-bowling)**: a projected path supports shot
  planning; physical pin impacts drive audiovisual emphasis and a dramatic cascade. Study
  [src/simulation/preview.ts](https://github.com/vosslab/super-bowling/blob/main/src/simulation/preview.ts)
  and
  [src/app/impact_presentation.ts](https://github.com/vosslab/super-bowling/blob/main/src/app/impact_presentation.ts).
  Borrow anticipation, commitment, readable consequence, and shared spectator enjoyment.
- **[Steroid Quest](https://github.com/vosslab/steroid-quest-into-the-nucleus)**: three main keys
  support currents, organelle rebounds, rides, binding, and a transcription finale. Required
  encounters and checkpoints give the journey structure. Study
  [src/progression.ts](https://github.com/vosslab/steroid-quest-into-the-nucleus/blob/main/src/progression.ts)
  and
  [docs/LEVEL_DESIGN.md](https://github.com/vosslab/steroid-quest-into-the-nucleus/blob/main/docs/LEVEL_DESIGN.md).
  Its recorded direction is to keep players wondering what strange thing the cell will throw at
  them next. Borrow frequent surprising interactions, stable controls, and quick recovery.

### Book sources and applications

These are paraphrased design lenses from the supplied editions in the local
`~/nsh/MARKDOWN_BOOKS/game_design/` collection, not universal empirical laws or copied checklists.

- **Raph Koster, A Theory of Fun for Game Design (2013)**, chapter 3, "What Games Are": patterns,
  understanding, mastery, and boredom inform the practice-and-variation guidance. Ask what the
  player is still discovering once the first solution works.
- **Steve Swink, Game Feel: A Game Designer's Guide to Virtual Sensation (2009)**, "Defining Game
  Feel" and the input, response, context, polish, metaphor, and rules framework: tune control in
  its environment and make sensory effects agree with interaction.
- **Tracy Fullerton, Game Design Workshop, third edition (2014)**, "A Playcentric Design Process"
  and chapter 9, "Playtesting": define the intended experience, prototype early, observe without
  coaching, and revise from evidence.
- **Jesse Schell, The Art of Game Design, third edition (2019)**, "The Lens of Essential
  Experience", "Meaningful Choices", "The Lens of Moments", and "Interest Curves": protect the
  central promise, give decisions consequences, and arrange memorable peaks with quieter passages.

### See also

- [PLAYFUL_TRAINING_GAME_STYLE.md](PLAYFUL_TRAINING_GAME_STYLE.md): relevant teaching within play.
- `docs/REPO_STYLE.md`: shared engineering and maintenance principles, supplied by the base template.
- `docs/MARKDOWN_STYLE.md`: writing conventions, supplied by the base template.
