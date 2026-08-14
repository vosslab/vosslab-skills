# Project workflow

Use this guide on the target project, not while authoring this skill.

## No container files yet

1. Identify the executable, supported runtime, listening port, health command,
   writable paths, configuration sources, and external dependencies.
2. Create the smallest Containerfile with a pinned base-image digest, a
   non-root runtime user, a read-only filesystem, and explicit writable mounts.
3. Build, run, inspect, and exercise one health or functional command through
   the exposed service boundary.
4. Add compose, a pod, Quadlet, or generated Kubernetes YAML only when its
   lifecycle owner is explicit.

## Containerfile or compose file already exists

1. Inventory the build context, base image and digest, stages, entry point,
   runtime user, exposed ports, environment and secret sources, networks, and
   named volumes or bind mounts before changing anything.
2. Preserve the existing lifecycle boundary unless the requested behavior
   requires a migration. Keep compose coordination separate from systemd or
   Quadlet host ownership.
3. Rebuild from the declared context, run the intended service path, and compare
   `podman inspect` output with the declared mounts, ports, user, and image.
4. For macOS, check `podman machine` before interpreting host mount or network
   behavior. For Linux, check UID mappings and SELinux labels when mounts fail.

For a requested deletion, forced removal, kill, or prune, identify the exact
target and provide the user-run `podman rm -f`, `podman rmi -f`, `podman kill`,
`podman stop -t 0`, system prune, volume or network prune or removal, or image
prune or removal command that applies. State the data-loss consequence.
