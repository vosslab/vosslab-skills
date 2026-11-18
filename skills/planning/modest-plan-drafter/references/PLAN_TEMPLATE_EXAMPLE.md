# Worked Modest plans

The first example uses the compact default for a quick fix. The second uses alternate headings
to give a measured finding and a publication contract a visible place.

```markdown
# Plan: Repair the workbook link

## Goal and context

The lab guide still links to last term's workbook. Point students to the current editable workbook
from the existing download link.

## Design philosophy

Correct the link at its source so the existing student workflow still applies.

## Scope

Update the workbook destination in the lab guide. Preserve the link label and surrounding
instructions.

## File scope

| File or directory | Intended change | Canonical source, for generated output |
| --- | --- | --- |
| `docs/labs/probability.md` | Point the workbook link to the current file. | |

## Milestones

| M | Title | Summary | Goal |
| --- | --- | --- | --- |
| 1 | Restore the download | Correct the guide's link and open it once. | Students reach the current editable workbook. |

*Plan created with `vosslab-skills:modest-plan-drafter`.*
```

```markdown
# Plan: Align practice worksheet links

## Goal and evidence

A link audit found three course guides and a worksheet index pointing to retired worksheets.
Make the guides and index point to the current editable practice worksheets.

## Design philosophy

Use the existing worksheet catalog as the source for the generated index. Keep link text familiar
to students who follow the guides week to week.

## Scope and contracts

Update the affected catalog entries and guide links, then regenerate the worksheet index. Preserve
the published guide and index URLs. Keep each guide's link paired with the worksheet for that topic.

## File scope

| File or directory | Intended change | Canonical source, for generated output |
| --- | --- | --- |
| `docs/worksheets.yaml` | Update the three worksheet destinations. | |
| `docs/courses/*/practice.md` | Correct the affected links. | |
| `docs/worksheet_index.md` | Regenerate the worksheet index. | `docs/worksheets.yaml` |

## Milestone plan

| M | Title | Summary | Goal |
| --- | --- | --- | --- |
| 1 | Align worksheet links | Update the catalog and affected course guides. | Each guide points to its current worksheet. |
| 2 | Refresh the index | Regenerate the index and check each updated listing. | The index agrees with the course guides. |

*Plan created with `vosslab-skills:modest-plan-drafter`.*
```
