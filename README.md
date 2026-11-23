# macOS Safe Disk Cleanup

An Agent Skill for reclaiming space on a macOS development machine while preserving active work and retained data.

It guides an agent to measure disk usage, identify disposable files, check active workloads, perform authorized cleanup, and verify the actual space recovered. It contains instructions, not an automatic deletion script. The agent still needs to inspect your machine and respect your permissions.

## Install

Review [SKILL.md](SKILL.md) before installing. With the [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add Makepad-fr/macos-safe-disk-cleanup --skill macos-safe-disk-cleanup
```

The CLI lets you select a supported agent and installation scope. You can also use your agent's skill installer with this repository's URL.

## Use

Ask your agent normally; you do not need to name the skill:

> Can you make space on my device without deleting my projects?

> My Mac is almost full. Find what is taking up space and clear disposable caches.

For an audit without deletion:

> What is taking up storage on my Mac? Show me cleanup candidates, but do not delete anything.

The description includes these everyday requests, and Codex implicit invocation is explicitly enabled. The agent still chooses whether the skill applies from the request and environment; automatic selection does not grant additional deletion permissions. You can also invoke `$macos-safe-disk-cleanup` explicitly.

## What it checks

- Actual free space on the APFS data volume, rather than adding overlapping folder totals.
- Active builds, open files, working directories, and recently used dependencies.
- Rebuildable caches versus source files, databases, archives, and retained evidence.
- Booted simulators and device data that may still be needed.
- Docker contexts, active containers, named volumes, and sandbox workspaces.
- CI runner registrations, pending work, reusable VM templates, and diagnostic exports before deleting old guests.
- Completion of cleanup and the state of workloads afterward.

APFS clones can share most of their disk blocks. A directory that reports 100 GB may release very little space when deleted. This skill reports the measured free-space change and does not promise savings from folder sizes alone.

## Scope

macOS is required for the cleanup workflow. Xcode tools are needed only for simulator work. Docker, a VM manager such as Tart, and CI-service access are needed only when inspecting those resources. Missing tools or denied filesystem access should result in a partial audit, not installation, privilege escalation, or service shutdown without authorization.

The [virtualization runbook](references/virtualization.md) explains why a stopped VM or an unattached volume can still matter. It also separates runner registration checks from proof that an actual CI job completed.

The package follows the [Agent Skills format](https://agentskills.io/specification) and includes optional Codex UI metadata. Its package structure is validated in CI; that check does not prove every cleanup decision is safe on every machine.

The public instructions were generalized from practical workstation cleanup sessions. They contain no personal filesystem paths, private repository names, credentials, or retained diagnostic records.

## License

MIT. See [LICENSE](LICENSE).
