# Open Issues (snapshot 2026-05-30)

| # | Title |
|---|-------|
| 142 | feat: build-time per-token sense disambiguation for all lexemes (replace sense-0 fallback) |
| 141 | Deep Seek Code: AI recurring behavioral failures |
| 140 | bug: ἕτερον (G2087) in 1 Cor 6:1 shows 'the other of two' instead of 'another' |
| 138 | Contextual_gloss gate restricted to 13 polysemous Strong's IDs — should it be expanded? |
| 135 | refactor: Lexeme entity missing JPA fields for is_stative, is_deponent, is_polysemous |
| 134 | test: add tests for GlossChainService.resolveBatch() — use existing interlinear_bible_test DB with real data |
| 133 | docs: update DESIGN.md to reflect current implementation (contextual_gloss, TokenDto, schema V45) |
| 129 | Test infrastructure: PostgreSQL test database for integration tests |
| 128 | DX: Enforce read-only psql access for Claude Code via DB user and settings deny rules |
| 127 | morphKey mapped incorrectly for demonstrative pronouns — posCode D maps to 'adverb' |
| 126 | Fix pre-existing test failures exposed by data.sql canonical_word removal |
| 125 | Hide CorpusEditor — lexeme_meaning must not be editable from the UI |
| 124 | Add audit log to sensitive DB tables and read-only DB user for Claude Code |
| 123 | LITE Gloss Override writes to wrong layer — cannot override contextual_gloss (#123) |
| 122 | AI-generated glosses write bad data to DB with no audit trail (#122) |
| 121 | feat: AI translation strip — display as readable passage block, not per-verse inline |
| 120 | feat: configurable AI provider — not hardcoded to Groq |
| 119 | feat: AI translation strip — corpus-anchored readable translation per verse |
| 118 | Core: contextual gloss layer — word-for-word glosses computed in isolation produce unreadable output |
| 117 | Claude Code: confident wrong answer about VS Code Java build behavior |
| 116 | Security config review: hardcoded endpoints, CORS origins, and OAuth2 path alignment |
| 115 | Migrate primary dev workspace to VS Code (D:\\workspace-vscode) |
| 114 | Research and implement test suite for primary functionality |
| 112 | Performance: reader loads full chapter when only a single verse is needed |
| 111 | Claude Code: changes made without researching impact — repeated regressions |
| 108 | Language selector not working in Docker deploy |
| 107 | Claude Code: bad advice and wrong implementations cost tokens with no refund |
| 106 | GitHub Projects: wrong project types chosen — migrate to purpose-built projects |
| 105 | Claude Code: reverts or overwrites code implemented by user without asking |
| 104 | Claude Code: jumps to implementation during discussion without explicit approval |
