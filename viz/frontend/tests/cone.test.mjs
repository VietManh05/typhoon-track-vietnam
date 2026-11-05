import assert from "node:assert/strict";
import test from "node:test";

import { sweptCone } from "../src/lib/cone.ts";

const KM = 110.57; // km per degree latitude

test("swept cone is one shape that widens along the track", () => {
    // Storm moving north: 20 km at the start, 200 km at +72 h.
    const nodes = [
        { lat: 10, lon: 110, radiusKm: 20 },
        { lat: 12, lon: 110, radiusKm: 80 },
        { lat: 14, lon: 110, radiusKm: 200 },
    ];
    const { rings, outline } = sweptCone(nodes);
    assert.equal(rings.length, 2); // one hull per consecutive pair
    const lats = outline.flat().map(([lat]) => lat);
    const lons = outline.flat().map(([, lon]) => lon);
    // Outer border reaches the tip circles but never cuts through the middle.
    assert.ok(Math.min(...lats) < 10 - 15 / KM && Math.max(...lats) > 14 + 190 / KM);
    const halfWidthNorth = (Math.max(...lons) - 110) * 111.32 * Math.cos((10 * Math.PI) / 180);
    assert.ok(halfWidthNorth > 190 && halfWidthNorth < 215, `width ${halfWidthNorth}`);
    // No outline vertex lies near the shared middle circle's interior.
    for (const [lat, lon] of outline.flat()) {
        const dx = (lon - 110) * 111.32 * Math.cos((10 * Math.PI) / 180);
        const dy = (lat - 12) * KM;
        assert.ok(Math.hypot(dx, dy) > 60, "outline must not run through the cone interior");
    }
});

test("single point and invalid input degrade safely", () => {
    assert.deepEqual(sweptCone([]), { rings: [], outline: [] });
    const one = sweptCone([{ lat: 15, lon: 112, radiusKm: 50 }]);
    assert.equal(one.rings.length, 1);
    assert.ok(one.outline.length >= 1);
    assert.deepEqual(sweptCone([{ lat: NaN, lon: 1, radiusKm: 5 }]), { rings: [], outline: [] });
});
