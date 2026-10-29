# Repository skill catalog

Use this map to choose a specialist, then read its actual SKILL.md. Paths are relative
to this reference file. The linked label is the frontmatter name; a differing directory
alias appears in parentheses. Resolve aliases by file path rather than inventing commands.

The catalog covers all 60 active top-level skill folders at this revision,
including this orchestrator. New or changed sibling SKILL.md metadata takes precedence;
rediscover it when this map does not fit. Exclude system-reference snapshots from active
routing. Tools, connections, and local dependencies must still be available.

## Contents

- [Web workflows and visual direction](#web-workflows-and-visual-direction)
- [Native mobile implementation and design services](#native-mobile-implementation-and-design-services)
- [Brand, image concepts, and reference implementation](#brand-image-concepts-and-reference-implementation)
- [Browser operation, automation, and verification](#browser-operation-automation-and-verification)
- [Engineering and repository health](#engineering-and-repository-health)
- [Research, extraction, and file operations](#research-extraction-and-file-operations)
- [Notion and knowledge workflows](#notion-and-knowledge-workflows)
- [Personal productivity and connected accounts](#personal-productivity-and-connected-accounts)
- [Skill management, output support, and this orchestrator](#skill-management-output-support-and-this-orchestrator)

## Web workflows and visual direction

| Skill | Use for | Boundary / handoff |
|---|---|---|
| [frontend-design](../../frontend-design/SKILL.md) | Build new websites, dashboards, product screens, and components. | General new-build route; honor the existing stack and brand. |
| [design-taste-frontend](../../design-taste-frontend/SKILL.md) | Build or redesign marketing sites and portfolios. | Excludes dashboards, data tables, and multistep product UI. |
| [impeccable](../../impeccable/SKILL.md) | Managed UI design, critique, refinement, and current command playbooks. | Reuse incumbent context; load the command reference before acting. |
| [project-ui-redesign](../../redesign-existing-projects/SKILL.md) (folder: `redesign-existing-projects`) | Redesign an existing built-out interface. | Needs an incumbent; platform specialists own native implementation. |
| [high-end-ui](../../high-end-visual-design/SKILL.md) (folder: `high-end-visual-design`) | Apply premium typography, spacing, color, and finish. | Visual overlay; avoid competing style presets. |
| [ui-gsap-taste](../../gpt-taste/SKILL.md) (folder: `gpt-taste`) | Build advanced GSAP and scroll interactions for websites. | Web motion, not native gesture code. |
| [emil-design-eng](../../emil-design-eng/SKILL.md) | Polish web components, interactions, transitions, and perceived performance. | Interaction specialist, not a second full redesign. |
| [minimalist-ui](../../minimalist-ui/SKILL.md) | Apply warm, restrained editorial styling. | Owns aesthetic decisions for that pass. |
| [brutalist-ui](../../industrial-brutalist-ui/SKILL.md) (folder: `industrial-brutalist-ui`) | Apply Swiss, terminal, mechanical, or blueprint styling. | Owns aesthetic decisions; preserve task usability. |
| [ui-ux-pro-max](../../ui-ux-pro-max/SKILL.md) | Consult static UI/UX and accessibility heuristics. | Supporting reference, not the default critique workflow. |
| [web-design-guidelines](../../web-design-guidelines/SKILL.md) | Review web UI code against current Vercel interface guidelines. | Fetch current rules; focused code review rather than full visual redesign. |

## Native mobile implementation and design services

| Skill | Use for | Boundary / handoff |
|---|---|---|
| [ios-ui-design](../../mobile-ios-design/SKILL.md) (folder: `mobile-ios-design`) | Choose iOS HIG patterns and native SwiftUI design direction. | Pair with SwiftUI Expert for implementation correctness. |
| [swiftui-expert-skill](../../swiftui-expert-skill/SKILL.md) | Implement, review, or refactor SwiftUI across iOS and macOS. | Includes layout, state, animation, accessibility, and profiling references. |
| [expo-overview](../../expo-overview/SKILL.md) | Identify Expo goals, SDK constraints, and the right installed leaf. | Use for actual Expo/EAS work; optional upstream modules may be absent. |
| [expo-native-ui](../../expo-native-ui/SKILL.md) | Build native-feeling Expo screens and platform styling. | Consult expo-ui for native controls; router and animation own their layers. |
| [expo-ui](../../expo-ui/SKILL.md) | Use real SwiftUI/Compose controls through @expo/ui. | Check SDK support; use virtualized RN lists for large data. |
| [expo-router](../../expo-router/SKILL.md) | Implement Expo stacks, tabs, sheets, links, and navigation. | Navigation responsibility, not a whole styling or animation workflow. |
| [expo-animation](../../expo-animation/SKILL.md) | Implement Expo motion, gestures, haptics, and keyboard-driven UI. | Respect reduced motion and UI-thread behavior. |
| [expo-design-system](../../expo-design-system/SKILL.md) | Create or maintain Expo tokens and reusable component conventions. | Extend the incumbent theme instead of introducing a second system. |
| [sleek-mobile-design](../../sleek-design-mobile-apps/SKILL.md) (folder: `sleek-design-mobile-apps`) | Create, inspect, or edit Sleek projects and screens. | Requires configured Sleek access; use returned code when implementing. |
| [stitch-ui-design](../../stitch-design-taste/SKILL.md) (folder: `stitch-design-taste`) | Produce semantic design-system instructions for Google Stitch. | Design specification; not application implementation. |

## Brand, image concepts, and reference implementation

| Skill | Use for | Boundary / handoff |
|---|---|---|
| [brand-kit](../../brandkit/SKILL.md) (folder: `brandkit`) | Generate brand identity, logos, guidelines boards, and visual worlds. | Brand output, not an automatic app build. |
| [web-image-direction](../../imagegen-frontend-web/SKILL.md) (folder: `imagegen-frontend-web`) | Generate website section design references. | One horizontal image per section; images are not working code. |
| [mobile-image-direction](../../imagegen-frontend-mobile/SKILL.md) (folder: `imagegen-frontend-mobile`) | Generate mobile screen and flow concepts. | Image deliverable; follow with native implementation only if requested. |
| [image-to-code](../../image-to-code/SKILL.md) | Implement a website from a supplied or generated visual reference. | Use for visual fidelity; not the native implementation default. |

## Browser operation, automation, and verification

| Skill | Use for | Boundary / handoff |
|---|---|---|
| [webapp-testing](../../webapp-testing/SKILL.md) | Verify a local web application's behavior and rendered UI. | Use available browser tools; match tests to the changed behavior. |
| [playwright](../../playwright/SKILL.md) | Automate a browser through the supported terminal runtime. | Browser operation; follow current session restrictions. |
| [playwright-builder](../../playwright-builder/SKILL.md) | Build or repair a reusable third-party browser script. | Prefer repeatable automation over a one-off extraction. |
| [browser-harness](../../browser-harness/SKILL.md) | Use a permitted existing Chrome/CDP session. | Live session must be available; connectors take precedence when sufficient. |
| [chrome-extension-development](../../chrome-extension-dev/SKILL.md) (folder: `chrome-extension-dev`) | Build, debug, and test Chrome extensions. | Manifest, content scripts, popup, and background behavior. |

## Engineering and repository health

| Skill | Use for | Boundary / handoff |
|---|---|---|
| [anthropic-api](../../claude-api/SKILL.md) (folder: `claude-api`) | Build with Claude API, Anthropic SDKs, or Agent SDK. | Only for Anthropic-specific work. |
| [mcp-server-builder](../../mcp-builder/SKILL.md) (folder: `mcp-builder`) | Build an MCP server integration. | Server architecture and tool design, not ordinary app UI. |
| [code-simplifier](../../code-simplifier/SKILL.md) | Refactor for clarity while preserving behavior. | Use when cleanup is requested; avoid unrelated rewrites. |
| [project-audit](../../project-auditor/SKILL.md) (folder: `project-auditor`) | Review project or portfolio health and technical debt. | Scope to requested projects; do not run a portfolio audit automatically. |
| [repo-secret-sweep](../../repo-secret-sweep/SKILL.md) | Audit owned repositories for accidentally committed secrets. | Explicit sweep scope; never expose discovered secret values. |

## Research, extraction, and file operations

| Skill | Use for | Boundary / handoff |
|---|---|---|
| [ai-weekly](../../ai-weekly/SKILL.md) | Run Kero's AI watch digest. | Use its named digest workflow; dependencies may be environment-specific. |
| [web-scraper](../../web-scraper/SKILL.md) | Extract structured public web data with HTTP parsing. | Use when a connector or interactive session is not needed. |
| [instagram-post-scraper](../../instagram-scraper/SKILL.md) (folder: `instagram-scraper`) | Extract tagged businesses, accounts, and places from Instagram posts. | Post content extraction, not follower relationships. |
| [instagram-followers](../../instagram-followers-scraper/SKILL.md) (folder: `instagram-followers-scraper`) | Export Instagram follower or following relationships. | Reusable script and CSV output; requires supported session access. |
| [notebooklm-bulk-research](../../notebooklm-scraper/SKILL.md) (folder: `notebooklm-scraper`) | Gather bulk source material for NotebookLM research. | Research and ingestion across a structured entity list. |
| [notebooklm](../../notebooklm/SKILL.md) | Query or manage NotebookLM notebooks and source ingestion. | Requires supported service access. |
| [semantic-file-extractor](../../bulk-extract-semantic/SKILL.md) (folder: `bulk-extract-semantic`) | Extract cross-file themes, facts, and searchable meaning. | Content analysis across files, not file reorganization. |
| [bulk-file-operations](../../bulk-file-operations/SKILL.md) | Rename, organize, deduplicate, merge, or move many files. | Use reversible plans and count checks. |

## Notion and knowledge workflows

| Skill | Use for | Boundary / handoff |
|---|---|---|
| [notion-lookup](../../notion-lookup/SKILL.md) | Find a Notion page or database by name. | Resolve the target before edits; verify lookup freshness if needed. |
| [notion-api](../../notion-api/SKILL.md) | Use the Notion REST API when connected tools are insufficient. | API fallback, not the first choice over a sufficient connector. |
| [notion-recipe-creator](../../notion-recipe-creator/SKILL.md) | Create structured Notion recipes from dishes or source material. | Recipe database workflow, not generic Notion content. |
| [notion-travel-links](../../notion-travel-links/SKILL.md) | Save destination-plus-URL content to Notion travel pages. | Travel link ingestion; use lookup for finding a page. |

## Personal productivity and connected accounts

| Skill | Use for | Boundary / handoff |
|---|---|---|
| [todoist-api](../../todoist-api/SKILL.md) | Read or change Todoist tasks, projects, and labels. | Task data operations through supported tools/CLI. |
| [todoist-router](../../todoist-task-router/SKILL.md) (folder: `todoist-task-router`) | Classify and execute Todoist Inbox workflows. | Use its route configuration and applicable authorization. |
| [calendar-cleanup](../../calendar-cleanup/SKILL.md) | Review a calendar week and apply authorized organization fixes. | Calendar efficiency, not yearly reflection. |
| [yearly-review](../../yearly-review/SKILL.md) | Summarize a requested calendar year from Google Calendar. | Read-only review, not event edits. |
| [email-cleanup](../../email-cleanup/SKILL.md) | Review Gmail filing, junk, and proposed filters. | Apply only authorized filing, trash, and filter changes. |
| [drive-organizer](../../gdrive-organizer/SKILL.md) (folder: `gdrive-organizer`) | Organize Drive files or a folder collection. | File organization; preserve its applicable approval boundary. |
| [personal-finance-reporting](../../personal-finance-reporting/SKILL.md) | Update Kero's Monthly Finances Budget from connected finances. | Specific budget reconciliation, not general investment research. |
| [linkedin-profile-cleanup](../../linkedin-cleanup/SKILL.md) (folder: `linkedin-cleanup`) | Improve headline, about, experience, and skills on LinkedIn. | Use its before/after review and authorized edit workflow. |

## Skill management, output support, and this orchestrator

| Skill | Use for | Boundary / handoff |
|---|---|---|
| [skill-discovery](../../find-skills/SKILL.md) (folder: `find-skills`) | Discover suitable installable skills. | Search when a capability is missing or discovery is requested; no automatic install. |
| [improve-skills](../../improve-skills/SKILL.md) | Audit skill quality, routing, and usage; apply requested repairs. | Read-only unless repair scope is authorized. |
| [full-output](../../full-output-enforcement/SKILL.md) (folder: `full-output-enforcement`) | Ensure exhaustive code or other unabridged output. | Supporting output policy; does not select the implementation workflow. |
| [concise-response](../../caveman/SKILL.md) (folder: `caveman`) | Apply the explicitly requested compressed response style. | Communication overlay; does not change task scope or correctness. |
| [ui-design-lead](../../ui-design-lead/SKILL.md) | Coordinate the repository's skill workflows. | Do not recursively dispatch back to this orchestrator. |

