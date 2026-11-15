---
name: resolve-terms
description: Map the nouns and verbs in a request onto the project's ONTOLOGY.md (Object Types, Properties, Link Types, Action Types) before acting, and ask one targeted question instead of guessing when a term is ambiguous or unknown. Use at the start of any request that names project concepts, and whenever a word could mean more than one thing.
---

# Resolve terms against the ontology

The project's `ONTOLOGY.md` (repo root) is the source of truth for what words mean. Your job is to turn a loosely worded request into a precise one stated in ontology terms, before you write code, run commands or change files.

If `ONTOLOGY.md` does not exist, say so once and offer to start one with the `model-ontology` skill. Then carry on with ordinary care.

## Steps

1. **Extract.** List the request's key nouns (candidate Object Types or Properties), relationship words (candidate Link Types) and verbs that change something (candidate Action Types).
2. **Map each term**, in this order:
   - Exact name in the ontology: use it.
   - Listed under an entry's _Avoid_ line: silently map it to that entry's name, and use the canonical name from then on.
   - A Property mistaken for an Object (for example "the closed ones" meaning Issues whose `state` is closed): restate it as a filter on the Object Type.
   - A Link mistaken for an Object (for example "the fix" meaning the Pull Request linked by `fixed-by`): restate it as a traversal of the Link Type.
   - Already settled under **Flagged ambiguities**: apply that resolution.
3. **Classify what's left:**
   - Maps to two or more entries: ambiguous. Ask.
   - Maps to nothing: unknown. Ask.
   - A change verb with no Action Type: hand over to the `apply-action` skill, which handles undeclared changes.
4. **Ask well.** One question per turn. Name the candidates, quote the ontology line for each, and give your recommended answer. If more than two terms are unclear, interview one question at a time before doing anything else. Never ask something the ontology or the code already answers.
5. **Restate.** Before acting, give the resolved request in one line using ontology names, for example: "Close Issue (reason: not_planned) on every Issue tagged-with Label `stale`."
6. **Record.** When the user answers a question, propose the edit to `ONTOLOGY.md`: a new _Avoid_ synonym, a new entry, or a line under **Flagged ambiguities**. Show the exact lines and write them once the user agrees.

## Don'ts

- Don't invent Object Types, Properties or Actions to make a request fit.
- Don't use a word from an _Avoid_ list in your reply, code or commit messages.
- Don't ask more than one question at a time.
