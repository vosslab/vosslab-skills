# CSS topic index

Choose the narrowest route that explains both the implementation and its visual
proof. Read the linked guide first, then use the listed local source only when
it is available.

| Problem | Guide and local source | Verification move |
| --- | --- | --- |
| Regions need fluid alignment or reordering | [project_workflow.md](project_workflow.md); `references/local-only/A_Complete_Guide_to_CSS_Grid_Layout-2021.md` | Screenshot intermediate widths and inspect overflow. |
| One-dimensional spacing or control alignment is wrong | [project_workflow.md](project_workflow.md); `references/local-only/A_Complete_Guide_to_CSS_Flexbox-2026.md` | Check wrapped, empty, and long-label states. |
| A selector change loses to legacy CSS | [project_workflow.md](project_workflow.md); `references/local-only/CSS_Selectors-2024.md` and `references/local-only/Cascade_Layers_Guide-2022.md` | Inspect cascade and computed value while keeping specificity stable. |
| Repeated values or themes drift | [project_workflow.md](project_workflow.md); `references/local-only/CSS_Custom_Properties_Guide-2021.md` | Inspect inherited token resolution in each theme. |
| Palette, gradients, or color interpolation needs design | [testing_and_oracles.md](testing_and_oracles.md); `references/local-only/CSS_Color_Functions-2025.md` and `references/local-only/CSS_Gradients_Guide-2020.md` | Screenshot both schemes; send measured contrast repair to `color-accessibility-expert`. |
| Surface depth, image, blend, or filter effect is weak | [task_selection.md](task_selection.md); `references/local-only/Background_Magic_CSS_The_Complete_Guide_to_Creating_Stunning_Backgrounds-2023.md` | Compare image-loaded and fallback surfaces. |
| Dark theme looks like an inversion | [project_workflow.md](project_workflow.md); `references/local-only/Dark_Mode_in_CSS_Guide-2020.md` | Compare semantic color roles in both schemes. |
| Breakpoints multiply or components need local adaptation | [project_workflow.md](project_workflow.md); `references/local-only/Responsive_Web_Design_with_HTML5_and_CSS-2022.md` and `references/local-only/CSS_in_Depth_Second_Edition-2024.md` | Screenshot the smallest, middle, and largest widths. |
| Decorative SVG needs CSS control or fallback | [testing_and_oracles.md](testing_and_oracles.md); `references/local-only/SVG_Properties_in_CSS_Guide-2019.md` | Inspect rendered SVG and fallback asset behavior. |
| Overlay or tooltip needs anchored positioning | [project_workflow.md](project_workflow.md); `references/local-only/CSS_Anchor_Positioning_Guide-2024.md` | Verify feature fallback and viewport-edge behavior. |
| Animation needs purpose or restraint | [testing_and_oracles.md](testing_and_oracles.md); `references/local-only/CSS_The_Definitive_Guide-2023.md` | Record normal and reduced-motion states. |

Use current MDN and CSS specifications whenever a source is thin, dated, or a
browser-support decision controls the design.
