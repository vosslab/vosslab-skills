# Testing and oracles

Use this reference when building the fixture corpus and validation checks for
WeBWorK PG/PGML problems. The goal is to prove that a problem renders correctly,
grades correctly, and is reproducible before it reaches students.

## Degenerate fixture corpus

Include at least these cases when writing or validating a problem set:

- **Correct answer**: the canonical solution; must grade as 100% correct.
- **Off-by-tolerance**: an answer just outside the tolerance window; must grade
  as wrong for numeric problems (validates the tolerance bound is enforced).
- **Wrong answer**: a clearly incorrect value or selection; must grade as 0%.
- **Partial credit**: for multi-part problems, a response with some sub-parts
  correct; must produce the expected fractional score.
- **Edge-case answer**: zero, negative, very large, or the boundary value
  if the problem involves inequalities or restricted domains.
- **PGML inline math**: a problem with `[` `$var` `]` inline math to verify the
  MathJax rendering path does not break on special characters.
- **PGML block math**: a problem with ``` [`` ``] ``` display math to verify
  block equation rendering.
- **Allowed HTML in PGML**: a problem using `div`, `span`, `br`, `p`, `img`;
  verify all allowed tags render correctly.
- **Forbidden HTML attempt**: verify that inserting a `table` or `td` tag
  triggers a lint warning or is stripped safely by the renderer.
- **Special characters**: ampersands, angle brackets, percent signs in question
  text; verify they are escaped correctly for HTML and TeX output modes.
- **Empty input**: student submits an answer box with no input; must not crash
  and must grade as wrong.
- **Two seeds**: run the same problem with two different `$problemSeed` values
  and confirm both render without errors and produce different (or the same,
  if the problem is non-random) question parameters.

## Oracles

Validate problem rendering and grading against a known-correct reference before
declaring a problem correct.

- **Renderer API lint**: run `python3 references/scripts/lint_pg_via_renderer_api.py -i <file>`
  and confirm `flags.error_flag` is false and `debug.pg_warn` is empty. This is
  the primary oracle for PGML syntax and macro correctness.
- **PG 2.17 HTML-whitelist validator**: check renderer HTML output for any
  `table`, `tr`, or `td` tags; their presence indicates a whitelist bypass
  that will fail on strict renderers.
- **Answer-checker test with known responses**: submit the correct answer,
  a wrong answer, and (where applicable) a partial answer via the renderer
  API's `answers_submitted` parameter; confirm the score matches expectation.
  See `references/docs/RENDERER_API_USAGE.md` for the submission format.
- **Seed reproducibility test**: run the renderer with `$problemSeed = N` twice;
  confirm the rendered HTML is byte-for-byte identical (or canonically
  equivalent) between runs.
- **OPL header validation**: confirm `DESCRIPTION`, `DBsubject`, and `KEYWORDS`
  header tags are present; check that `DBsubject` matches an existing OPL
  subject string if submitting to the OPL.

## Invariants

These properties must hold for every problem in the repo:

- **PGML single-pass**: the rendered HTML contains no literal `[$` or `[_`
  markup strings; these indicate an un-evaluated PGML token.
- **HTML whitelist only**: the rendered HTML contains no `<table`, `<tr`, or
  `<td` tags (check the `renderedHTML` field in the JSON response).
- **Reproducible per `$problemSeed`**: two renderer calls with the same seed
  produce identical question parameters, correct answers, and rendered HTML.
- **Correct grading**: the answer checker accepts the correct answer as 100%
  correct and rejects a clearly wrong answer as 0%.
- **No renderer errors**: `flags.error_flag` is false and `debug.pg_warn`
  contains no entries after a clean render.

## Artifacts

Collect these artifacts to prove a problem or a batch of problems improved:

- **Renderer lint output (before/after)**: capture the lint report for each
  changed file before the edit and after the edit; include both in the task
  handoff so reviewers can see what was fixed.
- **Visual render (HTML mode)**: save or paste the `renderedHTML` output for
  the canonical seed (e.g., `$problemSeed = 1234`) so reviewers can inspect
  layout without running the renderer.
- **Sample grading report**: a table of test responses (correct, wrong,
  partial, empty) with the expected score and the score returned by the
  renderer API.
- **Seed test log**: two renderer calls with different seeds (e.g., 1234 and
  5678) showing the question parameters differ as expected (for random
  problems) and the correct answer matches the changed parameters.
- **OPL header checklist**: a line-by-line listing of the required header tags
  and whether each is present in the file.

## How to prove a problem improved

To close a "fix this problem" task, provide evidence of all four of these:

1. Renderer lint output is clean after the change (no `error_flag`, no
   `pg_warn` entries). Include the before and after lint output if the problem
   previously had lint errors.
2. Visual render (HTML mode) shows the correct layout, with no broken tags,
   missing variables, or garbled math.
3. Grading test confirms correct answer grades as 100% correct and a wrong
   answer grades as 0%.
4. Seed reproducibility confirmed: two calls with the same seed produce the
   same output.
