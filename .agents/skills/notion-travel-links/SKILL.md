---
name: notion-travel-links
description: "Save travel content links (Instagram reels, YouTube shorts, websites) to Notion country/city travel pages. ALWAYS trigger when: (1) the user gives a country or destination name next to any URL or link, (2) the user says 'add this to [country]' or 'put this in [country]' with a link, (3) the user pastes a numbered/bulleted list where items have destination names and URLs, (4) the user says 'add these to notion' or 'save these' and there are destination+URL pairs, (5) a message has a bare URL right after a country/city name with no other explanation. Trigger even when phrased casually ('forgot to add this one', 'add these', 'these should go in my notion'). Do NOT trigger for: looking up page IDs, creating new country pages, adding database properties, or scraping/analyzing Instagram profiles without saving to Notion."
---

# Notion Travel Links

Adds Instagram/URL links as descriptive bullets inside the Notes section of Notion country travel pages.

## Browser runtime selection

Use the browser controls exposed and permitted in the current session. In the Codex Chrome extension, follow its `cua_repl` browser-instance selection and tab-claim instructions; read the returned API documentation and operate through supported snapshots, visible controls, screenshots, and navigation. For a referenced current tab, read `getTabContext` first when required. Do not launch a separate browser harness or run page scripts to bypass that runtime's restrictions.

The browser-harness scripts below are legacy implementation examples for sessions where that harness is explicitly available and permitted. In extension sessions, translate the workflow to the supported UI API instead of executing those scripts; refresh the visible state after transitions and read back saved changes.

## Input format

The user pastes destination + URL pairs in any format:
```
1. Batumi Georgia
   - https://www.instagram.com/reel/DZkudhjNcSo/...

2. Spain
   - https://www.instagram.com/reel/DZESO9DoG8c/...
```

## Step 1 — Parse the input

Extract every (label, URL) pair. Multiple URLs under one label each become separate bullets.

## Step 2 — Resolve Notion page IDs

For each unique destination, grep the local workspace map:
```bash
rg -i "DESTINATION" "$HOME/code-projects/notion/notion_map.json"
```

**Routing rules (apply before grepping):**
- "Canary Islands", "Lanzarote", "Tenerife", "Gran Canaria", "Fuerteventura", "Palma", "Palma de Mallorca", "Palma Mallorca", "Mallorca", "Ibiza", "Menorca" → **Spain** page `35593f98-a22d-42d7-86e5-63b9c55cc455`
- For destinations in the United States, resolve the specific state first (for example, "New Hampshire"), and prefer that state's page over the generic **United States** page whenever a matching state page exists in the Countries database. If no matching state page exists, fall back to **United States**.

**When grep returns multiple matches:**
- Prefer the page whose neighbors in the map are other country names (indicating it's in the Countries database under the Travel Dashboard)
- Prefer the more recently modified page (higher position in the file usually = more recent)
- If still ambiguous after these rules, ask the user which one

## Step 3 — Get descriptive titles from each URL

Read the source with the session's permitted browser controls and preserve its URL. In extension sessions, use `getTabContext`/`cua_repl` visible text or screenshots to derive the title; do not run metadata extraction scripts. The following metadata example applies only where a browser harness and page evaluation are explicitly supported.

```python
new_tab("https://www.instagram.com/reel/FIRST_URL/")
wait_for_load()
import time; time.sleep(3)
caption = js("(document.querySelector('meta[property=\"og:description\"]') || {}).content || ''")
```

From the `og:description`, distill a short descriptive title (≤12 words) that captures **what the content is actually about** — not the destination label the user used.

Good titles describe the specific content:
- "Maoshan Forest Night Rafting, Jiangsu" (not "China")
- "Bergpark Wilhelmshöhe Cascades, Kassel" (not "Germany")
- "Kayseri Yağlaması (TasteAtlas)" (not "Turkey")
- "Batumi — Dubai of Eastern Europe (60% Cheaper)" (not "Georgia")

If the caption is empty or uninformative, take a screenshot and read the visual content to name it.

## Step 4 — Fetch each Notion page

Call `notion-fetch` on each unique page ID. In the returned content, find the **last bullet point that appears before the first `<database` tag** — this is the anchor for insertion.

The Notes section is a list of bullets near the top of the page. The inline databases come after. The anchor is typically the last item in that bullet list.

## Step 5 — Insert bullets via update_content

For each Notion page, use `notion-update-page` with `command: update_content`.

If one page receives multiple new links, chain them all into a single update:

```json
{
  "page_id": "...",
  "command": "update_content",
  "content_updates": [
    {
      "old_str": "<exact text of last bullet>",
      "new_str": "<exact text of last bullet>\n- [Title A](url-a)\n- [Title B](url-b)"
    }
  ]
}
```

**Critical:** Never use `insert_content` with `position: end`. Country pages have inline databases after the Notes section — anything appended to the end lands below those databases, completely out of context.

## Step 6 — Report back

Fetch each updated page and verify the requested links are inside Notes before the inline databases, with no accidental duplicates. Then show a concise summary:

```
Added to 🇩🇪 Germany:
  • Top 12 German Desserts
  • Wilhelmshöhe Palace, Kassel

Added to 🇹🇷 Turkey:
  • Kayseri Yağlaması (TasteAtlas)
```
