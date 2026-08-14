# Topic index

Use this table to map an observed symptom to the owning route. Confirm current
Podman behavior in official documentation before relying on version-sensitive
flags, Quadlet syntax, or platform details.

| Symptom or task | First route | Primary evidence | Local source |
| --- | --- | --- | --- |
| Permission denied on bind mount | UID, label, mount boundary | `podman inspect`, host ownership, label | `references/local-only/Podman_for_DevOps-2022.md`, `rootless` |
| UID mapping surprise | Rootless user namespace | `podman unshare`, inspect, runtime user | `references/local-only/Podman_in_Action-2023.md`, `user namespace` |
| Container starts then exits | Runtime diagnosis | logs, entry point, exit status | `references/local-only/Podman_for_DevOps-2022.md`, `troubleshooting` |
| Image pull or push fails | Registry and Skopeo | image reference, digest, auth source | `references/local-only/Podman_for_DevOps-2022.md`, `Skopeo` |
| Port is unreachable | Network and platform boundary | inspect port bindings, host request | `references/local-only/Podman_in_Action-2023.md`, `network` |
| macOS mount or port differs | Podman machine | machine state, VM mount, host mapping | official Podman macOS documentation |
| Multi-service local stack | Compose | service graph, named volumes, health order | `references/local-only/Podman_in_Action-2023.md`, `compose` |
| Boot or restart lifecycle | Quadlet and systemd | unit scope, generated service, logs | `references/local-only/Podman_in_Action-2023.md`, `systemd` |
| Pod or Kubernetes handoff | Pod and generated YAML | pod membership, reviewed manifest | `references/local-only/Podman_in_Action-2023.md`, `Generating Podman pods` |

Read [project_workflow.md](project_workflow.md) before editing an existing
project. Read [testing_and_oracles.md](testing_and_oracles.md) before declaring
a build or deployment complete. Use [reference_survey.md](reference_survey.md)
to distinguish supported book guidance from current-documentation territory.
