# Deployment

Version: 0.1.0-phase7-local

This project is decision support, not an official warning system. Production acceptance remains pending until the external gates below have evidence.

## Local acceptance

Use the existing Python 3.11 environment and installed project extras. From the repository root:

```powershell
.venv\Scripts\python.exe -X utf8 -m pytest -q
.venv\Scripts\python.exe -X utf8 docs/planning/tools/validate_plan.py
.venv\Scripts\python.exe -m uvicorn typhoon_vn.api.app:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/ for the packaged dashboard and /docs for API contracts. /health is liveness; /ready checks database/model availability. Local baseline forecasts are not trained-model skill evidence.

For local development, copy `.env.example` to `.env`, keep `WEATHER_PROVIDER=open-meteo` and `CACHE_ENABLED=false`, then start FastAPI. The dashboard requests `/typhoons/active?source=jma` and `/typhoons/{id}/track?source=jma` from the same origin. These public JMA reads are rate limited. FastAPI translates the recent JMA bulletin to the same response shape as the Pages Functions. Stored observations and model inference remain on the existing protected API route when `source` is omitted. The live storm view refreshes every five minutes while the page is open. A JMA source outage returns 503 and clears the live badge.

FastAPI denies cross-origin browser reads by default. When a separate browser client is explicitly required, set `CORS_ORIGINS` to a JSON array of exact HTTPS origins, for example `["https://customer.example"]`. The Pages Functions bridge makes server-side requests and does not require CORS. Keep backend credentials in server-side secrets.

## Cloudflare Pages frontend

The production frontend is published at <https://baoviet2026.pages.dev/> through the Cloudflare Pages project `baoviet2026`. The deployment uploads the prebuilt package directory `src/typhoon_vn/dashboard`; Wrangler is pinned in `viz/frontend` so the upload workflow is reproducible.

The Pages release includes a small free-tier Functions layer. `/health` is an edge liveness endpoint, and `/api/weather/*` proxies the keyless Open-Meteo forecast API. `/typhoons/active` and `/typhoons/{storm_id}/track` read JMA's public tropical-cyclone JSON through Pages Functions. The adapter requires a recent issue time and returns `feedAvailable: false` when the source is stale or unavailable. The UI labels JMA data as processed by Typhoon VN and links to the source. JMA regional guidance is not an official Vietnam warning; follow NCHMF for that purpose. See [JMA's data terms](https://www.jma.go.jp/jma/en/copyright.html).

Without a configured backend, Pages reports `/auth/capabilities` as unavailable and returns JSON 503 from `/auth/session`, `/token`, `/alerts`, and `/ready`. The sign-in control is hidden in that state. Once `TYPHOON_BACKEND_URL` is configured, Pages forwards sign-in and authenticated alert-draft reads to FastAPI. A 200 response from `/health` means the edge site is alive; inspect `capabilities.modelForecast` and `/ready` separately. On the Python backend, `/auth/session` verifies an API key or bearer token before the UI treats sign-in as successful.

Pages can connect to a separately hosted FastAPI service using four server-side bindings: `TYPHOON_BACKEND_URL` (HTTPS origin), `TYPHOON_BACKEND_API_KEY` (encrypted secret for read-only storm API calls), `TYPHOON_APPROVED_MODEL_VERSION` and `TYPHOON_APPROVED_MODEL_REVISION` (the exact version and 64-character manifest hash approved by the operator). Pages checks `/ready` and `/version` before using backend storm data; backend track responses must carry that same trained-model version and recent observations. If a check fails, the Pages Functions keep using JMA. Browser sign-in can be forwarded to the backend without placing the service API key in frontend assets. Configure variables and encrypted secrets in Pages **Settings → Variables and Secrets**, then redeploy; see [Cloudflare's binding guidance](https://developers.cloudflare.com/pages/functions/bindings/).

This connection does not publish or approve a model by itself. The current IBTrACS candidate failed its held-out persistence comparison and is not eligible for `TYPHOON_APPROVED_MODEL_VERSION`. Alert subscriptions remain unavailable because FastAPI currently stores drafts without delivery; Pages requires `delivery: active` before forwarding sign-ups. JMA's forecast is external guidance, never a Typhoon VN model prediction. A production backend still needs HTTPS hosting, an approved model bundle, current ingestion, alert delivery and operational acceptance evidence.

### Ollama Cloud assistant

The AI tab calls the same-origin `/api/ai/chat` Pages Function. The function validates and limits the request, fixes the model server-side, adds meteorological safety instructions, and forwards only to Ollama Cloud. It deliberately returns `AI_NOT_CONFIGURED` until `OLLAMA_API_KEY` is added as a Cloudflare Pages secret for the `baoviet2026` project. Never place this key in a `VITE_*` variable, browser storage, source control, or chat messages. `OLLAMA_MODEL` is an optional server-side variable; the default is `gemma4:31b`.

The assistant explains concepts and preparedness guidance only. It must not be treated as a source of live observations, forecasts, warnings, or official NCHMF guidance.

## Production composition

`docker-compose.prod.yml` defines API, frontend, PostGIS 16, Redis and Prometheus. The optional worker profile consumes a mounted observation snapshot; it does not autonomously create an official storm archive.

Before running it, provide `POSTGRES_USER`, `POSTGRES_PASSWORD`, `MODEL_HOST_PATH` and an environment file selected by `TYPHOON_ENV_FILE` (default .env.production). Set `API_KEY` there; production requires `ALLOW_BASELINE=false`. Mount a reviewed model bundle at /app/models/promoted. Never use the synthetic smoke bundle as an operational model.

Run `docker compose -f docker-compose.prod.yml config --quiet` first. With an approved deployment target, `docker compose -f docker-compose.prod.yml up -d --build` starts the stack. These are operator instructions, not a claim that Docker was exercised in this session. API/frontend/Prometheus host ports bind loopback; configure an authenticated TLS gateway before external exposure.

Alembic uses `alembic.ini` or a supplied SQLAlchemy connection; do not assume that setting a database environment variable changes the Alembic URL automatically. Verify migrations against the designated database and retain a backup.

## External gates

Actual Docker/PostGIS/Redis operation, model accuracy/calibration, source rights, TLS/domain/hosting, monitoring destinations and alert recipients require separate evidence. Run the real PostGIS integration with `POSTGIS_TEST_URL` on a dedicated test database. See [runbook](runbook.md) and [NCHMF integration](nchmf.md).
