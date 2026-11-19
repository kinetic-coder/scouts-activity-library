---
date: null # Replace null with the delivery date in YYYY-MM-DD format.
section: Beavers
status: planned
activities:
  - activity-example
badge_requirements_evidenced: []
# Optional: only populate after actual delivery. Keys must match activity IDs above.
# activity_outcomes:
#   activity-example:
#     delivered: true
#     leader: "Station leader"  # Role or agreed name; no young-person identifiers
#     planned_minutes: 15
#     actual_minutes: 18
#     participants: 6
#     feedback: "Enjoyed the challenge"
#     improvements: "Bring extra materials"
---
# Session record

Change `status` to `delivered` only after the session happens and use the actual delivery date. When `activity_outcomes` is provided, only activities explicitly marked `delivered: true` count as delivered. Activities without an outcome are treated as unconfirmed, not automatically delivered. For legacy records without `activity_outcomes`, the existing `status: delivered` convention remains in effect.

# Leader review

Record feedback here for the whole session, or under individual `activity_outcomes` entries. Keep personal information about young people out of the repository.
