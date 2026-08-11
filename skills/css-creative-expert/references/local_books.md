# Local CSS books

Use this source map with [reference_survey.md](reference_survey.md). The 21
files are local, gitignored conversions; use the bare paths to search a named
term and read its surrounding passage. When the corpus is absent, use the
committed guides, MDN, the CSS specifications, and rendered evidence.

## Comprehensive foundations

1. `references/local-only/CSS_The_Definitive_Guide-2023.md` is the broad
   language reference for cascade, selectors, backgrounds, layout, and motion.
2. `references/local-only/CSS_in_Depth_Second_Edition-2024.md` is the modern
   design and architecture companion for responsive layout, components, and
   newer CSS features.

## Modern technique collections

3. `references/local-only/Modern_CSS-2020.md` supplies modern layout and
   effect patterns; corroborate version-sensitive claims.
4. `references/local-only/Unleashing_the_Power_of_CSS-2023.md` is a broad
   practical collection for modern CSS patterns.
5. `references/local-only/CSS_MagiC_51_Tricks_to_Take_Your_CSS_Skills_to_the_Next_Level-2023.md`
   supplies focused visual and interaction techniques.
6. `references/local-only/Responsive_Web_Design_with_HTML5_and_CSS-2022.md`
   is the responsive and container-query companion.
7. `references/local-only/Background_Magic_CSS_The_Complete_Guide_to_Creating_Stunning_Backgrounds-2023.md`
   is the visual-surface source for backgrounds, blending, and effects.

## Layout and cascade lookups

8. `references/local-only/A_Complete_Guide_to_CSS_Grid_Layout-2021.md` is the
   grid lookup for tracks, areas, placement, and alignment.
9. `references/local-only/A_Complete_Guide_to_CSS_Flexbox-2026.md` is the
   flexbox lookup for alignment, wrapping, ordering, and sizing.
10. `references/local-only/CSS_Anchor_Positioning_Guide-2024.md` is the
    anchored-overlay lookup; verify current browser support.
11. `references/local-only/CSS_Selectors-2024.md` is the selector lookup;
    confirm support for newer pseudo-classes in current documentation.
12. `references/local-only/Cascade_Layers_Guide-2022.md` is the layer-order
    lookup for making precedence explicit.
13. `references/local-only/CSS_Custom_Properties_Guide-2021.md` is the token,
    inheritance, and fallback lookup.
14. `references/local-only/Centering_in_CSS_Guide-2014.md` is a dated teaching
    lookup for centering patterns; prefer current layout primitives and MDN.

## Color and visual-media lookups

15. `references/local-only/CSS_Color_Functions-2025.md` is the current color
    function and interpolation lookup; use measured repairs from
    `color-accessibility-expert` when contrast is in scope.
16. `references/local-only/CSS_Gradients_Guide-2020.md` is the gradient syntax
    and composition lookup.
17. `references/local-only/CSS_Functions_Guide-2020.md` is a general function
    lookup; verify recently added functions in specifications.
18. `references/local-only/Dark_Mode_in_CSS_Guide-2020.md` is a dark-scheme
    introduction; design semantic roles and verify current behavior.
19. `references/local-only/SVG_Properties_in_CSS_Guide-2019.md` is the SVG-CSS
    property lookup.
20. `references/local-only/SVG_Fallbacks_Guide-2015.md` is a dated fallback
    lookup; use current browser and asset guidance before shipping.
21. `references/local-only/Working_With_Colors_Guide-2016.md` is a dated color
    teaching lookup; use current color specifications for syntax and gamut.

## Source boundary

- Start with one focused lookup or one comprehensive source, then add a second
  source only when corroboration improves the decision.
- Treat local prose as conceptual guidance; use MDN and CSS specifications for
  current syntax, browser support, and evolving features.
- Keep the local corpus optional so every target project works from committed
  guides and current primary documentation.
