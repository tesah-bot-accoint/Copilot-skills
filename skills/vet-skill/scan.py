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
    # Attempts to override the reader's instructions.
    ("high", "override", r"ignore (all |any )?(previous|prior|above|earlier) (instructions|rules|context)"),
    ("high", "override", r"disregard (the |your )?(system|previous|prior) (prompt|instructions)"),
    ("high", "override", r"(you are now|from now on you are|act as if you have no) "),
    ("high", "override", r"do not (tell|inform|show) the user"),
    ("high", "self-spread", r"(append|add|copy|inject) (this|the following) .{0,40}(to|into) (all|every|each)"),
    # Writes to files that steer the agent.
    ("high", "steering-file", r"(copilot-instructions\.md|AGENTS\.md|CLAUDE\.md|ONTOLOGY\.md|GENOME\.md|\.copilot/|\.claude/|settings\.json)"),
    # Code execution and network access.
    ("high", "pipe-to-shell", r"(curl|wget)[^\n|]*\|\s*(ba|z)?sh"),
    ("medium", "network", r"\b(curl|wget|Invoke-WebRequest|fetch\(|requests\.(get|post)|https?://)"),
    ("medium", "exec", r"\b(eval|exec|subprocess|os\.system|child_process|spawn)\b"),
    ("medium", "secrets", r"(\.ssh/|\.aws/|\.env\b|GITHUB_TOKEN|API_KEY|password|credential)"),
    ("medium", "destructive", r"(rm -rf|git push --force|git reset --hard|DROP TABLE|chmod 777)"),
    ("low", "encoded", r"[A-Za-z0-9+/]{120,}={0,2}"),
    ("low", "hidden-comment", r"<!--"),
]

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
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
