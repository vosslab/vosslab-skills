# Learn from successful games

The user selected these six games as stronger examples. Evidence was inspected
on 2026-10-22: local READMEs, guidance, selected implementation, and existing
screenshots. This is not a new runtime playtest or measured retention study.
Use each case to change a decision in the target game, then assess that change.

Local source roots are `~/nsh/TYPESCRIPT/<repository>/`. Paths below identify
optional source artifacts rather than skill dependencies. When unavailable,
use the observations here and inspect the target game. Recheck current sources
before relying on tunable values or claiming a source game still behaves identically.

## Bad Cell Day

- **Observed:** Isp and Pac have different bodies and cooperative roles. Villain
  attacks can impede play or become a useful ride or shove. Sources:
  `bad-cell-day/README.md` and `bad-cell-day/src/level_friendly_fire.ts`.
- **Recorded preference:** preserve good rooms, meaningful partner contributions,
  expressive molecular shapes, and anatomical environments. Make patient recovery
  substantial in tissue, skin, and face. Source: `bad-cell-day/docs/HUMAN_GUIDANCE.md`.
- **Decision to borrow:** give an existing hazard a helpful use that requires
  partners to contribute differently. Carry success into a visible world change.
- **Inspect in the target:** execute the interaction with both roles; compare
  beginning, partial, and completed recovery at gameplay scale. Distinguish puzzle
  discovery from precision and timing demands.
- **Transfer limit:** cooperative dependence suits cooperative games. Organic
  cartoon tissue, exact character proportions, and organ counts belong to this game.

## Glycolysis-okimon

- **Observed:** enzyme followers, cofactors, and reaction products participate in
  progression. Substrate challenges reuse recruited enzymes, and wrong choices
  explain the selected enzyme's substrate. Sources: `glycolysis-okimon/docs/GAME_DESIGN.md`
  and `glycolysis-okimon/src/gameplay.ts`.
- **Design hypothesis:** resources and companions become more meaningful when
  later actions depend on their identities and uses.
- **Decision to borrow:** let players use what they collect. When teaching is
  relevant, make a subject relationship determine a choice or transformation.
- **Inspect in the target:** trace acquisition, use, feedback, and a later reuse;
  verify a correct choice depends on the relationship rather than collection order.
- **Transfer limit:** an enzyme system is appropriate to this topic. A new game
  may benefit from analogous relationships without a quiz or follower collection.

## Ms Taq Man

- **Observed:** queued turns support familiar maze steering; enemies and helpers
  change chase behavior, and primer collection produces a visible helix. Sources:
  `ms-taq-man/src/game/actor.ts` and `ms-taq-man/README.md`.
- **Recorded preference:** wild spectacle, helpful rewards, adjustable challenge,
  clear celebration, and messages outside the play board. Source:
  `ms-taq-man/docs/HUMAN_GUIDANCE.md`.
- **Decision to borrow:** polish the familiar main action, then surprise players
  through assistance, enemy roles, and visible consequences of movement.
- **Inspect in the target:** try early turn input near a junction, distinguish
  enemy behaviors, and check that effects preserve hazard and player readability.
- **Transfer limit:** more challenge is not always an improvement. Choose input
  buffering, audio defaults, and spectacle for the actual game and audience.

## Plaque Attack

- **Observed:** firing splits lipid hazards; carving tissue trades shelter for
  firing lanes. Campaign victories restore a patient view. Sources:
  `plaque-attack/README.md` and `plaque-attack/src/simulation.ts`.
- **Recorded preference:** put fun first, add organic medical scenes, and make
  recovery visible. Six surgeons begin with identical abilities so preference
  does not change difficulty. Source: `plaque-attack/docs/HUMAN_GUIDANCE.md`.
- **Decision to borrow:** give a simple action a spatial tradeoff and a satisfying
  consequence beyond the score. Allow expressive cosmetic identity choices.
- **Inspect in the target:** compare sheltered and carved situations; exercise
  a tool introduction with reduced competing pressure; compare recovery states.
  `plaque-attack/docs/DIFFICULTY_RUBRIC.md` distinguishes modeled demands from play.
- **Transfer limit:** splitting hazards and medical imagery are contextual.
  Preserve clear boundaries between arcade abstractions and biological claims.

## Super Bowling

- **Observed:** a trajectory preview supports shot preparation; actual collisions
  drive the cascade and audiovisual payoff. The preview models pre-contact flight.
  Sources: `super-bowling/README.md` and `super-bowling/src/simulation/preview.ts`.
- **Recorded preference:** milestones must close through manager, subagents, and
  executable evidence without waiting for player feedback. Source:
  `super-bowling/docs/HUMAN_GUIDANCE.md`.
- **Decision to borrow:** connect anticipation, commitment, consequence, and
  celebration. Let presentation amplify the outcome the simulation produced.
- **Inspect in the target:** compare preview with intended launch behavior, then
  inspect real impacts, camera, sound, and outcome together, including reduced motion.
- **Transfer limit:** elaborate physics and huge object counts are not necessary
  to achieve dramatic payoff. A deterministic completion run cannot prove enjoyment.

## Steroid Quest

- **Observed:** a small core control set supports currents, rebounds, rides,
  binding, and a transcription finale across six regions, with checkpoints.
  Sources: `steroid-quest-into-the-nucleus/README.md` and
  `steroid-quest-into-the-nucleus/src/levels/surprise_patterns.ts`.
- **Recorded preference:** keep players wondering what strange thing comes next;
  use signature encounters, helpful chaos, absurd shortcuts, a wild first level,
  and quick recovery. Source:
  `steroid-quest-into-the-nucleus/docs/HUMAN_GUIDANCE.md`.
- **Decision to borrow:** retain dependable controls while the world supplies
  surprising interactions and fresh combinations throughout the journey.
- **Inspect in the target:** follow the sequence of actions within and between
  regions. Identify new discoveries, repetition, signature moments, and recovery;
  assess curiosity separately from increasing difficulty and travel duration.
- **Transfer limit:** fluid movement, cellular environments, campaign duration,
  and audio defaults are this game's choices. Transfer the cadence of discovery.

## Supporting cautions and boundaries

M.U.L.E. is not a success case. The user calls the project unsuccessful and reports
that its partially useful artwork bake-off cost too many tokens to continue.
`mule-game/docs/HUMAN_GUIDANCE.md` separately records overconstrained specifications
that produced similar designs. Apply the concise-brief and effort guidance in
[art_direction.md](art_direction.md).

`nobel-combat/docs/HUMAN_GUIDANCE.md` supplies a narrower identity lesson: judge
recognizable characters at their actual display scale. Guidance in
`virtual-lab-protocol-simulation/docs/HUMAN_GUIDANCE.md` supports consistent
physical state pairs and preservation of established artwork. These supporting
examples are not additions to the six-game success set or universal art pipelines.
