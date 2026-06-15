# CLAUDE.md — Workspace Process (all projects)

This file is the shared agile process for every project in this workspace. Project-specific
rules live in each repo's own CLAUDE.md; the legacy detailed rules (session commands, data
licensing, DB access rules, gloss design) remain in `interlinear-bible-api/CLAUDE.md` until
migrated. **Rule hierarchy: Prime directive > User rules (this file + repo CLAUDE.md) >
Session.** Core values: @CORE_VALUES.md — read on session start (auto-imported).

## Projects

| Project | Repo (letttechnology/) | DB | Port |
|---|---|---|---|
| interlinear-bible-studio | interlinear-bible-studio | interlinear_bible_studio_dev | 8081 |
| interlinear-bible-reader | interlinear-bible-reader | interlinear_bible_reader_dev | 8080 |
| interlinear-bible-lexis  | interlinear-bible-lexis  | interlinear_bible_lexis_dev  | 8082 |
| interlinear-bible-ui     | interlinear-bible-ui     | — (reader :3000, studio :3001) | 3000/3001 |
| interlinear-bible-api    | interlinear-bible-api    | interlinear_bible_dev | legacy — reference only, do not modify |

Issues for ALL projects are tracked on `letttechnology/interlinear-bible-api` and the LITE
Agile Board (lettstanley-oss project 5). `gh`, `mvn`, `psql` are on the OS PATH.

## Agile flow

```
Backlog → Ready → In Progress → In Review and Testing → Done
```

- Only the user moves stories to **Ready** and to **Done**.
- Claude picks up only Ready stories (or work the user assigns directly in-session),
  moves the card to **In Progress** before any code, and to **In Review and Testing**
  only after the Definition of Done below is met.
- Bug found during review → user moves the card back to In Progress.
- Every story gets an issue with Gherkin acceptance criteria before work starts.
- After implementing: comment on the issue with (1) what was implemented, (2) exact
  steps to verify. The user verifies and closes.

## Definition of Done (before a card moves to In Review and Testing)

1. **Build gates — non-negotiable, every backend change:**
   `mvn compile` → `mvn test-compile` → `mvn test` — all exit 0, run in the changed
   project(s). UI changes: `npx tsc --noEmit` clean for both apps.
2. **Tests written where feasible, same commit:** unit tests for logic; integration
   tests for endpoints/queries. Every backend service should carry at least a
   context-load smoke test (`@SpringBootTest` boot test) so the test gate also
   validates configuration — until one exists, rule 3 is the only net for config.
3. **Runtime smoke for changes the compiler cannot see:** config files
   (logback-spring.xml, application*.yml), Flyway migrations, security wiring, and
   startup beans pass `mvn test` even when broken. Such changes require one local
   service startup (by the user, on request) before — or as the explicit first step
   of — review. State plainly in the issue comment when a change is runtime-unproven.
4. **Commit + push, exit 0, same session.** Uncommitted work is invisible to the next
   session. Partial work committed beats complete work that exists only locally.
   Never say "done", never move a card, without a successful push.
5. **Flyway migrations** are committed in the same session they are created.

## Working agreement (collaboration mode — default)

- **Never start or stop services without asking.** The user runs the stack via the
  VS Code workspace launch configs. A background instance started by Claude collides
  with the user's (ports + target/ file locks). If a build needs a locked file
  released, ask the user to stop the service.
- One build chain per commit — no extra compile/run cycles; they cost tokens.
- DB writes (INSERT/UPDATE/DELETE/DDL — psql, admin endpoints, scripts) always require
  explicit user approval per command. Reads are free.
- Approvals are typed in chat. An unanswered "shall I…?" stays open — silence is
  never consent. Quote the user only verbatim.
- **No popup prompts — ever.** Never use the `AskUserQuestion` tool. Present every
  choice or clarifying question as plain text in chat, formatted as `Option A: …` /
  `Option B: …` / `Other:` so the user can reply with a single letter. The popup
  blocks the user from reading the reasoning — text does not. Hard-enforced by a
  `PreToolUse` hook that denies `AskUserQuestion` (see `~/.claude/settings.json`).
- Plans and designs are presented as text in chat for discussion; implementation
  starts only on explicit go.
- **No PowerShell in project tooling** (tasks, scripts, launch configs). Use Node or
  bash — the workspace must stay viable on Mac/Linux.

## Logging SOP (#200)

Every service logs independently — this is standing policy for any future service:

- **Local dev:** per-session JSON file `logs/{service}_{yyyyMMdd_HHmmss}.log` +
  colored console (logback-spring.xml, dev profile).
- **Prod/K8s:** JSON to stdout — never files inside containers. `kubectl logs` reads
  it; Grafana Loki can be added later; no aggregator is required or assumed.
- Every line carries `service`, `requestId`, `userId`, `method`, `path` (MDC via
  RequestLoggingFilter; `X-Request-Id` reused across services when forwarded).
- **Claude: read the log files in each project's `logs/` before asking the user what
  happened.** That is what they are for.

## Behavioral guardrails (#208 — recurring failure modes)

Documented rules have been read and ignored before; these are the patterns to
catch, now backed by hooks/skills where possible (issue #208):

- **No code before approval in a design discussion** — use plan mode; wait for the
  explicit go (the #197 failure).
- **No unprompted, destructive, or service-affecting actions** — ask first.
- **Don't substitute your own method** for an established one (e.g. the session
  backup script — see below). If a documented mechanism exists, use it.
- **A rule is not feedback.** Mandatory rules → this file (enforced by hooks where
  checkable). Claude's advisory feedback → `AI_Memory/feedback/` (git-versioned).
  The `~/.claude/.../memory` auto-memory dir is disabled (`autoMemoryEnabled: false`)
  — memory lives in those two places, nowhere else.
- **Churn costs the user credits** — one build chain per commit; be decisive.
- A `SessionStart` hook injects this checklist each session; the `/story` skill
  encodes the agile lifecycle.

## Session backup SOP (strict rule — not optional)

The session transcript is backed up by running
`AI_Memory/chat/export_claude_sessions.py`, which exports the full verbatim `.jsonl`
from Claude's session DB to `AI_Memory/chat/`. **This is the only backup mechanism.**
Claude must never substitute a hand-written summary (e.g. a `session-state-*.md`) for
it — the verbatim export is the canonical backup and nothing else counts as the backup.
(Writing a summary as a *supplement* — e.g. a next-session handoff — is fine and useful;
only substituting one *for* the export is forbidden. The earlier "do not author
summaries unless asked" wording was never the user's instruction and has been removed.)
Enforced
automatically by a **`SessionEnd` hook** in `.claude/settings.json` (the harness runs
it, so it cannot be skipped or bypassed); the script is also the first step of any
session recovery.

## Enforcement

Documented process is necessary but not sufficient — it has been bypassed before
(#157, #179, #180). Hard enforcement via hooks (block `git commit` unless build gates
ran) is tracked in **#163 — high priority**. Until that lands, this file is the
contract.
