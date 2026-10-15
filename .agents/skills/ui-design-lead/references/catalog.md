# Skill catalog

Every skill `ui-design-lead` can dispatch to, with the boundaries. When two look close,
the "Don't use when" and "Conflicts with" lines are what separate them.

Taste Skill v2 is installed as `design-taste-frontend`; route to that skill for marketing
sites and portfolios when the project is not on Impeccable. The official `frontend-design`
plugin is superseded by the skills below.

---

## Full-authority build / redesign skills

Exactly one of these runs per pass. They produce production code and own the whole design.

### impeccable
- **Invoke:** `/impeccable <command> <target>` — see the cheat sheet in `diagnosis.md`.
- **Produces:** production frontend code, plus a managed context system (`PRODUCT.md`,
  `DESIGN.md`, per-surface briefs, an optional detector hook).
- **Use when:** the project already carries impeccable artifacts (the common case for this
  user); the task maps to one of its ~22 sub-commands; the surface is product-shaped
  (app, dashboard, settings, editor, forms, tools, components); the user wants systematic
  rigor, a scored critique, or live in-browser iteration.
- **Don't use when:** the user explicitly wants a lighter one-off pass and the project has
  no artifacts — `redesign-existing-projects` or `design-taste-frontend` is less overhead.
- **Pairs with:** `full-output-enforcement` (large builds); `high-end-visual-design` /
  `gpt-taste` as taste overlays loaded before a build command; `browser-harness` /
  `playwright-cli` for screenshots.
- **Conflicts with:** `design-taste-frontend`, `redesign-existing-projects` — never run two
  full-authority skills together.

### design-taste-frontend
- **Invoke:** by name.
- **Produces:** landing pages, portfolios, and marketing-site redesigns — with a "design
  read" (page kind / audience / vibe), three dials (variance / motion / density), and an
  honest map to real design systems (Fluent, Carbon, Material, Polaris, Atlaskit, Primer,
  GOV.UK, USWDS, Radix, shadcn, Tailwind).
- **Use when:** greenfield or redesign of a **marketing site or portfolio**, especially
  when the right foundation/aesthetic is unclear and you want the skill to infer it; the
  project is *not* on impeccable's system.
- **Don't use when:** dashboards, data tables, multi-step product UI, app shells — the skill
  itself refuses these. Also skip it when the project has `PRODUCT.md` / `DESIGN.md` — stay
  on impeccable for consistency.
- **Pairs with:** `high-end-visual-design` or `gpt-taste` overlay; `imagegen-frontend-web`
  upstream.
- **Conflicts with:** impeccable, `redesign-existing-projects`.

### redesign-existing-projects
- **Invoke:** by name.
- **Produces:** targeted upgrades to an existing site or app — scan, diagnose against a
  fixed audit (typography, color, layout, states, motion), fix in place without breaking
  functionality. Stack-agnostic.
- **Use when:** "make my existing thing better / more premium / less generic", the project
  has **no impeccable artifacts**, it is product-shaped (so `design-taste-frontend` does
  not apply), and there is a **genuinely built-out UI** to audit.
- **Don't use when:** artifacts exist (use `/impeccable critique` → `polish`); it is a
  marketing site / portfolio (use `design-taste-frontend`); it is a from-scratch build; or
  the "existing" code is scaffold-level stubs — with nothing to audit it is a new build,
  route through `/impeccable shape` (+ `init`).
- **Pairs with:** `browser-harness` for before/after screenshots.
- **Conflicts with:** impeccable, `design-taste-frontend`.

---

## Taste overlays (load before a build skill — not standalone workflows)

### high-end-visual-design
- **Invoke:** by name, before the primary build skill.
- **Provides:** agency / Awwwards-tier rules — banned fonts (Inter, Roboto, Arial), banned
  icons, banned shadows/borders, the "Double-Bezel" nested-card technique, a vibe+layout
  variance engine, spring-physics motion choreography, GPU-safe performance guardrails.
- **Use when:** the brief is "make it feel expensive / like a $150k agency site / Linear-
  tier / Apple-esque" and no fixed style preset is named. Best on premium consumer and
  SaaS marketing.
- **Don't use when:** a style preset (`minimalist-ui`, `industrial-brutalist-ui`) is already
  chosen — their bans collide. Or when the user wants restraint (its default is maximal).
- **Pairs with:** impeccable new-work, `design-taste-frontend`, `gpt-taste`.

### gpt-taste
- **Invoke:** by name, before the primary build skill.
- **Provides:** GSAP motion engineering (scroll pinning, stacking, scrubbing, card
  stacking), strict AIDA page structure, wide editorial typography (bans 4+ line H1
  wraps), gapless `grid-flow-dense` bento grids, inline typography images, massive section
  spacing, a mandatory pre-flight `<design_plan>`.
- **Use when:** a marketing / landing site where **scroll choreography and motion are the
  point**, not a garnish.
- **Don't use when:** product UI (motion should be subtle there — use `/impeccable
  animate`); a style preset is chosen; the user wants a calm/static feel.
- **Pairs with:** `design-taste-frontend`, `high-end-visual-design`, `imagegen-frontend-web`.

---

## Style presets (terminal — they own the whole look)

### minimalist-ui
- **Invoke:** by name.
- **Provides:** warm-monochrome editorial "document-style" UI — off-white canvas, editorial
  serif headings + geometric sans body, muted pastel spot accents, flat 1px-border bento,
  crisp small radii, near-invisible shadows, no gradients, no pill-shaped large containers.
- **Use when:** the user names "minimal / warm / editorial / Notion-like / muted / calm /
  no gradients".
- **Don't use when:** the brief wants boldness, dark tech, heavy motion, or a specific
  different aesthetic.
- **Conflicts with:** `high-end-visual-design`, `gpt-taste`, `industrial-brutalist-ui`.

### industrial-brutalist-ui
- **Invoke:** by name.
- **Provides:** Swiss print × military-terminal UI — pick one substrate (light newsprint or
  dark CRT), monolithic grotesk macro-type + monospace telemetry micro-type, hazard red as
  the only accent, zero border-radius, visible grid compartmentalization, analog
  degradation (halftone, scanlines, dithering, grain).
- **Use when:** the user names "brutalist / terminal / CRT / Swiss / blueprint /
  declassified / tactical / industrial / HUD"; data-heavy dashboards, portfolios, or
  editorial sites that should feel like classified documents.
- **Don't use when:** consumer-friendly, soft, or premium-luxury briefs.
- **Conflicts with:** `high-end-visual-design`, `gpt-taste`, `minimalist-ui`.

---

## Image-generation pipeline (runs before code, never after)

### imagegen-frontend-web
- **Invoke:** by name.
- **Produces:** one horizontal reference image **per section** (8 sections → 8 images),
  with composition variety, varied hero scales, a narrative concept spine, one consistent
  palette. For landing pages, marketing sites, product comps.
- **Use when:** the user wants to see the design as images before any code, or wants
  polished comps to hand to a developer.
- **Then:** review with the user → build route (`image-to-code` for pixel-faithful, else
  the chosen images become the brief for the normal build route).

### imagegen-frontend-mobile
- **Invoke:** by name.
- **Produces:** premium mobile app screen and flow images inside phone mockups. iOS /
  Android / cross-platform. **Images only — no code.**
- **Use when:** concepting mobile app screens or flows before implementation.
- **Don't use when:** websites, desktop dashboards, or anything that needs code now.

### image-to-code
- **Invoke:** by name.
- **Produces:** generates section reference images itself, analyzes them deeply, then
  implements the site to match them closely. Codex-oriented; favors large readable
  section-specific images.
- **Use when:** the user wants the built result to match a generated design as closely as
  possible — visual fidelity is the priority.
- **Don't use when:** the user already has a clear brief and just wants a good build (use
  the normal route); mobile (use `imagegen-frontend-mobile`).

### brandkit
- **Invoke:** by name.
- **Produces:** brand-guidelines boards, logo systems, identity decks, visual-world
  presentations — a complete brand world in one image. Dark charcoal canvas, grid boards,
  sparse type, premium mockups.
- **Use when:** the task is brand identity, not interface — logos, brand systems,
  guidelines decks.

---

## Tool-specific

### stitch-design-taste
- **Invoke:** by name.
- **Produces:** a `DESIGN.md` file tuned for Google Stitch's semantic design language —
  atmosphere, calibrated color, typographic architecture, component behaviors, motion
  philosophy, an anti-pattern list.
- **Use when:** the user is generating screens in Google Stitch (labs.google/stitch) and
  needs a design spec to prompt it with.
- **Don't use when:** any non-Stitch workflow — this does not produce app code.

---

## Support

### full-output-enforcement
- **Invoke:** by name, alongside a build skill.
- **Provides:** bans placeholder patterns (`// ...`, "rest follows the same pattern"),
  enforces complete multi-file output, clean `[PAUSED — X of Y]` splits at token limits.
- **Use when:** the route will produce many files or long files and truncation is a real
  risk — large redesigns, `harden`, whole-site builds.

### browser-harness
- **Invoke:** `browser-harness` CLI (see the user's global browser-harness skill).
- **Use when:** you need to screenshot the user's **live Chrome** session for before/after
  diagnosis and verification. First navigation is `new_tab(url)`.

### playwright-cli
- **Invoke:** by name.
- **Use when:** you need a **fresh** browser for screenshots or visual QA — no live session
  to attach to, or you want isolation. Also for writing/debugging Playwright test scripts.
