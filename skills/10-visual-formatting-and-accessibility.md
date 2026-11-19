# Skill: Visual formatting and accessibility

Use this skill whenever creating or changing a session page, activity page, presentation, answer sheet, printable, leader-facing HTML file or the Pages renderer. Content remains Markdown-first; HTML artifacts should be created only where interactivity, projection or a deliberate printable layout is useful.

## Brand rules

1. Check the current [official UK Scouts brand guidance](https://www.scouts.org.uk/volunteers/running-things-locally/local-media-and-member-communications/our-brand/) when brand requirements may have changed.
2. Use Scouts Purple `#7413dc` as the core colour and Scouts Teal `#088486` as the primary supporting colour. Use the shared tokens in `assets/styles/scouts-core.css`, not locally retyped approximations.
3. Prefer `Nunito Sans`, then the repository's system fallback stack. Do not add third-party font requests: resources must continue to work offline and must not expose visitor data.
4. Use colour with restraint and strong contrast. Do not use black text on yellow as general decoration because UK Scouts reserves that combination primarily for safeguarding material. Do not use a section colour in a way that implies a different section.
5. Do not invent, trace, distort or recolour a Scouts logo. Use only an approved, unmodified asset with documented permission. A text label is preferable when no approved asset is present.

## Shared implementation

- Generated session and activity pages use `assets/styles/scouts-pages.css`.
- Projected interactive decks use `assets/styles/scouts-presentation.css`.
- Answer sheets, team sheets and other print-first HTML use `assets/styles/scouts-printables.css`.
- All three inherit `assets/styles/scouts-core.css`. Extend these shared files when a reusable pattern is needed. Keep artifact-local CSS limited to content-specific layout that cannot be shared.
- All HTML outputs load `assets/scripts/theme.js`. Generated pages place a `data-theme-selector` host in the header; standalone artifacts may use the script's floating selector. The selector must offer clearly named Light and Dark choices, save an explicit choice locally, and use the operating-system preference when no choice has been saved.
- Use the semantic `--color-*` tokens from `scouts-core.css` for surfaces, text, outlines, states and controls. The visual direction is clean and Material-inspired: tonal surfaces, restrained elevation, rounded components and consistent spacing. It must not copy Google logos, product identity or protected branding.
- Both themes are required. Do not hard-code an artifact to a light or dark background, and do not introduce content colours that become unreadable in either theme.
- Do not add remote scripts, analytics, fonts, trackers or image requests. Pages and artifacts must remain usable when opened locally without an internet connection.

## Accessibility requirements

Treat WCAG 2.2 Level AA as the minimum target and apply these project rules:

1. Use valid `lang`, UTF-8 and responsive viewport metadata. Use semantic `header`, `nav`, `main`, `article`, `section` and `footer` landmarks where appropriate; provide a skip link on document pages.
2. Use one descriptive page title and a logical heading hierarchy. Link and button names must describe their destination or action without relying on adjacent text, position, an icon or an arrow.
3. Ensure all actions work with a keyboard and retain a strong visible focus indicator. Pointer targets must be at least 44 by 44 CSS pixels. Do not use hover-only content.
4. Meet at least 4.5:1 contrast for normal text and 3:1 for large text and meaningful interface graphics. Do not use colour as the only indication of an answer, status, warning or selection.
5. Supply useful `alt` text for informative images and empty `alt` text for decorative images. Caption or transcribe meaningful audio/video. Do not place essential instructions only inside an image.
6. Support 320 CSS pixel viewports and 200% zoom without losing content or actions. The page itself must not scroll horizontally. Place intrinsically wide tables in a labelled, keyboard-focusable scroll container.
7. Respect `prefers-reduced-motion` and forced-colour modes. Avoid flashing, parallax, autoplay and auto-advancing content.
8. Keep body copy at least 16px and frequently used labels at least 14px. Prefer relative units so browser text settings continue to work.
9. Theme selection must be keyboard accessible, expose its current state with `aria-pressed`, and update without reloading. The saved preference must not require cookies, accounts or network access.

## Presentation requirements

- Provide visible Previous, Reveal (when applicable) and Next controls; keyboard shortcuts are enhancements, never the only controls.
- Announce slide changes with an appropriate live region and keep the slide counter available to assistive technology.
- Do not auto-advance. Preserve the user's revealed-answer state deliberately and expose the correct answer in text, not only through a green background.
- Keep projected text large, concise and high contrast. Controls must remain reachable on a narrow phone and on a projected desktop view.
- Provide print styling that separates slides cleanly and removes interactive navigation.

## Printable and plan requirements

- Use a readable single-column layout with deliberate page margins and page-break behaviour. Avoid splitting one question, risk row or instruction step unnecessarily.
- Remove interactive controls from print, render links legibly and ensure tables remain readable in monochrome.
- A generated binary is disposable output. Update the Markdown or HTML source and regenerate rather than editing a PDF directly.

## Validation before finishing

1. Run `python -m unittest discover -s tests` and `python scripts/build_pages.py`.
2. Check for broken local links and missing shared styles.
3. Inspect at least a narrow mobile viewport and a desktop viewport. Exercise the complete presentation flow with a keyboard.
4. Switch every representative page type between Light and Dark, reload at least one page to confirm persistence, and check both themes for readable contrast and layout stability.
5. Check print preview for a plan and each changed printable or presentation type.
6. Review source and generated output for PII. Automated checks do not replace human privacy or accessibility review.
