# Skill: Create a reusable activity

## Purpose
Create one independently usable, version-controlled Markdown activity document, separate from any particular meeting plan. Use `templates/activity.md`. Read `AGENTS.md`, `reference/sections.md`, `reference/activity-history.md`, and `reference/badges.md` first.

## Workflow
1. Establish the activity's purpose, intended sections and age suitability, approximate duration, group size and venue constraints. Ask only for essential missing details; mark other unknowns TBC.
2. Search existing `activities/` entries by title, ID and tags to avoid duplication. Reuse or improve an existing activity when appropriate.
3. Give the activity a stable, descriptive, lowercase hyphenated ID. Store at `activities/<id>.md`. Never encode a meeting date in the ID.
4. Include YAML front matter: `id`, `title`, `sections` (array), `duration_minutes`, `group_size`, `tags`, and `badge_requirements` (array of badge ID and requirement ID references). Include source URLs where relevant.
5. Include leader-ready sections: purpose and observable objectives, kit with quantities and low-kit alternatives, setup, numbered steps, discussion prompts, adaptations/accessibility, safety hazards and controls, tidy/reset, and optional variations.
6. Use `skills/06-risk-assessment.md` to identify activity-specific risks. Do not treat a draft as an approved risk assessment. Reference any specialist assessment required.
7. Map to all plausible relevant badge requirements using **current official Scouts sources**. Distinguish `potential` from `verified` mappings. Do not claim a badge is awarded or a requirement completed without leader-confirmed evidence.
8. Validate clarity, age suitability, timing, practical kit availability, safety, valid IDs, and links. A leader unfamiliar with the activity should be able to run it.
9. Link the activity ID from meeting plans and session records instead of copying instructions. An activity can be reused across sections and dates.
10. Only record a use when a session record has `status: delivered` and an actual date. Creating or editing this file must never increase usage counts.

## Output
One Markdown file at `activities/<id>.md`, plus links from any relevant plans. If new badge IDs are needed, propose updates to `reference/badges.md`. Prefer review via pull request.

## Example
A reusable `astronaut-fitness-circuit` activity might be appropriate for Beavers, with a 10-minute duration, cones and floor tape, inclusive alternatives and a supervised no-contact route. Link to a Space badge requirement only after checking the current wording.
