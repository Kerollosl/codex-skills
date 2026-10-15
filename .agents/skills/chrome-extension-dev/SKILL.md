---
name: chrome-extension-development
description: Develop and test Chrome extensions with validation, hotload cycles, and selector testing. Use this whenever you're working on Chrome extensions (manifest changes, content scripts, popup UI, background scripts). This skill validates manifest.json, automates the load-unpacked workflow, tests DOM selectors against live pages, and builds fast iteration loops—replacing manual reload cycles. Trigger whenever you're building, debugging, or iterating on any Chrome extension.
---

# Chrome Extension Dev

Accelerate Chrome extension development with validation, hotload loops, and live testing.

## What This Does

Handles:
- **Manifest validation** — Checks manifest.json for errors, deprecated APIs, permission issues
- **Load unpacked** — Automates chrome://extensions/ workflow (no manual clicking)
- **Selector testing** — Validates DOM selectors against actual target pages
- **Hotload loop** — Change → validate → load → test in seconds
- **Common gotchas** — Detects CSP issues, missing icons, bad content_scripts entries

## How to Use

**Start development session:**
```
/chrome-extension-dev
I'm working on the flight-email-parser extension
```

**Test a selector:**
```
/chrome-extension-dev
Does this selector work on gmail.com: .hP.m .Md
```

**Validate manifest after changes:**
```
/chrome-extension-dev
I changed the manifest, is it valid?
```

**Setup hotload loop:**
```
/chrome-extension-dev
Setup a fast reload cycle for my extension
```

## Workflow

**Manual flow (slow):**
1. Edit content script
2. Open chrome://extensions/
3. Click reload
4. Test on target page
5. Check console for errors
6. Repeat

**With this skill (fast):**
1. Edit content script
2. `/chrome-extension-dev` validates + reloads automatically
3. Test on target page
4. Errors surfaced immediately

## Checks Performed

✅ **Manifest** — Valid JSON, required fields, permission syntax  
✅ **Icons** — Referenced files exist  
✅ **Content scripts** — Valid match patterns, file paths  
✅ **Permissions** — Allowed for target URLs  
✅ **CSP** — Content Security Policy violations  
✅ **Selectors** — DOM queries tested against live target pages  

## Example Scenarios

**Scenario 1: Manifest error after changes**
```
/chrome-extension-dev
Validate the manifest
→ "Error in manifest: 'icons' field references icon.png but file doesn't exist in root. Create it or update the path."
```

**Scenario 2: Selector not matching**
```
/chrome-extension-dev
Test this selector on gmail.com: div.aKD
→ "Selector works but matches 14 elements. Be more specific: div.aKD.a82"
```

**Scenario 3: Hotload setup**
```
/chrome-extension-dev
Setup hotload for the text-case-converter extension
→ "Watching ~/Chrome Extensions/text-case-converter/ for changes. Reloading extension automatically on save."
```

## Performance

- **Manifest validation** — <1 second
- **Selector test** — 2-5 seconds (includes page load)
- **Hotload reload** — <2 seconds

## Output

Returns:
- ✅ **Valid** — No issues, extension is ready
- ⚠️ **Warnings** — Issues that may cause problems
- ❌ **Errors** — Critical issues blocking functionality
- 🔗 **Selector results** — Matches found, specificity suggestions
