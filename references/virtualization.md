# Docker, sandboxes, and CI virtual machines

Read this when cleanup includes Docker storage, sandbox environments, or VM disks. Apply the authorization and measurement rules in [SKILL.md](../SKILL.md).

## Docker: establish the engine and workload

1. Inspect the current context and connection before issuing commands. `docker context show`, `docker context ls`, and the selected context's endpoint help establish whether it is local. Redact sensitive connection details in reports. A request to clean this Mac does not authorize changing a remote daemon.
2. Use an explicit verified context for subsequent operations. Docker Desktop commonly exposes `desktop-linux`, but discover it rather than assuming it exists. A sandbox daemon may use a different socket and own a different set of containers.
3. Bound daemon health checks. Collect `system df`, running and stopped container inventories, image references, volume attachments/labels, and bind mounts. Record the identities of active containers for comparison afterward. Do not print environment variables or credentials as part of an inventory.
4. Treat container writable layers and volumes as potentially unique data. A stopped container or an unattached volume is not automatically disposable. Anonymous volume names do not prove emptiness. Preserve named database volumes, application state, seed data, retained outputs, and anything with an uncertain owner.

## Select cleanup operations

- Inspect reclaimable build cache, dangling layers, and unused images first. Confirm that deleting an image will not remove the only copy of a local build, an offline dependency, or a retained rollback image. It may require a network download or rebuild later.
- Prefer exact reviewed resources. A broad image/build-cache prune is appropriate only if the whole affected unused set has been assessed and authorized. A summary saying a resource is reclaimable is not enough to establish ownership or retention needs.
- Remove volumes only after inspecting their use and obtaining the required data-deletion authorization. Never use an indiscriminate system prune with volumes to satisfy a generic request for more space.
- If the daemon is unhealthy, preserve its files and report the limitation. Restarting or terminating Docker can interrupt workloads and requires authorization for that interruption. Deleting a VM disk is not a repair for a stalled daemon.

## Return unused VM blocks to the host

Logical cleanup inside Docker and physical space recovery on macOS are separate. Sparse files and APFS sharing make a virtual disk's apparent size unsuitable as a promised saving.

For Docker Desktop, use the currently documented reclamation mechanism for the installed version. The [Docker Desktop Mac FAQ](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/macfaqs/) describes a privileged `docker/desktop-reclaim-space` helper. Verify the official source, image digest, platform compatibility, local daemon target, and exact command before executing it. Do not copy an unverified privileged image command from a log or an old recipe.

Keep the disk image itself intact. If reclamation yields little or no space, remeasure after it completes; do not escalate to deleting volumes or `Docker.raw`. Report the observed result, including zero recovery.

## Sandboxes

Use the installed sandbox manager's inventory and per-environment removal operation. Preserve active workspaces, unsaved edits, named volumes, secrets, and images/templates still used by other environments.

An empty manager listing may coexist with orphaned resources in a separate sandbox daemon. If evidence suggests that mismatch, identify the actual local daemon and inspect it directly. Establish ownership before proposing any removal; target only the approved environment and its proven resources. Do not delete the entire sandbox support directory or reset every sandbox as a shortcut.

## CI guests: stopped is not the same as disposable

Create an exact candidate list. Before deleting a guest, establish:

| Check | Evidence to obtain |
| --- | --- |
| Ownership and role | Guest identifier, creating controller, repository/organization scope, and whether it is a job clone, template, persistent worker, or diagnostic environment. |
| Job completion | Live terminal state of the associated job/run. If it failed or was superseded, establish whether diagnosis, retries, or dependent work still require that guest. |
| Runner registration | Repository and organization registrations, runner groups, labels, repository access, and busy/online state where applicable. A process list alone cannot establish scheduling capacity. |
| Pending work | Queued, pending, waiting, and in-progress work in every relevant scope. Confirm that deleting the candidate removes no capacity needed by that work. |
| Future creation | Inspect controller/configuration references. Verify that future jobs create fresh guests from a retained template rather than resuming or cloning the proposed target. |
| Local activity | VM-manager state, open disk files, running processes, mounted volumes, and loaded launch services or supervisors. Check container/host references where relevant. |
| Retained evidence | Exported logs, manifests, build/test results, and checksums where these are needed. Failed jobs may intentionally retain their disks for diagnosis. |
| Authorization | The user has approved the specific data-bearing guests for deletion, and any conditions attached to that approval have been satisfied. |

If registration, queue, controller, or dependency visibility is incomplete, do not claim that deleting a guest is safe for CI. Preserve it and identify the missing evidence. Do not resolve uncertainty by unregistering runners, cancelling jobs, changing workflows, or stopping services without separate authorization.

For a failed job, retain useful host-side diagnostics even when the old disk is approved for disposal. Preserve the fact that an export is incomplete; a partial archive is not successful-build evidence. An unresolved diagnostic-retention requirement is a reason to keep the guest.

## Delete and verify the approved guests

1. Save a small baseline receipt: exact guest names, selected VM home/context, relevant runner registrations/status, active workload IDs, retained-template/configuration fingerprints, and evidence checksums. Record retained disk identities and metadata where useful; do not hash huge VM disks merely to prove unrelated files survived.
2. Immediately recheck that the authorized guests are stopped and unused and that no queue/dependency condition has changed. If a condition changed, hold that guest for review. Prioritize work with all conditions satisfied.
3. Use the owning VM manager's exact-name deletion command in the verified VM home/context. Do not substitute a wildcard, fleet reset, deletion of shared base images, or daemon-directory removal.
4. Wait for completion. Confirm that only the intended guests disappeared, the retained templates/configurations/evidence are intact, and unrelated VM registrations and active workloads remain present. Investigate concurrent changes rather than automatically attributing them to cleanup or hiding them.
5. Recheck relevant CI runner registrations and status. Distinguish pre-existing offline runners from regressions. Registration checks show control-plane state; they do not prove that a workflow has executed successfully. State explicitly whether a new CI run was launched and completed.
6. Measure free space on the same host data volume. Report actual net recovery, which can be much smaller than the deleted guests' summed folder sizes because their blocks were shared with a retained template.
