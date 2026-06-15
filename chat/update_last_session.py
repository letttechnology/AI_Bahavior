#!/usr/bin/env python3
"""SessionEnd companion to export_claude_sessions.py.

Mechanically extracts the final user message and the final assistant message
from the most recently exported transcript and writes them to LAST_SESSION.md,
a small handoff the SessionStart hook loads at the start of the next session.

This is a SUPPLEMENT to the verbatim export (the canonical backup) -- never a
substitute for it. It runs AFTER export_claude_sessions.py so the newest .md is
the session that just ended. Pure text extraction: no model call, no cost.
"""
import os
import re
import glob
import sys

CHAT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(CHAT_DIR, "LAST_SESSION.md")
HEADER_RE = re.compile(r"^## \[(user|assistant)\]")


def newest_transcript():
    files = [
        f
        for f in glob.glob(os.path.join(CHAT_DIR, "*.md"))
        if os.path.basename(f) != "LAST_SESSION.md"
    ]
    return max(files, key=os.path.getmtime) if files else None


def split_sections(text):
    sections = []  # list of [role, [lines...]]
    cur = None
    for line in text.splitlines():
        m = HEADER_RE.match(line)
        if m:
            if cur:
                sections.append(cur)
            cur = [m.group(1), [line]]
        elif cur:
            cur[1].append(line)
    if cur:
        sections.append(cur)
    return sections


def last_of(sections, role):
    for r, lines in reversed(sections):
        if r == role:
            return "\n".join(lines).strip()
    return None


def main():
    src = newest_transcript()
    if not src:
        return 0
    with open(src, encoding="utf-8", errors="replace") as fh:
        sections = split_sections(fh.read())
    last_user = last_of(sections, "user")
    last_assistant = last_of(sections, "assistant")
    parts = [
        "# Last session handoff (auto-generated)",
        "",
        "> Supplement only -- the canonical backup is the full verbatim transcript",
        f"> in this directory. Source: `{os.path.basename(src)}`.",
        "",
        "## Final user message",
        "",
        last_user or "_(none found)_",
        "",
        "## Final assistant message",
        "",
        last_assistant or "_(none found)_",
        "",
    ]
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
