# Project workflow

Use this reference when the skill is invoked on a TARGET biology-problems repo, not while
building or improving the bptools-writer-expert skill itself. The skill is always applied
to an external repo that contains bptools.py, TEMPLATE.py, and problem generator scripts
under `problems/*-problems/`.

## Detect project state

Inspect the target repo before writing or changing any generator:

- Run `git rev-parse --show-toplevel` to confirm the repo root.
- Check whether `bptools.py` exists at the repo root; this is mandatory.
- Inventory generator scripts with `find problems -name '*.py' -type f` or
  `git ls-files problems/`.
- Check for `TEMPLATE.py` at the repo root; it defines the required script structure.
- Check for `docs/QUESTION_PEDAGOGY_GUIDE.md`, `docs/QUESTION_VOICE_GUIDE.md`,
  `docs/QUESTION_EXEMPLARS.md`, and `devel/check_question_text.py`; the live copies win over the
  bundled snapshots when they differ.
- Scan `docs/CHANGELOG.md` and `docs/QUESTION_FUNCTION_INDEX.md` for recent changes
  and the existing function inventory.

If generators exist that cover the requested question type, follow the existing-repo path.
If none exist, follow the greenfield path.

## Authoring contract

Both paths begin with an authoring contract that records the design decisions for the task.
Use the target repo's existing docs location when present; otherwise record the contract in
comments at the top of the new generator file. The contract states:

- Question family (MC, MA, MAT, FIB, NUM, ORD, pedigree, phylogenetic tree, PubChem).
- Output formats required (BBQ text upload, QTI package, HTML self-test, or some combination).
- Reasoning target on the revised Bloom process scale: apply, analyze, evaluate, or recall
  (label recall items as recall). Example: "analyze a gel to identify the father".
- Data design: the table, figure, cross, sequence, or scenario that forces the reasoning, which
  parts are randomized, and why the arithmetic comes out whole.
- Named student errors: one entry per wrong choice, each naming the mistake that produces it;
  mark any seriously absurd choice as absurd.
- Chosen exemplar: the entry in `references/docs/QUESTION_EXEMPLARS.md` (or the live
  `docs/QUESTION_EXEMPLARS.md`) that the item imitates, and the pedagogy or voice heading it
  shows.
- Randomization strategy: per-instance (each N draws a scenario with true randomness from a
  pool sized for useful variation, while recognizing that random draws may repeat) or
  per-release (YAML bank driven). Deterministic selection appears only behind a debugging or
  test option.
- Sanitization level: which anti-cheat flags are active (`add_anticheat_args`,
  `apply_anticheat_args`) and whether any are intentionally overridden.
- Expected example: a sample stem, correct answer, and meaningful alternatives tagged with their
  named error or absurd role, to establish the intended output shape before writing code.

## Greenfield path

Use when no generator exists for the requested question type or domain.

1. Confirm evidence: verify `bptools.py` and `TEMPLATE.py` exist in the target repo.
   Read `bptools.py` to confirm the live API surface matches `references/api_surface.md`.
2. Write the authoring contract: state every item above, including the puzzle design
   (reasoning target, data, named student errors, exemplar), and one example input/output pair
   before writing any code.
3. Start from TEMPLATE.py: copy `TEMPLATE.py` to the target `problems/*-problems/` directory.
   Rename it to match the domain (for example `genetics_mc_questions.py`).
4. Implement with bptools primitives:
   - Build the stem and distractor list as plain strings and lists in `write_question(N, args)`.
   - Compute each distractor from its named error, with a comment naming the error.
   - Format with the relevant `bptools.formatBB_*` function.
   - Use `bptools.collect_and_write_questions(...)` and `bptools.make_outfile(...)` in `main()`.
   - When exposing anti-cheat overrides, add `add_anticheat_args(parser)` and call
     `apply_anticheat_args(args)` in `main()`; otherwise collection applies the shared defaults.
5. Validate with a small run: run `python generator.py -d 1` and inspect the
   BBQ text output. Confirm the stem is readable, the answer key is correct, and no debug or
   key-revealing content leaks into student-facing stems or choices.
6. Run the student-text review: render several items (`-d 5`), run
   `devel/check_question_text.py -i <bbq file>`, verify the key independently, apply the routed
   rubric items from `references/question_voice.md`, and revise.

## Existing-repo path

Use when generators already exist for the domain or a related question type.

1. Inspect first: read the live `bptools.py` from the repo root for the canonical API.
   Confirm signatures against the live file instead of memory or `references/api_surface.md`.
2. Inventory generators: list scripts under `problems/*-problems/` with
   `git ls-files problems/` and read `references/docs/QUESTION_FUNCTION_INDEX.md`
   to see which `write_question` patterns are already established.
3. Identify the current design: read the target generator to understand which
   `formatBB_*` function it uses, how it draws scenarios, and which anti-cheat flags
   are active. Record any deviations from the authoring contract.
4. Audit the current student-facing text: render several items from the unmodified generator,
   run `devel/check_question_text.py -i <bbq file>`, and score the output against the routed
   rubric items from `references/question_voice.md`. Record each failing item ID; this list is
   the before-state of the change and the work list for step 5.
5. Make repo-specific changes one generator at a time: modify `write_question` in the
   target script without touching unrelated generators. Match the existing indentation,
   comment style, and import order (tabs, ASCII, bptools import before local modules). Fix the
   audited failures; when a change adds or alters choices, name the student error behind each.
6. Prove improvement: collect the four proof artifacts from `references/testing_and_oracles.md`
   before closing the task:
   - Rendered before/after sample, side-by-side, showing the improvement.
   - Distractor-rationale table for a rendered item.
   - Key-verification note naming the independent method and its result.
   - Checker report excerpt, with the disposition of each finding.
   Add an anti-cheat audit note: the generator scrambles choices with no meaningful natural
   order, meaningful natural ladders are preserved, key cues stay out of student-facing stems,
   choices, and published self-tests, and metadata sanitization is applied where required.
   Instructor-console diagnostics may display the key.

## Closing checklist

Before finishing any bptools task, verify:

- `write_question(N, args)` produces well-formed BBQ text for at least two values of N.
- Student-facing scenario selection uses true randomness. Do not require two random draws to
  differ. Preserve meaningful natural choice order; scramble choices only when no meaningful
  order exists.
- Student-text review is done: rendered items read as a student, routed rubric items applied,
  advisory checker run, and the key verified independently.
- Every wrong choice has a named error or an absurd label.
- Anti-cheat defaults from collection are active unless intentionally overridden and documented.
- No debug prints, key-revealing content, or generator filenames are visible in student-facing
  stems, choices, or published self-tests. Instructor-console diagnostics and BBQ `Correct` /
  `Incorrect` fields may encode the key.
- `docs/CHANGELOG.md` in the TARGET repo is updated with a brief description of the change.
- Generated artifacts (`bbq-*.txt`, `qti*.zip`, `selftest-*.html`) are not staged for git.
