# Diagnosis rubric

Read this when the route is not obvious from the compact map in SKILL.md. It has four
parts:

1. [Classifying the task](#1-classifying-the-task)
2. [The AI-slop fingerprint glossary](#2-the-ai-slop-fingerprint-glossary)
3. [Per-type decision tables](#3-per-type-decision-tables)
4. [The `/impeccable` sub-command cheat sheet](#4-the-impeccable-sub-command-cheat-sheet)

---

## 1. Classifying the task

Match the request to one type. When two seem to apply, the more specific one wins
(a "make the spacing better on my new landing page" is **targeted refinement**, not **new
build**).

| Type | Signals | Notes |
|---|---|---|
| **New build** | "build", "create", "I need a page/screen/component for", nothing exists yet | Split on surface: product-shaped (app, dashboard, settings, editor, forms, tools) vs marketing-shaped (landing, pricing, campaign, portfolio). The split drives impeccable vs design-taste-frontend. |
| **Redesign — preserve** | "refresh", "modernize", "tighten up", keep the structure and content | Incumbent identity stays; you are refining, not replacing. |
| **Redesign — overhaul** | "redesign", "rethink", "it is dated", "start over on the look" | Old look is treated as anti-reference. impeccable calls this a new visual world. |
| **Targeted refinement** | One named dimension: spacing, hierarchy, type, color, motion, copy, responsiveness, performance, a11y | Route straight to the matching `/impeccable` mode. Do not open a full redesign. |
| **Evaluation** | "review", "audit", "critique", "what is wrong with", "roast" | `critique` (heuristic UX score) + `audit` (a11y / perf / responsive). No code changes unless asked. |
| **Named restyle** | The user names an aesthetic: "make it brutalist", "Notion-style", "warm editorial", "terminal vibe" | Route to the style preset that owns that look. The preset is terminal — it decides fonts, color, shadows. |
| **Reference-first** | "show me options", "mock it up first", "what would it look like", "I want to see before you code" | imagegen skill → review → then a build route. |
| **Design system** | "tokens", "design system", "component library", "extract the patterns", "document the design" | `/impeccable init` → `shape` for greenfield; `/impeccable document` / `extract` for existing code. |

If the request is genuinely trivial (one property, one string) or not UI, do not classify —
bow out per SKILL.md.

---

## 2. The AI-slop fingerprint glossary

The `scan-fingerprints.sh` script counts these. Here is what each one means and where it
points. Cite the specific hits in your DIAGNOSIS `Findings` line.

| Fingerprint | Why it reads as AI slop | Points toward |
|---|---|---|
| **Inter** as the primary/only font | The default of every AI build; zero character | `typeset`, or `high-end-visual-design` for a full type system |
| **Purple / indigo / violet gradients** (`from-purple`, `to-indigo`, mesh) | The single most recognizable "AI made this" tell | `colorize` or `critique` → `polish`; `redesign-existing-projects` |
| **`grid-cols-3` feature row** — three equal cards | The most overused AI layout | `layout`; `redesign-existing-projects` |
| **`h-screen` / `100vh`** for full-height sections | Breaks on iOS Safari; signals no device testing | `adapt`, or fold into any refinement pass |
| **`shadow-md/lg/xl`** everywhere | Generic Tailwind depth; no consistent light source | `layout` or `polish`; `high-end-visual-design` bans these |
| **`#000000` / `bg-black`** background | Pure black never appears in considered design | `colorize` or `polish` |
| **`outline-none`** without `focus-visible` | Accessibility failure; keyboard users lost | `audit`, then `harden` |
| **`backdrop-blur` on many elements** | Glassmorphism-on-everything; GPU cost, no restraint | `quieter` or `polish` |
| **`border-gray-200/300`** default hairlines | Untinted, lifeless borders | `polish`; `high-end-visual-design` |
| **Cliché copy** — "Elevate", "Seamless", "Unleash", "Supercharge", "Delve" | AI marketing voice | `clarify` |
| **Placeholder junk** — "Lorem ipsum", "John Doe", "Acme Corp" | Unfinished; no real content thinking | flag in `Findings`; `clarify` for copy, or send back to the user for real content |
| **Emoji in source / headings** | Banned by every taste skill here | flag; fixed in any refinement pass |
| **Many `text-center` blocks** | Centered-everything is a low-variance default | `layout`; `bolder` if the whole thing is timid |

Breadth across many categories at once → the task is a **redesign** (route it by the
Redesign table below — the scan tells you the *scope*, not the skill). A spike in one
category with the rest quiet → the matching **targeted refinement**. The scan is a
tiebreaker for scope, never the routing decision on its own.

---

## 3. Per-type decision tables

### New build

| Surface | Route | Overlay / sequence |
|---|---|---|
| Dashboard, admin, settings, editor, internal tool, data table | `/impeccable shape` → new-work | `industrial-brutalist-ui` only if the user wants the blueprint look |
| App shell, product screen, forms, onboarding | `/impeccable shape` → new-work | — |
| Component or small feature in an existing product | `/impeccable` general design work on the incumbent implementation | — |
| Landing / pricing / campaign / marketing site | project on impeccable's system → `/impeccable` new-work; otherwise `design-taste-frontend` | `high-end-visual-design` (premium consumer/SaaS) or `gpt-taste` (scroll-choreography) as overlay; `imagegen-frontend-web` first if previewing |
| Portfolio (designer / developer / studio) | `design-taste-frontend` | `imagegen-frontend-web` first if previewing |
| Mobile app (concepts, no code yet) | `imagegen-frontend-mobile` | pair with a native build route once concepts are approved |
| Brand identity, logo system, guidelines deck | `brandkit` | — |

### Redesign

First check there is a real, built-out UI to redesign. If the code is scaffold-level —
stub components, almost nothing styled, comments standing in for content — there is no
incumbent to audit; that is a **new build**, route it through the New build table
(`/impeccable shape`, with `init` first).

| Situation | Route |
|---|---|
| Project carries `PRODUCT.md` / `DESIGN.md` | `/impeccable document` (only if `DESIGN.md` missing) → `/impeccable critique <surface>` → `/impeccable polish` (preserve) or `/impeccable bolder` (overhaul) |
| No impeccable artifacts, product-shaped app, genuinely built out | `redesign-existing-projects` — and offer `/impeccable init` if the user wants this project on the system from here on |
| No impeccable artifacts, marketing site or portfolio | `design-taste-frontend` (its redesign path: audit-first, preserve vs overhaul) |
| User wants a scored backlog they can work down over time | `/impeccable critique` regardless — it writes a snapshot `polish` reads as its to-do list |

Before proposing changes, screenshot desktop + mobile **when a URL or running dev server is
available** — the DIAGNOSIS should cite what is actually on screen. If there is no server
and standing one up would mean writing into the project, say so and diagnose from the code;
fold the before/after screenshots into the dispatch step instead.

### Targeted refinement — one dimension

| Ask | Route |
|---|---|
| "spacing / rhythm / it feels cramped / too much whitespace / hierarchy is flat" | `/impeccable layout` |
| "fonts / typography / headings have no presence / pick a better typeface" | `/impeccable typeset` (or `high-end-visual-design` if they want the whole type architecture rethought) |
| "it is all grey / add some color / too monochrome" | `/impeccable colorize` |
| "add motion / animate / it feels static" — inside a product | `/impeccable animate` |
| "scroll animations / pinning / parallax / kinetic type" — on a marketing site | `gpt-taste` |
| "make it bolder / it is too safe / more personality" | `/impeccable bolder`, or `/impeccable delight` for memorable touches specifically |
| "tone it down / too much / overstimulating" | `/impeccable quieter` |
| "too complex / strip it back / simplify" | `/impeccable distill` |
| "error states / i18n / edge cases / production-ready" | `/impeccable harden` (+ `full-output-enforcement` if it is a large multi-file job) |
| "empty states / first-run / new-user experience" | `/impeccable onboard` |
| "the copy / labels / error messages / microcopy" | `/impeccable clarify` |
| "responsive / mobile / tablet / it breaks on small screens" | `/impeccable adapt` |
| "slow / janky / stutters / performance" | `/impeccable optimize` |

### Evaluation

Run both unless the user scopes it: `/impeccable critique <target>` for the UX heuristic
score, then `/impeccable audit <target>` for a11y / perf / responsive. Screenshot first.
Present findings; do not edit unless asked. If the score is low or P0/P1 issues exist and
the user wants them fixed, that becomes a **redesign** or **targeted refinement** — re-route.

### Named restyle

| Named aesthetic | Route |
|---|---|
| "minimal", "warm", "editorial", "Notion-like", "document-style", "muted", "no gradients" | `minimalist-ui` |
| "brutalist", "terminal", "CRT", "Swiss", "blueprint", "declassified", "tactical", "industrial", "military HUD" | `industrial-brutalist-ui` |
| "expensive", "agency", "Awwwards", "Linear-tier", "Apple-esque", "$150k site" — but no fixed style named | `high-end-visual-design` as the overlay on a build route (it is rules, not a preset) |

A style preset overrides the aesthetic dials. Do not also load `high-end-visual-design` or
`gpt-taste` on top — the bans conflict.

### Reference-first

1. `imagegen-frontend-web` (web) or `imagegen-frontend-mobile` (mobile) generates the
   references — one image per section for web.
2. User reviews and picks a direction.
3. Build route: `image-to-code` if they want the implementation to match the images
   pixel-for-pixel; otherwise the normal new-build route with the chosen images as the
   brief.

### Design system

| Ask | Route |
|---|---|
| Greenfield — "set up our design system / tokens" | `/impeccable init` (captures `PRODUCT.md`) → `/impeccable shape` |
| Existing code — "document what we have" | `/impeccable document` (generates `DESIGN.md` from the code) |
| Existing code — "pull these patterns into reusable tokens/components" | `/impeccable extract <target>` |
| User is prompting Google Stitch and wants a `DESIGN.md` for it | `stitch-design-taste` |

---

## 4. The `/impeccable` sub-command cheat sheet

Invoke as `/impeccable <command> <target>`. `<target>` is a file, route, or surface name.

| Command | Category | Reach for it when |
|---|---|---|
| `shape` | Build | Planning UX/UI before any code — flows, states, structure |
| `init` | Build | The project has no `PRODUCT.md` yet and needs durable context captured |
| `document` | Build | Existing code, no `DESIGN.md` — reverse-engineer the visual system |
| `extract` | Build | Pull repeated patterns into design-system tokens / components |
| `critique` | Evaluate | UX design review with a heuristic score and a P0–P3 issue list |
| `audit` | Evaluate | Technical quality — accessibility, performance, responsive behavior |
| `polish` | Refine | Final pass before shipping; reads the latest `critique` as its backlog |
| `bolder` | Refine | The design is safe / bland and should be amplified |
| `quieter` | Refine | The design is aggressive / overstimulating and should calm down |
| `distill` | Refine | Too much going on — strip to essence |
| `harden` | Refine | Make it production-ready — error states, i18n, edge cases |
| `onboard` | Refine | First-run flows, empty states, activation moments |
| `animate` | Enhance | Add purposeful motion and micro-interactions |
| `colorize` | Enhance | Add strategic color to a monochrome UI |
| `typeset` | Enhance | Fix typographic hierarchy and font choices |
| `layout` | Enhance | Fix spacing, rhythm, alignment, visual hierarchy |
| `delight` | Enhance | Add personality and memorable touches |
| `overdrive` | Enhance | Push past conventional limits — ambitious visual effects |
| `clarify` | Fix | Improve UX copy, labels, error messages |
| `adapt` | Fix | Adapt for different devices and screen sizes |
| `optimize` | Fix | Diagnose and fix UI performance problems |
| `live` | Iterate | In-browser variant mode — pick elements, generate alternatives (needs a running dev server; web only) |

`/impeccable` with **no argument** presents its own context-aware menu — route there only
when the user genuinely wants to browse options rather than solve a specific problem.

`/impeccable doctor` reports drift in the project's impeccable artifacts. Surface it if
`context.mjs` output or stale-looking `DESIGN.md` suggests it — but never run repairs as a
side effect of a design task.
