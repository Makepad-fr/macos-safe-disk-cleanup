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

Ask your agent:

> Use $macos-safe-disk-cleanup to find what is taking up space. Clear disposable caches, preserve my active projects and release evidence, and report the measured space recovered.

For an audit without deletion:

> Use $macos-safe-disk-cleanup to audit my Mac's storage. Show the largest consumers and concrete cleanup candidates; do not delete anything.

## What it checks

- Actual free space on the APFS data volume, rather than adding overlapping folder totals.
- Active builds, open files, working directories, and recently used dependencies.
- Rebuildable caches versus source files, databases, archives, and retained evidence.
- Booted simulators and device data that may still be needed.
- Completion of cleanup and the state of workloads afterward.

APFS clones can share most of their disk blocks. A directory that reports 100 GB may release very little space when deleted. This skill reports the measured free-space change and does not promise savings from folder sizes alone.

## Scope

macOS is required for the cleanup workflow. Xcode tools are needed only for simulator work. Missing tools or denied filesystem access should result in a partial audit, not installation, privilege escalation, or service shutdown without authorization.

The package follows the [Agent Skills format](https://agentskills.io/specification) and includes optional Codex UI metadata. Its package structure is validated in CI; that check does not prove every cleanup decision is safe on every machine.

The public instructions were generalized from practical workstation cleanup sessions. They contain no personal filesystem paths, private repository names, credentials, or retained diagnostic records.

## License

MIT. See [LICENSE](LICENSE).
