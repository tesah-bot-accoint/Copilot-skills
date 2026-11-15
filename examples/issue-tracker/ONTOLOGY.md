# Ontology

A worked example for a project that tracks work in GitHub Issues. Copy it as a starting point, or run the `model-ontology` skill to build one from your own code.

## Object Types

### Issue
A unit of tracked work in GitHub Issues.
- Primary key: `number`
- Properties: `title` (string), `state` (open | closed), `updated_at` (date)
- Avoid: ticket, task, bug (when it means any Issue)

### Pull Request
A proposed change to the code, reviewed before merging.
- Primary key: `number`
- Properties: `title` (string), `state` (open | merged | closed), `draft` (boolean)
- Avoid: PR (fine in speech, but write Pull Request), merge request, patch

### Label
A tag that groups Issues and Pull Requests.
- Primary key: `name`
- Properties: `color` (hex), `description` (string)
- Avoid: tag, category

### Person
Someone with access to the repository.
- Primary key: `login`
- Properties: `role` (maintainer | contributor)
- Avoid: user (ambiguous with end users of the product), dev

## Link Types

| Link | From | To | Cardinality |
| --- | --- | --- | --- |
| tagged-with | Issue | Label | many-to-many |
| assigned-to | Issue | Person | many-to-many |
| fixed-by | Issue | Pull Request | one-to-many |
| authored-by | Pull Request | Person | many-to-one |

## Action Types

### Close Issue
- Acts on: Issue
- Parameters: `reason` (completed | not_planned), `comment` (string, optional)
- Submission criteria: the Issue's `state` is open
- Effects: sets `state` to closed with `reason`; posts `comment` if given
- Avoid: resolve, kill, archive

### Label Issue
- Acts on: Issue
- Parameters: `label` (an existing Label)
- Submission criteria: the Label exists and the Issue isn't already tagged-with it
- Effects: adds a tagged-with link from the Issue to the Label
- Avoid: tag, categorize

### Assign Issue
- Acts on: Issue
- Parameters: `assignee` (a Person)
- Submission criteria: the Issue's `state` is open
- Effects: adds an assigned-to link from the Issue to the Person
- Avoid: give, hand off

## Flagged ambiguities

- "stale" was used both for Issues with no update in 60 days and for Issues tagged-with Label `stale`. Resolved: "stale" means tagged-with Label `stale`. Age alone is written as "no update in N days".
- "close the PR" could mean merge or close without merging. Resolved: always ask; never treat it as merge.
