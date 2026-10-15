---
name: notebooklm-bulk-research
description: Gather source material for a large structured list of entities and add it to NotebookLM when the user requests bulk research.
---

# NotebookLM Scraper

Turns any structured list of entities into grouped `.txt` files ready for NotebookLM upload.

**Core pattern:**
1. Pull entity list + metadata (name, category/sector) from a structured source
2. Fetch full Wikipedia article text for each entity via the Wikipedia API
3. Group by category → one `.txt` file per group (NotebookLM's 50-source limit fits easily)
4. Cache everything — reruns are instant, even for 500+ entities

---

## Step 1: Clarify the Request

Ask (or infer from context) these four things before writing any code:

1. **What list?** (Fortune 500 CEOs, US Senators, Forbes Billionaires, Premier League managers, etc.)
2. **What Wikipedia subject per entity?** Usually the person's bio, but could be the company description, the country profile, etc.
3. **How to group?** Sector, political party, position, country, market cap quartile — whatever makes the most analytical sense for this list. Aim for 8–20 groups so NotebookLM gets meaningful chunks.
4. **Output folder?** Default: the current workspace's `outputs/<topic-slug>/` (use `work/` for intermediate files)

If the user gave a clear enough request (e.g., "Fortune 500 CEOs by sector"), go straight to Step 2 without asking.

---

## Step 2: Identify the Best Data Sources

### For the entity list + grouping metadata

Pick the cleanest structured source available. In priority order:

| Source type | How to access | When to use |
|---|---|---|
| Site with `__NEXT_DATA__` JSON | `urllib` fetch → `re.search(r'__NEXT_DATA__...')` → `json.loads` | fortune.com, many modern ranking sites |
| Wikipedia table | Wikipedia API wikitext → parse `\|-\n\|RANK\n\|[[COMPANY]]` rows | Wikipedia "List of..." articles |
| Wikipedia category | `action=query&list=categorymembers&cmtitle=Category:X` | When entities are tagged in a category |
| Static CSV on GitHub/data source | Direct urllib fetch of raw URL | Public datasets |

**fortune.com trick**: The main Fortune 500/1000 list page embeds all 1000 companies in `__NEXT_DATA__` — company name, rank, sector, and slug — in a single page load. Individual company pages embed CEO name in the same structure. This is the gold standard when it applies.

**Wikipedia "List of..." articles**: The table format is newline-separated cells (not `||`-separated):
```
|-
|1
|[[Walmart]]
|Retail
|...other columns...
```
Parse row by row: detect `|-`, collect subsequent `|cell` lines until next `|-`.

### For entity descriptions (Wikipedia bio text)

Always use the Wikipedia API with these exact params — learned from building the Fortune 500 scraper:

```python
# CORRECT: omit exintro entirely to get full article
params = {"action": "query", "prop": "extracts", "explaintext": True, "titles": name, "format": "json"}

# WRONG: exintro=False encodes as the string "False" which Wikipedia treats as truthy
# This silently returns only the intro paragraph (~200 chars instead of 5000+)
```

---

## Step 3: Write the Scraper Script

Generate a single self-contained Python file. **No external dependencies** — stdlib only (`urllib`, `json`, `re`, `time`, `pathlib`). This matters because the user will run it without any pip setup.

### Script structure

```python
#!/usr/bin/env python3
"""
<Topic> Scraper → NotebookLM
Usage:
    python scraper.py          # full run
    python scraper.py --test   # first 10 only
    python scraper.py --clear  # wipe cache and rerun
"""
# Standard sections:
# 1. Constants (BASE_DIR, CACHE_TTL, group mapping dict)
# 2. Cache helpers (cache_get / cache_put with 7-day TTL)
# 3. HTTP helpers (http_get for target site, wiki_get for Wikipedia API)
# 4. fetch_entity_list() → list of {name, group, metadata...}
# 5. get_entity_name_from_source() → the Wikipedia search term per entity
# 6. get_wikipedia_bio(name) → full plain-text article with name variants
# 7. write_output(group_data, gaps) → sector .txt files
# 8. main()
```

### Cache pattern

```python
CACHE_TTL = 7 * 86400

def cache_get(subdir, key):
    p = CACHE_DIR / subdir / f"{slugify(key)}.json"
    if p.exists():
        d = json.loads(p.read_text())
        if time.time() - d.get("_t", 0) < CACHE_TTL:
            return d
    return None

def cache_put(subdir, key, data):
    p = CACHE_DIR / subdir / f"{slugify(key)}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    data["_t"] = time.time()
    p.write_text(json.dumps(data, ensure_ascii=False))
```

### Wikipedia bio lookup — handle name mismatches

Fortune 500 lesson: fortune.com gives "Andrew R. Jassy" but Wikipedia has "Andy Jassy". Always try multiple name variants before giving up:

```python
def name_variants(name):
    variants = [name]
    no_middle = re.sub(r'\b[A-Z]\.\s+', '', name).strip()  # strip middle initial
    if no_middle != name:
        variants.append(no_middle)
    parts = no_middle.split()
    if len(parts) >= 2:
        variants.append(f"{parts[0]} {parts[-1]}")  # first + last only
    return variants

def get_wikipedia_bio(name):
    cached = cache_get("bios", name)
    if cached:
        return cached.get("bio", "")

    bio = ""
    tried = set()

    for variant in name_variants(name):
        if variant in tried: continue
        tried.add(variant)
        time.sleep(0.5)
        candidate = wiki_extract(variant)
        if len(candidate) > len(bio):
            bio = candidate
        if len(bio) >= 1000:
            break

    # Search fallback — finds nicknames (Andy vs Andrew, etc.)
    if len(bio) < 400:
        time.sleep(0.5)
        first_last = name_variants(name)[-1]
        alt = wiki_search_title(f"{first_last} biography")
        if alt and alt not in tried:
            time.sleep(0.5)
            candidate = wiki_extract(alt)
            if len(candidate) > len(bio):
                bio = candidate

    bio = re.sub(r'\n{3,}', '\n\n', bio).strip()
    cache_put("bios", name, {"bio": bio})
    return bio
```

### Rate limiting

```python
# Between fortune.com requests: time.sleep(0.6)
# Between Wikipedia API requests: time.sleep(0.5)
# User-Agent for Wikipedia: "ResearchScraper/1.0 (educational; <user email>)"
# User-Agent for other sites: realistic browser UA
```

### Output file format

```
<TOPIC> — <GROUP NAME>
<N> entries
================================================================================

================================================================================
ENTITY: <Name>  |  <Key Metadata>  |  Group: <Group>
================================================================================

<Full Wikipedia text>


```

---

## Step 4: Run It

```bash
# Always test first with 10 entries
python scraper.py --test

# If test looks good, run full
python scraper.py
```

Watch the output — it prints each entity as it processes. Common issues:
- **NO BIO**: Entity has no Wikipedia page. Expected for ~5–15% of entries. Logged to `gaps.txt`.
- **Short bio (<300 chars)**: Name mismatch. The search fallback usually catches this; if not, note it.
- **HTTP Error 404**: URL slug is wrong — check how the source formats slugs.

---

## Step 5: Report Results

After completion, report:
- Files created with entity count and size per group
- Total coverage (e.g., "496/500 bios captured")
- Notable gaps from `gaps.txt`
- Location of output folder

Then offer next steps:
- Expand to a larger list (Fortune 1000 instead of 500, etc.)
- Add more sources (S&P 500, global equivalents)
- Upload to NotebookLM using the `/notebooklm` skill

---

## Common Expansions

When the user asks to expand an existing scraper, the most common cases and their answers:

**Fortune 500 → Fortune 1000**: The fortune.com page already loads all 1000 in `__NEXT_DATA__`. Change the rank filter (`rank > 500` → `rank > 1000`), update the cache key (`"fortune500_list"` → `"fortune1000_list"` + raise threshold from 400 to 900), and update cosmetic strings. The URL, sector map, and output structure are all unchanged.

**Add a second source to an existing scraper**: Run the new source through its own `fetch_entity_list()` function, merge the results (dedupe by name), and pass to the same `get_wikipedia_bio()` and `write_output()` functions.

**Run large scrapes in the background**: For 500+ entities, use background execution so the user can do other things:
```bash
python scraper.py > output/run.log 2>&1 &
# Then monitor with:
tail -f output/run.log
```

---

## Reference Implementation

The Fortune 500 CEO scraper at `/Users/kerolowandy/code-projects/Not on Github/notebooklm-tools/fortune500-ceos/scraper.py` is the canonical example of this pattern. When this local file exists, read the relevant functions as an example — adapt the cache, rate-limiting, name-variant, and output-writing patterns to the current source rather than copying site selectors blindly. If that file is unavailable, build from the supported caching, rate-limiting, and coverage workflow above; no missing local example should block research. The main things that change per use case are:

1. The `fetch_entity_list()` function (different source URL and parsing)
2. The group/sector mapping dict
3. The entity → Wikipedia name mapping (if the source gives a different name format)
