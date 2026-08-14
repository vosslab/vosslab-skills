# Task selection

Use this reference to classify a bptools authoring request before consulting the topic index or
domain guides. Answer all four dimension questions to frame the task, then locate the matching guide.

## Task dimensions

### Question family

Choose the family that best describes the content:

- Multiple-choice (MC): one correct answer, shuffled distractors. Format: `formatBB_MC_Question`.
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

Define which level of randomization applies:

- Per-instance: each call to `write_question(N, args)` produces a different question from the
  same generator. Distractors, values, and wording change for each N. This is the standard mode
  controlled by seeded randomness; use `random.seed(args.seed + N)` or the bptools convention.
- Per-version: the same seed produces an identical question set. Used for reproducibility checks
  and audit trails. Pass a fixed `--seed` argument; the output must be byte-identical on repeat
  runs.
- Per-release: a YAML bank is authored once; the generator reads the bank and draws from it
  across exam versions. The bank changes only when the domain content is updated, not on each run.

Identify the scope before writing or modifying `write_question`. Scope mismatches cause
unreproducible output or unintentional exam version drift.

### Anti-cheat policy

State the anti-cheat requirements before authoring question content:

- Distractor scrambling: answer-choice order must differ across instances. Enabled by default in
  `collect_and_write_questions` unless overridden. Do not disable without a documented reason.
- Hidden answer key: the BBQ text encodes the correct answer by position, not by label. Never
  print the answer key to stdout or embed it in the question stem.
- Metadata sanitization: Python comments, debug prints, and generator filenames must not leak
  subject matter in a way that reveals the answer. Apply `apply_anticheat_args(args)` when
  the generator uses `add_anticheat_args(parser)`.
- Seed reproducibility: a fixed `--seed` must reproduce the same question set for audit purposes.
  Verify by running twice with identical arguments and comparing output files byte-by-byte.

## Clarifying questions to answer internally

- What question family is requested? Is there an existing generator in the same domain to reuse?
- What output format does the target LMS require?
- Does the task require greenfield authoring or improvement of an existing generator?
- What randomization scope is needed: exploratory, reproducible, or release-stable?
- Are there anti-cheat requirements beyond the defaults?
- Which domain-specific guide must be loaded (matching, pedigree, phylogenetic, PubChem)?
