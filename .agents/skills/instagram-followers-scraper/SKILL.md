---
name: instagram-followers
description: >
  Scrape the full followers and/or following list (username + full name) from
  any Instagram profile into a CSV spreadsheet, using a repeatable Playwright
  script (not one-off browser commands). Use whenever the user wants a list
  or export of who follows them, who they follow, or who follows/is followed
  by another account — e.g. "export my Instagram followers to a spreadsheet",
  "get a list of everyone I follow on IG", "scrape @handle's follower list".
  Different from the instagram-scraper skill, which pulls tagged
  places/accounts out of someone's *posts* — this one is specifically for the
  followers/following relationship lists.
---

# Instagram Followers/Following Scraper

Exports followers and/or following for any Instagram account to a CSV, via a
real Playwright script the user can rerun anytime — not ad-hoc browser
commands typed into a session. Scripts live in `scripts/`.

## How To Use This Skill

**Run the bundled scripts. Don't reimplement this.** The scraping logic
below (selectors, scroll-stall handling, DOM structure) was reverse-engineered
by hand against the live site and is already working — writing fresh
browser-harness commands or new Playwright code for this task means
re-deriving all of it from scratch and likely re-hitting the same failure
modes documented under Known Gotchas. Every time this skill triggers:

1. Check whether `~/.codex/skills/instagram-followers-scraper/auth_state.json`
   exists.
   - If missing (or `scrape.py` reports the session expired): tell the user
     to run `auth.py` themselves and stop there — see Step 1. Do not attempt
     this step on the user's behalf; it requires them to type their own
     password into a real browser window, which you should never do for
     them.
   - If present, skip straight to Step 2.
2. Run `scrape.py` via Bash with flags matching what the user asked for
   (which handle, followers/following/both, output path if they named one).
3. Report the resulting counts and hand off the CSV (e.g. via SendUserFile).

## Why This Isn't Just an API Call

Instagram's internal `/api/v1/friendships/<id>/followers/` and `/following/`
endpoints refuse third-party fetches even with valid session cookies attached
— they return an empty user list or `{"message": "useragent mismatch"}`.
(This is unlike the post-feed API used by the sibling `instagram-scraper`
skill, which works fine.) So this skill drives the real web UI instead:
clicks the followers/following link, then scroll-scrapes the modal's
rendered DOM. Full technical rationale and the exact selector logic are
documented as comments at the top of `scripts/scrape.py` — read that before
changing the scraping logic, since the DOM structure it relies on is
non-obvious and was reverse-engineered by hand.

## Step 1 — One-Time Login

Never type or store the user's Instagram password. Instead, run the
auth script, which opens a real visible browser for the user to log into
by hand:

```bash
python3 ~/.codex/skills/instagram-followers-scraper/scripts/auth.py
```

This pauses and waits for the user to press Enter in the terminal after
they've logged in. It then saves the session (cookies + storage) to
`auth_state.json` next to the scripts. That file is a session-cookie
equivalent — treat it like a credential (don't commit it, don't share it,
don't put it anywhere synced/public).

Only needs to be re-run when the saved session expires — `scrape.py` will
detect that (redirect to the login page) and say so clearly rather than
failing silently or attempting anything with credentials.

## Step 2 — Scrape

```bash
python3 ~/.codex/skills/instagram-followers-scraper/scripts/scrape.py [options]
```

| Flag | Default | Meaning |
|---|---|---|
| `--handle` | auto-detect own account | Instagram handle to scrape (no `@`) |
| `--lists` | `both` | `followers`, `following`, or `both` |
| `--out` | `~/Downloads/instagram_<handle>_followers_following.csv` | Output CSV path |
| `--headed` | off | Show the browser window (useful for debugging) |
| `--pace` | `0.5` | Seconds between scroll ticks — raise this for large accounts |
| `--min-stall` | `10` | Consecutive no-growth scroll ticks (while at the bottom of loaded content) required before declaring a list complete |

Own-handle auto-detection looks for the nav bar's profile-picture image
(`img[alt*="profile picture"]` wrapped in a link) — reliable in practice but
not guaranteed across every Instagram layout change. If it fails, or to
scrape someone else's (public, or followed-by-you) account, pass `--handle`
explicitly.

Output is a CSV with columns `type,username,full_name`, one row per person,
sorted by type then username. The script prints running counts as it works,
not the full row list — keep it that way; a dump of hundreds of usernames in
terminal output isn't useful to a human watching.

## Known Gotchas

- **The follower/following link has no real `href`** — it's a client-side
  `<a href="#" role="link">` with an onClick handler. Select it by visible
  text ("...followers" / "...following"), not by href.
- **Lazy-load lag is the main failure mode.** Instagram can look "done"
  (bottom of currently-rendered content) while still fetching the next
  batch behind the scenes. A short stall tolerance cuts lists short — a
  388-account following list was truncated to 204 with only 4 stall ticks.
  `--min-stall 10` (the default) fixed it; raise it further if you notice
  undercounts on a rerun.
- **Rate limiting is a real risk on large accounts.** Follower/following
  scraping is watched more closely by Instagram than post scraping. This
  was only validated on a small account (~300-400 each way) with zero
  issues at the default pace. For accounts in the thousands, raise `--pace`
  (e.g. `--pace 1.0` or higher) and expect the run to take a while — don't
  assume the default pace is safe at scale.
- **CSS class names on this page are auto-generated and change often** —
  don't add selectors based on them. Everything in `scrape.py` intentionally
  uses structural/role/text-based selection instead.
- **Displayed counts (e.g. "306 followers") are approximate.** Expect the
  scraped count to land close to, not necessarily exactly matching, the
  number shown on the profile page.
