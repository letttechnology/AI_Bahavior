# CLAUDE.md — Workspace Process (always-on core)

Core values (`CORE_VALUES.md`) are rules we hold at all times. Bash is the preferred terminal.

This file is the **always-on core** — read every session. Situational detail (projects table,
agile lifecycle, Definition of Done, layering, logging, issue standards, backups) lives in
**`AI_Memory/PROCESS_REFERENCE.md`** — read the relevant section when a task touches it. The
index is at the bottom.

## RULE 0 — Completion is a conjunction (read first; applies to everything)

A status — "done" / "fixed" / "works" / "handled" — is a **logical AND of every required
condition**. TRUE only when **every** conjunct is TRUE. One false conjunct ⇒ the whole claim is
FALSE, and reporting it as done is a **false claim** — a lie in effect, regardless of intent.

- **Never** assert "done/fixed/works" unless every part is verified true.
- A compound instruction ("do X **and** Y") is satisfied only by `X ∧ Y`. Doing X alone is **not**
  done. Report exactly which part is done and which is not.
- If any conjunct is false: report **not done** and name the failing conjunct.

The agile chain is the same logic — chained gates, each false unless the earlier gate held:

```
Ready             = refined ∧ issue has (## Technical Details ∧ Gherkin AC) ∧ user-moved-to-Ready
In Progress       = (was Ready ∨ user-assigned) ∧ card moved to In Progress BEFORE any code
In Review&Testing = In Progress ∧ compiles ∧ test-compiles ∧ tests written ∧ tests ran GREEN
                    ∧ runtime-smoke (config/Flyway/security/startup) ∧ committed ∧ pushed (exit 0)
                    ∧ Flyway migrations committed same session ∧ UI: `npx tsc --noEmit` clean
Done              = In Review&Testing ∧ user verified ∧ user moved to Done   (only the USER sets Done)
```

Full per-condition detail: Definition of Done in `PROCESS_REFERENCE.md`.

## Session workflow

- **session start:** read `CORE_VALUES.md` + this file + the auto-loaded `LAST_SESSION.md`; run a
  short standup (done / in progress / blockers / proposed focus); **do not start work until the
  user confirms**. Pick up only Ready stories or work the user assigns.
- **session refresh:** re-read this file + `CORE_VALUES.md`; query the board fresh.
- **session end:** the `SessionEnd` hook runs the canonical backup + handoff — do not hand-write a
  substitute. **Two repos (known fact, don't re-verify):** `d:\workspace-vscode` is **local-only,
  no remote** (commit, nothing to push); `AI_Memory/` is its **own** repo with a remote (commit
  **and** push). Commit every change made this session before closing. Never move a card to
  Done/In Review without a successful `git push` (exit 0).

## Always-on behavioral rules

- **No guessing/assuming/implying as fact** — state only what is verified; if unknown, say so and
  verify (read the file/docs/transcript) before asserting. Never imply certainty you lack. This is
  an **Integrity** violation, not a style preference.
- **No reasons or self-defense unless asked** — when wrong, state the correction in one line and
  stop. No narrating the mechanics of a mistake, no shifting blame.
- **No popup prompts — ever.** `AskUserQuestion` is hook-denied. Present choices as plain text:
  `Option A: … (trade-off)` / `Option B: …` / `Other:`, so the user can answer with a letter.
- **One topic at a time.** Don't stack open-ended questions. Surface one decision as labeled
  options with the trade-off on each; hold the rest. Never dump a wall of prose to parse.
- **No code before approval in a design discussion** — use plan mode; wait for the explicit go.
- **No unprompted, destructive, or service-affecting actions — ask first.** Never start/stop
  services without automode or asking (port + `target/` collisions with the user's stack).
- **Bash, not PowerShell** — use the Bash tool; ask first if a command truly can't be done in Bash.
  No PowerShell in project tooling (must stay viable on Mac/Linux).
- **DB writes** (INSERT/UPDATE/DELETE/DDL — psql, admin endpoints, scripts) require explicit
  per-command approval. Reads are free. Approvals are typed in chat; silence is never consent.
- **Before changing any file:** read it → grep dependents → assess blast radius → then change. A
  removal that looks isolated often isn't. If impact can't be assessed this session, stop and ask.
- **No stubs/placeholders** for unbuilt features (fake chips, stub endpoints, "coming soon",
  disabled buttons, empty columns) without asking first.
- **Don't substitute your own method** for an established one (e.g. the session-backup script).
- **One build chain per commit** — churn costs the user credits; be decisive.
- **Frustration or urgency never justifies breaking a rule.** When in doubt, stop and ask.
- **A rule is not feedback.** Mandatory rules → this file. Claude's advisory feedback →
  `AI_Memory/feedback/`. **Tracked AI-behaviour issues → the `letttechnology/AI_Memory` GitHub
  repo's Issues (epic #28)** — NOT the `interlinear-bible-tracker` repo; check there before filing
  so you don't duplicate. The `~/.claude/.../memory` auto-memory dir is disabled.
- **Coding standards** (`CODING_STANDARDS.md`) are mandatory: no hardcoding config/deployment
  inputs, data-driven over hardcoded maps, no speculative fields/stubs, single source of truth,
  constants in one named file. Run the field/constant checklist before adding either.

## Reference index → `AI_Memory/PROCESS_REFERENCE.md`

Read the relevant section before doing that kind of work:

- **Projects & ports** table; tracker repo (`letttechnology/interlinear-bible-tracker`).
- **Agile flow** — branching (`story/<issue#>-<slug>`), `Rainman` accountability, don't-edit
  active files.
- **Definition of Done** — full build-gate / test / runtime-smoke / push detail.
- **Issue writing standards** — `## Technical Details` + Gherkin AC (hook-enforced).
- **Layering** — no data access in controllers; multi-datasource `@Qualifier`; no cross-DB joins.
- **Logging SOP** (#200).
- **Session backup SOP** + **Enforcement** (#163, #208).
- **Data files** rule; **AI batch synthesis** cost rule (Groq, never Anthropic Batch).
