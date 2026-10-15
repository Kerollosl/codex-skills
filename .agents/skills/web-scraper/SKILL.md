---
name: web-scraper
description: Extract structured public web data with lightweight HTTP parsing when no connector or browser interaction is needed.
---

# Web Scraper Pattern

Lightweight web scraping with `urllib` (stdlib only). No Playwright, no Selenium, no extra deps.
Best for: sites that server-render their key data into the HTML. Doesn't work for SPAs that
hydrate data purely client-side.

## Core Fetch

```python
import re
import urllib.request

def _fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8", errors="ignore")
```

A full browser User-Agent reduces 403/429 risk on most sites.

## Common Parsers

```python
# Page title
def _title(html: str) -> str:
    m = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
    return m.group(1).strip() if m else ""

# Strip all tags → plain text (for keyword search)
def _text(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))

# Dollar figure near a keyword (e.g. "valuation")
def _dollar_near(text: str, keyword: str, unit: str = "billion") -> float | None:
    signal_re = re.compile(keyword, re.IGNORECASE)
    amount_re = re.compile(rf"\$\s*(\d[\d,\.]*)\s*{unit}\b", re.IGNORECASE)
    for sig in signal_re.finditer(text):
        window = text[max(0, sig.start()-120):sig.end()+120]
        for m in amount_re.finditer(window):
            try:
                return float(m.group(1).replace(",", ""))
            except ValueError:
                pass
    return None

# JSON-LD structured data (Schema.org etc.)
import json
def _jsonld(html: str) -> list[dict]:
    out = []
    for m in re.finditer(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
                         html, re.DOTALL | re.IGNORECASE):
        try:
            out.append(json.loads(m.group(1)))
        except json.JSONDecodeError:
            pass
    return out
```

## Caching — The Key Pattern

Cache for 24h. **Don't cache failures** — if the fetch fails, raise so `@st.cache_data`
skips storage and the next page load retries automatically.

```python
import time
import streamlit as st

@st.cache_data(ttl=86_400, show_spinner=False)
def _fetch_all_cached() -> list[dict]:
    out = []
    for i, item in enumerate(_ITEMS):
        if i > 0:
            time.sleep(0.8)          # stagger to avoid rate limits
        try:
            html = _fetch(item["url"])
            data = _parse(html)
        except Exception:
            data = None
        out.append({**item, "data": data})

    if all(e["data"] is None for e in out):
        raise RuntimeError("all_failed")  # no cache stored → next load retries
    return out


def _fetch_all() -> tuple[list[dict], bool]:
    """Public wrapper — never raises."""
    try:
        return _fetch_all_cached(), True
    except Exception:
        return [{**item, "data": None} for item in _ITEMS], False
```

Refresh button pattern:
```python
if st.button("Refresh"):
    _fetch_all_cached.clear()
    st.rerun()
```

## Rate Limits (429)

- **Stagger requests** — `time.sleep(0.8)` between calls during the one daily fetch.
- **Don't cache failures** — the pattern above ensures 429 responses don't lock you out for 24h.
- **User-Agent** — realistic browser UA avoids most bot-detection 429s.
- If a site consistently 429s: increase TTL, add longer sleep, or fall back to static data.

## Static Assets (Logos, SVGs)

Don't hotlink external logos — download once, commit to the repo.

```bash
# Download from Simple Icons (free brand SVGs, white fill variant)
curl -sfL "https://cdn.simpleicons.org/{slug}/white" -o static/logos/{name}.svg
# Or from jsDelivr if not on simpleicons CDN:
curl -sfL "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg" -o static/logos/{name}.svg
```

Add `fill="#ffffff"` to the `<svg>` tag if the downloaded file lacks it.

Embed inline in HTML (no `<img>` — no external request, no CORS, works in Streamlit):
```python
from pathlib import Path

def _svg(filename: str) -> str:
    p = Path(__file__).parent / "static" / "logos" / filename
    return p.read_text() if p.exists() else ""

# In render:
svg_html = f'<span class="logo-wrap">{_svg("openai.svg")}</span>'
```

## What Works vs. What Doesn't

| Scenario | Works? | Notes |
|----------|--------|-------|
| Server-rendered HTML (Django, Rails, Next.js SSR) | ✅ | Page title, meta tags, visible text all parseable |
| Next.js App Router (streaming) | ⚠️ | Key data often in `<title>` and server chunks; body text usually available |
| Pure SPA / client-rendered React | ❌ | `urllib` gets the shell HTML only; use Playwright instead |
| Cloudflare-protected sites | ⚠️ | Realistic UA helps; persistent 403 → Playwright or give up |
| JSON APIs disguised as web pages (`/api/data.json`) | ✅ | Use `json.loads(_fetch(url))` directly |
| Sites with `application/ld+json` Schema.org blocks | ✅ | Structured, reliable; prefer over regex when available |

## When to Use Playwright Instead

- SPA where data doesn't appear in initial HTML
- Need to click/interact before data loads
- Form submissions
- Sites with aggressive JS-based bot detection

## Google Images — Landscape Image Scraping

Use browser harness (not `http_get`) — Google blocks urllib fetches. Navigate with `goto_url`, then extract URLs from script tags.

**Search URL with landscape filter:**
```python
goto_url(f"https://www.google.com/search?q={query}&tbm=isch&tbs=iar:w")
wait_for_load()
```

**Extract candidate URLs from script tags (IIFE — avoids bare `return` SyntaxError):**
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

**Check image dimensions (JPEG SOF marker parsing + PNG IHDR):**
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
        if data[:2] == b'\xff\xd8':  # JPEG
            i = 2
            while i + 4 < len(data):
                if data[i] != 0xff: break
                marker = data[i+1]
                if marker in (0xc0, 0xc1, 0xc2):
                    h, w = struct.unpack('>HH', data[i+5:i+9])
                    return w, h
                length = struct.unpack('>H', data[i+2:i+4])[0]
                i += 2 + length
        elif data[:8] == b'\x89PNG\r\n\x1a\n':  # PNG
            return struct.unpack('>II', data[16:24])
    except:
        pass
    return None, None

for u in urls:
    w, h = get_dims(u)
    if w and h:
        ratio = w / h
        print(f"ratio={ratio:.2f} {w}x{h} {u[:80]}")
```

**Pick best candidate:**
- Prefer ratio ≥ 1.3 (landscape) for Notion cover photos
- Prefer CDN-hosted images (S3, Cloudinary, Wikimedia, NYT, TripAdvisor CDN) — they hotlink reliably
- Avoid food blog `/wp-content/` square thumbnails (typically 1:1 even with landscape filter)
- When borderline, `capture_screenshot()` the search results page to visually pick the best image

## Finance Cockpit Reference

`ipo_monitor.py` implements this pattern for ipos.fyi:
- Page `<title>` → IPO status string
- Stripped body text near "valuation" keyword → dollar figure
- 3 companies fetched with 0.8s stagger
- 24h cache, failure does not cache
- SVGs saved in `static/logos/`, inlined as HTML
