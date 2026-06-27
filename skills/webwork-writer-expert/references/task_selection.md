# Task selection

Use this reference to classify a WeBWorK problem request before consulting the
topic index or authoring guides. Answer the questions below to frame the task,
then route to [topic_index.md](topic_index.md).

## Problem type

Identify the primary answer mechanism:

- **Multiple-choice (radio)**: one correct answer from a fixed list; use
  `RadioButtons` or `PopUp` depending on layout needs.
- **Numeric with tolerance**: a single numeric answer graded within a tolerance
  window; use `Compute()` with a numeric context and a tolerance setting.
- **Formula / symbolic**: an algebraic or mathematical expression graded by
  symbolic equivalence; use `Compute()` in a `Formula` or `Numeric` context
  with MathObject type matching the expected expression class.
- **Matching**: items from one list paired with items from another; use
  `PopUp` widgets in a PGML flex-div layout (table/tr/td are blocked).
- **Ordering / ranking**: a sequence to arrange in order; use
  `DraggableProof` or an ordered `PopUp` sequence.
- **Graph / image**: a static graph displayed via `PGgraphmacros.pl`; the
  answer may be numeric, formula, or multiple-choice depending on what the
  graph illustrates.
- **Essay**: free-text answer graded manually; use `essay_box()` and flag as
  instructor-graded.
- **Checkboxes**: one or more correct answers from a list; use
  `CheckboxList`.

## Input constraints

- HTML whitelist: `div`, `span`, `br`, `p`, `a`, `img`, `svg` are allowed
  inside PGML. `table`, `tr`, `td` are blocked by the PG 2.17 HTML whitelist;
  replace tables with flexbox `div` layouts or `niceTables`.
- PGML is single-pass: do not construct PGML tag wrappers inside Perl string
  variables. If a variable holds HTML, render it with `[$var]*` so the HTML
  is not double-escaped.
- MathJax color macros (`\color{red}{...}`) are blocked; use HTML `span` with
  inline CSS for colored text (see `references/docs/webwork/COLOR_TEXT_IN_WEBWORK.md`).
- Answer boxes appear inline inside PGML with `[_]{$answer}` syntax; keep
  setup, answer definitions, and PGML text in separate sections.

## Randomization strategy

- Use `PGrandom` seeded with `$problemSeed` (available in every problem as the
  seed value set by the student-assignment system) for deterministic, reproducible
  randomization.
- Do not use bare `rand()` or `SRAND()` unless you explicitly want to reset the
  global RNG; resetting the global RNG breaks reproducibility across macro calls.
- Sort hash keys before random selection so the ordering is stable across Perl
  versions and platforms.
- For randomized numeric parameters, choose bounds that keep the correct
  numeric answer reasonable for students and within any stated tolerance policy.
- Seed reproducibility is an invariant: the same `$problemSeed` must always
  produce the same question and the same correct answer.

## Grading model

Identify the grading mechanism before writing the problem:

- **Symbolic equivalence**: `Compute("expression")` in a matching MathObject
  context (e.g., `Context("Numeric")` or `Context("Formula")`); correct if the
  student answer is algebraically equivalent.
- **Numeric tolerance**: `Compute(value)->with(tolType => 'relative', tolerance => 0.001)`
  or an absolute tolerance; correct within the stated window.
- **Partial credit**: each sub-part graded independently; the overall score
  is the weighted sum; document weights in a comment near the answer definitions.
- **Custom checker**: a `sub` passed to `checker =>` inside `Compute()` or
  `List()`; use only when symbolic equivalence and tolerance are not sufficient
  (e.g., ordering problems, graph-based answers, multi-step proofs).
- **Manual / essay**: no auto-grader; mark the answer with `essay_cmp()` and
  note in the OPL header that grading is manual.

## Clarifying questions to answer internally

- What answer type does the student produce: a number, an expression, a
  selection, a sequence, or free text?
- Does the answer vary per seed, or is it a fixed correct answer across all seeds?
- What HTML elements are in the question body, and do any conflict with the
  whitelist?
- Does the problem require multi-part grading (partial credit)?
- Is a local renderer available to lint and visually verify the output?
- What PG version is the target renderer running (2.16, 2.17, 2.20)?
