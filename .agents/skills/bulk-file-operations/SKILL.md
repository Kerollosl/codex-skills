---
name: bulk-file-operations
description: Organize, rename, deduplicate, merge, or move many local files with a reversible plan and count checks.
---

# Bulk File Operations

When you need to manipulate many files at once, this skill provides structured patterns for batch operations.

## Patterns

### Pattern 1: Batch Rename by Regex

For renaming multiple files matching a pattern:

```bash
# Example: rename all "FINAL" versions to remove suffix
find /path -name "*FINAL*" -type f | while read file; do
  newname="${file// FINAL/}"
  mv "$file" "$newname"
done
```

Think about:
- What pattern identifies the files? (extension, naming convention, date)
- What transformation do you want? (remove substring, add prefix, change case)
- Should you preview first? (use `ls` with the find pattern before renaming)

### Pattern 2: Organize Files by Type

To sort files into subdirectories by type/extension:

```bash
# Create subdirs and move files
for ext in jpg png txt pdf; do
  mkdir -p /dest/${ext}s
  find /source -maxdepth 1 -name "*.${ext}" -exec mv {} /dest/${ext}s/ \;
done
```

Think about:
- What's your organizing principle? (file type, date, name prefix, size)
- Do subdirs already exist or should you create them?
- Should you handle naming conflicts? (mv -i for interactive)

### Pattern 3: Find and Remove Duplicates

To identify and remove duplicate files:

```bash
# Using md5 to find duplicates
find /path -type f -exec md5 {} \; | sort | uniq -d -w 32 | while read hash rest; do
  find /path -type f -exec md5 {} \; | grep "^$hash" | awk '{$1=""; print $0}' | tail -n +2
done
# Review the output, then delete manually
```

Or use a deduplication tool:

```bash
# Install fdupes if needed: brew install fdupes
fdupes -r /path/to/duplicates
```

Think about:
- How to identify duplicates? (content hash, filename, size)
- Should you keep the first occurrence or the newest?
- Do you need a preview before deletion?

### Pattern 4: Move Files Matching Criteria

To move files based on conditions (size, date, name):

```bash
# Example: move all files older than 30 days to archive
find /source -mtime +30 -type f -exec mv {} /archive/ \;

# Example: move large files (>100MB) to external drive
find /source -size +100M -type f -exec mv {} /external/ \;
```

Think about:
- What's the matching criteria? (name pattern, size, date, extension)
- Is there a priority order? (process by size first, then date)
- Should you create destination directories first?

## Workflow

1. **Identify the scope** — Which files? How many? What's the pattern?
2. **Preview first** — Use `find` with `-ls` or `ls` to see what will change before running commands
3. **Dry run** — For destructive operations, use `echo` or create a script you can review
4. **Execute** — Run the operation, checking for errors
5. **Verify** — Confirm files are in the right place and none were lost

## Scripts

For repeated operations, save scripts in `~/.codex/scripts/`:

```bash
#!/bin/bash
# organize-downloads.sh
# Move files from Downloads to appropriate folders

cd ~/Downloads

# Movies
mkdir -p ~/Media/Videos
find . -maxdepth 1 \( -name "*.mp4" -o -name "*.mkv" -o -name "*.mov" \) -exec mv {} ~/Media/Videos/ \;

# Documents
mkdir -p ~/Documents/Archived
find . -maxdepth 1 \( -name "*.pdf" -o -name "*.docx" \) -exec mv {} ~/Documents/Archived/ \;
```

Make it executable: `chmod +x ~/.codex/scripts/organize-downloads.sh`

Then run: `bash ~/.codex/scripts/organize-downloads.sh`

## Common Pitfalls

- **Not previewing first** — Always `ls` or `find` before bulk operations
- **Assuming consistent naming** — Check for edge cases (spaces, special chars, mixed case)
- **Not preserving originals** — For critical operations, backup first
- **Permission issues** — Use `ls -ld` to check directory permissions before moving
- **Whitespace in filenames** — Quote variables: `"$file"` not `$file`
