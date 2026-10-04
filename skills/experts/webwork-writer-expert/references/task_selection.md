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

## Item type

Name the PGML item type from the list above (radio or pop-up single answer,
checkbox list, matching pop-ups, numeric or string blank, draggable ordering).
The item type selects the student-text review rubric; the mapping lives in Review
rubric routing in [topic_index.md](topic_index.md). Note whether the item draws on
a true and false statement pool, because that adds the S rubric group.

## Reasoning target

State what the student does with the data, on the revised Bloom cognitive-process
scale, before choosing data or distractors:

- **Apply**: use a rule on a new case. Randomize the parts that change the answer
  and pick numbers that make the intended arithmetic come out whole.
- **Analyze**: pull structure out of data such as a gel, table, graph, or cross.
  Present the data first and let it carry the difficulty.
- **Evaluate**: judge a claim or a calculation. Use show-the-setup choices or an
  error-analysis stem ("What did they do wrong?").
- **Recall**: vocabulary and fact sets, such as matching sets and statement pools.
  Label these items as recall.

Examples: "analyze a gel to identify the father"; "apply 2/3 survival to a
lethal-allele cross"; "evaluate which worked distance calculation pairs the right
progeny classes". The full design steps are in
[references/docs/QUESTION_PEDAGOGY_GUIDE.md](docs/QUESTION_PEDAGOGY_GUIDE.md)
(Design workflow).

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
- What is the reasoning target: apply, analyze, evaluate, or recall?
- Which named student errors become the wrong choices?
- Does the answer vary per seed, or is it a fixed correct answer across all seeds?
- What HTML elements are in the question body, and do any conflict with the
  whitelist?
- Does the problem require multi-part grading (partial credit)?
- Is a local renderer available to lint and visually verify the output?
- What PG version is the target renderer running (2.16, 2.17, 2.20)?
