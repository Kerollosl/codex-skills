---
name: project-audit
description: Scan your entire project portfolio for health issues in minutes: stale branches, outdated dependencies, missing tests, code quality issues, and technical debt. Use this at the start of a coding session, before a major work push, or weekly to stay on top of portfolio health. Covers all projects in code-projects/, Chrome Extensions/, and other directories. Instantly shows what's broken, what's outdated, and what needs testing. Perfect for recurring weekly checks via /schedule.
---

# Project Auditor

Health check for your entire project portfolio in one command.

## What This Does

Scans **all your projects** and reports on:

**Git repos:**
- Stale branches (last commit >30 days ago)
- Unpushed commits
- Merge conflicts
- Uncommitted changes

**Dependencies:**
- Outdated packages (npm, pip, etc.)
- Security vulnerabilities
- Deprecated versions
- Missing package-lock files

**Code quality:**
- Missing tests
- Linting errors
- Type checking failures
- Code coverage gaps

**Documentation:**
- Missing README
- Outdated AGENTS.md
- Broken links in docs
- Missing API docs

**Configuration:**
- Missing .gitignore
- Exposed secrets
- Bad permissions
- Misconfigured CI/CD

## How to Use

**Full portfolio audit:**
```
/project-auditor
Audit all my projects
```

**Focus on one directory:**
```
/project-auditor
Scan ~/code-projects for health issues
```

**Prioritize by urgency:**
```
/project-auditor
What's the most critical issue across all projects?
```

**Schedule weekly reviews:**
```
/schedule
Run /project-auditor every Monday at 9am
```

## Output Format

**Dashboard summary:**
- 🔴 **Critical** — Security issues, broken tests, merge conflicts
- 🟡 **Warnings** — Stale branches, outdated deps, missing tests
- 🟢 **Healthy** — No issues found
- 📊 **Metrics** — Dependency age, code coverage, test count

**Per-project breakdown:**
- Project name + path
- Last commit date
- Branch status
- Dep versions vs latest
- Test coverage
- Issues found
- Recommended actions

## Example Output

```
📋 PORTFOLIO AUDIT REPORT
================================

🔴 CRITICAL ISSUES (3)
  - bulk-gcal-mover: 8 uncommitted changes
  - flight-email-parser: 1 merge conflict
  - todoist-ai: npm audit found vulnerabilities

🟡 WARNINGS (12)
  - 4 branches not merged in 60+ days
  - 6 packages 2+ major versions outdated
  - 3 projects missing tests

🟢 HEALTHY (5)
  - All dependencies current
  - Tests passing
  - Clean working tree

📊 PORTFOLIO METRICS
  - Total projects: 12
  - Avg dependency age: 1.3 months
  - Test coverage: 62%
  - Stale branches: 7
```

## Integration with /schedule

Perfect for recurring audits:
```
/schedule
Run /project-auditor every Monday
```

Get a weekly dashboard of what needs attention. Never let technical debt creep in unnoticed.

## Performance

- Small portfolios (5 projects): ~2 minutes
- Medium portfolios (10-20 projects): ~5 minutes
- Large portfolios (20+ projects): ~10 minutes

Scans in parallel where possible.
