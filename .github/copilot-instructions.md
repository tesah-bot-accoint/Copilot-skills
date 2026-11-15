# Working in this repo

## Resolve terms before acting

`ONTOLOGY.md` is this repo's ontology in the Palantir style: Object Types and their Properties, Link Types between them, and Action Types, the only sanctioned ways to change things. Before acting on any request, map its key nouns and verbs onto it (the `resolve-terms` skill has the full procedure).

1. **Synonym in an _Avoid_ list:** silently map it to the canonical name and use that name in your reply and in any file you write.
2. **Term that maps to more than one entry:** stop and ask ONE question that names the candidates. Do not guess.
3. **Property or Link mistaken for an Object:** restate the request as a filter on Properties or a traversal of Link Types, then proceed.
4. **Term not in the ontology at all:** ask what it means. Once it is answered, propose an entry in the file's existing format.
5. **A request that changes something:** do it only through a declared Action Type (the `apply-action` skill). If none fits, propose one first.

If more than two terms are unclear, interview the user one question at a time before writing anything.

## Asking well

- Ask one question per turn, and give your recommended answer with it.
- Quote the ontology entry you are weighing against.
- Never ask about something the code or the ontology already answers. Look it up first.

## Recording what you learn

When an ambiguity gets resolved, add it under **Flagged ambiguities** in `ONTOLOGY.md` so it is never asked again.
