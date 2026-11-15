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

# REVIEW R39 [clarify]: These four constants are the whole memory policy. Document them in SKILL.md
# and allow overrides (flags, or a line in MEMORY.md). The docstring also says the script always exits
# 0, so consolidate-memory can't detect malformed lines from the exit code. Consider exit 1 when any
# line is malformed.
BASE_DAYS = 7  # stability gained per use, in days
FORGET_BELOW = 0.2  # retention under this is forgotten
CRYSTALLIZE_USES = 3  # uses needed to propose a permanent entry
CRYSTALLIZE_SPAN_DAYS = 2  # and they must span at least this many days

ENTRY = re.compile(
    r"^- \[first: (?P<first>\d{4}-\d{2}-\d{2}) \| last: (?P<last>\d{4}-\d{2}-\d{2})"
    r" \| uses: (?P<uses>\d+)(?P<pinned> \| pinned)?\] (?P<text>.+)$"
)


def score(first, last, uses, pinned, today):
    # REVIEW R40 [clarify]: Pinned entries return before the crystallize check, so they can never be
    # promoted (R32).
    if pinned:
        return 1.0, "keep"
    stability = BASE_DAYS * max(uses, 1)
    retention = math.exp(-max((today - last).days, 0) / stability)
    if retention < FORGET_BELOW:
        return retention, "forget"
    # REVIEW R41 [clarify]: A difference of 2 or more days means 3 distinct calendar days, but the
    # README says 'over at least 2 days' (R12). Also, this check runs after the forget check (R37).
    if uses >= CRYSTALLIZE_USES and (last - first).days >= CRYSTALLIZE_SPAN_DAYS:
        return retention, "crystallize"
    return retention, "keep"


def main(argv):
    path, today = "MEMORY.md", date.today()
    # REVIEW R42 [must-fix]: Verified: passing the today flag as the last argument crashes with an
    # uncaught StopIteration, and a bad date raises ValueError with a traceback. Use argparse
    # (standard library) and exit 2 on usage errors, which matches scan.py.
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
        # REVIEW R43 [should-fix]: Entries written as '* [first: ...' or '-  [first: ...' are skipped
        # silently instead of being reported as malformed. Report any list item under a section that
        # doesn't parse as an entry.
        if not line.startswith("- ["):
            continue
        m = ENTRY.match(line)
        if not m:
            unparsed.append(n)
            continue
        # REVIEW R44 [should-fix]: Nothing is validated here. Verified: 'first 2026-11-20 | last
        # 2026-11-01 | uses 0' is scored as an ordinary forget. Report first after last, last in the
        # future (currently clamped to 0 days without a warning), uses of 0, and impossible dates like
        # 2026-02-30 (currently an uncaught ValueError) as malformed.
        first, last = date.fromisoformat(m["first"]), date.fromisoformat(m["last"])
        retention, verdict = score(first, last, int(m["uses"]), bool(m["pinned"]), today)
        print(f"{verdict:<11} R={retention:.2f} line {n} [{section}] {m['text']}")
    for n in unparsed:
        print(f"malformed   line {n}: does not match the entry format")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
