# Task selection

Use this reference to classify a bptools authoring request before consulting the topic index or
domain guides. Answer all six dimension questions to frame the task, then locate the matching guide.

## Task dimensions

### Question family

Choose the family that best describes the content:

- Multiple-choice (MC): one correct answer; preserve meaningful natural choice order and shuffle
  choices with no meaningful order. Format: `formatBB_MC_Question`.
- Multiple-answer (MA): one or more correct answers, student must select all. Format:
  `formatBB_MA_Question`.
- Matching set: pair a list of terms to a list of definitions or descriptions. Format:
  `formatBB_MAT_Question`. Requires YAML question bank; see the matching guide.
- Fill-in-the-blank (FIB): student types a short text answer. Format: `formatBB_FIB_Question` or
  `formatBB_FIB_PLUS_Question` (multiple blanks).
- Numeric (NUM): student enters a numeric value within a tolerance range. Format:
  `formatBB_NUM_Question`.
- Ordered list (ORD): student arranges items in the correct sequence. Format:
  `formatBB_ORD_Question`.
- Pedigree diagram: question embeds an SVG pedigree chart; answer logic may be MC or MA.
  Requires the pedigree pipeline and spec.
- Phylogenetic tree: question embeds a tree diagram; answer logic may be MC or MA.
  Requires the treelib pipeline and spec.
- PubChem molecule: question embeds or references a chemical structure from PubChem.
  Requires the PubChem bptools guide.
- Multi-select (essay prompt / complex MC): used when question context is long-form text
  and answer is constructed from multiple sub-parts. Typically uses `formatBB_MA_Question`
  with care for answer key ordering.

### Item type

Item type picks the rubric group that reviews the student-facing text. Pair it with the family:

- MC, MA, and figure-based families (pedigree, tree, PubChem) with MC or MA answers: universal
  items plus the multiple-choice items (U, M).
- MC statements from a YAML bank: universal, statement-bank, and multiple-choice items (U, S, M).
- Matching set: universal and matching items (U, T).
- FIB, FIB_PLUS, NUM: universal and fill-in-the-blank items (U, F).
- ORD: universal and ordering items (U, O).

`references/question_voice.md` lists the item IDs and routes each type to the guide headings that
govern its stem, choices, and instructions.

### Reasoning target

Name what the student does with the data, on the revised Bloom process scale:

- Apply: use a rule on a new case (a lethal-allele cross, a dilution, a restriction digest).
- Analyze: pull structure out of data (read a gel, a pedigree, a gene map).
- Evaluate: judge a claim or a calculation (find the error, pick the right setup).
- Recall: retrieve vocabulary or facts (matching sets, statement banks); label these as recall.

The target sets the data design and the named student errors recorded in the authoring contract
(see `references/project_workflow.md`).

### Output format

Choose the delivery format the LMS or test runner requires:

- Blackboard BBQ text upload: the default and most common. All `formatBB_*` functions target this.
  Output is a plain-text tab-separated file (usually `bbq-*.txt`).
- QTI package: a ZIP archive for Canvas, Moodle, and other IMS QTI-compatible LMS platforms.
  Produced by `qti_package_maker`; individual items are still formatted with `formatBB_*`
  functions before being passed to the QTI engine.
- HTML self-test: a standalone HTML file for browser-based practice (no LMS required).
  Produced by a separate engine path in `qti_package_maker`; same formatting pipeline.

When the output format is unspecified, default to BBQ text upload and confirm before adding
a QTI or HTML path.

### Randomization scope

The repo draws scenarios with true randomness for student assessments, because predictable
sequences make cheating easier. Define which level applies:

- Per-instance: each call to `write_question(N, args)` draws a scenario with true randomness.
  Size the pool for useful variation across the requested count, while recognizing that random
  draws may repeat. This is the standard mode.
- Per-release: a YAML bank is authored once; the generator reads the bank and draws from it
  across exam versions. The bank changes only when the domain content is updated, not on each run.
- Deterministic (debugging, reproducibility checks, and unit tests only): select scenarios in a
  fixed order behind an explicit option such as `--sorted` from `bptools.add_scenario_args`.
  Keep the student-facing default random.

Identify the scope before writing or modifying `write_question`. A scenario pool smaller than the
requested count produces repeated items; size the pool first.

### Anti-cheat policy

State the anti-cheat requirements before authoring question content:

- Distractor scrambling: the generator explicitly scrambles choices with no meaningful natural
  order. Preserve natural numeric, genotype, ratio, and short-string ladders; the formatter
  preserves the order it receives.
- Hidden answer key: BBQ encodes the key with `Correct` and `Incorrect` fields. Keep key cues
  out of student-facing stems, choices, and published self-tests. Instructor-console diagnostics
  may display the key.
- Metadata sanitization: Python comments, debug prints, and generator filenames must not leak
  subject matter in a way that reveals the answer. When a generator exposes anti-cheat overrides,
  use `add_anticheat_args(parser)` and `apply_anticheat_args(args)`; collection applies the
  shared defaults.
- Randomness: student-facing scenario selection uses true randomness. Choice sets with no
  meaningful natural order are scrambled; meaningful natural ladders stay in that order. Do not
  require two random draws to differ.

## Clarifying questions to answer internally

- What question family is requested? Is there an existing generator in the same domain to reuse?
- Which item type (rubric group) governs the review, and what reasoning target does the item test?
- What output format does the target LMS require?
- Does the task require greenfield authoring or improvement of an existing generator?
- What randomization scope is needed: per-instance, per-release, or a debugging-only deterministic mode?
- Are there anti-cheat requirements beyond the defaults?
- Which domain-specific guide must be loaded (matching, pedigree, phylogenetic, PubChem)?
