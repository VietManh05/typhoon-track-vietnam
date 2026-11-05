import { storm, targets, trackItem } from "../../_lib/jma.js";
import { approvedBackend, backendJson, freshBackendForecast, freshBackendStorm } from "../../_lib/backend.js";

export async function onRequestGet({ params, env, request }) {
    const id = params.storm_id;
    if (typeof id !== "string" || !/^[A-Za-z0-9_-]{2,40}$/.test(id)) {
        return Response.json({ error: "Invalid storm ID" }, { status: 400 });
    }
    const jma = /^TC\d{4}$/.test(id)
        ? (async () => {
            const list = await targets();
            if (!list.some((item) => item.tropicalCyclone === id)) return null;
            return trackItem(await storm(id));
        })().then((data) => data, () => null)
        : Promise.resolve(null);
    const approved = await approvedBackend(env, request.url);
    if (approved) {
        const response = await backendJson(env, request.url, `/typhoons/${id}/track`, {
            serviceKey: true,
            clientIp: request.headers.get("CF-Connecting-IP"),
            timeoutMs: 12000,
        });
        const data = response?.data;
        const latest = data?.observations?.at(-1);
        if (response?.ok && data?.storm_id === id &&
            Array.isArray(data.observations) && data.observations.length > 0 &&
            freshBackendStorm({ id, name: id, latest }) &&
            freshBackendForecast(data.forecast, approved.model_version)) {
            return Response.json(data, { headers: { "Cache-Control": "no-store" } });
        }
    }
    if (!/^TC\d{4}$/.test(id)) {
        return Response.json({ error: "Approved backend track unavailable" }, { status: 503 });
    }
    try {
        const fallback = await jma;
        if (!fallback) {
            return Response.json({ error: "Storm is not active" }, { status: 404 });
        }
        return Response.json(fallback, { headers: { "Cache-Control": "no-store" } });
    } catch {
        return Response.json({ error: "JMA storm feed unavailable or stale" }, { status: 503 });
    }
}
