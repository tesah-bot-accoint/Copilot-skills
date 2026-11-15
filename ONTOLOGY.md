# Ontology

This repo's own ontology: the plugin is built with the method it ships. Copilot maps every request in this repo onto these entries before acting (see `.github/copilot-instructions.md`). For an ontology of a typical project, see [examples/issue-tracker/ONTOLOGY.md](./examples/issue-tracker/ONTOLOGY.md).

## Object Types

### Skill
A folder under `skills/` holding a `SKILL.md` that Copilot loads on demand.
- Primary key: `name` (matches the folder name)
- Properties: `description` (string), `helper_scripts` (list of files)
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
- Primary key: its text
- Properties: `first`, `last` (dates), `uses` (integer), `pinned` (boolean), `retention` (computed by `score.py`)
- Avoid: note, log, crystal

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
- Avoid: install (that is what users do with the Plugin)

### Release Plugin
- Acts on: Plugin
- Parameters: `version`
- Submission criteria: tests pass; `version` is higher than the current one
- Effects: sets `version` in `plugin.json`; moves CHANGELOG's Unreleased entries under that version
- Avoid: publish, ship, deploy

## Flagged ambiguities

- "glossary" was the original name of the Ontology File. Resolved: always say Ontology File (or `ONTOLOGY.md`).
- "crystal" is Bitterbot's word for consolidated memory. Resolved: here a Memory Entry crystallizes-into the Ontology File; there is no separate crystal object.
