---
name: improve-skills
description: Audit Codex skills, agents, routing, and recent usage to produce an evidence-based improvement list. Read-only by default; apply scoped repairs when the user explicitly requests them.
---

# Improve Skills

Audit the requested assets. A request to run an audit produces a report; a request to fix named findings authorizes those repairs without asking again. Do not expand repairs to unrelated assets, delete files, change connected services, or rewrite memory based on the audit alone.

## Inventory and evidence

- Discover personal skills under `~/.agents/skills` and `~/.codex/skills`, plus project-local skill directories; inspect `~/.codex/agents`, commands, AGENTS.md, hooks/settings, and MCP configuration when relevant. Deduplicate symlinks/resolved paths.
- Use the current session's exposed skills and tools as the authority for runtime availability. Plugin cache files are installed artifacts, not proof that a plugin is enabled or its tools callable. Do not count every historical plugin version as a separate active asset.
- Read metadata and focused instructions. Validate referenced paths and script callers before recommending removals. Avoid printing configuration secrets or credential-bearing tool arguments.
- Run `python3 scripts/audit_usage.py --days 30` from this skill directory for aggregate modern-session evidence. Supports `--session-root PATH` (repeatable) for isolated or alternate stores. The helper is read-only and emits no prompt bodies or tool arguments.
- Its explicit user requests, skill-file reads, and tool calls are separate evidence categories. A skill mention, injected skill catalog, read command, cached file, or agent log does not establish successful execution. Inspect relevant tool results and verified artifacts for success; label it unknown otherwise. Copied sessions and mirrored user messages must not inflate counts.
- For workflow gaps, inspect a narrow sample of actual user requests locally: strip injected AGENTS.md/environment/skill blocks and Chrome tab context, retaining `## My request:` text. Never export private prompt text by default. Count repeated workflows across distinct sessions, and summarize themes without personal details.

## Recommendations

Classify each in-scope asset as active, underused, heavy, or insufficient evidence. Separate usage from correctness. Zero observed use is not a deletion verdict: verify at least 60 days of adequate evidence, no fitting requests, no rare critical role, and a maintained replacement. Keep newly created skills and useful low-maintenance workflows. Archive only when explicitly authorized; preserve a recoverable backup.

Check routing against live connectors before falling back to APIs or browser control. Check scripts, references, authorization boundaries, source-grounding, and mutation readback. Missing tools are availability findings, not proof of dead assets. Memory findings are recommendations; update memory only on a direct user request.

## Report

Lead with counts and scope/window/coverage limitations. Use a concise report with Summary, Delete Candidates, Improve Candidates, Create Candidates, Keep As-Is, and Next Audit (30 days). Tables should give asset/type, evidence, reason, priority, and proposed action. Include an inventory appendix when needed to make full coverage reviewable. Do not recommend disabling plugins or MCPs solely from missing historical invocations.

When remediation is requested, back up each affected file, apply only approved scope, validate metadata and meaningful script behavior, and report changes, checks, and unresolved items. Do not edit vendor plugin caches as a durable repair; use supported overrides or report upstream changes.
