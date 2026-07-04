# Fun vibes design style

Design guide for kid-arcade learning games. Captures the principles that
make `stem-lesson-quiz-game` feel like an arcade, not school software. Use
this doc as a checklist when porting the vibe to a new game.

## Scope

This guide is portable across TypeScript browser games and interactive
learning tools WHEN the target tone is kid-arcade: playful, replayable,
saturated, reward-driven. It is intentionally opinionated for that genre.

It is NOT intended for:

- Adult productivity tools.
- Dashboards, scientific visualizations, BI tools.
- Serious training apps, formal courseware, certification platforms.
- Accessibility-first public services (the colors-and-juice rules will
  conflict with WCAG-strict tone guidelines).
- Minimalist portfolio sites.
- General-purpose UI component libraries.

Applying this doc outside its genre will make the result feel infantile
where it should feel professional. Use the portable rules below in
non-arcade projects; skip the kid-arcade rules entirely.

## Rule layers

The doc has two layers. Layer 1 ports to most TypeScript interactive
projects. Layer 2 applies only inside the kid-arcade genre.

### Layer 1 (portable interaction + engineering rules)

These travel to almost any interactive project:

- Polish over expansion.
- Momentum is the product (fast feedback, clear state transitions).
- Big touch targets, keyboard parity, mobile bottom padding.
- Wrong answers should teach, not punish.
- Versioned save schema with forward migration.
- Centralized event dispatch for rewardable events.
- Cachebust at build time + random dev-server port.
- No hidden destructive actions (confirm irreversibles).
- Visual QA (screenshot the visual states, do not just unit-test logic).
- Avoid long help text (UI should be self-explanatory).
- Do not flag bold style as a defect unless it causes a SPECIFIC
  usability failure (see the load-bearing rule).

### Layer 2 (kid-arcade-only rules)

These apply ONLY when the desired vibe is playful kid replay:

- Saturated arcade palettes.
- Coins as reward currency.
- Streak bonuses and milestone banners.
- Mascot character with reaction states.
- Confetti bursts.
- Cosmetic shop + theme purchases.
- Daily goals, completion bonuses, anti-grind caps.
- Rarity tiers (Common / Rare / Legendary).
- School-mascot-style theme packs.
- "Middle school kid" framing for design decisions.

If you are using Layer 1 rules only, skip Layer 2 entirely. Applying
Layer 2 to an adult tool is the exact failure mode this doc is designed
to prevent.

## Audience and frame

This doc is for game design, not engine code. The target player is a 12-year-old
who picked up the game voluntarily and will close it the moment it feels like
homework. Every rule below is in service of one question:

> Would a middle school kid voluntarily replay this?

Not "is it correct," not "is it accessible by enterprise standards," not "is
the UI minimal." Replayability is the goal. Learning is the side effect of
replay.

## Core principles

These five principles override the others when they conflict.

- **Loud feedback beats restraint.** Saturated colors, chunky buttons, big
  fonts, hard drop-shadows, juicy motion: these are features, not noise.
  Pastel palettes and "clean" minimalism kill kid energy on contact.
- **Polish over expansion.** Tune what exists before adding new systems. A
  game with two well-felt mechanics replays better than one with eight
  half-finished ones.
- **Momentum is the product.** Frictionless input, fast transitions,
  rotating praise lines, animated counters, streak banners. Every second of
  dead time loses a kid.
- **Kid safety beats friction reduction only for irreversible actions.**
  Reversible things (preview, equip swap, toggle) are friction-free. Things
  that spend currency or destroy progress get a confirm step, but a juicy
  arcade-styled one, not a beige browser dialog.
- **WCAG matters for readability, NOT for muting color.** Hit contrast targets
  via outlines, token swaps, and bolder text. Never via desaturation.

## What goes loud (keep)

- Saturated color palettes per theme: candy-bright, neon, electric.
- 1-N keys mapped to distinct hot colors, one per active choice (coral,
  sunflower, lime, violet for a 4-choice round; extend the palette for 6 or
  8). Slot color = slot identity, persistent across rounds.
- Question text 28px+, choice text 20px+, streak counter 32px+.
- Rounded sans (Fredoka or similar), border-radius 16px+, drop-shadows.
- Mascot reactions (idle, cheer, wobble, party). CSS/SVG, 4 frames.
- Confetti bursts on streak milestones (3, 5, 10, 20, 30+).
- Praise pools that rotate without repeating in a row.
- Per-theme decorative motifs (stars on galaxy, lava bubbles, etc).
- Equipped-cosmetic indicators (glow border + ribbon badge).

## What goes quiet (avoid)

- Pastel palettes, grayscale UI, enterprise minimalism.
- Small buttons, thin fonts, low contrast in the name of "professionalism."
- Apology copy on wrong answers ("Incorrect," "Sorry, wrong").
- Browser-native `confirm()` and `alert()` dialogs.
- Zero-state walls of "Best: 0, Streak: 0, Goals 0/5" on first launch.
- Stats dashboards. Show one current number per pill, not three.
- Long help text. If a kid has to read a paragraph to learn the UI, the UI
  is wrong.

## Reward systems

The reward loop is the engagement engine. Keep it generous and visible.

- **One reward currency.** Coins (or your equivalent) are the main reward
  currency. Accuracy and streak are performance stats, not competing
  currencies. Resist a second spendable number alongside coins ("score"
  next to "coins" confuses kids about which one matters). Performance
  stats CAN coexist with coins as long as they read as feedback, not
  alternative loot.
- **Cumulative + spendable split.** "Lifetime Coins" (never decreases) +
  "Coins" (current balance) is the kid-readable version of XP + gold.
- **First unlock reachable in 1-2 rounds.** If the cheapest reward takes
  10 rounds, kids quit before the dopamine hit.
- **Top tier costs ~weeks of daily play.** Aspiration, not grind.
- **Streak bonuses stack and ramp.** Every correct in a row pays more than
  the last (capped). Tier banners at named thresholds (3 = "Nice streak!",
  5 = "On fire!", 10 = "UNSTOPPABLE!") for dopamine hits.
- **Daily goals refresh nightly.** Mix easy/medium/hard. Stratified draw
  (2 easy + 2 medium + 1 hard) avoids dead-on-arrival sets.
- **Completion bonuses at thresholds.** +N coins at 3 goals, +2N at 5 goals.
  Encourages finishing, not just starting.
- **Anti-grind cap.** Hard ceiling on daily-goal-driven rewards so a kid
  cannot speedrun infinite coins by refreshing.
- **Cosmetic-only spend.** Themes, mascots, skins. Never pay-to-win.

## Feedback rules

- **Correct**: check badge in the button CORNER (not overlaying the label),
  plus a non-destructive correctness signal: glow ring, pulse, brighter
  outline. Do NOT flood the whole button green if your design uses fixed
  slot colors for identity (changing the slot color confuses kids about
  which button they pressed). Coin counter ticks up with animation. Praise
  line rotates from a pool.
- **Wrong**: button shakes, X badge in corner (NOT overlaying the label),
  correct answer reveals with check badge + glow for ~1.5s, gentle copy
  ("Almost!", "Close one!", "Next time!"). NEVER shaming language.
- **Wrong = teaching moment.** Show the correct answer in context. This is
  the most important screen in the game pedagogically. Make it readable.
- **Praise never repeats consecutively.** Two "Got it!" in a row breaks the
  illusion that the game noticed.
- **Confetti for milestones only.** Every-answer confetti is noise.
- **Sound off by default.** Classroom-safe. Mute toggle persisted.

## Interaction rules

- **Big touch targets always.** Min 56px on mobile. Tappable areas should
  feel obviously tappable (border, shadow, hover lift).
- **Keyboard parity.** 1-N keys for active choices, Enter for next, Esc for home.
  Every action a touch user can do, a keyboard user can do.
- **Reversible = friction-free.** Theme preview, equip swap, lesson select,
  mode toggle: zero confirm dialogs.
- **Irreversible = confirm with juice.** Spending coins on a theme: arcade
  modal with big Yes/No buttons. Escape and overlay-tap cancel.
- **No accidental-destruction taps.** A kid will hammer the screen. Buttons
  near the edge of touch zones should not destroy state.
- **Mobile-first padding.** Bottom padding clears any fixed-position element
  (mascot, dock). Critical action buttons must be reachable without scrolling.

## Mode-gated complexity

- **Quick mode**: short (10 questions), no retry queue, no penalty for
  thin lesson selection. Pool inflation (repeat the pool when undersized) so
  the round always reaches its target length.
- **Challenge mode**: medium length (25 questions), retry queue ON, wider
  resurface gap (10-20 questions later). Spaced-rep without feeling
  repetitive.
- **Endless mode**: no length cap, retry queue ON. Use for "how far can
  you go" energy.
- **Always pad choices.** Choice count never flickers (4 stays 4). Borrow
  from full corpus as last resort if the same-lesson pool is too thin.

## Visual identity

- **Themes as palette swaps with attitude.** Each theme owns bg colors,
  accent, button colors, decorative motif. One body[data-theme="..."] attr
  switches everything via CSS variables. Zero JS branching per theme.
- **Theme categories AND tiers.** Two dimensions: a CATEGORY (Starter /
  World / Mascot / Ultimate) groups themes by flavor for shop scanning,
  and a RARITY tier (Common / Rare / Legendary) drives price + border glow.
  Three rarity tiers max (no Epic, no sub-tiers). Categories can be as
  many as the game needs.
- **Mascot-themed colors > mascot art.** School-color palettes (Marauders,
  Huskies, Wildcats) feel personal without requiring custom illustrations.
  Bad mascot art is much more damaging than no mascot art.
- **Tap-to-preview on shop cards.** Touch-first: a single tap on the card
  body previews the theme. Buy button is separate. Preview state restores
  on cancel.
- **Stat pills are tappable when they lead somewhere.** Daily Goals pill
  with a "TAP" hint badge routes to Goals scene. Visible affordance.

## Architecture rules that protect the vibe

- **Centralized event dispatch.** ONE `record_event(GameEvent)` funnel for
  every gameplay event. Each goal/quest declares its own handler inline. TS
  compiler enforces every goal has a handler. Adding a goal without wiring
  = build error. Eliminates the orphan-goal class of bug.
- **Versioned save schema.** Single localStorage key with a version field.
  Schema bumps migrate forward where possible, discard cleanly otherwise.
- **Coins are the reward currency.** Accuracy, streak, and completion rate
  are performance stats, not spendable currencies. Audit early so they do
  not drift into competing currencies.
- **Cachebust assets at build time.** Append a content-hash query string
  to script + style tags so browsers fetch fresh bundles. Hot-reload pain
  is a stealth replay-killer in dev playtests.
- **Random dev-server port.** Each session is a new browser origin, so the
  cache cannot serve a stale bundle from yesterday.

## Anti-patterns to refuse

These look reasonable in a code review and kill the vibe.

- "Tone down the colors for accessibility."
- "Replace the modal with a less intrusive snackbar."
- "Reduce confetti for performance."
- "Smaller buttons fit more content."
- "Hide the mascot on small viewports to save space."
- "Use system defaults instead of custom font."
- "Skip the praise rotation, just say 'Correct'."
- "Remove the streak banners, they're disruptive."
- "Make the home screen more information-dense."
- "Switch to grayscale for a modern look."

If a reviewer flags any of the above WITHOUT citing a specific usability
failure (unreadable text, hidden content, broken layout, keyboard failure,
visual ambiguity), the finding is auto-rejected.

## The load-bearing rule

Inject this rule into every reviewer prompt and every QA agent prompt for
any game following this style:

> Only flag saturated color, big shapes, playful motion, or loud contrast
> as a problem if it causes a specific usability failure: unreadable text,
> hidden content, broken layout, unclear feedback state, keyboard or
> accessibility failure, or visual ambiguity.

Aesthetic restraint, minimalism, and "feels too loud" are NOT valid
findings for games built in this style.

## Portability checklist

When applying this style to a new game, verify the MUST-HAVES first. The
SHOULD-HAVES are aspirational and best added incrementally after early
playtest signal. Resist shipping every system before the core loop feels
right.

### Must-have on day one

- [ ] One reward currency, distinct from any performance stats.
- [ ] Big touch targets (min 56px), keyboard parity, mobile bottom padding.
- [ ] Wrong-answer teaching moment with no shaming language.
- [ ] Centralized event dispatch for any rewardable event (goals, quests,
      achievements, etc).
- [ ] Versioned save schema with forward migration.
- [ ] Cachebust at build time + random dev-server port.
- [ ] The load-bearing rule pinned in every reviewer + QA prompt.

### Should-have, add as the loop matures

- [ ] First unlock reachable in 1-2 rounds at average performance.
- [ ] Streak system with stacking bonuses and milestone banners.
- [ ] At least 4 distinct themes, each a full palette swap.
- [ ] Theme preview before purchase, confirm modal on actual spend.
- [ ] Three reward rarity tiers (cheap / mid / aspirational).

### Nice-to-have, ship only after the core feels right

- [ ] Daily goals with stratified draw.
- [ ] Completion bonuses at goal-set thresholds.
- [ ] Anti-grind cap on daily rewards.
- [ ] Mascot character with reaction states (idle, cheer, wobble, party).
- [ ] Shop categories grouping themes by flavor.

## See also

- [docs/PLAYFUL_TRAINING_GAME_STYLE.md](PLAYFUL_TRAINING_GAME_STYLE.md):
  sibling doc tuned for older learners (lab students, technical apprentices).
  Same engine, calmer tone. Use that doc when the target is competence
  building rather than kid-arcade replay.
- `docs/REPO_STYLE.md`: repo-wide conventions, including
  the five core philosophies that underpin the engineering side.
- `docs/MARKDOWN_STYLE.md`: writing conventions for this
  doc.
