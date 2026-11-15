# Memory

A worked example of `MEMORY.md` for the issue-tracker ontology next to it. Run `python3 skills/consolidate-memory/score.py examples/issue-tracker/MEMORY.md --today 2026-11-15` from the repo root to see how each entry scores.

## Facts

- [first: 2026-11-02 | last: 2026-11-14 | uses: 4] Issues tagged-with Label `needs-repro` are closed with reason not_planned after 30 days with no update. (source: maintainer, chat)
- [first: 2026-09-20 | last: 2026-09-21 | uses: 1] The Label `p0` was briefly used for outages. (source: issue #112)

## Preferences

<!-- REVIEW R32 [clarify]: This is a rule about when Close Issue may run, which makes it a submission criterion. It's pinned, and score.py returns 'keep' for pinned entries before it checks for crystallize, so it can never be proposed for the ontology, which is where it belongs. Decide whether pinned entries can crystallize. -->
- [first: 2026-10-05 | last: 2026-10-05 | uses: 1 | pinned] Never Close Issue on an Issue assigned-to a maintainer without asking first. (source: maintainer)
- [first: 2026-11-10 | last: 2026-11-13 | uses: 2] Comments on closed Issues are one sentence and link the Pull Request that fixed it. (source: chat)

## Patterns

- [first: 2026-11-15 | last: 2026-11-15 | uses: 1] To find Issues fixed-by a merged Pull Request, search for "Fixes #" in the Pull Request body. (source: worked on issue #140)
