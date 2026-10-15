---
name: linkedin-profile-cleanup
description: Full LinkedIn profile improvement session — connects to the user's live Chrome session, scrapes headline, about, experience descriptions, and skills list, rewrites each section for clarity, impact, and authentic professional voice, presents a before/after approval table, then applies approved edits via browser automation. Use whenever the user says anything like "clean up my LinkedIn", "polish my LinkedIn", "fix my LinkedIn profile", "my LinkedIn needs work", "improve my about section", "update my LinkedIn headline", or wants to refresh their professional presence online. Always invoke this skill rather than attempting LinkedIn edits manually.
---

# LinkedIn Profile Cleanup

You are running a focused LinkedIn profile improvement session. Work through these four phases in order. **Take screenshots liberally — LinkedIn's DOM changes frequently and visual verification beats selector guessing.**

---

## Browser runtime selection

Use the browser controls exposed and permitted in the current session. In the Codex Chrome extension, follow its `cua_repl` browser-instance selection and tab-claim instructions; read the returned API documentation and operate through supported snapshots, visible controls, screenshots, and navigation. For a referenced current tab, read `getTabContext` first when required. Do not launch a separate browser harness or run page scripts to bypass that runtime's restrictions.

The browser-harness scripts below are legacy implementation examples for sessions where that harness is explicitly available and permitted. In extension sessions, translate the workflow to the supported UI API instead of executing those scripts; refresh the visible state after transitions and read back saved changes.

## Phase 1: Scrape Current Profile

Make sure the user has Chrome open with LinkedIn logged in. Then run:

```bash
browser-harness <<'PY'
import time, json

new_tab("https://www.linkedin.com/in/me")
wait_for_load()
time.sleep(3)

capture_screenshot("/tmp/li_01_load.png")

# Expand truncated sections before extracting
js("""
  document.querySelectorAll(
    'button.inline-show-more-text__button, button.show-more-less-html__button, button[aria-label*="see more"]'
  ).forEach(b => { try { b.click() } catch(e) {} })
""")
time.sleep(1)

# Scroll through to trigger lazy-loaded sections
for y in [800, 1600, 2400, 3200, 4000]:
    js(f"window.scrollTo(0, {y})")
    time.sleep(0.6)
js("window.scrollTo(0, 0)")
time.sleep(0.5)

capture_screenshot("/tmp/li_02_full.png")

def safe_js(code, fallback=""):
    try:
        r = js(code)
        return r if r else fallback
    except:
        return fallback

# --- Tagline (line directly under your name) ---
tagline = safe_js("""
  const candidates = [
    '.text-body-medium.break-words',
    '.pv-text-details__left-panel .text-body-medium',
    '[data-field="headline"]'
  ];
  for (const sel of candidates) {
    const el = document.querySelector(sel);
    if (el && el.innerText.trim().length > 2) return el.innerText.trim();
  }
  return '';
""")

# --- About section ---
about = safe_js("""
  // Expand if collapsed
  const moreBtn = document.querySelector('#about ~ * button.inline-show-more-text__button');
  if (moreBtn) moreBtn.click();

  const aboutEl = document.getElementById('about');
  if (!aboutEl) return '';

  // Walk up to find the section wrapper
  let container = aboutEl;
  for (let i = 0; i < 6; i++) {
    container = container.parentElement;
    if (!container) break;
    const spans = container.querySelectorAll('span[aria-hidden="true"]');
    for (const span of spans) {
      const txt = span.innerText.trim();
      if (txt.length > 50) return txt;
    }
  }
  return '';
""")

# --- Experience entries ---
experience_raw = safe_js("""
  const results = [];
  const expEl = document.getElementById('experience');
  if (!expEl) return '[]';

  let container = expEl;
  for (let i = 0; i < 6; i++) container = container.parentElement;

  const items = container.querySelectorAll('li.artdeco-list__item');
  for (const li of items) {
    const boldSpans = li.querySelectorAll('.mr1.t-bold span[aria-hidden="true"]');
    const normalSpans = li.querySelectorAll('.t-14.t-normal span[aria-hidden="true"]');
    const blackSpans = li.querySelectorAll('.t-14.t-normal.t-black span[aria-hidden="true"]');

    const title = boldSpans[0]?.innerText?.trim() || '';
    const company = normalSpans[0]?.innerText?.trim() || '';
    const desc = blackSpans[0]?.innerText?.trim() || '';

    if (title && title.length > 1) results.push({ title, company, description: desc });
  }
  return JSON.stringify(results);
""", "[]")

try:
    experience = json.loads(experience_raw)
except:
    experience = []

# --- Skills list ---
skills_raw = safe_js("""
  const results = [];
  const skillEl = document.getElementById('skills');
  if (!skillEl) return '[]';

  let container = skillEl;
  for (let i = 0; i < 6; i++) container = container.parentElement;

  container.querySelectorAll('.mr1.t-bold span[aria-hidden="true"]').forEach(el => {
    const txt = el.innerText.trim();
    if (txt && txt.length > 1 && !results.includes(txt)) results.push(txt);
  });
  return JSON.stringify(results.slice(0, 25));
""", "[]")

try:
    skills = json.loads(skills_raw)
except:
    skills = []

profile = {
    "tagline": tagline,
    "about": about,
    "experience": experience,
    "skills": skills,
}

print("=== PROFILE_DATA_START ===")
print(json.dumps(profile, indent=2))
print("=== PROFILE_DATA_END ===")
PY
```

**If any fields come back empty:** send the screenshots at `/tmp/li_01_load.png` and `/tmp/li_02_full.png` to the user and read the text visually from them to fill the gaps.

---

## Phase 2: Analyze and Propose Rewrites

Read the scraped data and generate improvements for each non-empty section. The goal is impact and authenticity — not a generic LinkedIn voice.

**Tagline:** Specific, memorable, under 220 chars. Should say what you do + what makes you distinctive. Avoid: "experienced professional", "passionate about X".

**About:** First sentence must hook. Concrete numbers and achievements beat adjectives. First person, active voice. No clichés. Max 5 paragraphs.

**Experience descriptions:** Lead every bullet with a strong action verb. Quantify impact wherever possible ("reduced load time by 40%" beats "improved performance"). Cut filler words and vague claims.

**Skills:** Flag anything that's generic (e.g. "Microsoft Office"), outdated, or not a real differentiator. Note what's missing that should be there.

Present changes in this format (include every non-empty section):

```
## LinkedIn Profile — Proposed Changes

### Tagline
**Current:** [text]
**Proposed:** [improved text]

---

### About
**Current:**
[text]

**Proposed:**
[rewritten text]

---

### Experience: [Title at Company]
**Current:** [description, or "(no description)"]
**Proposed:** [rewritten description]

[...repeat for each experience role...]

---

### Skills
**Current:** [comma list]
**Recommendation:** Remove: [...] | Add: [...] | (skills editing is manual — LinkedIn's skills UI is too complex for automation)
```

Then ask: **"Which sections should I apply? Say 'all', 'none', or name them (e.g. 'tagline, about, [job title]')."**

---

## Phase 3: Apply Approved Edits

For each approved section, apply the edit with the selected supported browser runtime. Always screenshot before and after, then read the saved profile section to verify persistence. Browser-harness examples below are conditional on that runtime being permitted.

### Editing the Tagline

```bash
browser-harness <<'PY'
import time, json

js("window.scrollTo(0, 0)")
time.sleep(0.5)
capture_screenshot("/tmp/li_before_tagline.png")

# Find the "Edit intro" pencil button in the profile header card
btn = js("""
  const btns = Array.from(document.querySelectorAll('button'));
  const match = btns.find(b => {
    const label = (b.getAttribute('aria-label') || b.innerText || '').toLowerCase();
    return label.includes('edit intro') || label.includes('edit your intro');
  });
  if (!match) return null;
  const r = match.getBoundingClientRect();
  return JSON.stringify({x: r.x + r.width/2, y: r.y + r.height/2});
""")

if not btn:
    print("MANUAL_NEEDED: could not find Edit intro button — see /tmp/li_before_tagline.png")
else:
    coords = json.loads(btn)
    click_at_xy(coords['x'], coords['y'])
    time.sleep(1.5)
    capture_screenshot("/tmp/li_tagline_modal.png")

    NEW_TAGLINE = "PASTE_APPROVED_TAGLINE_HERE"

    # React-safe setter for text inputs
    js(f"""
      const input = document.querySelector('#headline, input[name="headline"], input[id*="headline"]');
      if (!input) return;
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      setter.call(input, {json.dumps(NEW_TAGLINE)});
      input.dispatchEvent(new Event('input', {{bubbles: true}}));
      input.dispatchEvent(new Event('change', {{bubbles: true}}));
    """)
    time.sleep(0.5)

    # Click Save
    save = js("""
      const btns = Array.from(document.querySelectorAll('button'));
      const s = btns.find(b => b.innerText.trim() === 'Save');
      if (!s) return null;
      const r = s.getBoundingClientRect();
      return JSON.stringify({x: r.x + r.width/2, y: r.y + r.height/2});
    """)
    if save:
        click_at_xy(*json.loads(save).values())
        time.sleep(2)

    capture_screenshot("/tmp/li_after_tagline.png")
    print("Done — verify /tmp/li_after_tagline.png")
PY
```

### Editing the About Section

```bash
browser-harness <<'PY'
import time, json

js("document.getElementById('about')?.scrollIntoView({block: 'center'})")
time.sleep(1)
capture_screenshot("/tmp/li_about_before.png")

# Find the edit pencil for the About section
btn = js("""
  const aboutEl = document.getElementById('about');
  if (!aboutEl) return null;
  let container = aboutEl;
  for (let i = 0; i < 6; i++) {
    container = container.parentElement;
    const btns = Array.from(container.querySelectorAll('button'));
    const match = btns.find(b => {
      const label = (b.getAttribute('aria-label') || '').toLowerCase();
      return label.includes('edit') && (label.includes('about') || label.includes('summary'));
    });
    if (match) {
      const r = match.getBoundingClientRect();
      return JSON.stringify({x: r.x + r.width/2, y: r.y + r.height/2});
    }
  }
  // Fallback: first edit button inside about container
  const anyEdit = container.querySelector('button[aria-label*="Edit"]');
  if (anyEdit) {
    const r = anyEdit.getBoundingClientRect();
    return JSON.stringify({x: r.x + r.width/2, y: r.y + r.height/2});
  }
  return null;
""")

if not btn:
    print("MANUAL_NEEDED: could not find About edit button — see /tmp/li_about_before.png")
else:
    coords = json.loads(btn)
    click_at_xy(coords['x'], coords['y'])
    time.sleep(1.5)
    capture_screenshot("/tmp/li_about_modal.png")

    NEW_ABOUT = "PASTE_APPROVED_ABOUT_TEXT_HERE"

    js(f"""
      const ta = document.querySelector('textarea');
      if (!ta) return;
      const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
      setter.call(ta, {json.dumps(NEW_ABOUT)});
      ta.dispatchEvent(new Event('input', {{bubbles: true}}));
      ta.dispatchEvent(new Event('change', {{bubbles: true}}));
    """)
    time.sleep(0.5)

    save = js("""
      const s = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
      if (!s) return null;
      const r = s.getBoundingClientRect();
      return JSON.stringify({x: r.x + r.width/2, y: r.y + r.height/2});
    """)
    if save:
        click_at_xy(*json.loads(save).values())
        time.sleep(2)

    capture_screenshot("/tmp/li_about_after.png")
    print("Done — verify /tmp/li_about_after.png")
PY
```

### Editing an Experience Description

For each experience role, scroll to it, find its edit pencil, open the modal, and update the description textarea using the same React-safe setter pattern as above. Take a screenshot first to visually confirm which role you're editing.

### If a Button Can't Be Found Automatically

Take a screenshot, read the pixel coordinates of the edit pencil from the image, and use `click_at_xy(x, y)` directly. This is more reliable than selectors for LinkedIn's frequently-changing DOM.

---

## Phase 4: Wrap Up

After applying all edits, scroll the profile from top to bottom and take a final screenshot. Summarize what was changed and flag any sections that need manual attention (e.g. skills reordering, which LinkedIn doesn't expose via simple DOM edits).
