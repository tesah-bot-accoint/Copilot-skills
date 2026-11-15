#!/usr/bin/env python3
"""Score MEMORY.md entries on a forgetting curve and sort them into keep, forget and crystallize.

Retention follows an Ebbinghaus-style curve, R = exp(-t / S), where t is the
number of days since the entry was last used and S (stability) grows with
each use: S = BASE_DAYS * uses. Pinned entries never fade.

Usage: python3 score.py [path/to/MEMORY.md] [--today YYYY-MM-DD]
Prints one line per entry and exits 0. It never edits the file.
"""

import math
import re
import sys
from datetime import date

BASE_DAYS = 7  # stability gained per use, in days
FORGET_BELOW = 0.2  # retention under this is forgotten
CRYSTALLIZE_USES = 3  # uses needed to propose a permanent entry
CRYSTALLIZE_SPAN_DAYS = 2  # and they must span at least this many days

ENTRY = re.compile(
    r"^- \[first: (?P<first>\d{4}-\d{2}-\d{2}) \| last: (?P<last>\d{4}-\d{2}-\d{2})"
    r" \| uses: (?P<uses>\d+)(?P<pinned> \| pinned)?\] (?P<text>.+)$"
)


def score(first, last, uses, pinned, today):
    if pinned:
        return 1.0, "keep"
    stability = BASE_DAYS * max(uses, 1)
    retention = math.exp(-max((today - last).days, 0) / stability)
    if retention < FORGET_BELOW:
        return retention, "forget"
    if uses >= CRYSTALLIZE_USES and (last - first).days >= CRYSTALLIZE_SPAN_DAYS:
        return retention, "crystallize"
    return retention, "keep"


def main(argv):
    path, today = "MEMORY.md", date.today()
    args = iter(argv)
    for arg in args:
        if arg == "--today":
            today = date.fromisoformat(next(args))
        else:
            path = arg
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except FileNotFoundError:
        print(f"No memory file at {path}.")
        return 0
    section, unparsed = "", []
    for n, line in enumerate(lines, 1):
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if not line.startswith("- ["):
            continue
        m = ENTRY.match(line)
        if not m:
            unparsed.append(n)
            continue
        first, last = date.fromisoformat(m["first"]), date.fromisoformat(m["last"])
        retention, verdict = score(first, last, int(m["uses"]), bool(m["pinned"]), today)
        print(f"{verdict:<11} R={retention:.2f} line {n} [{section}] {m['text']}")
    for n in unparsed:
        print(f"malformed   line {n}: does not match the entry format")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
