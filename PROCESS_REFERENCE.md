# PROCESS_REFERENCE.md — situational detail

Reference material extracted from `CLAUDE.md` so the always-on core stays small. These are
**still mandatory rules** — read the relevant section before doing that kind of work. The core
file (`CLAUDE.md`) holds RULE 0, the session workflow, and the always-on behavioral rules.

## Projects & tracker

| Project | Repo (letttechnology/) | DB | Port |
|---|---|---|---|
| interlinear-bible-studio | interlinear-bible-studio | interlinear_bible_studio_dev | 8081 |
| interlinear-bible-reader | interlinear-bible-reader | interlinear_bible_reader_dev | 8080 |
| interlinear-bible-lexis  | interlinear-bible-lexis  | interlinear_bible_lexis_dev  | 8082 |
| interlinear-bible-ui     | interlinear-bible-ui     | — (reader :3000, studio :3001) | 3000/3001 |
| interlinear-bible-api    | interlinear-bible-api    | interlinear_bible_dev | legacy — reference only, do not modify |

Issues for ALL projects are tracked on **`letttechnology/interlinear-bible-tracker`** — the only
issue repo; `gh issue` commands must target `--repo letttechnology/interlinear-bible-tracker`. Do
**not** use `interlinear-bible-api` for issues (legacy/reference only). Issues also surface on the
LITE Agile Board (lettstanley-oss project 5). `gh`, `mvn`, `psql` are on the OS PATH.

## Agile flow

```
Backlog → Ready → In Progress → In Review and Testing → Done
```

- **Claude can refine** a Backlog item → Ready; drives In Progress and In Review and Testing; **may
  move to Done only after testing + review approval** (never on unreviewed work). Claude can also be
  a **reviewer** on stories it did not implement.
- Move the card to **In Progress before any code**; to **In Review and Testing** only after the
  Definition of Done is met. Bug found during review → back to In Progress.
- Every story gets an issue with Gherkin AC before work starts. After implementing, comment with
  (1) what was implemented, (2) exact verification steps. The user verifies and closes.

### Branching (per story)

- **Moving to In Progress → branch off `main`:** `story/<issue#>-<slug>` (e.g. `story/202-importer`).
  Do **all** that story's work on that branch.
- **Stay in your lane** — only touch files for *this* story; don't sweep in others' in-progress
  edits.
- **Merge into `main`/master only when the story is complete** (DoD met). One story, one branch,
  one merge.

### Accountability — `Rainman`

- Add `Rainman` to any story you pick up (assignee or a `Rainman` comment) so accountability is
  clear. Use `Rainman` as the working identity for stories you own.

### Don't edit files in active edit

- If a file has **uncommitted changes you did not make**, don't silently modify it. Fix an outright
  bug (and say so), but **ask first if the file is actively being edited**.

## Definition of Done (before a card moves to In Review and Testing)

1. **Build gates — non-negotiable, every backend change:** `mvn compile` → `mvn test-compile` →
   `mvn test`, all exit 0, in the changed project(s). UI: `npx tsc --noEmit` clean for both apps.
2. **Tests written where feasible, same commit:** unit tests for logic; integration tests for
   endpoints/queries. Every backend service should carry a context-load smoke test
   (`@SpringBootTest`) so the test gate also validates configuration.
3. **Runtime smoke for changes the compiler can't see:** config files (logback-spring.xml,
   application*.yml), Flyway migrations, security wiring, startup beans pass `mvn test` even when
   broken. Such changes require one local service startup (by the user, on request) before — or as
   the explicit first step of — review. State plainly when a change is runtime-unproven.
4. **Commit + push, exit 0, same session.** Partial work committed beats complete work that exists
   only locally. Never say "done", never move a card, without a successful push.
5. **Flyway migrations** committed the same session they are created.

## Issue writing standards

Every issue carries **both** (1) a `## Technical Details` section and (2) Gherkin AC
(`Given / When / Then`). No refinement phase — capture the technical surface (files/services
changed, DB schema impact, API contract, how the story splits) at creation. **Enforced** by the
`require_issue_details.py` PreToolUse hook, which denies `gh issue create` / `gh issue edit
--body*` lacking either section. Bug issues: full error, exact reproduction, expected vs actual.
Always reference an issue by number **and** title. Before marking Done, comment: what changed, how
to verify, commit link.

**Keep issues separate — never consolidate into closed issues.** Open issues are the only reliable
cross-session memory. If work "belongs to" a closed issue, link it and keep a new issue open until
committed and verified — don't fold it into the closed one.

## Layering — no data access in controllers

Controllers contain **no data access**: no `JdbcTemplate`, no `EntityManager`, no SQL literals, no
query logic. A controller binds/validates the request, calls a `@Service`, maps the result to HTTP.

- **Queries live in repositories** — Spring Data derived methods or `@Query`.
- **Orchestration/business logic in `@Service`.** Bulk ETL upserts may use batch `JdbcTemplate`,
  but inside a service/DAO bound to the correct datasource — never a controller.
- **Multi-datasource projects (Reader, #188):** every repository / `JdbcTemplate` / `DataSource` is
  **explicitly bound** with `@Qualifier`. Never rely on `@Primary` as a silent default.
- **Never write cross-database joins** — read each side from its own datasource, merge in Java.
- Checkable: `grep -rlE 'JdbcTemplate|"SELECT |EntityManager' <project>/src/main/java/**/controller`
  must return nothing.

## Logging SOP (#200)

Every service logs independently:

- **Local dev:** per-session JSON file `logs/{service}_{yyyyMMdd_HHmmss}.log` + colored console
  (logback-spring.xml, dev profile).
- **Prod/K8s:** JSON to stdout — never files inside containers. `kubectl logs` reads it.
- Every line carries `service`, `requestId`, `userId`, `method`, `path` (MDC via
  RequestLoggingFilter; `X-Request-Id` reused across services when forwarded).
- **Read the log files in each project's `logs/` before asking the user what happened.**

## Session backup SOP (strict)

The transcript is backed up by `AI_Memory/chat/export_claude_sessions.py`, which exports the full
verbatim `.jsonl` to `AI_Memory/chat/`. **This is the only backup mechanism** — never substitute a
hand-written summary *for* it (a supplemental handoff is fine). Enforced by a `SessionEnd` hook in
`.claude/settings.json`; the script is also the first step of session recovery.

## Enforcement (#163, #208)

Documented process has been bypassed before (#157, #179, #180). Hard enforcement via hooks (e.g.
block `git commit` unless build gates ran) is tracked in **#163 (high priority)**; recurring
failure-mode guardrails are #208. Until full hook coverage lands, `CLAUDE.md` + this file are the
contract. A `SessionStart` hook injects the checklist each session; the `/story` skill encodes the
agile lifecycle.

## Data files

Never modify anything under a project's `data/` directory without (1) explaining the plan,
(2) explicit user approval, and (3) a backup first. No exceptions.

## AI batch synthesis cost rule

Never use the Anthropic Batch API for batch AI generation — cost overran budget repeatedly. Use
Groq or another free service for batch synthesis work.
