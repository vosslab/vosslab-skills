# Reference survey

This survey records what the three `references/local-only/` conversions actually teach. It
is the source of truth for [local_books.md](local_books.md) and the local-source
column in [topic_index.md](topic_index.md). Ratings mean strong for a dedicated
treatment, partial for useful broader coverage, thin for corroboration only,
and not covered for a current-documentation fallback.

## How to use this survey

- Start with the named bare `references/local-only/` path, search the exact grep term, and
  read the surrounding passage before applying it.
- Keep gitignored books out of Markdown links; cite them as bare paths only.
- Use current official Podman documentation for version-sensitive CLI flags,
  Quadlet syntax, registries, and macOS behavior.
- When the corpus is absent or coverage is thin, follow the committed guides,
  first principles, and a build-then-run oracle.

## Rootless architecture and user namespaces

Coverage: strong.

- `references/local-only/Podman_in_Action-2023.md`, `Fully support user namespace`,
  compares user-namespace support and rootless compose behavior.
- `references/local-only/Podman_for_DevOps-2022.md`, `rootless`, develops rootless use in
  the architecture and security discussion.

## Pods and lifecycle

Coverage: partial.

- `references/local-only/Podman_in_Action-2023.md`, `Generating Podman pods and containers
  from Kubernetes YAML`, introduces Podman-managed pods and generated YAML.
- `references/local-only/Podman-2026.md`, `pods`, supplies a short current terminology
  orientation only.

## Containerfile, builds, images, and registries

Coverage: strong for principles; thin for current flags.

- `references/local-only/Podman_for_DevOps-2022.md`, `Meet Buildah - Building Containers
  from Scratch`, is the primary Buildah build source.
- `references/local-only/Podman-2026.md`, `Containerfile`, describes the shareable image
  recipe and OCI image context.
- `references/local-only/Podman_for_DevOps-2022.md`, `Skopeo`, covers the companion image
  inspection and transport tool.
- `references/local-only/Podman-2026.md`, `Container Registries`, describes registry and
  OCI interoperability at a high level.

Use official Podman, Buildah, and Skopeo documentation for exact current flags,
credential behavior, and digest-resolution details.

## Volumes, bind mounts, and SELinux labels

Coverage: partial.

- `references/local-only/Podman_in_Action-2023.md`, `volume`, covers persistent container
  storage and runtime volume concepts.
- `references/local-only/Podman_for_DevOps-2022.md`, `SELinux`, provides security context
  for host and container boundaries.

Use current Podman documentation and inspect output for mount options, UID maps,
and labeling syntax on the installed platform.

## Networking and compose

Coverage: partial.

- `references/local-only/Podman_in_Action-2023.md`, `network`, introduces container
  networking and runtime network tooling.
- `references/local-only/Podman_in_Action-2023.md`, `compose`, documents compose-oriented
  interoperability and rootless use.

Use current documentation for network backend, DNS, port-forwarding, and compose
compatibility choices.

## Systemd and Quadlet integration

Coverage: partial for systemd; thin for current Quadlet syntax.

- `references/local-only/Podman_in_Action-2023.md`, `systemd`, covers systemd integration
  and service-oriented Podman architecture.

Use official Quadlet and systemd documentation for current unit keys, user scope,
and generated-service behavior.

## Kubernetes YAML generation

Coverage: partial.

- `references/local-only/Podman_for_DevOps-2022.md`, `Kubernetes`, provides Kubernetes
  integration context for Podman workflows.

Use the current `podman kube generate` documentation and cluster policy for
current manifest options. Keep the older `podman generate kube` wording only as
historical source terminology; validate the application separately from generated YAML.

## macOS podman machine

Coverage: not covered.

The books are Linux-centric. Use official Podman macOS documentation to inspect
`podman machine` state, VM-backed mounts, and host-to-VM network boundaries.
