---
name: ember-weekly-planning
description: >-
  Run Ember's weekly Friday team review/planning session with Tom and Sebastian Varela, including recap-as-input, next-week planning, ICP refinement, customer/revenue experiments, sales-call commitments, separate economic-lane routing, and Monday launchpad creation. Use this skill whenever the user mentions Ember weekly recap, Friday review, Friday planning, Varela planning, Ember team planning, weekly sales experiment, ICP/customer-fit questions for Ember, or turning Friday recap into next-week execution—even if they do not explicitly say "skill" or "procedure".
---
# Ember Weekly Planning

Use this skill to run or maintain Ember's Friday team planning ritual. The session is not a generic weekly review: it is a startup operating meeting that uses the week's facts to create next week's customer/revenue plan.

## Core model

- Treat **recap as input** and **next-week execution as output**.
- Produce a Monday launchpad, not a reflective essay.
- Keep the ritual lightweight enough to run weekly with [[Sebastian Varela]].
- Run one main weekly customer/revenue experiment unless there is a deliberate reason to split focus.
- The external-evidence floor does not disappear when the product is unfinished. Use a mockup, flow, specification, backtest output, concierge/manual service, structured interview, pricing test, or commitment test when valid.
- Separate distinct economic lanes such as customer revenue, client/partner work, grants/funding, and salary/runway implications rather than blending them into one vague "cash" bucket.
- Preserve momentum: the team has learned that quick tangible artifacts create morale and feedback; stuckness drains both founders.
- Do not hide mutable weekly state inside this skill. Store actual plans, commitments, ICP changes, call lists, and outcomes in the user's note/task system.

## Default workflow

1. **Set the frame**
   - State: "Recap is input; next-week commitments are the output."
   - Confirm the target planning week and the review week.
   - Use the scaffold in `assets/runtime-surfaces/friday-team-planning-session.md` when creating a new session artifact.

2. **Capture raw recap first**
   - Ask Tom and Varela separately:
     1. What shipped this week?
     2. What did we learn?
     3. What slipped or took too long?
     4. What are we worried about?
     5. If next Friday felt obviously successful, what would be true?
   - Preserve raw wording before synthesis.

3. **Synthesize facts, not vibes**
   - Shipped / completed
   - Learned
   - Missed / slipped
   - Blockers / constraints
   - Strategic reality check:
     - cash / income reality
     - customer traction reality
     - funding / parallel economic-lane reality
     - team pace / commitment reality
     - morale / energy reality

4. **Choose next week's team MIT and outcome contract**
   - Make it a single shared outcome that would make the week clearly worthwhile.
   - State the externally observable finish line, explicit non-goals, fallback/bypass path, and at most one manually intensive enabler on the critical path.
   - Prefer customer/revenue evidence over internal polishing.
   - If the same gate missed last week too, do not carry it unchanged: continue deliberately, contract, bypass, change goal, add capacity/remove a lane, defer, or stop.
   - Example shape: "By next Friday, Ember has a precise customer thesis/persona and has run 7 high-signal sales calls against the founding-partner offer, producing evidence about whether first sales are reachable."

5. **Frame one weekly customer/revenue experiment**
   - This is a floor, not an optional add-on after product completion.
   - Use the lightweight experiment frame:
     - Hypothesis / question
     - Audience
     - Artifact or manual method
     - Action volume
     - Predicted signal
     - Disconfirmation signal
     - Decision rule next Friday
   - If the preferred product artifact is unavailable, choose the strongest valid lower-fidelity test rather than silently skipping external contact.
   - Use Riskiest Assumption Testing only as a lens. If assumptions are still fuzzy, do not force a full RAT apparatus; let customer contact reveal the assumptions.

6. **Refine ICP / qualification when relevant**
   - Use the qualification procedure in `references/icp-qualification.md`.
   - Read the current company/project note or weekly planning artifact for the live ICP; do not treat this skill as the source of current customer/persona state.
   - Convert vague audiences into testable qualification questions.
   - Distinguish:
     - prime sales target
     - high-signal discovery
     - learning-only call
     - not current ICP

7. **Commit by owner and capacity**
   - Assign Tom commitments.
   - Assign Varela commitments.
   - Assign joint commitments only when shared ownership is real.
   - Each commitment should have a clear deliverable or decision, capacity/timing, and required update—not just a work theme.
   - If either founder has no genuinely aligned lane or lacks capacity, plan from that reality instead of preserving aspirational shared ownership.

8. **Create the Monday launchpad**
   - First shared starting point
   - Tom's first block
   - Varela's first block
   - First customer/pitch action
   - Required artifact by Monday EOD

9. **Route separate economic lanes explicitly**
   - If a parallel client, partner, funding, grant, salary/runway, or strategic-pivot opportunity appears, name the lane and decide whether it belongs in next week's plan.
   - Record classification, owner, capacity, next external evidence, and what the lane displaces or is forbidden from displacing.
   - Do not let a parallel economic lane silently displace the weekly Ember customer/revenue experiment.
   - If the parallel lane matters next week, create a separate commitment/task with owner, timing, success criteria, and stop/review point.

10. **Prepare Sunday handoff**
    - Add a parking lot for Tom's Sunday Exo review.
    - Sunday review should sanity-check ambition, reconcile with Tom's whole-life weekly review, and polish Monday execution.
    - Do not treat the Friday team session as a replacement for Tom's personal weekly review.

## Output requirements

A completed Friday planning session should produce:

- Raw recap from Tom and Varela
- Fact-based synthesis of the week
- Strategic reality check
- Next-week team MIT plus externally observable outcome/release contract
- One primary customer/revenue experiment, even if it must use a lower-fidelity/manual artifact
- ICP / audience definition if relevant
- Commitments by owner, capacity, and required update
- Monday launchpad
- Sunday Exo handoff / parking lot
- Any explicit future-facing tasks needed for sales calls, customer list building, artifact work, or separate client/partner/funding follow-ups
- Explicit displacement/guardrail decisions for every separate economic or strategic lane

## Guardrails

- Do not let the session become only a recap.
- Do not let artifact polishing replace customer contact.
- Do not let product incompleteness become a blanket excuse for zero external evidence.
- Do not allow multiple legitimate tooling/product enablers to become serial release prerequisites without an explicit release contract and checkpoint.
- Do not keep the audience broad when the week requires sales calls.
- Do not conflate distinct economic lanes; separate customer revenue from client/partner/funding/salary implications when they affect planning.
- Do not let Varela/Tom commitments remain vibes; turn them into owner + deliverable + timing.
- Do not bury next actions only in the meeting note; create or update future-facing task artifacts where the user's system supports them.

## Reference map

- `assets/runtime-surfaces/friday-team-planning-session.md` — portable meeting scaffold.
- `references/icp-qualification.md` — procedure for turning live ICP state into sales-call qualification.
- Keep temporary deal-specific details in vault notes/tasks, not in this skill.
