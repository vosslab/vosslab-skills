# Topic index

This is the routing front door. Start here, match the user request to a row,
then open the named guide. Use [task_selection.md](task_selection.md) first if
the question family or output format is still unclear.

## Problem routing table

| User request / trigger | Question family | Primary guide |
| --- | --- | --- |
| Write or revise stems, choices, or hints | Any family (student-facing text) | `references/question_voice.md`, then `references/docs/QUESTION_PEDAGOGY_GUIDE.md` and `references/docs/QUESTION_VOICE_GUIDE.md` |
| Review question text (rendered output) | Any family | `references/question_voice.md` (rubric groups), then the Review rubric in `references/docs/QUESTION_PEDAGOGY_GUIDE.md` |
| Write a statement bank | MC statements from YAML | `references/question_voice.md`, then `references/docs/problems/multiple_choice_statements/MC_STATEMENTS_AUTHORING_GUIDE.md` |
| Write a matching set | Matching set (MAT) | `references/question_voice.md`, then `references/docs/problems/matching_sets/MATCHING_SET_AUTHORING_GUIDE.md` |
| Absurd or joke choices | MC or MA, statement banks | `references/question_voice.md` (Seriously absurd choices), `references/docs/QUESTION_EXEMPLARS.md` |
| Pick a worked example to imitate | Any family | `references/docs/QUESTION_EXEMPLARS.md` (model and fix entries) |
| Write or fix a multiple-choice question | MC choices in natural order or shuffled when no meaningful order exists | `references/docs/QUESTION_AUTHORING_GUIDE.md` |
| Multiple correct answers, student selects all that apply | Multiple-answer (MA) | `references/docs/QUESTION_AUTHORING_GUIDE.md` |
| Pair terms to definitions or descriptions | Matching set (MAT) | `references/docs/problems/matching_sets/MATCHING_SET_AUTHORING_GUIDE.md` |
| Student types a short text answer | Fill-in-the-blank (FIB) | `references/docs/QUESTION_AUTHORING_GUIDE.md` |
| Question involves chemical structures from PubChem | PubChem molecule | `references/docs/problems/biochemistry-problems/PUBCHEM/README_PUBCHEM_BPTOOLS.md` |
| Question embeds a pedigree chart | Pedigree diagram | `references/docs/problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md` |
| Question embeds a phylogenetic tree | Phylogenetic tree | `references/docs/problems/inheritance-problems/phylogenetic_trees/TREELIB_USAGE.md` |
| Audit or extend MC statement banks | MC statements from YAML | `references/docs/problems/multiple_choice_statements/MC_STATEMENTS_AUTHORING_GUIDE.md` |
| Find all write_question functions and their dates | Function inventory | `references/docs/QUESTION_FUNCTION_INDEX.md` |
| Standardize -d/-x flag handling across generators | Flag unification | `references/docs/UNIFICATION_PLAN.md` |
| Locate or audit YAML question banks | YAML bank index | `references/docs/YAML_QUESTION_BANK_INDEX.md` |
| Debug unexpected BBQ or QTI output format | Engine tracing | `references/api_surface.md` (qti_package_maker section) |

## Per-family detail

### Multiple-choice (MC and MA)

Use `formatBB_MC_Question` for single-correct-answer questions and
`formatBB_MA_Question` for multiple-correct-answer questions. Build the question
stem and distractor list in `write_question(N, args)`, then pass them to the
formatter. The helpers preserve the supplied choice order. Preserve meaningful natural choice
order; otherwise, explicitly scramble the distractors in the generator. Design the puzzle, the
named student errors, and the stem first (see
`references/question_voice.md`). Primary guide: `references/docs/QUESTION_AUTHORING_GUIDE.md`.

### Matching set

Matching sets draw term/definition pairs from a YAML bank. The generator reads
the bank with `bptools.readYamlFile(...)`, selects pairs, and formats with
`formatBB_MAT_Question`. The YAML schema and valid authoring patterns are in
`references/docs/problems/matching_sets/MATCHING_SET_AUTHORING_GUIDE.md`.

### PubChem molecule

PubChem generators use a specialized fetch/cache pattern to pull structure data
from the PubChem REST API. The conventions and caveats specific to bptools
integration are in
`references/docs/problems/biochemistry-problems/PUBCHEM/README_PUBCHEM_BPTOOLS.md`.
Add `time.sleep(random.random())` before any PubChem API call.

### Pedigree diagram

Pedigree questions generate SVG charts and embed them in the question stem.
The pipeline runs a separate SVG renderer; the spec contract for the data format
is in
`references/docs/problems/inheritance-problems/pedigrees/PEDIGREE_SPEC_v1.md`.
The pipeline overview is in
`references/docs/problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md`.

### Phylogenetic tree

Tree questions embed a rendered tree diagram. The spec contract is in
`references/docs/problems/inheritance-problems/phylogenetic_trees/TREELIB_SPEC_v1.md`.
Technical implementation notes are in `TREELIB_TECH.md` and usage examples are
in `TREELIB_USAGE.md` (same directory).

## Alias and trigger vocabulary

- BBQ: Blackboard question format; the default bptools output.
- QTI: IMS question-and-test-interoperability; produced by `qti_package_maker`.
- Distractor: a wrong answer choice in an MC question, derived from a named student error.
- Absurd choice: a deadpan joke choice on the item's own topic, placed beside error-derived choices.
- Stem: the question text presented to the student.
- Exemplar: a worked model or fix entry in `references/docs/QUESTION_EXEMPLARS.md`.
- Rubric: the U, M, S, T, F, and O review items listed in `references/question_voice.md`.
- Question bank: a YAML file containing authored question content drawn by a generator.
- Anti-cheat: the set of bptools flags and practices that prevent answer leakage.
- write_question: the required per-question function called by `collect_and_write_questions`.

## New request routing by shape

- Vague "improve my questions" request: follow [project_workflow.md](project_workflow.md)
  inspect-first path before writing any code.
- Clear new question family: check task_selection.md, load the primary guide above, design the
  puzzle (reasoning target, data, named student errors, exemplar), then start from the nearest
  template in `references/templates.md`.
- Wording complaint ("the stems are wordy", "the distractors are weak"): load
  `references/question_voice.md`, audit rendered output against the routed rubric items, then edit.
- Broken BBQ output: load `references/api_surface.md` and trace through the relevant
  `qti_package_maker` engine writer before changing `formatBB_*` calls.
- Performance or randomization concern: load `references/docs/QUESTION_AUTHORING_GUIDE.md`
  and confirm `collect_and_write_questions` usage, scenario-pool size, and distractor count.
