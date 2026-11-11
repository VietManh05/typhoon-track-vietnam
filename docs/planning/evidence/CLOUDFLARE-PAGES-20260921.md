# Cloudflare Pages deployment — 2026-09-21

- **Project:** `baoviet2026`
- **Production branch:** `main`
- **Production URL:** <https://baoviet2026.pages.dev/>
- **Deployment URL:** <https://75a6fef1.baoviet2026.pages.dev/>
- **Source revision attached by Wrangler:** `5baf229`
- **Uploaded output:** `src/typhoon_vn/dashboard` — 26 files plus Pages Functions and `_headers`.

## Verification

- Frontend and Pages Functions tests: 15 passed.
- TypeScript check: pass.
- Vite 5.4.21 production build: pass, 1,922 modules transformed.
- Production dependency audit: 0 vulnerabilities (`npm audit --omit=dev --audit-level=high`).
- Production hostname: HTTP 200 with `text/html; charset=utf-8`.
- Browser QA: title, Vietnamese UI, fonts, JS/CSS, province/island data, Leaflet map and OpenTopoMap tiles loaded.
- Edge `/health`, `/typhoons/active`, weather locations/current/hourly/daily bundle: HTTP 200 JSON.
- Clean isolated-browser verification: Open-Meteo current conditions, 24 hourly points, seven daily forecasts, all six map locations, and the explicit missing-storm-feed notice rendered successfully.
- Ollama AI tab: production UI, semantic form, safety notice, suggestions, and keyboard interaction verified. `OLLAMA_API_KEY` is stored as a Pages secret; the same-origin endpoint returned HTTP 200 with `gemma4:31b`. The Worker trims secret whitespace, enforces byte-size limits, rejects foreign origins, and applies a best-effort per-client rate limit.
- Security headers are present on static and Function responses: HSTS, `nosniff`, `DENY` framing, strict-origin referrer policy, and restrictive camera/microphone/geolocation permissions.
- Weather routes cache successful results, retry one transient 429/5xx, and returned current + 24 hourly + seven daily points for all six configured locations on the acceptance pass.
- `/api/weather/nchmf` and `/subscriptions` return explicit, non-cacheable 503 JSON responses with recovery guidance; they do not silently claim unavailable integrations are live.
- Deployment uses `npm run deploy:pages`, which builds and rejects stale output unless the emitted bundle contains both the Ollama UI and same-origin API markers.
- OpenStreetMap tiles were refused by the QA browser network, then the designed OpenTopoMap fallback loaded successfully. The unavailable NCHMF route remains visibly identified and linked to the official source.

## Scope and remaining gate

This deployment combines the static frontend with a free Cloudflare Pages Functions layer for health, keyless Open-Meteo weather, and an Ollama Cloud explainer. It is not a deployment of the Python backend or a claim that trained-model forecasts, database-backed storm tracks, alert delivery, subscriptions, or NCHMF ingestion are production-ready. The storm feed is explicitly unavailable and sample tracks remain opt-in. A reviewed HTTPS Python backend and approved live data sources are still required for those capabilities.
