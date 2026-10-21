# Select the OpenSCAD task path

## Route by outcome

- **New model or major redesign:** establish dimensions, coordinate frame, interfaces, print orientation, and the target process before writing geometry. Read [project_workflow.md](project_workflow.md) and [topic_index.md](topic_index.md).
- **Feature or refactor in an existing model:** map the module tree and parameter flow, retain existing public parameters, and make one scoped change. Read [project_workflow.md](project_workflow.md) and [code_best_practices.md](code_best_practices.md).
- **Broken Boolean, missing surface, or failed STL export:** reproduce with the smallest source case, inspect exact render output, then check coplanar/tangent faces, disconnected shells, degeneracy, and units. Read [topic_index.md](topic_index.md) and [testing_and_oracles.md](testing_and_oracles.md).
- **Mating parts, holes, clips, or tolerance-sensitive features:** obtain printer, material, nozzle, orientation, and slicer settings. If any are unknown, state assumptions and produce a small fit coupon rather than asserting a universal clearance.
- **Unknown intended task:** ask for the desired part, dimensions, critical interfaces, print process, and whether the user expects source, exported mesh, or both. Continue with explicit assumptions only when safe and useful.
- **Review only:** report concrete source or printability issues with location and a correction; distinguish a geometry defect from a printer-specific risk.

## Define the acceptance target

Before editing, record only constraints relevant to this model:

- Overall dimensions and allowed envelope.
- Datum/origin and the direction of critical axes.
- Mating dimensions, fit type, and required motion or retention.
- Load direction or functional strength requirement.
- Print process, printer/build volume, nozzle, material, slicer, and likely orientation.
- Required deliverables: `.scad`, STL/3MF, parameter variants, or a test print/coupon.

Do not replace missing constraints with precise-looking defaults. Mark unknowns and choose measurements or coupons that can resolve them.