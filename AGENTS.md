# Agent instructions: Scouts Activity Library

Primary tool: Codex. These instructions use the broadly supported AGENTS.md convention; all content and source-of-truth files are plain Markdown.

Before creating or modifying a meeting plan:
1. Read `reference/sections.md` for verified section ages, national duration guidance, and local overrides.
2. Read `skills/README.md`, the relevant files under `skills/`, and `templates/meeting-plan.md`.
3. Use the **local meeting schedule** when known, never silently replace it with national examples. If unknown, ask for the actual meeting start/end times or mark TBC.
4. Validate arithmetic: sum activities, ceremonies, rotations, transitions, tidy-up and departure time within the session window. Flag unrealistic durations or age-inappropriate tasks and suggest alternatives.
5. Check the official Scouts source when facts or requirements may have changed. Distinguish verified rules from typical guidance and local conventions.
6. Draft risk assessments for leader review, not as automatic safety approval. Never store identifiable young-person data.
7. Keep Markdown as the source of truth; link official documents, and generate binaries only when needed.

For section-specific defaults and citations, see `reference/sections.md`. Do not duplicate facts in multiple skills. Prefer a pull request for changes to shared instructions so they can be reviewed.

## Activity history
Read `reference/activity-history.md` before creating reusable activities or session records. Use `templates/activity.md` and `templates/session-record.md`. A Git commit does not prove delivery: only `status: delivered` with an actual date contributes to history. Keep badge requirement coverage separate from badge awards. Do not store identifiable young people's details.

When asked to create a reusable activity, follow `skills/08-create-reusable-activity.md` and write an independent `activities/<id>.md` document. Link it from meeting plans rather than duplicating its instructions.
