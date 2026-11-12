# Voice-first session planning workflow (proposal)

Status: **Design proposal, not implemented**.

## Principles
- GitHub Markdown is the source of truth; retain existing file conventions until reviewed.
- ChatGPT voice and a future web editor use the same session and activity IDs.
- Brainstorm freely, but persist only agreed decisions to draft plans.
- Search the existing activity library before proposing new activities.
- Never treat a planned activity as delivered.
- Keep Scouts UK POR and badge requirements linked to verified, dated sources; adult leaders review safety and ratios.

## Session lifecycle
1. **Draft**: select section, date, location and section-specific template; discuss and save agreed activities and timings.
2. **Ready for review**: validate timings, kit, accessibility, supervision and risk-assessment coverage; flag unknowns.
3. **Approved**: leader explicitly approves; generate versioned leader pack from the approved revision.
4. **Completed**: record activities actually delivered and attendance; skip cancelled items.
5. **Retrospective**: collect feedback for the entire session or one activity at a time; reopen and regenerate packs if plans change.

## Section templates
Support Squirrels, Beavers, Cubs and Scouts, with hall and offsite variants. Hall routines should be configurable: opening flag break, Beaver chant or Cub howl as appropriate, closing flag down, section-specific prayer or reflection where applicable, next-week announcements, collecting possessions and dismissal. Do not assume every section follows the same routine.

## Suggested data model
Each activity has a stable `activity_id`, title, suitable sections, category tags, equipment, instructions, safety notes, and optional badge requirement references. Session plans reference activity IDs and specify planned duration, order, assigned leader and section.

An append-only **usage record** is created only for delivered activities:
- `session_id`, `activity_id`, `date`, `section` (squirrels/beavers/cubs/scouts)
- `leader`, `planned_minutes`, `actual_minutes`, `participants`
- `badge_requirements_covered`, `feedback`, `improvement_suggestions`

Store usage records centrally (e.g. JSONL or YAML) rather than rewriting activity files. Preserve historical observations. Suggest updates to activity instructions based on feedback, subject to leader approval.

## Voice-first interactions
- “Plan next Monday’s Beavers”: load section template and latest draft.
- “What have we done recently?”: search section-specific usage history and badge coverage.
- “Add that to the plan”: save an agreed decision.
- “Read back the timetable”: summarize current draft for hands-free review.
- “The relay took 18 minutes”: append feedback to the correct completed activity.
- “Review the whole night”: walk through the completed session, allowing skipped questions.

## Leader pack
Build deterministic, versioned Markdown/PDF output from an approved plan and referenced activities: timetable, leader assignments, equipment, instructions, safety/risk assessment references, supervision checks, and open questions. Generation must flag missing inputs rather than inventing them.

## Delivery phases
1. Audit current repository structure, templates, skills and scripts; agree backward-compatible schema.
2. Implement draft planning, activity IDs, usage log, post-session feedback and tests.
3. Implement validation and reproducible leader-pack generation.
4. Add programme variety/badge coverage reports and optional web interface.

## Open design questions
- Existing naming and metadata conventions in the repository.
- Whether leader names and participant counts should be stored in private GitHub history, and retention expectations.
- How to verify and refresh Scouts UK POR/badge requirement references.
- Whether the web interface writes through GitHub directly or via an authenticated backend.
