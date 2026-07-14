# README scoring rubric

Score the current README before editing and the finished README after verification. Read
the whole page as a newcomer, interpret it in the context of this project, and use
repository evidence for every awarded point. Record one short evidence note per category
so the score makes the judgment inspectable.

## Read and interpret

Score through editorial reading and repository evidence. Award points for reader
outcomes, placement, and project fit. Use automated checks for the quality gates. Treat
headings, badges, screenshots, code blocks, tables of contents, and section counts as
tools whose value comes from the reader outcome they create.

Interpret proof according to the project:

- A library can prove value with a small input/output example and stable API path.
- A CLI can prove value with one real command, representative output, and exit behavior.
- A GUI or web app can prove value with a focused screenshot or short interaction.
- A research, data, or educational project can prove value with provenance, method,
  sample results, and a route to reproduce them.
- A skill collection can prove value with representative tasks, selection guidance, and
  a concrete before/after outcome.

Use the closest fit and explain the choice. Give full credit when the reader outcome is
excellent even when the README uses an unconventional structure. Convert every material
deduction into a specific next step.

## Quality gates

A README reaches the 90+ `Distinctive landing page` band when all gates pass:

- The opening passes the repository's first-paragraph test, including the 250-character
  About-field limit.
- Quick-start and representative-example commands are verified through safe execution
  or an equivalent canonical check.
- Local Markdown links pass the repository link test.
- Current-behavior claims, status, and compatibility trace to repository evidence. Any
  license statement also traces to repository evidence.
- Adoption-blocking limitations appear before the onboarding path.
- Animated proof follows the screenshot skill's duration, motion, prose-equivalent,
  alt-text, and file-size requirements.

Treat an unmet gate as the highest-priority next step even when the numeric score is
high.

## Scorecard

| Category | Points | Full-credit evidence |
| --- | ---: | --- |
| Purpose, audience, and value | 15 | Opening and orientation make what, who, problem, and benefit clear in audience language |
| Distinctive project identity | 15 | Signature promise, project-specific voice or heading, and a treatment unique to this project |
| Proof and demonstration | 20 | Live demo, visual, output, transformation, benchmark, or worked example directly proves the main promise |
| Meaningful first success | 15 | Canonical prerequisites, install, real run, and expected result form one verified path |
| Usage and conceptual orientation | 10 | Representative example plus the concepts or constraints readers need before deeper work |
| Documentation navigation | 10 | Curated, audience-ordered routes with accurate one-line descriptions |
| Adoption context | 5 | Status and adoption-blocking limitations are clear; optional help, license, or provenance routes are concise, useful, and evidenced |
| Presentation, accessibility, and currency | 10 | Scannable hierarchy, descriptive visuals, prose equivalents, current links and commands, resolved placeholders |
| **Total** | **100** | |

Score `Adoption context` against the information this project's audience needs. Award
full credit without help or license sections when those routes would add little reader
value; evaluate their accuracy and usefulness when the README includes them.

## Awarding points

For each category, choose the supported level and its exact whole-point score:

| Level | 20-point category | 15-point category | 10-point category | 5-point category | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| Full | 20 | 15 | 10 | 5 | Complete, specific, verified, and well placed |
| Strong | 15 | 11 | 8 | 4 | Useful and convincing, with one visible gap |
| Partial | 10 | 8 | 5 | 3 | Present but generic, incomplete, weakly placed, or lightly evidenced |
| Minimal | 5 | 4 | 3 | 1 | Mentioned with little practical value |
| Unmet | 0 | 0 | 0 | 0 | The reader outcome has no current, supported evidence |

Use one listed score per category. Add a one-line evidence note and one-line improvement
for every category below full credit. This produces deterministic whole-point totals
while preserving editorial judgment about the supported level.

## Score bands

| Score | Interpretation | Next action |
| ---: | --- | --- |
| 90-100 | Distinctive landing page | Polish details and keep proof current |
| 75-89 | Strong project README | Complete the highest-value proof, identity, or first-success gap |
| 60-74 | Functional but plain | Strengthen value, first success, examples, and project-specific presentation |
| 40-59 | Thin or documentation-first | Rebuild the newcomer journey around purpose and proof |
| 0-39 | Missing or misleading front door | Establish verified identity, status, and onboarding foundations |

## Scoring report

Use this compact format in the verification report:

```text
README score: 82/100 -> 94/100
Gates: 6/6 pass
Strongest gain: Proof and demonstration, 10 -> 20
Remaining opportunity: Add a current output comparison, owner screenshot-docs,
target README.md and docs/screenshots/output_comparison.png
```

Pair every remaining opportunity with the dispatch brief in
[landing_page_ideas.md](landing_page_ideas.md): owner, target files, evidence, work,
success criteria, and verification.

## Source interpretation

- [Axiom README Score](https://github.com/axiom-experiment/readme-score) provides a useful
  completeness model and actionable suggestions. This rubric applies those ideas through
  close reading and repository evidence.
- [Better README scoring rubric](https://github.com/Thomaszhou22/better-readme/blob/main/references/scoring-rubric.md)
  shows that repository type changes what good evidence looks like. Its separate
  marketing-heavy and skill-repository tracks are replaced here by one project-aware
  interpretation step for a broader maintainer audience.
- [ScoreMe](https://clayallsopp.github.io/readme-score/) illustrates measurable README
  surface features. This rubric awards their demonstrated value to a newcomer.

Source availability note: the SkillsMP README Score listing supplied during research
was unavailable for direct review and contributed no guidance to this rubric.
