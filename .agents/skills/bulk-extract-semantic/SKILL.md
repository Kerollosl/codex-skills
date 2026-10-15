---
name: semantic-file-extractor
description: Extract and organize meaning from a large set of local files when the user needs cross-file themes, facts, or a searchable index.
---

# Bulk Extract Semantic

Extract insights from large file collections in one efficient pass.

## What This Does

Analyzes 10+ files and extracts:
- **Key concepts** — Main ideas, patterns, themes
- **Connections** — How files relate to each other
- **Summaries** — Condensed understanding per file + aggregate
- **Structure** — Organization, hierarchy, dependencies
- **Gaps** — What's missing or needs clarification

Handles:
- Text-heavy files (PDFs, docs, transcripts, videos)
- Code repositories (architecture, patterns, entry points)
- Large folders (automated chunking, batch processing)
- Mixed media (combines insights across formats)

## How to Use

**Bulk extract from a folder:**
```
/bulk-extract-semantic
Extract semantic knowledge from ~/my-project/docs
```

**Analyze a codebase:**
```
/bulk-extract-semantic
Understand the architecture of ~/code-projects/todoist-ai
```

**Process text collections:**
```
/bulk-extract-semantic
Extract themes from the 50 transcripts in ~/notes/interviews
```

## What You Get

- **Semantic summary** — Unified understanding of the collection
- **Per-file insights** — Key concepts from each file
- **Connections** — Relationships and dependencies
- **Structured knowledge** — Ready to save to /graphify or knowledge base
- **Gap analysis** — What's unclear or incomplete

## Compared to Manual Extraction

| Manual | With Skill |
|--------|-----------|
| 1 file at a time | All files batched together |
| Repeated setup per run | One setup, multiple files |
| Misses connections | Finds patterns across files |
| Takes 20+ min | Takes 5-10 min |

## Example Scenarios

**Scenario 1: Large codebase**
```
/bulk-extract-semantic
Extract knowledge from ~/code-projects/bulk-gcal-mover/
→ Analyzes code.gs, index.html, CLAUDE.md together
→ Returns: Architecture (FullCalendar + GAS), key patterns (event caching, filtering), dependencies
```

**Scenario 2: Document collection**
```
/bulk-extract-semantic
Process all PDFs in ~/research/papers
→ Handles 15+ papers in one pass
→ Returns: Main themes, conflicting conclusions, citation patterns, research gaps
```

**Scenario 3: Video transcripts**
```
/bulk-extract-semantic
Extract insights from ~/notes/video-transcripts
→ Chunks long transcripts automatically
→ Returns: Key takeaways per video, common topics, actionable insights
```
