# Design Review: NESO Media Intelligence Pipeline

The source material covers two design iterations. Below is the architecture for each, with a code review wherever Python is present.

---

## Iteration 1 — Minimal Foundry Test App

**Design overview:** Single-file proof of concept validating that a Foundry "instant-access" model (gpt-5-mini) can be called by name with no deployment resource, using `DefaultAzureCredential` instead of an API key. Structure: env-var loader → client factory → prompt-and-call function → orchestrator.

**Code review — `main.py`:**

- **Good:** fail-fast `get_environment_variable`, typed function signatures, empty-response guard, clean separation of client creation / generation / orchestration.
- **Issues:**
  - `project_client` is created and returned but never used after extracting `openai_client` — dead reference.
  - No exception handling around the actual `responses.create()` call — auth or network failures propagate raw instead of being caught and reported cleanly.
  - Article text is hardcoded in `main()` rather than parameterised — fine for a smoke test, not reusable as-is.
  - No check that the Foundry project region matches the stated West US 3 requirement for the instant-access preview — a silent failure point if someone reuses this against a different region.

---

## Iteration 2 — Inoreader → PostgreSQL → Foundry Pipeline

**Design overview:** Event-sourced ingestion pipeline. OAuth2 authenticates against Inoreader, articles are pulled from a labelled stream, deduplicated into Postgres via a unique constraint + status state machine (`NEW → SUMMARISED/ERROR`), then processed through the same Foundry summarisation call as iteration 1.

```
Inoreader --OAuth2--> Python app --REST--> Postgres (Article table) --status=NEW--> Foundry AI --> summary
```

**Code review — `config.py`:**

- Reuses the fail-fast env pattern well; single source of truth loaded at import.
- **Design inconsistency worth flagging:** iteration 1 deliberately avoided API keys in favour of `DefaultAzureCredential`; `config.py` now requires `AZURE_AI_API_KEY` — a reversal that isn't explained or reconciled with the earlier design decision.
- Requires *all* env vars (Postgres, Inoreader, Foundry) at import time — importing `config` for any single purpose fails hard if unrelated vars are unset.

**Code review — `inoreader_auth.py`:**

- Clean OAuth2 authorization-code implementation; timeouts set on all requests.
- **CSRF gap:** the `state` parameter is a hardcoded literal (`"media-intelligence"`) rather than a random, per-session value that's verified on callback — this defeats the purpose of `state` as a CSRF defence.
- No automatic persistence/rotation of refresh tokens — the documented workflow is manual copy-paste into `.env`, which is fragile for anything beyond local testing.

**Code review — `inoreader.py`:**

- Clean class-based REST wrapper; correct URL-encoding of stream IDs; good encapsulation of auth headers.
- No retry/backoff logic, despite the pipeline being explicitly rate-limited (100 requests/day on Pro) — a transient failure burns a scarce quota unit for nothing.
- No handling of token expiry (401) — no hook to trigger `refresh_access_token`.

**Code review — `models.py`:**

- Solid dedup design: DB-level unique constraint on `inoreader_id` plus a `status` field driving a simple state machine.
- `datetime.utcnow` is deprecated in modern Python in favour of timezone-aware `datetime.now(timezone.utc)`.
- `status` is a free-text `String`, not an `Enum` — risk of value drift between code and DB over time.
- No index declared on `status`, despite it being the primary filter column in the processing query — likely fine at prototype scale, worth revisiting before volume grows.

**Code review — `article_ingestion.py`:**

- `convert_timestamp` correctly handles Inoreader's microsecond-epoch format.
- `extract_content` has a weak fallback: if no summary body exists, it substitutes the *feed origin title* as "content" — this can silently feed the LLM a near-empty article disguised as real content, with no flag raised downstream.
- `save_inoreader_article` does check-then-insert (select, then add) — a race condition under concurrent runs. It relies on the DB unique constraint as a backstop but doesn't catch the resulting `IntegrityError`, so concurrent execution would crash rather than skip gracefully.

**Code review — `auth_server.py`:**

- Reasonable for a one-time local OAuth handshake.
- Returns `access_token`/`refresh_token` directly in the JSON response body for manual copying — acceptable for localhost-only dev use, but flagged as unsafe if this pattern is ever reused beyond that context.
- `state` sent in the auth request is never validated on the callback — same CSRF weakness noted above, unaddressed at the point it matters most.

**Code review — `main.py` (pipeline orchestrator):**

- Good resilience pattern: each article is processed in its own try/except with rollback + `ERROR` status on failure, so one bad article can't crash the batch.
- Commits happen per-article rather than batched — correct but not optimised for volume.
- **Gap:** depends on `summarise_article` (`media_agent.py`) and `Base`/`engine` (`database.py`), neither of which appear in the source material — their design can't be reviewed from what's available.

---

## Open Items

- `database.py`, `tools.py`, `media_agent.py` are referenced but not shown — no design review possible until provided.
- The API-key vs. `DefaultAzureCredential` inconsistency between iterations should be resolved deliberately, not left as an artifact of copy-pasted config.
