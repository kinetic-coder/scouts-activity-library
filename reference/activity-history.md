# Activity and badge history: data contract

Use **stable identifiers** and explicit delivery records. Do not count a plan merely because it was committed. A planned activity becomes completed only when a leader marks it `delivered` with an actual date.

- `activities/<id>.md`: reusable activity; front matter `id`, `title`, `badge_requirements` (array of `badge_id` and `requirement_id`), `tags`.
- `sessions/YYYY-MM-DD-<section>-<slug>.md`: session record; front matter `date`, `section`, `status` (`planned` or `delivered`), `activities` (list of stable IDs), and `badge_requirements_evidenced` (list of requirement IDs, if verified).
- `reference/badges.md`: canonical badge IDs and links to current official criteria. One activity can support multiple badge requirements; **participation is not automatic badge completion**.

Dashboard definitions:
- Activity use count: number of distinct delivered session records containing that activity ID.
- Last used: latest actual date among delivered sessions.
- Badge coverage: count distinct delivered sessions evidencing at least one requirement for the badge; label this **badge-related sessions**, not badges awarded.
- Badge completions: only count explicitly confirmed completion records, if that capability is added later. Never infer an individual award from activity history.
- Group by section and calendar year; show last-used date and trend over time. Keep personally identifying young-person data out of the repo.

Suggested automated checks on pull requests and pushes to `master`: validate IDs, dates, status, duplicate session IDs, dangling references, and impossible dates; regenerate dashboard Markdown and optional SVG graphs from source records. Workflow must have least-privilege permissions and avoid committing generated files recursively.

An activity repeated at two meetings counts twice; editing the same meeting record does not increase its count. Multiple badges linked to one activity must not multiply activity use counts.
