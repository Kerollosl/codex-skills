#!/usr/bin/env python3
"""
No-Enter variant of auth.py — for environments where an interactive
`input()` prompt can't be fed stdin (e.g. Claude Code's `!` bar).

Opens a real, visible Chromium window pointed at Instagram. You log in
by hand exactly as with auth.py — username/password, 2FA, "Save login
info?", whatever. Instead of waiting for you to press Enter, this script
polls the browser's cookies and auto-saves the session the moment it
sees you're logged in (sessionid + ds_user_id cookies present).

Nothing here sees or stores your password. Same real human login in a
real visible browser.
"""
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

AUTH_STATE_PATH = Path(__file__).resolve().parent.parent / "auth_state.json"

POLL_SECONDS = 3
TIMEOUT_SECONDS = 600           # give up after 10 min
STABLE_CHECKS_REQUIRED = 2      # consecutive logged-in reads before saving


def _logged_in(cookies) -> bool:
    names = {c["name"]: c.get("value", "") for c in cookies}
    return bool(names.get("sessionid")) and bool(names.get("ds_user_id"))


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.instagram.com/")

        print()
        print("A Chromium window just opened.")
        print("Log in to Instagram in that window (handle 2FA / prompts as needed).")
        print("Nothing to press here — this will auto-save once you're logged in.")
        print()

        deadline = time.time() + TIMEOUT_SECONDS
        stable = 0
        while time.time() < deadline:
            try:
                cookies = context.cookies()
            except Exception:
                print("Browser window was closed before login completed. Nothing saved.")
                return 1

            if _logged_in(cookies):
                stable += 1
                if stable >= STABLE_CHECKS_REQUIRED:
                    break
                print("Detected login — confirming...")
            else:
                stable = 0

            time.sleep(POLL_SECONDS)
        else:
            print(f"Timed out after {TIMEOUT_SECONDS}s waiting for login. Nothing saved.")
            browser.close()
            return 1

        # let any final XHR / cookie writes settle
        time.sleep(3)
        context.storage_state(path=str(AUTH_STATE_PATH))
        browser.close()

        print(f"Session saved to {AUTH_STATE_PATH}")
        print("You can now run scrape.py. Re-run this step whenever the session")
        print("expires (scrape.py will tell you clearly if that happens).")
        return 0


if __name__ == "__main__":
    sys.exit(main())
