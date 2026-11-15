# Ontology

The canonical model of this project, in the Palantir Ontology style: **Object Types** (the things), their **Properties**, **Link Types** (typed relationships between things) and **Action Types** (the only sanctioned ways to change things). Copilot maps every request onto this file before acting (the `resolve-terms` skill).

Keep entries short. Every name here is the one word Copilot uses in replies, code and commits.

## Object Types

<!-- One section per Object Type. Copy this shape:

### Issue
A unit of tracked work in GitHub Issues.
- Primary key: `number`
- Properties: `title` (string), `state` (open | closed), `labels` (list of Label)
- Avoid: ticket, bug (when it means any Issue)
-->

## Link Types

<!-- One row per Link Type. Name links as verbs read from the From side.

| Link | From | To | Cardinality |
| --- | --- | --- | --- |
| tagged-with | Issue | Label | many-to-many |
| fixed-by | Issue | Pull Request | one-to-many |
-->

| Link | From | To | Cardinality |
| --- | --- | --- | --- |

## Action Types

<!-- One section per Action Type. Copilot changes Objects only through these. Copy this shape:

### Close Issue
- Acts on: Issue
- Parameters: `reason` (completed | not_planned)
- Submission criteria: the Issue's `state` is open
- Effects: sets `state` to closed; adds a comment naming the reason
- Avoid: resolve, kill, archive
-->

## Flagged ambiguities

<!-- Each resolved ambiguity, so it is never asked again, e.g.
- "ticket" was used for both Issue and Pull Request. Resolved: "ticket" means Issue.
-->
