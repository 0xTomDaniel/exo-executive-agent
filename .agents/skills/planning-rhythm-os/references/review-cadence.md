---
aliases:
  - Review Cadence Policy
  - Weekly Review Process
---
# Review Cadence

> This file is the canonical operational reference for Sunday routing, review cadence, and weekly review flow.

## Core cadence rule

Reviews normally happen on **Sundays**.
On a given Sunday, review **every planning timeframe that is closing** that day.
The review should look back across the **entire duration** of that timeframe, not just the last few days.

## Covered timeframes
- [[Week]]
- [[Sprint]] (2 weeks)
- [[Cycle]] (6 weeks)
- [[Quarter]]
- [[Year]]

## Review stack order
If multiple periods close on the same Sunday, run them from **smallest to largest**:
1. Weekly review
2. Sprint review
3. Cycle review
4. Quarterly review
5. Yearly review

This lets higher-level reviews synthesize the lower-level ones created in the same session.

## Review-stack integrity
- Create/use the required review notes for every period closing that day before running the stack.
- Instantiating a higher-level review note is **not** the same as completing that review.
- Higher-level reviews may synthesize lower-level outputs, but each level still requires explicit discussion/confirmation before it counts as complete.
- If time/energy only allows a scaffold, label it explicitly as a draft / first-pass artifact and keep the review stack in progress.
- If the full review stack is not recoverable in the available window, choose an explicit graceful-degradation path: reduced review, minimum viable review, or intentional defer with a named re-entry point.
- Do not mark the current day review stack complete until each required level has actually been worked through with the user.
- If admin/inbox items interrupt a Sunday review, treat them as a bounded interruption: capture or clear them, then explicitly return to the review stack at the exact next unfinished review step. Do not answer "what's next?" with a normal admin/execution list unless the review stack has been closed or the user explicitly chooses to pause it.

## Balanced-life review lens
Every cadence review and next-period plan should explicitly consider:
- work / mission / craft
- health / body / recovery
- relationships / love / friendship / family
- hobbies / play / exploration / creative nourishment
- soul / meaning / spirit / inner life

The goal is not fake equal weighting. Startup-founder periods may be intentionally asymmetric. The rule is to make that asymmetry explicit: note what is being protected, what is being consciously deferred, and what minimum anchor keeps a non-work dimension alive.

## Weekly review semantics
- `review_week` = the ISO week being closed / reviewed
- `plan_week` = the upcoming ISO week being planned
- On Sunday, these are different weeks.
- Sunday's current day artifact still belongs to the current ISO week.

## Weekly review process
1. **Mind dump first**
   - Capture the user's raw thoughts in their own words before opening structured task views.
   - Do not pre-fill the mind dump from system summaries.
2. **Read the week back through day logs / daily artifacts**
   - Read every day log / daily artifact from the week, including chat/message logs.
   - Look for repeated blockers, hidden insights, and pattern signals.
3. **Review the current week**
   - Wins, misses, lessons, habits, notable constraints, and balance across work / health / relationships / hobbies / soul.
4. **Run backlog hygiene**
   - Open the relevant task surface (normally the system's current-week task view, plus overdue / surfaced items as needed).
   - Explicitly include overdue (`due < today`) and stale-review (`review_on < today`) debt; weekly reviews are the deep cleanup layer, but daily fall-through sweeps must still catch this debt if the review is missed.
   - Do not skip Sunday stale-debt cleanup merely because a cleanup task exists. If time/energy is constrained, run a lean pass: clear obvious Done/Drop/Someday items, recommit true current items, and create a dated cleanup block only for the remainder.
   - Distinguish metadata/surface hygiene from substantive review. Emptying an overdue/stale Base view is not enough; meaningful stale items should be batched and walked through with the user unless they are obvious mechanical completions or low-value incubations.
   - Hand off to `planning-task-os` and its canonical references for Now/Later/Drop rules, carry-forward logic, completed-task cleanup, and task-metadata updates.
5. **Explore the knowledge graph / resurfacing**
   - Preserve both lanes: planned/cadenced resurfacing and random rediscovery.
   - Revisit older journal entries, saved media, or forgotten notes when possible rather than only current tasks.
   - If a resurfaced item should matter next week/period, operationalize it before closing the review.
6. **Choose the Weekly MIT**
   - Name the single best lever for the upcoming week.
7. **Prepare next week**
   - Ensure the next week artifact and week plan exist; if the week artifact is missing, create it using the system's current week-artifact runtime surface.
   - Verify the next week artifact's cadence fields / period links are correct (for example `week_of_year`, `week_start`, `week_end`, `quarter`, `cycle`, `sprint`, `period_type`).
   - If the next week is a bonus week, surface it by name/dates/focus mode and do not create the next cycle's execution plan over it unless the user explicitly chooses that tradeoff.
   - Before starting a new cycle, check whether a scheduled bonus week lies between the closed cycle/quarter and the new cycle; if yes, instantiate/link the bonus-week artifact and future-facing reminder first.
   - Advance any period-scoped task surfaces / Bases / dashboards that are supposed to track the live current week / cycle / sprint, and validate them immediately after rollover.
   - Confirm hard dates, decision deadlines, and non-negotiable constraints.
   - Pre-select Monday Top 3 and the first deep-work block.
   - On Sunday, committed carry-forwards target `plan_week`, not `review_week`.
8. **Close out**
   - Before saying the review/planning is complete, explicitly state the habit score/assessment, planned resurfacing reviewed, random rediscovery reviewed, and overdue/stale debt disposition.
   - Link the review to the next-week plan.
   - Propagate Now / Later / Drop and carry-forward decisions into the real task notes / metadata.
   - Remove draft / provisional markers from finalized planning artifacts once the user confirms them.
   - Mark finalized planning artifacts as locked/planned once the user confirms them.
   - Write a concise sentence about what changes next week.

## Required review outputs
Each review should produce:
- reflection on wins, misses, lessons, and pattern changes
- balanced-life reflection plus explicit next-period protection / defer decisions across work, health, relationships, hobbies/play, and soul/meaning
- resurfaced items worth carrying forward now
- a handoff into the next period's plan
- explicit Now / Later / Drop decisions where relevant
- habit / operating-system observations

## Follow-up rule
Do not leave explicit post-review follow-ups as plain-text reminders inside ritual notes.
Examples:
- browser tabs
- admin capture
- relationship follow-up
- inbox cleanup

Before closing the review, either:
- complete them
- or convert them into explicit future-facing artifacts

## Runtime surface boundary
The canonical cadence-review procedure lives in this skill/reference, not in checklist notes or templates.
Runtime surfaces can point, prompt, and summarize, but if reusable review/planning procedure changes, migrate that logic here (or another relevant skill) rather than letting hidden canonical logic accumulate in a checklist.
Portable scaffolds for common cadence artifacts also live in `../assets/runtime-surfaces/`; local system templates may mirror/adapt them, but should not be the only copy needed for the skill to function.

## Templates / artifacts
Common runtime artifacts include:
- a weekly review artifact named `Weekly Review - YYYY-W##`
- a week artifact for the period being executed / planned
- a week-plan artifact for the upcoming week
- optional higher-level review artifacts for sprint/cycle/quarter/year

## Boundary with planning-task-os
Use this skill for cadence/review flow.
Use `planning-task-os` for:
- task property semantics
- carry-forward requirements
- Now / Later / Someday / Drop calibration
- `importance` / `due` / `review_on` / `status` updates
