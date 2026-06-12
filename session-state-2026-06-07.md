# Session State — 2026-06-07

## What was done

### Issue #188 — Resilient LLM Gateway (completed from prior session)
- All code was already committed from the prior session
- Added issue to LITE Agile Board, moved to In Review and Testing
- Added verification comment to issue #188

### VertexAiIntegrationTest.java — NEW
- Added `src/test/java/com/interlinear/bible/service/VertexAiIntegrationTest.java`
- Tests all three pipeline prompts against Vertex AI Gemini directly
- Fails hard (not skip) if bean is null or calls fail
- Logs full exception cause chain for diagnosis
- Run: `mvn test -Dtest=VertexAiIntegrationTest -Dspring.profiles.active=integration,admin`

### Issue #189 — Vertex AI integration failing (OPEN, unresolved)
- Vertex AI Gemini HIGH-tier is not working
- curl test PASSES: `gemini-3.1-pro-preview` at `global` via REST API works
- Spring AI M6 test FAILS: gRPC transport hits non-existent endpoint for `global` location
- Setting `Transport.REST` on `VertexAI.Builder` does not resolve it — Spring AI M6 appears to ignore it
- `VertexAiGeminiChatOptions.TransportType` class exists in jar but no setter on builder
- Root cause not fully diagnosed

### application.yml current state
- `spring.ai.vertex.ai.gemini.location: ${GCP_LOCATION:global}`
- `spring.ai.vertex.ai.gemini.chat.options.model: ${GEMINI_MODEL:gemini-3.1-pro-preview}`

### LlmGatewayConfig.java current state
- Builds `VertexAiGeminiChatModel` manually (no longer uses Spring AI autoconfiguration for Vertex AI)
- Uses `VertexAI.Builder` with `Transport.REST` and `setApiEndpoint("aiplatform.googleapis.com")`
- Still failing — Spring AI gRPC transport is not being overridden

## What is next

1. **Issue #189** — Research Spring AI M6 Vertex AI REST transport support. Options:
   - Find how `VertexAiGeminiChatOptions.TransportType` is actually set
   - OR switch to the OpenAI-compatible Gemini endpoint already in `.env` (`AI_HIGH_BASE_URL_4=https://generativelanguage.googleapis.com/v1beta/openai`, `AI_HIGH_MODEL_4=gemini-flash-latest`) — add as `tier: high` provider in `application.yml`
2. **Issue #181** and **#183** — still need user verification
3. **Anthropic/Claude** — `ANTHROPIC_API_KEY` is already in `.env` — can be wired in when ready

## Behavioral issues logged
- Issue #187 comment added: dismissed user-provided URL without reading, jumped between auth approaches, made unverified claims about Spring AI internals

## Test state
- 234 tests, 4 pre-existing failures (data-dependent), 0 errors
- `VertexAiIntegrationTest` fails (expected — Vertex AI not working yet)

---

## Session continuation (2026-06-07, evening) — Recovered hung #186 architecture discussion

A prior Claude Code chat hung mid-conversation (around 22:06) while discussing the #186
Studio/Reader split. User asked to locate it via the chat export script and resume.

### What was done
- Ran `AI_Memory\chat\export_claude_sessions.py` to export sessions from `.jsonl` —
  **fixed a UnicodeEncodeError** in it (the `→` character crashes on Windows cp1252 console);
  added `sys.stdout.reconfigure(encoding='utf-8')` at the top of the script
- Located and read the hung conversation (`claude_2026-06-07_2206_f0ef0e14.md`, lines 592–832)
- Found the session ended right after user said "yes" + "update md ;)" to a final architecture
  framing — the edit was never made
- **Wrote the missing note into [STUDIO_READER_SPLIT.md](../interlinear-bible-api/docs/STUDIO_READER_SPLIT.md#L148-L182)**:
  the "Word/Grammar/Lexicon/Insight/Ask panel — standalone microservice" section, which the
  prior session had promised (table forward-reference at line 144) but never wrote

### Architecture decision now documented (was at risk of being lost)
The Word/Grammar/Lexicon/Insight/Ask right-panel (shared between Reader and Studio's Pipeline
Staging Editor preview) will be served by a **new standalone microservice with its own DB**,
populated via export from Studio (corpus-LITE.json-style handoff) — not duplicated backend code,
not a shared-DB microservice. Driven by real production concern: unexplained K8s lag/React-cache
issues that were never root-caused, plus wanting independent scaling for lexicon-lookup-heavy
traffic vs. lightweight passage serving.
- `WordInsightController` splits: AI-insight *generation* stays Studio (curation work);
  *serving* moves to the microservice
- The only remaining coupling: `verse_word.lexeme_id` ↔ microservice `lexeme.id` consistency,
  enforced at export time
- UI: one shared React component consumed by both `interlinear-bible-ui` and the Pipeline
  Staging Editor frontend
- Open question left in the doc: does Reader still need its own minimal `lexeme`/`verse_word`
  for base token rendering, or does all lexicon/insight content come from the microservice?

## What is next (added)
4. **#186 split** — when picking this back up, the move-list and microservice framing in
   `STUDIO_READER_SPLIT.md` are now the source of truth; resolve the open question about
   Reader's minimal local lexicon copy before scaffolding the microservice
- No code was committed this session (user explicitly asked not to) — only the doc edit and
  the `export_claude_sessions.py` encoding fix are uncommitted changes pending review
