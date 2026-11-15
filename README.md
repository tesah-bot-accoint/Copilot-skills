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
| [remember](./skills/remember/SKILL.md) | Records facts, preferences, corrections and working patterns in `MEMORY.md`, and refreshes entries each time they prove useful. |
| [consolidate-memory](./skills/consolidate-memory/SKILL.md) | Scores memory on a forgetting curve, drops what has faded, merges duplicates, and proposes long-lived entries as `ONTOLOGY.md` additions for you to approve. |
| [vet-skill](./skills/vet-skill/SKILL.md) | Quarantines and scans an outside skill for prompt injection and risky capabilities, and installs it only after you approve. |
| [tone-mode](./skills/tone-mode/SKILL.md) | Switches between focused, exploratory, careful and default modes that set how terse, curious and cautious Copilot is. |

## Fixed rules and fluid memory

Each project gets two files with different jobs, an idea adapted from the GENOME.md / MEMORY.md split in Bitterbot:

- `ONTOLOGY.md` is the fixed half: definitions and the allowed actions. Only you change it, or Copilot with your approval.
- `MEMORY.md` is the fluid half: what Copilot learned by working with you. Copilot writes it freely.

Memory fades unless it is used. Each entry's retention is `exp(-days since last use / (7 × uses))`. Entries below 0.2 are forgotten, pinned entries never are, and entries used 3 or more times over at least 2 days are proposed for the ontology. Run `consolidate-memory` now and then (for example weekly) to apply this. The rule lives in `skills/consolidate-memory/score.py`, so it gives the same answer every time.

## Files in this repo

- `.github/plugin/plugin.json`: the plugin manifest.
- `skills/`: the skills above. `skills/model-ontology/ONTOLOGY.template.md` and `skills/remember/MEMORY.template.md` are the blank starting files; `score.py` and `scan.py` are the helper scripts (Python 3, standard library only).
- `ONTOLOGY.md`: this repo's own ontology (empty sections for now).
- `.github/copilot-instructions.md`: the standing rule for Copilot when it works inside this repo.

## Try it

In a project, ask Copilot to "set up an ontology for this repo" (`model-ontology`). Then ask something vague, such as "close the stale tickets". It should map "tickets" to an Object Type or ask one question naming the candidates, then run the matching Action Type, showing a preview before it changes anything.
