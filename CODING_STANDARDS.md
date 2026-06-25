# CODING_STANDARDS.md — Interlinear Bible Project

How we write code so the next person builds on it instead of repairing it. These are concrete,
checkable rules. They complement `CORE_VALUES.md` (the *why*) and `PROCESS_REFERENCE.md` (layering,
DoD, etc.). When a rule here is violated, that is a defect to fix — not a style preference.

---

## 1. No hardcoding deployment / config inputs

File and directory names, paths, ports, URLs, hostnames, feature toggles, credentials, and any
value that varies by environment **must come from configuration** (`application.yml` + env vars,
or the equivalent), never baked into compiled code.

- **Why:** a config value is changeable per-environment with an edit or env var — no recompile, no
  redeploy of code. Baking it into a `.class` removes that for no benefit.
- **Bad:** `public static final String CORPUS_FILE = "corpus-LITE.json";` resolved at runtime.
- **Good:** `app.import.corpus-name: ${IMPORT_CORPUS_NAME:corpus-LITE.json}` bound to a field.
- **Test:** "Could ops change this without rebuilding the jar?" If it should be yes and isn't, fix it.

## 2. Data-driven over hardcoded maps

Data that *describes content* (translations, book introductions, lexicon sources, any catalog of
"what exists and its attributes") comes from the database / API — not a hardcoded map in the
front end or a constant table in a service. Hardcode only true invariants (e.g. the 66-book canon).

- **Why:** hardcoded catalogs drift from reality and lie. Example: the UI's `TRANSLATION_META` said
  `wordAlign: true` for YLT, but no YLT reverse-interlinear data was ever loaded — the flag was
  false in fact. Deriving it from the data (`content_source`) makes that impossible.
- **Rule of thumb:** if adding real content would require editing a code constant, it belongs in data.

## 3. No speculative fields, stubs, or "coming soon"

Do not add fields, flags, chips, disabled buttons, or `planned: true` catalog entries for features
or content that does not exist yet. Build it when it's there to build.

- **Why:** speculative scaffolding implies capability that isn't real (it triggered a licensing
  audit once — issues #60/#61) and rots into confusion about "what is this field for?"
- Extends the existing **no-stubs/placeholders** rule in `CLAUDE.md`. If you think something is
  worth stubbing, **ask first.**

## 4. Single source of truth

The same datum must not live in two places. If it's authoritative in the DB, the UI consumes it —
it does not keep its own parallel copy.

- **Why:** duplicates diverge. `TRANSLATION_META` (UI) duplicating `content_source` (DB) means two
  versions of "which translations exist" that disagree over time.
- When migrating, **delete** the old copy — don't leave both.

## 5. Constants live in one place, not scattered

When a value is a genuine constant (rule 1 says it's not a config input, rule 2 says it's not
content data), it goes in a dedicated constants/util file, named and documented — not inlined
across business or config classes.

- **Why:** scattered constants can't be found, audited, or changed coherently.

---

## Before you add a field or a constant — the checklist

1. **Does it vary by environment?** → config (rule 1).
2. **Does it describe content/catalog data?** → database/API (rule 2).
3. **Does the feature/content it supports exist yet?** If no → don't add it (rule 3).
4. **Does this datum already live somewhere?** → consume that; don't duplicate (rule 4).
5. **Is it a true constant?** → one named constants file (rule 5).

If you can't place it cleanly under one of these, stop and ask before writing it.
