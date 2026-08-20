# Alternative prototype workstream

**Purpose:** try multiple approaches in parallel when the next step is
ambiguous. Each prototype is its own subagent dispatch.

## Templates

- Prototype A: implement `<feature>` using `<approach 1>`. Single file,
  bounded acceptance: `<test>`. No production wiring.
- Prototype B: implement `<feature>` using `<approach 2>`. Same
  acceptance bar as A. Independent file.
- Comparison report: read both prototype diffs and produce
  `output/proto_compare_<name>.md` with a recommendation grounded in
  acceptance evidence.

**Artifact:** prototype file paths plus comparison report path.

**Blocked fallback:** emit whichever prototype completed plus a
`NEEDS_CONTEXT` note identifying which input the blocked prototype
required.
