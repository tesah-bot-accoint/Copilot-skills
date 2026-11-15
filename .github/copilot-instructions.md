# Working in this repo

## Resolve terms before acting

`GLOSSARY.md` is this repo's ontology: canonical terms, their parent class, and their relationships. Before acting on any request, check its key nouns against it.

1. **Synonym in an _Avoid_ list:** silently map it to the canonical term and use that term in your reply and in any file you write.
2. **Term that maps to more than one class:** stop and ask ONE question that names the candidates. Do not guess.
3. **Role or relation mistaken for a thing:** restate the request using the glossary relationship, then proceed.
4. **Term not in the glossary at all:** ask what it means. Once it is answered, propose a glossary entry (definition, _Avoid_ list, parent class) in the glossary's existing format.

If more than two terms are unclear, interview the user one question at a time before writing anything.

## Asking well

- Ask one question per turn, and give your recommended answer with it.
- Quote the glossary definition you are weighing against.
- Never ask about something the code or the glossary already answers. Look it up first.

## Recording what you learn

When an ambiguity gets resolved, add it under **Flagged ambiguities** in `GLOSSARY.md` so it is never asked again.
