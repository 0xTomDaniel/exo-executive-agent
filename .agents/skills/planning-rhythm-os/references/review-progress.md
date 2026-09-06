# Review progress and resumption

This reference owns completion and resumption across daily startup, retrospective review, and next-period planning. Cadence discovery remains in `review-cadence.md`; reminder coverage in `resurfacing.md`; task lifecycle in `planning-task-os`.

## One record per scope

Store one `review-state` fenced JSON block in the actual daily/review/plan note for the scope being worked. Generate its initial shape with:

```bash
python3 scripts/review_state.py init --kind week --period 2026-W37 --phase planning
```

Kinds: day, week, sprint, cycle, quarter, year. Phases: startup, review, planning. Use actual period identity, never the example value by default. A week review and its next-week plan are separate scopes; a sprint plan is not confirmed by either week. Do not use one completion flag for an entire stack.

The generated record has mandatory steps, evidence references, coverage dates, missing-date resolution, unresolved decisions, exact next step, and confirmation. Update it through the approved persistence layer after each substantive step and before changing topic or ending an interrupted session. Preserve the user's raw capture separately from Exo synthesis.

## Beginning and resuming

1. Read the relevant period notes, recent dated reality, current habit roster and the existing progress record. Enumerate missing dates and missed boundaries. Missing notes/interactions are unknown evidence, not proof that a habit was skipped or done.
2. Discover the full review stack, including older open recovery artifacts. Record missing artifacts and uncertainty explicitly; do not treat absent review files as completed work or silently begin the next cycle.
3. Resume the exact unfinished step. Capture tangential items, then return to that step. Record task and non-task reminder query evidence; an empty task view alone cannot satisfy coverage.
4. A step may be complete only after the named work is actually performed. Attach source references to discussion, decisions, or checked records. Drafting a scaffold, updating a date, or naming a future task is not evidence that its substantive review occurred.

## Completion check

```bash
python3 scripts/review_state.py check /path/to/review-or-plan.md
```

Exit 0 means the recorded evidence/confirmation contract is structurally complete; 1 means work remains; 2 means the record is missing or malformed. Read the returned errors and next step. Only after a successful check **and cross-checking its evidence against the actual user discussion** may the scope's status be advanced. This helper is not independent proof of human agreement and is not a security boundary against its editor.

Record a user confirmation quote and source that explicitly apply to this scope and mode. Never manufacture historical consent or copy week confirmation to a sprint/cycle. A coherent reduced review may complete when the user explicitly accepts its omissions and remaining coverage; list each omitted step, rationale and source, and mirror those names in `confirmation.accepted_omissions`. An unresolved substantive decision stays open rather than being relabeled an omission just to pass the check.

Coverage can end Friday when Friday's retrospective is honestly finished and Sunday owns the weekend addendum. A blank missing-date list still needs an explicit `missing_dates_resolution` such as `none; all dates accounted for`. When dates are missing, state what is known, what remains unknown, and what limitation the user accepted. Do not impose the newest habit schedule on earlier dates.

## Existing records

Do not bulk rewrite historical statuses to fit this schema. For an already closed historical review, report legacy completion as unverified by this checker unless the source evidence is actually reconciled. Initialize a record when an unfinished scope is next resumed, carrying forward only the work supported by its current notes/transcript. Keep the exact unresolved handoff; adding a record does not confirm the review.
