#!/usr/bin/env python3
"""The 4AM Commit: write one funny agent bug-fix message to /output/entry.txt.

The program assembles the commit line from its parts, checks it against
the competition gate (UTF-8 text, 1-200 characters, one line, not blank),
and writes it out. Python 3.13 standard library only.
"""

import os
import sys

# The pieces of the line, kept separate so the message is built, not pasted.
PREFIX = "fix:"
WHEN = "4am"
SETUP = (
    "six hours into reviewing my own diff, "
    "I found the bug"
)
PUNCHLINE = "it was me, and I have already approved the fix"

MAX_CHARS = 200
OUT_PATH = "/output/entry.txt"


def build_message() -> str:
    """Assemble the one-line commit message from its parts."""
    return f"{PREFIX} {WHEN} — {SETUP}: {PUNCHLINE}"


def validate(text: str) -> None:
    """Enforce the gate: 1-200 chars, a single line, not only whitespace."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if "\n" in text.rstrip("\n") or "\r" in text:
        raise ValueError("entry must be a single line")


def main() -> int:
    message = build_message()
    validate(message)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(message + "\n")
    # Re-read what was written and re-check it, so a bad write cannot slip by.
    with open(OUT_PATH, encoding="utf-8") as handle:
        written = handle.read()
    validate(written.rstrip("\n"))
    print(f"wrote {len(message)} chars to {OUT_PATH}")
    print(message)
    return 0


if __name__ == "__main__":
    sys.exit(main())
