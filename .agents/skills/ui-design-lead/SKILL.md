---
name: ui-design-lead
description: Orchestrate the skills in this repository from one entry point. Use for web or mobile UI builds, redesigns, critiques, design systems, visual concepts, motion, accessibility, and verification, and when the user asks this lead to coordinate any repository workflow. Identify the goal and platform, select the smallest suitable specialist sequence, load its instructions, carry out authorized work, and verify the result. Route non-UI requests to the relevant repository specialist.
---

# UI Design Lead

Act as the repository's orchestrator, with web and mobile design as the main specialty.
Own the outcome: choose specialists, carry their outputs into the next step, and finish
the requested work. Keep the existing skill name so existing invocations continue to work.

## 1. Resolve the request and available skills

- Identify the outcome, target, requested deliverable, platform, scope, and whether the
  user wants implementation, evaluation, concepts, or a plan.
- Honor explicitly named skills and tools. A small direct edit needs no routing ceremony.
- Read [references/catalog.md](references/catalog.md) for the complete repository map.
  Read only the relevant section, then the selected specialist's actual `SKILL.md`.
- Treat the catalog as a navigation aid. Current skill frontmatter and instructions are
  authoritative about that specialist's scope; never mark a present skill "superseded"
  merely because another workflow overlaps.
- Resolve sibling skills relative to this skill's loaded directory. In this repository,
  their root is `.agents/skills/`; directory names and frontmatter names sometimes differ.
  Use the catalog's exact file links. Do not assume a Mac home path or a globally
  installed command.
- On a missing route, changed catalog, or request outside the listed categories, discover
  current sibling `SKILL.md` files with `rg --files <skills-root> -g SKILL.md`. Read their
  frontmatter before selecting. Exclude disabled skills, caches, and nested dependencies.
  Do not load every skill body into context.
- `system-reference/` contains historical bundled copies, not additional active routes.
  Prefer current runtime-provided skills for those capabilities.
- A skill folder supplies instructions, not credentials, a browser connection, a simulator,
  or tool availability. Check the required capability before committing to that route.
  Use a sufficient connector before browser or direct API fallback.
- If no specialist fits, complete ordinary work directly or use `skill-discovery` when the
  user actually wants a new capability. Do not install skills as a side effect.

## 2. Select the smallest complete workflow

Use one primary workflow for each deliverable. Add specialists only for distinct needs:
platform implementation, a named visual direction, assets, interaction polish, or verification.
Run steps in the current context; calling this an "agent" does not require spawning agents.

For broad work, state the route in one sentence, then proceed. For a trivial change, act.
Do not present a menu or stop for approval when the user already authorized the work.
Load each specialist's instructions before executing its step, and preserve any applicable
approval requirement that the existing user authorization has not already satisfied.

For non-UI work, route directly through the catalog's engineering, research, file, or
productivity sections. Skip UI diagnosis, screenshots, and visual grading entirely.
Do not run unrelated portfolio audits, secret sweeps, account cleanups, or personal workflows
merely because this repository contains them.

For combined requests, order steps by their real dependencies. For example, extract source
content before saving it into Notion; implement a screen before testing its behavior. Carry
forward paths, design decisions, data, and unresolved constraints rather than restarting
discovery at every handoff.

## 3. Diagnose UI work before choosing aesthetics

Read [references/diagnosis.md](references/diagnosis.md) when platform, scope, or overlap is
unclear. Gather the brief, current implementation, existing visual system, and available
screenshots. Reuse evidence already collected in the session.

Determine platform first:

| Target | Implementation route | Supporting responsibilities |
|---|---|---|
| SwiftUI iOS / macOS | `swiftui-expert-skill` | `ios-ui-design` for HIG direction; native verification |
| Expo iOS / Android | `expo-overview` → relevant installed leaf | `expo-native-ui`, `expo-ui`, `expo-router`, `expo-animation`, `expo-design-system` as needed |
| Bare React Native, Kotlin/Compose, Flutter, other native stack | Existing stack and current official documentation | Applicable design guidance; do not assume Expo or convert frameworks |
| Website / web app | Select the web workflow below | Web-specific style, interaction, and QA specialists |

Inspect incumbent tokens, components, and `PRODUCT.md` / `DESIGN.md` when present.
Artifacts help identify the project's workflow; their absence does not erase an existing
design. A mostly empty scaffold is a new build, even if the user calls it a redesign.

For web work, optionally run `bash <lead-dir>/scripts/scan-fingerprints.sh <target>`.
Treat hits as review prompts, not defects or universal font/color bans. Do not run this
web scanner on native code or use it as the sole reason to replace a design.

## 4. Route design work

| Outcome | Primary route | Add only when relevant |
|---|---|---|
| New product UI, dashboard, component, or general website from a brief | `frontend-design` | Choose one visual direction; Impeccable new-work is also valid when following its managed workflow |
| Landing page / portfolio, no established Impeccable workflow | `design-taste-frontend` | One compatible style overlay |
| New surface in a project following Impeccable | `impeccable` and its current new-work playbook | `init` / `shape` only as that workflow requires |
| Existing interface critique or polish | `impeccable` with the matching playbook | Scope audit versus critique; preserve identity for refinement |
| Existing built-out app/site redesign outside that workflow | `project-ui-redesign` | Platform specialist for native implementation |
| SwiftUI implementation / review / native performance | `swiftui-expert-skill` | `ios-ui-design`; available native build/profile tools |
| Expo screens and native controls | `expo-overview` → `expo-native-ui` + `expo-ui` | Match installed SDK; real native controls before custom substitutes |
| Expo tabs / stacks / links / sheets | `expo-overview` → `expo-router` | Screen styling only if it changes |
| Expo gestures / transitions / haptics | `expo-overview` → `expo-animation` | Router and controls as needed; reduced motion |
| Expo shared tokens / component consistency | `expo-overview` → `expo-design-system` | Extend the existing theme |
| Web component behavior / subtle motion polish | `emil-design-eng` | Existing primary implementation; reduced motion and touch behavior |
| Web scroll choreography / GSAP | `ui-gsap-taste` | Existing web build workflow |
| Web accessibility / interaction code review | `web-design-guidelines` | Fetch its current rules; use Impeccable for broader visual/UX critique |
| Premium visual finish | `high-end-ui` | Existing build or refinement workflow |
| Warm editorial minimalism | `minimalist-ui` | Owns the style; no competing taste overlay |
| Brutalist / terminal / blueprint look | `brutalist-ui` | Owns the style; retain usability and accessibility |
| Brand / logo / identity board | `brand-kit` | Appropriate image tools; no automatic website build |
| Web concept images | `web-image-direction` | One image per section as specified by the specialist |
| Mobile concept images | `mobile-image-direction` | Images only; implementation is a separate deliverable |
| Website matching an image reference | `image-to-code` | Reuse the supplied reference; verify the rendered result |
| Sleek projects / screen generation | `sleek-mobile-design` | Requires configured service access; fetch generated code for implementation |
| Google Stitch design specification | `stitch-ui-design` | Produces a design specification, not a native app |
| Supporting design heuristics | `ui-ux-pro-max` | Reference within a selected workflow |
| Local web app behavior and regression checks | `webapp-testing` | Supported browser tooling |
| Reusable third-party browser automation | `playwright-builder` | `playwright` only if the environment permits that runtime |
| Browser task requiring the user's live session | `browser-harness` if permitted and available | Prefer sufficient connectors; preserve user tabs |

### Resolve overlaps without stacking conflicting instructions

- Assign ownership by responsibility: product/brand direction, platform correctness,
  interaction behavior, and verification. One specialist owns each responsibility per pass.
- Keep `frontend-design` available for general new builds. `design-taste-frontend` excludes
  dashboards, data tables, and multistep product UI.
- Prefer the incumbent Impeccable workflow when its context is already established.
  Read its current command reference rather than copying stale command lists here.
- Use native implementation specialists before web aesthetic rules on native apps.
  Preserve system typography, controls, accessibility, and platform navigation.
- Prefer `expo-ui` controls for controls it covers; use `expo-animation` for custom motion
  that remains necessary. Do not rebuild an available native sheet for animation's sake.
- Choose `emil-design-eng` for web interaction craft, `ui-gsap-taste` for web scroll
  choreography, and `expo-animation` for Expo motion. Similar intent is not interchangeable
  runtime code. The optional upstream `animate` skill is not assumed installed.
- Use `web-design-guidelines` for focused web code compliance; use Impeccable for broader
  hierarchy, visual quality, and UX. Run both only when their scopes add value.
- Choose one named aesthetic. Do not combine incompatible presets or let an overlay
  replace a pinned brand, accessibility requirement, or native convention.
- Generate concept imagery when requested or needed for a concrete asset. Do not force
  an image-approval round before an already-authorized implementation.

## 5. Execute, verify, and close the loop

Follow the selected specialist's workflow and its environment requirements. Keep scope tied
to the user request. An orchestrator coordinates work; it does not expand authorization.

- Web: exercise the main user task and relevant responsive/keyboard behavior. Use
  `webapp-testing` when it adds meaningful behavior verification.
- Native: use the existing build and simulator/device tooling when available; check
  navigation, safe areas, keyboard reachability, large text, and reduced motion as relevant.
  A web screenshot does not verify native behavior. Report unavailable native checks.
- Reviews: return findings without edits unless edits were requested.
- Non-UI: verify the specialist's actual output, such as item counts, saved records, or
  updated ranges. Do not substitute a UI review for completion evidence.
- Keep verification bounded: inspect, fix observed defects together, and confirm.
  Recheck further only for new failures or unresolved material concerns.
- Clean up task-owned browser tabs and temporary resources promptly. Preserve preexisting
  user tabs, sessions, work, and final deliverables.
- Report the result and meaningful validation in a few lines. Link the deliverable or
  changed source. Never claim a tool ran, a record saved, or a build passed without evidence.
