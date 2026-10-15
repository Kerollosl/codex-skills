---
name: todoist-router
description: >
  Route Todoist inbox tasks through sibling routes.yaml, present a concrete approval
  plan, then execute authorized actions through available connected services or the
  todoist-api CLI. Use /todoist-router with an optional task filter or --dry-run.
---

# Task Router

Cross-app task execution with a mandatory approval gate. Every run shows a full plan table — nothing executes until you say yes.

## Tools Available

- Use the available Todoist connector, or the `todoist-api` skill's `td` CLI when no connector supports the operation.
- Use available Notion, Google Drive, and Google Calendar connectors; discover their current tool schemas rather than assuming legacy tool names.
- Use osascript for Apple Notes when authorized and available.
- Read PROJECT-MAP.md, sibling routes.yaml, and the required project source files.
- Execution mode describes the supported workflow; it never expands user authorization. Preserve existing approvals for the same concrete actions.

---

## Step 1 — Read Routes Config

Before fetching any tasks, read the routes config:

```
<skill-base-dir>/routes.yaml
```

Resolve `<skill-base-dir>` to the directory containing this loaded SKILL.md (currently `/Users/kerolowandy/.agents/skills/todoist-task-router`); it is independent of the project cwd. Read `routes.yaml` there. Load all routes into memory. Each route has: `id`, `name`, `keywords`, `target_type`, `target_id`, `target_url`, `execution` (auto/semi/manual), `notes`.

Also read `~/code-projects/PROJECT-MAP.md` so you have full project context for code task routing.

---

## Step 2 — Fetch Tasks

Default: fetch all tasks from the Todoist inbox:
```
find-tasks → projectId: "inbox", limit: 100
```

If the user passed an argument:
- A filter string (e.g. "today", "overdue") → use as `filter` parameter
- A specific task description → search for that task
- `--dry-run` → run full classification but skip execution step

---

## Step 3 — Classify Each Task + Detect Consolidations

### 3a — Classify

For each task, match it against routes.yaml using this logic:

1. **Keyword scan**: check task `content` and `description` against each route's `keywords` list (case-insensitive, partial match allowed)
2. **Context reasoning**: use Codex's judgment — a task saying "Yummy bowl and golden corral" has no keyword "restaurant" but is clearly restaurants → Beli
3. **Strongest match wins**: if multiple routes match, pick the one with the most signals
4. **Ambiguous**: if two routes are nearly equal confidence, note both and ask user in the approval table
5. **No match**: flag as `unrouted` — never silently drop a task

Extract from each task:
- The **destination** (route id + name)
- The **formatted entry** (what will actually be added to the target — cleaned up, not raw task text)
- The **execution type** (auto / semi / manual)
- Any **ambiguity** worth noting

### 3b — Detect Consolidation Opportunities

After classifying all tasks, scan for these patterns and flag each as a consolidation suggestion:

**Pattern 1 — Same destination, multiple tasks**
Multiple tasks routing to the same target → suggest batching their execution. For Beli: combine into one open-app session. For Sheets: add all rows in one visit. Don't necessarily merge the Todoist tasks unless they're truly about the same thing.

**Pattern 2 — Near-duplicates**
Two tasks with essentially the same meaning (e.g., "Email zumigo back" + "Follow up with zumigo") → suggest merging into one task in Todoist to reduce clutter.

**Pattern 3 — Sub-items of a theme**
Several tasks that are clearly fragments of a bigger project or action (e.g., "Buy groceries", "Pick up dry cleaning", "Call doctor" — all errands) → suggest optionally grouping them as subtasks under a parent task.

**Pattern 4 — Multi-item tasks that should be split**
A single task listing multiple distinct things (e.g., "Yummy bowl and golden corral" = 2 restaurants) → flag that the routing will handle them as separate items even though they're one task. Ask if user wants to split the Todoist task too.

Only suggest consolidations where the benefit is clear. Don't force groupings that fragment natural meaning.

### 3c — Assign Friction Scores

After classifying all tasks, score each routed task on this scale. Lower = less friction = appears first in the plan:

| Score | Execution | Target type | Why |
|-------|-----------|-------------|-----|
| 1 | auto | todoist_section | Single API call, instant, zero follow-up |
| 2 | auto | apple_notes | osascript append, ~2s, auto-verified |
| 3 | auto | notion_db | One MCP call, no user action needed |
| 4 | auto | google_calendar | MCP call + date parse, auto-confirmed |
| 5 | semi | google_doc | Open doc, paste one line |
| 6 | semi | google_sheet | Open sheet, find right column/row, paste |
| 7 | manual | beli | Open phone app, search, tap × N restaurants |
| 8 | semi | code_project | Read files, edit code, git diff, push |
| 9 | — | unrouted | Decision needed before anything can happen |

**Tiebreaker within the same score:** shorter task content (fewer words) comes first — it's usually quicker to process.

Sort all tasks by this score before building the plan table. Do NOT group by auto/semi/manual — show one unified list in friction order, with a tag on each item showing its execution type.

---

## Step 4 — Show Approval Table (MANDATORY — never skip this)

Always show the full plan before executing anything. Consolidation suggestions come first so you can clean up before routing. Tasks are listed in friction order (1 = instant, 9 = most work) — this is also the order they will be reordered to in Todoist after approval.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋  TASK ROUTER PLAN  —  [N] tasks, [X] routed, [Y] unrouted
     Ordered: least friction → most friction
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗  CONSOLIDATION SUGGESTIONS  (optional — clean up inbox first)
─────────────────────────────────────────────────
 C1. MERGE (near-duplicates):
     "Email zumigo back"  +  "Shield AI"
     → Both are work follow-ups going to the Work section
     → Combine into: "Work follow-ups: Email Zumigo, look into Shield AI"
     → Deletes task 2, updates task 1 in Todoist

 C2. BATCH (same destination):
     3 tasks → Beli (restaurants)
     → Will be handled as one Beli session (open once, add all 3)
     → No Todoist merge needed — just good to know

 C3. SPLIT SUGGESTION:
     "Yummy bowl and golden corral" contains 2 restaurants
     → Routing both to Beli regardless, but want to split into 2 Todoist tasks?

Apply consolidations? [yes / no / pick C1,C3]
─────────────────────────────────────────────────

📋  ROUTING PLAN  (friction order — Todoist will be reordered to match)
─────────────────────────────────────────────────
 1. [AUTO] "[task content]"
    → [Destination name]
    → Entry: "[formatted entry that will be added]"

 2. [AUTO] "[task content]"
    → [Destination name]
    → Entry: "[formatted entry]"

 3. [SEMI] "[task content]"
    → [Sheet/Doc name]  [direct link]
    → Add to [column/section]: "[exact text to paste]"

 4. [MANUAL] "[task content]"
    → Beli
    → Open Beli → tap + → Search "[restaurant]" → Save to Wishlist

 5. [UNROUTED] "[task content]"
    → No route matched. Options: skip / tell me where this goes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Approve all? Type:
  yes           → execute everything above + reorder Todoist to match
  skip [N,N]   → approve all except items N and N
  only [N,N]   → only execute items N and N
  cancel        → abort
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Wait for the user's response before proceeding.

---

## Consolidation Execution (Todoist)

When the user approves a consolidation, execute it before the routing step.

### Merge (near-duplicates)
1. Call `update-tasks` on the task to KEEP — update its `content` to the merged text
2. Call `delete-object` on the task(s) being removed (use the Todoist task ID)
3. Proceed to route the surviving merged task

### Split (one task → multiple)
1. Call `update-tasks` on the original task — set its content to item 1
2. Call `add-tasks` to create a new task with item 2 (and item 3, etc.), same section/project
3. Proceed to route all resulting tasks

### Group as subtasks (theme grouping)
1. Keep the parent task as-is (or update its content to be a clear parent title)
2. Call `update-tasks` on each subtask with `parentId` set to the parent task's ID
3. Subtasks are then routed individually

Never delete a task without showing the user what's being removed in the approval table.

---

## Step 5 — Execute Approved Actions

### 5a — Reorder Todoist Tasks First (always do this before routing)

Before executing any routing, physically reorder the Todoist inbox tasks to match the friction-sorted plan order. This ensures the inbox reflects the priority order even if you don't complete every task right now.

1. Load the `reorder-objects` tool via ToolSearch if not already loaded
2. Call `reorder-objects` with the task IDs in friction-sorted plan order (item 1 first, last item last)
3. Include ALL tasks shown in the plan (routed + unrouted) so the full inbox is reordered, not just the routed subset
4. Confirm the reorder succeeded before proceeding to routing execution

```
reorder-objects:
  - type: task
  - items: [{ id: "<task_id_1>", childOrder: 0 }, { id: "<task_id_2>", childOrder: 1 }, ...]
```

After reordering, proceed with routing execution in the same friction order.

### 5b — Route Each Task

Process in friction order (lowest score first). Show a checkmark as each completes.

### Apple Notes Adapter (auto)

```bash
osascript <<'EOF'
tell application "Notes"
  tell account "iCloud"
    set n to note "[NOTE_NAME]"
    set body of n to (body of n) & "<br>• [ENTRY]"
  end tell
end tell
EOF
```

Replace `[NOTE_NAME]` with the `target_id` from routes.yaml. Replace `[ENTRY]` with the formatted entry.

After writing, verify with a read-back:
```bash
osascript -e 'tell application "Notes" to tell account "iCloud" to get body of note "[NOTE_NAME]"'
```
Confirm the new entry appears.

### Notion Database Adapter (auto)

Inspect the destination database and live schema with the available Notion connector. Resolve its current data source ID and create pages with `data_source_id` when the tool requires it; do not substitute a collection URL for an ID. Populate:
- `Places` property (title) = location or place name
- `Notes` property = any additional context from the task description
- Leave relation fields (`Country (Manual)`, `Trip`) empty

### Google Calendar Adapter (auto)

Parse the task for:
- Event title (clean up the task text)
- Date and time (if mentioned; default to all-day if no time)
- Duration (default 1 hour if timed)

Use `create_event` MCP tool. Confirm the event URL in the completion report.

### Todoist Section Move Adapter (auto)

Use `update-tasks` with:
- `taskId` = the task's Todoist ID
- `sectionId` = the section ID from routes.yaml `target_id`

### Google Sheets / Docs Adapter (semi)

1. Call `read_file_content` with the `target_id` (file ID) to understand the current structure (columns, last row, etc.)
2. Determine the exact cell/row/column where the new entry belongs
3. Output:
   ```
   ✅ Ready to add to [Sheet Name]:
   → Open: [target_url]
   → [Specific instruction: "Add to column B, next empty row:" / "Add under [header]:"]
   → Copy: [exact text or row data]
   ```
4. Mark the task as "action needed" in the completion report — user must complete this manually

### Beli Adapter (manual)

Extract all restaurant/place names from the task. Output:
```
📌 Beli — add these manually:
  1. Open Beli app → tap + (bottom center)
  2. Search "[Restaurant 1]" → tap Save to Wishlist
  3. Search "[Restaurant 2]" → tap Save to Wishlist
  (repeat for each)
```

### Code Project Adapter (semi)

1. Match the task to a project using `~/code-projects/PROJECT-MAP.md`
2. Read the relevant source files in that project
3. Make the code change (use Edit/Write tools)
4. Output:
   ```
   ✅ Code updated in ~/code-projects/[repo]/[file]:
   → Review with: git diff
   → Push when ready: git push
   ```
5. Do NOT push automatically. Mark as "action needed" in completion report.

---

## Step 6 — Completion Report

After all actions are done, output:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅  DONE — mark these complete in Todoist:
─────────────────────────────────────────────────
  • "[task]" → added to Apple Notes
  • "[task]" → added to Notion Places
  • "[task]" → moved to Work section

📋  ACTION NEEDED — complete these, then mark done:
─────────────────────────────────────────────────
  • "[task]" → paste row into Movies sheet [link]
  • "[task]" → add to Beli manually (instructions above)
  • "[task]" → git push ~/code-projects/[repo]

⚠️   SKIPPED / UNROUTED:
─────────────────────────────────────────────────
  • "[task]" → no route matched, still in inbox
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Do NOT mark tasks complete in Todoist automatically. Let the user decide.

---

## Extending Routes

Tell the user: to add a new destination, edit `<skill-base-dir>/routes.yaml` and append a new route block. The skill reads this file fresh every run — no changes to SKILL.md needed.

Template:
```yaml
  - id: my_new_route
    name: "Human-readable name"
    keywords:
      - keyword1
      - keyword2
    target_type: google_sheet  # or: apple_notes | notion_db | google_calendar | todoist_section | google_doc | beli | code_project
    target_id: "file-id-or-collection-url-or-section-id"
    target_url: "https://..."  # direct edit link (for semi-auto targets)
    execution: semi            # auto | semi | manual
    notes: >
      Any context Codex should use when routing here and formatting entries.
```
