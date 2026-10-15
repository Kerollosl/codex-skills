#!/usr/bin/env python3
"""
Scrape an Instagram account's followers and/or following list to a CSV.

Reuses the session saved by auth.py — no password ever touches this script.
Run `python auth.py` first if auth_state.json doesn't exist yet or has expired.

Why this works the way it does (read before "fixing" it):

- Instagram's internal REST API (`/api/v1/friendships/<id>/followers/`) refuses
  these requests even with valid session cookies attached — it silently
  returns an empty user list or a "useragent mismatch" error. That's not a
  bug in this script; it's Instagram specifically guarding that endpoint
  (unlike the post-feed API, which is fine with third-party fetches). So
  this script drives the real web UI instead: it clicks the followers/
  following link like a person would, and reads the names straight out of
  the rendered modal.

- The follower/following links render as `<a role="link" href="#">` with an
  onClick handler — there is no real `href` to select by, so we match on
  visible text ("...followers" / "...following") instead.

- Row structure inside the modal: each row has two `<a role="link"
  href="/username/">` tags (an avatar-image link with no text, then a
  username-text link) plus a sibling `<span>` holding the display name.
  Walking 5 `parentElement` steps up from the username link lands on a row
  container whose `children[1]` is that display-name span. CSS class names
  on this page are auto-generated/obfuscated and change often — this
  structural walk is far more stable than any class selector.

- The scrollable list is a `div` *inside* the dialog, not the dialog itself.
  It's found by scanning the dialog's descendants for the first element
  whose scrollHeight exceeds its clientHeight.

- Instagram lazy-loads more rows as you approach the bottom, and the fetch
  can lag behind the scroll. A naive "stop after 1-2 scrolls with no new
  rows" check will cut a list short (tested: cut a 388-account list off at
  204). This script requires --min-stall consecutive no-growth scroll ticks
  *and* being at the bottom of the currently-rendered content before it
  decides the list is actually finished.
"""
import argparse
import csv
import sys
import time
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

SKILL_DIR = Path(__file__).resolve().parent.parent
AUTH_STATE_PATH = SKILL_DIR / "auth_state.json"

DETECT_OWN_HANDLE_JS = """
() => {
  const imgs = Array.from(document.querySelectorAll('img[alt*="profile picture" i]'));
  for (const img of imgs) {
    const a = img.closest('a');
    if (!a) continue;
    const href = a.getAttribute('href');
    if (href && /^\\/[^\\/]+\\/$/.test(href)) return href.slice(1, -1);
  }
  return null;
}
"""

FIND_SCROLL_CONTAINER_JS = """
() => {
  const dialog = document.querySelector('div[role="dialog"]');
  if (!dialog) return false;
  const all = dialog.querySelectorAll('*');
  for (const node of all) {
    if (node.scrollHeight > node.clientHeight + 20 && node.clientHeight > 100) {
      window.__igScrollEl = node;
      return true;
    }
  }
  return false;
}
"""

EXTRACT_AND_SCROLL_JS = """
() => {
  const dialog = document.querySelector('div[role="dialog"]');
  const links = Array.from(dialog.querySelectorAll('a[role="link"]'))
    .filter(a => /^\\/[^\\/]+\\/$/.test(a.getAttribute('href') || '') && a.textContent.trim() !== '');
  const rows = [];
  for (const a of links) {
    const href = a.getAttribute('href');
    const username = href.slice(1, -1);
    let row = a;
    for (let i = 0; i < 5; i++) { if (row.parentElement) row = row.parentElement; }
    let fullName = '';
    if (row.children.length > 1) fullName = row.children[1].textContent.trim();
    rows.push([username, fullName]);
  }
  const el = window.__igScrollEl;
  el.scrollTop = el.scrollTop + el.clientHeight * 0.9;
  return {
    rows,
    scrollTop: el.scrollTop,
    scrollHeight: el.scrollHeight,
    clientHeight: el.clientHeight,
  };
}
"""


def detect_own_handle(page: Page) -> str | None:
    page.goto("https://www.instagram.com/")
    page.wait_for_load_state("networkidle")
    return page.evaluate(DETECT_OWN_HANDLE_JS)


def scrape_list(page: Page, kind: str, min_stall: int, tick_sleep: float, max_ticks: int) -> dict[str, str]:
    """kind: 'followers' or 'following'. Returns {username: full_name}."""
    link = page.locator('a[role="link"]', has_text=kind).first
    link.click()
    page.wait_for_selector('div[role="dialog"]', timeout=15000)
    time.sleep(1)

    if not page.evaluate(FIND_SCROLL_CONTAINER_JS):
        raise RuntimeError(f"Could not find the scrollable container inside the {kind} dialog")

    results: dict[str, str] = {}
    stall = 0
    for i in range(max_ticks):
        batch = page.evaluate(EXTRACT_AND_SCROLL_JS)
        before = len(results)
        for username, full_name in batch["rows"]:
            results[username] = full_name
        added = len(results) - before

        at_bottom = batch["scrollTop"] + batch["clientHeight"] >= batch["scrollHeight"] - 5
        stall = stall + 1 if added == 0 else 0
        if stall >= min_stall and at_bottom:
            break
        time.sleep(tick_sleep)
    else:
        print(f"  warning: hit max_ticks ({max_ticks}) before settling — list may be incomplete", file=sys.stderr)

    page.keyboard.press("Escape")
    time.sleep(0.5)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--handle", help="Instagram handle to scrape (default: auto-detect your own logged-in account)")
    parser.add_argument("--lists", choices=["followers", "following", "both"], default="both", help="Which list(s) to pull (default: both)")
    parser.add_argument("--out", help="Output CSV path (default: ~/Downloads/instagram_<handle>_followers_following.csv)")
    parser.add_argument("--headed", action="store_true", help="Show the browser window (default: headless)")
    parser.add_argument("--pace", type=float, default=0.5, help="Seconds to sleep between scroll ticks (default: 0.5). Increase for large accounts to reduce rate-limit risk.")
    parser.add_argument("--min-stall", type=int, default=10, help="Consecutive no-growth scroll ticks required (while at the bottom of loaded content) before declaring a list complete (default: 10)")
    args = parser.parse_args()

    if not AUTH_STATE_PATH.exists():
        print(f"No saved session at {AUTH_STATE_PATH}.", file=sys.stderr)
        print("Run `python auth.py` first to log in once.", file=sys.stderr)
        return 1

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        context = browser.new_context(storage_state=str(AUTH_STATE_PATH))
        page = context.new_page()

        handle = args.handle
        if not handle:
            handle = detect_own_handle(page)
            if not handle:
                print("Could not auto-detect your handle. Pass --handle explicitly.", file=sys.stderr)
                browser.close()
                return 1
            print(f"Detected own handle: @{handle}")

        page.goto(f"https://www.instagram.com/{handle}/")
        page.wait_for_load_state("networkidle")

        if "accounts/login" in page.url:
            print("Redirected to the Instagram login page — your saved session has expired.", file=sys.stderr)
            print("Run `python auth.py` again to log back in.", file=sys.stderr)
            browser.close()
            return 1

        rows: list[tuple[str, str, str]] = []

        if args.lists in ("followers", "both"):
            print("Scraping followers...")
            followers = scrape_list(page, "followers", args.min_stall, args.pace, max_ticks=2000)
            print(f"  {len(followers)} followers collected")
            rows += [("follower", u, n) for u, n in followers.items()]

        if args.lists in ("following", "both"):
            print("Scraping following...")
            following = scrape_list(page, "following", args.min_stall, args.pace, max_ticks=2000)
            print(f"  {len(following)} following collected")
            rows += [("following", u, n) for u, n in following.items()]

        browser.close()

    rows.sort(key=lambda r: (r[0], r[1].lower()))

    out_path = Path(args.out) if args.out else Path.home() / "Downloads" / f"instagram_{handle}_followers_following.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "username", "full_name"])
        writer.writerows(rows)

    print(f"\nSaved {len(rows)} rows to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
