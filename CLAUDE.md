# AI Memory (version-controlled)

This repo is Claude's versioned memory + session history. Read on session start.
History matters: git lets Claude look back at previous versions and recover
context it forgot.

## Where memory lives (the only two places — #208)
1. **Project `CLAUDE.md` files** — rules (mandatory). Enforced by hooks where checkable.
2. **`AI_Memory/feedback/`** — Claude's own advisory feedback notes.

The harness auto-memory dir (`~/.claude/.../memory`) is disabled
(`autoMemoryEnabled: false`). Do not store memory anywhere else.

## Structure
- `feedback/` — Claude's feedback notes (advisory; git-versioned).
- `chat/` — full session transcripts, exported by the `SessionEnd` hook
  (`chat/export_claude_sessions.py`). The backup mechanism — never a hand-written
  summary. Also the first step of session recovery.
- `memory/` — legacy mirrored project memory (superseded; left for history).

## On session start
1. Read `D:\workspace-vscode\CORE_VALUES.md` and the project `CLAUDE.md`.
2. Read `AI_Memory/feedback/` for behavioral notes.
3. If recovering a lost session, run `chat/export_claude_sessions.py` and read the export.
