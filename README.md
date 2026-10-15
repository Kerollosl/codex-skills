# Personal Codex skills

Private, portable snapshots of the standalone skills in `~/.codex/skills` and
`~/.agents/skills`. Personal skills live in `.agents/skills/`, which Codex discovers
when working in this repository. `sources.json` records each local source.

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
