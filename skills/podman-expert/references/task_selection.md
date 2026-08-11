# Task selection

Classify the request before writing a Containerfile or running a command. Name
the target platform, service boundary, persistence requirement, registry, and
desired operator before choosing a route.

| Request | Route | First evidence |
| --- | --- | --- |
| New image or build failure | Containerfile or Buildah | Build context, base digest, build output |
| One service will not start | Run and diagnose | Entry point, logs, inspect, health command |
| Several local services coordinate | Compose | Service graph, ports, networks, named volumes |
| Services share a namespace | Pod | Pod membership, ports, lifecycle owner |
| Host-managed service | Quadlet and systemd | Unit owner, user scope, restart policy |
| Publish, copy, or inspect images | Registry and Skopeo | Fully qualified reference, digest, credentials source |
| Port or mount differs on macOS | `podman machine` | Machine status, VM mount, host port mapping |
| Cluster handoff | Generate Kubernetes YAML | Reviewed manifest and target-cluster contract |

Choose rootless operation first. State why rootful operation is necessary before
using it. Use a read-only root filesystem and explicit writable mounts unless a
documented application requirement says otherwise.

For a request that needs cleanup, first identify the exact container, image,
volume, or network. For `podman rm -f`, `podman rmi -f`, `podman kill`,
`podman stop -t 0`, `podman system prune`, or any volume, network, or image
removal or prune, give the user the exact resolved command, target, and effect.
