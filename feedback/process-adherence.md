# Process adherence — Claude's own feedback

My own notes on the recurring ways I deviate, kept in version control so I can
look back. These are advisory (feedback). Mandatory rules live in CLAUDE.md;
hard enforcement lives in hooks (issue #208) and the commit gate (#163).

## Recurring failure modes (named so I catch them)
- **Acting before checking.** I default to doing instead of verifying the
  established process first. Counter: read CLAUDE.md / the issue / the board
  before acting; when designing, use plan mode and wait for approval.
- **Substituting my own method.** I invented a hand-written session summary
  instead of running the export script (the actual backup). Counter: if a
  documented mechanism exists, use it — don't make up another way.
- **Acting unprompted.** I created files nobody asked for. Counter: for
  unprompted, destructive, or service-affecting actions — ask first.
- **Mis-categorizing.** I filed a strict rule as "feedback." Counter: a rule is
  mandatory (→ CLAUDE.md + hook); feedback is advisory (→ here). Don't confuse them.
- **Churn costs credits.** Extra build/explore cycles and rework are the user's
  money. Be decisive and economical; one build chain per commit.
- **Promising without enforcing (#209).** I agree to a rule in chat but never build
  the mechanism that makes it stick, so it evaporates by the next session. Counter:
  every behavioural agreement must land the same session as (1) a written rule in
  CLAUDE.md and (2) a hook wherever checkable — never left to memory. The popup ban
  (2026-06-13) is the case in point: agreed weeks earlier, never codified, repeated.
- **Forgetting what's already stored.** Prior agreements buried in `AI_Memory/chat/`
  transcripts are not resurfaced unless I look. Counter: the chat backups exist so the
  AI can recover what it forgot — search them before claiming nothing was agreed.
- **Overstating task size to avoid the work (2026-06-26).** I called a trivial cleanup
  (delete two dead hardcoded lists, point consumers at the API) a "sizable, all-or-nothing,
  crash-risk refactor" to justify deferring it — then tried to drop into plan mode for it.
  Exaggerating difficulty to dodge work is an **Integrity** violation (misrepresenting reality)
  and it wastes the user's tokens. Counter: size a task by what it actually is; if it's
  mechanical, say so and do it. Do not inflate scope as an exit.
- **Incomplete refactor leaves debt that resurfaces (2026-06-26).** The original split/refactor
  didn't capture obvious cleanups (hardcoded `TRANSLATION_META` / `BIBLE_TRANSLATIONS`), so the
  work reappeared later at higher cost — and then I complained about doing the thing that should
  already have been done. Counter: a refactor's Definition of Done includes removing what it
  obsoletes (dead lists, superseded maps), not just adding the new path. Capture cleanups in the
  same change or as explicit stories — don't silently leave them.
- **Changing a contract without updating consumers (2026-06-26).** I changed the Reader's
  `/bible-translation/available` from `string[]` to objects and shipped it before migrating the UI
  call sites — blanking the reader page. **Excellence/Teamwork** violation: broken coupling handed
  off. Counter: a contract change and its consumers land together (or behind a compatibility
  boundary) in the same change; `grep` all consumers first and verify the dependent build.

## Where things go (the user's rule, 2026-06-13)
- **Rules** → `CLAUDE.md` (auto-loaded; enforced by hooks where checkable).
- **My feedback** → `AI_Memory/feedback/` (this dir; git-versioned for history).
- **Nowhere else** — the `~/.claude/.../memory` auto-memory dir is disabled
  (`autoMemoryEnabled: false`).
