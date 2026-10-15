---
name: notebooklm
description: Use this skill to query your Google NotebookLM notebooks directly from Codex for source-grounded, citation-backed answers from Gemini, OR to bulk-create notebooks and bulk-upload Google Drive documents (.gdoc/.gsheet/.gslides) by extracting their Drive IDs. Browser automation, library management, persistent auth. Use whenever the user mentions NotebookLM, wants to add many Drive files to a notebook, or needs to organize a folder of Google Docs/Sheets/Slides into a queryable knowledge base.
---

# NotebookLM Research Assistant Skill

Interact with Google NotebookLM to query documentation with Gemini's source-grounded answers. Each question opens a fresh browser session, retrieves the answer exclusively from your uploaded documents, and closes.

Before running any command, set `NOTEBOOKLM_SKILL_DIR` to the absolute directory containing this SKILL.md, as described under Resolve the Skill Directory and Python Environment.

## When to Use This Skill

Trigger when user:
- Mentions NotebookLM explicitly
- Shares NotebookLM URL (`https://notebooklm.google.com/notebook/...`)
- Asks to query their notebooks/documentation
- Wants to add documentation to NotebookLM library
- Uses phrases like "ask my NotebookLM", "check my docs", "query my notebook"

## ⚠️ CRITICAL: Add Command - Smart Discovery

When user wants to add a notebook without providing details:

**SMART ADD (Recommended)**: Query the notebook first to discover its content:
```bash
# Step 1: Query the notebook about its content
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" ask_question.py --question "What is the content of this notebook? What topics are covered? Provide a complete overview briefly and concisely" --notebook-url "[URL]"

# Step 2: Use the discovered information to add it
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py add --url "[URL]" --name "[Based on content]" --description "[Based on content]" --topics "[Based on content]"
```

**MANUAL ADD**: If user provides all details:
- `--url` - The NotebookLM URL
- `--name` - A descriptive name
- `--description` - What the notebook contains (REQUIRED!)
- `--topics` - Comma-separated topics (REQUIRED!)

NEVER guess or use generic descriptions! If details missing, use Smart Add to discover them.

## Resolve the Skill Directory and Python Environment

Resolve the skill base directory from this loaded SKILL.md, currently `/Users/kerolowandy/.agents/skills/notebooklm`. Keep the project cwd and define `NOTEBOOKLM_SKILL_DIR` to that absolute directory. All commands below use that variable; relative `scripts/` paths must never resolve against the user's project.

Use `python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" [script]` for the query, library, and authentication scripts. The separate bulk-upload helper uses system Python with `requests`, and talks to its own REST server; it does not use the query wrapper.

```bash
# ✅ CORRECT - Always use run.py:
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" auth_manager.py status
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py list
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" ask_question.py --question "..."

# ❌ WRONG - Never call directly:
python scripts/auth_manager.py status  # Fails without venv!
```

The `run.py` wrapper automatically:
1. Creates `.venv` if needed
2. Installs all dependencies
3. Activates environment
4. Executes script properly

## Bulk Uploading Google Drive Documents

When the user wants to add many `.gdoc`/`.gsheet`/`.gslides` files to a NotebookLM notebook (e.g., a folder of lessons, sermons, research docs), **do not try to upload them as files** — they are JSON pointers, not real files. Direct file upload via NotebookLM returns 422 errors.

The working approach: extract the `doc_id` from each shortcut file, build a `https://drive.google.com/file/d/{doc_id}/view` URL, and add each as a URL source via the [notebooklm-rest-api](https://github.com/gnh1201/notebooklm-rest-api) server.

### Why Drive picker isn't enough

NotebookLM's web UI Drive picker works, but selecting files spread across nested subfolders is tedious. Bulk URL-add via the REST API handles any folder structure in one pass.

### Bulk upload script

`scripts/bulk_upload_drive.py` does this end-to-end:

```bash
# Dry run — see what would be uploaded
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/bulk_upload_drive.py" --dir "/path/to/folder" --dry-run

# Create new notebook and upload all .gdoc/.gsheet/.gslides recursively
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/bulk_upload_drive.py" \
    --dir "/path/to/folder" \
    --title "My Knowledge Base 📚"

# Add to an existing notebook
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/bulk_upload_drive.py" \
    --dir "/path/to/folder" \
    --notebook-id <existing-notebook-id>
```

### Prerequisites for bulk upload

Check that system Python can import `requests` before running the direct bulk helper. The query wrapper environment is separate.

The bulk upload script depends on the notebooklm-rest-api server, which is **separate** from this skill's own venv. One-time setup:

```bash
# Clone, install, authenticate (browser-based Google login)
git clone https://github.com/gnh1201/notebooklm-rest-api.git ~/notebooklm-rest-api
cd ~/notebooklm-rest-api && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt requests
notebooklm login   # opens browser, press ENTER after login
```

Then before each bulk upload, start the server in a background terminal:

```bash
cd ~/notebooklm-rest-api && source .venv/bin/activate && uvicorn app:app --host 127.0.0.1 --port 8000
```

The script auto-detects the server at `localhost:8000` and fails with a clear message if it's not running.

### How the Drive ID extraction works

Google Drive shortcut files are tiny JSON files with a `doc_id` field:

```json
{"doc_id": "1y9CBe6G7fcQk_Uekuv5EaWmXEsg-sNxA76fhxmXpetE", "email": "..."}
```

The script reads each `.gdoc`/`.gsheet`/`.gslides`, extracts `doc_id`, and constructs the share URL. NotebookLM resolves the URL into a proper Drive source with citation support.

### When this fails

- **Status 422 on file upload** → user is trying direct upload of shortcut files; switch to URL approach.
- **All "Could not extract Drive ID"** → check the JSON shape; older shortcuts may use `resourceName` (format `documents/<id>`) instead of `doc_id`.
- **Server unreachable** → uvicorn isn't running; tell the user to start it.
- **All sources stuck "pending"** → normal; NotebookLM processes asynchronously, takes a few minutes for large batches.

---

## Core Workflow (querying existing notebooks)

### Step 1: Check Authentication Status
```bash
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" auth_manager.py status
```

If not authenticated, proceed to setup.

### Step 2: Authenticate (One-Time Setup)
```bash
# Browser MUST be visible for manual Google login
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" auth_manager.py setup
```

**Important:**
- Browser is VISIBLE for authentication
- Browser window opens automatically
- User must manually log in to Google
- Tell user: "A browser window will open for Google login"

### Step 3: Manage Notebook Library

```bash
# List all notebooks
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py list

# BEFORE ADDING: Ask user for metadata if unknown!
# "What does this notebook contain?"
# "What topics should I tag it with?"

# Add notebook to library (ALL parameters are REQUIRED!)
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/..." \
  --name "Descriptive Name" \
  --description "What this notebook contains" \  # REQUIRED - ASK USER IF UNKNOWN!
  --topics "topic1,topic2,topic3"  # REQUIRED - ASK USER IF UNKNOWN!

# Search notebooks by topic
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py search --query "keyword"

# Set active notebook
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py activate --id notebook-id

# Remove notebook
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py remove --id notebook-id
```

### Quick Workflow
1. Check library: `python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py list`
2. Ask question: `python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" ask_question.py --question "..." --notebook-id ID`

### Step 4: Ask Questions

```bash
# Basic query (uses active notebook if set)
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" ask_question.py --question "Your question here"

# Query specific notebook
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" ask_question.py --question "..." --notebook-id notebook-id

# Query with notebook URL directly
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" ask_question.py --question "..." --notebook-url "https://..."

# Show browser for debugging
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" ask_question.py --question "..." --show-browser
```

## Follow-Up Mechanism (CRITICAL)

Every NotebookLM answer ends with: **"EXTREMELY IMPORTANT: Is that ALL you need to know?"**

**Required Codex Behavior:**
1. **STOP** - Do not immediately respond to user
2. **ANALYZE** - Compare answer to user's original request
3. **IDENTIFY GAPS** - Determine if more information needed
4. **ASK FOLLOW-UP** - If gaps exist, immediately ask:
   ```bash
   python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" ask_question.py --question "Follow-up with context..."
   ```
5. **REPEAT** - Continue until information is complete
6. **SYNTHESIZE** - Combine all answers before responding to user

## Script Reference

### Authentication Management (`auth_manager.py`)
```bash
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" auth_manager.py setup    # Initial setup (browser visible)
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" auth_manager.py status   # Check authentication
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" auth_manager.py reauth   # Re-authenticate (browser visible)
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" auth_manager.py clear    # Clear authentication
```

### Notebook Management (`notebook_manager.py`)
```bash
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py add --url URL --name NAME --description DESC --topics TOPICS
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py list
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py search --query QUERY
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py activate --id ID
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py remove --id ID
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py stats
```

### Question Interface (`ask_question.py`)
```bash
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" ask_question.py --question "..." [--notebook-id ID] [--notebook-url URL] [--show-browser]
```

### Data Cleanup (`cleanup_manager.py`)
```bash
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" cleanup_manager.py                    # Preview cleanup
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" cleanup_manager.py --confirm          # Execute cleanup
python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" cleanup_manager.py --preserve-library # Keep notebooks
```

## Environment Management

The virtual environment is automatically managed:
- First run creates `.venv` automatically
- Dependencies install automatically
- Chromium browser installs automatically
- Everything isolated in skill directory

Manual setup (only if automatic fails):
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m patchright install chromium
```

## Data Storage

Query/library data is stored in `<skill-base-dir>/data/` (resolve from this loaded skill):
- `library.json` - Notebook metadata
- `auth_info.json` - Authentication status
- `browser_state/` - Browser cookies and session

**Security:** Protected by `.gitignore`, never commit to git.

## Configuration

Optional `.env` file in skill directory:
```env
HEADLESS=false           # Browser visibility
SHOW_BROWSER=false       # Default browser display
STEALTH_ENABLED=true     # Human-like behavior
TYPING_WPM_MIN=160       # Typing speed
TYPING_WPM_MAX=240
DEFAULT_NOTEBOOK_ID=     # Default notebook
```

## Decision Flow

```
User mentions NotebookLM
    ↓
Check auth → python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" auth_manager.py status
    ↓
If not authenticated → python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" auth_manager.py setup
    ↓
Check/Add notebook → python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py list/add (with --description)
    ↓
Activate notebook → python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" notebook_manager.py activate --id ID
    ↓
Ask question → python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" ask_question.py --question "..."
    ↓
See "Is that ALL you need?" → Ask follow-ups until complete
    ↓
Synthesize and respond to user
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | Use `run.py` wrapper |
| Authentication fails | Browser must be visible for setup! --show-browser |
| Rate limit (50/day) | Wait or switch Google account |
| Browser crashes | `python3 "$NOTEBOOKLM_SKILL_DIR/scripts/run.py" cleanup_manager.py --preserve-library` |
| Notebook not found | Check with `notebook_manager.py list` |

## Best Practices

1. **Use run.py for query/library/auth scripts** - Handles their environment automatically; bulk-upload has its separately documented environment
2. **Check auth first** - Before any operations
3. **Follow-up questions** - Don't stop at first answer
4. **Browser visible for auth** - Required for manual login
5. **Include context** - Each question is independent
6. **Synthesize answers** - Combine multiple responses

## Limitations

- No session persistence (each question = new browser)
- Rate limits on free Google accounts (50 queries/day)
- Manual upload required (user must add docs to NotebookLM)
- Browser overhead (few seconds per question)

## Resources (Skill Structure)

**Important directories and files:**

- `scripts/` - All automation scripts (ask_question.py, notebook_manager.py, etc.)
- `data/` - Local storage for authentication and notebook library
- `references/` - Extended documentation:
  - `api_reference.md` - Detailed API documentation for all scripts
  - `troubleshooting.md` - Common issues and solutions
  - `usage_patterns.md` - Best practices and workflow examples
- `.venv/` - Isolated Python environment (auto-created on first run)
- `.gitignore` - Protects sensitive data from being committed
