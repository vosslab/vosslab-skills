# Plan headings reference

Use `# Plan: <descriptive title>` and sentence-case headings. Fill the applicable sections in the
order below. Copy the default shape from [PLAN_TEMPLATE_BLANK.md](PLAN_TEMPLATE_BLANK.md) and use
[PLAN_TEMPLATE_EXAMPLE.md](PLAN_TEMPLATE_EXAMPLE.md) for illustrations. Honor a requested format
and carry the same information into it.

| Default heading | When and how to use it |
| --- | --- |
| Goal and context | Required. State the problem, relevant context, and intended outcome. Use **Goal and evidence** when a finding or measurement motivates the work. Split into **Context** and **Objectives**, in that order, when the outcomes need their own list. |
| Design philosophy | Required. Explain a guiding choice or tradeoff. One sentence is enough when the choice is simple. |
| Scope | Required. Define the work covered. Use **Scope and contracts** when authoring rules, compatibility requirements, or existing behavior materially constrain the deliverable. |
| Non-goals | Include when exclusions clarify the boundary. |
| Current state summary | Include when material facts about current behavior need more room than the opening. |
| Architecture boundaries and ownership | Include when component responsibilities constrain the work. |
| File scope | Required for identifiable file changes. Use the standalone table to name expected paths, intended changes, and canonical sources for generated outputs. Use a single row for one file or directory and pattern rows for broad changes. Use **File scope and interfaces** when known interfaces also constrain the edits. |
| Milestones | Required. Use the `M / Title / Summary / Goal` table. State the deliverable and purpose of each milestone at a high level. Cover the whole scope. One row can cover a quick fix. **Milestone plan** is an alternate heading for the same table. |
| Open questions and decisions needed | Include when material decisions remain unresolved. Give enough context for the planner or implementer to resolve them. |

Reserve prerequisite and sequencing detail, risk registers, acceptance evidence, and execution
status for detailed plans or delivery records. Finish the plan with the exact footer specified in
[../SKILL.md](../SKILL.md).
