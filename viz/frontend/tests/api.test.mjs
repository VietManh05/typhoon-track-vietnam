import assert from "node:assert/strict";
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { after, before, test } from "node:test";

import { build } from "esbuild";

let api;
let bundleDirectory;
const originalFetch = globalThis.fetch;

test("session login sends scoped headers and logout clears them", async () => {
    globalThis.fetch = async (url, options) => {
        if (url === "/token") {
            assert.deepEqual(JSON.parse(options.body), { username: "review", password: "fixture" });
            return Response.json({ access_token: "short-lived-fixture", token_type: "bearer" });
        }
        assert.equal(options.headers.Authorization, "Bearer short-lived-fixture");
        return Response.json({ typhoons: [] });
    };
    await api.loginWithPassword("review", "fixture");
    await api.fetchActiveTyphoons();
    api.clearCredentials();
    assert.deepEqual(api.authHeaders(), {});
});

test("API key is verified before use and expired credentials are cleared", async () => {
    globalThis.fetch = async (url, options) => {
        assert.equal(url, "/auth/session");
        assert.equal(options.headers["X-API-Key"], "fixture-key");
        return Response.json({ authenticated: true });
    };
    await api.loginWithKey("fixture-key");
    globalThis.fetch = async () => Response.json({ typhoons: [] });
    await api.fetchActiveTyphoons();
    globalThis.fetch = async () => Response.json({}, { status: 401 });
    await assert.rejects(api.fetchActiveTyphoons(), error => error.status === 401);
    assert.deepEqual(api.authHeaders(), {});
    await assert.rejects(api.loginWithKey("invalid"));
    assert.deepEqual(api.authHeaders(), {});
});

test("a public storm response cannot authenticate an API key", async () => {
    globalThis.fetch = async (url) => {
        assert.equal(url, "/auth/session");
        return Response.json({ typhoons: [], feedAvailable: false });
    };
    await assert.rejects(api.loginWithKey("invalid"), /not verified/);
    assert.deepEqual(api.authHeaders(), {});
});

before(async () => {
    bundleDirectory = await mkdtemp(path.join(tmpdir(), "typhoon-dashboard-api-"));
    const outfile = path.join(bundleDirectory, "api.mjs");
    await build({
        entryPoints: [path.resolve("src/services/api.ts")],
        bundle: true,
        format: "esm",
        platform: "browser",
        outfile,
    });
    api = await import(pathToFileURL(outfile).href);
});

after(async () => {
    globalThis.fetch = originalFetch;
    await rm(bundleDirectory, { recursive: true, force: true });
});

test("an empty active-storm response is a successful live API result", async () => {
    globalThis.fetch = async (url) => {
        assert.equal(url, "/typhoons/active?source=jma");
        return Response.json({ typhoons: [], feedAvailable: true, disclaimer: "decision support" });
    };

    assert.deepEqual(await api.fetchActiveTyphoons(), {
        typhoons: [],
        isLive: true,
        feedAvailable: true,
    });
});

test("edge API reports a missing live storm feed without failing connectivity", async () => {
    globalThis.fetch = async () =>
        Response.json({ typhoons: [], feedAvailable: false });

    assert.deepEqual(await api.fetchActiveTyphoons(), {
        typhoons: [],
        isLive: true,
        feedAvailable: false,
    });
});

test("active-storm API failure is surfaced instead of replaced by demo data", async () => {
    globalThis.fetch = async () =>
        Response.json(
            { error: { message: "database unavailable" } },
            { status: 503 },
        );

    await assert.rejects(
        api.fetchActiveTyphoons(),
        (error) =>
            error instanceof api.DashboardApiError &&
            error.status === 503 &&
            /active storms/i.test(error.message),
    );
});

test("track network failure is surfaced instead of returning an unrelated mock storm", async () => {
    globalThis.fetch = async () => {
        throw new TypeError("connection refused");
    };

    await assert.rejects(
        api.fetchStormTrack("WP012026"),
        (error) =>
            error instanceof api.DashboardApiError &&
            error.status === undefined &&
            /WP012026/.test(error.message),
    );
});

test("Ollama requests remain same-origin and return the validated answer", async () => {
    globalThis.fetch = async (url, options) => {
        assert.equal(url, "/api/ai/chat");
        assert.equal(options.method, "POST");
        assert.deepEqual(JSON.parse(options.body), {
            question: "Nón bất định là gì?",
            history: [],
            language: "vi",
        });
        return Response.json({ answer: "Một vùng xác suất.", model: "gemma4:31b" });
    };

    assert.deepEqual(await api.askOllama("Nón bất định là gì?", [], "vi"), {
        answer: "Một vùng xác suất.",
        model: "gemma4:31b",
    });
});

test("Ollama API errors are shown without leaking response internals", async () => {
    globalThis.fetch = async () =>
        Response.json(
            { error: { code: "AI_NOT_CONFIGURED", message: "Ollama Cloud chưa được cấu hình." } },
            { status: 503 },
        );

    await assert.rejects(
        api.askOllama("Xin chào", [], "vi"),
        /Ollama Cloud chưa được cấu hình/,
    );
});
