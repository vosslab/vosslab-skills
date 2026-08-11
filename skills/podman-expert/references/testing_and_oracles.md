# Testing and oracles

Use build-then-run as the primary oracle. Prove the entry point, mounts, ports,
and runtime user after every successful image build.

1. Build from the declared context and record the resulting image digest.
2. Run the intended entry point with explicit ports, network, and named volumes
   or bind mounts; use a temporary, bounded target for development data.
3. Inspect the container to verify image identity, runtime user, mounts, port
   bindings, and restart or health configuration.
4. Read logs and execute the documented health command or make a request through
   the published port. Assert the user-visible service result.
5. Rebuild from a clean build context and repeat the run to prove the declared
   inputs are sufficient and anonymous storage is unnecessary.

Use `podman inspect` and `podman logs` as configuration and failure oracles.
For compose, verify each service and its dependency boundary. For Quadlet,
verify the resulting systemd service in the intended user or system scope. For
macOS, verify machine status and the host-to-VM port and mount boundary.

Treat destructive cleanup as an operator handoff: state the exact resolved
`podman rm -f`, `podman rmi -f`, `podman kill`, `podman stop -t 0`, system prune,
volume or network prune or removal, or image prune or removal command, its
target, and its data-loss consequence for the user to run. Keep this handoff as
one-time implementation evidence; keep permanent tests focused on durable
build, runtime, and service behavior.
