# Playful training game style

Design guide for arcade-style onboarding trainers aimed at older learners
(lab students, new hires, technical apprentices). Sibling document to
[docs/FUN_VIBES_DESIGN_STYLE.md](FUN_VIBES_DESIGN_STYLE.md), which targets
middle-school kids. Same engine. Tighter tone.

## Scope

This guide is portable across TypeScript browser games and interactive
trainers WHEN the audience is age 15-30, learning a real-world skill
(lab safety, equipment, protocols, professional practice), and the
desired emotional outcome is COMPETENCE BUILDING rather than collection
or completion.

Use this doc when the player should leave saying:

> I feel more competent and want to keep practicing.

Not:

> I want the coolest theme.

It is NOT for:

- Middle-school audiences (use FUN_VIBES_DESIGN_STYLE.md).
- Adult productivity tools or dashboards.
- Formal certification exams or record-bearing assessments, unless used
  only as a practice layer before the real assessment.
- Long-form courseware that needs lecture-style depth.

## Framing

The mental model is "arcade onboarding trainer," not "kid arcade game."

- Fast. Visible progress. Immediate feedback.
- Playful enough that practicing voluntarily is plausible.
- Restrained enough that an instructor recommending it does not feel
  embarrassed.
- Mistakes are pedagogical, never punitive.

## Core principles

Five principles override others when they conflict.

- **Competence is the product.** Every interaction should leave the
  learner more capable. Reward systems are scaffolding for repetition,
  not the goal.
- **Wrong answers are the lesson.** This is the single highest-value
  screen in the entire trainer. Make it readable, specific, and
  context-rich. See "Wrong-answer teaching contract" below.
- **Momentum is the product.** Fast feedback, clear state transitions,
  no dead time between scenarios.
- **Polish over expansion.** Tune what exists before adding modes. A
  trainer with two strong scenario types replays better than one with
  six half-baked ones.
- **Loud feedback only when it serves recall.** Color, motion, and
  emphasis are tools for marking what the learner should remember, not
  decoration.

## What goes loud (keep)

- Saturated colors for status: green for correct, amber for warning,
  red for hazard. Match real lab/safety semantics.
- Mid-bright accent palette for buttons and progress. Bright, not candy.
- Large fonts on scenario stems and on the wrong-answer teaching panel.
- Bold borders/outlines on the correct answer when it reveals.
- Streak indicators with subtle pulse on milestone (3, 5, 10).
- Progress rings and competency stamps as visible long-term progress.
- Big rounded buttons with hover lift and active settle.

## What goes quiet (avoid or soften)

- Confetti bursts. Restrict to genuine milestones (module complete,
  certification-ready). Never on every correct answer.
- "UNSTOPPABLE!" style ALL CAPS exclamations. Replace with calm
  affirmations: "Strong run", "Solid streak", "Sharp work".
- Mascot-heavy reaction art. A subtle helper-TA character is fine for
  flavor; do not make it perform every event.
- Candy palettes (pink/lime/violet pop). Use lab-clean brights.
- "Coolest theme" coin-shop emphasis. Themes exist; they are not the
  goal of play.
- Long help text walls. Same rule as kid arcade.
- Shaming copy. "Wrong" alone is shaming; "Not quite - here's why" is
  not.

## Reward systems

- **One reward currency**, treated as professional progress, not loot.
  Suggested vocabulary: "lab credits", "XP", "competency points",
  "progress tokens". Avoid "coins" if the trainer is graded coursework.
- **Performance stats coexist as feedback**, not competing currencies:
  accuracy, longest streak, fastest module. These read as self-knowledge.
- **Badges over coins.** Competency stamps per topic ("PPE: Verified",
  "Chemical storage: Verified", "Biohazard waste: Verified"). Visible
  on a progress board.
- **Unlockables tied to competence.** Cosmetic bench themes, equipment
  stickers, lab-coat accents - unlocked by demonstrating mastery in the
  matching topic, not by grinding credits. Earned, not bought.
- **Daily or session goals.** Stratified: one "easy refresher", one
  "scenario you fumbled last time", one "new topic". Keep the pool
  varied so it does not feel like a chore.
- **Anti-grind cap.** Same rule as the kid version: hard ceiling on
  reward-granting events per day so a learner cannot speedrun
  completion. Encourages spaced practice.
- **Visible "ready for wet lab" checklist** as the long-term goal.
  Competency stamps roll up into a readable readiness statement.

## Wrong-answer teaching contract

The single most important rule in this doc. Every wrong answer must
deliver, in this order:

1. **What the learner picked**, repeated back verbatim.
2. **The correct answer**, marked clearly.
3. **Why** - one sentence of context that connects the choice to a
   real-world consequence or principle.

Concrete example for a lab-waste scenario:

> You chose: dispose in regular trash
> Correct: dispose in biohazard waste
> Why: Anything contaminated with cells or biological material goes
> into biohazard waste so it can be autoclaved before entering the
> waste stream.

Anti-example (do not ship):

> Incorrect.

The teaching panel is also the most-frequent failure-mode UI to test
on mobile - make sure the continue affordance is reachable without
scrolling, and the panel itself is tap-to-continue.

## Scenario authenticity

Scenarios should sound like real lab situations, not textbook trivia. The
game can be polished and still fail if learners think "this would never
happen." Prefer:

- Messy but realistic context.
- Common beginner mistakes as distractors.
- Decisions with real consequences.
- Short explanations tied to actual lab practice.

Avoid trick questions, obscure policy trivia, and scenarios that punish
learners for not knowing unstated assumptions. If a scenario only makes
sense to someone who already wrote it, rewrite it.

## Feedback rules

- **Correct**: check badge in the button corner (not overlaying the
  label). Non-destructive correctness signal: outline glow, brighter
  border, brief pulse. Do not flood the whole button green if slot
  colors carry identity. Streak counter ticks up. Affirmation rotates
  from a calm pool: "Got it.", "Solid.", "Nice catch.", "Sharp."
- **Wrong**: shake the button, X badge in corner (not overlaying the
  label), reveal correct answer with check badge + glow + the
  teaching panel above. Copy is matter-of-fact: "Not quite - here's
  the answer.", "Common mistake - see why.", "Close - one detail off."
- **Affirmation never repeats consecutively.**
- **Sound off by default.** Mute toggle persisted. Required for
  shared lab spaces.

## Interaction rules

- **Big touch targets** (min 56px). Required for the trainer to work
  on a benchtop tablet or shared kiosk.
- **Keyboard parity.** 1-N keys for choices, Enter to advance, Esc to
  return to menu. Lab students often work one-handed.
- **Reversible = friction-free.** Theme switch, lesson select, mode
  toggle: no confirms.
- **Irreversible = confirm.** Resetting progress, deleting a saved
  scenario, abandoning a partial module: confirm modal. Same arcade
  pattern, calmer copy.
- **No accidental destruction.** Same rule as kid game. A tablet
  smudge should not wipe progress.

## Suggested game modes

These slot into the same engine as the stems quiz. Each is a scenario
type - the engine handles draw, answer, scoring, feedback identically.

- **Safety Sprint**: PPE, chemical storage, waste handling. Rapid-fire
  one-correct choice per scenario.
- **Protocol Builder**: ordered-step puzzle. "Choose the correct next
  step in this protocol." Reveals the rationale after each step.
- **Spot the Mistake**: scenario with an image or text describing lab
  behavior. Identify which element is unsafe or incorrect.
- **Instrument Quest**: match tool to use case. Builds equipment
  recognition.
- **Emergency Drill**: branching response. "What do you do when
  something goes wrong?" Teaches under-pressure decision-making.
- **Lab Culture**: communication, authorship, data integrity,
  troubleshooting etiquette. The "soft skills" topic most lab trainings
  skip.

## Reward catalog (suggested)

- **Competency stamps**: per-topic mastery markers ("Biohazard: Verified",
  "Centrifuge: Verified"). Permanent.
- **Bench themes**: cosmetic backdrop for the play screen. Unlocked by
  topic mastery, not bought.
- **Equipment stickers**: small decorative badges for the progress board.
  Earned for finishing scenario sets.
- **Lab-coat accents**: cosmetic only, signals tenure ("100 scenarios
  cleared", "All topics passed once").
- **Readiness checklist**: the only "real" reward. Visible on home,
  fills in as competencies stamp. Goal of the trainer.

## Visual identity

- **Lab-clean palette.** Bright but not candy. Think clinical surfaces:
  white card, dark text, saturated accents (true red for hazard,
  forest green for safe, amber for warn). Themed backgrounds can be
  more decorative; the play surface stays clean.
- **Two-dimension theme catalog**: category (Lab Specialization:
  microbio / chem / physics / clinical) + rarity tier (Standard /
  Advanced / Specialist). Same shape as the kid game's
  category-plus-rarity, different vocabulary.
- **Helper TA character** is optional. If included, keep them subtle:
  small portrait, calm reactions, no party mode. Skip if it reads as
  childish for your audience.
- **Progress board** as the dominant home-screen element. Stats and
  competency stamps tell the learner where they stand.

## Architecture rules that protect the vibe

Same as the kid game - these are Layer 1 rules.

- **Centralized event dispatch** (`record_event(GameEvent)`). One funnel
  for every gameplay event. TS compiler enforces every goal/badge has a
  handler.
- **Versioned save schema.** Single key, version field, forward
  migration. Critical for a multi-session trainer - losing progress
  destroys trust.
- **One reward currency**, performance stats separate.
- **Cachebust assets at build time.** Random dev-server port. Same
  rules as kid game.
- **Mode-gated complexity.** Quick refresher modes skip retry queues
  and resurface logic; long-form modes turn them on.

## Anti-patterns to refuse

These look reasonable in review and kill the trainer's tone.

- "Make it more game-y with confetti on every correct."
- "Add a mascot that cheers loudly."
- "Use pink and lime green for the theme - kids love it." (audience is
  not kids)
- "Replace the explanation with just 'Correct' or 'Wrong'."
- "Hide the why-text behind a 'Show more' toggle."
- "Add badges for trivial things like 'opened the trainer'."
- "Make rewards purchasable, not earned." (kills competence framing)
- "Use formal courseware tone, drop the playfulness." (kills replay)

If a reviewer pushes any of the above WITHOUT citing a specific
usability failure or pedagogical regression, the finding is auto-
rejected.

## The load-bearing rule

Inject this into every reviewer / QA prompt for trainers in this style:

> Only flag playful color, large buttons, scenario framing, or
> reward systems as a problem if they cause a specific usability
> failure (unreadable text, hidden content, broken layout, keyboard
> failure, visual ambiguity) OR a specific pedagogical regression
> (the learner cannot tell what they got wrong, the explanation is
> missing or vague, the reward overshadows the lesson).

Aesthetic restraint and "feels too playful for lab training" are not
valid findings on their own.

## Portability checklist

Day-one MUST-HAVES:

- [ ] One reward currency, plus performance stats as feedback only.
- [ ] Wrong-answer teaching contract: picked / correct / why.
- [ ] Big touch targets (min 56px), keyboard parity, mobile padding.
- [ ] Versioned save schema with forward migration.
- [ ] Centralized event dispatch for rewardable events.
- [ ] Cachebust at build time + random dev-server port.
- [ ] At least one scenario mode wired end-to-end.

SHOULD-HAVE, add as the loop matures:

- [ ] Competency stamps with visible progress board.
- [ ] Two to three scenario modes (Safety Sprint, Protocol Builder, etc).
- [ ] Streak system with calm milestone pulses.
- [ ] Daily/session goal draw with stratified mix.

NICE-TO-HAVE, ship after the core feels right:

- [ ] Bench themes / equipment stickers / lab-coat accents.
- [ ] Helper TA character with restrained reactions.
- [ ] "Ready for wet lab" rollup checklist.
- [ ] Cross-topic competency badges (e.g. "All safety topics passed").

## See also

- [docs/FUN_VIBES_DESIGN_STYLE.md](FUN_VIBES_DESIGN_STYLE.md): sibling
  doc for younger audiences. Same engine, louder tone, kid-arcade
  framing.
- `docs/REPO_STYLE.md`: repo-wide conventions and the
  five core engineering philosophies.
- `docs/MARKDOWN_STYLE.md`: writing conventions for
  this doc.
