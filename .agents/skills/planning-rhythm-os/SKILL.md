---
name: planning-rhythm-os
description: >-
  Daily/weekly planning-rhythm operating system, including day-of-week modes,
  morning-foundation rules, graceful-degradation/re-entry handling,
  resurfacing cadence, Sunday review/reset flow, weekly review process,
  review-stack semantics, and planning-period taxonomy.
  Use when the user is starting the day or week, needs cadence-aware routing
  (weekday vs Saturday vs Sunday), is running or redesigning
  weekly/sprint/cycle review flow, or is changing planning-period semantics,
  review surfaces, or day-level cadence metadata.
metadata:
  exo.category: general
---
# Planning Rhythm OS

Use this skill when the job is about **how the day/week/period should flow**, not just how individual tasks are represented.

## Core model

- Route by **mode and cadence**, not by assuming every day is a generic workday.
- Treat the day-routing surface as a **routing aid**, not the primary source of logic.
- Resolve the ritual-critical morning foundations before advancing to execution.
- Use graceful degradation for rhythm-critical rituals/reviews: full version → reduced explicit version → minimum viable version → intentional defer + named re-entry point. A broken step does not invalidate the day/week.
- Run the cadence layer as a Detect → Decide → Act → Review loop: detect the real mode/constraints, decide the day's lane, act inside the chosen mode, and review with explicit closeout.
- Preserve both resurfacing lanes: **planned/cadenced resurfacing** and **random rediscovery**.
- Treat open tasks with `due == today()` or `review_on == today()` as hard morning-start surfacing obligations; do not lock the day until each has been explicitly named and routed.
- Run a daily fall-through sweep for `due < today` and `review_on < today`; surface counts plus high-salience names/next actions before locking the day, and route cleanup debt rather than letting it disappear.
- Treat bonus weeks as first-class cadence periods that can override normal weekday execution mode; surface them explicitly before starting the next cycle.
- On Sundays, determine the full review stack from the periods that are actually closing.
- Run review stacks from **smallest to largest**.
- Treat this skill and its references as the **canonical operational source** for planning rhythm / cadence behavior unless explicitly superseded.
- Keep day-shaping execution tactics in skill references rather than scattering them through dashboard prose or day-log improvisation.
- Avoid duplicated planning-rhythm policy prose across the vault and the skill. Retire duplicated policy notes after migration; keep only the minimum breadcrumbs needed during transition.

## Default workflow

1. **Identify the rhythm job**
   - Distinguish between:
     - day-mode routing
     - morning-start / closeout flow
     - resurfacing / weekly-minimum surfacing
     - weekly review process
     - review cadence semantics
     - bonus-week routing / surfacing
     - planning-period taxonomy / metadata

2. **Read the right reference**
   - Read `references/daily-rhythm.md` for day-of-week modes, morning foundations, and closeout.
   - Read `references/review-cadence.md` for Sunday routing, weekly review flow, and review-stack semantics.
   - Read `references/resurfacing.md` for the canonical resurfacing / spaced-repetition rules.
   - Read `references/periods-taxonomy.md` for planning-period meanings and cadence metadata.
   - Read `references/execution-tactics.md` when shaping the execution part of a day, containing shallow/admin sprawl, or deploying named tactics such as Admin Strike.
   - If the task involves creating or revising daily/review/planning/week runtime surfaces, read the relevant scaffold under `assets/runtime-surfaces/` and treat that skill-owned asset as the portable source.
   - If the work also changes task schema, backlog triage, carry-forward metadata, or task-property semantics, read `planning-task-os` too.

3. **Use the note-system operation layer for persistence**
   - Use the system's note/persistence layer for notes, runtime surfaces, and structured trackers when appropriate.
   - Use filesystem edits for precise Markdown changes when safer.
   - Persist important cadence/rhythm decisions to the current day log and the relevant canonical instruction/pointer artifact.

4. **Keep cross-skill boundaries clear**
   - This skill owns day modes, rhythm, cadence, review flow, and period semantics.
   - `planning-task-os` owns task/backlog schema, `importance`, carry-forward metadata, and task calibration.
   - When weekly review flow reaches backlog hygiene or task-metadata updates, hand off to `planning-task-os` rather than duplicating those rules here.

5. **Validate after changes**
   - Re-read representative policy/runtime artifacts.
   - Check that day-level routing still matches weekday/Saturday/Sunday semantics.
   - Verify that review-stack logic still matches the current period notes.

## Guardrails

- Do not let the day-routing surface become the hidden source of truth for cadence logic.
- Do not advance from morning-start into execution while ritual-critical foundations remain implicit.
- Do not confuse graceful degradation with silent omission or lowered standards; if a ritual/review is reduced or deferred, name the reduced version or re-entry point explicitly.
- Do not treat the "at least one planned/cadenced resurfacing item" rule as permission to omit open tasks whose `due` or `review_on` is today.
- Do not report "no tasks surfaced" after checking only exact-today items; also check overdue and stale-review debt.
- Do not collapse Sunday review/reset into a normal execution day.
- Do not let a bonus week be silently overwritten by the next cycle's execution plan; if it is intentionally sacrificed, say so explicitly and record the tradeoff.
- Do not duplicate task-schema rules here that belong in `planning-task-os`.
- Do not maintain two full prose sources of truth for the same cadence logic.

## Reference map

- `references/daily-rhythm.md` — daily modes, morning foundations, weekly minimum radar, and closeout.
- `references/review-cadence.md` — Sunday routing, review stack, weekly review flow, and review outputs.
- `references/resurfacing.md` — planned/cadenced resurfacing and random rediscovery rules.
- `references/periods-taxonomy.md` — planning-period hierarchy, review-week vs plan-week semantics, and day-level cadence metadata.
- `references/execution-tactics.md` — bounded execution tactics that protect the main lane (for example Admin Strike and single-work-lane shaping).
- `assets/runtime-surfaces/` — portable daily/week/review/plan scaffolds (including day-routing surfaces and mode partials) that local systems may mirror or adapt without making vault templates the only copy.
