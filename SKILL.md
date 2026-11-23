---
name: macos-safe-disk-cleanup
description: Audit and reclaim macOS disk space from stale caches, generated build files, and unused simulator data while preserving active work. Use when asked to free storage, investigate large folders, or clean a Mac development machine.
license: MIT
---

# macOS Safe Disk Cleanup

Recover useful space without interrupting current work or treating retained data as disposable. This is a cleanup procedure, not permission to erase everything that is large or old.

## Establish scope and measure

- Distinguish a read-only audit from a request to perform cleanup. Honor specific exclusions and authorization already given in the conversation. Do not repeatedly ask for permission to remove the same approved disposable files.
- Preserve personal documents, photos, source trees, credentials, databases, backups, release archives and symbols, security findings, test evidence, and explicitly retained files unless their deletion is specifically authorized.
- Resolve the actual home directory and selected paths. Do not assume a username, repository layout, Docker context, or installed developer tool. Do not follow symlinks outside the approved scope.
- Capture data-volume free space before cleanup. On current macOS installations, use `df -k /System/Volumes/Data`; if that mount is absent, identify the volume containing the user's data first.
- Start with shallow, targeted size scans of likely consumers and drill down into the largest relevant directories. For example, `du -k -d 1 "$HOME/Library/Caches"`. Bound expensive scans and tool health checks. Report inaccessible locations instead of silently treating them as empty or escalating privileges.

Folder totals are not independent physical allocations. APFS clones, hard links, snapshots, and sparse VM disks can make summed `du` output misleading. Use the same `df` measurement before and after; describe the difference as net observed recovery, which concurrent writes can affect.

## Decide what is disposable

Build a concrete candidate list: exact path or resource name, purpose, estimated allocation, last use, active references, and the operation proposed. Inspect candidates before deleting them.

- Favor known regenerable caches and generated intermediates. A path named `cache`, a stopped process, or an old timestamp is not sufficient evidence by itself.
- Check relevant running processes, open files, working directories, active builds, application state, and mounted or shared paths. An empty open-file result alone does not prove a service will not use a file later. If visibility is incomplete or a dependency remains uncertain, preserve the candidate and explain the limit.
- Use modification/access times only as supporting evidence. Freshness cutoffs are conservative filters, not proof of inactivity; timestamps can be preserved during copying or changed by inspection.
- For installed project dependencies, confirm the package manifest and lockfile exist, the directory is generated and untracked, and it has no intentional local changes. Check host processes and container bind mounts. If dependencies are customized, needed offline, or cannot reliably be restored, retain them. Explain when a future build will require reinstalling dependencies.
- For Xcode caches, distinguish build intermediates from `.xcarchive`, `.dSYM`, `.xcresult`, logs, and retained test evidence. Check generated package checkouts for local changes before considering a complete cache reset.
- Use package-manager or application cleanup operations when they provide an inspectable, appropriately scoped mechanism. Avoid leaving half-deleted package bundles, registries, or manifests. Do not blanket-delete `~/Library/Caches`, application-support folders, worktrees, or dated task directories.
- Treat VM disks, container volumes, and sandbox workspaces as data-bearing resources. Keep them outside routine cache deletion until their dependencies and deletion authorization have been established.

## Simulators

If Xcode tools are installed, inspect `xcrun simctl list devices` and `xcrun simctl list runtimes`. Preserve booted devices, named diagnostic environments, required runtime versions, and any device data or test evidence the user needs.

Unavailable devices are candidates, not automatic trash. Once the unavailable-device set has been inspected and authorized, `xcrun simctl delete unavailable` is a scoped cleanup operation. For other devices, use explicit identifiers. Do not erase all simulators or remove runtimes simply because they are not currently booted.

## Execute and verify

1. For an audit, stop after presenting findings. For authorized cleanup, state the concrete scope and expected effects, including re-downloads or rebuilds.
2. Request specific authorization for uncertain or data-bearing candidates, service interruptions, or scope expansion. Finish independent, already-authorized cleanup while clarification is pending. Do not infer approval from elapsed time.
3. Recheck candidate activity immediately before removal. Use exact verified paths or resource identifiers, proper argument quoting, and the owning tool where appropriate. Do not construct broad wildcard deletions or derive executable commands from filenames or logs.
4. Keep a lightweight receipt of affected paths/resources, operation outcomes, and failures. Avoid recording secrets or copying private file contents into reports.
5. Wait for each cleanup operation to finish. Verify intended removals, preservation of excluded data, and the state of previously active workloads. Do not report a background deletion as completed when it has only started.
6. Recheck free space on the same data volume. Report measured recovery, remaining free space, removed categories, preserved large consumers, and any limitations. Files moved to Trash still occupy space; do not claim recovery until space is actually released. Emptying unrelated Trash contents needs its own authorization.

If a tool stalls, preserve its data and report the blocked portion. Do not kill an engine, restart a service, delete its disk image, or escalate to broader deletion merely because cache cleanup recovered little space.
