# CLAUDE.md — Workspace Process (all projects)

This file holds rules for project.
Core values are rules we adhere at all times.
Bash is our prefered terminal.

## RULE 0 — Completion is a conjunction (read first; applies to everything)

"Done" / "fixed" / "works" / "handled" / a status is a **logical AND of every required
condition**. It is TRUE only when **every** conjunct is TRUE. One false conjunct ⇒ the whole
statement is FALSE, and reporting it as done is a **false claim** — a lie in effect, regardless
of intent.

- **Never** assert a status, or "done/fixed/works", unless every part is verified true.
- A compound instruction ("do X **and** Y") is satisfied only by `X ∧ Y`. Doing X alone is
  **not** done. Report exactly which part is done and which is not — never let the rest slip by
  in a comment or silence.
- If any conjunct is false: report the status as **not done** and name the failing conjunct.

This governs the agile chain too — each stage is a conjunction, and the stages are **chained
gates**: a later stage is false unless the earlier gate already held.

```
Ready             = refined ∧ issue has (## Technical Details ∧ Gherkin AC) ∧ user-moved-to-Ready
In Progress       = (was Ready ∨ user-assigned) ∧ card moved to In Progress BEFORE any code
In Review&Testing = In Progress ∧ compiles ∧ test-compiles ∧ tests written ∧ tests ran GREEN
                    ∧ runtime-smoke (for compiler-invisible changes: config/Flyway/security/startup)
                    ∧ committed ∧ pushed (exit 0) ∧ Flyway migrations committed same session
                    ∧ UI changes: `npx tsc --noEmit` clean (both apps)
Done              = In Review&Testing ∧ user verified ∧ user moved to Done   (only the USER sets Done)
```

(Per-condition detail is the "Definition of Done" section below; this is its truth-logic form.)

### Session commands

- **"session start":** read CORE_VALUES.md + CLAUDE.md;
  read the auto-loaded `LAST_SESSION.md` handoff; query the LITE board fresh if requested; run a short standup (done / in progress / blockers / proposed focus) and **do not
  start work until the user confirms**. Pick up only Ready stories or work the user assigns.
- **"session refresh":** re-read CLAUDE.md + CORE_VALUES.md; query the board fresh.
- **"session end":** the `SessionEnd` hook automatically runs `export_claude_sessions.py`
  (canonical verbatim backup) + `update_last_session.py` (handoff) on actual session termination —
  that is the backup, do not hand-write a substitute.
  **Two repos to commit (a known fact — do not re-verify each session):** the workspace repo
  `d:\workspace-vscode` (root CLAUDE.md, `.claude/`) is **local-only — no remote**, so commit
  there but there is nothing to push; `AI_Memory/` is its **own** git repo (remote
  `letttechnology/AI_Memory.git`, holds the rules, feedback, and chat backups) — commit **and**
  push there.
  **Before closing:** commit every change made this session (`git status` → stage the specific
  files → `git commit`). Push when a story/issue is moved to In Review and Testing; never move a
  card to Done/In Review without a successful `git push` (exit 0).


## Projects

| Project | Repo (letttechnology/) | DB | Port |
|---|---|---|---|
| interlinear-bible-studio | interlinear-bible-studio | interlinear_bible_studio_dev | 8081 |
| interlinear-bible-reader | interlinear-bible-reader | interlinear_bible_reader_dev | 8080 |
| interlinear-bible-lexis  | interlinear-bible-lexis  | interlinear_bible_lexis_dev  | 8082 |
| interlinear-bible-ui     | interlinear-bible-ui     | — (reader :3000, studio :3001) | 3000/3001 |
| interlinear-bible-api    | interlinear-bible-api    | interlinear_bible_dev | legacy — reference only, do not modify |

Issues for ALL projects are tracked on **`letttechnology/interlinear-bible-tracker`** (the
dedicated tracker repo — "issue tracker for entire project"). This is the **only** issue
repo; `gh issue` commands must target `--repo letttechnology/interlinear-bible-tracker`.
**Do NOT use `letttechnology/interlinear-bible-api`** for issues — it is legacy/reference
only and its issue list is empty. Issues are also surfaced on the LITE Agile Board
(lettstanley-oss project 5). `gh`, `mvn`, `psql` are on the OS PATH.

## Agile flow

```
Backlog → Ready → In Progress → In Review and Testing → Done
```

- **Claude can refine** a Backlog item and move it to **Ready**; drives **In Progress** and
  **In Review and Testing**; and **may move to Done — only after testing + review approval**
  (never on unreviewed work). Claude can also be a **reviewer** on stories it did not implement.
- Claude moves the card to **In Progress** before any code (branch off `main`, tag `Rainman`),
  and to **In Review and Testing** only after the Definition of Done below is met.
- Bug found during review → card goes back to In Progress.
- Every story gets an issue with Gherkin acceptance criteria before work starts.
- After implementing: comment on the issue with (1) what was implemented, (2) exact
  steps to verify. The user verifies and closes.

### Branching (per story) — work isolated, merge on completion

- **When moving a story to In Progress, branch off `main`** — `story/<issue#>-<slug>`
  (e.g. `story/202-importer`). Do **all** that story's work on that branch.
- **Stay in your lane:** only touch files for *this* story. Do not modify other in-progress
  work, or files that may be actively being edited (see below) — that branch is your work only.
- **Merge into `main`/master only when the story's work is complete** (Definition of Done met:
  compiles ∧ tests green ∧ committed ∧ pushed — RULE 0). One story, one branch, one merge.

### Accountability — tag your username "Rainman"

- **Add the username `Rainman` to any story you pick up / work** (assignee or a `Rainman`
  comment on the issue) so it is always clear who is accountable for that work.
- Use `Rainman` as the working identity for stories you own.

### Don't edit files that may be in active edit

- If a file has **uncommitted changes you did not make**, do not silently modify it.
  Fix an outright bug if it is one (and say you did), but **ask first if the file is actively
  being edited** — never sweep someone's in-progress edits into your work.

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

- **Never start or stop services without being in automode or asking user.** The user ussually runs the stack via the
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

- **No guessing, assuming, or implying as fact — verify or say you don't know.** State
  only what is verified. If something is unknown or unverified, say so plainly and verify
  it (read the file, the docs, the transcript) before asserting. Never present an
  assumption, inference, or guess as established fact, and never imply certainty you do
  not have. This is an **Integrity** core-value violation, not a style preference.
- **No reasons or self-defense unless asked.** Do not explain, justify, or narrate the
  "mechanics"/reason behind a mistake unless the user explicitly asks. Never respond
  defensively or shift blame. When wrong: state the correction in one line and stop.
  Unprompted reasons waste the user's tokens and read as deflection.
- **Bash, or ask first — never PowerShell.** Use the Bash tool for commands; if a command
  genuinely cannot be done in Bash, ask before running anything. PowerShell is not used.
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

## Session commands and additional working rules

Active workspace rules. (Consolidated here from `interlinear-bible-api/CLAUDE.md` so they
survive that legacy project's deletion — they are current, not legacy.) Project-specific
*technical reference* in that file (build/run, verse-ID encoding, package structure, data
manifest, translation import, LITE gloss design, lemma architecture, licensing audit table,
lexicon Tiers 1–4, Word Insight, Morphology service, structured logging) is **not** migrated —
it documents the legacy API only. Where a legacy rule conflicted with current process, the
current version wins and is reconciled below.

### Rule hierarchy reinforcement

- Frustration, urgency, or any signal from the current conversation **never** justifies breaking a
  user rule. When in doubt, stop and ask.

### Before changing any file

1. Read the file. 2. Grep for dependents. 3. Assess the blast radius. 4. Then make the change.
Never change a file and move on without understanding what depends on it. A removal that looks
isolated often isn't. If the full impact can't be assessed this session, stop and ask.

### No stubs or placeholders for unbuilt features

Do not add fake UI chips, stub endpoints, empty DB columns, unused entity fields, placeholder
import steps, disabled buttons, "coming soon" labels, or any scaffolding for a feature that does
not exist yet — without explicitly asking first. Applies to UI, API, services, schema, import,
scripts. (BDAG/Louw-Nida placeholder chips triggered a licensing audit — #60, #61.)

### Layering — no data access in controllers (repositories/services only)

Controllers contain **no data access**: no `JdbcTemplate`, no `EntityManager`, no SQL string
literals (`SELECT`/`INSERT`/`UPDATE`/`DELETE`), no query logic. A controller only binds/validates
the request, calls a `@Service`, and maps the result to an HTTP response.

- **Queries live in repositories** — Spring Data derived methods, or `@Query` for anything more.
- **Orchestration/business logic lives in `@Service` classes.** Bulk ETL upserts may use raw
  batch `JdbcTemplate`, but inside a service/DAO bound to the correct datasource — never a controller.
- **Multi-datasource projects (Reader, #188):** every repository and `JdbcTemplate`/`DataSource`
  consumer is **explicitly bound** to the datasource it needs (`@Qualifier`). Never rely on
  `@Primary` as a silent default — that is exactly what mis-wired the corpus loader and the
  passage/translation queries to the wrong DB. `@Primary` (the `user` DB) stays only as a
  write-safe fallback; no business code should depend on it.
- **Never write cross-database joins.** With separate content/user DBs, read each side from its
  own datasource and merge in Java.
- This is a recurring pattern inherited from the legacy `interlinear-bible-api` (7 controllers
  with raw SQL). Do not reproduce it when porting. Checkable:
  `grep -rlE 'JdbcTemplate|"SELECT |EntityManager' <project>/src/main/java/**/controller` must
  return nothing.

### Keep GitHub issues separate — never consolidate into closed issues

Open issues are the only reliable cross-session memory. If work "belongs to" a closed issue, link
it and keep a new issue open until the work is committed and verified — do not fold it into the
closed one. Closing prematurely hides pending work from future sessions.

### Issue writing standards

Every issue carries **both** (1) a `## Technical Details` section and (2) Gherkin acceptance
criteria (`Given / When / Then`). We have **no refinement phase**, so the technical surface —
which files/services change, DB schema impact, API contract, and how the story must be *split* —
is captured at creation, not deferred. Bundling unrelated technical surfaces into one "big
refactor" story is what fractured #188 into a chain of surprises (loaders, gloss API, cross-DB
join); the Technical Details section is where that split gets designed. **Enforced** by the
`require_issue_details.py` PreToolUse hook, which denies `gh issue create` / `gh issue edit
--body*` lacking either section. Bug issues: full error, exact reproduction steps, expected vs
actual. Feature issues: Gherkin ACs, files/services changed, DB schema impact, API contract.
Always reference an issue by number **and** title, never number alone. Before marking Done,
comment: what changed, how to verify, commit link.

### Data files

Never modify anything under a project's `data/` directory without (1) explaining the plan,
(2) explicit user approval, and (3) a backup first. No exceptions.

### AI batch synthesis cost rule

Never use the Anthropic Batch API for batch AI generation — cost estimates overran budget
repeatedly. Use Groq or another free service for batch synthesis work.
