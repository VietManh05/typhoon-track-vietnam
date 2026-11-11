import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const read = (path) => readFile(new URL(path, import.meta.url), "utf8");

test("demo map compares trained forecast with post-issue actual track", async () => {
  const [app, map, mock, types] = await Promise.all([
    read("../src/App.tsx"),
    read("../src/components/Map/TyphoonMap.tsx"),
    read("../src/services/mockData.ts"),
    read("../src/types/index.ts"),
  ]);

  assert.ok(types.includes("actual_track?: VerificationPoint[]"));
  assert.ok(app.includes("actualTrack={isDemoMode ? stormTrack?.actual_track || [] : []}"));
  assert.ok(map.includes("leaflet.polyline(actualCoords"));
  assert.ok(map.includes("Thực tế kiểm chứng"));
  assert.ok(mock.includes("MOCK_TRACK_YAGI.actual_track"));
  assert.ok(mock.includes("MOCK_TRACK_SIM.actual_track"));
});
