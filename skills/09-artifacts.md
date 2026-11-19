# Skill: Artifacts

Every session plan must include an `# Artifacts` section. Do not omit it.

## Required behaviour
1. Create or use a session `assets/` folder next to the plan when the session has presentation, printable, or other leader-facing files (for example `sessions/Cubs/<session-slug>/assets/`).
2. List each artifact as a Markdown link whose label is the human name and whose target is the relative path to the file. Clicking the link must open that artifact (presentation HTML, answer sheet, printable, and so on).
3. Prefer one primary launch link when a chooser/menu page exists (for example a quiz selection presentation). Also link secondary sheets leaders need on the night.
4. Keep reusable activity kit under top-level `assets/<activity-id>/` when shared across sessions; still link those files from this session's Artifacts section when the session uses them.
5. If the session truly has no files, write `None` under `# Artifacts` rather than removing the heading.
6. Before finishing, verify every artifact link resolves to an existing path from the session plan file.

## Example
```markdown
# Artifacts
- [Quiz night presentation](./assets/presentation.html) — choose a quiz and project the slides
- [Music quiz leader answers](../../../assets/cubs-music-quiz/answers.html)
- [Marvel quiz leader answers](../../../assets/cubs-marvel-quiz/answers.html)
```

Session layout for that example:

```text
sessions/Cubs/<session-slug>/<session-slug>.md
sessions/Cubs/<session-slug>/assets/presentation.html
```
