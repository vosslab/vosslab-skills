# CSS reference survey

This survey records verified grep routes for the local CSS corpus. Ratings mean
**strong** for a dedicated treatment, **partial** for a useful section in a
broader source, **thin** for a mention or dated treatment, and **not covered**
for a topic that must use current primary documentation.

## How to use this survey

- Search the listed term in the named bare path and read the surrounding passage
  before applying it; establish the implementation with the passage and target
  evidence.
- Prefer strong coverage, use partial or thin sources as corroboration, and
  check MDN and CSS specifications for browser support and evolving syntax.
- With `references/local-only/` unavailable, continue through the committed
  guides, semantic CSS reasoning, rendered screenshots, computed styles, and
  current primary documentation.
- Delegate measured contrast audits and palette repair to
  `color-accessibility-expert`; retain accessible color-role design here.

## Layout systems

| Topic | Path and verified grep term | Section | Rating |
| --- | --- | --- | --- |
| Grid tracks, areas, and placement | `references/local-only/A_Complete_Guide_to_CSS_Grid_Layout-2021.md`; `grid-template-areas` | Grid properties | strong |
| Flex alignment and distribution | `references/local-only/A_Complete_Guide_to_CSS_Flexbox-2026.md`; `justify-content` | Flexbox alignment | strong |
| Centering patterns | `references/local-only/Centering_in_CSS_Guide-2014.md`; `transform: translate` | Transform centering | thin; dated 2014, prefer grid/flex and MDN |
| Responsive and container strategy | `references/local-only/Responsive_Web_Design_with_HTML5_and_CSS-2022.md`; `Media Queries and Container Queries` | Responsive chapters | strong |

## Selectors and cascade layers

| Topic | Path and verified grep term | Section | Rating |
| --- | --- | --- | --- |
| Layered cascade control | `references/local-only/Cascade_Layers_Guide-2022.md`; `@layer reset` | Layer declaration | strong |
| Relational selectors | `references/local-only/CSS_Selectors-2024.md`; `:has(` | Pseudo-class examples | partial; verify support in MDN |
| Broad cascade and animation context | `references/local-only/CSS_The_Definitive_Guide-2023.md`; `@keyframes` | Animation chapter | strong |

## Custom properties and theming

| Topic | Path and verified grep term | Section | Rating |
| --- | --- | --- | --- |
| Token inheritance and fallbacks | `references/local-only/CSS_Custom_Properties_Guide-2021.md`; `var(--spacing)` | Custom-property examples | strong |
| Dark-scheme preference | `references/local-only/Dark_Mode_in_CSS_Guide-2020.md`; `prefers-color-scheme` | System scheme detection | partial; verify current behavior |
| Component-local responsive design | `references/local-only/CSS_in_Depth_Second_Edition-2024.md`; `Container queries` | Chapter 10 | strong |

## Color functions and gradients

| Topic | Path and verified grep term | Section | Rating |
| --- | --- | --- | --- |
| Modern perceptual color functions | `references/local-only/CSS_Color_Functions-2025.md`; `oklch()` | Oklab and Oklch | strong |
| Gradient construction | `references/local-only/CSS_Gradients_Guide-2020.md`; `linear-gradient` | Linear gradients | strong |
| Legacy web-color background | `references/local-only/Working_With_Colors_Guide-2016.md`; `Working With Colors` | Title and introduction | thin; dated 2016, use current Color specifications |

## Backgrounds and visual effects

| Topic | Path and verified grep term | Section | Rating |
| --- | --- | --- | --- |
| Image blending and layered surfaces | `references/local-only/Background_Magic_CSS_The_Complete_Guide_to_Creating_Stunning_Backgrounds-2023.md`; `Image blending` | Image blending | strong |
| Current effects landscape | `references/local-only/CSS_MagiC_51_Tricks_to_Take_Your_CSS_Skills_to_the_Next_Level-2023.md`; `blend modes` | Modern CSS effects | partial |

## SVG in CSS

| Topic | Path and verified grep term | Section | Rating |
| --- | --- | --- | --- |
| CSS properties applied to SVG | `references/local-only/SVG_Properties_in_CSS_Guide-2019.md`; `SVG Properties in CSS Guide` | Title and source route | partial; confirm property behavior in MDN |
| SVG fallback planning | `references/local-only/SVG_Fallbacks_Guide-2015.md`; `SVG Fallbacks Guide` | Title and source route | thin; dated 2015, use current browser guidance |

## Animation and positioning

| Topic | Path and verified grep term | Section | Rating |
| --- | --- | --- | --- |
| Named keyframe animation | `references/local-only/CSS_The_Definitive_Guide-2023.md`; `@keyframes` | Animation chapter | strong |
| Anchored overlays | `references/local-only/CSS_Anchor_Positioning_Guide-2024.md`; `anchor-name` | Anchor declaration | partial; verify current support and fallback |

## Coverage gaps and fallback

- Treat current browser support, shipping status, and exact syntax for anchor
  positioning, `:has()`, container queries, and modern color as MDN-and-
  specification questions.
- Use current MDN and CSS specifications for platform-specific rendering,
  assistive-technology behavior, then establish target behavior with a rendered
  target-page check.
- Use `ui-ux-engineer` when the question is whether an interaction or flow is
  understandable; use `color-accessibility-expert` to measure and repair
  contrast with its measurement workflow.
