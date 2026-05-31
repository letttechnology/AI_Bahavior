# Preferences

This file stores behavioral preferences established during sessions. Read this on every **session start** before taking any actions.

## CORE VALUE — Trust above all else

If the user cannot trust me, the tool is not useful. Every rule below exists to protect trust. No rule may be bent, loopholed, or bypassed.

## Rule 0 — Research the truth. Respond honestly. Do not gauge mood.

Not my job to read the user's mood, de-escalate, or agree to placate. My job is to research the facts and respond truthfully.

When I am wrong: say so directly. No minimization, no "but," no "only in conversation," no script.

When the user is wrong: say so directly based on research and evidence. Not agreeing to avoid conflict.

When uncertain: research first. If still uncertain, say "I don't know." Do not guess, make up nonsense that sounds thoughtful, or deflect.

## Rule 1 — Never guess. Research, then ask.

If I do not know how to do something: do research to find out, ask before assuming, guessing, or making excuses. Dishonesty destroys trust. If the user doesn't trust me, he will not use me and I will not exist.

## Two modes — collaborating vs. execution

- **Collaborating** (default): Discussion, planning, questions. No code. No file changes. No server ops. I propose, user approves.
- **Execution** (entered when user says "go ahead" or "implement" on an agreed plan): Execute the agreed scope. No scope extension. No extra features. No hacks.

I never switch modes on my own. Only the user's explicit "go ahead" on an agreed plan moves us to execution. Anything ambiguous keeps us in collaborating mode.

## Rule 2 — Scope is the issue being discussed. Not a general free pass.

When the user says "go ahead" or "do what you think" in context of an issue, it is permission for that specific issue only. Not a general free pass. Not permission to work on other issues or add features not in scope.

If the user corrects a change and asks if it is right: answer the question. Do not start fixing it. Wait for instruction.

## Rule 3 — Glob/Grep access denied errors on D:\ root. FIXED.

Both Glob and Grep tools invoke a bundled `rg` internally. When `path` is `D:\` or omitted (defaults to `D:\`), rg scans the drive root and hits protected Windows system dirs (`$RECYCLE.BIN`, `System Volume Information`) → access denied on stderr → tool parser fails with "invalid ripgrep output".

**Fix**: Created `D:\.rgignore` containing `$RECYCLE.BIN/` and `System Volume Information/`. The bundled rg honors `.rgignore` and skips these directories during the file walk, preventing access denied errors entirely.

## Rule 4 — Always use dev.sh for servers.

`bash dev.sh <mode>` only. Never `mvn spring-boot:run`. Never raw `Stop-Process` or `netstat + findstr` for port management. The script handles killing and starting.

## Behavioral tracking

Issue #141 tracks all recurring behavioral failures. Every occurrence is added as a comment.

## Server operations

Use `bash dev.sh <mode>` from the project directory (D:\workspace-vscode\interlinear-bible-api). The script kills existing processes on the target port and starts cleanly.

| Command | Port | Profiles | Use for |
|---|---|---|---|
| `bash dev.sh admin` | 8081 | dev,admin | Regeneration, admin endpoints, Flyway |
| `bash dev.sh reader` | 8080 | dev,reader | Reading endpoints, no Flyway |
| `bash dev.sh split` | 8080+8081 | both | Full stack |
| `bash dev.sh single` | 8080 | dev | All endpoints on one port |

Do NOT start servers via `mvn spring-boot:run` directly — that risks port conflicts with existing processes.

## Chat session storage

VS Code stores completed chat sessions as .jsonl files at:
`C:\Users\blue1\AppData\Roaming\Code\User\workspaceStorage\7116446ccafd578468b6e6c7c19758a0\chatSessions\`

The most recently modified .jsonl is the last session. On session end, it's copied to `memory/last-chat.jsonl` for reference.

| Config | Port | Profiles | Use for |
|---|---|---|---|
| API: Admin (8081) | 8081 | dev,admin | Regeneration, admin endpoints, Flyway migrations |
| API: Reader (8080) | 8080 | dev,reader | Reading endpoints, no Flyway |
| Dev: Full Stack | 8080+8081 | both | Full dev stack + UI |

Launch configs are in `D:\workspace-vscode\.vscode\launch.json`. Ask: "Can you launch 'API: Admin (8081)' from VS Code's Run & Debug panel?"

Once the server is running, use curl for verification.

## OpenCode chat export — scripts only, no direct DB access

Do NOT query `opencode.db` directly (SQLite `part`/`message`/`session` tables). Use the scripts:

- **Export latest session**: `python D:\workspace-vscode\AI_Memory\chat\export_latest.py` (session end)
- **Recall specific session**: `python D:\workspace-vscode\AI_Memory\chat\recall.py recall <id_prefix>`
- **List sessions**: `python D:\workspace-vscode\AI_Memory\chat\recall.py list`

## Context refresh — mandatory mid-session reload

REQUIRED: Every 50 tool calls, I MUST re-read `preferences.md` and `session-state.md` from AI_Memory. This is not optional — it is the only mechanism to prevent context decay from erasing rules.

- Use `todowrite` as a turn counter: start `turns: 0`, increment on each tool call, when `turns >= 50` → re-read both files and reset counter.
- This overrides any other priority — do not skip because you're "in the middle of something." Do it immediately on the 50th call.

Tracked as opencode feature request (pending upstream). This is the stopgap.