# Local books

Use this source map to choose among the three Markdown conversions in
`references/local-only/` relative to this skill root. The books are gitignored and may be
absent. Search each named bare path with `rg`, read the surrounding passage, and
use [reference_survey.md](reference_survey.md) for verified coverage.

1. `references/local-only/Podman_in_Action-2023.md` is the primary practical source for
   Podman architecture, rootless operation, containers, pods, networking,
   volumes, compose, systemd, and day-to-day lifecycle. Search `rootless`,
   `pod`, `network`, `volume`, or `systemd`.
2. `references/local-only/Podman_for_DevOps-2022.md` is the primary engineering source for
   Podman internals, Buildah, Skopeo, image workflow, security, troubleshooting,
   and Kubernetes integration. Search `Buildah`, `Skopeo`, `troubleshooting`,
   `SELinux`, or `Kubernetes`.
3. `references/local-only/Podman-2026.md` is a short recency note for current terminology,
   OCI images, Containerfiles, registries, and lifecycle orientation. Treat it
   as thin corroboration, not the primary source for current CLI flags or
   service syntax. Search `Containerfile`, `Container Registries`, or `pods`.

When a book is absent, a term is thin, or current CLI, Quadlet, registry, or
macOS behavior is in question, use official Podman documentation and an
executed build-then-run oracle instead.
