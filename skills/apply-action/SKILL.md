---
name: apply-action
description: Carry out a change to project data or state only through an Action Type declared in ONTOLOGY.md, checking its parameters and submission criteria first. Use whenever a request would create, update, delete, close, move or otherwise change an Object, including through scripts, migrations or API calls.
---

# Apply a change through an Action Type

In the ontology approach, Objects change only through declared Action Types. Each one names what it acts on, its parameters, its submission criteria (preconditions) and its effects. This keeps changes predictable and reviewable.

Run `resolve-terms` first if the request has not yet been restated in ontology terms.

## Steps

1. **Find the Action Type** in `ONTOLOGY.md` under **Action Types** that matches the requested change.
   - None matches: stop. Tell the user that no Action Type covers this change and propose one in the file's format (Acts on, Parameters, Submission criteria, Effects, Avoid). Continue only after the user approves it or explicitly says to do a one-off change.
   - More than one matches: ask one question naming the candidates.
2. **Bind parameters.** Fill every parameter from the request. Ask for any that are missing; don't pick defaults the Action Type doesn't state.
3. **Select the target Objects.** State exactly which Objects the action applies to and how they were selected (filter on Properties, traversal of Link Types). Give the count.
4. **Check submission criteria** against each target. List any Object that fails and leave it out.
5. **Preview** in one block: the Action Type, the bound parameters, the targets and the effects that will happen. For changes that are destructive, outward-facing or touch more than a handful of Objects, wait for the user to confirm.
6. **Apply** the effects, and only those. Something the Action Type doesn't list as an effect needs its own Action Type.
7. **Report** what changed, per Object, and any that were skipped and why.

## Don'ts

- Don't change Objects through side doors (direct edits, ad hoc scripts) when an Action Type exists for the change.
- Don't widen the effects beyond what the Action Type declares.
