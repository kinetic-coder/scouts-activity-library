# Visual formatting and accessibility

The library uses one shared, offline-capable design system for generated Pages, presentations and printable HTML. Its clean, modern interface uses Material-inspired tonal surfaces, restrained elevation, rounded components and consistent spacing while following the current [official UK Scouts brand guidance](https://www.scouts.org.uk/volunteers/running-things-locally/local-media-and-member-communications/our-brand/): Scouts Purple is the core colour, Scouts Teal is the principal supporting colour, and Nunito Sans is preferred where it is installed.

This repository does not contain an approved Scouts logo, so the interface uses a text label rather than recreating one. Do not add, trace or alter a logo without an approved source and documented permission.

## Shared styles

- `assets/styles/scouts-core.css`: brand tokens, type scale, focus treatment and accessibility foundations.
- `assets/styles/scouts-pages.css`: generated session and activity pages.
- `assets/styles/scouts-presentation.css`: projected interactive decks.
- `assets/styles/scouts-printables.css`: answer sheets, team sheets and print-first resources.
- `assets/scripts/theme.js`: shared Light/Dark selector, system-theme fallback and local preference persistence.

Artifacts may keep small content-specific rules, but colour, typography, controls, focus and responsive structure belong in the shared styles. Use the semantic `--color-*` tokens rather than hard-coded light or dark values. Every HTML artifact loads the shared theme script and provides the named Light/Dark selector. The files deliberately make no remote font, script or analytics requests so they continue to work offline.

## Project accessibility baseline

Target WCAG 2.2 AA. Pages provide landmarks, skip navigation, visible keyboard focus, responsive type, 44px controls, keyboard-scrollable wide tables, reduced-motion handling, forced-colour support and purposeful print rules. Presentations must offer visible controls in addition to keyboard shortcuts and must not auto-advance.

Run these checks before review:

```shell
python -m unittest discover -s tests
python scripts/build_pages.py
```

Also inspect a plan, presentation and printable at narrow mobile and desktop widths; switch each between Light and Dark; confirm the saved preference survives navigation or reload; operate the whole presentation using a keyboard; and check print preview. Automated tests do not prove WCAG conformance; leader review and manual accessibility checking are still required.
