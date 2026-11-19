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
8. Every session plan must include an `# Artifacts` section per `skills/09-artifacts.md`: Markdown links that open the real files (session `assets/` presentations, answer sheets, printables). Use `None` only when there are no artifacts.
9. For any web page, presentation, answer sheet, printable or generated visual output, read and follow `skills/10-visual-formatting-and-accessibility.md`. Reuse the shared styles under `assets/styles/`; do not create a new visual system inside an individual artifact.

For section-specific defaults and citations, see `reference/sections.md`. Do not duplicate facts in multiple skills. Prefer a pull request for changes to shared instructions so they can be reviewed.

## Activity history
Read `reference/activity-history.md` before creating reusable activities or session records. Use `templates/activity.md` and `templates/session-record.md`. A Git commit does not prove delivery: only `status: delivered` with an actual date contributes to history. Keep badge requirement coverage separate from badge awards. Do not store identifiable young people's details.

When asked to create a reusable activity, follow `skills/08-create-reusable-activity.md` and write an independent `activities/<id>.md` document. Link it from meeting plans rather than duplicating its instructions.

## Leader packs
Keep meeting plans concise and link reusable activities by stable ID. For a self-contained printable pack, run `python scripts/build_leader_pack.py <session-plan.md>` or the `Build leader pack` GitHub Action. See `docs/leader-packs.md`. Do not manually duplicate activity instructions into source plans; generated packs are disposable output.

## Visual formatting and accessibility

- Use the current official UK Scouts brand guidance as the visual source of truth. The core digital colours are Scouts Purple `#7413dc` and Scouts Teal `#088486`; use Nunito Sans first with system fallbacks. Do not invent, redraw or modify a Scouts logo. Only use an approved logo asset when the repository has a documented right to use it.
- Reuse `assets/styles/scouts-core.css` and the appropriate shared page, presentation or printable stylesheet. Do not paste a separate colour palette or full CSS theme into a session artifact.
- Use the shared Material-inspired semantic surface tokens for a clean, modern interface. Every HTML page and artifact must load `assets/scripts/theme.js` and expose the accessible Light/Dark selector. Do not hard-code a page to one colour theme.
- Target WCAG 2.2 AA. Provide semantic landmarks and heading order, keyboard access, a visible focus indicator, text alternatives, labels, sufficient contrast, and controls at least 44 by 44 CSS pixels. Never encode meaning by colour alone.
- Layouts must reflow at 320 CSS pixels and at 200% browser zoom without page-level horizontal scrolling. Wide data tables may use a labelled, keyboard-focusable scroll region. Use responsive type and spacing; body copy must be at least 16px.
- Presentations must have on-screen Previous, Reveal and Next controls, support keyboard operation, announce slide changes accessibly, never auto-advance, and remain usable without animation. Printables and plans must include deliberate print styles.
- Keep artifacts offline-capable: do not load fonts, scripts, analytics or images from third parties. Respect reduced-motion, high-contrast/forced-colour and browser font preferences.
- Validate source and generated output before review. A page looking correct on one desktop width is not sufficient evidence of accessibility or responsiveness.


## Mandatory privacy rules for AI-authored and published content

**Never write personally identifiable information (PII) into any repository Markdown file, generated HTML, presentation, leader pack, attachment, test fixture, or Git commit message.** Treat all content as potentially publicly accessible through GitHub Pages, including drafts and previous Git history. This applies to adults as well as children and to indirect identification through combinations of details.

- Do not include real names, initials linked to a person, dates of birth, ages tied to an individual, photographs of identifiable people, personal email addresses, phone numbers, home addresses, precise locations of individuals, medical/disability information, safeguarding incidents, attendance registers, individual behaviour or performance notes, emergency contacts, or account identifiers.
- Use non-identifying roles such as "Duty leader", "Station leader", "Cub A", or aggregate participant counts. Avoid even pseudonyms when a combination of details could re-identify someone.
- Organisation names, generic meeting locations and dates may be used only when they cannot identify an individual or disclose sensitive information. Never copy personal details from user messages, connected sources or uploads into the repository.
- If a request requires PII, **stop that part of the task** and explain that it belongs in an approved, access-controlled Scout system, not GitHub or GitHub Pages. Ask for a redacted alternative. Do not silently include it in a private branch: Git history persists.
- Before writing or committing, inspect Markdown, front matter, links, embedded media, generated HTML and diffs for direct and indirect identifiers. Remove them before commit. Avoid third-party resources that could expose personal data.
- Generated Pages content must be reviewed for privacy before deployment. A successful automated scan does not establish that content is safe: scanners cannot reliably detect every name, photo or identifying context.
- Apply these rules to all sections and all future AI agents, including Codex and Copilot. Treat privacy violations as blockers, not warnings.
