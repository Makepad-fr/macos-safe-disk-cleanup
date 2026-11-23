# Security and contribution policy

This package contains cleanup instructions, not an unattended deletion service.
Report vulnerabilities privately through GitHub private vulnerability reporting;
please do not post credentials or private workstation evidence in public issues.

## Protected changes

The main branch requires a pull request, one independent approval, resolved review
threads, an up-to-date passing `package` check from GitHub Actions, verified commit
signatures, and linear history. New commits dismiss stale approvals. Force pushes
and branch deletion are blocked; the ruleset has no bypass actors. CODEOWNERS
covers the package and its CI configuration.

Repository Actions defaults to a read-only token and cannot approve pull requests.
Every external contributor requires workflow approval. Actions must use full
commit SHAs; the allowlist currently contains only the reviewed checkout action.
This approval limits who can start jobs; it does not make submitted code trusted.
Never add repository or organization-wide deployment credentials to this public
repository. Keep any future publishing credentials behind a separate reviewed
release boundary.

CI validates the package format and whitespace. It never performs disk cleanup.
Installation reads the public repository directly; there is no deployment secret
or automatic publishing job. A successful validation does not establish that
every cleanup operation is safe on every device.

## Self-hosted execution boundary

All CI jobs request the `macos-skill-isolated` organization group, which permits
only this public repository. No persistent build or release runner belongs to
that group. Each job receives a fresh Linux VM and single-job JIT registration;
registration credentials stay on the controller. The VM is destroyed afterward.
There is no hosted fallback and no job-level skip that makes missing capacity
look successful.

Guest networking is restricted by the hypervisor to a host-controlled HTTPS
proxy. The proxy allows GitHub and Python package endpoints, resolves and checks
numeric destinations before connecting, and denies private, link-local, reserved,
and configured production addresses. No host folders, Docker socket, SSH agent,
signing identities, or deployment credentials are shared. CPU, memory, disk growth,
and VM lifetime are bounded outside guest control. The host deletes the guest
overlay after normal completion, cancellation, or the hard lifetime deadline.

These controls require a separately maintained controller and virtualization host;
workflow labels alone do not provide isolation. The operator must verify fresh
credentials, blocked network routes, absent host mounts, real job execution, and
teardown. Keep the hypervisor and base image patched. Even with these controls,
self-hosting public contributor code retains hypervisor and supply-chain risk;
no configuration can guarantee zero vulnerabilities.
