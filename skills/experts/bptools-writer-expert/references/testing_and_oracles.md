# Testing and oracles

Use this reference when validating a new or modified bptools generator. Define fixtures, choose
oracles, and collect the three required proof artifacts before closing any authoring task.

## Degenerate fixture corpus

Include at least these cases when authoring or validating a generator:

- Single instance: run with `-d 1` to confirm the script does not crash and produces one
  well-formed BBQ line.
- Multi-seed variation: run with two different seeds (for example `-s 1` and `-s 99`) and
  confirm the output differs in stem content or distractor order.
- Long answer text: supply a distractor or stem that is near the maximum expected length;
  confirm the formatter does not truncate or corrupt it.
- Unicode and special characters: if the domain uses Greek letters, subscripts, or HTML
  entities, confirm they appear as escaped HTML entities (`&alpha;`, `&beta;`) and not as
  raw UTF-8 in the BBQ output.
- Empty or minimal YAML bank: for YAML-driven generators (matching sets, MC statements),
  test with a bank containing only one valid pair; the generator must handle it without
  crashing or producing duplicate distractors.
- Edge case per family:
  - MC/MA: only two distractors available (minimum for Blackboard).
  - MAT: only one matching pair available; generator must warn or skip gracefully.
  - FIB: blank field that expects an exact numeric match; test with `formatBB_FIB_Question`
    or `formatBB_NUM_Question` as appropriate.
  - Pedigree: a degenerate pedigree with no offspring (terminal generation).
  - Phylogenetic tree: a tree with only two leaf taxa.
  - PubChem: a compound ID that exists but has no 2D structure available.

## Oracles

Validate generator output against a trusted reference before declaring it correct.

- BBQ schema validator: parse the output file line-by-line and confirm each line starts with
  a recognized BBQ type prefix (`MC`, `MA`, `MAT`, `FIB`, `FIB_PLUS`, `NUM`, `ORD`).
  The validator path in `qti_package_maker` is
  `qti_package_maker/assessment_items/validator.py`.
- QTI validation: if a QTI package is produced, open the ZIP and verify the
  `imsmanifest.xml` is present and well-formed. Use
  `qti_package_maker/engines/bbq_text_upload/write_item.py` as the reference for
  expected BBQ field ordering.
- Manual BBQ text inspection: open the output file in a text editor and read at least
  three generated questions. Confirm: stem is readable, correct answer is marked, distractors
  are plausible, no debug text or answer key is visible.
- Seed-reproducibility test: run the generator twice with `--seed 12345 -d 10` and compare
  the output files with a byte-by-byte diff. The files must be identical.
- Anti-cheat audit: confirm distractor order varies across two seeds, the correct answer
  position is not always first, and `apply_anticheat_args(args)` was called in `main()`.

## Invariants

Test these invariants for every generator, regardless of question family:

- The correct answer is never placed in the distractor list.
- Randomization is reproducible: given the same seed and count, output is byte-identical.
- BBQ format is valid: each line is tab-separated and the type prefix is recognized.
- Metadata is sanitized: no Python comments, debug strings, or generator filenames appear
  in the BBQ output when anti-cheat mode is active.
- UTF-8 encoding: the output file is valid UTF-8; confirm with `file -i output.txt` or
  Python `open(..., encoding='utf-8')`.
- YAML-driven generators: all keys accessed from the YAML bank use direct key access
  (`bank[key]`), not `.get(key, default)`, so missing required fields fail loudly.

## Required proof artifacts

Collect these three artifacts before closing any bptools task:

1. Before/after sample output: two BBQ text snippets (or full small output files) showing
   the state before the change and the improved state after. Include at least one question
   instance from each. Place under `debug/bptools/` in the target repo if the directory
   exists; otherwise attach as a comment in the task or changelog entry.
2. Seed-reproducibility log: the terminal output of two runs with `--seed 12345 -d 5`
   followed by a diff showing zero differences. A one-line diff output (`Files identical`)
   is sufficient.
3. Anti-cheat audit checklist: a brief written note confirming:
   - Distractor scrambling active (yes / no / overridden with reason).
   - Answer key not printed to stdout (confirmed by inspecting BBQ output).
   - Metadata sanitization applied (`apply_anticheat_args` called, or not required with reason).

## How to prove the target improved

Answer these questions to demonstrate measurable improvement for an existing-repo task:

- What was the specific defect before (wrong format, missing distractors, leaking answer key,
  non-reproducible output)?
- Show the before/after BBQ snippets with the defect highlighted.
- Run the seed-reproducibility test on the new version and attach the diff.
- Run the anti-cheat audit and confirm no regression.
- Confirm the output passes manual BBQ text inspection for at least three question instances.

A task that cannot produce these three artifacts is not ready to close.
