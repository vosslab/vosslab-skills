# CSS reference survey

This survey records verified search routes for the mixed local CSS corpus.
Ratings mean **strong** for a dedicated treatment, **partial** for a useful
section or example collection, **thin** for dated or narrow treatment, and
**not covered** for a topic that requires current primary documentation.

## How to use this survey

- Start from [topic_index.md](topic_index.md), then search one listed term in
  its named bare path. Read the complete surrounding section before applying it.
- Prefer strong coverage, use partial or thin sources as corroboration, and
  check MDN and CSS specifications for browser support and evolving syntax.
- Use focused guides for exact lookups, broad books for the surrounding design
  model, and secondary examples only for ideas. The source classes are recorded
  in [local_books.md](local_books.md).
- With `references/local-only/` unavailable, continue through the committed
  guides, semantic CSS reasoning, rendered screenshots, computed styles, and
  current primary documentation.
- Delegate measured contrast audits and palette repair to
  `color-accessibility-expert`; retain accessible color-role design here.

## Visual craft

| Topic | Path and verified grep term | Section | Rating |
| --- | --- | --- | --- |
| Layered and image backgrounds | `references/local-only/css-creative/Background_Magic_CSS_The_Complete_Guide_to_Creating_Stunning_Backgrounds-2023.md`; `Chapter 8: Creating Multi-Layer Backgrounds` | Chapter 8 | strong |
| Blend, mask, clip, and filter recipes | `references/local-only/css-creative/CSS_MagiC_51_Tricks_to_Take_Your_CSS_Skills_to_the_Next_Level-2023.md`; `How to use CSS blend modes` | Advanced tricks | partial; pattern source, validate semantics and support |
| Color atmosphere and visual effects | `references/local-only/css-creative/Working_With_Colors_Guide-2016.md`; `Color and Atmosphere` | Color design | partial; dated syntax and accessibility treatment |

## Layout and responsiveness

| Topic | Path and verified grep term | Section | Rating |
| --- | --- | --- | --- |
| Grid tracks, areas, and placement | `references/local-only/css-technical/A_Complete_Guide_to_CSS_Grid_Layout-2021.md`; `grid-template-areas` | Grid properties | strong |
| Flex alignment and distribution | `references/local-only/css-technical/A_Complete_Guide_to_CSS_Flexbox-2026.md`; `justify-content` | Flex container properties | strong |
| Intrinsic responsive components | `references/local-only/css-technical/Unleashing_the_Power_of_CSS-2023.md`; `Practical Uses of Container Queries` | Chapter 3 | strong; confirm current style-query support |
| Media and container query strategy | `references/local-only/css-technical/Responsive_Web_Design_with_HTML5_and_CSS-2022.md`; `Media Queries and Container Queries` | Chapter 3 | strong |
| Centering decision cases | `references/local-only/css-technical/Centering_in_CSS_Guide-2014.md`; `Both Horizontally & Vertically` | Two-axis centering | thin; prefer current grid and flexbox |

## Cascade and theming

| Topic | Path and verified grep term | Section | Rating |
| --- | --- | --- | --- |
| Cascade, specificity, and architecture | `references/local-only/css-technical/CSS_in_Depth_Second_Edition-2024.md`; `Cascade, specificity, and inheritance` | Chapter 1 | strong |
| Explicit cascade layer order | `references/local-only/css-technical/Cascade_Layers_Guide-2022.md`; `Establishing a layer order` | Layer ordering | strong |
| Selector and combinator mechanics | `references/local-only/css-technical/CSS_Selectors-2024.md`; `Pseudo-selectors` | General selectors | strong; use current docs for new pseudo-classes |
| Token inheritance and fallbacks | `references/local-only/css-technical/CSS_Custom_Properties_Guide-2021.md`; `Custom property fallbacks` | Fallbacks | strong |
| Dark-theme design and preference flow | `references/local-only/css-technical/Dark_Mode_in_CSS_Guide-2020.md`; `Design Considerations` | Theme design | partial; verify current preference and user-agent behavior |
| Functional sizing and transforms | `references/local-only/css-technical/CSS_Functions_Guide-2020.md`; `Comparison Functions` | `min()`, `max()`, and `clamp()` | partial; verify newer functions and support |

## Color functions and gradients

| Topic | Path and verified grep term | Section | Rating |
| --- | --- | --- | --- |
| Modern perceptual color and mixing | `references/local-only/css-technical/CSS_Color_Functions-2025.md`; `color-mix()` | Color mixing | strong; confirm current syntax and gamut behavior |
| Gradient construction and patterns | `references/local-only/css-technical/CSS_Gradients_Guide-2020.md`; `Conic CSS gradients` | Conic gradients | strong; confirm current interpolation behavior |

## SVG and motion

| Topic | Path and verified grep term | Section | Rating |
| --- | --- | --- | --- |
| CSS-driven SVG interface motion | `references/local-only/css-creative/SVG_Animations-2017.md`; `UI/UX Animations with No External Libraries` | Chapter 5 | strong concept coverage; verify current APIs |
| Responsive SVG insertion | `references/local-only/css-technical/Responsive_Web_Design_with_HTML5_and_CSS-2022.md`; `What you can do with each SVG insertion method` | Chapter 10 | strong |
| SVG fallback planning | `references/local-only/css-technical/SVG_Fallbacks_Guide-2015.md`; `What KIND of fallback do you need?` | Fallback decision | thin; verify which fallbacks remain necessary |
| Anchored overlay fallback | `references/local-only/css-technical/CSS_Anchor_Positioning_Guide-2024.md`; `Setting fallback positions` | Fallback positions | strong concept coverage; verify current support |
| Generated CSS3 and SVG examples | `references/local-only/css-technical/CSS3_and_SVG_with_GPT-4-2024.md`; `SVG and GPT-4` | Chapter 7 | partial; secondary examples only |

## Coverage gaps and fallback

- Treat reduced-motion design, view transitions, scroll-driven animation,
  current browser support, and exact syntax for evolving features as MDN-and-
  specification questions.
- Use current MDN and CSS specifications for platform-specific rendering,
  assistive-technology behavior, then establish target behavior with a rendered
  target-page check.
- Use `ui-ux-engineer` when the question is whether an interaction or flow is
  understandable; use `color-accessibility-expert` to measure and repair
  contrast with its measurement workflow.
