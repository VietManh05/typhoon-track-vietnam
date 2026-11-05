import assert from "node:assert/strict";
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { after, before, test } from "node:test";

import { build } from "esbuild";

let windyMap;
let bundleDirectory;
let receivedOptions;
const originalDocument = globalThis.document;
const originalWindow = globalThis.window;

function fakeScriptElement() {
    const listeners = new Map();
    return {
        dataset: {},
        addEventListener(event, callback) {
            listeners.set(event, callback);
        },
        dispatch(event) {
            listeners.get(event)?.();
        },
    };
}

before(async () => {
    bundleDirectory = await mkdtemp(path.join(tmpdir(), "typhoon-windy-map-"));
    const outfile = path.join(bundleDirectory, "windy-map.mjs");
    await build({
        entryPoints: [path.resolve("src/services/windyMap.ts")],
        bundle: true,
        format: "esm",
        platform: "browser",
        outfile,
    });

    const elements = new Map();
    globalThis.window = globalThis;
    globalThis.document = {
        getElementById(id) {
            return elements.get(id) ?? null;
        },
        createElement() {
            return fakeScriptElement();
        },
        head: {
            appendChild(script) {
                elements.set(script.id, script);
                queueMicrotask(() => {
                    if (script.src.includes("leaflet@1.4.0")) {
                        globalThis.window.L = { version: "1.4.0-test" };
                    } else {
                        globalThis.window.windyInit = (options, callback) => {
                            receivedOptions = options;
                            callback({
                                map: { id: "windy-map" },
                                store: { set() {} },
                                picker: { open() {}, close() {} },
                            });
                        };
                    }
                    script.dispatch("load");
                });
            },
        },
    };
    windyMap = await import(pathToFileURL(outfile).href);
});

after(async () => {
    globalThis.document = originalDocument;
    globalThis.window = originalWindow;
    await rm(bundleDirectory, { recursive: true, force: true });
});

test("Windy runtime loads the documented Leaflet version and forwards map options", async () => {
    const result = await windyMap.initializeWindyMap("test-map-key", {
        lat: 16.5,
        lon: 110,
        zoom: 6,
        overlay: "wind",
        level: "surface",
        particlesAnim: "on",
        hourFormat: "24h",
        lang: "vi",
        verbose: false,
    });

    assert.equal(result.leaflet.version, "1.4.0-test");
    assert.equal(result.api.map.id, "windy-map");
    assert.equal(receivedOptions.key, "test-map-key");
    assert.equal(receivedOptions.overlay, "wind");
});
