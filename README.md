# Personal Codex skills

Private, portable snapshots of the standalone skills in `~/.codex/skills` and
`~/.agents/skills`. Personal skills live in `.agents/skills/`, which Codex discovers
when working in this repository. `sources.json` records each local source.

## One entry point for repository workflows

Use [UI Design Lead](.agents/skills/ui-design-lead/SKILL.md) to choose and run the
appropriate skills for a task. It specializes in web/mobile design and also hands
off engineering, research, file, and connected-account work to the right specialist.
Its [catalog](.agents/skills/ui-design-lead/references/catalog.md) covers all 60
active skill folders and resolves directory aliases to their actual skill names;
it checks current sibling metadata when the catalog does not fit.

Example: "Use $ui-design-lead to build this Expo screen and verify its behavior."
The orchestrator loads only the skills needed for the task and retains existing
platform, design-system, tool-access, and authorization constraints.

## Codex Cloud

Grant the Codex GitHub connection access to this private repository, then select
it for a cloud environment/task. Repository skills are already in the discovery
layout; no installation step is needed when working in this repo.

To use selected skills in another project, copy those skill directories into
that project's `.agents/skills/` and commit them there. Access to this repository
alone does not automatically add its skills to unrelated cloud environments.

Skills that call Mac apps, absolute local paths, connected tools, or authenticated
services still need compatible tools and configuration in their target environment.
This repository supplies instructions and resources, not connector credentials.

Official discovery documentation: https://learn.chatgpt.com/docs/build-skills

## Local workflow

Install the complete personal skill collection for Codex or Claude Code:

```sh
python3 scripts/install.py
```

Choose the agent at the prompt, or use `--target codex` or `--target claude`
for unattended setup. The installer copies complete skill folders to
`~/.codex/skills` (or `$CODEX_HOME/skills` when set) or `~/.claude/skills`.
Existing folders are skipped and reported, so local edits are preserved;
remove or rename a folder yourself before reinstalling it. Restart the agent
to discover new skills. System reference skills and plugin-managed skills are
not installed. Some skills require additional tools, services, or configuration.

This clone lives under `~/code-projects/Github-Repos/codex-skills`. The existing
zsh startup sync discovers repositories recursively under `~/code-projects`
and pulls their configured upstream with `git pull --ff-only`.

The existing local skill folders remain intact. This repo is a snapshot, so
pulling it does not overwrite the installed skills. To explicitly refresh the
snapshot after editing local skills:

```sh
python3 scripts/export-local.py
git diff
git add .
git commit -m "Update personal skills"
git push
```

Export is additive: it does not delete stale snapshot files. Review deletions and
renames manually. Review every diff before committing, including newly added
files, for credentials and private data.

## Included and excluded

- All standalone personal skill folders, including their scripts and resources.
- Bundled OpenAI skills preserved in `system-reference/` for reference only.
- Differing duplicate instructions, if present, preserved in `source-variants/`.
- A snapshot of the local skill index; its Mac-specific paths are historical.
- No browser login state, NotebookLM personal data, virtual environments, caches,
  nested Git histories, or local secrets/configuration.
- Plugin-managed skills remain managed by their plugins and are not vendored.
  Install the relevant plugins separately in each supported environment.

Third-party skills retain their included licenses and attribution.

## Curated mobile and web design additions

Reviewed on October 29, 2026. The focused selection complements the existing
Frontend Design, Impeccable, Taste, image-direction, and iOS design skills.

| Need | Start with | Use alongside |
| --- | --- | --- |
| Native iOS / macOS implementation | [SwiftUI Expert](.agents/skills/swiftui-expert-skill/SKILL.md) | Existing mobile-ios-design for design direction |
| Expo iOS / Android screens | [Expo Native UI](.agents/skills/expo-native-ui/SKILL.md) | [Expo UI](.agents/skills/expo-ui/SKILL.md) for real native controls |
| Native tabs, stacks, sheets, navigation | [Expo Router](.agents/skills/expo-router/SKILL.md) | Expo Native UI |
| Mobile gestures, haptics, transitions | [Expo Animation](.agents/skills/expo-animation/SKILL.md) | Expo Router |
| Consistent mobile themes and components | [Expo Design System](.agents/skills/expo-design-system/SKILL.md) | Expo Native UI |
| Choose the Expo workflow and check SDK | [Expo Overview](.agents/skills/expo-overview/SKILL.md) | Relevant installed Expo leaf skill |
| Web component and interaction polish | [Emil Design Engineering](.agents/skills/emil-design-eng/SKILL.md) | Existing build workflow |
| Web accessibility and UX code review | [Web Design Guidelines](.agents/skills/web-design-guidelines/SKILL.md) | Existing Impeccable review workflow |

These are repository snapshots, not automatic installations in other projects
or the ChatGPT Skills tab. Copy only the skills needed into a project's
`.agents/skills/`. Preserve each complete folder, including references, scripts,
assets, and license/notice files. SwiftUI trace tools require macOS and Xcode;
Vercel's review skill fetches its current guidelines over the network.

[third-party-sources.json](third-party-sources.json) records primary sources,
immutable revisions, upstream blob hashes, license evidence, and local adaptations.
The Expo snapshot includes only the UI-focused subset; other upstream modules
are optional. External Expo feedback requires an explicit user request.

Local export metadata remains in `sources.json`. The additive local export does
not remove these additions; review any future export that introduces a local
skill with the same name before replacing a curated snapshot.
