---
name: notion-lookup
description: Instantly find Notion page IDs and URLs by name across your entire 3,500+ page workspace. Use this when you need to find a page, get its URL, or locate a database without opening Notion. Much faster than the Notion search API. Trigger whenever you need to reference a Notion page by name (e.g., "find my Travel page", "get the Database ID for Projects").
---

# Notion Lookup Skill

Look up Notion page IDs and URLs from the local workspace map.

## Instructions

1. Read the user's query to determine what page(s) they're looking for.
2. Use `Grep` to search `~/code-projects/notion/notion_map.json` for matching page names (case-insensitive). Do NOT load the entire file into context.
3. When you find matches, read just those lines (with a few lines of context) to extract the `name`, `id`, `type`, and `url` fields.
4. Return the matching results to the user.

## Example

User: "find my Travel page"

```
Grep pattern: "Travel" (case-insensitive) in ~/code-projects/notion/notion_map.json
```

Then read the matching entries and return:
- **Name:** Travel Planning
- **ID:** abc123...
- **URL:** https://www.notion.so/...

## Notes

- Always search case-insensitively
- If multiple matches, show all relevant ones
- Only fall back to the Notion MCP search API if the local map doesn't have what's needed

## Known Databases (skip lookup for these)

### Recipes Database

- **data_source_id**: `7eed774c-d1b9-4a3d-a640-d8a2c39b1904`
- **Parent database ID**: `148dc361ad2a440899224f33d4397fe0`
- Use `data_source_id` (not `page_url`) when calling `notion-create-pages` or searching within it

**Schema:** (select/multi_select option lists drift — re-fetch `notion-fetch(id="7eed774c-d1b9-4a3d-a640-d8a2c39b1904")` before writing properties rather than trusting this table)

| Property | Type | Notes |
|----------|------|-------|
| Recipe Name | title | |
| Dish Type | select | as of last check: "Food", "Drink", "Dessert" |
| Meal Type | multi_select | cuisine/course tags, e.g. "Seafood", "Middle Eastern", "Italian" |
| Key Ingredients | multi_select | closed enum (~26 ingredients) — not freeform, leave empty if nothing fits |
| Prep Time | number | minutes |
| Link | url | plain `Link`, no `userDefined:` prefix (that's only for properties named "id"/"url") |
| Rating | number | |
| Notes | text | |
| Fasting? | checkbox | `__YES__` / `__NO__` |
| To Make | checkbox | `__YES__` / `__NO__` |

**Two-column recipe page layout:**

```markdown
<columns>
<column>
# Ingredients {color="green_bg"}
---
- [ ] **ingredient** — quantity/note
</column>
<column>
# Instructions {color="green_bg"}
---
1. Numbered step
</column>
</columns>
```
