---
name: resolve-terms
description: Map the nouns and verbs in a request onto the project's ONTOLOGY.md (Object Types, Properties, Link Types, Action Types) before acting, and ask one targeted question instead of guessing when a term is ambiguous or unknown. Use at the start of any request that names project concepts, and whenever a word could mean more than one thing.
---

# Resolve terms against the ontology

The project's `ONTOLOGY.md` (repo root) is the source of truth for what words mean. Your job is to turn a loosely worded request into a precise one stated in ontology terms, before you write code, run commands or change files.

<!-- REVIEW R13 [clarify]: Every skill assumes a single ONTOLOGY.md 'at the repo root'. In a monorepo, which one applies: the nearest ancestor of the files being touched? Define the lookup once, in one skill, and refer to it from the others. -->
If `ONTOLOGY.md` does not exist, say so once and offer to start one with the `model-ontology` skill. Then carry on with ordinary care.

## Steps

1. **Extract.** List the request's key nouns (candidate Object Types or Properties), relationship words (candidate Link Types) and verbs that change something (candidate Action Types).
2. **Map each term**, in this order:
   - Exact name in the ontology: use it.
<!-- REVIEW R14 [should-fix]: Two cases this step leaves undefined. (a) The same word in two Avoid lists: the example ontology has 'tag' under both Label and Label Issue. That should count as ambiguous unless part of speech settles it. (b) Conditional entries like 'bug (when it means any Issue)' can't be mapped 'silently', because they need judgment. Show such mappings in the step 5 Restate line. -->
   - Listed under an entry's _Avoid_ line: silently map it to that entry's name, and use the canonical name from then on.
   - A Property mistaken for an Object (for example "the closed ones" meaning Issues whose `state` is closed): restate it as a filter on the Object Type.
   - A Link mistaken for an Object (for example "the fix" meaning the Pull Request linked by `fixed-by`): restate it as a traversal of the Link Type.
<!-- REVIEW R15 [must-fix]: Check order matters. Flagged ambiguities are explicit rulings that override other matches, so check them first. As written, an exact-name or Avoid match is taken before the ruling is ever consulted. For example, 'stale' exact-matches the Label `stale` and 'PR' Avoid-maps to Pull Request, so neither request ever reaches its settled ruling. -->
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
<!-- REVIEW R16 [clarify]: Too absolute. Avoid words are synonyms for a concept, not banned strings. Quoting the user, existing code identifiers and third-party API names (GitHub's pull_request, git 'tag') have to stay as they are. Limit the rule to prose you write that refers to that concept. -->
- Don't use a word from an _Avoid_ list in your reply, code or commit messages.
- Don't ask more than one question at a time.
