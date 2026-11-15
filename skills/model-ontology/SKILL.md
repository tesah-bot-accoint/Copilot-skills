---
name: model-ontology
description: Create or extend the project's ONTOLOGY.md in the Palantir Ontology style (Object Types, Properties, Link Types, Action Types) by interviewing the user and reading the code. Use when a project has no ontology yet, when the user wants to add or rename a concept, or when resolve-terms or apply-action found a term or change the ontology doesn't cover.
---

# Model the ontology

Build `ONTOLOGY.md` at the repo root so other skills can resolve terms and apply changes against it. If the file is missing, start from [ONTOLOGY.template.md](./ONTOLOGY.template.md).

## Steps

1. **Read before asking.** Look at the code, schemas, API types, issue labels and docs for the concepts that already exist. Draft candidate entries from them. Don't ask the user about anything you can read.
<!-- REVIEW R21 [should-fix]: Add the fields the other skills need. (1) A title property, which is what apply-action shows when it lists targets. (2) A fixed set of base types: string, integer, boolean, date, timestamp, enum (a | b), list of <base type>. References to other Objects go only through Links. (3) An optional 'Status: active | experimental | deprecated', so a renamed concept can be retired instead of deleted. Also require primary keys to be unique and never change (see R3). -->
2. **Object Types first.** For each candidate, settle the name (a singular noun), a one-sentence definition, its primary key and its Properties with types. Collect synonyms people use into _Avoid_.
<!-- REVIEW R22 [should-fix]: Links get a name only from the From side, but resolve-terms has to traverse them both ways ('the Issues this Pull Request fixes'). Foundry names each side separately: add an inverse-name column (fixed-by / fixes). Also record where each link is stored (the label list, 'Fixes #' in a Pull Request body) so traversal is mechanical, not guessed. The example MEMORY.md has a Patterns entry only because this is missing. -->
3. **Then Link Types.** For each pair of Object Types that relate, name the link as a verb read from the From side, and give its cardinality.
4. **Then Action Types.** For each way the project changes Objects, record Acts on, Parameters, Submission criteria and Effects. Name actions as verb plus Object Type (for example "Close Issue").
5. **Interview one question at a time.** When a definition or boundary is unclear, ask one question, name the options and give your recommendation. Watch for one word covering two concepts: split it into two entries and add a line under **Flagged ambiguities**.
<!-- REVIEW R23 [should-fix]: Renames: when a concept is renamed, add the old name to Avoid and propose updating the MEMORY.md entries that use it. Those entries are written 'in ontology terms', so after a rename they contradict the ontology and trigger remember's conflict rule. -->
6. **Show the diff** of `ONTOLOGY.md` before writing it, and write only after the user agrees.

## Rules for entries

- One canonical name per concept. Every other name goes under _Avoid_.
<!-- REVIEW R24 [clarify]: The template's own example contradicts this rule (`labels (list of Label)` on Issue, next to a tagged-with link). And 'exactly one' rules out shared properties: Issue and Pull Request both have `title` and `state`. Foundry handles that with shared properties and interfaces. Is the rule that each Property definition belongs to one Object Type? -->
- Properties belong to exactly one Object Type. A Property that points at another Object is a Link Type instead.
- An Action's Effects list every change it makes. Nothing else changes.
- Keep definitions to one sentence. Put examples in Flagged ambiguities, not in the definition.
