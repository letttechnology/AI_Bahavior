# TESTING.md — test layers, what each proves, and its blind spots

Born from a real miss (#209 split, 2026-06-26 — AI_Memory#31): a Reader Flyway migration passed
the Testcontainers boot test but **failed to start against the dev DB** (checksum mismatch), because
a fresh container has no applied history to validate against. Green integration tests are
**necessary but not sufficient**. This doc says what each layer can and cannot catch.

## Layers

1. **Unit (no DB)** — pure logic (parse→row mapping, `ProAccess`, gloss resolution). Fast.
   *Blind to:* anything needing a DB, Spring wiring, or config.

2. **Integration / Testcontainers** (fresh ephemeral Postgres, single service). Proves: Flyway
   migrates **from zero**, the schema supports the repositories/queries, datasource wiring, endpoints
   serve. *Blind to (because the DB is fresh, single-service, isolated):*
   - **Flyway VALIDATE against an already-applied history** — checksum mismatch, repair, out-of-order
     (there is no prior history in a fresh container). ← the bug that bit us.
   - **Migrations against EXISTING DATA** — NOT NULL adds, backfills, data migrations (container is empty).
   - **Two services migrating the SAME DB** — ownership/ordering conflicts (our shared content DB).
   - Real **config/profile** (it overrides datasource props), secrets, external services.
   - Cross-service contracts, the Vite proxy / CORS, the browser.

3. **e2e / cross-service** (the real running stack — importer→reader→lexis→ui against the dev DBs).
   Proves: service-to-service **contracts**, proxy routing (`/api`→reader, `/api/lexis`→lexis), auth
   across services, behaviour with **real data**. Catches: endpoint-not-ported (concordance 404),
   response-shape changes (`/available` string[]→objects), chat routing.

4. **Runtime-smoke** (start the service against the **dev DB** before calling it done; curl health +
   one real endpoint). Proves: Flyway **validate** against the persistent dev history, config, security
   filters, startup. **Required by the DoD** (`runtime-smoke (config/Flyway/security/startup)`).
   Catches: checksum mismatch, config drift, bean wiring under the real profile.

## Required gates by change type

- **Pure logic** → unit.
- **Repository / query / new endpoint** → Testcontainers integration **+ runtime-smoke**.
- **Flyway migration** → Testcontainers (migrate-from-zero) **AND runtime-smoke against a dev DB that
  already has prior migrations applied** (catches checksum/validate). If the migration alters EXISTING
  DATA, also exercise it against a DB **seeded with representative pre-migration data**, not a fresh one.
- **Shared DB across services** → the services' migration sets must be byte-identical / non-conflicting;
  the durable fix is a single sole owner (#203). Until then, changing one service's content migration
  means changing the other's identically.
- **API response-shape change** → update and verify **all consumers** in the same change (e2e /
  dependent build), not just the producer.

## The rule
Green Testcontainers tests do not make a story done. A story is done only when **runtime-smoke passes
against the dev environment** (DoD). Testcontainers cannot see persistent-state, existing-data,
config, cross-service, or browser problems — name the gate the change needs and run it.
