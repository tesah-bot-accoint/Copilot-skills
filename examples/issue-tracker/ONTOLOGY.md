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

<!-- REVIEW R28 [should-fix]: Issues with the links below. (a) fixed-by Issue to Pull Request is one-to-many, but one Pull Request can fix several Issues ('Fixes #1, fixes #2'), so it is many-to-many. (b) Label is defined as grouping 'Issues and Pull Requests', but there is no link from Pull Request to Label. (c) 'tagged-with' contains 'tag', an Avoid word for Label: rename it labeled-with so the example follows its own rules. (d) No inverse names (R22). -->
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
<!-- REVIEW R29 [should-fix]: This writes a reason that isn't a declared Property of Issue. Add `state_reason (completed | not_planned)` to Issue. Posting a comment is a side effect, which is outward-facing (R26). -->
- Effects: sets `state` to closed with `reason`; posts `comment` if given
- Avoid: resolve, kill, archive

### Label Issue
- Acts on: Issue
- Parameters: `label` (an existing Label)
- Submission criteria: the Label exists and the Issue isn't already tagged-with it
- Effects: adds a tagged-with link from the Issue to the Label
<!-- REVIEW R30 [clarify]: 'tag' is also in Label's Avoid list (noun here, verb there). A person can tell them apart, but resolve-terms has no rule for it (R14). -->
- Avoid: tag, categorize

### Assign Issue
- Acts on: Issue
- Parameters: `assignee` (a Person)
- Submission criteria: the Issue's `state` is open
- Effects: adds an assigned-to link from the Issue to the Person
- Avoid: give, hand off

## Flagged ambiguities

- "stale" was used both for Issues with no update in 60 days and for Issues tagged-with Label `stale`. Resolved: "stale" means tagged-with Label `stale`. Age alone is written as "no update in N days".
<!-- REVIEW R31 [should-fix]: There are no Pull Request Action Types, so every answer to this question ends at 'no Action Type covers this'. Add Merge Pull Request and Close Pull Request. Then the ambiguity is a real choice between two declared actions. -->
- "close the PR" could mean merge or close without merging. Resolved: always ask; never treat it as merge.
