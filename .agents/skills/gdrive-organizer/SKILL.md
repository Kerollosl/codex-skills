---
name: drive-organizer
description: Organize a Google Drive folder or collection by reviewing contents, proposing a structure, and making approved file moves.
---

# Google Drive Organizer

## Choose the interface

Use the available Google Drive connector as the primary interface for connected Drive work, following its current tool schemas and matching Google Drive skill. Resolve the target folder and file IDs, list all pages of contents, and inspect current parents before planning. For Google native documents, operate on their Drive IDs rather than local `.gdoc`/`.gsheet`/`.gslides` pointers.

The local-sync examples below apply only when the user explicitly requests local synced-folder work or the connector lacks the required operation and an appropriate local fallback is authorized. Verify that the configured sync root actually exists; do not assume an old account path is current.

## Connector workflow

1. Inventory the requested folder, recording file ID, name, and existing parent IDs. Propose the smallest structure that fits the user's retrieval pattern.
2. Present the concrete move/rename plan when approval is needed. Existing authorization for that plan carries forward; do not ask again.
3. Execute the approved changes with supported folder-create, parent-update/move, and rename operations. Preserve file IDs, content, and sharing. Do not copy-and-delete files to simulate a move or trash anything unless separately requested.
4. Fetch/list the affected files and folders again; verify names, parents, item counts, and no unintended duplicates. Keep the original-to-new-parent mapping for reversal and report verified results. A local directory listing alone does not establish Drive sync completion.

## The User's Naming Convention

When organizing, follow the existing pattern:

```
[N] Section Name 🔣/
├── [1] Sub-section A 📚/
├── [2] Sub-section B 💻/
└── [3] Sub-section C 📁/
```

**Format rules:**
- `[N]` prefix — numeric ordering (controls Finder/Drive sort order)
- Title in title case
- Emoji suffix that hints at the content type
- Spaces around the brackets, no leading dash

Examples from the user's existing structure:
- `[1] SELF IMPROVEMENT JOURNEY` (no emoji needed at top level if implied)
- `[2] Church/[1] SM JH 8th Grade ⛪`
- `[3] Colab Notebooks/[0] Financial Analysis 📊/`
- `[1] SELF IMPROVEMENT JOURNEY/[3] Misc./Financial💵`

## Local synced-folder workflow (conditional)

### Step 1: Survey Before You Touch

Always understand the current state first:

```bash
# Get a tree view with sizes
cd "/Users/kerolowandy/Library/CloudStorage/GoogleDrive-klowandy@gmail.com/My Drive/<target>"
ls -lh
find . -maxdepth 2 -type d
find . -maxdepth 2 -type f | head -30

# Check what file types are present
find . -maxdepth 2 -type f -name '*.*' | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

### Step 2: Propose the Structure

Before moving anything, draft the new structure as a tree and show it to the user:

```
NEW STRUCTURE:
[1] Lessons 📖/
├── [1] Old Testament 📜/
│   ├── Genesis lessons.pdf
│   └── Exodus notes.docx
└── [2] New Testament ✝️/
    ├── Matthew lessons.pdf
    └── Acts notes.docx
[2] Resources 📚/
└── ...
```

Get approval before executing — the user can usually spot issues with the grouping you'd miss.

### Step 3: Execute Safely

Drive sync caveats:

- **Don't delete** — move to an `[Archive]/` folder instead. Drive sync won't recover deletes from local instantly.
- **Quote paths** — Drive folders often contain spaces and emojis. Always quote: `mv "$source" "$dest"`.
- **Watch for sync conflicts** — if the user has Drive open in a browser doing things, wait until they're done.
- **Preserve originals and identity** — prefer a move within the same sync root and record the prior path; do not copy-and-delete as a default.

Pattern for safe reorganization:

```bash
cd "/Users/kerolowandy/Library/CloudStorage/GoogleDrive-klowandy@gmail.com/My Drive/<target>"

# Create new dirs
mkdir -p "[1] New Section 📁"
mkdir -p "[2] Other Section 📂"

# Move files into place (use mv, not cp+rm — single atomic op when same fs)
mv "old-file-1.pdf" "[1] New Section 📁/"
mv "old-file-2.docx" "[1] New Section 📁/"

# Verify
ls -la "[1] New Section 📁/"
```

### Step 4: Handle Special File Types

Different file types need different treatment:

- **Google native** (`.gdoc`, `.gsheet`, `.gslides`) — use the connector to move the native Drive object by ID; a local pointer move may not move the underlying document.
- **Synced binary files** (.pdf, .docx, etc.) — fully present locally, syncs back to Drive on move
- **Symlinks/aliases** — check with `file <name>` first; moving a symlink doesn't move the target

### Step 5: Update References

After reorganizing, check if anything references the old paths:
- The user's directory map memory, if present under the current agent's memory directory
- NotebookLM notebooks pointing to specific files
- Any scripts or shortcuts

Offer to update these too.

## Common Organizational Patterns

### By Topic (subject matter)
```
[1] Bible Study 📖/
[2] Theology 🕊️/
[3] Church History ⛪/
```

### By Audience / Lesson Group
```
[1] Adults 👨/
[2] Teens 🧑/
[3] Kids 👶/
```

### By Type
```
[1] Lessons 📚/
[2] Activities 🎨/
[3] Worksheets 📝/
```

### By Time Period
```
[1] Ongoing 🟢/
[2] Archive 2025 📦/
[3] Archive 2024 📦/
```

Pick whichever matches how the user thinks about retrieval. If they say "find me last year's stuff", use time period. If they say "show me everything for the 8th graders", use audience.

## Reference: Common Drive Path Shortcuts

To save typing, set up aliases:

```bash
# In ~/.zshrc
alias gdrive='cd "/Users/kerolowandy/Library/CloudStorage/GoogleDrive-klowandy@gmail.com/My Drive"'
alias gdrive-self='gdrive && cd "[1] SELF IMPROVEMENT JOURNEY"'
alias gdrive-church='gdrive && cd "[2] Church"'
alias gdrive-colab='gdrive && cd "[3] Colab Notebooks"'
```

## Output Discipline

After organizing, give the user:
1. **Before/after tree** — what moved where
2. **What you didn't touch** — files you left in place and why
3. **Verification** — report fetched Drive parents/names or explicitly state that cloud sync is unverified
4. **Any followups** — broken references, files needing manual review
