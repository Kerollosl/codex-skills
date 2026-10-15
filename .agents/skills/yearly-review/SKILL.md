---
name: yearly-review
description: Review a requested calendar year and produce a thoughtful, growth-oriented summary grounded in the user's Google Calendar. Use for requests such as `/yearly-review 2025`; do not use for scheduling or calendar edits.
---

# Yearly Review

Create a clear, honest reflection of the requested year from the user's calendar. The goal is insight, not productivity scoring: surface themes, commitments, memorable periods, and useful patterns without treating calendar entries as proof that an activity happened or was completed.

## Scope the review

- Accept a four-digit year, normally through `/yearly-review YYYY`.
- Use the user's calendar timezone. If the requested year is the current year, review from January 1 through the current local time. If it is in the past, review the full calendar year. If it is in the future, explain that the period has not occurred and ask whether the user instead wants a planning review.
- Begin by listing calendars. Include calendars the user owns, including their primary calendar, rather than assuming `primary` contains the whole story. Include a readable calendar only when it clearly represents the user's commitments or the user asks for it.
- Retrieve the complete bounded window with explicit RFC3339 times. Page results fully; use smaller time windows when a calendar is dense. Do not silently drop later-in-year events because an API result was capped.
- Treat all-day events, recurring instances, and task-style calendar entries as calendar evidence. Label them accurately in the review.

## Analyze before interpreting

- Use titles, calendar names, times, recurrence, locations, and descriptions. Read full details for events that materially support a specific claim; descriptions often contain the real purpose of an entry.
- Separate recurring series from individual instances so daily routines, birthdays, holidays, or task reminders do not swamp the narrative. Report repeated commitments as patterns and use one-off events for moments, projects, trips, appointments, or milestones.
- Group the year into a small set of human-readable themes based on the actual calendar content. Calendar names can guide grouping but are not conclusions by themselves.
- Identify meaningful patterns such as sustained habits, seasonal shifts, focused stretches, variety, recurring care/maintenance, or commitments that repeatedly displaced each other. Treat overlaps, reschedules, and missing events cautiously; they may be intentional or incomplete data.
- State the difference between calendar facts and interpretation. Avoid medical, psychological, or moral judgments, and do not infer achievement, attendance, or relationships beyond what the calendar directly supports.

## Default response shape

Keep the response reflective but concrete:

1. **Period and coverage** — exact window, calendars reviewed, event count, and any relevant limits.
2. **At a glance** — a short portrait of the year, with the dominant themes and the most informative time or recurrence patterns.
3. **What you made room for** — recurring commitments and sustained priorities, with representative calendar evidence.
4. **Notable chapters** — the most meaningful projects, events, trips, care, celebrations, or transitions found in the period.
5. **A few growth reflections** — 3–5 kind, specific observations that could help the user decide what to continue, reduce, protect, or explore. Phrase these as invitations, not verdicts.
6. **A next-review prompt** — a compact question or two for journaling or the next planning session.

Use dates, counts, and examples when they make a point clearer. Omit any section that the calendar cannot support. Do not pad the response with generic self-improvement advice.

## Safety and follow-through

- This skill is read-only. Do not create, move, update, or delete calendar events, or write a document/spreadsheet, unless the user separately asks for that outcome.
- If the user asks for a report artifact after reading the review, use the appropriate document or spreadsheet workflow and preserve the distinction between factual calendar data and interpretation.
- If a Calendar connector is unavailable or a calendar cannot be read, say which coverage is missing and provide the best bounded review possible.
