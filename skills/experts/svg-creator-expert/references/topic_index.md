# SVG topic index

Use the narrowest row that covers the asset. Local book paths are optional;
current specifications and rendered target evidence remain authoritative.

| Problem | Guide and local source | Verification move |
| --- | --- | --- |
| A user asks for an SVG of an ordinary or manufactured object | [object_illustration.md](object_illustration.md); use the audited Robertson source under `WORKING WITH VOLUME` and Mastering SVG under `viewBox and viewport in SVG` | Render at target and thumbnail sizes; verify recognition, silhouette, projection, line hierarchy, and editable grouping. |
| One object, color family, label, component, or state needs a bounded edit | [targeted_editing.md](targeted_editing.md); use Mastering SVG under `presentation attributes` when paint inheritance needs clarification | Map the rendered target to its owning nodes, then compare matched before/after renders through the real consumer. |
| Canvas scales, crops, or leaves unexpected space | [project_workflow.md](project_workflow.md); `local-only/svg_authoring/Mastering_SVG-2018.md`, search `viewBox and viewport in SVG` | Render the smallest and largest target boxes and inspect edge clipping. |
| A complex contour needs readable path construction | [project_workflow.md](project_workflow.md); `local-only/svg_authoring/Generative_Art_with_JavaScript_and_SVG-2024.md`, search `The All-Powerful Path` | Check path closure, joins, bounds, and control-point continuity. |
| Repeated elements or paint definitions drift | [project_workflow.md](project_workflow.md); `local-only/svg_authoring/Generative_Art_with_JavaScript_and_SVG-2024.md`, search `Grouping and Reusing Elements` | Validate every reference and compare repeated instances after transforms. |
| Existing editor export is hard to maintain | [project_workflow.md](project_workflow.md); `local-only/vector_tools/Adobe_Illustrator_Classroom_in_a_Book_2022_Release-2022.md`, search `Organizing Your Artwork with Layers` | Confirm the cleaned structure still round-trips or meets the chosen source contract. |
| Composition feels crowded or lacks focus | [task_selection.md](task_selection.md); `local-only/drawing_fundamentals/The_Everything_Drawing_Book-2005.md`, search `Thumbnail Sketches and Working Drawings` | Compare several thumbnail/block layouts before detailed rendering. |
| Biological or botanical figure needs accurate simplification | [testing_and_oracles.md](testing_and_oracles.md); `local-only/scientific_illustration/A_Handbook_of_Biological_Illustration-1988.md`, search `OBSERVATION`; and `Botanical_Art_with_Scientific_Illustration-2018.md`, search `Scientific approaches to illustration` | Trace labels and defining features to observations or named references. |
| A biological or medical component may already exist locally | `local-only/LOCAL_SERVIER_SVG_FILE_PATHS.txt`; search a subject term, then inspect the selected SVG | Verify the file exists and confirm license, attribution, ownership, visual fit, and editability before reuse. |
| Publication figure becomes illegible when reduced | [testing_and_oracles.md](testing_and_oracles.md); `local-only/scientific_illustration/Preparing_Scientific_Illustrations_a_Guide_to_Better_Posters_Presentations-1996.md`, search `REDUCTION` | Render at final publication dimensions and inspect labels, strokes, and symbols. |
| Medical figure must represent a specific case or specimen | [testing_and_oracles.md](testing_and_oracles.md); `local-only/scientific_illustration/Medical_Illustration_in_the_Courtroom_Proving_Injury_Causation_and_Damages-2024.md`, search `WHY ARE ACCURACY` | Compare every depicted condition against the supplied case evidence and expert review. |
| Multiview or section drawing is ambiguous | [testing_and_oracles.md](testing_and_oracles.md); `local-only/technical_drawing/Technical_Drawing_with_Engineering_Graphics_Sixteenth_Edition-2023.md`, search `Orthographic Projection` | Cross-check aligned views, shared dimensions, hidden edges, and section conventions. |
| Line styles need clearer technical meaning | [testing_and_oracles.md](testing_and_oracles.md); the engineering graphics source, search `Alphabet of Lines` | Verify each line role and its contrast at final scale. |
| Generative art needs reproducible, bounded output | [testing_and_oracles.md](testing_and_oracles.md); `local-only/svg_authoring/Generative_Art_with_JavaScript_and_SVG-2024.md`, search `Randomness and Regularity` | Repeat the same seed, check bounds and node budget, then compare a different seed. |
| Animation is janky or excludes some users | [testing_and_oracles.md](testing_and_oracles.md); the generative SVG source, search `requestAnimationFrame` | Test keyboard input, paused/static state, reduced motion, and frame behavior. |
| Optimization changes appearance or semantics | [testing_and_oracles.md](testing_and_oracles.md); `local-only/svg_authoring/Mastering_SVG-2018.md`, search `Tools to Optimize Your SVG` | Compare before/after renders and validate IDs, ARIA, CSS hooks, and references. |

Use [reference_survey.md](reference_survey.md) when a second source would
corroborate the decision or when OCR damage makes a passage uncertain.
