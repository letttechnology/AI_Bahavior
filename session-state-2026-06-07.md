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
