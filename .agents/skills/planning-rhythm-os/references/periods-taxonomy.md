---
aliases:
  - Planning Periods Taxonomy
---
# Planning Periods Taxonomy

> This file is the canonical operational reference for planning-period hierarchy and cadence metadata.

## Canonical terms
- [[Year]]
- [[Quarter]]
- [[Cycle]] (6 weeks)
- [[Sprint]] (2 weeks)
- [[Bonus Week]]
- [[Week]]
- [[Day]]

## Planning cadence hierarchy
- [[Cycle]] (6 weeks) is the primary planning cadence.
- [[Sprint]] (2 weeks) is the secondary planning cadence for checkpointing and re-scoping inside the cycle.
- [[Week]] is the main execution/review rhythm for day-to-day commitments.
- [[Quarter]] and [[Year]] are primarily for directional framing, synthesis, and review rather than detailed commitment planning.
- Default rule: do not make detailed promises beyond the current 6-week cycle unless there is a true hard external commitment.

## Property conventions
- Categorical/entity fields use wikilinks.
- Machine dates use ISO values.
- Core **task** property semantics such as `importance`, `status`, `due`, and `review_on` belong to `planning-task-os`.

### Planning hierarchy properties
Use these when relevant:
- `week`
- `sprint`
- `cycle`
- `quarter`
- `period_type`
- `day_of_week`

### Bonus week modeling
- `period_type: [[Bonus Week]]`
- Optional `focus_mode`: [[Reflection]] | [[Catch-up]] | [[Cleanup]] | [[Recovery]] | [[Vacation]]
- Bonus weeks must have concrete `week`, `week_start`, and `week_end` anchors before the preceding cycle/quarter review is considered closed.
- A bonus week is a first-class cadence period, not a vague buffer. It must surface in the weekly review before it begins, the first morning start inside the week, and any next-cycle planning session that might otherwise overwrite it.
- Do not instantiate the next cycle's week plan over a scheduled bonus week unless the user explicitly chooses to sacrifice/defer the bonus week; record that tradeoff in the bonus-week note and in the plan that overrides it.
- Use a future-facing artifact (`review_on`, target week note, or target review note) so upcoming bonus weeks cannot rely on memory or passive quarter-note links.

## Day-level cadence metadata
Day logs / daily artifacts should carry:
- `week`
- `quarter`
- `cycle`
- `sprint`
- `period_type`
- `day_of_week`

For bonus weeks, `cycle` and `sprint` may be intentionally absent; `period_type: [[Bonus Week]]` and the bonus-week link/focus mode are the routing-critical fields.

In note-based systems, these may be generated at note-creation time via templating.
The canonical source should be the corresponding week artifact for that system.
That means weekly rollover should ensure the upcoming week artifact exists before dependent day artifacts are created.

## Sunday semantics
- Sunday still belongs to the current ISO week.
- Therefore, on Sunday:
  - the current day artifact remains tagged with the current week
  - the weekly review closes the current week
  - the week plan targets the next week starting Monday

More generally: on any Sunday, review whichever planning periods are closing that day.

## Naming conventions
- `Weekly Review - YYYY-W##`
- `Sprint Review - YYYY-C#-S#`
- `Cycle Review - YYYY-C#`
- `Quarterly Review - YYYY-Q#`
- `Yearly Review - YYYY`

## Design principle
Cadence metadata should make routing more obvious, not more confusing.
Day artifacts and runtime surfaces should support the real planning semantics rather than silently overriding them.
