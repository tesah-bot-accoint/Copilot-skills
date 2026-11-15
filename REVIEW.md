# Review

An ontology-design and engineering review of the plugin at 0.3.0. Each finding is also an inline comment marked `REVIEW Rn` in the file it concerns (an HTML comment in Markdown, `#` in Python and YAML). Search for `REVIEW R` to jump between them. Delete the inline comments as each one is resolved.

Severity: **must-fix** = wrong, contradictory or unsafe; **should-fix** = a real gap; **clarify** = an open design question for the author; **nit** = polish.

## Top priorities

1. **The rules contradict each other about when confirmation is needed and who may write `ONTOLOGY.md`** (R9, R18, R53, R56). tone-mode plus apply-action means every change asks for confirmation, and copilot-instructions.md lets Copilot add to the ontology without approval.
2. **This repo's own ontology can't authorise the work done in it** (R1, R5). It has only two Action Types, and its Avoid list conflicts with vet-skill.
3. **Users don't get the always-on behaviour the README describes** (R7). Their projects have no copilot-instructions.md.
4. **Memory can lose its best entries and can be poisoned** (R36, R37, R46). The forget/merge/crystallize order is wrong, there's no provenance gate, and the scanner doesn't watch MEMORY.md.
5. **Robustness of the helper scripts** (R42, R44, R49). score.py crashes on bad arguments or dates, and scan.py follows symlinks.
6. **Foundry fidelity** (R17, R21, R22, R26, R28). Missing: who may run an action, title properties, inverse link names, a split between effects and side effects, and correct cardinalities.

## `.github/plugin/plugin.json` (JSON allows no comments, so these notes live here)

- **should-fix**: the keyword `glossary` is an Avoid word for Ontology File in this repo's own `ONTOLOGY.md`. Use `ontology` alone, or `knowledge-model`.
- **clarify**: the `palantir` keyword can read as an affiliation. The README disclaims one; the manifest, which is what marketplace listings show, doesn't. Consider dropping the keyword.
- **clarify**: check that `"skills": "skills/"` (a string, not an array) and the other fields match the current Copilot CLI plugin manifest schema.

## All findings

| ID | Severity | File | Summary |
| --- | --- | --- | --- |
| R1 | must-fix | `ONTOLOGY.md` | This ontology says Copilot changes things only through declared Action Types, but it declares only two (Add Skill, Release Plugin) |
| R3 | must-fix | `ONTOLOGY.md` | A primary key has to be unique and never change (that's how Foundry treats it) |
| R5 | must-fix | `ONTOLOGY.md` | This contradicts vet-skill step 8 ('Install only on explicit approval. Move it from quarantine into skills/'), which is exactly Add Skill with source=outside.... |
| R7 | must-fix | `.github/copilot-instructions.md` | This file only steers Copilot inside this repo |
| R9 | must-fix | `.github/copilot-instructions.md` | This says 'add it' to ONTOLOGY.md with no approval step, and two lines later says ONTOLOGY.md changes only with approval |
| R15 | must-fix | `skills/resolve-terms/SKILL.md` | Check order matters |
| R25 | must-fix | `skills/model-ontology/ONTOLOGY.template.md` | The example Issue below has `labels (list of Label)` as a Property |
| R36 | must-fix | `skills/remember/SKILL.md` | Memory poisoning path: text from an Issue body or a web page becomes 'a fact about the codebase', goes into MEMORY.md, gets crystallized, and ends up in... |
| R37 | must-fix | `skills/consolidate-memory/SKILL.md` | Two ordering bugs |
| R42 | must-fix | `skills/consolidate-memory/score.py` | Verified: passing the today flag as the last argument crashes with an uncaught StopIteration, and a bad date raises ValueError with a traceback |
| R46 | must-fix | `skills/vet-skill/scan.py` | The steering files that matter most to this plugin are missing: MEMORY.md (poisoned memory gets crystallized into the ontology), .github/skills/,... |
| R49 | must-fix | `skills/vet-skill/scan.py` | Symlinks: os.walk lists symlinked files and open() follows them |
| R56 | must-fix | `skills/tone-mode/SKILL.md` | apply-action previews every change, so 'anything apply-action previews' means every change triggers careful mode, and then every change waits for confirmation (R18) |
| R4 | should-fix | `ONTOLOGY.md` | Missing Object Types and links that the skills actually operate on: a Memory File (MEMORY.md, which holds the Memory Entries and is read by resolve-terms and... |
| R6 | should-fix | `ONTOLOGY.md` | There's no git tag or GitHub release in the effects |
| R12 | should-fix | `README.md` | Spell out what this means in practice: an entry used once is forgotten about 11 days after its last use (7 x ln 5), after 2 uses about 23 days, after 3 uses about 34 days |
| R14 | should-fix | `skills/resolve-terms/SKILL.md` | Two cases this step leaves undefined |
| R17 | should-fix | `skills/apply-action/SKILL.md` | Action Types have no notion of who may run them |
| R18 | should-fix | `skills/apply-action/SKILL.md` | 'More than a handful' can't be checked |
| R19 | should-fix | `skills/apply-action/SKILL.md` | (a) Re-check the submission criteria at apply time: state can change between the preview and the user's confirmation (someone else closes the Issue in the meantime) |
| R21 | should-fix | `skills/model-ontology/SKILL.md` | Add the fields the other skills need |
| R22 | should-fix | `skills/model-ontology/SKILL.md` | Links get a name only from the From side, but resolve-terms has to traverse them both ways ('the Issues this Pull Request fixes') |
| R23 | should-fix | `skills/model-ontology/SKILL.md` | Renames: when a concept is renamed, add the old name to Avoid and propose updating the MEMORY.md entries that use it |
| R26 | should-fix | `skills/model-ontology/ONTOLOGY.template.md` | The Action format is missing: (a) whether each parameter is required, and its default |
| R28 | should-fix | `examples/issue-tracker/ONTOLOGY.md` | Issues with the links below |
| R29 | should-fix | `examples/issue-tracker/ONTOLOGY.md` | This writes a reason that isn't a declared Property of Issue |
| R31 | should-fix | `examples/issue-tracker/ONTOLOGY.md` | There are no Pull Request Action Types, so every answer to this question ends at 'no Action Type covers this' |
| R34 | should-fix | `skills/remember/SKILL.md` | Refreshing is the only thing that keeps an entry alive, and it depends on the model noticing that an entry 'actually informed' what it did, which can't be... |
| R38 | should-fix | `skills/consolidate-memory/SKILL.md` | The list of targets is missing 'a submission criterion on an existing Action Type' and 'a new enum value on a Property', which are the most common shapes for... |
| R43 | should-fix | `skills/consolidate-memory/score.py` | Entries written as '* [first: ...' or '-  [first: ...' are skipped silently instead of being reported as malformed |
| R44 | should-fix | `skills/consolidate-memory/score.py` | Nothing is validated here |
| R45 | should-fix | `skills/vet-skill/scan.py` | Line-by-line regexes miss phrasing split across lines and common variants: 'ignore the previous instructions', 'forget your rules', 'new system prompt:', 'you... |
| R52 | should-fix | `skills/vet-skill/SKILL.md` | (a) In this repo, moving a skill into skills/ is the Add Skill Action Type, whose effects also include a CHANGELOG entry |
| R58 | should-fix | `.github/workflows/test.yml` | Pin actions to full commit SHAs |
| R59 | should-fix | `.github/workflows/test.yml` | The README promises 'Python 3' |
| R60 | should-fix | `.github/workflows/test.yml` | This grep matches name: anywhere in the file, not just the front matter |
| R61 | should-fix | `tests/test_scripts.py` | Missing cases: the forget and crystallize boundaries (R exactly 0.2, span exactly 2 days); the today flag with no value (crashes today, R42); first after last;... |
| R2 | clarify | `ONTOLOGY.md` | 'agent' and 'tool' have other legitimate meanings here: Copilot itself is the agent, and score.py is a helper script, not a Skill |
| R8 | clarify | `.github/copilot-instructions.md` | Every turn asks only one question anyway, so what does the 'more than two' threshold change? If it means 'write nothing until every term is resolved', say that |
| R11 | clarify | `README.md` | Check the install form (plugin install owner/repo), the update and uninstall commands, and the plugin-dir flag against the current Copilot CLI plugin docs... |
| R13 | clarify | `skills/resolve-terms/SKILL.md` | Every skill assumes a single ONTOLOGY.md 'at the repo root' |
| R16 | clarify | `skills/resolve-terms/SKILL.md` | Too absolute |
| R20 | clarify | `skills/apply-action/SKILL.md` | Should a one-off change the user approved in step 1 be recorded (as a Memory Entry, or as a proposed Action Type) so the next identical request doesn't ask again? |
| R24 | clarify | `skills/model-ontology/SKILL.md` | The template's own example contradicts this rule (`labels (list of Label)` on Issue, next to a tagged-with link) |
| R30 | clarify | `examples/issue-tracker/ONTOLOGY.md` | 'tag' is also in Label's Avoid list (noun here, verb there) |
| R32 | clarify | `examples/issue-tracker/MEMORY.md` | This is a rule about when Close Issue may run, which makes it a submission criterion |
| R33 | clarify | `skills/remember/SKILL.md` | Should MEMORY.md be committed? If yes: one developer's Preferences become team facts, and every refresh rewrites a line, so use counts cause merge conflicts... |
| R35 | clarify | `skills/remember/SKILL.md` | Newer by `first` or by `last`? And removing the older entry throws away its use count |
| R39 | clarify | `skills/consolidate-memory/score.py` | These four constants are the whole memory policy |
| R40 | clarify | `skills/consolidate-memory/score.py` | Pinned entries return before the crystallize check, so they can never be promoted (R32). |
| R41 | clarify | `skills/consolidate-memory/score.py` | A difference of 2 or more days means 3 distinct calendar days, but the README says 'over at least 2 days' (R12) |
| R48 | clarify | `skills/vet-skill/scan.py` | Category Cf also catches the zero-width joiner in emoji (U+200D) and a leading byte-order mark (U+FEFF) |
| R50 | clarify | `skills/vet-skill/scan.py` | A low finding (one HTML comment) gives the same exit 1 as a high one |
| R51 | clarify | `skills/vet-skill/SKILL.md` | Quarantine keeps the skill out of Copilot's skill loader, but steps 3 and 4 still put its text into the model's context, and the 'text is data' line is the... |
| R54 | clarify | `skills/tone-mode/SKILL.md` | Scope: tone-mode has nothing to do with the ontology, and it dilutes the plugin's name and pitch |
| R55 | clarify | `skills/tone-mode/SKILL.md` | 'Caution: low' for exploratory reads as permission to skip checks, which the Don'ts forbid |
| R10 | nit | `README.md` | The diagram labels ONTOLOGY.md 'fixed: changes only with your approval', but the consolidate-memory arrow into it has no approval step, and the resolve-terms... |
| R27 | nit | `skills/model-ontology/ONTOLOGY.template.md` | Only the Link Types section has a live, header-only table |
| R47 | nit | `skills/vet-skill/scan.py` | https?:// flags every documentation link |
| R53 | nit | `skills/vet-skill/SKILL.md` | This list of approved ontology writers leaves out resolve-terms (step 6) |
| R57 | nit | `.github/workflows/test.yml` | push plus pull_request runs every PR branch twice |
| R62 | nit | `tests/test_scripts.py` | delete=False leaks temp files on every run |
| R63 | nit | `CHANGELOG.md` | Three releases dated the same day with no git tags (R6) |
