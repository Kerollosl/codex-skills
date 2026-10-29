# Routing and diagnosis

Use this reference when the primary workflow is unclear. Start with the requested
deliverable and platform; only then select design or implementation specialists.

## Contents

1. [Task and platform](#task-and-platform)
2. [Evidence and scope](#evidence-and-scope)
3. [Overlap decisions](#overlap-decisions)
4. [Useful sequences](#useful-sequences)
5. [Verification](#verification)

## Task and platform

| User wants | Decide first | Route |
|---|---|---|
| Working code | Existing stack and new build versus incumbent | Platform implementation specialist |
| Visual concepts | Web/mobile/brand and image versus design-service output | Relevant image-direction, brand, or Sleek skill |
| Evaluation | Code compliance, visual UX, native correctness, or runtime behavior | Matching review specialist; no edits unless requested |
| Refinement | The concrete defect and existing visual identity | Focused playbook or native specialist |
| Redesign | Preserve versus replace, and whether a built-out interface exists | Incumbent workflow or project-ui-redesign |
| Design system | Existing theme, tokens, components, and platform | Expo Design System on Expo; incumbent web/native system elsewhere |
| Non-UI workflow | Requested account/data/file operation | Relevant section of the full catalog; no UI phases |

Platform examples:

- `*.swift` / SwiftUI project → SwiftUI Expert. Use iOS UI Design when HIG decisions need
  attention. Do not introduce a web stack or Expo merely because the task is a mobile app.
- `package.json` contains `expo`, or user explicitly requests Expo/EAS → Expo Overview,
  then only the needed installed leaf skills. Read the actual SDK version.
- Bare React Native, Compose, Flutter, or another native framework → keep that stack.
  Use applicable general design guidance and current official framework documentation.
- HTML/CSS/React/Vue/Svelte/etc. website → choose a web route. "Mobile responsive" is web
  adaptation, not a request for a native application.
- Native simulator/device unavailable → implement from source and report the verification
  limit; do not treat a browser rendering as proof that a native app works.

## Evidence and scope

Inspect what is available: task/PRD, audience, existing screens, target files, tokens,
shared components, assets, accessibility requirements, and supported device classes.
Preserve brand and behavior unless the user requests replacement.

Use `PRODUCT.md` / `DESIGN.md` as evidence of workflow, not as a binary quality check.
A missing file does not authorize replacing the current design. An empty scaffold is a
new build; a developed interface is an incumbent even without these files.

Optional web fingerprint scans surface candidates for inspection. Inter, black, centered
text, cards, gradients, and emoji are not intrinsically defects. A concrete problem is
"focus disappears on keyboard navigation" or "the primary action is hidden below the
keyboard," not "the scan found a banned color." Verify suspected defects against the brief,
rendered UI, and accessibility behavior.

State a short diagnosis only when useful: "Expo settings screen; inconsistent tokens and
custom controls; keep the existing theme and use native controls." Avoid scoring, fixed
phase banners, or repeated design-plan templates unless requested by a specialist.

## Overlap decisions

| Close alternatives | Choose by responsibility |
|---|---|
| Frontend Design vs Design Taste | General new product UI/components → Frontend Design; marketing/portfolio direction → Design Taste |
| Impeccable vs a fresh build skill | Follow established Impeccable context/playbooks when relevant; do not label other installed skills obsolete |
| Impeccable vs Project UI Redesign | Existing managed workflow or focused critique/refinement → Impeccable; built-out interface needing a redesign outside that workflow → Project UI Redesign |
| SwiftUI Expert vs iOS UI Design | Implementation, state, performance, modern API usage → SwiftUI Expert; HIG and native interaction choices → iOS UI Design |
| Expo Native UI vs Expo UI | Native screen structure/styling → Native UI; native controls and component selection → UI |
| Expo Router vs Expo Animation | Native navigation behavior → Router; custom gestures, haptics, worklets → Animation |
| Expo UI vs custom sheet motion | Use an available native sheet/control; only build custom motion when the task requires behavior it cannot provide |
| Emil vs GSAP vs Expo Animation | Web component interaction → Emil; web scroll choreography → GSAP; Expo motion → Expo Animation |
| Web Guidelines vs Impeccable | Web code compliance and accessibility rules → Guidelines; hierarchy, visual world, and broader UX → Impeccable |
| Browser Harness vs Playwright vs connector | Sufficient service connector first; permitted live session when required; supported isolated browser runtime otherwise |
| Web Scraper vs Playwright Builder | Public static HTTP extraction → Scraper; durable interactive site script → Builder |
| Semantic extraction vs file organization | Understand content across files → Semantic File Extractor; change names/locations/deduplicate → Bulk File Operations |
| Native implementation vs image concept | Match the deliverable; an image generation skill does not produce a working native app |

Consult the selected specialist's current SKILL.md for commands and required resources.
For Impeccable, read its Commands table and linked playbook; use the native variant where
provided. Do not freeze a duplicate command cheat sheet in this router.

## Useful sequences

Use only the steps demanded by the task:

- New Expo settings screen: Overview → Native UI + UI → Router if navigation changes →
  native behavior checks. Add Design System only when shared tokens/components need work.
- Expo theme cleanup: Overview → Design System, with Native UI for platform values.
  Preserve an existing NativeWind/Tamagui/other theme in its own idiom.
- SwiftUI form redesign: iOS UI Design if interaction choices need work → SwiftUI Expert →
  available build/device checks, including large text and keyboard reachability.
- Website build from a brief: Frontend Design (or Design Taste for marketing) → one
  compatible visual direction → behavior/visual verification.
- Website interaction polish: Emil Design Engineering → scoped browser checks.
- Accessibility-only code review: Web Design Guidelines → findings with locations.
  Do not redesign or edit merely because a review identified defects.
- Mobile concepts in Sleek: Sleek screen generation → screenshots; if implementation was
  also requested, fetch returned component code and hand it to the target platform route.
- Instagram places to Notion travel pages: Post Scraper → destination resolution/Lookup →
  Travel Links. Carry source URLs through rather than rediscovering them.
- Calendar or Gmail cleanup: relevant specialist only; preserve its actual approval
  boundary and any authorization already provided by the user.
- A one-property color fix: edit and verify the affected surface directly.

## Verification

Test what changed and the user journey it affects. Check meaningful edge/failure states
when they are part of the work. Respect specialist verification requirements and available
tooling. Report checks that could not run without claiming the result was verified.

Keep QA bounded. Do one inspection pass, batch observed fixes, and confirm; extend only
for a new failure or unresolved concern. Close task-created tabs promptly, retain user
tabs and deliverables, and finish with the result, useful validation, and a link.
