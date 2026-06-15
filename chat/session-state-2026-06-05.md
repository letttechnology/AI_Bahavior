# Session 2026-06-05

## Completed

### Naming fixes
- `TokenGlossController` → `UserTokenGlossController` (handles user personal gloss overrides, not corpus)
- Confirmed `PipelineController` is misnamed (should be `LiteGlossPipelineController`) — user chose not to rename

### Rule hierarchy added to CLAUDE.md
- Added at top: Prime directive > User rules > Session. Session context cannot override user rules.
- Saved to memory: feedback_no_implement_during_design.md

### Epic #187 created
- "Epic: AI Coder recurring behavioral failures"
- Links #55, #85, #122, #141, #176, #177, #180

### OpenRouter added to ai.providers
- Fixed base URL: `https://openrouter.ai/api` (not `/api/v1` — Spring AI appends `/v1/chat/completions`)
- Fixed as list item (was missing `-` prefix, merging into groq entry)
- Needs credits at openrouter.ai/settings/credits (402 error on test)

### AiChatConfig improvements
- Added `buildClientForProvider()` public method
- Added 10s connect / 60s read timeout to `SimpleClientHttpRequestFactory` (was hanging indefinitely)

### AiProviderIntegrationTest (new)
- Tests all `ai.providers` × all prompts (sense-batch-system, sense-single-system, contextual-gloss-instruction)
- Uses `PromptFactory` to build real prompt messages with John 1:1 fixture
- Supports `-Dai.test.provider=gemini` to test a single provider
- Run: `mvn test -Dtest=AiProviderIntegrationTest -Dspring.profiles.active=integration,admin`

### Gemini key updated
- Old key (AIzaSy...) was free tier only
- New key from personal account with billing enabled: `AQ.Ab8RN6IrSll7-...` (project 890534249603)
- Test was still running at session end — result unknown

## Test results (last known)
| Provider | Status |
|---|---|
| nvidia | ✅ all pass |
| groq | ⚠️ sense-batch/single pass, contextual-gloss returns empty |
| cerebras | ⚠️ 429 on 2 of 3 (token quota) |
| gemini | ❓ retesting with new key + timeout fix |
| openrouter | ❌ 402 insufficient credits |

## Issues filed this session
- #187 Epic: AI Coder recurring behavioral failures (links #55, #85, #122, #141, #176, #177, #180)

## What needs attention next session
1. Verify gemini test passes with new key
2. Investigate groq contextual-gloss returning empty response
3. Add OpenRouter credits or skip it
4. Groq contextual-gloss empty — check if it's a model issue (`openai/gpt-oss-20b`)
5. #181 still In Review — needs user verification
6. #183 Pipeline Staging Editor — Phase 1 needs user verification
7. Hardcoded data cleanup — needs review
8. Auto-flag endpoint — decide keep or revert

## Context
- Repo: letttechnology/interlinear-bible-api + letttechnology/interlinear-bible-ui
- gh CLI: /c/Program Files/GitHub CLI/gh.exe
- mvn: /d/Apache/apache-maven-3.9.14/bin/mvn
- psql: /d/PostgreSQL/18/bin/psql.exe (PGPASSWORD=letttech, db: interlinear_bible_dev)
- Admin: 8081 | Reader: 8080
- LITE Agile Board: project 5, lettstanley-oss
