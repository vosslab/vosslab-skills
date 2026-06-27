# Topic index

This is the routing front door for WeBWorK problem authoring. Start here, match
the user symptom or request to a row, then open the named guide. Paths shown are
relative to `skills/webwork-writer-expert/`. Derived from
[docs.md](docs.md).

## Problem routing table

| User problem / trigger | Question type | Primary guide | Secondary guide |
| --- | --- | --- | --- |
| Numeric answer, tolerance-based grading | Numeric with tolerance | `references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md` | `references/docs/webwork/PGML_QUESTION_TYPES.md` |
| Formula or symbolic expression answer | Formula / symbolic | `references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md` | `references/docs/webwork/PGML_QUESTION_TYPES.md` |
| Dropdown or list matching | Matching with PopUp layout | `references/docs/webwork/MATCHING_PROBLEMS.md` | `references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md` |
| Ranking, sequencing, or drag-and-drop order | Ordering / ranking | `references/docs/webwork/ORDERING_PROBLEMS.md` | `references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md` |
| Checkbox list, select-all-that-apply | Checkboxes | `references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md` | `references/docs/webwork/PGML_QUESTION_TYPES.md` |
| Radio-button multiple choice | Multiple-choice | `references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md` | `references/docs/webwork/PGML_QUESTION_TYPES.md` |
| Static graph displayed in problem | Graph display | `references/docs/webwork/HOW_TO_MAKE_GRAPHS.md` | `references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md` |
| Molecule or SMILES structure displayed | Graph / molecule | `references/docs/webwork/RDKIT_MOLECULAR_STRUCTURES.md` | `references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md` |
| Free-text / manually graded answer | Essay | `references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md` | `references/docs/webwork/PGML_QUESTION_TYPES.md` |
| Renderer or API lint fails | Lint / rendering error | `references/docs/HOW_TO_LINT.md` | `references/linting.md` |
| PGML renders blank, escaping bug | PGML pitfall | `references/docs/PG_COMMON_PITFALLS.md` | `references/docs/webwork/PGML_LINTER_EXPECTATIONS.md` |
| Color, highlighted text not rendering | Color / accessibility | `references/docs/webwork/COLOR_TEXT_IN_WEBWORK.md` | `references/docs/webwork/COLOR_CONTRAST_ACCESSIBILITY.md` |
| Table or grid layout blocked or broken | HTML whitelist / tables | `references/docs/webwork/HTML_TO_WEBWORK_PLAN.md` | `references/docs/webwork/NICETABLES_TRANSLATION_PLAN.md` |
| Randomization not reproducible, wrong seed | Randomization | `references/docs/webwork/RANDOMIZATION_REFERENCE.md` | `references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md` |
| OPL header tags missing or wrong | Header metadata | `references/docs/webwork/WEBWORK_HEADER_STYLE.md` | `references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md` |
| Key phrase or data not emphasized in stem | Question statement | `references/docs/webwork/QUESTION_STATEMENT_EMPHASIS.md` | `references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md` |
| PG macro not found, wrong PG version | Macro / version | `references/docs/webwork/PG_2_17_RENDERER_MACROS.md` | `references/docs/webwork/PG_2.20_to_2.16_features.md` |
| PubChem or biochem molecule problem | PubChem PGML | `references/docs/pubchem/PGML_PUBCHEM_CONVERSION_SUMMARY.md` | `references/docs/pubchem/PUBCHEM_PGML_SYNTAX_NOTES.md` |

## Per-type detail

### Numeric and formula answers

Default grading uses `Compute()` in a matching MathObject context with
an explicit tolerance. Document the tolerance policy in a comment near the
answer variable. See `references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md`
(grep `Compute`, `tolerance`).

### Matching with PopUp

PG 2.17 does not allow `table`/`tr`/`td` in HTML mode. Use `PopUp` widgets
inside flexbox `div` containers. See `references/docs/webwork/MATCHING_PROBLEMS.md`
(grep `PopUp`, `flex`).

### Ordering / DraggableProof

Use `DraggableProof` for ordering questions. Seeds must be reproducible.
See `references/docs/webwork/ORDERING_PROBLEMS.md` (grep `DraggableProof`,
`$problemSeed`).

### Checkboxes

Use `CheckboxList` with an explicit correct-answer list. Partial credit applies
when multiple boxes are correct. See `references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md`
(grep `CheckboxList`, `partial`).

### Graphs and SVG

Use `PGgraphmacros.pl` for static display graphs. SVG inline is allowed in the
HTML whitelist. See `references/docs/webwork/HOW_TO_MAKE_GRAPHS.md`
(grep `PGgraphmacros`, `insertGraph`).

### Lint and rendering errors

Run the renderer API lint script first. Check `flags.error_flag`,
`debug.pg_warn`, and `debug.internal` in the JSON response. See
`references/docs/HOW_TO_LINT.md` and `references/linting.md`.

## Alias and trigger vocabulary

- Numeric: calculate, compute, exact answer, round to, within tolerance.
- Symbolic: simplify, factor, expand, formula, expression.
- Matching: match each, pair, which goes with, drag to match.
- Ordering: rank, put in order, arrange, sequence, sort.
- Checkboxes: select all, check all that apply, which of the following.
- Essay: explain, describe, justify, short answer, manually graded.
- HTML whitelist: table blocked, tr/td forbidden, use div, use niceTables.
- PGML single-pass: variable contains HTML, use `[$var]*`, not `[$var]`.
- Randomization: `$problemSeed`, `PGrandom`, reproducible, same seed same answer.
