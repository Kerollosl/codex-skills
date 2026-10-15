---
name: instagram-post-scraper
description: >
  Bulk-scrape every tagged account, place, or business from any Instagram profile
  using the live Chrome session + Instagram's internal feed API (no clicking each
  post). Use whenever the user wants to extract a list from an Instagram account —
  restaurants from a food blogger, venues from a travel account, brands from an
  influencer, shops from a style account (e.g. "scrape all places from @nova_nomz",
  "get every restaurant that account has tagged", "pull all the brands mentioned by X").
  Output: categorized .txt files (food/places vs. everything else).
---

# Instagram Account Scraper

Scrapes all tagged businesses from an Instagram profile using the **internal feed API**
via a supported authenticated browser session. The internal-feed implementation below requires a permitted harness; restricted UI sessions use the separate route below.

## Browser runtime selection

Use the browser controls exposed and permitted in the current session. In the Codex Chrome extension, follow its `cua_repl` browser-instance selection and tab-claim instructions; read the returned API documentation and operate through supported snapshots, visible controls, screenshots, and navigation. For a referenced current tab, read `getTabContext` first when required. Do not launch a separate browser harness or run page scripts to bypass that runtime's restrictions.

The browser-harness scripts below are legacy implementation examples for sessions where that harness is explicitly available and permitted. In extension sessions, translate the workflow to the supported UI API instead of executing those scripts; refresh the visible state after transitions and read back saved changes.

### Bulk extraction in restricted UI sessions

The internal-feed scripts require authenticated page evaluation and network access through a supported harness. If the current runtime does not permit those operations, do not run internal API fetches, extract cookies, or attach another runtime to Chrome. Use the visible profile/posts to collect tagged accounts through supported UI controls, including pagination/scrolling, when feasible. Report the number of posts actually inspected and any coverage gap; do not label a partial UI collection “every post.” If full coverage requires a supported scraper session unavailable here, state that limitation and provide the concrete remaining step.

## Why Not urllib?

Instagram blocks unauthenticated requests. The internal API (`/api/v1/feed/user/…`)
requires session cookies — browser-harness's `js()` helper runs inside the live Chrome
tab, so cookies are included automatically.

## Why Tagged Accounts (Not Captions)?

Caption text is free-form and rarely names the restaurant in a parseable way.
`usertags` in each post item gives structured data: `full_name` (e.g. "Hanabi Ramen")
and `username` (e.g. "hanabi_ramen") for every tagged account. Far more reliable than
regex on captions.

---

## Step 1 — Navigate to the Profile

```python
browser-harness <<'PY'
import time
goto_url("https://www.instagram.com/<handle>/")
wait_for_load()
time.sleep(2)
PY
```

## Step 2 — Extract User ID

```python
user_id = js("""
  const scripts = document.querySelectorAll('script[type="application/json"]');
  for (const s of scripts) {
    try {
      const str = JSON.stringify(JSON.parse(s.textContent));
      const match = str.match(/"pk":"(\\d+)"/);
      if (match) return match[1];
    } catch(e) {}
  }
  const html = document.documentElement.innerHTML;
  const m = html.match(/"profilePage_(\\d+)"/);
  if (m) return m[1];
  const m2 = html.match(/"id":"(\\d{5,})"/);
  return m2 ? m2[1] : null;
""")
print("User ID:", user_id)
```

## Step 3 — Paginate the Feed API

```python
import json, time

all_items = []
next_max_id = None

while True:
    url = f'/api/v1/feed/user/{user_id}/?count=50'
    if next_max_id:
        url += f'&max_id={next_max_id}'

    result = js(f"""
      return (async () => {{
        const resp = await fetch('{url}', {{
          headers: {{
            'x-ig-app-id': '936619743392459',
            'x-requested-with': 'XMLHttpRequest'
          }}
        }});
        return await resp.json();
      }})();
    """)

    items = result.get('items') or []

    for item in items:
        location = (item.get('location') or {}).get('name', '')
        usertags = list((item.get('usertags') or {}).get('in') or [])

        # Also check carousel slides
        for c in (item.get('carousel_media') or []):
            usertags += list((c.get('usertags') or {}).get('in') or [])

        tagged = []
        for tag in usertags:
            u = tag.get('user') or {}
            tagged.append({
                'username': u.get('username', ''),
                'full_name': u.get('full_name', '')
            })

        all_items.append({'location': location, 'tagged': tagged})

    if not result.get('more_available') or not result.get('next_max_id'):
        break
    next_max_id = result['next_max_id']
    time.sleep(0.4)   # avoid rate limiting

print(f"Total posts: {len(all_items)}")
```

### IMPORTANT: async IIFE required for fetch

`js()` does not support bare `await`. Always wrap in `(async () => { ... })()` and
`return` the result. Bare `await fetch(...)` raises `SyntaxError: await is only valid
in async functions`.

---

## Step 4 — Extract & Deduplicate Tagged Places

```python
seen = set()
places = []

for item in all_items:
    for t in item['tagged']:
        username = t['username']
        full_name = t['full_name'].strip()
        if not full_name or username in seen:
            continue
        seen.add(username)
        places.append({
            'name': full_name,
            'instagram': f'@{username}',
            'location': item['location']
        })

places.sort(key=lambda x: x['name'].lower())
print(f"Unique tagged places: {len(places)}")
```

---

## Step 5 — Split Food vs. Everything Else

Filtering heuristic — adjust keyword lists for the account's focus area:

```python
FOOD_EXCLUDE_KEYWORDS = [
    'museum', 'park', 'farm park', 'credit union', 'jewelry', 'festival', 'fair',
    'yoga', 'spa', 'hotel', 'inn', 'resort', 'college', 'university',
    'zoo', 'aquarium', 'theater', 'theatre', 'cinema', 'arcade',
    'boathouse', 'marina', 'cruise', 'flight', 'balloon',
    'market', 'markt', 'flea', 'vintage', 'shopping', 'mall',
    'garden', 'botanical', 'cemetery', 'library', 'gallery',
    'magazine', 'association', 'candle', 'florist', 'floral', 'piano', 'music',
    'orchard', 'vineyard', 'winery', 'brewing', 'cellars',
    'transit', 'metro ', 'wmata',
    'pinball', 'swingers', 'drive-in',
]

EXCLUDE_ACCOUNT_TYPES = {
    # tourism boards, government accounts, media, personal chefs, event pop-ups
    # add specific usernames to always skip
}

restaurants = []
other = []

for p in places:
    username = p['instagram'].lstrip('@')
    full_lower = p['name'].lower()

    if username in EXCLUDE_ACCOUNT_TYPES:
        other.append(p)
        continue

    if any(kw in full_lower or kw in username.lower() for kw in FOOD_EXCLUDE_KEYWORDS):
        other.append(p)
    else:
        restaurants.append(p)

print(f"Food: {len(restaurants)}  |  Other: {len(other)}")
```

---

## Step 6 — Write Output Files

```python
def write_txt(path, entries, title):
    lines = [title, '=' * 50, '']
    for e in sorted(entries, key=lambda x: x['name'].lower()):
        loc = f" — {e['location']}" if e['location'] else ''
        lines.append(f"{e['name']}{loc}")
    with open(path, 'w') as f:
        f.write('\n'.join(lines))

write_txt('/tmp/<handle>_restaurants.txt', restaurants,
          f'@<handle> Restaurants & Food Places ({len(restaurants)})')
write_txt('/tmp/<handle>_other.txt', other,
          f'@<handle> Everything Else ({len(other)})')

print("Done.")
```

---

## Full Single-Script Template

```python
browser-harness <<'PY'
import json, time

HANDLE = "nova_nomz"   # change this

# -- navigate & get user_id --
goto_url(f"https://www.instagram.com/{HANDLE}/")
wait_for_load()
time.sleep(2)

user_id = js("""
  const scripts = document.querySelectorAll('script[type="application/json"]');
  for (const s of scripts) {
    try {
      const str = JSON.stringify(JSON.parse(s.textContent));
      const m = str.match(/"pk":"(\\d+)"/);
      if (m) return m[1];
    } catch(e) {}
  }
  const html = document.documentElement.innerHTML;
  const m2 = html.match(/"profilePage_(\\d+)"/);
  if (m2) return m2[1];
  const m3 = html.match(/"id":"(\\d{5,})"/);
  return m3 ? m3[1] : null;
""")
assert user_id, "Could not find user_id — make sure you're logged into Instagram"
print(f"User ID: {user_id}")

# -- paginate feed --
all_items = []
next_max_id = None
page = 0
while True:
    url = f'/api/v1/feed/user/{user_id}/?count=50'
    if next_max_id:
        url += f'&max_id={next_max_id}'
    result = js(f"""
      return (async () => {{
        const resp = await fetch('{url}', {{
          headers: {{'x-ig-app-id': '936619743392459', 'x-requested-with': 'XMLHttpRequest'}}
        }});
        return await resp.json();
      }})();
    """)
    items = result.get('items') or []
    page += 1
    print(f"  page {page}: {len(items)} posts")
    for item in items:
        location = (item.get('location') or {}).get('name', '')
        usertags = list((item.get('usertags') or {}).get('in') or [])
        for c in (item.get('carousel_media') or []):
            usertags += list((c.get('usertags') or {}).get('in') or [])
        tagged = [{'username': (t.get('user') or {}).get('username',''),
                   'full_name': (t.get('user') or {}).get('full_name','')}
                  for t in usertags]
        all_items.append({'location': location, 'tagged': tagged})
    if not result.get('more_available') or not result.get('next_max_id'):
        break
    next_max_id = result['next_max_id']
    time.sleep(0.4)

print(f"Total posts scraped: {len(all_items)}")

# -- deduplicate --
seen = set()
places = []
for item in all_items:
    for t in item['tagged']:
        u, n = t['username'], t['full_name'].strip()
        if not n or u in seen: continue
        seen.add(u)
        places.append({'name': n, 'instagram': f'@{u}', 'location': item['location']})

print(f"Unique tagged places: {len(places)}")

with open(f'/tmp/{HANDLE}_all.json', 'w') as f:
    json.dump(places, f, indent=2)
print(f"Saved raw data to /tmp/{HANDLE}_all.json")
PY
```

Then run the split + write step in a separate Python call with your filter lists.

---

## Known Gotchas

- **`await` outside async** → always use `(async () => { return await fetch(...); })()`
- **Null guards** — `item.get('usertags')` can be `None`, not `{}`. Use `or {}` everywhere.
- **Carousel posts** — usertags live on each slide, not the parent item. Always check `carousel_media`.
- **Rate limiting** — `time.sleep(0.4)` between pages is enough at 50 items/page. Don't remove it.
- **user_id extraction** — the `"pk":"..."` pattern in JSON script tags is most reliable; the `profilePage_` pattern is a fallback for older page formats.
- **Not all posts have usertags** — posts tagging no accounts just contribute empty lists; that's fine.
- **Instagram app ID** — `936619743392459` is Instagram's stable web app ID. It's public and unchanged for years.
