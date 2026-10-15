---
name: calendar-cleanup
description: "Reviews a week on Google Calendar for organizational inefficiencies (junk-drawer catch-all blocks, buried deadlines, threads scattered across days, overloaded time slots, duplicate info, vague titles) and proposes concrete batching/renaming fixes, then edits the calendar directly once approved."
---

# Calendar Cleanup

## Preferred calendar tool routing

When possible and helpful, prefer the connected
[google-calendar](app://connector_947e0d954944416db111db556030eea6) plugin/connector
for this skill's calendar operations. Route reads through its event-list/search
and read-event tools, and route approved changes through its create, update, and
delete-event tools. Use another available route only when it is more suitable,
more reliable, or necessary for the specific operation; do not force the plugin
when it is unavailable or would make the task worse. Browser control may be used
to identify the week the user is viewing and, if useful, visually verify the
result. Keep the user's calendar workflow intact and do not move items to Todoist
or another task app.

The user manages tasks by time-blocking them directly on Google Calendar rather than
in a separate to-do app. Titles are often terse or generic ("TODOs", "Work Tasks",
"Call Jon") while the actual substance — sub-items, links, deadlines, context — lives
in the event `description`. That's a deliberate, working system, not a mistake — the
job here is to make it *more efficient on its own terms*, not to replace it with a
different tool or workflow. The user has explicitly said they do NOT want items moved
into a separate task app like Todoist — everything stays as calendar events, just
organized into fewer, clearer, better-titled ones. Read descriptions as carefully as
titles; that's where most of the signal is.

The larger goal is to make intentions and life admin easier to keep moving, not to
maximize calendar tidiness or build a separate life-management system. When the user
asks for a weekly review, combine the event-level cleanup below with a short review
of loose ends and near-term capacity. Keep the calendar as the task system; do not
move tasks to Todoist or another app.

## 1. Figure out which week

In priority order:
1. If the user's request names a date range or week, use that.
2. If this is running in a browser session and a Google Calendar tab is open showing
 a specific week (check the tab title/URL, e.g. "7 days, starting Sunday, September
 13, 2026"), use that week — the user likely navigated there on purpose.
3. Otherwise default to the rolling 7 days starting today.

State which window you're reviewing up front in one line so the user can redirect
you if you picked wrong ("Looking at Aug 30–Sep 5...").

## 2. Pull everything, descriptions included

Use the Google Calendar connector's `list_events` for the window (primary calendar
unless the user says otherwise), then read each event's `description` field —
`list_events` may truncate or omit it, so call `get_event` on anything whose
description looks cut off or whose title alone doesn't tell you what it actually is.
Don't skip short/all-day/free-availability events — some of the highest-value catches
(a trip-booking deadline, a stock buy trigger) live inside otherwise easy-to-ignore
all-day events.

For a weekly attention review, use the requested week (or the default rolling 7 days)
as the detailed cleanup window, and inspect the following four weeks at a summary
level for existing commitments and open time. Read descriptions in detail for the
review week and for upcoming events that contain deadlines, unfinished project work,
or potentially duplicative tasks. Treat the four-week view as a capacity check, not
as a mandate to reorganize every event in that period. If the user asks only for a
calendar cleanup, keep the review focused on the selected week.

## 3. Look for these specific inefficiency patterns

Work through the week with these lenses. Not every week will have every pattern —
only report what's actually there, with the specific events named. Some weeks will
already be well-organized (e.g. a multi-leg trip correctly split into one event per
leg, each with a clear title and a rich description) — say so rather than manufacturing
issues that aren't there.

- **Junk-drawer blocks**: a generic title ("TODOs", "Tasks") whose description is a
 numbered list of unrelated items at wildly different stakes (e.g. "tape trunk" next
 to "book the Bolivia trip by Oct 17"). The real deadline item is getting the same
 visual weight as a trivial errand and can get lost. Flag high-stakes items buried
 this way as candidates for their own named event.
- **Same thread, scattered across days**: multiple separate events this week that are
 really one topic (car maintenance, a move, a trip, investing/finance, reaching out
 to specific people). List them together so the user can see the fragmentation, and
 propose batching them into one well-placed block with a combined checklist —
 especially when they're not sequentially dependent (no reason "call the mechanic"
 and "drop car off at mechanic" and "ask about brakes at mechanic" are three
 different days if they can be one visit).
- **Overloaded slots**: one event asking for multiple calls, multiple people's gifts,
 or multiple errands in a slot too short to plausibly fit them, or bundling
 unrelated people/topics that don't belong together just because they landed on the
 same day or in the same catch-all note.
- **Duplicate info**: the same to-do line copy-pasted into two different events'
 descriptions (search for repeated phrases across descriptions). Flag it — if it
 gets done via one event, the other still shows it as outstanding.
- **Vague titles**: a title that gives no signal of what's inside ("Ramy App",
 "Software was just Level 1") next to others that are perfectly clear from the title
 alone ("Call Ayman"). Propose renaming to match the actually-useful ones.
- **Stale recurring cleanup that isn't cleaning**: if there's a recurring
 "review/prune your tasks" style event, check whether the same low-value-looking
 items are still riding along week over week despite it. Worth naming as a pattern,
 not necessarily something to act on this run.
- **Loose ends and stale projects**: identify tasks that appear repeatedly without
  progress, projects that remain active across weeks, and one-off tasks that have
  lost urgency or a clear next action. Distinguish recurring routines and temporary
  project blocks from permanent workload before calling the calendar overloaded.
- **Near-term capacity**: compare proposed next steps with the upcoming four weeks,
  including church, travel, work, routines, and workouts. Recommend only a few
  realistic next actions and place them where there is actual capacity; don't turn
  every open slot into task time.

## 4. Present findings, grouped by theme

Name the specific events (with day/time), say what's inefficient about the grouping,
and propose the concrete after-state — e.g. "Merge these 3 into one 'Car: Fairfax
mechanic' block on Monday with a combined checklist" rather than just "your car tasks
are scattered." Concrete beats abstract: the user should be able to say yes/no/tweak
per group without having to reconstruct what you mean.

When the user requested a weekly attention review, finish with a compact disposition
for the meaningful loose ends: **do**, **schedule**, **delegate**, or **drop**. Give
each kept item one concrete next action and, when useful, a realistic amount of time.
For scheduled items, propose a specific open slot or a small number of options that
fit the next four weeks. Treat "delegate" and "drop" as recommendations only; do
not contact anyone or remove calendar content without explicit approval. If a task's
owner, deadline, or importance is unclear, say what is uncertain instead of guessing.

## 5. Wait for approval, then implement directly

Don't touch the calendar until the user says which changes to make (all of them,
some of them, or with tweaks). Once approved, use the Google Calendar connector to:

- **Merge**: create one consolidated event at the best-fitting time/duration with a
 combined description (keep every sub-item and link from the originals — merging is
 about location, not about dropping content), then delete the redundant source
 events.
- **Split**: if a block is overloaded, break it into separate right-sized events
 instead of one that can't fit what's asked of it. When placing a new event on a day
 it didn't already occupy, pick a slot that doesn't conflict with anything already
 on the calendar that week.
- **Rename**: update vague titles to match the concrete, self-explanatory style the
 user already uses for their clearer events.
- **Surface buried deadlines**: pull a high-stakes item out of a junk-drawer
 description into its own appropriately-titled event, and remove it from the
 original description so it isn't duplicated.

Be careful with recurring events — a change should apply to a single instance unless
the user clearly wants the whole series changed; ask if it's ambiguous. Never delete
an event the user didn't approve removing, and never drop content from a description
during a merge — when in doubt, keep it.

## 6. Confirm what changed

Close with a short summary of what got merged/renamed/split/created, not a restated
list of the plan — the user already saw the plan and approved it.
