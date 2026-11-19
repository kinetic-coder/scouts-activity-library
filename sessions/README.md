# Session plans by section

Save each session under `sessions/Beavers/`, `sessions/Cubs/`, or `sessions/Scouts/` according to its `section:` metadata. Keep reusable activities in the top-level `activities/` folder.

Use one folder per session, with the plan and an `assets/` directory together:

```text
sessions/Cubs/<session-slug>/<session-slug>.md
sessions/Cubs/<session-slug>/assets/   # presentations and other night-of files
```

Every session plan must include an `# Artifacts` section (see `skills/09-artifacts.md`) with Markdown links that open the session's files. Shared reusable decks may stay under top-level `assets/`.

From a nested session plan, link to activities and shared assets with `../../../activities/...` or `../../../assets/...`, and to session assets with `./assets/...`. Update linked references and tests whenever moving a session file.
