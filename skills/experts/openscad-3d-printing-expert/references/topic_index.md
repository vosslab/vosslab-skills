# OpenSCAD topic index

## Practical guides

- Writing or reviewing source: [code_best_practices.md](code_best_practices.md).
- Assemblies, part APIs, section views, text, and external generators:
  [extended_modeling.md](extended_modeling.md).
- Fits, orientation, walls, and artwork: [print_design.md](print_design.md).
- Lessons from historical models: [model_patterns.md](model_patterns.md).
- Book lookup: [local_books.md](local_books.md); passage-level evidence and source limitations:
  [reference_survey.md](reference_survey.md).
- Project setup: [project_workflow.md](project_workflow.md); completion checks:
  [testing_and_oracles.md](testing_and_oracles.md).

## Topic routing

| Topic | Read next | Main checks |
| --- | --- | --- |
| Parameters, variables, modules, scope | [code_best_practices.md](code_best_practices.md) | Compile-time variable binding, explicit module arguments, stable parameter defaults |
| CSG and Boolean modeling | Official language reference, Boolean operations | Child order, cutter overlap, no face/edge-only joins, exact render |
| Tessellation and curved detail | Official language reference, `$fa`, `$fs`, `$fn` | Facet quality at actual scale; practical render time |
| FDM/FFF wall thickness and feature size | Prusa modeling guide; local technical drawing reference | Nozzle/perimeter compatibility and printed validation; no universal minimum |
| Fits, clearances, holes, clips | Prusa modeling guide; local technical drawing reference | Process-specific tolerance, orientation, shrinkage, coupon or measured fit |
| Overhangs, bridging, supports, orientation | Prusa modeling guide | Printer-specific support limit, bridge span and finish, split/reorient options |
| Mesh validity and STL/3MF export | OpenSCAD STL export and command-line docs; computational geometry reference | Exact render succeeds, mesh is manifold, slicer accepts and orients the part |
| Geometry regression or parameter sweep | [testing_and_oracles.md](testing_and_oracles.md) | Reproducible parameter values, bounds, mesh checks, regression on intended interfaces |

## Primary online sources

- [OpenSCAD documentation](https://openscad.org/documentation.html): official user manual and language reference.
- [OpenSCAD language reference](https://files.openscad.org/documentation/manual/The_OpenSCAD_Language.html): modules, variables, transformations, Boolean operations, tessellation, and syntax.
- [OpenSCAD command-line documentation](https://files.openscad.org/documentation/manual/Using_OpenSCAD_in_a_command_line_environment.html): batch rendering and export options; verify flags against the installed version.
- [OpenSCAD STL export](https://files.openscad.org/documentation/manual/STL_Export.html): mesh export and manifold requirements.
- [OpenSCAD FAQ](https://files.openscad.org/documentation/manual/FAQ.html): preview artifacts, overlapping Boolean cutters, and mesh troubleshooting.
- [Prusa: Modeling with 3D printing in mind](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135): process-dependent overhangs, walls, part splits, tolerances, and manifold models.
- [Prusa: Layers and perimeters](https://help.prusa3d.com/article/layers-and-perimeters_1748): slicer behavior for thin walls and shells.

## Local book evidence

Use [local_books.md](local_books.md) to locate books and
[reference_survey.md](reference_survey.md) for inspected headings, lines, and cautions.

- Code organization and iterative modeling: *Programming with OpenSCAD*, *OpenSCAD Cookbook*,
  and *Simplifying 3D Printing with OpenSCAD*.
- Debugging, sections, and hollow parts: *Creating 3D Models for 3D Printing Using OpenSCAD*.
- Historical libraries and hull patterns: *OpenSCAD for 3D Printing* and *OpenSCAD Basics Tutorial*;
  verify current semantics and minimum wall thickness rather than copying old listings.
- External generation and sampled geometry: *Python for 3D Printing*; audit wrapper semantics.
- Fit, orientation, loads, and process constraints: the additive-manufacturing guide,
  *3D Printing For Dummies*, the failure reference, and the technical drawing book.
- Mesh topology: the computational geometry handbook.
- Mathematical examples: *Learning Mathematics in the Context of 3D Printing*.
- Machine operations and application/industry narratives: background only, with scope limits
  recorded in the survey rather than promoted to language or safety rules.

Prefer current official docs for language/API details, and printer/slicer documentation for numeric print limits. Treat numeric ranges from one machine as machine-specific.