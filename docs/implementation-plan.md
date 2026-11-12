# Existing repository audit and implementation plan

Date: 2026-11-12
Status: Proposed, based on inspected files on `master`.

## What already exists
- `AGENTS.md`: agent rules for planning, history and leader packs.
- `reference/sections.md`: local section times and Scouts source links.
- `reference/activity-history.md`: stable IDs, delivered-only counting and dashboard definitions.
- `reference/badges.md`: referenced as canonical badge catalogue (contents not yet audited).
- `skills/README.md` and `skills/08-create-reusable-activity.md`: section authoring and reusable activity workflow.
- `templates/meeting-plan.md`, `templates/activity.md`, `templates/session-record.md`: Markdown/YAML templates.
- `scripts/build_leader_pack.py`: stdlib-only assembler that reads activity IDs from front matter or links and generates a self-contained Markdown pack.
- `docs/leader-packs.md`: documents local generation and a GitHub Action. The action itself has not yet been inspected.

## Gaps and compatibility issues
1. Existing session records use `planned|delivered`, while the proposed lifecycle has `draft|ready-for-review|approved|completed|retrospective`. Keep **planning approval status** separate from **delivery status** to avoid breaking existing history.
2. Existing usage counts are derived from delivered session records. Extend the same canonical records with per-activity outcomes (leader, planned/actual duration, participants, feedback) rather than create a conflicting second history.
3. Existing builder does **not** check approval status, validate POR or ratios, or create PDFs. It assembles Markdown and fails on missing referenced activities.
4. Section ceremony templates and voice-friendly resume/update conventions are not yet present in the inspected templates.
5. Existing dashboard automation, tests, full skills, session examples and workflow files still need inspection before implementation.

## Proposed backward-compatible schema
Retain existing session front matter fields `date`, `section`, `status` and `activities`. Add optional `planning_status: draft|review|approved` and an optional `activity_outcomes` collection keyed by stable activity ID. Preserve `status: delivered` as the sole signal for activity use counting. Record retrospective notes without changing delivery history. Confirm schema against real session files before coding.

## Implementation tasks
- [ ] Inspect real session/activity files, all skills, badge references, workflow definitions and any tests.
- [ ] Write compatibility fixtures for current Markdown plans and session records.
- [ ] Add per-section hall/offsite templates with configurable ceremonies.
- [ ] Extend session record schema with optional per-activity delivery feedback and safe leader attribution.
- [ ] Implement delivered-only history reporting by section, activity, year and badge-related sessions; add tests.
- [ ] Add voice-first planning/resume instructions with explicit agreed-change saving.
- [ ] Add approval and validation checks without silently changing the existing Markdown pack builder.
- [ ] Add PDF export and versioned outputs after Markdown generation is verified.
- [ ] Add dashboard and web UI later.

## Safety and data handling
Do not store identifiable young-person data. Confirm whether leader names are appropriate for the private repository, or prefer leader role/initials. Treat POR and badge information as dated, externally verified references; human leaders approve safety decisions.

## Immediate next step
Inspect representative session files and the GitHub Actions workflow before modifying implementation code. Avoid duplicating the already-present activity-history model or leader-pack script.
