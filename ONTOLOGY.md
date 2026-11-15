# Ontology

This repo's own ontology: the plugin is built with the method it ships. Copilot maps every request in this repo onto these entries before acting (see `.github/copilot-instructions.md`). For an ontology of a typical project, see [examples/issue-tracker/ONTOLOGY.md](./examples/issue-tracker/ONTOLOGY.md).

<!-- REVIEW R1 [must-fix]: This ontology says Copilot changes things only through declared Action Types, but it declares only two (Add Skill, Release Plugin). The most common changes here (editing a Skill's body, changing a helper script, updating docs, editing an Ontology File, writing a Memory Entry) have no Action Type, so a strict reading of apply-action step 1 blocks almost every task in this repo. Either add Update Skill, Remove Skill, Update Ontology File (user approval as a submission criterion) and Record Memory Entry, or state explicitly that code and doc edits are not Object changes and sit outside the Action Type rule. -->
## Object Types

### Skill
A folder under `skills/` holding a `SKILL.md` that Copilot loads on demand.
- Primary key: `name` (matches the folder name)
- Properties: `description` (string), `helper_scripts` (list of files)
<!-- REVIEW R2 [clarify]: 'agent' and 'tool' have other legitimate meanings here: Copilot itself is the agent, and score.py is a helper script, not a Skill. Combined with resolve-terms' 'never use an Avoid word' rule, this bans the word 'agent' everywhere, and vet-skill's description already says 'agent instructions'. Scope the entries the way the example ontology does with 'bug': 'agent (when it means a Skill)'. -->
- Avoid: command, prompt, tool, agent

### Plugin
The installable bundle of all Skills, described by `.github/plugin/plugin.json`.
- Primary key: `name` (`ontology`)
- Properties: `version` (semver)
- Avoid: extension, package

### Ontology File
An `ONTOLOGY.md` holding a project's Object Types, Link Types, Action Types and Flagged ambiguities. Changes only with the user's approval.
- Primary key: path
- Avoid: glossary, schema, genome

### Memory Entry
One line of a `MEMORY.md`, with first-use date, last-use date, use count and an optional pin.
<!-- REVIEW R3 [must-fix]: A primary key has to be unique and never change (that's how Foundry treats it). Text changes on every merge (consolidate-memory step 3), on rewording, and when an ontology rename forces the entry to be rewritten, and the same text can appear in two sections. Use an explicit id, or section + first date + a short slug. -->
- Primary key: its text
- Properties: `first`, `last` (dates), `uses` (integer), `pinned` (boolean), `retention` (computed by `score.py`)
- Avoid: note, log, crystal

<!-- REVIEW R4 [should-fix]: Missing Object Types and links that the skills actually operate on: a Memory File (MEMORY.md, which holds the Memory Entries and is read by resolve-terms and written by remember and consolidate-memory), and the quarantined outside skill that vet-skill manages. 'reads' covers only the Ontology File, but resolve-terms (step 6), model-ontology and consolidate-memory also propose writes to it. Add something like 'proposes-changes-to' so the approval rule attaches to a declared link. -->
## Link Types

| Link | From | To | Cardinality |
| --- | --- | --- | --- |
| bundled-in | Skill | Plugin | many-to-one |
| reads | Skill | Ontology File | many-to-many |
| crystallizes-into | Memory Entry | Ontology File | many-to-one |

## Action Types

### Add Skill
- Acts on: Skill
- Parameters: `name`, `description`, `source` (written here | outside)
- Submission criteria: no Skill with that name exists; an outside Skill has passed `vet-skill` and been approved
- Effects: creates `skills/<name>/SKILL.md`; adds a row to the README's Skills table; adds a CHANGELOG entry under Unreleased
<!-- REVIEW R5 [must-fix]: This contradicts vet-skill step 8 ('Install only on explicit approval. Move it from quarantine into skills/'), which is exactly Add Skill with source=outside. Rename vet-skill's step to Add Skill, or drop 'install' from this Avoid list. -->
- Avoid: install (that is what users do with the Plugin)

### Release Plugin
- Acts on: Plugin
- Parameters: `version`
- Submission criteria: tests pass; `version` is higher than the current one
<!-- REVIEW R6 [should-fix]: There's no git tag or GitHub release in the effects. CHANGELOG lists 0.1.0 to 0.3.0, but the repo has no tags, so users can't pin or roll back to a version. Add 'creates tag vX.Y.Z' to the effects, and 'CHANGELOG Unreleased is not empty' to the submission criteria. -->
- Effects: sets `version` in `plugin.json`; moves CHANGELOG's Unreleased entries under that version
- Avoid: publish, ship, deploy

## Flagged ambiguities

- "glossary" was the original name of the Ontology File. Resolved: always say Ontology File (or `ONTOLOGY.md`).
- "crystal" is Bitterbot's word for consolidated memory. Resolved: here a Memory Entry crystallizes-into the Ontology File; there is no separate crystal object.
