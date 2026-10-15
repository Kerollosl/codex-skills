---
name: repo-secret-sweep
description: Audit owned repositories for accidentally committed secrets and guide safe remediation when the user requests a secret sweep.
---

# Repo Secret Sweep

Find leaked secrets in the user's own repositories (working tree and full git history). Report first; rewrite history only with approval.

This is defensive security on the user's own repositories. Never run against repos the user doesn't own.

## Tooling (detected at runtime)
- **Secret scan**: prefer `gitleaks` if on PATH; otherwise fall back to the grep patterns below.
- **History rewrite**: prefer `git-filter-repo` (installed) over `git filter-branch`.

## Step 1 — Enumerate targets
Ask the user for scope if unclear. Default sources:
```bash
# Remote repos owned by the user
gh repo list --limit 200 --json name,visibility,url --jq '.[] | [.visibility, .name, .url] | @tsv'
# Local clones
find ~/code-projects -maxdepth 3 -name .git -type d -prune 2>/dev/null | sed 's:/.git::'
```
Prioritize **public** repos — a leaked key in a public repo is live exposure.

## Step 2 — Scan for secrets (read-only)
Per repo, scan working tree + history.

**With gitleaks:**
```bash
gitleaks detect --source . --no-banner --redact -v
```

**Fallback (no gitleaks)** — scan history with `git log -p` / `git grep` over patterns. High-signal regexes:
| Secret | Pattern |
|---|---|
| AWS access key | `AKIA[0-9A-Z]{16}` |
| Google API key | `AIza[0-9A-Za-z_\-]{35}` |
| OpenAI / Anthropic | `sk-[A-Za-z0-9]{20,}`, `sk-ant-[A-Za-z0-9-]{20,}` |
| GitHub token | `gh[pousr]_[A-Za-z0-9]{36,}` |
| Slack token | `xox[baprs]-[A-Za-z0-9-]{10,}` |
| Private key block | `-----BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY-----` |
| Generic | `(api[_-]?key|secret|token|password)\s*[:=]\s*['"][^'"]{12,}` |
| Committed env | tracked `.env`, `.env.*`, `*.pem`, `credentials.json`, `service-account*.json` |

```bash
# tracked secret-bearing files
git ls-files | grep -iE '(^|/)\.env($|\.)|\.pem$|credentials\.json$|service-account.*\.json$'
# history scan for a pattern (example)
git log -p --all -S 'AKIA' --pickaxe-regex -- . | python3 -c 'import re, sys; pattern = re.compile(r"AKIA[0-9A-Z]{16}"); [print(str(n) + ": AWS key [REDACTED, ending " + m.group(0)[-4:] + "]") for n, line in enumerate(sys.stdin, 1) for m in pattern.finditer(line)]'
```

For every fallback pattern, emit only finding metadata and a redacted matched-value suffix; never print the surrounding source line, which may contain other credentials. Keep raw values inside the scanner process.

Report findings as a table: repo / file / commit / secret type / **in history?** (true = needs rewrite, not just deletion). A secret that ever touched history is compromised even if later deleted — flag it for rotation.

## Step 3 — Triage with the user
For each finding state the remediation, do not auto-fix:
- **Rotate the credential first** (the key is already exposed; rewriting history doesn't un-leak it). Surface this prominently.
- Remove from working tree + add to `.gitignore`.
- Purge from history (Step 4) only if the user confirms — rewriting is destructive and breaks clones/forks.

## Step 4 — Remediate confirmed secret exposure

After the user approves the specific repository and remediation, use `git-filter-repo` to remove the confirmed secret or secret-bearing file. Inspect the planned replacement rules locally without printing credential values. Back up the repository, verify the rewritten history no longer contains the credential, and show the exact push plan before an authorized push. Credential rotation remains necessary.

## Safety rules
- **Always back up before any history rewrite**: `git clone --mirror <repo> ~/.codex/.archive/$(date +%F)/<repo>.mirror` or note the current HEAD per branch.
- Secrets in history = **rotate the credential**, do not rely on rewrite alone.
- Never print full secret values in output; redact to last 4 chars.
- `--force-with-lease`, never bare `--force`.
- Get explicit per-repo confirmation before any push or history rewrite.

## Output
Lead with counts: "N repos scanned, M secrets found (K in history)." Then the findings table, then the remediation offer. Keep it actionable in under 5 minutes.
