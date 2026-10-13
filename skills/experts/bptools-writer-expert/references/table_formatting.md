# Table formatting best practices

Use this guide for student-facing HTML tables in bptools questions. Apply the live repository's
question voice and pedagogy guides first. The recommendations below synthesize BPQ generator
sources and BPW emitted question banks; the corpus also contains legacy patterns worth improving.

## Choose an educational family

Use consistent, understated formatting for information tables. When layout conveys scientific
meaning, prioritize those visual relationships. These are flexible defaults, not one universal
table style. Website interface tables have a separate purpose and belong to the website.

| Family | Types and examples | Formatting priority |
| --- | --- | --- |
| Data tables | Lists, measurements, statistical references, calculations | Readable labels, units, numerical alignment, and restrained row shading |
| Reasoning matrices | Experimental conditions, growth tests, inheritance grids | Clear axes, visible cell boundaries, consistent cell dimensions where useful |
| Scientific visuals | Octads, chromosomes, gels, phylogenetic trees | Preserve meaningful geometry, spacing, borders, and colors |
| Supporting layouts | Stacked fractions, diagrams alongside counts | Preserve the relationship between components; style each component by its purpose |

### Data tables

Prefer subtle alternating row shading for longer lists and measurement tables, particularly when
students track a row across several columns. Use white and very pale gray or blue, a slightly
darker neutral header, thin subtle rules, and consistent compact padding. Define explicit text
and background colors for reliable standalone rendering. For example, dark `#202020` text on
`#ffffff` / `#f2f5f7` body rows with a `#e3e8ed` header is a starting palette, not a required one.

Use plain rows for very small tables when striping adds little. Readability shading helps students
track rows; scientific color coding identifies categories. Give experimental groups and biological
colors visual priority. Generate essential row styles inline for portable output.

Left-align descriptions, right-align comparable measurements, and use consistent decimal precision
and units. Keep columns wide enough for their contents. In statistical reference tables, emphasize
the lookup headers; in calculation tables, distinguish totals and intermediate results without
making every row visually prominent.

### Reasoning matrices

Label both axes and center short entries such as genotypes or growth symbols. Use visible cell
boundaries and consistent dimensions when students compare intersections or combinations. Give
long row labels room without sacrificing the regular data grid. Grouped treatment/gene headers
should expose the experimental hierarchy. Apply shading to meaningful groups when useful;
let that grouping determine the shading pattern.

### Scientific visuals

Treat HTML-table diagrams as diagrams first. Preserve the domain renderer's geometry, precise
dimensions, spacing, and meaningful colors, especially for HTML-to-image exams. Equal cells,
nested tables, or fixed widths may be essential. Choose fills, alignment, and wrapping according
to the scientific representation and the domain renderer's contract.

### Supporting and hybrid layouts

Preserve the numerator/denominator relationship in fractions. In an octad-and-count table, use
data-table conventions for the count column and retain the octad renderer's internal formatting.
Scope styling to each component so nested diagrams retain their own formatting.

Put the table before the question it supports. Let headers carry labels and units instead of
repeating the data in prose. Retain meaningful numeric/time order; randomize scenario selection
and unordered experimental labels according to the question design.

## Shared data-table mechanics

The following mechanics support data tables and matrices; apply them to diagram layouts only
where they preserve the scientific representation.

- Use `<th scope="col">` for column headers and `<th scope="row">` for row labels in data
  tables. Bold `<td>` text supplies appearance but no header relationship.
- Prefer one header row. When grouped conditions need multiple rows, make the association explicit
  using appropriate groups/scopes or `id`/`headers`; simplify the hierarchy when possible.
- Name both axes of a matrix. Explain symbols such as `+`, `&ndash;`, and blanks once beside the
  table. Distinguish zero, missing measurements, and not-applicable cells.
- Add a short identifying caption only when needed under the live voice guide. Prefer a real
  `<caption>` when a caption is warranted; give it a concise identifying role distinct from the stem.
- Check the effective column count through every `rowspan` and `colspan`, including totals.
  Verify that randomized headers and values still describe the same observations.

These semantic recommendations follow the
[W3C accessible tables tutorial](https://www.w3.org/WAI/tutorials/tables/).
HTML semantics help the HTML consumer; image conversion loses those header relationships.

## Alignment and compact styling

- Start with `border-collapse: collapse`, thin neutral rules, and modest cell padding. Existing
  sources commonly use roughly 4-10 px padding; choose by content, not a universal pixel target.
  A header rule and row separators can suffice for a small reference table; matrices benefit
  from cell boundaries when students must track intersections.
- Left-align phrases and descriptions. Right-align comparable numbers with consistent precision
  within each measurement column. Center categorical symbols and short matrix entries.
- Use monospace for sequences, genotypes, and lab values/units where alignment helps. Keep prose
  in the normal text font. Format displayed precision intentionally without changing grading data.
- Put shared units in headers. Keep a value and its unit together with `&nbsp;` where necessary;
  use CSS padding for cell spacing. Preserve subscripts, superscripts, and HTML entities.
- Allow prose headers to wrap. A deliberate `<br/>` between a label and its units can help.
  Allocate enough column space for readable text at the intended output size.
## Inline CSS and portability

- Put essential colors, borders, padding, and alignment inline on the relevant elements so the
  question can render independently of BPW stylesheets, CSS classes, and complex selectors.
  Reuse existing Python formatting helpers or shared style strings within the owning module.
  Validate inline styling in the intended consumer.
- Use valid properties and values: `padding: 6px`, `border: 1px solid #888`, and
  `font-size: 1em`. Give nonzero lengths explicit units.
  Use `px` for intentional border/diagram dimensions, `em` for text-relative sizing, and `%`
  where a proportion of available space is intended. `rem` depends on the host's root font size.
- Keep valid unitless values: `line-height: 1.4`, `font-weight: 600`, and zero lengths such as
  `margin: 0`. See MDN's [CSS lengths](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/length)
  and [line-height](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/line-height).
- Use `vertical-align: middle` for compact matrix cells and `vertical-align: top` for multiline
  descriptions when that improves scanning. Use standard CSS declarations for alignment and spacing.

## Width and scientific geometry

- Use content-driven sizing for ordinary data tables: let the browser calculate the overall width
  from the cells. A typical opening tag is `<table style="border-collapse: collapse;">`.
  Add width declarations only where the scientific geometry requires them. For those intentional
  dimensions, keep the overall width consistent with column requirements, padding, borders, and
  spacing. Evaluate the result in the available display area.
- A `500px` table with two `300px` columns can expand beyond its declared width under automatic
  table layout. A scrolling ancestor can then show a horizontal scrollbar. Inspect actual rendered
  widths and ancestor overflow settings; declared widths alone do not establish that a table fits.
  See the [CSS table-width algorithms](https://www.w3.org/TR/CSS22/tables.html#width-layout).
- Give descriptive labels more space than short counts and allow prose to wrap naturally.
  Keep the complete table readable and visible in its intended display area. Resolve excess width
  through content, column allocation, and wrapping. Wide content, fixed columns, and unbreakable
  sequences can still overflow a naturally sized table; check their rendered dimensions explicitly.
- Keep `white-space: nowrap` local to short scientific tokens. Preserve sequence alignment or
  diagram geometry when wrapping would change meaning.
- BPW's `.qpm-selftest[data-bbq]` container currently provides horizontal scrolling. This is an
  existing surrounding-container fallback, not a recommended table design or evidence that a wide
  table is acceptable. Fixing that website container is a separate owner-side task.
- For wide data, improve column allocation and wrapping, shorten headers, or split into labeled
  related tables when the reasoning survives the split. Preserve readable text sizes. If necessary
  scientific geometry still exceeds the available space, report the consumer layout constraint
  and resolve the surrounding layout or output size while preserving full visibility.
- Fixed widths, equal cells, nested tables, and stronger borders may be necessary in Punnett
  squares, octads, gels, or tree renderers. Preserve their domain-specific meaning. Apply data-table
  header rules to the surrounding data, not indiscriminately to each diagram cell.

## Color and theme behavior

- Use restrained shading to help students track ordinary data rows. When color encodes scientific
  meaning, pair it with text or a symbol. Both uses should support the problem rather than compete
  with its content.
- Choose either inherited theme colors on an inherited surface or an explicit foreground/background
  pair for a self-contained scientific table. Hard-coded dark text on a transparent table and
  pale cells with inherited light text both need review in dark mode.
- When a cell overrides the table background, check its text and nested spans against that actual
  surface. Define essential scientific styling in the generated fragment so it survives without
  BPW's site stylesheet. Check contrast with the applicable accessibility guidance.
- Correct source-owned color pairs in the generator/shared helper. Diagnose wrapper or renderer
  defects at their owner; a site-wide recoloring rule can erase scientific color meanings.

## Minimal starting example

This illustrative two-column fragment uses an explicit neutral surface for standalone rendering.
Adapt it to the data; it is not an LMS-certified template or a replacement for a domain helper.

```html
<table style="border-collapse: collapse; color: #202020; background-color: #ffffff;">
  <thead>
    <tr>
      <th scope="col" style="padding: 4px 8px; text-align: left; border-bottom: 1px solid #767676;">Sample</th>
      <th scope="col" style="padding: 4px 8px; text-align: right; border-bottom: 1px solid #767676;">Volume (mL)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row" style="padding: 4px 8px; text-align: left; font-weight: normal;">A</th>
      <td style="padding: 4px 8px; text-align: right; font-family: monospace;">12.5</td>
    </tr>
  </tbody>
</table>
```

## Verify the actual consumer

1. Generate several items, including long labels and the largest supported table. Check data,
   units, precision, totals, header associations, spans, and absence of answer-revealing styling.
2. Inspect emitted BBQ HTML, then render the standalone self-test and the intended BPW integration
   at narrow and desktop widths in light/dark themes. Inspect wrapping, clipping, border visibility,
   scientific symbols, and choice/control separation. Check that the complete table is readable
   and visible at once in its intended display area. Source inspection is not visual acceptance.
3. For image-backed exports, inspect the captured image and package: full table, readable text,
   correct colors, and a usable text alternative where needed. Report lost semantics as an export
   limitation; headers in source HTML do not establish screen-reader access to a bitmap.
   For printed homework or exams, inspect the final page at its intended size and in grayscale.
   Labels, boundaries, and scientific distinctions should remain clear if pale shading disappears.
   Check page breaks: keep a table together when it fits, and retain header context when a longer
   table must span pages. Resolve pagination in the exam/document pipeline using the actual table
   and page dimensions.
4. Claim Blackboard/LMS acceptance only after checking that target. A working BPW page does not
   prove an LMS import, and changing a generator does not refresh already-generated BPW banks.

## Find corpus examples

Read [table_corpus_examples.md](table_corpus_examples.md) when choosing an existing pattern or
tracing a table to its generator. It records survey scope, representative BPQ/BPW paths, useful
patterns, legacy caveats, and evidence limits.
