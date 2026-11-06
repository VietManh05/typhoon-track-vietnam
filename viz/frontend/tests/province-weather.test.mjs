import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { weatherLocationForProvince } from "../src/data/vietnamLocations.ts";

const provinces = JSON.parse(
    readFileSync(new URL("../public/data/vietnam_provinces.geojson", import.meta.url), "utf8"),
).features.map((f) => f.properties);

test("old provinces map to the merged 2025 unit by name", () => {
    const at = (name) => provinces.find((p) => p.name === name);
    const pick = (name) => weatherLocationForProvince(name, at(name).centroid).id;
    assert.equal(pick("ThừaThiênHuế"), "hue");
    assert.equal(pick("KiênGiang"), "an-giang");
    assert.equal(pick("HoàBình"), "phu-tho");
    assert.equal(pick("TháiBình"), "hung-yen");
    assert.equal(pick("HồChíMinh"), "ho-chi-minh"); // centroid fallback
});

test("every map province resolves to a weather location", () => {
    for (const p of provinces) {
        assert.ok(weatherLocationForProvince(p.name, p.centroid).id, p.name);
    }
});
