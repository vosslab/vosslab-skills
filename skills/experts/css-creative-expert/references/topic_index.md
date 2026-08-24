# CSS topic index

Choose the narrowest route that explains both the implementation and its visual
proof. Read the linked committed guide first, then use one listed local source
when the gitignored corpus is available. Source types and cautions live in
[local_books.md](local_books.md); verified searches live in
[reference_survey.md](reference_survey.md).

| Problem | Guide and local source | Verification move |
| --- | --- | --- |
| Page looks flat or generic | [task_selection.md](task_selection.md); `references/local-only/css-creative/CSS_MagiC_51_Tricks_to_Take_Your_CSS_Skills_to_the_Next_Level-2023.md` | Compare hierarchy, readability, and one deliberately polished state. |
| Background needs depth, layering, or a resilient image treatment | [task_selection.md](task_selection.md); `references/local-only/css-creative/Background_Magic_CSS_The_Complete_Guide_to_Creating_Stunning_Backgrounds-2023.md` | Compare image-loaded, image-failed, and narrow-screen surfaces. |
| Filter, mask, clip, shadow, or blend effect needs craft | [task_selection.md](task_selection.md); `references/local-only/css-creative/CSS_MagiC_51_Tricks_to_Take_Your_CSS_Skills_to_the_Next_Level-2023.md` | Inspect readability, clipping, and compositing on real content. |
| Palette or color atmosphere lacks intent | [testing_and_oracles.md](testing_and_oracles.md); `references/local-only/css-creative/Working_With_Colors_Guide-2016.md` and `references/local-only/css-technical/CSS_Color_Functions-2025.md` | Compare semantic roles in both schemes; delegate measured contrast repair. |
| Gradient syntax or composition needs precision | [testing_and_oracles.md](testing_and_oracles.md); `references/local-only/css-technical/CSS_Gradients_Guide-2020.md` | Check interpolation, fallback color, banding, and text readability. |
| Regions need two-dimensional alignment or reordering | [project_workflow.md](project_workflow.md); `references/local-only/css-technical/A_Complete_Guide_to_CSS_Grid_Layout-2021.md` | Screenshot intermediate widths and inspect overflow and source order. |
| One-dimensional spacing or control alignment is wrong | [project_workflow.md](project_workflow.md); `references/local-only/css-technical/A_Complete_Guide_to_CSS_Flexbox-2026.md` | Check wrapped, empty, and long-label states. |
| Breakpoints multiply or components need local adaptation | [project_workflow.md](project_workflow.md); `references/local-only/css-technical/Unleashing_the_Power_of_CSS-2023.md` and `references/local-only/css-technical/Responsive_Web_Design_with_HTML5_and_CSS-2022.md` | Screenshot the smallest, middle, and largest widths. |
| Cascade or stylesheet architecture is hard to reason about | [project_workflow.md](project_workflow.md); `references/local-only/css-technical/CSS_in_Depth_Second_Edition-2024.md` and `references/local-only/css-technical/Cascade_Layers_Guide-2022.md` | Inspect layer order, specificity, and the winning computed declaration. |
| Selector change loses or overmatches | [project_workflow.md](project_workflow.md); `references/local-only/css-technical/CSS_Selectors-2024.md` and `references/local-only/css-technical/Unleashing_the_Power_of_CSS-2023.md` | Check match scope and computed value without escalating specificity. |
| Repeated values or themes drift | [project_workflow.md](project_workflow.md); `references/local-only/css-technical/CSS_Custom_Properties_Guide-2021.md` | Inspect inherited token resolution, fallbacks, and each theme boundary. |
| Dark theme looks like an inversion | [project_workflow.md](project_workflow.md); `references/local-only/css-technical/Dark_Mode_in_CSS_Guide-2020.md` | Compare semantic color roles and user preference behavior in both schemes. |
| Fluid sizing or transform/filter function is unclear | [project_workflow.md](project_workflow.md); `references/local-only/css-technical/CSS_Functions_Guide-2020.md` | Inspect computed values at the contract's narrow and wide bounds. |
| Overlay or tooltip needs anchored positioning | [project_workflow.md](project_workflow.md); `references/local-only/css-technical/CSS_Anchor_Positioning_Guide-2024.md` | Verify fallback placement, viewport edges, keyboard order, and support. |
| Centering depends on unknown content size | [project_workflow.md](project_workflow.md); `references/local-only/css-technical/Centering_in_CSS_Guide-2014.md` | Prefer grid or flexbox, then check both axes with short and long content. |
| SVG needs responsive embedding or a fallback | [testing_and_oracles.md](testing_and_oracles.md); `references/local-only/css-technical/Responsive_Web_Design_with_HTML5_and_CSS-2022.md` and `references/local-only/css-technical/SVG_Fallbacks_Guide-2015.md` | Inspect each insertion mode, intrinsic size, fallback, and accessible name. |
| SVG or CSS motion needs choreography | [testing_and_oracles.md](testing_and_oracles.md); `references/local-only/css-creative/SVG_Animations-2017.md` | Record normal and reduced-motion states and inspect transform origin. |
| A secondary generated CSS or SVG example would help exploration | [task_selection.md](task_selection.md); `references/local-only/css-technical/CSS3_and_SVG_with_GPT-4-2024.md` | Rebuild the chosen idea from current primary docs and rendered evidence. |

Use current MDN and CSS specifications whenever a source is thin, dated, or a
browser-support decision controls the design.
