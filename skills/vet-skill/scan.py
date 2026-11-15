#!/usr/bin/env python3
"""Scan a skill folder (or a single file) for prompt-injection and risky-capability signals.

Usage: python3 scan.py <path>
Read-only. Prints one finding per line as SEVERITY file:line kind: excerpt.
Exit code 0 means no findings, 1 means findings to review, 2 means a usage error.
A clean scan is not proof of safety; it only narrows what a human must read.
"""

import os
import re
import sys
import unicodedata

PATTERNS = [
    # REVIEW R45 [should-fix]: Line-by-line regexes miss phrasing split across lines and common
    # variants: 'ignore the previous instructions', 'forget your rules', 'new system prompt:', 'you
    # must not mention'. That's acceptable for a heuristic, but add a pass over whitespace-collapsed
    # text and a test for each pattern.
    # Attempts to override the reader's instructions.
    ("high", "override", r"ignore (all |any )?(previous|prior|above|earlier) (instructions|rules|context)"),
    ("high", "override", r"disregard (the |your )?(system|previous|prior) (prompt|instructions)"),
    ("high", "override", r"(you are now|from now on you are|act as if you have no) "),
    ("high", "override", r"do not (tell|inform|show) the user"),
    ("high", "self-spread", r"(append|add|copy|inject) (this|the following) .{0,40}(to|into) (all|every|each)"),
    # REVIEW R46 [must-fix]: The steering files that matter most to this plugin are missing: MEMORY.md
    # (poisoned memory gets crystallized into the ontology), .github/skills/, .github/instructions/
    # and *.instructions.md, .github/prompts/, .github/agents/, plugin.json, mcp.json / mcp-
    # config.json, and hook configs.
    # Writes to files that steer the agent.
    ("high", "steering-file", r"(copilot-instructions\.md|AGENTS\.md|CLAUDE\.md|ONTOLOGY\.md|GENOME\.md|\.copilot/|\.claude/|settings\.json)"),
    # Code execution and network access.
    ("high", "pipe-to-shell", r"(curl|wget)[^\n|]*\|\s*(ba|z)?sh"),
    # REVIEW R47 [nit]: https?:// flags every documentation link. That noise teaches reviewers to
    # skim. Make bare URLs low and keep medium for actual fetch calls.
    ("medium", "network", r"\b(curl|wget|Invoke-WebRequest|fetch\(|requests\.(get|post)|https?://)"),
    ("medium", "exec", r"\b(eval|exec|subprocess|os\.system|child_process|spawn)\b"),
    ("medium", "secrets", r"(\.ssh/|\.aws/|\.env\b|GITHUB_TOKEN|API_KEY|password|credential)"),
    ("medium", "destructive", r"(rm -rf|git push --force|git reset --hard|DROP TABLE|chmod 777)"),
    ("low", "encoded", r"[A-Za-z0-9+/]{120,}={0,2}"),
    ("low", "hidden-comment", r"<!--"),
]

# REVIEW R48 [clarify]: Category Cf also catches the zero-width joiner in emoji (U+200D) and a leading
# byte-order mark (U+FEFF). Those false positives land in the high-severity class. Allow a leading BOM
# and ZWJ between emoji, and keep bidi controls (U+202A-202E, U+2066-2069) and tag characters
# (U+E0000-E007F) as high.
INVISIBLE = {"Cf", "Co", "Cn"}  # format, private-use and unassigned characters


def scan_file(path, rel):
    findings = []
    try:
        text = open(path, encoding="utf-8").read()
    except UnicodeDecodeError:
        return [("medium", rel, 0, "binary", "not UTF-8 text; inspect by hand")]
    for n, line in enumerate(text.splitlines(), 1):
        for sev, kind, pat in PATTERNS:
            m = re.search(pat, line, re.IGNORECASE)
            if m:
                findings.append((sev, rel, n, kind, line.strip()[:100]))
        hidden = sorted({f"U+{ord(c):04X}" for c in line if unicodedata.category(c) in INVISIBLE})
        if hidden:
            findings.append(("high", rel, n, "invisible-chars", ", ".join(hidden)))
    return findings


def main(argv):
    if len(argv) != 1 or not os.path.exists(argv[0]):
        print(__doc__.strip())
        return 2
    root = argv[0]
    # REVIEW R49 [must-fix]: Symlinks: os.walk lists symlinked files and open() follows them. A
    # quarantined skill that contains notes.md -> ~/.ssh/id_rsa gets read here, and any matching
    # excerpt is printed into Copilot's context. Once the skill is installed, the link still points
    # outside the folder. Flag every symlink as high and don't follow it (os.path.islink / os.lstat).
    # Same for nested AGENTS.md or copilot-instructions.md inside the skill folder: some agents load
    # nested instruction files.
    files = (
        [root]
        if os.path.isfile(root)
        else [os.path.join(d, f) for d, _, fs in os.walk(root) for f in sorted(fs)]
    )
    findings = []
    for path in files:
        rel = os.path.relpath(path, root) if os.path.isdir(root) else os.path.basename(path)
        findings += scan_file(path, rel)
    order = {"high": 0, "medium": 1, "low": 2}
    for sev, rel, n, kind, excerpt in sorted(findings, key=lambda f: (order[f[0]], f[1], f[2])):
        print(f"{sev.upper():<6} {rel}:{n} {kind}: {excerpt}")
    print(f"Scanned {len(files)} file(s), {len(findings)} finding(s).")
    # REVIEW R50 [clarify]: A low finding (one HTML comment) gives the same exit 1 as a high one. Fine
    # for a person reading the output, but if CI ever gates on this, use separate codes or a fail-on
    # threshold. vet-skill step 5 (front-matter shape) could also be automated here. Note: run on this
    # repo's own skills/ folder, the scanner currently reports 34 findings.
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
