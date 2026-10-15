#!/usr/bin/env python3
"""
One-time (or re-run-when-expired) Instagram login step.

Opens a real, visible Chromium window. Log in by hand — username/password,
2FA, "Save your login info?" prompts, whatever Instagram asks for. Once
you're looking at your home feed, come back to this terminal and press
Enter. The session gets saved to auth_state.json so scrape.py can reuse it
without ever touching your password.

Nothing in this script sees or stores your password — it's a real human
login in a real visible browser, same as opening Chrome yourself.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

AUTH_STATE_PATH = Path(__file__).resolve().parent.parent / "auth_state.json"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.instagram.com/")

        print()
        print("A Chromium window just opened.")
        print("Log in to Instagram in that window (handle 2FA / prompts as needed).")
        print("Once you can see your home feed, come back here and press Enter.")
        print()
        input("Press Enter once you're logged in... ")

        context.storage_state(path=str(AUTH_STATE_PATH))
        browser.close()

        print(f"Session saved to {AUTH_STATE_PATH}")
        print("You can now run scrape.py. Re-run this auth step whenever the")
        print("session expires (scrape.py will tell you clearly if that happens).")


if __name__ == "__main__":
    sys.exit(main())
