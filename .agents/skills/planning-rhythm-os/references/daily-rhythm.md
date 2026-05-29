---
aliases:
  - Daily Enforcement Protocol
---
# Daily Rhythm

> This file is the canonical operational reference for daily planning rhythm and mode routing. Do not duplicate the same policy prose elsewhere unless there is a strong reason.

## Day-of-week modes

### Period-type override — Bonus Week
- If the current week artifact has `period_type: [[Bonus Week]]`, that overrides normal weekday execution mode.
- Surface the bonus week by name, dates, and focus mode before setting Top 3 or starting work.
- Default lane: reflection, cleanup, recovery, catch-up, vacation, or the explicitly chosen focus mode—not automatic launch/execution mode.
- If urgent work must override the bonus week, record the tradeoff explicitly in the daily note and bonus-week note; do not let the next cycle silently consume the buffer.

### Monday-Friday — execution days
- Default mode: focused work / delivery.
- Open the current day surface and apply the current routing surface.
- Run normal daily planning: capture, resurfacing checks, Top 3, first deep-work block, hard commitments.
- Surface both resurfacing lanes when realistic:
  - at least one planned/cadenced resurfacing item from the system
  - and at least one random rediscovery item when possible
- Treat that "at least one planned/cadenced item" rule as a floor, not permission to omit open tasks whose `due` or `review_on` is today.
- Also run the daily fall-through sweep: check overdue tasks (`due < today`) and stale resurfacing tasks (`review_on < today`) so missed weekly reviews or busy days cannot let the system fill with hidden debt.
- Treat distraction control and deep-work protection as first-class.
- When shallow/admin residue threatens to sprawl, use a bounded tactic from `execution-tactics.md` rather than letting miscellaneous work leak across the whole day.
- Default execution-day surfaces include the structured task views that support due-today, resurfacing, overdue, and carry-risk work.

### Saturday — lighter day
- Default mode: recovery, leisure, relationships, errands, and core habits.
- Saturday is not a default hard-core workday.
- If work is needed, prefer the smallest context-fit action or a short intentional block.
- If a real work lane exists, prefer one intentional work lane and use a bounded admin tactic only when it protects that lane.
- Still surface at least one resurfacing item so the memory system stays alive.
- Keep obligations visible without turning the day into a weekday clone.

### Sunday — review / reset day
- Default mode: review stack + weekly reset.
- Determine the full cadence stack before any normal daily planning.
- Do cadence reviews before admin/inbox cleanup unless the user explicitly chooses otherwise.
- Sunday can still include habits, relationships, and light responsibilities, but it is not a standard execution day unless intentionally chosen.

## Morning foundations

At the day-shaping level, think in a Detect → Decide → Act → Review loop:
- **Detect** the real mode, current week `period_type` (especially bonus week), constraints, resurfacing, and missing reality from yesterday.
- **Decide** the day's lane and what gets protected versus deferred.
- **Act** inside that lane rather than staying in open-ended sorting.
- **Review** with explicit closeout so the next day starts from reality.

Before advancing to execution:
- if the previous day did not receive a real closeout, reconcile where it actually landed before locking today's plan
- if there are one or more missing/incomplete dates since the last Exo interaction, run interaction-gap recovery across all missing dates before locking today's plan: enumerate dates, ask for compact per-date reality/habit/ritual status, and create/update retroactive daily notes where meaningful reality surfaced
- if reconciliation surfaces date-specific accomplishments, habits, events, or reflections from a missing/incomplete day, update or create that actual target daily note retroactively with a clear source/creation marker; do not leave the actual day blank just because it was reported later
- verify the current week artifact exists and read its `period_type`; if it is missing, stop and create/repair it before assuming weekday execution mode
- if `period_type` is `[[Bonus Week]]`, surface the bonus week and focus mode explicitly before any normal planning
- confirm core habits / virtues for the current mode, including any named mandatory habit or day-specific weekly ritual from the visible habit roster; ask about it explicitly instead of hiding it behind generic "movement"
- surface the day's resurfacing items explicitly by name
- explicitly name every open task with `due` today or `review_on` today, and route each one (Top 3, Admin Strike, Later, delegation, or drop)
- run the fall-through sweep for `due < today` and `review_on < today`: name counts plus high-salience items/next actions, then decide whether to clear, defer, or schedule cleanup
- surface active weekly minimums as a radar check
- confirm non-negotiables / hard constraints

Think in terms of **ritual-critical foundations**, not isolated checklist boxes.

### Graceful degradation and re-entry
When the preferred daily rhythm breaks, do not collapse into "the system failed." Choose the strongest recoverable version:
1. **Full version** — run the ritual/tactic as designed.
2. **Reduced explicit version** — shorten it while keeping the structure visible.
3. **Minimum viable version** — do the smallest action that preserves continuity.
4. **Intentional defer + re-entry point** — explicitly defer and name when/how to restart.

Use this for morning foundations, closeout, resurfacing, weekly reset anchors, and other rhythm-critical steps. A lapse should become a concrete re-entry decision, not shame or silent omission. If deferring, record the re-entry point in the day note, task metadata, or the relevant review artifact.

### Interaction-gap recovery
When the user returns after one or more missed interaction days, recover continuity before locking the current day.

Use a compact by-date pass:
- What happened / where did the day actually land?
- Completed work, errands, relationship events, or notable constraints?
- Core habits: water, meditation, movement/training, planning/closeout.
- Named weekly rituals or mandatory habits for that date, especially Saturday run and Sunday yoga.
- Open loops that should carry forward into tasks, reviews, or future-facing reminders.

For one missed day, ask directly. For multi-day gaps, use a low-friction table or summary prompt and drill only into high-salience or uncertain dates. Create/update actual retroactive daily notes for meaningful day-specific reality.

### Weekly minimum radar
Surface important non-daily minimums during morning review so they do not disappear just because they are not due today.
Examples include:
- long-form reading sessions
- full weekly review
- training minimums
- Saturday run / mandatory movement reset or intentional substitute when blocked
- Sunday yoga / creative reset or intentional substitutes when blocked

## Resurfacing

Use two lanes:

### Planned / cadenced resurfacing
- `review_on`
- `due`
- week/sprint placement
- explicit plan/review commitments

### Random rediscovery
- older notes
- journal entries
- saved media
- graph exploration
- surprising linked notes

If a resurfaced item should matter in the current day or upcoming period, operationalize it into a task, plan line, decision checkpoint, or other future-facing artifact.

### Daily fall-through sweep
Every day is a fallback for cleanup and organization, even when the weekly review is missed or the day cannot support deep triage.
- Query exact-today obligations first (`due == today` / `review_on == today`) and route every matching open task by name.
- Then query older debt (`due < today` / `review_on < today`) before locking the plan.
- Surface counts plus the high-salience names and next actions: all `[[Extremely important]]` / `[[Very important]]`, imminent external deadlines, relationship/admin commitments, and current sprint/cycle items.
- If the stale list is too large for chat, do not silently omit it. Say how many remain, name the top items, and create a bounded cleanup block or review artifact to process the rest.
- Never describe the day as clear merely because no task is exactly due/reviewable today.

## Midday
- Re-check whether the day is still aligned with its intended mode.
- Re-scope if needed.
- Use named bounded tactics when they protect the main lane; do not let them silently expand into day-long miscellaneous work.
- In short windows before hard stops, prefer concrete context-fit next actions over large planning rituals.

## End of day / closeout
- Complete the end-of-day scorecard or review closeout appropriate to the mode.
- Carry forward unfinished work intentionally.
- Use `planning-task-os` for the exact task carry-forward metadata rules.
- Set the next relevant starting point for tomorrow.

## Design principles

- The active mode should be visually and operationally obvious.
- Important things should surface when they should.
- The day should match reality rather than forcing every day into the same workflow.
- The day-routing surface is a routing aid; policy/rhythm logic should not be buried only inside runtime-surface code.
- Portable daily-routing scaffolds should live with the skill (for example under `assets/runtime-surfaces/`); local note-system wiring may point to them directly or mirror/adapt them, but should not make a vault template the only copy.
