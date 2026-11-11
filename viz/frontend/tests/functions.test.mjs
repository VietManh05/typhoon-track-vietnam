import assert from "node:assert/strict";
import test from "node:test";

import { onRequest as securityMiddleware } from "../functions/_middleware.js";
import { onRequestPost as chat } from "../functions/api/ai/chat.js";
import { onRequestGet as weather } from "../functions/api/weather/[[path]].js";
import { onRequestGet as health } from "../functions/health.js";
import { onRequestGet as authCapabilities } from "../functions/auth/capabilities.js";
import { onRequestGet as authSession } from "../functions/auth/session.js";
import { onRequestGet as ready } from "../functions/ready.js";
import { onRequestPost as token } from "../functions/token.js";
import { onRequestGet as alerts } from "../functions/alerts.js";
import { onRequestGet as subscriptionStatus, onRequestPost as subscribe } from "../functions/subscriptions.js";

const originalFetch = globalThis.fetch;
const context = () => ({
    env: {},
    request: new Request("https://example.test/"),
});

test.afterEach(() => {
    globalThis.fetch = originalFetch;
});

test("security middleware applies browser hardening headers", async () => {
    const response = await securityMiddleware({
        next: async () => new Response("ok", { headers: { "Cache-Control": "no-store" } }),
    });

    assert.equal(response.headers.get("x-content-type-options"), "nosniff");
    assert.equal(response.headers.get("x-frame-options"), "DENY");
    assert.equal(response.headers.get("cache-control"), "no-store");
});

test("health reports configured and intentionally unavailable capabilities", async () => {
    globalThis.fetch = async () => { throw new Error("JMA unavailable"); };
    const response = await health({ ...context(), env: { OLLAMA_API_KEY: " secret " } });
    const payload = await response.json();

    assert.deepEqual(payload.capabilities, {
        weather: true,
        ai: true,
        stormFeed: false,
        modelForecast: false,
        modelVersion: null,
        alertDelivery: false,
    });
    assert.equal(response.headers.get("cache-control"), "no-store");
});

test("Pages never claims authenticated or forecast-ready status", async () => {
    assert.equal((await (await authCapabilities(context())).json()).available, false);
    assert.equal((await authSession(context())).status, 503);
    const response = await ready(context());
    assert.equal(response.status, 503);
    assert.equal((await response.json()).status, "not_ready");
    assert.equal((await token({
        ...context(),
        request: new Request("https://example.test/token", { method: "POST", body: "{}" }),
    })).status, 503);
    assert.equal((await alerts(context())).status, 503);
});

test("NCHMF route returns an explicit controlled unavailable response", async () => {
    const response = await weather({
        request: new Request("https://example.test/api/weather/nchmf"),
        params: { path: "nchmf" },
    });
    const payload = await response.json();

    assert.equal(response.status, 503);
    assert.equal(payload.error.code, "NCHMF_SOURCE_UNAVAILABLE");
    assert.match(payload.error.sourceUrl, /nchmf\.gov\.vn/);
});

test("weather route retries one transient provider failure", async () => {
    const request = new Request(
        "https://example.test/api/weather/current?location_id=hai-phong",
    );
    let attempts = 0;
    globalThis.fetch = async () => {
        attempts += 1;
        if (attempts === 1) return new Response("temporary", { status: 503 });
        return Response.json({
            current: {
                time: "2026-09-21T22:30",
                temperature_2m: 28,
                apparent_temperature: 31,
                weather_code: 2,
                relative_humidity_2m: 82,
                wind_speed_10m: 12,
                wind_gusts_10m: 20,
                wind_direction_10m: 90,
                surface_pressure: 1007,
                cloud_cover: 50,
            },
        });
    };

    const response = await weather({ request, params: { path: "current" } });
    assert.equal(response.status, 200);
    assert.equal(attempts, 2);
    assert.equal((await response.json()).location.id, "hai-phong");
});

test("Pages alert route fails honestly with a recovery message", async () => {
    const response = await subscribe(context());
    const payload = await response.json();

    assert.equal(response.status, 503);
    assert.equal(payload.error.code, "ALERT_DELIVERY_UNAVAILABLE");
    assert.match(payload.error.message, /NCHMF/);
});

test("Pages subscription status explains that alert service is unavailable", async () => {
    const response = await subscriptionStatus(context());
    const payload = await response.json();

    assert.equal(response.status, 503);
    assert.equal(payload.error.code, "ALERT_DELIVERY_UNAVAILABLE");
    assert.match(payload.error.message, /NCHMF/);
});

test("AI route rejects a body larger than the byte limit without Content-Length", async () => {
    const response = await chat({
        request: new Request("https://example.test/api/ai/chat", {
            method: "POST",
            headers: { Origin: "https://example.test", "CF-Connecting-IP": "192.0.2.10" },
            body: JSON.stringify({ question: "x".repeat(21000) }),
        }),
        env: { OLLAMA_API_KEY: "secret" },
    });

    assert.equal(response.status, 413);
    assert.equal((await response.json()).error.code, "PAYLOAD_TOO_LARGE");
});

test("AI route trims the secret and calls the documented Ollama endpoint", async () => {
    globalThis.fetch = async (url, options) => {
        assert.equal(url, "https://ollama.com/api/chat");
        assert.equal(options.headers.Authorization, "Bearer valid-key");
        return Response.json({
            model: "gemma4:31b",
            message: { role: "assistant", content: "An toàn trước hết." },
        });
    };

    const response = await chat({
        request: new Request("https://example.test/api/ai/chat", {
            method: "POST",
            headers: {
                Origin: "https://example.test",
                "Content-Type": "application/json",
                "CF-Connecting-IP": "192.0.2.11",
            },
            body: JSON.stringify({ question: "Tôi cần làm gì?", history: [], language: "vi" }),
        }),
        env: { OLLAMA_API_KEY: " valid-key\n" },
    });
    const payload = await response.json();

    assert.equal(response.status, 200);
    assert.equal(payload.answer, "An toàn trước hết.");
});

test("AI route applies a best-effort per-client rate limit", async () => {
    globalThis.fetch = async () =>
        Response.json({ model: "gemma4:31b", message: { content: "ok" } });

    const request = () =>
        new Request("https://example.test/api/ai/chat", {
            method: "POST",
            headers: {
                Origin: "https://example.test",
                "Content-Type": "application/json",
                "CF-Connecting-IP": "192.0.2.12",
            },
            body: JSON.stringify({ question: "test" }),
        });

    for (let index = 0; index < 10; index += 1) {
        assert.equal((await chat({ request: request(), env: { OLLAMA_API_KEY: "key" } })).status, 200);
    }
    const limited = await chat({ request: request(), env: { OLLAMA_API_KEY: "key" } });
    assert.equal(limited.status, 429);
    assert.equal(limited.headers.get("retry-after"), "60");
});


test("weather catalogue exposes all 34 current provinces and searches former names", async () => {
    const allResponse = await weather({
        request: new Request("https://example.test/api/weather/locations/search"),
        params: { path: "locations/search" },
    });
    const all = (await allResponse.json()).locations;
    assert.equal(all.length, 34);
    assert.equal(new Set(all.map((item) => item.id)).size, 34);

    const aliasResponse = await weather({
        request: new Request("https://example.test/api/weather/locations/search?q=binh%20duong"),
        params: { path: "locations/search" },
    });
    const aliasMatches = (await aliasResponse.json()).locations;
    assert.equal(aliasMatches[0].id, "ho-chi-minh");
});

test("AI route rejects scripted calls without an Origin header", async () => {
    const response = await chat({
        request: new Request("https://example.test/api/ai/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: "test" }),
        }),
        env: { OLLAMA_API_KEY: "secret" },
    });
    assert.equal(response.status, 403);
});

test("AI route uses the shared rate-limit binding when configured", async () => {
    const response = await chat({
        request: new Request("https://example.test/api/ai/chat", {
            method: "POST",
            headers: { Origin: "https://example.test", "CF-Connecting-IP": "192.0.2.13" },
            body: JSON.stringify({ question: "test" }),
        }),
        env: { OLLAMA_API_KEY: "secret", AI_RATE_LIMITER: { limit: async () => ({ success: false }) } },
    });
    assert.equal(response.status, 429);
});

test("one invalid JMA bulletin does not hide the other active storms", async () => {
    const { activeStorms } = await import("../functions/_lib/jma.js");
    const now = new Date().toISOString();
    globalThis.fetch = async (url) => {
        const path = String(url);
        if (path.endsWith("targetTc.json")) {
            return Response.json([
                { tropicalCyclone: "TC2601", issue: now },
                { tropicalCyclone: "TC2602", issue: now },
                { tropicalCyclone: "TC2603", issue: "2000-01-01T00:00:00Z" },
            ]);
        }
        if (path.includes("TC2602")) return Response.json([{ issue: { UTC: now } }]);
        return Response.json([
            { issue: { UTC: now }, name: { en: "GOOD" } },
            { advancedHours: 0, validtime: { UTC: now }, position: { deg: [15, 115] }, category: { en: "TS" } },
        ]);
    };
    const storms = await activeStorms();
    assert.deepEqual(storms.map((item) => item.id), ["TC2601"]);
});

test("AI route reports the Ollama upstream status and a specific reason", async () => {
    globalThis.fetch = async () => new Response("quota exceeded", { status: 429 });
    const response = await chat({
        request: new Request("https://example.test/api/ai/chat", {
            method: "POST",
            headers: { Origin: "https://example.test", "CF-Connecting-IP": "192.0.2.14" },
            body: JSON.stringify({ question: "test" }),
        }),
        env: { OLLAMA_API_KEY: "secret" },
    });
    const payload = await response.json();
    assert.equal(response.status, 503);
    assert.equal(payload.error.upstreamStatus, 429);
    assert.match(payload.error.message, /quota/);
});

test("AI route explains an Ollama billing (402) failure", async () => {
    globalThis.fetch = async () => new Response("payment required", { status: 402 });
    const response = await chat({
        request: new Request("https://example.test/api/ai/chat", {
            method: "POST",
            headers: { Origin: "https://example.test", "CF-Connecting-IP": "192.0.2.15" },
            body: JSON.stringify({ question: "test" }),
        }),
        env: { OLLAMA_API_KEY: "secret" },
    });
    const payload = await response.json();
    assert.equal(payload.error.upstreamStatus, 402);
    assert.match(payload.error.message, /thanh toán/);
});
