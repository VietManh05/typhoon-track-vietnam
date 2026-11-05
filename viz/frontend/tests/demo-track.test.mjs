import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";
import test from "node:test";

const read = (path) => readFile(new URL(path, import.meta.url), "utf8");

test("hindcast mode compares the trained forecast with the actual track", async () => {
  const [app, map, types] = await Promise.all([
    read("../src/App.tsx"),
    read("../src/components/Map/TyphoonMap.tsx"),
    read("../src/types/index.ts"),
  ]);
  assert.ok(types.includes("actual_track?: VerificationPoint[]"));
  assert.ok(app.includes("actualTrack={isDemoMode ? stormTrack?.actual_track || [] : []}"));
  assert.ok(app.includes("fetchHindcastTrack(selectedStormId)"));
  assert.ok(map.includes("leaflet.polyline(actualCoords"));
  assert.ok(map.includes("forecast?.suggestion"), "k-NN suggestion layer is drawn");
});

test("no fabricated storm data or invented values remain", async () => {
  const [app, card, i18n] = await Promise.all([
    read("../src/App.tsx"),
    read("../src/components/StormOverviewCard.tsx"),
    read("../src/i18n/index.ts"),
  ]);
  const services = await readdir(new URL("../src/services/", import.meta.url));
  assert.ok(!services.includes("mockData.ts"));
  for (const invented of ["?? 35", "?? 970", "?? 285", "?? 20;"]) {
    assert.ok(!app.includes(invented) && !card.includes(invented), invented);
  }
  assert.ok(!i18n.includes("Dự báo chính thức NCHMF/JTWC"));
});

test("hindcast archive files match the StormTrackResponse contract", async () => {
  const index = JSON.parse(await read("../public/data/hindcast/index.json"));
  assert.ok(index.typhoons.length > 0);
  for (const item of index.typhoons) {
    assert.match(item.id, /^HC-[A-Z0-9]+$/);
    const track = JSON.parse(await read(`../public/data/hindcast/${item.id}.json`));
    assert.equal(track.storm_id, item.id);
    assert.ok(track.observations.length >= 4);
    assert.equal(track.forecast.points.length, track.actual_track.length);
    assert.ok(track.forecast.warnings.some((w) => w.startsWith("Hindcast")));
    const issue = Date.parse(track.observations.at(-1).timestamp);
    for (const point of track.actual_track) {
      assert.equal(Date.parse(point.valid_time), issue + point.horizon_hours * 3.6e6);
    }
  }
});
