#!/usr/bin/env python3
"""Install the repository's personal skills for Codex or Claude Code."""
import argparse
import os
from pathlib import Path
import shutil
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=('codex', 'claude'), help='Skip the interactive choice')
    args = parser.parse_args()
    target = args.target
    if not target:
        if not sys.stdin.isatty():
            parser.error('choose --target codex or --target claude when running non-interactively')
        while target not in ('codex', 'claude'):
            choice = input('Install skills for [1] Codex or [2] Claude Code? ').strip().lower()
            target = {'1': 'codex', 'codex': 'codex', '2': 'claude', 'claude': 'claude', 'claude code': 'claude'}.get(choice)
            if not target:
                print('Enter 1 or 2.')
    source = Path(__file__).resolve().parent.parent / '.agents' / 'skills'
    skills = sorted(p for p in source.iterdir() if p.is_dir() and (p / 'SKILL.md').is_file())
    if not skills:
        parser.error(f'No skills found in {source}')
    base = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex') if target == 'codex' else Path.home() / '.claude'
    destination = base / 'skills'
    destination.mkdir(parents=True, exist_ok=True)
    installed, skipped = 0, []
    for skill in skills:
        dest = destination / skill.name
        if dest.exists() or dest.is_symlink():
            skipped.append(skill.name)
            continue
        shutil.copytree(skill, dest, symlinks=True)
        installed += 1
    print(f'Installed {installed} skills to {destination}.')
    if skipped:
        print(f'Skipped {len(skipped)} existing skills: {", ".join(skipped)}')
    print('Restart your coding agent to discover newly installed skills.')


if __name__ == '__main__':
    main()
