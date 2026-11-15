---
name: consolidate-memory
description: Consolidate the project's MEMORY.md, like sleep consolidation. Score every entry on a forgetting curve, drop the ones that have faded, merge duplicates, and propose entries that keep proving useful as permanent ONTOLOGY.md entries. Use when the user asks to consolidate, tidy or review memory, at the end of a long session, or when MEMORY.md has grown past about 100 entries.
---

# Consolidate memory

`MEMORY.md` collects what was learned while working; `ONTOLOGY.md` holds what is settled. Consolidation moves knowledge one way: noise fades out of memory, and patterns that keep proving useful are promoted ("crystallized") into the ontology, with the user's approval.

## Steps

1. **Score.** Run [score.py](./score.py) on the memory file:

   ```sh
   python3 <this skill's folder>/score.py MEMORY.md
   ```

   Each entry's retention is `R = exp(-days since last use / (7 × uses))`, so every use makes an entry fade more slowly. Pinned entries never fade. The script prints a verdict per entry and changes nothing. If Python isn't available, apply the same formula by hand.

2. **Forget.** Entries marked `forget` (R below 0.2) are removed. List them for the user first, grouped by section.
3. **Merge.** Among the remaining entries, combine ones that say the same thing. Keep the earliest `first`, the latest `last` and the sum of `uses`.
4. **Fix malformed lines** the script reports, so they can be scored next time.
5. **Crystallize.** For each `crystallize` entry (3 or more uses over at least 2 days), decide where it belongs in `ONTOLOGY.md`: a new _Avoid_ synonym, a Property, a Link Type, an Action Type or a Flagged ambiguity. Draft the exact lines in the ontology's format. If it doesn't fit any of those, leave it in memory.
6. **Preview** in one block: what will be forgotten, what merged, and the proposed ontology additions.
7. **Apply on approval.** Edit `MEMORY.md` for forgets and merges. Write each crystallized entry to `ONTOLOGY.md` only if the user approves it, then remove it from memory. Rejected proposals stay in memory, marked `| pinned` if the user wants to keep them anyway.

## Don'ts

- Don't write to `ONTOLOGY.md` without approval. It is the fixed half of the pair.
- Don't forget pinned entries, and don't pin anything the user didn't ask to keep.
- Don't change scores by hand to keep an entry you like. Ask the user to pin it instead.
