# Question voice and design routing

Use this guide to jump from an authoring task to the exact headings in the three bundled
student-text guides, then to the rubric items that review the result. Read the headings named
for your task in full; the bundled guides own every rule, and this file only routes.

Bundled guides (snapshots from the target repo, see [docs.md](docs.md)):

- Pedagogy: [QUESTION_PEDAGOGY_GUIDE.md](docs/QUESTION_PEDAGOGY_GUIDE.md) covers design workflow,
  distractor design, item structure, answer verification, and the review rubric.
- Voice: [QUESTION_VOICE_GUIDE.md](docs/QUESTION_VOICE_GUIDE.md) covers stem anatomy, choices,
  instructions by item type, numbers and symbols, and mechanics.
- Exemplars: [QUESTION_EXEMPLARS.md](docs/QUESTION_EXEMPLARS.md) holds worked examples, each
  labeled model (imitate) or fix (flaw plus rewrite).

Headings below are quoted from the snapshots. When a snapshot refresh renames a heading, update
the matching row here.

## Task routing

### Write a new stem

- Pedagogy: Puzzle first, few words; Design workflow (Name the reasoning target, Build the data,
  Write the thinnest wrapper); Data first and shared-figure sets.
- Voice: Stem anatomy (Rule, case, question; Lead-ins; Figure pointers; What to leave out);
  Emphasis.
- Exemplars: Stems (Data first, one choice set for sibling questions; Lab scenario in second
  person; Transfer to a new case; Rule, case, question).
- Rubric: U1, U2, U3, U4, M1.

### Write distractors

- Pedagogy: Distractor design (Error-derived distractors; Show-the-setup choices; Misconception
  placement; Cannot be determined); Design workflow (List the student errors; Compute the wrong
  answers).
- Voice: Choices (Layout and order; Fixed ladders; Parallel form).
- Exemplars: Distractor recipes (Dilution; Transcription; Lethal alleles; Restriction digests;
  Statement swap); Choices (Show the setup; Formula variants as distractors; Fixed ladder across
  a multi-part story; Natural order and type labels).
- Rubric: M2, M3, M4, M5.

### Write absurd or joke choices

- Pedagogy: Seriously absurd choices; Decision hierarchy (the absurd-versus-plausible conflict).
- Voice: Choices > Parallel form (an absurd choice keeps the grammar, length, and register of the
  real choices).
- Exemplars: Seriously absurd choices (Absurd choices delivered deadpan).
- Rubric: M2 (tag the choice as absurd), M3, M4.

### Write a statement bank

- Pedagogy: Statement banks (One-term swaps; Out-of-scope facts and bracketed numbers; Balanced
  hedges and absolutes; Pool sizes).
- Voice: Statement bank form.
- Exemplars: Statement banks (Out-of-scope and bracketed values; Hedges on true, absolutes on
  false; Explanation on the key only); Distractor recipes > Statement swap.
- Bank format and YAML conversion: [MC_STATEMENTS_AUTHORING_GUIDE.md](docs/problems/multiple_choice_statements/MC_STATEMENTS_AUTHORING_GUIDE.md).
- Rubric: S1, S2, S3, S4, then M1 to M5 on the rendered item.

### Write a matching set

- Pedagogy: Matching sets (Applied pairings; Values without cues).
- Voice: Instructions by item type > Matching.
- Exemplars: Matching sets (Applied pairing with mirrored values; Value repeats the key; Giveaway
  date; Exact letter-use instruction with mnemonic labels).
- YAML schema and generator behavior: [MATCHING_SET_AUTHORING_GUIDE.md](docs/problems/matching_sets/MATCHING_SET_AUTHORING_GUIDE.md).
- Rubric: T1, T2, T3.

### Write FIB or NUM entry rules

- Pedagogy: Review rubric (F items).
- Voice: Instructions by item type > Fill in the blank and numeric; Numbers, units, and symbols.
- Exemplars: Entry rules and mechanics (Fill-in-the-blank entry rule; Template slips).
- Rubric: F1, F2, F3.

### Write multiple-answer or ordering instructions

- Voice: Instructions by item type (Multiple answer; Ordering).
- Rubric: M1 to M5 for multiple answer; O1, O2 for ordering.

### Write hints and notes

- Pedagogy: Difficulty from data (hints exist only to resolve an ambiguity).
- Voice: Hints and notes.
- Exemplars: Emphasis, hints, and notes (Hint that resolves ambiguity; Note that hands over
  arithmetic; Solution-path hint).
- Rubric: U8.

### Design a multi-part story, puzzle, or invented world

- Pedagogy: Item structure (Multi-part stories; Self-checking answers and puzzles; Red herrings;
  Scenario variety; Names and invented worlds).
- Exemplars: Puzzles, stories, and worlds (Invented names that help memory; Error analysis;
  Self-checking answer; Cannot be determined, used correctly).
- Rubric: U5, U6, U8.

### Review rendered text

- Pedagogy: Review rubric (apply the universal items plus the group for the item type);
  Answer verification.
- Voice: Mechanics; Numbers, units, and symbols; HTML and formatting.
- Exemplars: scan the fix entries for the flaw you find; each shows a rewrite.
- Checker: `devel/check_question_text.py -i <bbq file>` in the target repo (advisory).
- Rubric: U1 to U9 plus the item-type group in the table below.

### Fix an existing generator's wording

- Start with Review rubric on rendered output of the current generator, then edit only the
  failing items.
- Pedagogy: Puzzle first, few words; Scenario variety (reworded stems with identical data are
  one question).
- Voice: What to leave out; Parallel form; Mechanics.
- Exemplars: the fix entries under Stems, Choices, Statement banks, Matching sets, and Entry
  rules and mechanics.
- Verify the key independently after any edit to choices or scenarios: Pedagogy > Answer
  verification (rubric U9).

## Rubric groups by item type

The rubric lives under Review rubric in the pedagogy guide. Rubric labels there mention PGML
widgets; in bptools read them as the BBQ types below.

| Item type | Rubric items to apply |
| --- | --- |
| MC, MA | U1 to U9, M1 to M5 |
| MC statements from YAML | U1 to U9, S1 to S4, M1 to M5 |
| MAT | U1 to U9, T1 to T3 |
| FIB, FIB_PLUS, NUM | U1 to U9, F1 to F3 |
| ORD | U1 to U9, O1, O2 |
| Pedigree, tree, PubChem (MC or MA answers) | U1 to U9, M1 to M5 |

## Rubric item IDs

Universal items, applied to every question:

| ID | Name |
| --- | --- |
| U1 | Data or scenario first; one lead-in |
| U2 | Emphasis only on discriminating words and negations |
| U3 | What is counted is explicit; whole-number arithmetic where intended |
| U4 | Nothing said twice; no preamble, caveat, or citation in the stem |
| U5 | Sampled items differ in data or scenario, not only wording |
| U6 | Names are deliberate (real, or mnemonic and letter-matched) |
| U7 | Clean mechanics: spelling, spacing, articles, units, entities |
| U8 | Difficulty comes from data; hints only resolve ambiguity |
| U9 | Key verified independently |

Multiple choice and multiple answer:

| ID | Name |
| --- | --- |
| M1 | Cover-the-options: answerable from the stem alone |
| M2 | Each distractor tagged with its error or as absurd |
| M3 | Options homogeneous, in natural order when one exists |
| M4 | No testwise cues (longest key, hedge asymmetry, key-word echo, grammar mismatch) |
| M5 | "Cannot be determined" only when sometimes the key and never ambiguous |

Statement banks:

| ID | Name |
| --- | --- |
| S1 | Lowercase fragments that finish the stem |
| S2 | False statements are one-term swaps (plus absurd variants) |
| S3 | Hedges and absolutes balanced across true and false |
| S4 | False pool larger than true pool |

Matching:

| ID | Name |
| --- | --- |
| T1 | Instruction states letter use exactly |
| T2 | Values echo no key words, category words, or giveaway dates |
| T3 | Values parallel, one idea each |

Fill in the blank and numeric:

| ID | Name |
| --- | --- |
| F1 | Entry rules come with a worked example |
| F2 | Units and rounding stated |
| F3 | Tolerance matches the arithmetic |

Ordering:

| ID | Name |
| --- | --- |
| O1 | One unambiguous ordering criterion stated |
| O2 | Items share one format |

## Advisory checker

The target repo's `devel/check_question_text.py` flags mechanical cues for M4, S3, T2, and parts
of U4 and U7. Run it from the target repo root:

```bash
source source_me.sh && python3 devel/check_question_text.py -i <bbq file>
```

A finding sends the item to a closer read; a clean report leaves the rubric read and the key
verification in place. The live tool owns its output format and flags, so read its `--help`
before quoting results.
