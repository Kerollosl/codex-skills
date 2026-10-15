---
name: ui-design-lead
description: Choose the right design workflow when the user asks for UI direction, a broad redesign plan, or help deciding among design skills.
---

# UI Design Lead

Use this skill when the user asks for design direction, a broad redesign plan, or help
choosing among overlapping UI skills. Look at the actual UI, identify the design problem,
and choose the smallest workflow that addresses the requested outcome. If the user has
already asked you to implement the work, proceed with the selected workflow.

Keep routing brief. Explain the choice when it helps the user understand the work, then
load the selected skill and complete the task. Respect an explicitly named skill or tool.

## Communicate the route

For broad work, give a concise diagnosis and name the selected workflow in a progress
update. For a small change, just make it. Do not add fixed banners or phase markers.

## When to bow out fast

Not everything needs a skill, and ceremony over a trivial change wastes the user's time. If
the request is a one-line change (swap a color, fix a typo, nudge a single margin), a pure
copy edit with no UX dimension, or simply not UI, say so in one line and just do it. Route
only genuine design work: builds, redesigns, restyles, evaluations,
systematic refinement, motion systems, and "make this actually good".

## Phase 1 — Read the target

Diagnose from evidence, not from the prompt alone — the prompt is often vague on purpose
("make it nicer") because the user is trusting you to see what they cannot name. Gather
whatever applies:

- **Brief.** Vibe words ("minimal", "Linear-like", "brutalist", "premium", "playful"),
  references (URLs, pasted screenshots, named products or competitors), audience, hard
  constraints (accessibility-critical, existing brand assets, "do not break X"), and scope
  — the whole surface or one element.
- **Code.** If a repo or path is in play: detect the framework and styling approach, then
  run `bash ~/.codex/skills/ui-design-lead/scripts/scan-fingerprints.sh <path>` for a fast
  read on AI-slop tells (Inter, purple gradients, `grid-cols-3`, `h-screen`, heavy shadows,
  pure black, cliché copy). Also check for impeccable's artifacts — `PRODUCT.md`,
  `DESIGN.md`, `.codex/skills/impeccable/`, `.agents/skills/impeccable/` — because this user's projects usually carry
  them, and their presence decides the route (see Phase 3).
- **Pixels.** If there is a URL or a running dev server, screenshot it desktop *and* mobile
  — in Chrome extension sessions use the permitted `cua_repl` instance and tab controls; elsewhere use a browser runtime exposed and allowed by that session. Read its API documentation rather than assuming `browser-harness` or `playwright-cli` is available.
  Analyze any pasted screenshot directly.

Close the phase with one line:
`Target read: <surface> · <stack> · impeccable <set up | not> · <n> slop hits`.

## Phase 2 — Diagnose

Classify the task and name the specific problems — not "the design is weak" but "hero H1 is
Inter at 40px with no tracking, three equal feature cards, `#000` background, no focus
rings". The full rubric, the fingerprint glossary, and the per-type decision tables are in
[references/diagnosis.md](references/diagnosis.md) — read it whenever the pick is not
immediately obvious.

Task types: **new build** · **redesign** (preserve or overhaul) · **targeted refinement**
(one dimension — layout, type, color, motion, copy, responsive, perf, a11y) · **evaluation**
(critique / audit) · **named restyle** (user wants a specific aesthetic) · **reference-first**
(see it as images before code) · **design system** (tokens, components).

A vague complaint ("looks cheap", "feels off", "make it nicer") is not its own task type —
it is one of the above wearing a disguise, and resolving *which* one is the core of the
diagnosis. Let the evidence decide: many fingerprints across the whole surface, or the user
wants it to feel different → **redesign**; the weakness sits in one dimension (the spacing,
the type, the color) → **targeted refinement**; barely anything is built yet → **new build**.
Route on the resolved type, never on the vague phrasing.

Output:

```
DIAGNOSIS
  Task:        <type>
  Surface:     <landing | dashboard | component | app screen | brand | ...>
  Findings:    <specific — the fingerprints, missing states, weak hierarchy, etc.>
  Constraints: <stack · don't-break · a11y · brand assets>
```

## Phase 3 — Route

Pick from the catalog — [references/catalog.md](references/catalog.md) carries each skill's
"use when / do not / produces / pairs with / conflicts with". Compact map:

| Diagnosis | Primary route | Common overlay / sequence |
|---|---|---|
| New build — product UI, dashboard, app shell, component, forms | `/impeccable shape` → build (`/impeccable init` first if no `PRODUCT.md`) | style preset if a look is named |
| New build — landing page or portfolio (marketing) | `/impeccable` (new-work) **if** the project is on impeccable's system; else `design-taste-frontend` | `high-end-visual-design` or `gpt-taste` overlay for premium / motion-heavy; `imagegen-frontend-web` first if the user wants to preview |
| Redesign of a real, built-out UI — on impeccable's system | `/impeccable document` (if no DESIGN.md) → `/impeccable critique` → `/impeccable polish` or `bolder` | screenshot first |
| Redesign of a real, built-out UI — no impeccable artifacts | `redesign-existing-projects` (product); `design-taste-frontend` (marketing site / portfolio) | offer `/impeccable init` if the user wants this project on the system going forward |
| "Redesign" but the code is scaffold-level — stubs, almost nothing styled | treat as **new build**, not redesign — `/impeccable shape` (+ `init`) | there is nothing to preserve; `redesign-existing-projects` has no incumbent to audit |
| Fix spacing / hierarchy / rhythm | `/impeccable layout` | |
| Typography / fonts | `/impeccable typeset` | `high-end-visual-design` for a full type system |
| Add color to a monochrome UI | `/impeccable colorize` | |
| Motion — product micro-interactions | `/impeccable animate` | |
| Motion — scroll choreography on a marketing site | `gpt-taste` | |
| Bolder / more delightful | `/impeccable bolder` or `delight` | |
| Too loud / tone down | `/impeccable quieter` | |
| Strip complexity | `/impeccable distill` | |
| Production-ready — errors, i18n, edge cases | `/impeccable harden` | `full-output-enforcement` for large multi-file output |
| Empty states / first-run | `/impeccable onboard` | |
| UX copy / error messages | `/impeccable clarify` | |
| Responsive / adapt for a device | `/impeccable adapt` | |
| Janky / slow UI | `/impeccable optimize` | |
| Review / audit / critique | `/impeccable critique` + `/impeccable audit` | screenshot first |
| Named look — warm minimal, editorial, Notion-ish | `minimalist-ui` | terminal — no taste overlay on top |
| Named look — brutalist, terminal, blueprint, declassified | `industrial-brutalist-ui` | terminal — no taste overlay on top |
| Brand / logo system / identity deck | `brandkit` | |
| "Show me before you build" — web | `imagegen-frontend-web` → then a build route | `image-to-code` for pixel-faithful implementation |
| Mobile app screens / flows (concepts) | `imagegen-frontend-mobile` | images only — pair with a build route for code |
| User is working in Google Stitch | `stitch-design-taste` | |
| Iterate on an element live in the browser | `/impeccable live` (needs a dev server) | |
| Extract / document a design system | `/impeccable extract` or `document` | |

When two routes both fit, reason it through — this is the judgement the user is delegating:

- **impeccable vs design-taste-frontend.** `design-taste-frontend` is landing / portfolio /
  redesign only and explicitly *excludes* dashboards, data tables, and multi-step product
  UI. Marketing or portfolio → it is a fine pick. Anything product-shaped → impeccable.
  When the project already carries `PRODUCT.md` / `DESIGN.md`, stay on impeccable so the
  work matches the committed world — that is the usual case for this user.
- **impeccable vs redesign-existing-projects.** `redesign-existing-projects` audits an
  incumbent and improves it in place — it needs a real, built-out UI to work on. Reach for
  it when the project has no impeccable artifacts, the surface is product-shaped, and there
  is genuine existing design to upgrade. Reach for impeccable instead when artifacts are
  present, when the user wants a scored backlog (`document` → `critique` → `polish`), or
  when the "existing" UI is scaffold-level — stubs with almost no styling — because then
  there is nothing to audit and the honest task is a new build (`/impeccable shape`, with
  `init` first). This user's projects are usually on impeccable's system, so absent
  artifacts is itself worth a beat: offer `/impeccable init` rather than silently routing
  around impeccable for good.
- **Overlays are not workflows.** `high-end-visual-design` and `gpt-taste` supply taste
  rules, not a process. Load one *before* the build skill so its rules are in context, then
  build. Do not run them alone unless the user only wants the rules.
- **Style presets are terminal.** `minimalist-ui` / `industrial-brutalist-ui` own the whole
  look; do not stack a taste overlay on top, since their font / shadow / color bans collide.
- **One full-authority skill per pass.** Never impeccable + design-taste + redesign together.
- **Imagegen precedes code, never follows it.**

When the user asks for a plan or skill recommendation, present the route briefly:

```
ROUTE
  1. <skill / command>   — <one line: why>
  2. <skill / command>   — <why>
  overlay: <skill>       — <applied during step 1>

OPTIONAL ALTERNATIVE
  <skill> — <why it might fit>
```

If the user requested implementation, continue directly. Ask only when the user explicitly
requested a plan before changes or a decision materially affects the result.

## Phase 4 — Dispatch

Run the route in order. Invoke each step by loading the relevant Codex skill
instructions and applying its workflow — `/impeccable` with its sub-command and target, the
others by name. If a step's output changes the picture — a critique surfaces something
bigger than the original ask — say so and re-present the remaining route
rather than pushing on with a plan that no longer fits.

After the last step, give a one-paragraph recap: what ran, what changed, what is left.

If the user named a skill up front, use it. Mention any concrete conflict with the requested
outcome and resolve it within the task where possible.
