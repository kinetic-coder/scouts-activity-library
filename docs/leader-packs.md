# Generating leader packs

**Source of truth:** Meeting plans reference reusable activity IDs, rather than copying their instructions. The generated leader pack contains the full meeting plan followed by each referenced activity's instructions.

## Create a pack locally

1. Create an activity at `activities/<id>.md` using `templates/activity.md`.
2. Create a meeting plan at `sessions/<Section>/YYYY-MM-DD-<section>-<slug>/YYYY-MM-DD-<section>-<slug>.md`.
3. In its YAML front matter add:

```yaml
activities:
  - astronaut-fitness-circuit
  - rocket-building
```

4. Run `python scripts/build_leader_pack.py sessions/<Section>/YYYY-MM-DD-<section>-<slug>/YYYY-MM-DD-<section>-<slug>.md`.
5. Read `build/<plan-stem>-leader-pack.md`. Print Markdown or convert it to PDF using your preferred tool.

## GitHub Actions

The **Build leader pack** workflow runs when session/activity files are pushed to `master`. It also supports manual runs via Actions > Build leader pack > Run workflow, where you provide a session plan path. Generated packs are downloadable workflow artifacts; no generated copies are committed.

## Important
- The script uses Python's standard library; no external dependencies.
- A missing activity reference fails the build instead of silently omitting instructions.
- An activity is included once, in the order of its IDs in front matter or links.
- The pack is generated, not the authoritative copy. Update the original activity document and rebuild.
- This first version produces **printable Markdown**, not a PDF. PDF export can be added later.
- Review safety and risk assessments before delivery. The generated pack is not an approval.
