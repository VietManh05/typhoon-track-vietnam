const BASE = "https://www.jma.go.jp/bosai/typhoon/data/";
const STORM_ID = /^TC\d{4}$/;

async function readJson(path) {
    const response = await fetch(new URL(path, BASE), {
        headers: { Accept: "application/json" },
        signal: AbortSignal.timeout(8000),
        cf: { cacheEverything: true, cacheTtl: 180 },
    });
    if (!response.ok) throw new Error(`JMA returned HTTP ${response.status}`);
    const body = await response.text();
    if (body.length > 500_000) throw new Error("JMA response exceeds size limit");
    return JSON.parse(body);
}

function fresh(timestamp) {
    const issued = Date.parse(timestamp);
    const age = Date.now() - issued;
    return Number.isFinite(issued) && age >= -30 * 60_000 && age <= 24 * 60 * 60_000;
}

function position(value) {
    const [lat, lon] = value || [];
    if (!Number.isFinite(lat) || !Number.isFinite(lon) || lat < -90 || lat > 90 || lon < -180 || lon > 180) {
        throw new Error("JMA position is invalid");
    }
    return { lat, lon };
}

function numberOrNull(value) {
    if (value === null || value === undefined || value === "") return null;
    const result = Number(value);
    return Number.isFinite(result) ? result : null;
}

function category(value) {
    return ["TD", "TS", "STS", "TY", "STY", "SUPERTY"].includes(value) ? value : "UNK";
}

function sourceUrl(id) {
    return `https://www.jma.go.jp/bosai/map.html#contents=typhoon&elem=root&typhoon=${id}`;
}

export async function targets() {
    const items = await readJson("targetTc.json");
    if (!Array.isArray(items) || items.length > 20) throw new Error("JMA active list is invalid");
    for (const item of items) {
        if (!STORM_ID.test(item?.tropicalCyclone) || !fresh(item.issue)) {
            throw new Error("JMA active list is invalid or stale");
        }
    }
    return items;
}

export async function storm(id) {
    if (!STORM_ID.test(id)) throw new Error("Invalid storm ID");
    const items = await readJson(`${id}/specifications.json`);
    const title = Array.isArray(items) && items[0];
    const analysis = Array.isArray(items) && items.find((item) => item.advancedHours === 0);
    if (!title?.issue?.UTC || !fresh(title.issue.UTC) || !analysis?.validtime?.UTC ||
        !fresh(analysis.validtime.UTC)) {
        throw new Error("JMA storm bulletin is invalid or stale");
    }
    const { lat, lon } = position(analysis.position?.deg);
    const wind = numberOrNull(analysis.maximumWind?.sustained?.["m/s"]);
    const pressure = numberOrNull(analysis.pressure);
    if (wind !== null && (wind < 0 || wind > 150)) throw new Error("JMA wind value is invalid");
    if (pressure !== null && (pressure < 850 || pressure > 1050)) throw new Error("JMA pressure is invalid");
    return {
        id,
        title,
        items,
        latest: {
            timestamp: analysis.validtime.UTC,
            lat,
            lon,
            wind_ms: wind,
            pressure_hpa: pressure,
            intensity: category(analysis.category?.en),
            source: "JMA RSMC Tokyo (processed by Typhoon VN)",
            source_url: sourceUrl(id),
        },
    };
}

function circle(lat, lon, radiusKm) {
    const points = [];
    const latRadius = radiusKm / 111.2;
    const lonRadius = radiusKm / (111.2 * Math.max(0.1, Math.cos(lat * Math.PI / 180)));
    for (let i = 0; i <= 36; i += 1) {
        const angle = 2 * Math.PI * i / 36;
        points.push([lon + lonRadius * Math.cos(angle), lat + latRadius * Math.sin(angle)]);
    }
    return { type: "Polygon", coordinates: [points] };
}

export function activeItem(data) {
    return {
        id: data.id,
        name: data.title.name?.en || data.title.typhoonNumber || data.id,
        year: Number(data.title.issue.UTC.slice(0, 4)),
        latest: data.latest,
        observation_count: 1,
        status: "active",
    };
}

export function trackItem(data) {
    const points = data.items
        .filter((item) => Number.isInteger(item.advancedHours) && item.advancedHours > 0 && item.advancedHours <= 72)
        .map((item) => {
            const { lat, lon } = position(item.position?.deg);
            const radius = numberOrNull(item.probabilityCircleRadius?.km);
            if (!item.validtime?.UTC || !Number.isFinite(radius) || radius < 0 || radius > 1000) {
                throw new Error("JMA forecast point is invalid");
            }
            return {
                horizon_hours: item.advancedHours,
                valid_time: item.validtime.UTC,
                lat,
                lon,
                intensity: category(item.category?.en),
                radius_km: radius,
                cone: circle(lat, lon, radius),
                wind_ms: numberOrNull(item.maximumWind?.sustained?.["m/s"]),
                pressure_hpa: numberOrNull(item.pressure),
            };
        });
    return {
        storm_id: data.id,
        observations: [data.latest],
        forecast: points.length ? {
            forecast_id: `JMA-${data.id}-${Date.parse(data.title.issue.UTC)}`,
            storm_id: data.id,
            issue_time: data.title.issue.UTC,
            generated_at: data.title.issue.UTC,
            model_version: "JMA RSMC Tokyo",
            model_kind: "external guidance",
            dataset_version: "JMA live bulletin",
            sources: ["JMA RSMC Tokyo"],
            uncertainty_method: "JMA probability circle radius; Typhoon VN approximates circles for map display.",
            warnings: ["Regional JMA guidance. Follow NCHMF for official warnings in Vietnam."],
            disclaimer: `JMA data processed by Typhoon VN. Source: ${sourceUrl(data.id)}. Not an official Vietnam warning.`,
            points,
        } : null,
    };
}

export const attribution = "JMA data processed by Typhoon VN; source: https://www.jma.go.jp/bosai/typhoon/. Follow NCHMF for official warnings in Vietnam.";
