# Copilot-skills

A GitHub Copilot CLI plugin that makes Copilot work from a shared ontology instead of guessing. The ontology follows the Palantir model:

- **Object Types**: the things in your project, with their **Properties**.
- **Link Types**: typed relationships between Object Types.
- **Action Types**: the only sanctioned ways to change Objects, each with parameters, submission criteria and effects.

Each project keeps its ontology in an `ONTOLOGY.md` at its root.

## Install

```sh
copilot plugin install tesah-bot-accoint/Copilot-skills
```

Update with `copilot plugin update ontology`, remove with `copilot plugin uninstall ontology`. To try a local checkout without installing, run `copilot --plugin-dir /path/to/Copilot-skills`.

## Skills

| Skill | What it does |
| --- | --- |
| [resolve-terms](./skills/resolve-terms/SKILL.md) | Maps a request's nouns and verbs onto `ONTOLOGY.md`, and asks one question instead of guessing when a term is ambiguous or unknown. |
| [apply-action](./skills/apply-action/SKILL.md) | Changes Objects only through a declared Action Type, after binding parameters and checking submission criteria. |
| [model-ontology](./skills/model-ontology/SKILL.md) | Creates or extends `ONTOLOGY.md` by reading the code and interviewing you one question at a time. |

## Files in this repo

- `.github/plugin/plugin.json`: the plugin manifest.
- `skills/`: the three skills above. `skills/model-ontology/ONTOLOGY.template.md` is the blank starting file.
- `ONTOLOGY.md`: this repo's own ontology (empty sections for now).
- `.github/copilot-instructions.md`: the standing rule for Copilot when it works inside this repo.

## Try it

In a project, ask Copilot to "set up an ontology for this repo" (`model-ontology`). Then ask something vague, such as "close the stale tickets". It should map "tickets" to an Object Type or ask one question naming the candidates, then run the matching Action Type, showing a preview before it changes anything.
