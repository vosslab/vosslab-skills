# Project workflow

Use this reference when the skill is invoked on a target WeBWorK problem repo,
not while building webwork-writer-expert itself.

## Detect project state

Inspect the target repo before writing or editing any PG/PGML file:

- Search for existing `.pg` and `.pgml` files to gauge the current authoring
  style and macro usage.
- Search for a local renderer harness or lint script.
- Search for OPL header tags (`DESCRIPTION`, `DBsubject`, `KEYWORDS`) to gauge
  metadata coverage.
- Search for grading checks or test scripts that verify correct/incorrect answers.

If any of these exist, follow the existing-repo path. If none exist, follow the
greenfield path.

## WebWork design contract

Both paths write and maintain a design contract. Use the target repo's existing
docs location when present; otherwise create `docs/WEBWORK_DESIGN.md`. The
contract records:

- PG version the target renderer runs (2.16, 2.17, 2.20, or later).
- HTML whitelist policy: which tags are allowed and which are blocked (default:
  `div`, `span`, `br`, `p`, `a`, `img`, `svg` allowed; `table`, `tr`, `td` blocked
  on PG 2.17 and later).
- Rendering mode in use: `HTML`, `TeX`, or `PTX` (affects PGML escaping rules and
  color strategies).
- Tolerance policy: one location per problem repo, one tolerance type
  (`absolute` or `relative`), documented reason and magnitude.
- `$problemSeed` source: how seeds are set by the assignment system and whether
  the repo has a custom seed-injection mechanism.
- Inline grading convention: answer boxes use `[_]{$answer}` syntax inside PGML.
- Whether partial credit applies globally or per problem type.

## Greenfield path

Use when the target repo contains no existing PG/PGML files or grading harness.

1. Write the WebWork design contract first as the authoring source of truth.
2. Choose PGML primitives against explicit criteria:
   - What answer types are needed (numeric, symbolic, matching, ordering,
     checkbox, essay, graph)?
   - What PG version does the target renderer run?
   - Are there custom macros or macro packages already installed on the renderer?
   - Is partial credit required globally?
3. State early scope assumptions: number of problems, subject area (PGML
   `DBsubject`), intended student level, and whether problems will be submitted
   to the OPL.
4. Seed a fixture set: write at least one representative problem per question
   type, rendered and lint-checked before declaring the scaffold done.
5. Build the minimal problem scaffold. The scaffold is complete only when all
   of these pass:
   - PGML structure follows `references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md`.
   - Renderer API lint returns no `error_flag` and no `pg_warn` entries.
   - Visual render (via `--html` mode) is inspected and confirmed correct.
   - OPL header tags are present and valid.
   - Randomization is tested with at least two distinct seed values.
6. Add problems on top of the validated scaffold following the design contract.

## Existing-repo path

Use when the target repo already has `.pg`/`.pgml` files, a renderer harness,
or grading checks.

1. Inspect first before changing anything:
   - List existing `.pg`/`.pgml` files and note the question types in use.
   - Read the renderer harness setup (how to run the renderer, what port, what
     lint script).
   - Read OPL header tags in a sample of problems to identify the current
     metadata style.
   - Read any grading checks to understand what answer-checker patterns are
     established.
2. Identify the current design:
   - Which PGML patterns are used consistently vs. inconsistently?
   - Are there any problems that fail renderer lint today (before changes)?
   - Are there problems that use blocked HTML (`table`, `tr`, `td`)?
   - Are there problems with non-reproducible randomization?
3. Propose and implement repo-specific changes one category at a time:
   - Fix PGML syntax or escaping bugs first (renderer lint output is the oracle).
   - Replace blocked HTML second (one problem at a time; render after each fix).
   - Improve randomization or grading third.
   - Add missing OPL header metadata last.
4. Prove improvement after each category of change:
   - Capture renderer lint output before and after the change for the affected
     file.
   - Confirm visual render looks correct via `--html` mode.
   - Confirm correct/incorrect/partial-credit answers grade as expected using
     the renderer API's `answers_submitted` field.
   - Confirm the same `$problemSeed` produces the same question and answer
     before and after (seed reproducibility invariant).

## Problem authoring review checklist

Before closing any problem authoring task, verify:

- PGML structure follows setup / answer-definitions / PGML-text separation.
- Renderer API lint is clean: `error_flag` false, no `pg_warn` entries.
- Visual render (`--html` mode) is inspected and confirmed correct.
- HTML whitelist is respected: no `table`, `tr`, or `td` in PGML output.
- PGML single-pass rule is respected: no tag wrappers built inside Perl strings.
- Randomization is seeded with `$problemSeed` and is reproducible.
- Correct answer grades correctly; a clearly wrong answer grades wrong; a
  partial answer grades with partial credit when applicable.
- OPL header tags are present (`DESCRIPTION`, `DBsubject`, `KEYWORDS` at minimum).
- Color is implemented via HTML span/CSS, not MathJax macros.
