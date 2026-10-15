---
name: notion-recipe-creator
description: >
  Parse a list of dishes from any source (YouTube transcript, webpage, text) and create
  structured recipe pages in the Notion Recipes database — with ingredients, instructions,
  properties, and a landscape cover photo from Google Images. Use when the user pastes a
  transcript, article, or dish list and wants recipe pages created in Notion.
---

# Notion Recipe Creator

Turns unstructured dish content (transcripts, articles, lists) into fully-formed Notion recipe
pages with cover photos. Wraps a workflow that otherwise takes ~40 tool calls into a repeatable
sequence.

## Recipes Database

- **data_source_id**: `7eed774c-d1b9-4a3d-a640-d8a2c39b1904` (stable — hardcoded is fine)
- **Ancestor DB ID**: `148dc361ad2a440899224f33d4397fe0`

**Property values drift — the select/multi_select options below are NOT hardcoded.** Before Step 2, fetch the live schema:

```
notion-fetch(id="7eed774c-d1b9-4a3d-a640-d8a2c39b1904")
```

Read the `<data-source-state>` schema block for the current option lists. As of the last check:
- `Dish Type` (single select): `Food`, `Drink`, `Dessert`
- `Meal Type` (multi_select): cuisine/course tags — `Seafood`, `Pasta`, `Soup`, `Southern`, `Middle Eastern`, `Italian`, `American`, `Breakfast`, `French`, `Indian`
- `Key Ingredients` (multi_select): a **closed enum** of ~26 specific ingredients (Salmon, Chicken, Rice, Heavy Cream, etc.) — not freeform tagging

Only pick from the options the live fetch returns. If nothing fits a dish well (e.g. an ingredient outside the enum), leave that field empty rather than forcing a mismatched or invented tag. Options change over time, so don't trust this list — always re-fetch.

## Browser runtime selection

Use the browser controls exposed and permitted in the current session. In the Codex Chrome extension, follow its `cua_repl` browser-instance selection and tab-claim instructions; read the returned API documentation and operate through supported snapshots, visible controls, screenshots, and navigation. For a referenced current tab, read `getTabContext` first when required. Do not launch a separate browser harness or run page scripts to bypass that runtime's restrictions.

The browser-harness scripts below are legacy implementation examples for sessions where that harness is explicitly available and permitted. In extension sessions, translate the workflow to the supported UI API instead of executing those scripts; refresh the visible state after transitions and read back saved changes.

## Source fidelity and duplicate prevention

Use the current connected Notion tools and their live schemas. Discover required capability/access prerequisites from the tool descriptions before searches or writes; illustrative tool names and property examples below do not override the live schema.

Before creating a recipe, fetch the Recipes database schema and query its actual `Link` property for the exact source URL. Reuse/update a matching page when that satisfies the request instead of creating a duplicate; if multiple matches or several dishes from one source exist, compare dish names and contents before deciding. Preserve the original source link.

Separate source-extracted ingredients/steps from adaptations. If the source lacks quantities or steps, label any added culinary guidance “Adapted recipe — quantities/steps added from culinary knowledge” in the page. Do not present inferred ratios or a visually identified dish as the creator's recipe. If the source cannot be read well enough to identify it, report that limitation instead of guessing.

## Step 1 — Extract the Dish List

Read the user's input and identify each distinct dish with:
- Name (as it should appear in Notion)
- Country/origin (if known)
- Key ingredients mentioned
- Any recipe details in the source

If the source is a transcript or article that describes recipes, extract what you can. Any gaps filled from culinary knowledge must be explicitly labeled as adaptations, as described above.

**Caption-less reels:** some Instagram reels carry no recipe text at all (caption is just a joke/hashtags, or a language mismatch). If `og:description` has no ingredients/steps, don't guess blind — watch the video:

```python
dur = js("(document.querySelector('video')||{}).duration || 0")
for t in [dur*0.2, dur*0.5, dur*0.85]:
    js(f"var v=document.querySelector('video'); v.pause(); v.currentTime={t};")
    import time; time.sleep(1)
    capture_screenshot()  # then Read the screenshot to see the frame
```

Identify the dish from what's visually happening (ingredients on the counter, technique, final plated shot), then write a clearly labeled adapted recipe from culinary knowledge if requested; keep observed source details distinct from added ratios and technique.

## Step 2 — Create the Pages

Use `notion-create-pages` with `data_source_id` (not `page_url`). Create all pages in a single call (batch up to 25).

**Properties to set per page** (values below are illustrative — always use the live-fetched option lists from the section above):

```json
{
  "Recipe Name": "French Jambon-Beurre",
  "Dish Type": "Food",
  "Meal Type": ["French"],
  "Key Ingredients": [],
  "Prep Time": 10,
  "Link": "https://...",
  "To Make": "__YES__"
}
```

**Page content — two-column layout:**

```markdown
<columns>
<column>
# Ingredients {color="green_bg"}
---
- [ ] **baguette** — 1 demi (about 30 cm)
- [ ] **unsalted butter** — 2 tbsp, softened
- [ ] **ham** — 4 slices good-quality jambon de Paris
- [ ] **flaky salt** — pinch
</column>
<column>
# Instructions {color="green_bg"}
---
1. Split baguette lengthwise, leaving a hinge.
2. Spread butter generously on both cut sides. Season with flaky salt.
3. Layer ham evenly across the bottom half.
4. Close, press lightly, slice in half. Serve immediately.
</column>
</columns>
```

Use your knowledge to write real quantities and proper technique — don't just copy the source verbatim.

## Step 3 — Add Cover Photos

For each page, find a landscape cover photo from Google Images.

**Search URL pattern:**
```python
goto_url(f"https://www.google.com/search?q={dish_name}+{dish_type}&tbm=isch&tbs=iar:w")
wait_for_load()
```

**Extract candidate URLs from script tags:**
```javascript
(function() {
    var results = [];
    var seen = {};
    document.querySelectorAll('script').forEach(function(s) {
        var p = /"(https:\/\/(?!encrypted-tbn)[^"]{40,}\.(jpg|jpeg|png|webp)[^"]*)"/g;
        var m;
        while ((m = p.exec(s.textContent)) !== null && results.length < 20) {
            var u = m[1];
            if (!seen[u] && u.indexOf('google') < 0 && u.indexOf('gstatic') < 0) {
                seen[u] = true;
                results.push(u);
            }
        }
    });
    return results;
})()
```

**Check dimensions (JPEG SOF marker parser):**
```python
import struct, urllib.request

def get_dims(url):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Referer': 'https://www.google.com/',
        })
        with urllib.request.urlopen(req, timeout=8) as r:
            data = r.read(131072)
        if data[:2] == b'\xff\xd8':
            i = 2
            while i + 4 < len(data):
                if data[i] != 0xff: break
                marker = data[i+1]
                if marker in (0xc0, 0xc1, 0xc2):
                    h, w = struct.unpack('>HH', data[i+5:i+9])
                    return w, h
                length = struct.unpack('>H', data[i+2:i+4])[0]
                i += 2 + length
        elif data[:8] == b'\x89PNG\r\n\x1a\n':
            return struct.unpack('>II', data[16:24])
    except:
        pass
    return None, None
```

**Selection criteria:**
- Ratio ≥ 1.3 (landscape)
- Prefer CDN hosts: Wikimedia, S3/Cloudinary, NYT, TripAdvisor CDN — they hotlink reliably
- Avoid `/wp-content/` square thumbnails (food blogs often 1:1 even in landscape search)
- When unsure between candidates, `capture_screenshot()` the search page and pick visually

Apply cover via `notion-update-page` with `cover` param alongside `update_properties`.

## Step 4 — Update Page IDs after Creation

`notion-create-pages` returns page IDs. Use them for cover updates — search is slower.

Batch cover updates: call `notion-update-page` in parallel (one call per page) in a single message.

## Step 5 — Verify the finished recipe

Fetch every final page after content, properties, and cover updates. Verify the title, exact source `Link`, live-schema property values, ingredient/step content, adaptation label when needed, and landscape cover URL. Resolve any missing component before claiming completion. Report the final page link and any source limitation.

## Efficiency Notes

- Pages: one `notion-create-pages` call for all dishes (up to 25)
- Properties + content: included in the create call — no separate update needed
- Cover photos: one browser harness session per dish (or batch if doing a loop), then parallel MCP update calls
- Total for 12 dishes: ~15 tool calls when batched correctly

## Common Gotchas

- Use `data_source_id` not `page_url` for the Recipes database — the MCP requires data source ID for databases with a single collection
- Set the `Link` property plain, no prefix — the `userDefined:` prefix only applies to properties literally named "id" or "url" (case-insensitive), and "Link" isn't either
- `tbs=iar:w` landscape filter still returns some square images — always verify with dimension check
- Google Images script-tag extraction must use an IIFE — bare `return` at top level throws SyntaxError in browser harness `js()`
- After page creation, record page IDs from the response — don't re-search for them
