#!/usr/bin/env python3
"""SessionStart hook: inject the last-session handoff (if present) as context.

Reads the small LAST_SESSION.md written by update_last_session.py at the
previous SessionEnd and emits it as additionalContext so a new session starts
knowing what was last in flight. Cheap: loads one small file, not the full
transcript. If the file is absent (first ever session), emits nothing.
"""
import os
import json

CHAT_DIR = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(CHAT_DIR, "LAST_SESSION.md")


def main():
    if not os.path.exists(PATH):
        return
    with open(PATH, encoding="utf-8", errors="replace") as fh:
        content = fh.read().strip()
    if not content:
        return
    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "## Last session handoff (auto-loaded)\n\n" + content,
        }
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
