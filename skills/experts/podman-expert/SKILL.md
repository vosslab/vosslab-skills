---
name: podman-expert
description: "Engineer rootless Podman containers, pods, Containerfile/Buildah builds, images, registries, Skopeo, volumes, compose, Quadlet/systemd, networking, podman kube generate, and macOS podman machine. Use for Podman lifecycle or deployment work."
---

# Podman expert

## Overview

Build repeatable, rootless-first container workflows with an explicit runtime,
storage, networking, and operator contract. Own Podman, Buildah, Skopeo,
Containerfiles, compose, pods, Quadlet, and `podman machine` work. Start with
[references/task_selection.md](references/task_selection.md), then use
[references/topic_index.md](references/topic_index.md) to route the symptom.

## Workflow

1. Classify the project shape and state the container contract.
- Inspect the repository for a Containerfile, compose file, Quadlet units,
  systemd integration, image references, ports, health checks, and CI commands.
- Name the service, build context, base image, runtime user, ports, persistent
  paths, secrets source, registry, platform, and the required success signal.
- Follow the existing-project or greenfield branch in
  [references/project_workflow.md](references/project_workflow.md).
2. Select the lifecycle route before changing files.
- Route build, run, compose, service, pod, registry, troubleshooting, or macOS
  machine work through [references/task_selection.md](references/task_selection.md).
- Confirm current CLI flags, Quadlet syntax, and platform behavior in the
  official Podman documentation when versions matter.
3. Build the smallest rootless, reproducible image.
- Use a Containerfile or Buildah recipe with a minimal build context and a
  pinned base-image digest; record the resolved image identity.
- Prefer a non-root runtime user and read-only filesystem. Mount only named,
  explicit writable volumes or bind mounts with documented ownership and labels.
- Read [references/topic_index.md](references/topic_index.md) for focused
  commands and [references/local_books.md](references/local_books.md) when the
  local corpus is available.
4. Run and observe one bounded service path.
- Start with explicit ports, environment sources, network, and volume mounts;
  use `podman inspect` and `podman logs` to verify the actual configuration.
- For macOS, establish the `podman machine` state and host-to-VM mount or port
  boundary before diagnosing the container.
- Use [references/testing_and_oracles.md](references/testing_and_oracles.md)
  for the build-then-run oracle and reproducibility evidence.
5. Choose the durable deployment boundary.
- Keep one-process services simple; use compose for an explicitly coordinated
  local stack, pods for Podman-managed co-location, and Quadlet/systemd for a
  host-managed service lifecycle.
- Pair generated Kubernetes YAML with application and target-cluster validation.
6. Hand off destructive operations explicitly.
- Inspect, build, run, and use ordinary stop operations within the resolved
  service boundary.
- For `podman rm -f`, `podman rmi -f`, `podman kill`, `podman stop -t 0`,
  `podman system prune`, or any volume, network, or image removal or prune,
  give the user the exact resolved command, target, and data-loss effect.
- Resume after the user confirms the resulting state.

## Implementation defaults

- Default to rootless Podman; document every justified rootful exception.
- Default to a read-only root filesystem plus explicit named volumes or bind
  mounts for each writable path; declare every persistence boundary explicitly.
- Pin production image references by digest and record the human-readable tag
  separately for discovery.
- Use registry credentials through the target environment's secret mechanism;
  keep Containerfiles, compose files, images, and command history credential-free.
- Treat Linux SELinux labels, UID mappings, and macOS VM mounts as different
  boundaries, each with its own observable check.
- Consult [references/reference_survey.md](references/reference_survey.md) for
  passage-verified local coverage; use current official documentation when the
  corpus is absent or the topic is thin.

## Quality bar

- Rebuild from a clean context, run the intended entry point, and verify a
  health or functional command through the published port or service boundary.
- Inspect image identity, effective mounts, ports, user, environment sources,
  and logs; report the configuration that actually took effect.
- Keep persistent data and secret handling explicit and recoverable.
- Provide a precise operator handoff for each destructive cleanup request,
  including every resolved `podman rm -f`, `podman rmi -f`, `podman kill`,
  `podman stop -t 0`, system prune, volume prune or removal, network prune or
  removal, and image prune or removal command.

## Output expectations

When using this skill, produce:

- The project shape, selected lifecycle route, rootless or rootful decision,
  image identity, runtime user, writable paths, ports, network, and platform.
- File- and service-specific changes with an explanation of volumes, UID or
  SELinux labeling, and macOS machine boundaries where applicable.
- Executed build, run, inspection, log, health, and clean-rebuild evidence.
- The exact user-run command and consequence when deletion, kill, or prune is
  required, plus a clear next step after the user completes it.
