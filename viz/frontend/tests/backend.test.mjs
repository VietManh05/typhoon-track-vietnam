import assert from "node:assert/strict";
import test from "node:test";

import { approvedActiveFeed, activeAlertDelivery, backendJson } from "../functions/_lib/backend.js";
import { onRequestGet as backendTrack } from "../functions/typhoons/[storm_id]/track.js";
import { onRequestGet as edgeReady } from "../functions/ready.js";

const originalFetch = globalThis.fetch;
const pageUrl = "https://baoviet2026.pages.dev/";
const revision = "a".repeat(64);
const env = {
    TYPHOON_BACKEND_URL: "https://api.example.test/",
    TYPHOON_BACKEND_API_KEY: "server-only-key",
    TYPHOON_APPROVED_MODEL_VERSION: "approved-v1",
    TYPHOON_APPROVED_MODEL_REVISION: revision,
};

test.afterEach(() => { globalThis.fetch = originalFetch; });

test("backend bridge rejects insecure origins and never sends its key to the browser", async () => {
    let called = false;
    globalThis.fetch = async () => { called = true; throw new Error("unexpected request"); };
    assert.equal(await backendJson({ TYPHOON_BACKEND_URL: "http://external.test/" }, pageUrl, "/health"), null);
    assert.equal(await backendJson({ TYPHOON_BACKEND_URL: pageUrl }, pageUrl, "/health"), null);
    assert.equal(called, false);
});

test("approved model bridge requires exact revision and fresh observations", async () => {
    const timestamp = new Date().toISOString();
    globalThis.fetch = async (url, options) => {
        const path = new URL(url).pathname;
        if (path === "/ready") return Response.json({ status: "ready" });
        if (path === "/version") return Response.json({
            model_kind: "trained-model",
            model_version: "approved-v1",
            model_revision: revision,
            dataset_version: "ibtracs-v04",
        });
        if (path === "/typhoons/active") {
            assert.equal(options.headers.get("X-API-Key"), "server-only-key");
            assert.equal(options.headers.get("X-Client-IP"), "203.0.113.7");
            return Response.json({ typhoons: [{
                id: "WP012026", name: "Fixture", latest: {
                    timestamp, lat: 15, lon: 120, source: "reviewed-observation",
                },
            }] });
        }
        throw new Error(`Unexpected path ${path}`);
    };
    const feed = await approvedActiveFeed(env, pageUrl, "203.0.113.7");
    assert.equal(feed.version.model_version, "approved-v1");
    assert.equal(feed.items[0].id, "WP012026");
    assert.equal(await approvedActiveFeed({ ...env, TYPHOON_APPROVED_MODEL_REVISION: "b".repeat(64) }, pageUrl, "203.0.113.7"), null);
});

test("track bridge returns only a matching approved forecast", async () => {
    const timestamp = new Date().toISOString();
    globalThis.fetch = async (url) => {
        const path = new URL(url).pathname;
        if (path === "/ready") return Response.json({ status: "ready" });
        if (path === "/version") return Response.json({
            model_kind: "trained-model", model_version: "approved-v1",
            model_revision: revision, dataset_version: "ibtracs-v04",
        });
        if (path.endsWith("/track")) return Response.json({
            storm_id: "WP012026",
            observations: [{ timestamp, lat: 15, lon: 120, source: "reviewed-observation" }],
            forecast: { model_kind: "trained-model", model_version: "approved-v1",
                issue_time: timestamp, points: [{ horizon_hours: 6, lat: 16, lon: 119 }] },
        });
        throw new Error(`Unexpected path ${path}`);
    };
    const response = await backendTrack({
        params: { storm_id: "WP012026" }, env, request: new Request(pageUrl),
    });
    assert.equal(response.status, 200);
    assert.equal((await response.json()).forecast.model_kind, "trained-model");
});

test("alert capability requires an active delivery channel", async () => {
    globalThis.fetch = async () => Response.json({ available: true, delivery: "draft-only" });
    assert.equal(await activeAlertDelivery(env, pageUrl), false);
    globalThis.fetch = async () => Response.json({ available: true, delivery: "active" });
    assert.equal(await activeAlertDelivery(env, pageUrl), true);
});

test("Pages readiness requires both a fresh approved storm feed and active alert delivery", async () => {
    const timestamp = new Date().toISOString();
    globalThis.fetch = async (url) => {
        const path = new URL(url).pathname;
        if (path === "/ready") return Response.json({ status: "ready" });
        if (path === "/version") return Response.json({
            model_kind: "trained-model", model_version: "approved-v1",
            model_revision: revision, dataset_version: "ibtracs-v04",
        });
        if (path === "/typhoons/active") return Response.json({ typhoons: [{
            id: "WP012026", name: "Fixture", latest: {
                timestamp, lat: 15, lon: 120, source: "reviewed-observation",
            },
        }] });
        if (path === "/subscriptions") return Response.json({ available: true, delivery: "active" });
        throw new Error(`Unexpected path ${path}`);
    };
    const response = await edgeReady({ env, request: new Request(pageUrl) });
    assert.equal(response.status, 200);
    assert.equal((await response.json()).status, "ready");
});
