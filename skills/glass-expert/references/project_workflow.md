# Project workflow

Use this reference when the skill is invoked on a target SwiftUI app, not
while building glass-expert itself. The target may be a new app (greenfield)
or an existing repo to improve. Detect which case applies, then follow the
matching workflow.

## Detect project state

Inspect the target repo before writing glass code:

- Search for glass usage: `grep -rn 'glassEffect\|GlassEffectContainer\|glassEffectID' Sources/ src/ 2>/dev/null`.
- Check the deployment target (Package.swift `platforms` or the Xcode
  project): custom glass needs the macOS 26+ SDK.
- Check Info.plist for the `UIDesignRequiresCompatibility` opt-out; when
  present and true, the app renders the legacy design and no glass appears.
- Search for accessibility handling:
  `grep -rn 'accessibilityReduceTransparency\|colorSchemeContrast' Sources/ src/ 2>/dev/null`.

If glass usage exists, follow the existing-repo workflow. If the target is a
fresh scaffold or has no glass yet, follow the greenfield workflow.

## Glass contract

Both workflows maintain a glass contract. Use the target repo's docs location
when present; otherwise create `docs/GLASS_SURFACES.md` in the target. One row
per glass surface:

| Surface | Layer role | Backdrop | Contrast strategy | Evidence file |
| --- | --- | --- | --- | --- |

- Layer role: control, navigation, or transient (per
  [design_placement.md](design_placement.md)); system chrome rows say
  "standard API" and get no custom glass.
- Backdrop: app-controlled or user-controlled; user-controlled forces the
  layered contrast strategy in
  [color_and_contrast.md](color_and_contrast.md).
- Evidence file: the labeled capture set proving the surface, per
  [testing_and_oracles.md](testing_and_oracles.md).

## Greenfield workflow

1. Placement first: decide which surfaces are glass at all using
   [design_placement.md](design_placement.md); standard components cover most
   of the app.
2. Write the glass contract before implementing custom surfaces.
3. Copy the seeds from [component_seeds.md](component_seeds.md):
   `GlassSurface` for text-bearing surfaces, `GlassEvidenceView` as the
   verification harness. Wire the harness into a debug build target early so
   evidence capture is cheap from day one.
4. Implement each surface with a clear sampling path
   ([layers_and_sampling.md](layers_and_sampling.md)).
5. Validate every surface with the evidence protocol; attach capture files to
   the contract rows.

## Existing-repo workflow

1. Inspect first, before any edit: inventory every `glassEffect` call site,
   its layer role, and its backdrop; record the deployment target and
   accessibility handling found above.
2. Audit each surface against the sampling-path rules (opaque backgrounds,
   glass on glass, empty backdrops) and the contrast rules (hardcoded colors,
   missing accessibility fallbacks). Record each defect with file and line.
3. Capture baseline evidence for the surfaces being changed, so before/after
   comparison is possible.
4. Fix one surface at a time; prefer replacing ad-hoc glass code with the
   `GlassSurface` seed where the surface carries text.
5. Prove improvement with the evidence protocol per surface; update the glass
   contract rows with the new capture files.
