# AI-writing review checklist

Use the checks that fit the draft. For a short email, get the logistics, obligations, and voice
right first. For longer prose, fix the argument and reader obstacles before scanning for patterns.
A useful finding names the passage, what the reader might miss or misunderstand, and the smallest
edit that fixes it. Keep passages that already work.

## Read for meaning first

- [ ] **E01-E04, E26: Establish what the author is doing.** Name the reader, what they need to
  know or do, and what the user asked you to change. For a difficult draft, outline the author's
  claim, evidence, and limits before polishing. If the outline exposes a missing decision or
  link in the argument, flag it rather than supplying it. Use the author's current draft and
  accepted examples in the same genre before guessing at voice.
  Basis: [Vinitsky discussion and Bhat et al.](checklist-sources.md#clarity-and-structure)
- [ ] **E05-E08, E25: Find who did what, what the words refer to, and where the point is.**
  Zonder Labs distinguishes three reading problems:
  1. **Hidden actors and actions.** Find nouns that name actions, then ask who actually
     did them. Put the actor in the subject and the action in the verb when it clarifies the
     sentence. Keep a useful passive or one that avoids inventing an actor.
  2. **Vague wording.** Check ambiguous `this`, compressed noun strings, and odd word
     pairings. Could the reader tell which quantity `within 2%` refers to? Name it from the
     source or ask. Keep technical terms when plain substitutions would lose a distinction.
  3. **Empty statements and misplaced emphasis.** On a quick read, find the result or request.
     Move it ahead of filler and side issues. Keep conditions that change the result or action.
  See [zonderlabs-clarity.md](zonderlabs-clarity.md) for before/after examples and study limits.
- [ ] **E09-E13, C04, C12, C18: Check whether the reasoning works.** Can you point to the result
  that supports each claim? Say what was measured, compared, or inferred when the distinction
  matters. Replace `research shows` with a checked source and what it found. Keep roadmap text
  and parallel methods if they help readers navigate. Don't invent a gap to fill a research
  introduction template, or a causal explanation to connect two findings.
  Basis: [Zonder Labs](checklist-sources.md#clarity-and-structure) and
  [McDonald on peer review](checklist-sources.md#voice-and-human-judgment). The wiki's
  revision-practices guide has the research-introduction studies.

## Edit for this writer and reader

- [ ] **E14-E19, E27, C20: Keep the author's voice and role.** Start with their sentences and
  fix specific problems. Preserve viewpoint, level of formality, terms of address, and emphasis
  when they serve the reader. Notes can supply facts without supplying a personal reaction.
  Ask for one if it matters. Read the result aloud for difficult clause pileups.
  Basis: [McDonald, authorship research, and author feedback](checklist-sources.md#voice-and-human-judgment).
- [ ] **C01-C03, C05-C07, C17: Replace vagueness, not vocabulary.** If `robust` means the
  estimator is resistant to outliers, say so when that helps. Keep `robust estimation` as an
  established term. Drop `highlighting its potential` if it adds no finding; keep a clause that
  explains an effect the evidence supports. Repeat a precise name for the same object rather
  than rotating synonyms. Keep `serves as` if a temporary role differs from identity.
  Basis: [Zonder Labs](checklist-sources.md#clarity-and-structure) and
  [pattern catalogs](checklist-sources.md#pattern-tools).
- [ ] **C08-C11, C13-C16, C21-C22: Check what each repeated form does.** Read adjacent
  sentences for matching openers, repeated `not X but Y`, `No X. No Y.` chains, staged reveals,
  stacked questions, or a concluding slogan. Remove a frame that delays or repeats the point.
  Keep a real contrast, teaching question, three-item list, or useful signpost. Keep the writer's
  em dashes, Oxford commas, and other punctuation unless there is a specific style or reading
  problem. Give the reader the current decision rather than draft history unless a change
  matters to them. Clear draft markers and verify references.
  Basis: [Willison and Bronsdon](checklist-sources.md#pattern-tools),
  [Powell and Pew](checklist-sources.md#punctuation-and-prevalence), and the
  [Vinitsky discussion](checklist-sources.md#clarity-and-structure).

## Check the final version against the original

- [ ] **C19, E20-E23: Compare commitments, claims, and scope.** Compare final wording with
  the author's original, even after several rounds. Check actor, action, facts, dates, units,
  attribution, negation, causal direction, and conditions. Check both directions of certainty:
  `may` becoming `does` and a warranted `does` becoming `might`. Keep an association distinct
  from a cause, an option from a requirement, and an overdue task from a new deadline. Check
  that a citation still supports, contrasts with, or gives context for the same claim. Verify
  newly added plans or examples; get approval for substantive changes outside the request.
  Basis: [Abdulhai et al. and Baradziej](checklist-sources.md#meaning-and-certainty).
- [ ] **C23-C24, E24, E28: Separate a match, an editing finding, and a decision.** A
  highlighter match is a place to read. A classifier score does not establish writing quality,
  provenance, or misconduct. Use drafts and revision history when authorship matters. In a
  copyedit, preserve quotations, code, URLs, IDs, and data. For consequential work, show the
  original and proposed wording and why the change is warranted. Leave judgments about novelty
  or misconduct with the responsible person.
  Basis: [Bronsdon](checklist-sources.md#pattern-tools),
  [Pew and detector documentation](checklist-sources.md#detection-is-a-separate-question), and
  [McDonald on peer review](checklist-sources.md#voice-and-human-judgment).

## What to keep or change

The Biostats examples come from Dr. Voss's corrections to an actual draft, not a controlled
reader study. The other examples are constructed checks.

| Draft or proposed edit | What to do |
| --- | --- |
| `Please be in class at 5 p.m.` | In Dr. Voss's course email, state the meeting and keep his format: `We're meeting in person today at 5pm in SCH 612.` |
| `If your group hasn't submitted the form, we'll settle your topic at the check-in.` | State that the form was due last week and have one person submit it now. Don't make the check-in a substitute. |
| `Bring the work you've completed.` | If work wasn't assigned, keep `If you've started working on your tutorial, bring what you have.` |
| `We'll work through the tutorial and discuss how to choose a regression model.` | Keep the existing tutorial. Don't add a separate lesson the instructor hasn't planned. |
| `The reduction was observed following implementation.` | Find what fell, what was implemented, and who did it if the reader needs to know. Don't invent the actor or change `following` to `because of`. |
| `The results suggest that the treatment may reduce growth in this sample.` | Keep `may` and `in this sample`; dropping them changes the conclusion. Keep a definite description of an observed result if the evidence warrants it. |
| `Bring your notes, your draft, and any questions.` | Keep the real list and the author's Oxford comma. A pattern match isn't a reason to edit. |

## Updating the checklist

The weekly `ai-writing-research` digest updates this skill when a source or human review
changes an editing decision. Record the finding, its limits, and one before/after or keep-as-is
case in [checklist-sources.md](checklist-sources.md). Amend an existing check when possible.
Leave the file alone when new material only repeats an existing point. Preserve the original
source list and the C01-C20 references to the wiki's living checklist.

To try a proposed rule with people, compare original and edited drafts from the same genre.
Ask intended readers, without identifying the rewrite, to say what happened, what they're
supposed to do, or what the evidence supports. Separately ask the writer which phrasing sounds
like them and whether either draft changes their meaning. Record what readers got wrong or
couldn't find and whether the edit helped. This is a proposed spot check, not validation of the
checklist.

The checklist works without the wiki. For research details and technical voice samples, see
`guides/ai-writing-revision-practices.md`, `guides/ai-writing-cliche-checklist.md`, and
`reports/neil-voss-writing-style-analysis.md` under
`/srv/samba/share/wiki/research/ai-writing-and-authorship/`. Coauthored papers are secondary
evidence for individual voice, not a style guide for student email.
