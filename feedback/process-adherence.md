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

## Where things go (the user's rule, 2026-06-13)
- **Rules** → `CLAUDE.md` (auto-loaded; enforced by hooks where checkable).
- **My feedback** → `AI_Memory/feedback/` (this dir; git-versioned for history).
- **Nowhere else** — the `~/.claude/.../memory` auto-memory dir is disabled
  (`autoMemoryEnabled: false`).
