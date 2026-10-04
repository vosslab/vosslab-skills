# Testing and oracles

Use this reference when validating a new or modified bptools generator. Define fixtures, choose
oracles, run the student-text review, and collect the four proof artifacts before closing any
authoring task.

## Degenerate fixture corpus

Include at least these cases when authoring or validating a generator:

- Single instance: run with `-d 1` to confirm the script does not crash and produces one
  well-formed BBQ line.
- Student-facing randomness: run the generator with `-d 5` and confirm it uses true-random
  scenario selection and produces valid items. Do not require two random draws to differ: a
  random draw may repeat. Preserve a meaningful natural choice order; for choices with no
  meaningful order, inspect a sample to confirm the generator explicitly scrambles them.
- Long answer text: supply a distractor or stem that is near the maximum expected length;
  confirm the formatter does not truncate or corrupt it.
- Unicode and special characters: if the domain uses Greek letters, subscripts, or HTML
  entities, confirm they appear as escaped HTML entities (`&alpha;`, `&beta;`) and not as
  raw UTF-8 in the BBQ output.
- Empty or minimal YAML bank: for YAML-driven generators (matching sets, MC statements),
  test with a bank containing only one valid pair; the generator must handle it without
  crashing or producing duplicate distractors.
- Edge case per family:
  - MC/MA: too few meaningful alternatives to assess the intended reasoning; revise the scenario
    or item format instead of padding the choices with weak distractors.
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
  are plausible or deliberately absurd, and no debug or key-revealing text appears in a
  student-facing stem or choice.
- Anti-cheat audit: for choices with no meaningful natural order, confirm the generator
  explicitly scrambles them and the correct answer position is not systematically first. For a
  meaningful natural ladder, confirm the displayed order remains natural. When a generator
  exposes anti-cheat overrides, confirm it applies them; collection otherwise applies defaults.

## Student-text oracles

These oracles judge the words a student reads. They follow the Review rubric in
`references/docs/QUESTION_PEDAGOGY_GUIDE.md`; `references/question_voice.md` routes each item
type to its rubric items.

- Rendered-sample review: render at least five items (`-d 5`), read each stem and choice set as a
  student, and score it against the routed rubric items. Record each failing item ID and the
  edit that fixed it, then re-run the generator and re-read.
- Distractor-rationale table: list every choice of one rendered item with its source. Each wrong
  choice names the student error that produces it, or carries the label "absurd". Each named
  error maps to the line or comment in the generator that computes it. Example for a dilution
  item (total volume 400 &micro;L, 1:10 dilution):

  | Choice | Source | Generator location |
  | --- | --- | --- |
  | 40 &micro;L | key: total volume / dilution factor | `calc_aliquot()` |
  | 360 &micro;L | named error: aliquot and diluent swapped | `distractor_swapped()` |
  | 400 &micro;L | named error: total volume used as the aliquot | `distractor_total()` |
  | 80 &micro;L | named error: aliquot doubled | `distractor_doubled()` |

- Advisory checker run: from the target repo root, run
  `source source_me.sh && python3 devel/check_question_text.py -i <bbq file>`. Findings map to
  rubric items M4, S3, T2, and parts of U4 and U7. Fix each finding or record why it is
  intentional (for example a deliberate absurd choice). A clean report supports the rubric read;
  the read still happens.
- Independent answer-key verification, by item type:
  - Computed items (crosses, distances, dilutions, digests): enumerate every scenario in a
    temporary check under `tests/_temp/` of the target repo, or recompute with a second
    implementation, and compare each result to the generator's key.
  - Recall, matching, and statement items: a separate reader (another agent or a person) checks
    each key against the source data or YAML bank, item by item.
  - Verification comes from a method independent of the generator's own logic; a reread of that
    logic leaves a real key bug in place.

## Invariants

Test these invariants for every generator, regardless of question family:

- The correct answer is never placed in the distractor list.
- All choices are distinct; every wrong choice has a named error or an absurd label.
- Student-facing scenario selection uses true randomness. Preserve meaningful natural choice
  order; explicitly scramble choices in the generator only when no meaningful order exists.
  Deterministic scenario selection exists only for debugging, reproducibility checks, or unit
  tests, behind an explicit option such as `--sorted` from `bptools.add_scenario_args`.
- BBQ format is valid: each line is tab-separated and the type prefix is recognized.
- Metadata is sanitized: no Python comments, debug strings, or generator filenames appear
  in the BBQ output when anti-cheat mode is active.
- UTF-8 encoding: the output file is valid UTF-8; confirm with `file -i output.txt` or
  Python `open(..., encoding='utf-8')`.
- YAML-driven generators: all keys accessed from the YAML bank use direct key access
  (`bank[key]`), not `.get(key, default)`, so missing required fields fail loudly.

## Required proof artifacts

Collect these four artifacts before closing any bptools task:

1. Rendered before/after sample: two BBQ text snippets (or full small output files) showing
   the state before the change and the improved state after. Include at least one question
   instance from each. Greenfield tasks supply the after sample only. Place under
   `debug/bptools/` in the target repo if the directory exists; otherwise attach as a comment
   in the task or changelog entry.
2. Distractor-rationale table: the table described under Student-text oracles, for at least
   one rendered item per question family touched.
3. Key-verification note: a short written note naming the verification method used for each item
   type, the scenarios or items covered, and the result.
4. Checker report excerpt: the `devel/check_question_text.py` output lines for the changed
   generator (or the line stating no findings), with the disposition of each finding.

## How to prove the target improved

Answer these questions to demonstrate measurable improvement for an existing-repo task:

- What was the specific defect before (wrong format, missing distractors, leaking answer key,
  rubric failures such as a testwise cue, a preamble in the stem, or a distractor with no named
  error)?
- Show the before/after BBQ snippets with the defect highlighted.
- Run the advisory checker on both versions and compare the findings.
- Run the anti-cheat audit and confirm no regression.
- Confirm the output passes the rendered-sample review for at least five question instances and
  that the key is verified independently.

A task that cannot produce the four proof artifacts is not ready to close.
