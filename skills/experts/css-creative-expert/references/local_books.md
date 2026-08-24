# Local CSS source map

Use this map with [reference_survey.md](reference_survey.md). The local,
gitignored corpus contains broad books, focused web guides, and one secondary
example collection. Its folders describe the job a source serves: visual
outcomes in `css-creative/`, language mechanics in `css-technical/`.

## Source classes

- Broad book: search a chapter or topic, then read enough surrounding material
  to understand the design model.
- Focused guide: search the exact property, function, or technique and read the
  nearby examples and limitations.
- Secondary examples: mine patterns and prompts for ideas, then establish the
  implementation from primary documentation and rendered evidence.

## Visual craft sources

- `references/local-only/css-creative/Background_Magic_CSS_The_Complete_Guide_to_Creating_Stunning_Backgrounds-2023.md`:
  focused guide for layered, image, pattern, gradient, and video backgrounds.
- `references/local-only/css-creative/CSS_MagiC_51_Tricks_to_Take_Your_CSS_Skills_to_the_Next_Level-2023.md`:
  broad recipe book for shadows, masks, clipping, blend modes, filters, and
  small interaction effects.
- `references/local-only/css-creative/SVG_Animations-2017.md`: broad book for
  SVG structure, CSS animation, motion choreography, and animated interfaces;
  verify current APIs and library advice.
- `references/local-only/css-creative/Working_With_Colors_Guide-2016.md`:
  focused guide for color models, atmosphere, shadows, blend modes, and color
  accessibility concepts; verify current color syntax and gamut behavior.

## Technical mechanism sources

- `references/local-only/css-technical/A_Complete_Guide_to_CSS_Flexbox-2026.md`:
  focused guide for axes, alignment, wrapping, order, and flex sizing.
- `references/local-only/css-technical/A_Complete_Guide_to_CSS_Grid_Layout-2021.md`:
  focused guide for tracks, areas, placement, auto-flow, subgrid, and alignment.
- `references/local-only/css-technical/CSS3_and_SVG_with_GPT-4-2024.md`:
  secondary CSS3 and SVG examples; use its CSS3 and SVG chapters, then verify
  every selected pattern independently.
- `references/local-only/css-technical/CSS_Anchor_Positioning_Guide-2024.md`:
  focused guide for anchors, target placement, fallback positions, and edges.
- `references/local-only/css-technical/CSS_Color_Functions-2025.md`: focused
  guide for color spaces, Oklab/Oklch, `color()`, `color-mix()`, and relative
  color syntax.
- `references/local-only/css-technical/CSS_Custom_Properties_Guide-2021.md`:
  focused guide for token naming, inheritance, fallbacks, `@property`, state,
  and JavaScript integration.
- `references/local-only/css-technical/CSS_Functions_Guide-2020.md`: focused
  index for sizing, comparison, transform, filter, gradient, and shape
  functions; verify additions and support in current specifications.
- `references/local-only/css-technical/CSS_Gradients_Guide-2020.md`: focused
  guide for linear, radial, conic, repeating, and patterned gradients.
- `references/local-only/css-technical/CSS_Selectors-2024.md`: focused selector
  and combinator lookup, including attributes, pseudo-selectors, and nesting.
- `references/local-only/css-technical/CSS_in_Depth_Second_Edition-2024.md`:
  broad book for cascade, units, layout, stacking, responsive design, layers,
  modular CSS, scope, typography, and motion.
- `references/local-only/css-technical/Cascade_Layers_Guide-2022.md`: focused
  guide for layer order, origins, `!important`, use cases, and debugging.
- `references/local-only/css-technical/Centering_in_CSS_Guide-2014.md`: dated
  focused guide for centering decision cases; prefer current grid and flexbox.
- `references/local-only/css-technical/Dark_Mode_in_CSS_Guide-2020.md`: focused
  guide for preference detection, user toggles, persistence, user-agent styles,
  and dark-theme design considerations.
- `references/local-only/css-technical/Responsive_Web_Design_with_HTML5_and_CSS-2022.md`:
  broad book for media and container queries, fluid layout, images, SVG,
  effects, animation, custom properties, functions, and forms.
- `references/local-only/css-technical/SVG_Fallbacks_Guide-2015.md`: dated
  focused guide for `<img>`, `<object>`, background-image, inline SVG, and icon
  fallbacks; verify which fallbacks remain necessary.
- `references/local-only/css-technical/Unleashing_the_Power_of_CSS-2023.md`:
  broad technical book for `:has()`, container queries, intrinsic responsive
  layout, and modern CSS organization.

## Lookup method

1. Start with [topic_index.md](topic_index.md) and choose one source.
2. Use the verified term and rating in
   [reference_survey.md](reference_survey.md).
3. Run `rg -n -C 8 -F` with that term and bare path, then read the full
   surrounding section rather than copying an isolated match.
4. Add a second source only when it clarifies a competing design choice.
5. Use MDN, CSS specifications, and rendered target evidence when the corpus is
   absent, thin, dated, or version-sensitive.
