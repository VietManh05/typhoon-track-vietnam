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

test("merged units are labelled at the centre of their whole area", async () => {
    const { unitCentres } = await import("../src/data/vietnamLocations.ts");
    const centres = unitCentres(provinces);
    assert.equal(Object.keys(centres).length, 34);
    const at = (name) => provinces.find((p) => p.name === name).centroid;
    // Gia Lai now includes Binh Dinh: the label sits between the two old centres.
    const [lat, lon] = centres["gia-lai"];
    const [gLat, gLon] = at("GiaLai");
    const [bLat, bLon] = at("BìnhĐịnh");
    assert.ok(lat > Math.min(gLat, bLat) && lat < Math.max(gLat, bLat));
    assert.ok(lon > Math.min(gLon, bLon) && lon < Math.max(gLon, bLon));
    // Unmerged Nghe An stays on its own polygon centre.
    assert.deepEqual(centres["nghe-an"].map((v) => +v.toFixed(4)), at("NghệAn").map((v) => +v.toFixed(4)));
});

test("risk list has one row per current province, closest member first", async () => {
    const { impactsByUnit } = await import("../src/data/vietnamLocations.ts");
    const rows = provinces
        .map((p, i) => ({ id: p.id, name: p.name, centroid: p.centroid, min_forecast_distance_km: i }))
        .sort((a, b) => a.min_forecast_distance_km - b.min_forecast_distance_km);
    const units = impactsByUnit(rows);
    assert.equal(units.length, 34);
    const hue = units.find((u) => u.name === "Huế");
    assert.ok(hue.member_ids.length >= 1);
    const merged = units.find((u) => u.member_ids.length > 1);
    // Representative is the member with the smallest distance.
    const memberDistances = merged.member_ids.map((id) => rows.find((r) => r.id === id).min_forecast_distance_km);
    assert.equal(merged.min_forecast_distance_km, Math.min(...memberDistances));
});
