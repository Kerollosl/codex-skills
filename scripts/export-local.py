#!/usr/bin/env python3
"""Explicitly refresh the repository snapshot from this Mac's skill folders."""
from pathlib import Path
import json
import shutil

REPO = Path(__file__).resolve().parents[1]
HOME = Path.home()
EXCLUDED = {
    '.git', '.venv', 'venv', 'node_modules', '__pycache__', '.DS_Store',
    '.pytest_cache', '.mypy_cache', '.ruff_cache', '.idea', '.vscode',
    'data', 'browser_state', 'browser_profile', 'auth_state.json',
    'auth_info.json', 'cookies.json', 'storage_state.json', 'state.json',
    'logs', 'dist', 'build', 'optimizer-results',
}


def ignored(path):
    name = path.name
    return (name in EXCLUDED or name == '.env' or
            (name.startswith('.env.') and name != '.env.example') or
            name.endswith(('.pyc', '.pyo', '.log', '.bak', '.tmp')))


def copy_tree(source, target):
    count = 0
    for item in sorted(source.iterdir()):
        if ignored(item) or (item.is_symlink() and item.name != 'SKILL.md'):
            continue
        destination = target / item.name
        if item.is_dir():
            count += copy_tree(item, destination)
        elif item.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, destination)
            count += 1
    return count


def main():
    origins = {}
    files = 0
    # Prefer the active legacy Codex version when a folder exists in both roots.
    for label in ('.agents/skills', '.codex/skills'):
        root = HOME / label
        for skill in sorted(root.iterdir()):
            if not (skill / 'SKILL.md').is_file() or skill.name.startswith('.'):
                continue
            if skill.name in origins:
                old = HOME / origins[skill.name] / 'SKILL.md'
                if old.read_bytes() != (skill / 'SKILL.md').read_bytes():
                    archived = REPO / 'source-variants' / skill.name / 'agents-SKILL.md'
                    archived.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(old, archived)
            files += copy_tree(skill, REPO / '.agents/skills' / skill.name)
            origins[skill.name] = str(skill.relative_to(HOME))
    # Preserve system instructions as reference; Codex provides its own built-ins.
    system = HOME / '.codex/skills/.system'
    for skill in sorted(system.iterdir()):
        if (skill / 'SKILL.md').is_file():
            files += copy_tree(skill, REPO / 'system-reference' / skill.name)
    index = HOME / '.codex/skills/SKILL_INDEX.md'
    if index.is_file():
        shutil.copy2(index, REPO / 'LOCAL_SKILL_INDEX.md')
    (REPO / 'sources.json').write_text(json.dumps(origins, indent=2) + '\n')
    print(f'Exported {len(origins)} personal skills; copied {files} source files.')
    print('Review git diff before committing. Removed local files are not deleted here.')


if __name__ == '__main__':
    main()
