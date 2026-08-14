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
- Scan `docs/CHANGELOG.md` and `docs/QUESTION_FUNCTION_INDEX.md` for recent changes
  and the existing function inventory.

If generators exist that cover the requested question type, follow the existing-repo path.
If none exist, follow the greenfield path.

## Authoring contract

Both paths begin with an authoring contract that records the design decisions for the task.
Use the target repo's existing docs location when present; otherwise record the contract in
comments at the top of the new generator file. The contract must state:

- Question family (MC, MA, MAT, FIB, NUM, ORD, pedigree, phylogenetic tree, PubChem).
- Output formats required (BBQ text upload, QTI package, HTML self-test, or some combination).
- Seeded-randomization strategy: per-instance (each N gets different content),
  per-version (fixed seed reproduces identical output), or per-release (YAML bank driven).
- Sanitization level: which anti-cheat flags are active (`add_anticheat_args`,
  `apply_anticheat_args`) and whether any are intentionally overridden.
- Expected example: a sample stem, correct answer, and at least two distractors to establish
  the intended output shape before writing code.

## Greenfield path

Use when no generator exists for the requested question type or domain.

1. Confirm evidence: verify `bptools.py` and `TEMPLATE.py` exist in the target repo.
   Read `bptools.py` to confirm the live API surface matches `references/api_surface.md`.
2. Write the authoring contract: state question family, output formats, seeded-randomization
   strategy, sanitization level, and one example input/output pair before writing any code.
3. Start from TEMPLATE.py: copy `TEMPLATE.py` to the target `problems/*-problems/` directory.
   Rename it to match the domain (for example `genetics_mc_questions.py`).
4. Implement with bptools primitives:
   - Build the stem and distractor list as plain strings and lists in `write_question(N, args)`.
   - Format with the relevant `bptools.formatBB_*` function.
   - Use `bptools.collect_and_write_questions(...)` and `bptools.make_outfile(...)` in `main()`.
   - Add `add_anticheat_args(parser)` and call `apply_anticheat_args(args)` in `main()`.
5. Validate with a small run: run `python generator.py -d 1 -s 12345` and inspect the
   BBQ text output. Confirm the stem is readable, the answer key is correct, and no debug
   content leaks into the output.
6. Prove reproducibility: run twice with the same seed and compare outputs; they must be
   byte-identical.

## Existing-repo path

Use when generators already exist for the domain or a related question type.

1. Inspect first: read the live `bptools.py` from the repo root for the canonical API.
   Do not copy signatures from memory or from `references/api_surface.md` without
   confirming they match the live file.
2. Inventory generators: list scripts under `problems/*-problems/` with
   `git ls-files problems/` and read `references/docs/QUESTION_FUNCTION_INDEX.md`
   to see which `write_question` patterns are already established.
3. Identify the current design: read the target generator to understand which
   `formatBB_*` function it uses, how it seeds randomness, and which anti-cheat flags
   are active. Record any deviations from the authoring contract.
4. Make repo-specific changes one generator at a time: modify `write_question` in the
   target script without touching unrelated generators. Match the existing indentation,
   comment style, and import order (tabs, ASCII, bptools import before local modules).
5. Prove improvement: collect three pieces of evidence before closing the task:
   - Sample BBQ output before and after the change, side-by-side, showing the improvement.
   - A seed-reproducibility log: two runs with `--seed 12345` producing byte-identical output.
   - An anti-cheat audit note: confirm distractor scrambling is active, answer key is not
     printed to stdout, and metadata sanitization is applied where required.

## Closing checklist

Before finishing any bptools task, verify:

- `write_question(N, args)` produces well-formed BBQ text for at least two values of N.
- Output is reproducible: same seed, same output.
- Anti-cheat defaults are active unless intentionally overridden and documented.
- No debug prints, answer keys, or generator filenames are visible in the BBQ output.
- `docs/CHANGELOG.md` in the TARGET repo is updated with a brief description of the change.
- Generated artifacts (`bbq-*.txt`, `qti*.zip`, `selftest-*.html`) are not staged for git.
